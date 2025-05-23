# hcp_client.py
"""
Client for interacting with HashiCorp Cloud Platform APIs.
Handles OAuth 2.0 client credentials grant for authentication and making HTTP requests.
"""
import requests
import time
from typing import Optional, Dict, Any

# Assuming config.py is in the same directory or accessible via PYTHONPATH
from config import HCP_AUTH_URL, HCP_CLIENT_ID, HCP_CLIENT_SECRET, HCP_API_BASE_URL, HCP_TOKEN_AUDIENCE

class HCPClient:
    """
    A client for making authenticated requests to the HashiCorp Cloud Platform API.
    It handles fetching and refreshing OAuth2 access tokens.
    """
    def __init__(self):
        self.client_id: Optional[str] = HCP_CLIENT_ID
        self.client_secret: Optional[str] = HCP_CLIENT_SECRET
        self.access_token: Optional[str] = None
        self.token_expiry_time: float = 0  # Stores the epoch time when the token expires
        self.session = requests.Session() # Use a session for connection pooling

    def _get_access_token(self) -> bool:
        """
        Retrieves an access token from the HCP authentication server using client credentials.
        Returns True if successful, False otherwise.
        """
        if not self.client_id or not self.client_secret:
            print("Error: HCP_CLIENT_ID or HCP_CLIENT_SECRET is not configured in hcp_client.")
            return False

        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        payload = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "audience": HCP_TOKEN_AUDIENCE,
        }
        try:
            print(f"Attempting to get access token from: {HCP_AUTH_URL}")
            response = requests.post(HCP_AUTH_URL, headers=headers, data=payload, timeout=10)
            response.raise_for_status()  # Raises HTTPError for bad responses (4XX or 5XX)
            
            token_data = response.json()
            self.access_token = token_data.get("access_token")
            expires_in = token_data.get("expires_in", 3600)  # Default to 1 hour
            # Set expiry time slightly earlier (e.g., 60 seconds buffer) to avoid using an expired token
            self.token_expiry_time = time.time() + expires_in - 60 
            
            if not self.access_token:
                print("Error: Access token not found in response from HCP auth server.")
                return False
            print("Successfully obtained new HCP access token.")
            return True
        except requests.exceptions.HTTPError as e:
            print(f"HTTP error obtaining access token: {e.response.status_code} - {e.response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Request error obtaining access token: {e}")
        except ValueError as e: # Includes JSONDecodeError
            print(f"Error decoding token response JSON: {e}")
        return False

    def _ensure_token(self) -> bool:
        """
        Ensures that a valid (non-expired) access token is available.
        Fetches a new token if the current one is missing or expired.
        Returns True if a valid token is available or obtained, False otherwise.
        """
        if not self.access_token or time.time() >= self.token_expiry_time:
            print("Access token is missing or expired. Fetching new token.")
            if not self._get_access_token():
                return False
        return True

    def _make_request(
        self,
        method: str,
        path: str, # Relative path to the API endpoint (e.g., /iam/v1/users)
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Makes an authenticated request to the HCP API.
        Handles token refresh if necessary.
        Returns a dictionary containing the response data or an error structure.
        """
        if not self._ensure_token():
            return {"error": "Authentication failed: Could not obtain access token.", "status_code": 401, "details": "Client ID or Secret might be invalid or auth server unreachable."}

        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        url = f"{HCP_API_BASE_URL}{path}"

        try:
            response = self.session.request(method, url, headers=headers, params=params, json=json_data, timeout=30)
            
            # Check for HTTP errors
            if not response.ok: # status_code >= 400
                error_details = response.text # Default to raw text
                try:
                    error_details_json = response.json() # Try to parse JSON error
                    error_details = error_details_json
                except ValueError:
                    pass # Keep raw text if not JSON
                print(f"HCP API Error: {response.status_code} to {url}. Response: {error_details}")
                return {
                    "error": f"HCP API request failed with status {response.status_code}",
                    "status_code": response.status_code,
                    "details": error_details
                }

            # Handle successful responses
            if response.status_code == 204:  # No Content
                return {"status_code": 204, "data": {}} # Successfully processed, no content to return
            
            # Attempt to parse JSON for other successful responses
            try:
                return {"status_code": response.status_code, "data": response.json()}
            except ValueError: # JSONDecodeError
                print(f"Could not decode JSON response from {url}, status: {response.status_code}, content: {response.text[:200]}...") # Log snippet
                return {"error": "Failed to decode API JSON response", "status_code": response.status_code, "details": "Response was not valid JSON."}

        except requests.exceptions.Timeout:
            print(f"Request to {url} timed out.")
            return {"error": "Request timed out", "status_code": 408, "details": f"The request to {url} exceeded the timeout limit."}
        except requests.exceptions.ConnectionError:
            print(f"Connection error when requesting {url}.")
            return {"error": "Connection error", "status_code": 503, "details": f"Could not connect to {url}."}
        except requests.exceptions.RequestException as e:
            print(f"Generic request exception for {url}: {e}")
            return {"error": "Request exception", "status_code": 500, "details": str(e)}

    # Convenience methods for GET, POST, PUT, PATCH, DELETE
    def get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return self._make_request("GET", path, params=params)

    def post(self, path: str, data: Optional[Dict[str, Any]] = None, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return self._make_request("POST", path, json_data=data, params=params)

    def put(self, path: str, data: Optional[Dict[str, Any]] = None, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return self._make_request("PUT", path, json_data=data, params=params)

    def patch(self, path: str, data: Optional[Dict[str, Any]] = None, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return self._make_request("PATCH", path, json_data=data, params=params)

    def delete(self, path: str, params: Optional[Dict[str, Any]] = None, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return self._make_request("DELETE", path, params=params, json_data=data)


