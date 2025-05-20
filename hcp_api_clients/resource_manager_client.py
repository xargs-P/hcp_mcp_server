# hcp_mcp_server/hcp_api_clients/resource_manager_client.py
# Client functions for interacting with HCP Resource Manager APIs.
# Based on OpenAPI spec: cloud-resource-manager/stable/2019-12-10/hcp.swagger.json

import httpx
import logging
from typing import Dict, Any, List
from .base_client import make_hcp_api_request

logger = logging.getLogger(__name__)

async def list_organizations(http_client: httpx.AsyncClient, token: str) -> Dict[str, Any]:
    """Lists all organizations the authenticated principal has access to."""
    endpoint = "/resource-manager/2019-12-10/organizations"
    # Example response: {"organizations": [{"id": "org-uuid", "resource_name": "...", ...}]}
    return await make_hcp_api_request(http_client, "GET", endpoint, token)

async def get_organization(
    http_client: httpx.AsyncClient, token: str, organization_id: str
) -> Dict[str, Any]:
    """Gets details for a specific organization."""
    endpoint = f"/resource-manager/2019-12-10/organizations/{organization_id}"
    return await make_hcp_api_request(http_client, "GET", endpoint, token)

async def list_projects(
    http_client: httpx.AsyncClient, token: str, organization_id: str
) -> Dict[str, Any]:
    """Lists all projects within a given organization."""
    params = {"scope.type": "ORGANIZATION", "scope.id": organization_id}
    endpoint = f"/resource-manager/2019-12-10/projects"
    # Example response: {"projects": [{"id": "project-uuid", "name": "...", ...}]}
    return await make_hcp_api_request(http_client, "GET", endpoint, token, params)

async def get_project(
    http_client: httpx.AsyncClient, token: str, organization_id: str, project_id: str
) -> Dict[str, Any]:
    """Gets details for a specific project within an organization."""
    endpoint = f"/resource-manager/2019-12-10/projects/{project_id}"
    return await make_hcp_api_request(http_client, "GET", endpoint, token)

# Add more resource manager client functions as needed