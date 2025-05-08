import httpx
import json
from mcp.types import TextContent

async def get_office_list(arguments: dict) -> list[TextContent]:
    async with httpx.AsyncClient() as client:
        try:
            headers = {"Authorization": f"Bearer {arguments['access_token']}"}
            response = await client.get("https://expense.moneyforward.com/api/external/v1/offices", headers=headers)
            
            return [TextContent(type="text", text=json.dumps(response.json()))]
        except Exception as e:
            return [TextContent(type="text", text=str(e))]
