"""Verify that the service entry point speaks MCP over stdio."""

import asyncio
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def initialize_service() -> str:
    params = StdioServerParameters(
        command=sys.executable,
        args=["-c", "from luma_mcp import main; main()"],
    )
    async with stdio_client(params) as (reader, writer):
        async with ClientSession(reader, writer) as session:
            return (await session.initialize()).server_info.name


def test_service_initializes_over_stdio() -> None:
    assert asyncio.run(asyncio.wait_for(initialize_service(), timeout=10)) == "Luma"
