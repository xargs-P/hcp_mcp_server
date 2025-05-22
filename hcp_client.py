# hcp_client.py
import httpx
import os
import time
import logging
from typing import Optional, Dict, Any, Tuple

logger = logging.getLogger(__name__)

class HcpClient:
    """
    A client for making authenticated calls to HashiCorp Cloud Platform APIs.
    Handles token acquisition and renewal.
    """
    def __init__(self, base_url: str, auth_url: str, client_id: str, client_secret: str):
        self.base_url = base_url
        self.auth_url = auth_url
        self.client_id = client_id
        self.client_secret = client_secret
        self._access_token: Optional[str] = None
        self._token_expires_at: Optional[float] = None
        self.http_client = httpx.AsyncClient(timeout=30.0) # Increased timeout

    async def _get_access_token(self) -> Optional[str]:
        """Fetches a new access token from HCP."""
        payload = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "client_credentials",
            "audience": "https://api.hashicorp.cloud",
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        try:
            response = await self.http_client.post(self.auth_url, data=payload, headers=headers)
            response.raise_for_status()  # Raise an exception for bad status codes
            token_data = response.json()
            self._access_token = token_data.get("access_token")
            expires_in = token_data.get("expires_in", 3600)  # Default to 1 hour
            self._token_expires_at = time.time() + expires_in - 60  # Refresh 60s before expiry
            logger.info("Successfully obtained HCP access token.")
            return self._access_token
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error obtaining access token: {e.response.status_code} - {e.response.text}")
            self._access_token = None
            self._token_expires_at = None
            return None
        except Exception as e:
            logger.error(f"Error obtaining access token: {e}")
            self._access_token = None
            self._token_expires_at = None
            return None

    async def ensure_authenticated(self) -> bool:
        """Ensures the client has a valid access token, refreshing if necessary."""
        if self._access_token and self._token_expires_at and time.time() < self._token_expires_at:
            return True
        logger.info("Access token expired or not present. Fetching new token.")
        return await self._get_access_token() is not None

    async def _request(
        self, method: str, endpoint: str, params: Optional[Dict[str, Any]] = None, json_data: Optional[Dict[str, Any]] = None
    ) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """
        Makes an authenticated request to the HCP API.
        Returns (response_json, error_message).
        """
        if not await self.ensure_authenticated():
            return None, "Authentication failed. Cannot make API request."

        headers = {
            "Authorization": f"Bearer {self._access_token}",
            "Accept": "application/json",
        }
        if method in ["POST", "PUT", "PATCH"]:
            headers["Content-Type"] = "application/json"

        url = f"{self.base_url}{endpoint}"
        try:
            logger.debug(f"Making {method} request to {url} with params: {params}, data: {json_data}")
            response = await self.http_client.request(
                method, url, params=params, json=json_data, headers=headers
            )
            
            if response.status_code == 204: # No Content
                return {}, None

            response.raise_for_status()
            return response.json(), None
        except httpx.HTTPStatusError as e:
            error_message = f"HCP API Error: {e.response.status_code} - {e.response.text} for {method} {url}"
            logger.error(error_message)
            return None, error_message
        except httpx.RequestError as e:
            error_message = f"HCP Request Error: {e} for {method} {url}"
            logger.error(error_message)
            return None, error_message
        except Exception as e:
            error_message = f"Unexpected error during HCP API call: {e} for {method} {url}"
            logger.exception(error_message) # Log full traceback for unexpected errors
            return None, error_message

    async def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        return await self._request("GET", endpoint, params=params)

    async def post(self, endpoint: str, data: Dict[str, Any], params: Optional[Dict[str, Any]] = None) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        return await self._request("POST", endpoint, json_data=data, params=params)

    async def put(self, endpoint: str, data: Dict[str, Any], params: Optional[Dict[str, Any]] = None) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        return await self._request("PUT", endpoint, json_data=data, params=params)

    async def patch(self, endpoint: str, data: Dict[str, Any], params: Optional[Dict[str, Any]] = None) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        return await self._request("PATCH", endpoint, json_data=data, params=params)

    async def delete(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        return await self._request("DELETE", endpoint, params=params)

    async def close(self):
        """Closes the underlying HTTP client."""
        await self.http_client.aclose()
