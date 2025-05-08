import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mcp.server import Server
from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
import httpx
import json

from proxy.client import connect_to_sse_server, list_tools, call_tool

@asynccontextmanager
async def handle_lifespan(server: Server) -> AsyncIterator[dict]:
    async with connect_to_sse_server() as session:
        yield {"session": session}

app = Server("mcp-proxy", lifespan=handle_lifespan)

@app.list_tools()
async def handle_list_tools() -> list[Tool]:
    ctx = app.request_context
    session = ctx.lifespan_context["session"]
    
    return await list_tools(session)

@app.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[TextContent | ImageContent | EmbeddedResource]:

    if name == "refresh_token":
        auth_credentials = os.getenv("AUTH_CREDENTIALS")
        refresh_token = None
        if auth_credentials:
            with open(auth_credentials, "r") as f:
                tokens = json.load(f)
                refresh_token = tokens["refresh_token"]

        async with httpx.AsyncClient() as client:
            body = {
                "refresh_token": refresh_token
            }
            response = await client.post(f"{os.getenv('MCP_SSE_SERVER')}/oauth/refresh", json=body)
            tokens = response.json()
            with open(auth_credentials, "w") as f:
                json.dump(tokens, f, indent=2)

        return [TextContent(type="text", text=json.dumps({"message": "Token refreshed successfully"}))]

    ctx = app.request_context
    session = ctx.lifespan_context["session"]

    return await call_tool(session, name, arguments)
