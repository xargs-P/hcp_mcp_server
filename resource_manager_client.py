# resource_manager_client.py
import logging
from typing import Optional, Dict, Any, List, Tuple
from hcp_client import HcpClient

logger = logging.getLogger(__name__)
RESOURCE_MANAGER_API_VERSION = "2019-12-10"

class ResourceManagerClient:
    """Client for interacting with HCP Resource Manager APIs."""
    def __init__(self, hcp_client: HcpClient):
        self.hcp_client = hcp_client

    async def list_organizations(self, page_size: int = 50, next_page_token: Optional[str] = None) -> Tuple[Optional[List[Dict[str, Any]]], Optional[str], Optional[str]]:
        """Lists organizations the caller has access to."""
        endpoint = f"/resource-manager/{RESOURCE_MANAGER_API_VERSION}/organizations"
        params: Dict[str, Any] = {'pagination.page_size': page_size}
        if next_page_token:
            params['pagination.next_page_token'] = next_page_token
        
        response_data, error = await self.hcp_client.get(endpoint, params=params)
        if error:
            return None, None, error
        if response_data:
            return response_data.get("organizations", []), response_data.get("pagination", {}).get("next_page_token"), None
        return [], None, "No data received"

    async def get_organization(self, organization_id: str) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """Retrieves an organization by ID."""
        endpoint = f"/resource-manager/{RESOURCE_MANAGER_API_VERSION}/organizations/{organization_id}"
        return await self.hcp_client.get(endpoint)

    async def list_projects(self, organization_id: str, page_size: int = 50, next_page_token: Optional[str] = None) -> Tuple[Optional[List[Dict[str, Any]]], Optional[str], Optional[str]]:
        """Lists projects within an organization."""
        endpoint = f"/resource-manager/{RESOURCE_MANAGER_API_VERSION}/projects"
        # Scope is defined as scope.type and scope.id in swagger
        params: Dict[str, Any] = {
            "scope.type": "ORGANIZATION",
            "scope.id": organization_id,
            'pagination.page_size': page_size
        }
        if next_page_token:
            params['pagination.next_page_token'] = next_page_token
            
        response_data, error = await self.hcp_client.get(endpoint, params=params)
        if error:
            return None, None, error
        if response_data:
            return response_data.get("projects", []), response_data.get("pagination", {}).get("next_page_token"), None
        return [], None, "No data received"

    async def get_project(self, project_id: str) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """Retrieves a project by ID."""
        endpoint = f"/resource-manager/{RESOURCE_MANAGER_API_VERSION}/projects/{project_id}"
        return await self.hcp_client.get(endpoint)

    async def get_organization_iam_policy(self, organization_id: str) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """Retrieves the IAM policy for an organization."""
        endpoint = f"/resource-manager/{RESOURCE_MANAGER_API_VERSION}/organizations/{organization_id}/iam-policy"
        return await self.hcp_client.get(endpoint)

    async def set_organization_iam_policy(self, organization_id: str, policy: Dict[str, Any]) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """Sets the IAM policy for an organization."""
        endpoint = f"/resource-manager/{RESOURCE_MANAGER_API_VERSION}/organizations/{organization_id}/iam-policy"
        # The body for PUT is {"policy": PolicyObject}
        return await self.hcp_client.put(endpoint, data={"policy": policy})

    async def get_project_iam_policy(self, project_id: str) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """Retrieves the IAM policy for a project."""
        endpoint = f"/resource-manager/{RESOURCE_MANAGER_API_VERSION}/projects/{project_id}/iam-policy"
        return await self.hcp_client.get(endpoint)

    async def set_project_iam_policy(self, project_id: str, policy: Dict[str, Any]) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """Sets the IAM policy for a project."""
        endpoint = f"/resource-manager/{RESOURCE_MANAGER_API_VERSION}/projects/{project_id}/iam-policy"
        return await self.hcp_client.put(endpoint, data={"policy": policy})

    # Add other resource manager methods as needed (create project, delete project, etc.)
