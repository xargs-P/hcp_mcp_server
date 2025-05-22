# vault_secrets_client.py
import logging
from typing import Optional, Dict, Any, List, Tuple
from hcp_client import HcpClient

logger = logging.getLogger(__name__)
VAULT_SECRETS_API_VERSION = "2023-11-28"

class VaultSecretsClient:
    """Client for interacting with HCP Vault Secrets APIs."""
    def __init__(self, hcp_client: HcpClient):
        self.hcp_client = hcp_client

    async def list_apps(self, organization_id: str, project_id: str, page_size: int = 50, next_page_token: Optional[str] = None) -> Tuple[Optional[List[Dict[str, Any]]], Optional[str], Optional[str]]:
        """Lists Vault Secrets applications within a project."""
        endpoint = f"/secrets/{VAULT_SECRETS_API_VERSION}/organizations/{organization_id}/projects/{project_id}/apps"
        params: Dict[str, Any] = {'pagination.page_size': page_size}
        if next_page_token:
            params['pagination.next_page_token'] = next_page_token
            
        response_data, error = await self.hcp_client.get(endpoint, params=params)
        if error:
            return None, None, error
        if response_data:
            return response_data.get("apps", []), response_data.get("pagination", {}).get("next_page_token"), None
        return [], None, "No data received"

    async def create_app(self, organization_id: str, project_id: str, app_name: str, description: Optional[str] = None) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """Creates a Vault Secrets application."""
        endpoint = f"/secrets/{VAULT_SECRETS_API_VERSION}/organizations/{organization_id}/projects/{project_id}/apps"
        payload = {"name": app_name}
        if description:
            payload["description"] = description
        return await self.hcp_client.post(endpoint, data=payload)

    async def get_app(self, organization_id: str, project_id: str, app_name: str) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """Retrieves a Vault Secrets application."""
        endpoint = f"/secrets/{VAULT_SECRETS_API_VERSION}/organizations/{organization_id}/projects/{project_id}/apps/{app_name}"
        return await self.hcp_client.get(endpoint)

    async def delete_app(self, organization_id: str, project_id: str, app_name: str) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """Deletes a Vault Secrets application."""
        endpoint = f"/secrets/{VAULT_SECRETS_API_VERSION}/organizations/{organization_id}/projects/{project_id}/apps/{app_name}"
        return await self.hcp_client.delete(endpoint)

    async def create_kv_secret(self, organization_id: str, project_id: str, app_name: str, secret_name: str, secret_value: str) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """Creates or updates a KV secret in a Vault Secrets application."""
        endpoint = f"/secrets/{VAULT_SECRETS_API_VERSION}/organizations/{organization_id}/projects/{project_id}/apps/{app_name}/secret/kv"
        payload = {"name": secret_name, "value": secret_value}
        return await self.hcp_client.post(endpoint, data=payload)

    async def open_kv_secret(self, organization_id: str, project_id: str, app_name: str, secret_name: str) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """Opens (retrieves the value of) a KV secret."""
        # Path: /secrets/2023-11-28/organizations/{organization_id}/projects/{project_id}/apps/{app_name}/secrets/{secret_name}:open
        endpoint = f"/secrets/{VAULT_SECRETS_API_VERSION}/organizations/{organization_id}/projects/{project_id}/apps/{app_name}/secrets/{secret_name}:open"
        return await self.hcp_client.get(endpoint)

    async def delete_kv_secret(self, organization_id: str, project_id: str, app_name: str, secret_name: str) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """Deletes a KV secret."""
        # Path: /secrets/2023-11-28/organizations/{organization_id}/projects/{project_id}/apps/{app_name}/secrets/{secret_name}
        endpoint = f"/secrets/{VAULT_SECRETS_API_VERSION}/organizations/{organization_id}/projects/{project_id}/apps/{app_name}/secrets/{secret_name}"
        return await self.hcp_client.delete(endpoint)

    async def list_app_secrets(self, organization_id: str, project_id: str, app_name: str, page_size: int = 50, next_page_token: Optional[str] = None) -> Tuple[Optional[List[Dict[str, Any]]], Optional[str], Optional[str]]:
        """Lists secrets within a Vault Secrets application."""
        endpoint = f"/secrets/{VAULT_SECRETS_API_VERSION}/organizations/{organization_id}/projects/{project_id}/apps/{app_name}/secrets"
        params: Dict[str, Any] = {'pagination.page_size': page_size}
        if next_page_token:
            params['pagination.next_page_token'] = next_page_token
            
        response_data, error = await self.hcp_client.get(endpoint, params=params)
        if error:
            return None, None, error
        if response_data:
            return response_data.get("secrets", []), response_data.get("pagination", {}).get("next_page_token"), None
        return [], None, "No data received"

    # Add other Vault Secrets methods as needed (versions, other secret types, etc.)
