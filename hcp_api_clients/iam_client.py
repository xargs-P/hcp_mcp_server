# hcp_mcp_server/hcp_api_clients/iam_client.py
# Client functions for interacting with HCP IAM APIs.
# Based on OpenAPI spec: cloud-iam/stable/2019-12-10/hcp.swagger.json

import httpx
import logging
from typing import Dict, Any, List
from .base_client import make_hcp_api_request

logger = logging.getLogger(__name__)

# --- Organization Endpoints (subset) ---
async def list_organization_service_principal_keys(
    http_client: httpx.AsyncClient, token: str, organization_id: str
) -> Dict[str, Any]:
    """Lists service principal keys for an organization."""
    endpoint = f"/iam/2019-12-10/organizations/{organization_id}/service-principal-keys"
    return await make_hcp_api_request(http_client, "GET", endpoint, token)

async def list_organization_roles(
    http_client: httpx.AsyncClient, token: str, organization_id: str
) -> Dict[str, Any]:
    """Lists roles available within an organization."""
    #endpoint = f"/iam/2019-12-10/organizations/{organization_id}/roles"
    endpoint = f"/resource-manager/2019-12-10/organizations/{organization_id}/roles"
    # Example response: {"roles": [{"id": "contributor", "resource_name": "...", ...}]}
    return await make_hcp_api_request(http_client, "GET", endpoint, token)

async def get_organization_role(
    http_client: httpx.AsyncClient, token: str, organization_id: str, role_id: str
) -> Dict[str, Any]:
    """Gets a specific role by its ID within an organization."""
    #endpoint = f"/iam/2019-12-10/organizations/{organization_id}/roles/{role_id}"
    endpoint = f"/resource-manager/2019-12-10/organizations/{organization_id}/{role_id}"
    return await make_hcp_api_request(http_client, "GET", endpoint, token)

async def list_organization_users(
    http_client: httpx.AsyncClient, token: str, organization_id: str
) -> Dict[str, Any]:
    """Lists users belonging to an organization."""
    endpoint = f"/iam/2019-12-10/organizations/{organization_id}/user-principals"
    # Example response: {"users": [{"email": "user@example.com", "resource_name": "...", ...}]}
    return await make_hcp_api_request(http_client, "GET", endpoint, token)

# --- Project Endpoints (subset, if needed, though IAM is often org-level) ---
# Most IAM resources like users and roles are managed at the organization level.
# If project-specific IAM resources are needed, they would be added here.

# --- Service Principal Endpoints (subset) ---
async def list_service_principals(
    http_client: httpx.AsyncClient, token: str, organization_id: str
) -> Dict[str, Any]:
    """Lists service principals for an organization."""
    endpoint = f"/iam/2019-12-10/organizations/{organization_id}/service-principals"
    return await make_hcp_api_request(http_client, "GET", endpoint, token)

async def get_service_principal(
    http_client: httpx.AsyncClient, token: str, organization_id: str, service_principal_id: str
) -> Dict[str, Any]:
    """Gets a specific service principal by its ID."""
    endpoint = f"/iam/2019-12-10/organizations/{organization_id}/service-principals/{service_principal_id}"
    return await make_hcp_api_request(http_client, "GET", endpoint, token)

# Add more IAM client functions as needed based on MCP requirements