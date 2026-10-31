"""Typed client operations for the Luma Calendars API."""

from luma_mcp.client.base import LumaClient
from luma_mcp.models import calendars as models


class CalendarsClient(LumaClient):
    async def get_calendar(
        self, request: models.GetCalendarRequest
    ) -> models.GetCalendarResponse:
        return await self.request(
            "GET", "/v1/calendars/get", request, models.GetCalendarResponse
        )

    async def list_events(
        self, request: models.ListEventsRequest
    ) -> models.ListEventsResponse:
        return await self.request(
            "GET", "/v1/calendars/events/list", request, models.ListEventsResponse
        )

    async def list_contact_tags(
        self, request: models.ListContactTagsRequest
    ) -> models.ListContactTagsResponse:
        return await self.request(
            "GET",
            "/v1/calendars/contact-tags/list",
            request,
            models.ListContactTagsResponse,
        )

    async def list_event_tags(
        self, request: models.ListEventTagsRequest
    ) -> models.ListEventTagsResponse:
        return await self.request(
            "GET",
            "/v1/calendars/event-tags/list",
            request,
            models.ListEventTagsResponse,
        )

    async def list_calendar_admins(
        self, request: models.ListCalendarAdminsRequest
    ) -> models.ListCalendarAdminsResponse:
        return await self.request(
            "GET",
            "/v1/calendars/admins/list",
            request,
            models.ListCalendarAdminsResponse,
        )

    async def lookup_event(
        self, request: models.LookupEventRequest
    ) -> models.LookupEventResponse:
        return await self.request(
            "GET", "/v1/calendars/events/lookup", request, models.LookupEventResponse
        )

    async def list_contacts(
        self, request: models.ListContactsRequest
    ) -> models.ListContactsResponse:
        return await self.request(
            "GET", "/v1/calendars/contacts/list", request, models.ListContactsResponse
        )

    async def list_calendar_coupons(
        self, request: models.ListCalendarCouponsRequest
    ) -> models.ListCalendarCouponsResponse:
        return await self.request(
            "GET",
            "/v1/calendars/coupons/list",
            request,
            models.ListCalendarCouponsResponse,
        )

    async def create_calendar_coupon(
        self, request: models.CreateCalendarCouponRequest
    ) -> models.CreateCalendarCouponResponse:
        return await self.request(
            "POST",
            "/v1/calendars/coupons/create",
            request,
            models.CreateCalendarCouponResponse,
        )

    async def update_calendar_coupon(
        self, request: models.UpdateCalendarCouponRequest
    ) -> models.UpdateCalendarCouponResponse:
        return await self.request(
            "POST",
            "/v1/calendars/coupons/update",
            request,
            models.UpdateCalendarCouponResponse,
        )

    async def import_contacts(
        self, request: models.ImportContactsRequest
    ) -> models.ImportContactsResponse:
        return await self.request(
            "POST",
            "/v1/calendars/contacts/import",
            request,
            models.ImportContactsResponse,
        )

    async def block_contact(
        self, request: models.BlockContactRequest
    ) -> models.BlockContactResponse:
        return await self.request(
            "POST", "/v1/calendars/contacts/block", request, models.BlockContactResponse
        )

    async def remove_contact(
        self, request: models.RemoveContactRequest
    ) -> models.RemoveContactResponse:
        return await self.request(
            "POST",
            "/v1/calendars/contacts/remove",
            request,
            models.RemoveContactResponse,
        )

    async def restore_contact(
        self, request: models.RestoreContactRequest
    ) -> models.RestoreContactResponse:
        return await self.request(
            "POST",
            "/v1/calendars/contacts/restore",
            request,
            models.RestoreContactResponse,
        )

    async def create_contact_tag(
        self, request: models.CreateContactTagRequest
    ) -> models.CreateContactTagResponse:
        return await self.request(
            "POST",
            "/v1/calendars/contact-tags/create",
            request,
            models.CreateContactTagResponse,
        )

    async def update_contact_tag(
        self, request: models.UpdateContactTagRequest
    ) -> models.UpdateContactTagResponse:
        return await self.request(
            "POST",
            "/v1/calendars/contact-tags/update",
            request,
            models.UpdateContactTagResponse,
        )

    async def delete_contact_tag(
        self, request: models.DeleteContactTagRequest
    ) -> models.DeleteContactTagResponse:
        return await self.request(
            "POST",
            "/v1/calendars/contact-tags/delete",
            request,
            models.DeleteContactTagResponse,
        )

    async def apply_contact_tag(
        self, request: models.ApplyContactTagRequest
    ) -> models.ApplyContactTagResponse:
        return await self.request(
            "POST",
            "/v1/calendars/contact-tags/apply",
            request,
            models.ApplyContactTagResponse,
        )

    async def unapply_contact_tag(
        self, request: models.UnapplyContactTagRequest
    ) -> models.UnapplyContactTagResponse:
        return await self.request(
            "POST",
            "/v1/calendars/contact-tags/unapply",
            request,
            models.UnapplyContactTagResponse,
        )

    async def create_event_tag(
        self, request: models.CreateEventTagRequest
    ) -> models.CreateEventTagResponse:
        return await self.request(
            "POST",
            "/v1/calendars/event-tags/create",
            request,
            models.CreateEventTagResponse,
        )

    async def update_event_tag(
        self, request: models.UpdateEventTagRequest
    ) -> models.UpdateEventTagResponse:
        return await self.request(
            "POST",
            "/v1/calendars/event-tags/update",
            request,
            models.UpdateEventTagResponse,
        )

    async def delete_event_tag(
        self, request: models.DeleteEventTagRequest
    ) -> models.DeleteEventTagResponse:
        return await self.request(
            "POST",
            "/v1/calendars/event-tags/delete",
            request,
            models.DeleteEventTagResponse,
        )

    async def apply_event_tag(
        self, request: models.ApplyEventTagRequest
    ) -> models.ApplyEventTagResponse:
        return await self.request(
            "POST",
            "/v1/calendars/event-tags/apply",
            request,
            models.ApplyEventTagResponse,
        )

    async def unapply_event_tag(
        self, request: models.UnapplyEventTagRequest
    ) -> models.UnapplyEventTagResponse:
        return await self.request(
            "POST",
            "/v1/calendars/event-tags/unapply",
            request,
            models.UnapplyEventTagResponse,
        )

    async def add_event(
        self, request: models.AddEventRequest
    ) -> models.AddEventResponse:
        return await self.request(
            "POST", "/v1/calendars/events/add", request, models.AddEventResponse
        )

    async def approve_event(
        self, request: models.ApproveEventRequest
    ) -> models.ApproveEventResponse:
        return await self.request(
            "POST", "/v1/calendars/events/approve", request, models.ApproveEventResponse
        )

    async def reject_event(
        self, request: models.RejectEventRequest
    ) -> models.RejectEventResponse:
        return await self.request(
            "POST", "/v1/calendars/events/reject", request, models.RejectEventResponse
        )

    async def add_calendar_admins(
        self, request: models.AddCalendarAdminsRequest
    ) -> models.AddCalendarAdminsResponse:
        return await self.request(
            "POST",
            "/v1/calendars/admins/add",
            request,
            models.AddCalendarAdminsResponse,
        )

    async def update_calendar(
        self, request: models.UpdateCalendarRequest
    ) -> models.UpdateCalendarResponse:
        return await self.request(
            "POST", "/v1/calendars/update", request, models.UpdateCalendarResponse
        )
