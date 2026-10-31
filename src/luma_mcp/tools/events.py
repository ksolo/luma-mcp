"""MCP tools for Luma events; credentials come from HTTP request context."""

from mcp.server.mcpserver import Context, MCPServer
from mcp.types import ToolAnnotations

from luma_mcp.models import events as models
from luma_mcp.tools.context import event_client


async def get_event(
    request: models.GetEventRequest, ctx: Context
) -> models.GetEventResponse:
    'Return details about an event. For events you manage (`access: "manage"`), this includes full detail, host contact info, and a breakdown of guest counts by status. For public events you don’t manage (`access: "view"`), only the fields a regular event-page visitor could see are returned.'
    async with event_client(ctx) as client:
        return await client.get_event(request)


async def get_guest(
    request: models.GetGuestRequest, ctx: Context
) -> models.GetGuestResponse:
    "Get detailed information for an event guest by looking them up by their ID. This supports looking them up by different parameters.\n\nThis response includes `event_ticket_orders`, which includes `coupon_info` when a coupon was applied."
    async with event_client(ctx) as client:
        return await client.get_guest(request)


async def list_guests(
    request: models.ListGuestsRequest, ctx: Context
) -> models.ListGuestsResponse:
    "Get list of guests who have registered or been invited to an event.\n\nThis list response includes guest summaries and `event_tickets`, but not order-level details like `event_ticket_orders`. Use `/v1/events/guests/get` when you need detailed ticket order data for a specific guest."
    async with event_client(ctx) as client:
        return await client.list_guests(request)


async def list_event_coupons(
    request: models.ListEventCouponsRequest, ctx: Context
) -> models.ListEventCouponsResponse:
    "List all coupons that have been created for an event."
    async with event_client(ctx) as client:
        return await client.list_event_coupons(request)


async def list_ticket_types(
    request: models.ListTicketTypesRequest, ctx: Context
) -> models.ListTicketTypesResponse:
    "List all ticket types for an event"
    async with event_client(ctx) as client:
        return await client.list_ticket_types(request)


async def get_ticket_type(
    request: models.GetTicketTypeRequest, ctx: Context
) -> models.GetTicketTypeResponse:
    "Get a single ticket type by ID"
    async with event_client(ctx) as client:
        return await client.get_ticket_type(request)


async def list_blasts(
    request: models.ListBlastsRequest, ctx: Context
) -> models.ListBlastsResponse:
    "List the blasts (emails to guests) on an event, newest first. Sent blasts include `recipient_count` and `email_open_count`."
    async with event_client(ctx) as client:
        return await client.list_blasts(request)


async def get_blast(
    request: models.GetBlastRequest, ctx: Context
) -> models.GetBlastResponse:
    "Get a blast by ID."
    async with event_client(ctx) as client:
        return await client.get_blast(request)


async def create_event(
    request: models.CreateEventRequest, ctx: Context
) -> models.CreateEventResponse:
    "Create Event"
    async with event_client(ctx) as client:
        return await client.create_event(request)


async def update_event(
    request: models.UpdateEventRequest, ctx: Context
) -> models.UpdateEventResponse:
    "Update Event"
    async with event_client(ctx) as client:
        return await client.update_event(request)


async def update_guest_status(
    request: models.UpdateGuestStatusRequest, ctx: Context
) -> models.UpdateGuestStatusResponse:
    'Update a guest’s status. Set `status` to `approved` ("Going"), `declined`, `pending_approval`, or `waitlist`. Use `should_refund` to refund a paid guest when moving them out of an approved state. Use `message` to include a personal note in the email we send the guest. To send a soft invite that guests can accept, use `/v1/events/guests/send-invites` instead.'
    async with event_client(ctx) as client:
        return await client.update_guest_status(request)


async def update_guest_tickets(
    request: models.UpdateGuestTicketsRequest, ctx: Context
) -> models.UpdateGuestTicketsResponse:
    "Add or remove tickets from an existing guest. Added tickets are complimentary. Removed tickets are invalidated and, if `should_refund` is set, refunded for what the guest paid for them; otherwise no money moves. You can’t change tickets for guests with pending payment holds. Administrative ticket changes can exceed event or ticket-type capacity."
    async with event_client(ctx) as client:
        return await client.update_guest_tickets(request)


async def send_invites(
    request: models.SendInvitesRequest, ctx: Context
) -> models.SendInvitesResponse:
    "Send guests an invite to an event. We'll send an email, and if their phone number is linked to their Luma account, they'll also receive an SMS. Invites are sent in the background; the response lists any guests that will be skipped because they unsubscribed from your calendar, were removed by an admin, or blocked you."
    async with event_client(ctx) as client:
        return await client.send_invites(request)


async def add_guests(
    request: models.AddGuestsRequest, ctx: Context
) -> models.AddGuestsResponse:
    'Add guests to the event. By default, guests are added with the status "Going" (approved) and receive one ticket of the default ticket type. Use the `ticket` or `tickets` parameter to specify custom ticket assignments. Get available ticket types using `/v1/events/ticket-types/list`. Use `approval_status` to add guests as pending approval or on the waitlist instead of immediately approved. Use `registration_answers` on each guest to record answers to the event\'s registration questions — question IDs come from the `registration_questions` field of Get Event. Guests are added in the background; the response lists any guests that will be skipped because they unsubscribed from your calendar, were removed by an admin, or blocked you.'
    async with event_client(ctx) as client:
        return await client.add_guests(request)


