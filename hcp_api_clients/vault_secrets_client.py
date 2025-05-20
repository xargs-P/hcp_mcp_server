# hcp_mcp_server/hcp_api_clients/vault_secrets_client.py
# Client functions for interacting with HCP Vault Secrets APIs.
# Based on OpenAPI spec: cloud-vault-secrets/stable/2023-11-28/hcp.swagger.json

import httpx
import logging
from typing import Dict, Any, List, Optional
from .base_client import make_hcp_api_request

logger = logging.getLogger(__name__)

def _get_vault_secrets_base_path(organization_id: str, project_id: str) -> str:
    """Helper to construct the base path for Vault Secrets API calls."""
    #return f"/secrets/v1/organizations/{organization_id}/projects/{project_id}"
    return f"/secrets/2023-11-28/organizations/{organization_id}/projects/{project_id}"

async def list_apps(
    http_client: httpx.AsyncClient, token: str, organization_id: str, project_id: str
) -> Dict[str, Any]:
    """Lists all secret applications within a project."""
    base_path = _get_vault_secrets_base_path(organization_id, project_id)
    endpoint = f"{base_path}/apps"
    # Example response: {"apps": [{"name": "my-app", ...}]}
    return await make_hcp_api_request(http_client, "GET", endpoint, token)

async def get_app(
    http_client: httpx.AsyncClient, token: str, organization_id: str, project_id: str, app_name: str
) -> Dict[str, Any]:
    """Gets details for a specific secret application."""
    base_path = _get_vault_secrets_base_path(organization_id, project_id)
    endpoint = f"{base_path}/apps/{app_name}"
    return await make_hcp_api_request(http_client, "GET", endpoint, token)

async def list_secrets(
    http_client: httpx.AsyncClient, token: str, organization_id: str, project_id: str, app_name: str
) -> Dict[str, Any]:
    """Lists secrets (metadata) within a specific application."""
    base_path = _get_vault_secrets_base_path(organization_id, project_id)
    endpoint = f"{base_path}/apps/{app_name}/secrets"
    # Example response: {"secrets": [{"name": "my-secret", "latest_version": "v1", ...}]}
    return await make_hcp_api_request(http_client, "GET", endpoint, token)

async def get_secret_value(
    http_client: httpx.AsyncClient,
    token: str,
    organization_id: str,
    project_id: str,
    app_name: str,
    secret_name: str,
) -> Dict[str, Any]:
    """
    Retrieves the value of a specific secret.
    This requires the 'action=reveal' parameter as per HCP Vault Secrets API.
    """
    base_path = _get_vault_secrets_base_path(organization_id, project_id)
    endpoint = f"{base_path}/apps/{app_name}/secrets/{secret_name}"
    params = {"action": "reveal"}
    # Example response: {"secret": {"name": "my-secret", "version": {"version": "v1", "type": "kv", "value": "actual_secret_value", ...}}}
    return await make_hcp_api_request(http_client, "GET", endpoint, token, params=params)

async def get_secret_metadata( # Added for completeness, if only metadata is needed
    http_client: httpx.AsyncClient,
    token: str,
    organization_id: str,
    project_id: str,
    app_name: str,
    secret_name: str,
) -> Dict[str, Any]:
    """Retrieves the metadata of a specific secret (without revealing its value)."""
    base_path = _get_vault_secrets_base_path(organization_id, project_id)
    endpoint = f"{base_path}/apps/{app_name}/secrets/{secret_name}"
    return await make_hcp_api_request(http_client, "GET", endpoint, token)


# Add more Vault Secrets client functions as needed