"""Typed operations for Luma membership tiers and members."""

from luma_mcp.client.base import LumaClient
from luma_mcp.models import memberships as models


class MembershipsClient(LumaClient):
    async def list_membership_tiers(
        self,
        request: models.ListMembershipTiersRequest,
    ) -> models.ListMembershipTiersResponse:
        return await self.request(
            "GET",
            "/v1/memberships/tiers/list",
            request,
            models.ListMembershipTiersResponse,
        )

    async def add_member_to_tier(
        self,
        request: models.AddMemberToTierRequest,
    ) -> models.AddMemberToTierResponse:
        return await self.request(
            "POST",
            "/v1/memberships/members/add",
            request,
            models.AddMemberToTierResponse,
        )

    async def update_member_status(
        self,
        request: models.UpdateMemberStatusRequest,
    ) -> models.UpdateMemberStatusResponse:
        return await self.request(
            "POST",
            "/v1/memberships/members/update-status",
            request,
            models.UpdateMemberStatusResponse,
        )
