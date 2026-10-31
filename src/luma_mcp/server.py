"""MCP server construction and tool registration."""

from mcp.server.mcpserver import MCPServer

mcp = MCPServer("Luma")


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
