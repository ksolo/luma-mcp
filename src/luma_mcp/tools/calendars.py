"""MCP tools for Luma calendars using caller-supplied HTTP credentials."""

from mcp.server.mcpserver import Context, MCPServer
from mcp.types import ToolAnnotations

from luma_mcp.models import calendars as models
from luma_mcp.tools.context import calendar_client


async def get_calendar(
    request: models.GetCalendarRequest, ctx: Context
) -> models.GetCalendarResponse:
    "Get information about the calendar."
    async with calendar_client(ctx) as client:
        return await client.get_calendar(request)


async def list_events(
    request: models.ListEventsRequest, ctx: Context
) -> models.ListEventsResponse:
    'Every event and API key on Luma is managed by a [Luma Calendar](https://help.luma.com/p/luma-calendar-overview). By default this lists the events your Calendar manages.\n\nEach event includes an `access` field. Pass `access=manage&access=view` to also return events that are listed on the Calendar but managed elsewhere — those come back with `access: "view"`, their location obfuscated to city level, and host-only fields like `meeting_url`, `registration_questions`, and `feedback_email` omitted. Private events the Calendar doesn\'t manage are never returned.'
    async with calendar_client(ctx) as client:
        return await client.list_events(request)


async def list_contact_tags(
    request: models.ListContactTagsRequest, ctx: Context
) -> models.ListContactTagsResponse:
    "List Contact Tags"
    async with calendar_client(ctx) as client:
        return await client.list_contact_tags(request)


async def list_event_tags(
    request: models.ListEventTagsRequest, ctx: Context
) -> models.ListEventTagsResponse:
    "List Event Tags"
    async with calendar_client(ctx) as client:
        return await client.list_event_tags(request)


async def list_calendar_admins(
    request: models.ListCalendarAdminsRequest, ctx: Context
) -> models.ListCalendarAdminsResponse:
    "List all admins for the calendar."
    async with calendar_client(ctx) as client:
        return await client.list_calendar_admins(request)


async def lookup_event(
    request: models.LookupEventRequest, ctx: Context
) -> models.LookupEventResponse:
    "See if an event already exists on the calendar. This is useful when figuring out if you want to submit an event to the calendar."
    async with calendar_client(ctx) as client:
        return await client.lookup_event(request)


async def list_contacts(
    request: models.ListContactsRequest, ctx: Context
) -> models.ListContactsResponse:
    "List Contacts"
    async with calendar_client(ctx) as client:
        return await client.list_contacts(request)


async def list_calendar_coupons(
    request: models.ListCalendarCouponsRequest, ctx: Context
) -> models.ListCalendarCouponsResponse:
    "List all coupons that have been created for a calendar."
    async with calendar_client(ctx) as client:
        return await client.list_calendar_coupons(request)


async def create_calendar_coupon(
    request: models.CreateCalendarCouponRequest, ctx: Context
) -> models.CreateCalendarCouponResponse:
    "Create a coupon that can be applied to any event that is managed by the calendar. Be careful not to have the same code on an event and on the calendar."
    async with calendar_client(ctx) as client:
        return await client.create_calendar_coupon(request)


async def update_calendar_coupon(
    request: models.UpdateCalendarCouponRequest, ctx: Context
) -> models.UpdateCalendarCouponResponse:
    "Update Coupon"
    async with calendar_client(ctx) as client:
        return await client.update_calendar_coupon(request)


async def import_contacts(
    request: models.ImportContactsRequest, ctx: Context
) -> models.ImportContactsResponse:
    "Import contacts to your calendar to easily invite them to events and send them newsletters."
    async with calendar_client(ctx) as client:
        return await client.import_contacts(request)


async def block_contact(
    request: models.BlockContactRequest, ctx: Context
) -> models.BlockContactResponse:
    "Block a contact so they can’t follow your calendar or join its events. They stop receiving your invites and newsletters until you restore them."
    async with calendar_client(ctx) as client:
        return await client.block_contact(request)


async def remove_contact(
    request: models.RemoveContactRequest, ctx: Context
) -> models.RemoveContactResponse:
    "Remove a contact from your calendar. They stop receiving your invites and newsletters but can follow again on their own later."
    async with calendar_client(ctx) as client:
        return await client.remove_contact(request)


async def restore_contact(
    request: models.RestoreContactRequest, ctx: Context
) -> models.RestoreContactResponse:
    "Restore a blocked or removed contact, returning them to your active contacts."
    async with calendar_client(ctx) as client:
        return await client.restore_contact(request)


async def create_contact_tag(
    request: models.CreateContactTagRequest, ctx: Context
) -> models.CreateContactTagResponse:
    "Create Contact Tag"
    async with calendar_client(ctx) as client:
        return await client.create_contact_tag(request)


async def update_contact_tag(
    request: models.UpdateContactTagRequest, ctx: Context
) -> models.UpdateContactTagResponse:
    "Update Contact Tag"
    async with calendar_client(ctx) as client:
        return await client.update_contact_tag(request)


