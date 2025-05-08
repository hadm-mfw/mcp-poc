from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
import json

from logging import getLogger
logger = getLogger("uvicorn")

class BearerTokenMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        # Get authorization header
        auth_header = request.headers.get('Authorization')
        access_token = None
        
        if auth_header and auth_header.startswith('Bearer '):
            access_token = auth_header.split(' ')[1]

        if access_token:
            try:
                # Get the original body
                body = await request.body()
                # Parse and modify the body to include token
                body_json = json.loads(body)
                if isinstance(body_json, dict) and 'params' in body_json and 'arguments' in body_json['params']:
                    body_json['params']['arguments']['access_token'] = access_token
                
                request._body = json.dumps(body_json).encode()
            except json.JSONDecodeError:
                logger.error("Could not parse request body as JSON")

        response = await call_next(request)
        return response
