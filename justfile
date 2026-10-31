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
    npx @modelcontextprotocol/inspector

# Launch the service over Streamable HTTP.
serve:
    uv run luma-mcp

# Launch the service over Streamable HTTP.
serve-http: serve

# Regenerate Pydantic models from a checked-in schema snapshot.
generate-models domain="events":
    uv run python scripts/generate_models.py {{domain}}
    uv run ruff check --fix src/luma_mcp/models/{{domain}}.py
    uv run ruff format src/luma_mcp/models/{{domain}}.py
