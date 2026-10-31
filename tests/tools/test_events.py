"""Ensure event tools use request headers and the typed client."""

import asyncio
from types import SimpleNamespace

import httpx
import pytest
from mcp.server.mcpserver.exceptions import ToolError

from luma_mcp.models import events as models
from luma_mcp.tools import context, events


def test_event_tool_forwards_callers_key(monkeypatch, event_case):
    seen = []

    def respond(request):
        seen.append(request.headers["x-luma-api-key"])
        return httpx.Response(200, json=event_case["response"])

    monkeypatch.setattr(
        context,
        "http_client",
        lambda: httpx.AsyncClient(transport=httpx.MockTransport(respond)),
    )
    request = getattr(models, event_case["model"] + "Request").model_validate(
        event_case["request"]
    )
    result = asyncio.run(
        getattr(events, event_case["operation"])(
            request, SimpleNamespace(headers={"x-luma-api-key": "caller-key"})
        )
    )
    assert result.model_dump(mode="json", exclude_unset=True) == event_case["response"]
    assert seen == ["caller-key"]


def test_no_environment_key_fallback(monkeypatch):
    monkeypatch.setenv("LUMA_API_KEY", "environment-key")
    with pytest.raises(ToolError, match="Missing X-Luma-API-Key"):
        context.api_key(SimpleNamespace(headers={}))
