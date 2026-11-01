"""MCP tools for Luma organizations using the caller's API key."""

from mcp.server.mcpserver import Context, MCPServer
from mcp.types import ToolAnnotations

from luma_mcp.models import organizations as models
from luma_mcp.tools.context import organization_client


async def list_organization_admins(
    request: models.ListOrganizationAdminsRequest, ctx: Context
) -> models.ListOrganizationAdminsResponse:
    "List all admins for the organization."
    async with organization_client(ctx) as client:
        return await client.list_organization_admins(request)


async def list_organization_calendars(
    request: models.ListOrganizationCalendarsRequest, ctx: Context
) -> models.ListOrganizationCalendarsResponse:
    "List all calendars belonging to the organization."
    async with organization_client(ctx) as client:
        return await client.list_organization_calendars(request)


async def list_organization_events(
    request: models.ListOrganizationEventsRequest, ctx: Context
) -> models.ListOrganizationEventsResponse:
    "List all events across all calendars belonging to the organization. Events are deduplicated if they appear on multiple calendars within the organization."
    async with organization_client(ctx) as client:
        return await client.list_organization_events(request)


async def create_calendar(
    request: models.CreateCalendarRequest, ctx: Context
) -> models.CreateCalendarResponse:
    "Create a new calendar within the organization. The calendar will be managed by the API key owner."
    async with organization_client(ctx) as client:
        return await client.create_calendar(request)


async def transfer_event_calendar(
    request: models.TransferEventCalendarRequest, ctx: Context
) -> models.TransferEventCalendarResponse:
    "Transfer an event from its current managing calendar to a different calendar within the organization. The event's managing calendar changes to the destination calendar. Both the source and destination calendars must belong to the organization."
    async with organization_client(ctx) as client:
        return await client.transfer_event_calendar(request)


OPERATIONS = [
    (list_organization_admins, True),
    (list_organization_calendars, True),
    (list_organization_events, True),
    (create_calendar, False),
    (transfer_event_calendar, False),
]


def register_organizations(server: MCPServer) -> None:
    for operation, read_only in OPERATIONS:
        server.tool(
            annotations=ToolAnnotations(
                read_only_hint=read_only,
                destructive_hint=not read_only,
                idempotent_hint=read_only,
                open_world_hint=True,
            ),
        )(operation)
