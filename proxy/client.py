from mcp.client.sse import sse_client
from mcp import ClientSession
from contextlib import asynccontextmanager
from mcp.types import TextContent, ImageContent, EmbeddedResource, Tool
import os
import json

@asynccontextmanager
async def connect_to_sse_server():
    auth_credentials = os.getenv("AUTH_CREDENTIALS")
    access_token = None
    refresh_token = None
    
    if auth_credentials:
        with open(auth_credentials, "r") as f:
            tokens = json.load(f)
            access_token = tokens["access_token"]
            refresh_token = tokens["refresh_token"]

    async with sse_client(f"{os.getenv('MCP_SSE_SERVER')}/sse", headers={f"Authorization": f"Bearer {access_token}"}) as streams:
        async with ClientSession(*streams) as session:
            await session.initialize()
            yield session

async def list_tools(session: ClientSession) -> list[Tool]:
    result = await session.list_tools()
    
    return result.tools

async def call_tool(session: ClientSession, tool_name: str, arguments: dict) -> list[TextContent | ImageContent | EmbeddedResource]:
    result = await session.call_tool(tool_name, arguments)

    if result.isError:
        raise Exception(result.content[0].text)
    
    return result.content
