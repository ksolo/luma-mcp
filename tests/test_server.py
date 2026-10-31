"""Exercise MCP over HTTP, including per-request credential isolation."""

import asyncio
import json

import httpx

from luma_mcp.server import create_app
from luma_mcp.tools import context

HEADERS = {
    "Accept": "application/json, text/event-stream",
    "MCP-Protocol-Version": "2025-03-26",
}


async def rpc(http, method, params=None, key=None):
    response = await http.post(
        "/mcp",
        headers={"X-Luma-API-Key": key} if key else {},
        json={"jsonrpc": "2.0", "id": 1, "method": method, "params": params or {}},
    )
    assert response.status_code == 200, response.text
    return response.json()


def test_http_initialize_and_discovery():
    asyncio.run(discover())


async def discover():
    app = create_app()
    async with app.router.lifespan_context(app):
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app),
            base_url="http://localhost:8000",
            headers=HEADERS,
        ) as http:
            initialized = await rpc(
                http,
                "initialize",
                {
                    "protocolVersion": "2025-03-26",
                    "capabilities": {},
                    "clientInfo": {"name": "tests", "version": "1"},
                },
            )
            assert initialized["result"]["serverInfo"]["name"] == "Luma"
            tools = (await rpc(http, "tools/list"))["result"]["tools"]
    assert len(tools) == 27
    assert all("api_key" not in json.dumps(tool["inputSchema"]) for tool in tools)
    cancel = next(tool for tool in tools if tool["name"] == "cancel_event")
    assert cancel["annotations"]["destructiveHint"] is True


def test_http_tools_keep_concurrent_callers_separate(monkeypatch):
    seen = []

    def respond(request):
        seen.append(request.headers["x-luma-api-key"])
        return httpx.Response(200, json={"id": "evt-new"})

    monkeypatch.setattr(
        context,
        "http_client",
        lambda: httpx.AsyncClient(transport=httpx.MockTransport(respond)),
    )
    asyncio.run(call_concurrently())
    assert sorted(seen) == ["caller-a", "caller-b"]


async def call_concurrently():
    app = create_app()
    params = {
        "name": "create_event",
        "arguments": {
            "request": {
                "name": "Meetup",
                "start_at": "2026-11-12T00:00:00Z",
                "timezone": "America/Chicago",
            }
        },
    }
    async with app.router.lifespan_context(app):
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app),
            base_url="http://localhost:8000",
            headers=HEADERS,
        ) as http:
            results = await asyncio.gather(
                *(
                    rpc(http, "tools/call", params, key)
                    for key in ["caller-a", "caller-b"]
                )
            )
            assert all(not result["result"].get("isError") for result in results)
            missing = await rpc(http, "tools/call", params)
            assert missing["result"]["isError"] is True
