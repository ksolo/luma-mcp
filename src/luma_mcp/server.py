"""MCP server construction and tool registration."""

import os

import uvicorn
from mcp.server.mcpserver import MCPServer
from opentelemetry.instrumentation.asgi import OpenTelemetryMiddleware

from luma_mcp.telemetry import configure, redact_request_url
from luma_mcp.tools.calendars import register_calendars
from luma_mcp.tools.events import register_events

mcp = MCPServer("Luma")
register_events(mcp)
register_calendars(mcp)


def create_app():
    app = mcp.streamable_http_app(stateless_http=True, json_response=True)
    app.add_middleware(
        OpenTelemetryMiddleware,
        http_capture_headers_sanitize_fields=[".*"],
        server_request_hook=redact_request_url,
    )
    return app


def main() -> None:
    configure()
    uvicorn.run(
        create_app(),
        host=os.getenv("HOST", "127.0.0.1"),
        port=int(os.getenv("PORT", "8000")),
    )


if __name__ == "__main__":
    main()
