"""Typed operations for Luma organization administration."""

from luma_mcp.client.base import LumaClient
from luma_mcp.models import organizations as models


class OrganizationsClient(LumaClient):
    async def list_organization_admins(
        self, request: models.ListOrganizationAdminsRequest
    ) -> models.ListOrganizationAdminsResponse:
        return await self.request(
            "GET",
            "/v1/organizations/admins/list",
            request,
            models.ListOrganizationAdminsResponse,
        )

    async def list_organization_calendars(
        self, request: models.ListOrganizationCalendarsRequest
    ) -> models.ListOrganizationCalendarsResponse:
        return await self.request(
            "GET",
            "/v1/organizations/calendars/list",
            request,
            models.ListOrganizationCalendarsResponse,
        )

    async def list_organization_events(
        self, request: models.ListOrganizationEventsRequest
    ) -> models.ListOrganizationEventsResponse:
        return await self.request(
            "GET",
            "/v1/organizations/events/list",
            request,
            models.ListOrganizationEventsResponse,
        )

    async def create_calendar(
        self, request: models.CreateCalendarRequest
    ) -> models.CreateCalendarResponse:
        return await self.request(
            "POST",
            "/v2/organizations/calendars/create",
            request,
            models.CreateCalendarResponse,
        )

    async def transfer_event_calendar(
        self, request: models.TransferEventCalendarRequest
    ) -> models.TransferEventCalendarResponse:
        return await self.request(
            "POST",
            "/v1/organizations/events/transfer-calendar",
            request,
            models.TransferEventCalendarResponse,
        )
