from mcp.client.stdio import stdio_client
from mcp import ClientSession, StdioServerParameters
from asyncio import run
import json

async def connect_to_server():
    """
    Connect to an MCP server
    """
    server_params = StdioServerParameters(
        command="/path/to/uv",
        args=[
            "--directory",
            "/path/to/stdio",
            "run",
            "main.py"
        ],
        env={
            "AUTH_CREDENTIALS": "/path/to/credentials.json",
        },
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            response = await session.list_tools()
            print(response.tools)
            response = await session.call_tool("fetch_office_list", {})
            print(json.loads(response.content[0].text))

run(connect_to_server())
