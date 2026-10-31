"""Typed client operations for the Luma Events API."""

from luma_mcp.client.base import LumaClient
from luma_mcp.models import events as models


class EventsClient(LumaClient):
    async def get_event(
        self, request: models.GetEventRequest
    ) -> models.GetEventResponse:
        return await self.request(
            "GET", "/v1/events/get", request, models.GetEventResponse
        )

    async def get_guest(
        self, request: models.GetGuestRequest
    ) -> models.GetGuestResponse:
        return await self.request(
            "GET", "/v1/events/guests/get", request, models.GetGuestResponse
        )

    async def list_guests(
        self, request: models.ListGuestsRequest
    ) -> models.ListGuestsResponse:
        return await self.request(
            "GET", "/v1/events/guests/list", request, models.ListGuestsResponse
        )

    async def list_event_coupons(
        self, request: models.ListEventCouponsRequest
    ) -> models.ListEventCouponsResponse:
        return await self.request(
            "GET", "/v1/events/coupons/list", request, models.ListEventCouponsResponse
        )

    async def list_ticket_types(
        self, request: models.ListTicketTypesRequest
    ) -> models.ListTicketTypesResponse:
        return await self.request(
            "GET",
            "/v1/events/ticket-types/list",
            request,
            models.ListTicketTypesResponse,
        )

    async def get_ticket_type(
        self, request: models.GetTicketTypeRequest
    ) -> models.GetTicketTypeResponse:
        return await self.request(
            "GET", "/v1/events/ticket-types/get", request, models.GetTicketTypeResponse
        )

    async def list_blasts(
        self, request: models.ListBlastsRequest
    ) -> models.ListBlastsResponse:
        return await self.request(
            "GET", "/v1/events/blasts/list", request, models.ListBlastsResponse
        )

    async def get_blast(
        self, request: models.GetBlastRequest
    ) -> models.GetBlastResponse:
        return await self.request(
            "GET", "/v1/events/blasts/get", request, models.GetBlastResponse
        )

    async def create_event(
        self, request: models.CreateEventRequest
    ) -> models.CreateEventResponse:
        return await self.request(
            "POST", "/v1/events/create", request, models.CreateEventResponse
        )

    async def update_event(
        self, request: models.UpdateEventRequest
    ) -> models.UpdateEventResponse:
        return await self.request(
            "POST", "/v1/events/update", request, models.UpdateEventResponse
        )

    async def update_guest_status(
        self, request: models.UpdateGuestStatusRequest
    ) -> models.UpdateGuestStatusResponse:
        return await self.request(
            "POST",
            "/v1/events/guests/update-status",
            request,
            models.UpdateGuestStatusResponse,
        )

    async def update_guest_tickets(
        self, request: models.UpdateGuestTicketsRequest
    ) -> models.UpdateGuestTicketsResponse:
        return await self.request(
            "POST",
            "/v1/events/guests/update-tickets",
            request,
            models.UpdateGuestTicketsResponse,
        )

    async def send_invites(
        self, request: models.SendInvitesRequest
    ) -> models.SendInvitesResponse:
        return await self.request(
            "POST",
            "/v1/events/guests/send-invites",
            request,
            models.SendInvitesResponse,
        )

    async def add_guests(
        self, request: models.AddGuestsRequest
    ) -> models.AddGuestsResponse:
        return await self.request(
            "POST", "/v1/events/guests/add", request, models.AddGuestsResponse
        )

    async def add_host(self, request: models.AddHostRequest) -> models.AddHostResponse:
        return await self.request(
            "POST", "/v1/events/hosts/add", request, models.AddHostResponse
        )

    async def update_host(
        self, request: models.UpdateHostRequest
    ) -> models.UpdateHostResponse:
        return await self.request(
            "POST", "/v1/events/hosts/update", request, models.UpdateHostResponse
        )

    async def remove_host(
        self, request: models.RemoveHostRequest
    ) -> models.RemoveHostResponse:
        return await self.request(
            "POST", "/v1/events/hosts/remove", request, models.RemoveHostResponse
        )

    async def create_coupon(
        self, request: models.CreateCouponRequest
    ) -> models.CreateCouponResponse:
        return await self.request(
            "POST", "/v1/events/coupons/create", request, models.CreateCouponResponse
        )

    async def update_coupon(
        self, request: models.UpdateCouponRequest
    ) -> models.UpdateCouponResponse:
        return await self.request(
            "POST", "/v1/events/coupons/update", request, models.UpdateCouponResponse
        )

    async def create_ticket_type(
        self, request: models.CreateTicketTypeRequest
    ) -> models.CreateTicketTypeResponse:
        return await self.request(
            "POST",
            "/v1/events/ticket-types/create",
            request,
            models.CreateTicketTypeResponse,
        )

    async def update_ticket_type(
        self, request: models.UpdateTicketTypeRequest
    ) -> models.UpdateTicketTypeResponse:
        return await self.request(
            "POST",
            "/v1/events/ticket-types/update",
            request,
            models.UpdateTicketTypeResponse,
        )

    async def delete_ticket_type(
        self, request: models.DeleteTicketTypeRequest
    ) -> models.DeleteTicketTypeResponse:
        return await self.request(
            "POST",
            "/v1/events/ticket-types/delete",
            request,
            models.DeleteTicketTypeResponse,
        )

    async def create_blast(
        self, request: models.CreateBlastRequest
    ) -> models.CreateBlastResponse:
        return await self.request(
            "POST", "/v1/events/blasts/create", request, models.CreateBlastResponse
        )

    async def update_blast(
        self, request: models.UpdateBlastRequest
    ) -> models.UpdateBlastResponse:
        return await self.request(
            "POST", "/v1/events/blasts/update", request, models.UpdateBlastResponse
        )

    async def delete_blast(
        self, request: models.DeleteBlastRequest
    ) -> models.DeleteBlastResponse:
        return await self.request(
            "POST", "/v1/events/blasts/delete", request, models.DeleteBlastResponse
        )

    async def request_event_cancellation(
        self, request: models.RequestEventCancellationRequest
    ) -> models.RequestEventCancellationResponse:
        return await self.request(
            "POST",
            "/v1/events/cancel/request",
            request,
            models.RequestEventCancellationResponse,
        )

    async def cancel_event(
        self, request: models.CancelEventRequest
    ) -> models.CancelEventResponse:
        return await self.request(
            "POST", "/v1/events/cancel", request, models.CancelEventResponse
        )
