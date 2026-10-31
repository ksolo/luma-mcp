"""Check documented HTTP contracts across every Events endpoint."""

import asyncio
import json

import httpx
from pydantic import SecretStr

from luma_mcp.client.events import EventsClient
from luma_mcp.models import events as models


def test_documented_request_and_response(event_case):
    asyncio.run(call_endpoint(event_case))


async def call_endpoint(case):
    def respond(request):
        assert request.method == case["method"]
        assert request.url.host == "public-api.luma.com"
        assert request.url.path == case["path"]
        assert request.headers["x-luma-api-key"] == "synthetic-key"
        assert_payload(request, case)
        return httpx.Response(200, json=case["response"])

    async with httpx.AsyncClient(transport=httpx.MockTransport(respond)) as http:
        client = EventsClient(SecretStr("synthetic-key"), http)
        payload = getattr(models, case["model"] + "Request").model_validate(
            case["request"]
        )
        result = await getattr(client, case["operation"])(payload)
    assert result.model_dump(mode="json", exclude_unset=True) == case["response"]


def assert_payload(request, case):
    if case["method"] == "GET":
        assert dict(request.url.params) == {
            key: str(value) for key, value in case["request"].items()
        }
        assert not request.content
    else:
        assert json.loads(request.content) == case["request"]
