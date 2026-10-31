"""MCP tools for managing Luma webhook endpoints."""

from mcp.server.mcpserver import Context, MCPServer
from mcp.types import ToolAnnotations

from luma_mcp.models import webhooks as models
from luma_mcp.tools.context import webhook_client


async def list_webhooks(
    request: models.ListWebhooksRequest, ctx: Context
) -> models.ListWebhooksResponse:
    "List all webhook endpoints for the calendar."
    async with webhook_client(ctx) as client:
        return await client.list_webhooks(request)


async def get_webhook(
    request: models.GetWebhookRequest, ctx: Context
) -> models.GetWebhookResponse:
    "Get details about a specific webhook endpoint."
    async with webhook_client(ctx) as client:
        return await client.get_webhook(request)


async def create_webhook(
    request: models.CreateWebhookRequest, ctx: Context
) -> models.CreateWebhookResponse:
    "Create a new webhook endpoint to receive event notifications."
    async with webhook_client(ctx) as client:
        return await client.create_webhook(request)


async def update_webhook(
    request: models.UpdateWebhookRequest, ctx: Context
) -> models.UpdateWebhookResponse:
    "Update a webhook endpoint's event types or status (active/paused)."
    async with webhook_client(ctx) as client:
        return await client.update_webhook(request)


async def delete_webhook(
    request: models.DeleteWebhookRequest, ctx: Context
) -> models.DeleteWebhookResponse:
    "Delete a webhook endpoint."
    async with webhook_client(ctx) as client:
        return await client.delete_webhook(request)


OPERATIONS = [
    (list_webhooks, True),
    (get_webhook, True),
    (create_webhook, False),
    (update_webhook, False),
    (delete_webhook, False),
]


def register_webhooks(server: MCPServer) -> None:
    for operation, read_only in OPERATIONS:
        server.tool(
            annotations=ToolAnnotations(
                read_only_hint=read_only,
                destructive_hint=not read_only,
                idempotent_hint=read_only,
                open_world_hint=True,
            ),
        )(operation)
