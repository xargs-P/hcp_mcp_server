# hcp_mcp_server/hcp_auth.py
# This module handles authentication with HashiCorp Cloud Platform (HCP)
# to obtain an OAuth 2.0 access token.

import os
import httpx
from dotenv import load_dotenv
import logging
from typing import Optional, Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

HCP_AUTH_URL = "https://auth.idp.hashicorp.com/oauth/token"
HCP_API_AUDIENCE = "https://api.hashicorp.cloud"

# Global variable to cache the token (in a real scenario, consider a more robust caching/refresh mechanism)
_current_token: Optional[str] = None


async def get_hcp_access_token() -> Optional[str]:
    """
    Fetches an HCP access token using client credentials.
    Caches the token for subsequent calls within its validity period (not implemented here for simplicity).
    A more robust implementation would handle token expiration and refresh.
    """
    global _current_token
    # In a production system, you'd check token expiry before returning a cached token.
    # For this example, we fetch a new token if one isn't cached.
    # A robust solution would involve storing the token with its expiry time and refreshing it.
    # if _current_token:
    #     logger.info("Using cached HCP access token.")
    #     return _current_token

    client_id = os.getenv("HCP_CLIENT_ID")
    client_secret = os.getenv("HCP_CLIENT_SECRET")

    if not client_id or not client_secret:
        logger.error("HCP_CLIENT_ID or HCP_CLIENT_SECRET environment variables not set.")
        return None

    payload = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials",
        "audience": HCP_API_AUDIENCE,
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(HCP_AUTH_URL, data=payload)
            response.raise_for_status()  # Raises an HTTPStatusError for bad responses (4xx or 5xx)
            token_data = response.json()
            _current_token = token_data.get("access_token")
            if _current_token:
                logger.info("Successfully obtained HCP access token.")
                # You might also get 'expires_in', 'token_type' here.
                # For simplicity, we are not handling token expiry and refresh here.
            else:
                logger.error(f"Failed to retrieve access_token from response: {token_data}")
            return _current_token
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error occurred while fetching HCP token: {e.response.status_code} - {e.response.text}")
        return None
    except httpx.RequestError as e:
        logger.error(f"Request error occurred while fetching HCP token: {e}")
        return None
    except Exception as e:
        logger.error(f"An unexpected error occurred while fetching HCP token: {e}")
        return None

if __name__ == "__main__":
    # Example usage (for testing the auth module directly)
    import asyncio
    async def main_auth_test():
        token = await get_hcp_access_token()
        if token:
            print(f"Access Token: {token[:20]}...") # Print first 20 chars for brevity
        else:
            print("Failed to get access token.")
    asyncio.run(main_auth_test())