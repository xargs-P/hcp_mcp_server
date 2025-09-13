import os
import httpx
from dotenv import load_dotenv

load_dotenv()

HCP_CLIENT_ID = os.getenv("HCP_CLIENT_ID")
HCP_CLIENT_SECRET = os.getenv("HCP_CLIENT_SECRET")
HCP_AUTH_URL = "https://auth.idp.hashicorp.com/oauth/token"

async def get_access_token():
    """
    Retrieves an access token from the HCP authentication server.
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(
            HCP_AUTH_URL,
            data={
                "client_id": HCP_CLIENT_ID,
                "client_secret": HCP_CLIENT_SECRET,
                "grant_type": "client_credentials",
                "audience": "https://api.hashicorp.cloud",
            },
        )
        response.raise_for_status()
        return response.json()["access_token"]
