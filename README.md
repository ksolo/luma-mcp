# Luma MCP

An MCP server for integrating agents with the [Luma API](https://docs.luma.com/reference/getting-started-with-your-api)
to manage meetup events and guests.

The server currently starts, but Luma API tools and caller-supplied credential handling
are still under development.

## Luma prerequisites

- A **Luma Plus** subscription is required for API access, according to the
  [Luma API documentation](https://docs.luma.com/reference/getting-started-with-your-api).
- Generate an API key from your calendar's [API key settings](https://luma.com/calendar/manage/api-keys).
  Each key is scoped to one calendar; generate a separate key for each calendar you manage.

The intended HTTP integration accepts the caller's key through the `X-Luma-API-Key`
header on each request. Keep keys out of source control and tool arguments.

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
just serve-http
```

This starts the service over Streamable HTTP, the transport intended for caller-supplied
headers. `just serve` currently starts the stdio transport, which cannot receive HTTP headers.

`just inspector` launches the MCP Inspector using the current stdio setup and requires
Node.js and `npx`. HTTP Inspector configuration is still pending.

## Checks

```sh
just lint
just format-check
just test
```

Use `just format` to format Python code and `just hooks` to run pre-commit against all
tracked files. GitHub Actions checks lint, formatting, and tests on pushes and pull requests.
Run `just` to list all available commands.

## Project layout

```text
src/luma_mcp/
├── __init__.py    # Command entry point
├── server.py      # MCP server setup and tool registration
├── client/        # Luma HTTP client and authentication
├── models/        # Pydantic request and response models
└── tools/         # MCP tool definitions
tests/            # Mirrors the structure inside src/luma_mcp/
```

See [AGENTS.md](AGENTS.md) for development conventions.
