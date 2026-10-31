# List available commands.
default:
    @just --list

# Install project and development dependencies.
sync:
    uv sync

# Run unit tests.
test:
    uv run pytest

# Check Python code for lint errors.
lint:
    uv run ruff check .

# Format Python code.
format:
    uv run ruff format .

# Check formatting without changing files.
format-check:
    uv run ruff format --check .

# Install the pre-commit hooks in this checkout.
install-hooks:
    uv run pre-commit install

# Run hooks against all tracked files.
hooks:
    uv run pre-commit run --all-files

# Launch the MCP Inspector against the package server.
inspector:
    uv run mcp dev src/luma_mcp/server.py

# Launch the service over Streamable HTTP.
serve-http:
    uv run mcp run src/luma_mcp/server.py:mcp --transport streamable-http