async def delete_contact_tag(
    request: models.DeleteContactTagRequest, ctx: Context
) -> models.DeleteContactTagResponse:
    "Delete Contact Tag"
    async with calendar_client(ctx) as client:
        return await client.delete_contact_tag(request)


async def apply_contact_tag(
    request: models.ApplyContactTagRequest, ctx: Context
) -> models.ApplyContactTagResponse:
    "Apply a tag to existing calendar contacts. This will not create new contacts."
    async with calendar_client(ctx) as client:
        return await client.apply_contact_tag(request)


async def unapply_contact_tag(
    request: models.UnapplyContactTagRequest, ctx: Context
) -> models.UnapplyContactTagResponse:
    "Unapply a tag from calendar contacts. Only affects existing contacts."
    async with calendar_client(ctx) as client:
        return await client.unapply_contact_tag(request)


async def create_event_tag(
    request: models.CreateEventTagRequest, ctx: Context
) -> models.CreateEventTagResponse:
    "Create Event Tag"
    async with calendar_client(ctx) as client:
        return await client.create_event_tag(request)


async def update_event_tag(
    request: models.UpdateEventTagRequest, ctx: Context
) -> models.UpdateEventTagResponse:
    "Update Event Tag"
    async with calendar_client(ctx) as client:
        return await client.update_event_tag(request)


async def delete_event_tag(
    request: models.DeleteEventTagRequest, ctx: Context
) -> models.DeleteEventTagResponse:
    "Delete Event Tag"
    async with calendar_client(ctx) as client:
        return await client.delete_event_tag(request)


async def apply_event_tag(
    request: models.ApplyEventTagRequest, ctx: Context
) -> models.ApplyEventTagResponse:
    "Apply a tag to events on the calendar."
    async with calendar_client(ctx) as client:
        return await client.apply_event_tag(request)


async def unapply_event_tag(
    request: models.UnapplyEventTagRequest, ctx: Context
) -> models.UnapplyEventTagResponse:
    "Unapply a tag from events on the calendar."
    async with calendar_client(ctx) as client:
        return await client.unapply_event_tag(request)


async def add_event(
    request: models.AddEventRequest, ctx: Context
) -> models.AddEventResponse:
    'Add or submit an existing event (on Luma or on an external platform) to the Luma calendar. By default, events added by a calendar manager are approved immediately. Use `submission_mode: "pending"` to keep the submission pending.\n\nOn calendars with `require-manage-access`, submitting a Luma event you manage can also grant the target calendar manage access once the submission is approved.'
    async with calendar_client(ctx) as client:
        return await client.add_event(request)


async def approve_event(
    request: models.ApproveEventRequest, ctx: Context
) -> models.ApproveEventResponse:
    "Approve a pending event submission on your calendar. The event becomes visible on the calendar and the submitter is notified."
    async with calendar_client(ctx) as client:
        return await client.approve_event(request)


async def reject_event(
    request: models.RejectEventRequest, ctx: Context
) -> models.RejectEventResponse:
    "Reject a pending event submission on your calendar. The submitter is only emailed when you pass `notify_submitter: true` or a `message`."
    async with calendar_client(ctx) as client:
        return await client.reject_event(request)


async def add_calendar_admins(
    request: models.AddCalendarAdminsRequest, ctx: Context
) -> models.AddCalendarAdminsResponse:
    "Add admins to the calendar. Existing admins are skipped. On a Luma Plus calendar, adds that need more paid admin seats are rejected — add those admins in the Luma app, where the seat charge can be confirmed."
    async with calendar_client(ctx) as client:
        return await client.add_calendar_admins(request)


async def update_calendar(
    request: models.UpdateCalendarRequest, ctx: Context
) -> models.UpdateCalendarResponse:
    "Update a calendar's settings. Only the provided fields are changed. Pass null or an empty string to clear the website or a social handle."
    async with calendar_client(ctx) as client:
        return await client.update_calendar(request)


OPERATIONS = [
    (get_calendar, True),
    (list_events, True),
    (list_contact_tags, True),
    (list_event_tags, True),
    (list_calendar_admins, True),
    (lookup_event, True),
    (list_contacts, True),
    (list_calendar_coupons, True),
    (create_calendar_coupon, False),
    (update_calendar_coupon, False),
    (import_contacts, False),
    (block_contact, False),
    (remove_contact, False),
    (restore_contact, False),
    (create_contact_tag, False),
    (update_contact_tag, False),
    (delete_contact_tag, False),
    (apply_contact_tag, False),
    (unapply_contact_tag, False),
    (create_event_tag, False),
    (update_event_tag, False),
    (delete_event_tag, False),
    (apply_event_tag, False),
    (unapply_event_tag, False),
    (add_event, False),
    (approve_event, False),
    (reject_event, False),
    (add_calendar_admins, False),
    (update_calendar, False),
]


def register_calendars(server: MCPServer) -> None:
    for operation, read_only in OPERATIONS:
        server.tool(
            annotations=ToolAnnotations(
                read_only_hint=read_only,
                destructive_hint=not read_only,
                idempotent_hint=read_only,
                open_world_hint=True,
            ),
        )(operation)
