# Luma MCP

An MCP server for integrating agents with the [Luma API](https://docs.luma.com/reference/getting-started-with-your-api)
to manage meetup events and guests.

The Events, Calendars, Memberships, and Webhooks APIs are implemented, including
guests, hosts, tickets, blasts, calendar settings, event submissions, contacts,
admins, tags, and coupons. Organizations and miscellaneous operations will follow
in separate PRs.

Calendar coupon tools are named `create_calendar_coupon` and `update_calendar_coupon`
to distinguish them from the event coupon tools. `list_events` lists events on the
caller's calendar, with filters for managed, listed, and external events.

Membership tools list tiers, add members, and approve or decline memberships.
For paid tiers, callers must explicitly set `skip_payment: true` when payment is
handled externally. Approving a paid member captures payment; declining cancels
an active subscription. These writes are never retried automatically.

Webhook tools create, get, list, update, and delete subscriptions. Updates can pause
or resume delivery and change subscribed event types, including `*` for all types.
Responses preserve Luma's signing secret; telemetry excludes it. This server manages
subscriptions; notification delivery goes to the URL supplied by the caller.

## Luma prerequisites

- A **Luma Plus** subscription is required for API access, according to the
  [Luma API documentation](https://docs.luma.com/reference/getting-started-with-your-api).
- Generate an API key from your calendar's [API key settings](https://luma.com/calendar/manage/api-keys).
  Each key is scoped to one calendar; generate a separate key for each calendar you manage.

The HTTP integration accepts the caller's key through the `X-Luma-API-Key`
header on each request. Keep keys out of source control and tool arguments.
Keys are used only for the current request. The service has no separate login.

## Developer setup

Install Python 3.13 or newer, [uv](https://docs.astral.sh/uv/getting-started/installation/),
and [just](https://just.systems/man/en/packages.html). Python packages and the lockfile
are managed with uv; use `uv add` for dependencies and `uv add --dev` for development tools.

From the repository root:

```sh
just sync
just install-hooks
```

The commit hooks fix Ruff lint issues where possible and format staged Python files.

## Running locally

```sh
just serve
```

This starts Streamable HTTP at `http://127.0.0.1:8000/mcp`.
`just serve-http` is an alias. Set `HOST` and `PORT` to override the listen address.

In another terminal, run `just inspector` (requires Node.js and `npx`). In the Inspector,
select Streamable HTTP, enter the URL above, and add `X-Luma-API-Key` as a custom header.
Tool arguments never include the key.

Read operations retry transient failures up to three attempts within a five-second
budget. Rate-limit waits honor `Retry-After`; longer waits are returned to the caller.
Writes are never automatically replayed. Errors include `code`, `status`, `retry_after`,
and `outcome_unknown` so callers can decide how to proceed.

## Observability

Set `OTEL_EXPORTER_OTLP_ENDPOINT` to your collector's OTLP HTTP base URL, for example
`http://localhost:4318`, to export traces and metrics. Standard signal-specific
endpoint and exporter header variables are also supported. Without an endpoint,
the service does not export telemetry. `OTEL_SERVICE_NAME` defaults to `luma-mcp`.

Traces cover incoming HTTP requests, tool execution, and outgoing Luma operations.
Metrics track upstream attempt counts, durations, and response statuses, including
rate limits. Upstream spans omit query parameters and payloads; captured HTTP headers
are redacted, including the Luma key.

## Checks

```sh
just lint
just format-check
just test
```

Use `just format` to format Python code and `just hooks` to run pre-commit against all
tracked files. GitHub Actions checks lint, formatting, and tests on pushes and pull requests.
Run `just` to list all available commands.

Tests use synthetic examples in `tests/fixtures/`, validated against
Luma's [public OpenAPI specification](https://public-api.luma.com/openapi.json).
The checked-in snapshots live in `schemas/`. Regenerate a domain's Pydantic models
with `just generate-models events`, `just generate-models calendars`,
`just generate-models memberships`, or `just generate-models webhooks`.
Calendar fixtures cover repeated query parameters, mixed event types, pagination,
and partial updates. Membership fixtures
cover free, paid, recurring, and hidden tiers, registration answers, and payment
flags. Webhook fixtures cover mixed v1/v2 routes, wildcard subscriptions, pause/resume,
and signing-secret responses. Tests never contact Luma or require a real API key.

## Project layout

```text
src/luma_mcp/
├── __init__.py    # Command entry point
├── server.py      # MCP server setup and tool registration
├── telemetry.py   # OpenTelemetry exporter configuration
├── client/        # Luma HTTP client and authentication
├── models/        # Pydantic request and response models
└── tools/         # MCP tool definitions
tests/            # Mirrors the structure inside src/luma_mcp/
schemas/          # OpenAPI snapshots
scripts/          # Model regeneration
```

See [AGENTS.md](AGENTS.md) for development conventions.
