"""Resolve upstream credentials for one MCP tool request."""

import json
from contextlib import asynccontextmanager

import httpx
from mcp.server.mcpserver import Context
from mcp.server.mcpserver.exceptions import ToolError
from opentelemetry import trace
from pydantic import SecretStr

from luma_mcp.client.base import LumaClient
from luma_mcp.client.calendars import CalendarsClient
from luma_mcp.client.errors import LumaError
from luma_mcp.client.events import EventsClient
from luma_mcp.client.memberships import MembershipsClient
from luma_mcp.client.webhooks import WebhooksClient

tracer = trace.get_tracer(__name__)


def api_key(ctx: Context) -> SecretStr:
    key = (ctx.headers or {}).get("x-luma-api-key", "").strip()
    if not key:
        raise ToolError("Missing X-Luma-API-Key request header.")
    return SecretStr(key)


def event_client(ctx: Context):
    return luma_client(ctx, EventsClient)


def calendar_client(ctx: Context):
    return luma_client(ctx, CalendarsClient)


def membership_client(ctx: Context):
    return luma_client(ctx, MembershipsClient)


def webhook_client(ctx: Context):
    return luma_client(ctx, WebhooksClient)


@asynccontextmanager
async def luma_client[T: LumaClient](ctx: Context, client_type: type[T]):
    key = api_key(ctx)
    try:
        with tracer.start_as_current_span("mcp.tool", record_exception=False):
            async with http_client() as http:
                yield client_type(key, http)
    except LumaError as error:
        raise ToolError(json.dumps(error.details)) from None


def http_client() -> httpx.AsyncClient:
    return httpx.AsyncClient(timeout=10, follow_redirects=False)
