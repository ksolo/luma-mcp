"""Luma MCP service entry point."""


def main() -> None:
    from luma_mcp.server import main as run_server

    run_server()
