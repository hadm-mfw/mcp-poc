from mcp.types import Tool

REFRESH_TOKEN = Tool(
    name="refresh_token",
    description="Refresh the access token",
    inputSchema={
        "type": "object",
        # "properties": {
        #     "refresh_token": {
        #         "type": "string",
        #         "description": "The refresh token to refresh the access token"
        #     }
        # },
        # "required": ["refresh_token"]
    }
)

FETCH_OFFICE_LIST = Tool(
    name="fetch_office_list",
    description="Fetch the list of offices",
    inputSchema={
        "type": "object",
        # "properties": {
        #     "access_token": {
        #         "type": "string",
        #         "description": "The access token to fetch the office list"
        #     }
        # },
        # "required": ["access_token"]
    },
)
