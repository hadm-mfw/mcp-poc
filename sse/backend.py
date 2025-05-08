from mcp.server import Server
from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.tools import FETCH_OFFICE_LIST, REFRESH_TOKEN
from core.handler import get_office_list
app = Server("mcp-poc")

@app.list_tools()
async def list_tools() -> list[Tool]:
    return [FETCH_OFFICE_LIST, REFRESH_TOKEN]

@app.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[TextContent | ImageContent | EmbeddedResource]:

    if name == FETCH_OFFICE_LIST.name:
        return await get_office_list(arguments)

    else:
        raise Exception(f"Tool {name} not found")
