# Project

Build a uv-managed Python MCP service wrapping the Luma event platform API.
API documentation: https://docs.luma.com/reference/getting-started-with-your-api

# Layout

- `src/luma_mcp/`: package and command entry point.
- `src/luma_mcp/server.py`: MCP server construction and tool registration.
- `src/luma_mcp/client/`: Luma HTTP requests, authentication, and API errors.
- `src/luma_mcp/models/`: Pydantic request and response models.
- `src/luma_mcp/tools/`: MCP tool definitions, delegating to the client.
- `tests/`: pytest tests mirroring the structure inside `src/luma_mcp/`
  (for example, `tests/client/` and `tests/test_server.py`).
- `schemas/`: versioned Luma OpenAPI snapshots used to generate models.
- `scripts/`: maintainer tools, including model regeneration.

Keep MCP concerns out of the client and HTTP concerns out of tools and models.

# Development

- Use the `uv` CLI for dependency changes; never edit dependency declarations in
  `pyproject.toml` directly. Use `uv add` and `uv add --dev` as appropriate.
- Use Pydantic for API data models when implementing them.
- Use pytest for unit tests and run them with `uv run pytest`.
- Use `just lint` and `just format-check` before reporting code changes complete.
- Use `just format` to format code and `just install-hooks` to install pre-commit hooks.
- Mock Luma requests in unit tests; do not require real credentials or network calls.
- Keep code self documenting through clear names and focused responsibilities.
- Aim for functions averaging 4–5 lines. Multiline data structures are an exception;
  preserve readability rather than compressing statements to meet a line count.
- Add comments and docstrings where they explain contracts or non-obvious choices.
- Verify changes with checks appropriate to their scope before reporting completion.

# Credentials

The HTTP service accepts the caller's Luma key in `X-Luma-API-Key` on every tool
request. Keep credentials request-scoped; never store them globally, fall back to
an environment key, or expose them as tool arguments. Never commit or log API keys.
The MCP endpoint has no service authentication initially; that can be added at
the HTTP boundary later.

# API behavior and observability

- Keep retries in the shared client, bounded by attempt count and elapsed time.
- Retry safe reads only. Respect `Retry-After`; do not replay ambiguous writes.
- Base mocked requests and responses on the checked-in OpenAPI schemas, with
  synthetic data and separate scenarios for pagination and failure behavior.
- Generate models with `just generate-models`; do not hand-edit generated files.
- Export OpenTelemetry traces and metrics through configured OTLP endpoints.
  Exclude keys, guest data, payloads, and query parameters from telemetry.