async def add_host(
    request: models.AddHostRequest, ctx: Context
) -> models.AddHostResponse:
    "Add a host to an event. This works for both managers and check-in staff — use the access_level parameter to control permissions."
    async with event_client(ctx) as client:
        return await client.add_host(request)


async def update_host(
    request: models.UpdateHostRequest, ctx: Context
) -> models.UpdateHostResponse:
    "Update a host's permissions or visibility on an event. Use this to change a host between check-in and manager access levels. The event creator's access level cannot be changed."
    async with event_client(ctx) as client:
        return await client.update_host(request)


async def remove_host(
    request: models.RemoveHostRequest, ctx: Context
) -> models.RemoveHostResponse:
    "Remove a host from an event. The event creator cannot be removed."
    async with event_client(ctx) as client:
        return await client.remove_host(request)


async def create_coupon(
    request: models.CreateCouponRequest, ctx: Context
) -> models.CreateCouponResponse:
    "Create a coupon that can be applied when a guest is registering for an event. Restrict it to a ticket type with `event_ticket_type_id` — when that ticket type is hidden, this creates an unlock (access) code. You are not able to edit the coupon terms after it has been created."
    async with event_client(ctx) as client:
        return await client.create_coupon(request)


async def update_coupon(
    request: models.UpdateCouponRequest, ctx: Context
) -> models.UpdateCouponResponse:
    "Update Coupon"
    async with event_client(ctx) as client:
        return await client.update_coupon(request)


async def create_ticket_type(
    request: models.CreateTicketTypeRequest, ctx: Context
) -> models.CreateTicketTypeResponse:
    "Create a new ticket type for an event. Paid ticket types require the calendar to have a connected Stripe account."
    async with event_client(ctx) as client:
        return await client.create_ticket_type(request)


async def update_ticket_type(
    request: models.UpdateTicketTypeRequest, ctx: Context
) -> models.UpdateTicketTypeResponse:
    "Update an existing ticket type configuration"
    async with event_client(ctx) as client:
        return await client.update_ticket_type(request)


async def delete_ticket_type(
    request: models.DeleteTicketTypeRequest, ctx: Context
) -> models.DeleteTicketTypeResponse:
    "Soft delete a ticket type. Guests already registered with it keep their tickets. Cannot delete the last visible ticket type."
    async with event_client(ctx) as client:
        return await client.delete_ticket_type(request)


async def create_blast(
    request: models.CreateBlastRequest, ctx: Context
) -> models.CreateBlastResponse:
    "Email a message to an event's guests now, or at `scheduled_for`. Blasts go out in the background, count against the calendar's send limit, and can't be recalled once sent. Returns the blast with `status: scheduled` until it's sent. Limited to 10 blasts per 5 minutes."
    async with event_client(ctx) as client:
        return await client.create_blast(request)


async def update_blast(
    request: models.UpdateBlastRequest, ctx: Context
) -> models.UpdateBlastResponse:
    "Edit a blast. Only the fields you pass change. Before a blast is sent, everything can change. After it's sent, only `subject` and `content_md` can, which updates the post on the event page but not the emails already delivered. Blasts under review can't be edited."
    async with event_client(ctx) as client:
        return await client.update_blast(request)


async def delete_blast(
    request: models.DeleteBlastRequest, ctx: Context
) -> models.DeleteBlastResponse:
    "Delete a blast. Deleting a scheduled blast cancels the send. Deleting a sent blast removes the post from the event page, but the emails already delivered stay delivered."
    async with event_client(ctx) as client:
        return await client.delete_blast(request)


async def request_event_cancellation(
    request: models.RequestEventCancellationRequest, ctx: Context
) -> models.RequestEventCancellationResponse:
    "Request a cancellation token for an event. Canceling an event is irreversible — it notifies all guests, processes refunds, and permanently deletes the event. Because of this, cancellation uses a two-step flow: first request a token here, then pass it to /events/cancel to execute. The token expires after 15 minutes."
    async with event_client(ctx) as client:
        return await client.request_event_cancellation(request)


async def cancel_event(
    request: models.CancelEventRequest, ctx: Context
) -> models.CancelEventResponse:
    "Cancel an event. You must first call /events/cancel/request to get a cancellation_token, then pass it here. This is irreversible — the event will be deleted, all guests will be notified, and refunds will be processed if should_refund is true. For paid events, you must specify should_refund."
    async with event_client(ctx) as client:
        return await client.cancel_event(request)


OPERATIONS = [
    (get_event, True),
    (get_guest, True),
    (list_guests, True),
    (list_event_coupons, True),
    (list_ticket_types, True),
    (get_ticket_type, True),
    (list_blasts, True),
    (get_blast, True),
    (create_event, False),
    (update_event, False),
    (update_guest_status, False),
    (update_guest_tickets, False),
    (send_invites, False),
    (add_guests, False),
    (add_host, False),
    (update_host, False),
    (remove_host, False),
    (create_coupon, False),
    (update_coupon, False),
    (create_ticket_type, False),
    (update_ticket_type, False),
    (delete_ticket_type, False),
    (create_blast, False),
    (update_blast, False),
    (delete_blast, False),
    (request_event_cancellation, False),
    (cancel_event, False),
]


def register(server: MCPServer) -> None:
    for operation, read_only in OPERATIONS:
        server.tool(
            # MCP output schemas must be objects; get_event returns a top-level union.
            structured_output=operation is not get_event,
            annotations=ToolAnnotations(
                read_only_hint=read_only,
                destructive_hint=not read_only,
                idempotent_hint=read_only,
                open_world_hint=True,
            ),
        )(operation)
