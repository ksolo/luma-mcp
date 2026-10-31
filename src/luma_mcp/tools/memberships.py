"""MCP membership tools using the caller's request-scoped Luma key."""

from mcp.server.mcpserver import Context, MCPServer
from mcp.types import ToolAnnotations

from luma_mcp.models import memberships as models
from luma_mcp.tools.context import membership_client


async def list_membership_tiers(
    request: models.ListMembershipTiersRequest,
    ctx: Context,
) -> models.ListMembershipTiersResponse:
    """List the calendar's membership tiers, including hidden ones, one page at a time."""
    async with membership_client(ctx) as client:
        return await client.list_membership_tiers(request)


async def add_member_to_tier(
    request: models.AddMemberToTierRequest,
    ctx: Context,
) -> models.AddMemberToTierResponse:
    """Add a member to a tier. Paid tiers require explicit skip_payment=true for payment handled externally."""
    async with membership_client(ctx) as client:
        return await client.add_member_to_tier(request)


async def update_member_status(
    request: models.UpdateMemberStatusRequest,
    ctx: Context,
) -> models.UpdateMemberStatusResponse:
    """Approve or decline a member. Approval captures paid-tier payments; declining cancels active subscriptions."""
    async with membership_client(ctx) as client:
        return await client.update_member_status(request)


OPERATIONS = [
    (list_membership_tiers, True),
    (add_member_to_tier, False),
    (update_member_status, False),
]


def register_memberships(server: MCPServer) -> None:
    for operation, read_only in OPERATIONS:
        server.tool(
            annotations=ToolAnnotations(
                read_only_hint=read_only,
                destructive_hint=not read_only,
                idempotent_hint=read_only,
                open_world_hint=True,
            ),
        )(operation)
