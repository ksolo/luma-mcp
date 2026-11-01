"""Exercise registered organization tools through MCP's HTTP boundary."""

import asyncio
import json

import httpx
import pytest

from luma_mcp.server import create_app
from luma_mcp.tools import context


def test_organization_tool_forwards_callers_key(monkeypatch, organization_case):
    seen = []

    def respond(request):
        seen.append(request.headers["x-luma-api-key"])
        return httpx.Response(200, json=organization_case["response"])

    monkeypatch.setattr(
        context,
        "http_client",
        lambda: httpx.AsyncClient(transport=httpx.MockTransport(respond)),
    )
    result = asyncio.run(call_organization_tool(organization_case))
    assert not result.get("isError"), result
    assert result["structuredContent"] == organization_case["response"]
    assert seen == ["caller-key"]


async def call_organization_tool(case, key="caller-key"):
    app = create_app()
    async with app.router.lifespan_context(app):
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app),
            base_url="http://localhost:8000",
            headers={
                "Accept": "application/json, text/event-stream",
                "MCP-Protocol-Version": "2025-03-26",
                **({"X-Luma-API-Key": key} if key else {}),
            },
        ) as http:
            response = await http.post(
                "/mcp",
                json={
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "tools/call",
                    "params": {
                        "name": case["operation"],
                        "arguments": {"request": case["request"]},
                    },
                },
            )
    assert response.status_code == 200, response.text
    return response.json()["result"]


@pytest.mark.parametrize("status,code", [(429, "rate_limited"), (403, "forbidden")])
def test_organization_tool_returns_sanitized_upstream_error(monkeypatch, status, code):
    monkeypatch.setattr(
        context,
        "http_client",
        lambda: httpx.AsyncClient(
            transport=httpx.MockTransport(
                lambda request: httpx.Response(
                    status,
                    headers={"Retry-After": "60"} if status == 429 else {},
                    text="private-upstream-data",
                )
            ),
        ),
    )
    result = asyncio.run(
        call_organization_tool({"operation": "list_organization_admins", "request": {}})
    )
    assert result["isError"] is True
    error = json.loads(result["content"][0]["text"].partition(": ")[2])
    assert error["code"] == code and error["status"] == status
    assert error["retry_after"] == (60 if status == 429 else None)
    assert "private-upstream-data" not in str(result)


def test_missing_organization_key_never_opens_upstream_client(monkeypatch):
    def unexpected_client():
        raise AssertionError("No upstream client should open without a caller key")

    monkeypatch.setattr(context, "http_client", unexpected_client)
    result = asyncio.run(
        call_organization_tool(
            {"operation": "list_organization_admins", "request": {}}, key=None
        )
    )
    assert result["isError"] is True
    assert "Missing X-Luma-API-Key" in result["content"][0]["text"]


@pytest.mark.parametrize(
    "operation,payload",
    [
        ("create_calendar", {"name": "New Community"}),
        (
            "transfer_event_calendar",
            {"event_id": "evt-meetup", "calendar_id": "cal-labs"},
        ),
    ],
)
def test_organization_writes_are_not_replayed(monkeypatch, operation, payload):
    seen = []

    def respond(request):
        seen.append(request)
        return httpx.Response(503)

    monkeypatch.setattr(
        context,
        "http_client",
        lambda: httpx.AsyncClient(transport=httpx.MockTransport(respond)),
    )
    result = asyncio.run(
        call_organization_tool({"operation": operation, "request": payload})
    )
    assert result["isError"] is True and len(seen) == 1
    error = json.loads(result["content"][0]["text"].partition(": ")[2])
    assert error["outcome_unknown"] is True
