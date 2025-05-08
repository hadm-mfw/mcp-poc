from mcp.server.stdio import stdio_server
from mcp.server import Server
from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource
import asyncio

import json
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from libs.oidc import refresh_access_token
from core.tools import FETCH_OFFICE_LIST, REFRESH_TOKEN
from core.handler import get_office_list

app = Server("mcp-poc")

@app.list_tools()
async def list_tools() -> list[Tool]:
    return [FETCH_OFFICE_LIST, REFRESH_TOKEN]

@app.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[TextContent | ImageContent | EmbeddedResource]:

    auth_credentials = os.getenv("AUTH_CREDENTIALS")
    if auth_credentials:
        with open(auth_credentials, "r") as f:
            tokens = json.load(f)
            arguments['access_token'] = tokens["access_token"]
            arguments['refresh_token'] = tokens["refresh_token"]

    if name == FETCH_OFFICE_LIST.name:
        return await get_office_list(arguments)

    if name == REFRESH_TOKEN.name:
        try:
            response = await refresh_access_token(arguments["refresh_token"])
            with open(auth_credentials, "w") as f:
                json.dump({"access_token": response["access_token"], "refresh_token": response["refresh_token"]}, f, indent=2)

            return [TextContent(type="text", text=json.dumps({"message": "Token refreshed successfully"}))]
        except Exception as e:
            return [TextContent(type="text", text=str(e))]

    else:
        raise Exception(f"Tool {name} not found")

async def main():
    async with stdio_server() as streams:
        await app.run(streams[0], streams[1], app.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())
