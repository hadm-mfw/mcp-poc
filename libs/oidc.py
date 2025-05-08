import os
from dotenv import load_dotenv
import httpx
load_dotenv(override=True)

def get_authorization_url():

    client_id = os.getenv("CLIENT_ID", None)
    idp_url = os.getenv("IDP_URL", None)
    redirect_url = os.getenv("REDIRECT_URL", None)

    scope = [
        "office_setting:write",
        "user_setting:write",
        "transaction:write",
        "report:write",
        "account:write",
        "public_resource:read",
    ]
    scope = "+".join(scope)

    return f"{idp_url}/authorize?client_id={client_id}&redirect_uri={redirect_url}&response_type=code&scope={scope}"
    
async def get_access_token(authorization_code: str):
    client_id = os.getenv("CLIENT_ID", None)
    client_secret = os.getenv("CLIENT_SECRET", None)
    idp_url = os.getenv("IDP_URL", None)
    redirect_url = os.getenv("REDIRECT_URL", None)
    
    async with httpx.AsyncClient() as client:
        try:
            data = {
                "client_id": client_id,
                "client_secret": client_secret,
                "redirect_uri": redirect_url,
                "grant_type": "authorization_code",
                "code": authorization_code
            }
            response = await client.post(f"{idp_url}/token", data=data)
            
            return response.json()
        except Exception as e:
            return {"error": str(e)}
            
async def refresh_access_token(refresh_token: str):
    client_id = os.getenv("CLIENT_ID", None)
    client_secret = os.getenv("CLIENT_SECRET", None)
    idp_url = os.getenv("IDP_URL", None)

    async with httpx.AsyncClient() as client:
        try:
            data = {
                "client_id": client_id,
                "client_secret": client_secret,
                "grant_type": "refresh_token",
                "refresh_token": refresh_token
            }
            response = await client.post(f"{idp_url}/token", data=data)
            
            return response.json()
        except Exception as e:
            return {"error": str(e)}

