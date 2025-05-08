
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from starlette.middleware import Middleware
from starlette.requests import Request
from starlette.responses import RedirectResponse, JSONResponse
from starlette.routing import Route, Mount
from starlette.applications import Starlette

from mcp.server.sse import SseServerTransport

import logging
logger = logging.getLogger("uvicorn")

from sse.backend import app
from libs.oidc import get_authorization_url, get_access_token, refresh_access_token
from middleware import BearerTokenMiddleware

sse = SseServerTransport("/messages/")

async def handle_sse(request):
    async with sse.connect_sse(request.scope, request.receive, request._send) as streams:
        await app.run(streams[0], streams[1], app.create_initialization_options())

async def handle_messages(scope, receive, send):
    request = Request(scope, receive)
    logger.info(f"handle_messages: {request.query_params.get('session_id')}")
    await sse.handle_post_message(scope, receive, send)

async def handle_authorization(request):
    return RedirectResponse(url=get_authorization_url())

async def handle_oidc_callback(request):
    logger.info(f"handle_oidc_callback: {request.query_params.get('code')}")
    authorization_code = request.query_params.get("code")
    response = await get_access_token(authorization_code)
    return JSONResponse(response)

async def handle_refresh_token(request: Request):
    body = await request.json()
    logger.info(f"handle_refresh_token: {body}")
    response = await refresh_access_token(body["refresh_token"])
    return JSONResponse(response)

starlette_app = Starlette(
    routes=[
        Route("/sse", endpoint=handle_sse),
        Mount("/messages", app=handle_messages),
        Route("/oauth/authorize", endpoint=handle_authorization),
        Route("/oauth/callback", endpoint=handle_oidc_callback),
        Route("/oauth/refresh", endpoint=handle_refresh_token, methods=["POST"]),
    ],
    middleware=[Middleware(BearerTokenMiddleware)]
)
