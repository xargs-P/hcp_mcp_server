# hcp_mcp_server/hcp_api_clients/base_client.py
# Base utilities for making authenticated calls to HCP APIs.

import httpx
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

HCP_API_BASE_URL = "https://api.cloud.hashicorp.com"

async def make_hcp_api_request(
    http_client: httpx.AsyncClient,
    method: str,
    endpoint: str,
    token: str,
    params: Optional[Dict[str, Any]] = None,
    json_data: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Makes an authenticated request to the HCP API.

    Args:
        http_client: An instance of httpx.AsyncClient.
        method: HTTP method (e.g., "GET", "POST").
        endpoint: API endpoint path (e.g., "/iam/v1/organizations").
        token: The Bearer token for authentication.
        params: Optional dictionary of query parameters.
        json_data: Optional dictionary for the request body (for POST, PUT).

    Returns:
        A dictionary containing the JSON response from the API.

    Raises:
        httpx.HTTPStatusError: If the API returns an error status.
        httpx.RequestError: For other request-related issues.
    """
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    }
    if json_data:
        headers["Content-Type"] = "application/json"

    url = f"{HCP_API_BASE_URL}{endpoint}"
    logger.debug(f"Making HCP API request: {method} {url} Params: {params} Body: {json_data is not None}")

    try:
        response = await http_client.request(
            method, url, headers=headers, params=params, json=json_data
        )
        response.raise_for_status()  # Raise an exception for 4xx/5xx status codes
        return response.json()
    except httpx.HTTPStatusError as e:
        logger.error(
            f"HCP API HTTP error: {e.response.status_code} - {e.response.text} for {method} {url}"
        )
        raise  # Re-raise the exception to be handled by the caller
    except httpx.RequestError as e:
        logger.error(f"HCP API Request error: {e} for {method} {url}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error during HCP API request: {e} for {method} {url}")
        raise