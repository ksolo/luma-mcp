"""Resolve upstream credentials for one MCP tool request."""

import json
from contextlib import asynccontextmanager

import httpx
from mcp.server.mcpserver import Context
from mcp.server.mcpserver.exceptions import ToolError
from opentelemetry import trace
from pydantic import SecretStr

from luma_mcp.client.errors import LumaError
from luma_mcp.client.events import EventsClient

tracer = trace.get_tracer(__name__)


def api_key(ctx: Context) -> SecretStr:
    key = (ctx.headers or {}).get("x-luma-api-key", "").strip()
    if not key:
        raise ToolError("Missing X-Luma-API-Key request header.")
    return SecretStr(key)


@asynccontextmanager
async def event_client(ctx: Context):
    key = api_key(ctx)
    try:
        with tracer.start_as_current_span("mcp.tool", record_exception=False):
            async with http_client() as http:
                yield EventsClient(key, http)
    except LumaError as error:
        raise ToolError(json.dumps(error.details)) from None


def http_client() -> httpx.AsyncClient:
    return httpx.AsyncClient(timeout=10, follow_redirects=False)
