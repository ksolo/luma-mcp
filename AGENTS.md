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

Credential delivery for a shared service is still an open design decision. Do not
assume a single global key or require API keys as MCP tool arguments without
discussing that design first. Never commit or log API keys.
