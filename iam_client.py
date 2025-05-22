# iam_client.py
import logging
from typing import Optional, Dict, Any, List, Tuple
from hcp_client import HcpClient

logger = logging.getLogger(__name__)
IAM_API_VERSION = "2019-12-10" # Primary version for IAM

class IamClient:
    """Client for interacting with HCP IAM APIs."""
    def __init__(self, hcp_client: HcpClient):
        self.hcp_client = hcp_client

    async def list_service_principals_org(self, organization_id: str, page_size: int = 50, next_page_token: Optional[str] = None) -> Tuple[Optional[List[Dict[str, Any]]], Optional[str], Optional[str]]:
        """Lists service principals at the organization level."""
        # Path from iam.hcp.swagger.json: /iam/2019-12-10/organizations/{organization_id}/service-principals
        endpoint = f"/iam/{IAM_API_VERSION}/organizations/{organization_id}/service-principals"
        params: Dict[str, Any] = {'pagination.page_size': page_size}
        if next_page_token:
            params['pagination.next_page_token'] = next_page_token
        
        response_data, error = await self.hcp_client.get(endpoint, params=params)
        if error:
            return None, None, error
        if response_data:
            return response_data.get("service_principals", []), response_data.get("pagination", {}).get("next_page_token"), None
        return [], None, "No data received"

    async def create_service_principal_org(self, organization_id: str, name: str) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """Creates a service principal at the organization level."""
        endpoint = f"/iam/{IAM_API_VERSION}/organizations/{organization_id}/service-principals"
        payload = {"name": name}
        return await self.hcp_client.post(endpoint, data=payload)

    async def get_service_principal_org(self, organization_id: str, principal_id: str) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """Gets a service principal at the organization level."""
        endpoint = f"/iam/{IAM_API_VERSION}/organizations/{organization_id}/service-principals/{principal_id}"
        return await self.hcp_client.get(endpoint)

    async def delete_service_principal_org(self, organization_id: str, principal_id: str) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """Deletes a service principal at the organization level."""
        endpoint = f"/iam/{IAM_API_VERSION}/organizations/{organization_id}/service-principals/{principal_id}"
        return await self.hcp_client.delete(endpoint)

    async def list_service_principals_project(self, organization_id: str, project_id: str, page_size: int = 50, next_page_token: Optional[str] = None) -> Tuple[Optional[List[Dict[str, Any]]], Optional[str], Optional[str]]:
        """Lists service principals at the project level."""
        # Path from iam.hcp.swagger.json: /iam/2019-12-10/organizations/{organization_id}/projects/{project_id}/service-principals
        endpoint = f"/iam/{IAM_API_VERSION}/organizations/{organization_id}/projects/{project_id}/service-principals"
        params: Dict[str, Any] = {'pagination.page_size': page_size}
        if next_page_token:
            params['pagination.next_page_token'] = next_page_token
        
        response_data, error = await self.hcp_client.get(endpoint, params=params)
        if error:
            return None, None, error
        if response_data:
            return response_data.get("service_principals", []), response_data.get("pagination", {}).get("next_page_token"), None
        return [], None, "No data received"

    async def create_service_principal_project(self, organization_id: str, project_id: str, name: str) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """Creates a service principal at the project level."""
        endpoint = f"/iam/{IAM_API_VERSION}/organizations/{organization_id}/projects/{project_id}/service-principals"
        payload = {"name": name}
        return await self.hcp_client.post(endpoint, data=payload)

    async def get_service_principal_project(self, organization_id: str, project_id: str, principal_id: str) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """Gets a service principal at the project level."""
        endpoint = f"/iam/{IAM_API_VERSION}/organizations/{organization_id}/projects/{project_id}/service-principals/{principal_id}"
        return await self.hcp_client.get(endpoint)

    async def delete_service_principal_project(self, organization_id: str, project_id: str, principal_id: str) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """Deletes a service principal at the project level."""
        endpoint = f"/iam/{IAM_API_VERSION}/organizations/{organization_id}/projects/{project_id}/service-principals/{principal_id}"
        return await self.hcp_client.delete(endpoint)
        
    async def create_service_principal_key_org(self, organization_id: str, principal_id: str) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """Creates a key for an organization-level service principal."""
        # Path: /iam/2019-12-10/organizations/{organization_id}/service-principal-keys
        # The swagger has parent_resource_name in the path like /2019-12-10/{parent_resource_name}/keys
        # which translates to /2019-12-10/iam/organization/{org_id}/service-principal/{sp_id}/keys
        # However, the more specific path /iam/2019-12-10/organizations/{organization_id}/service-principal-keys
        # seems more appropriate for creating a key when you already know the org_id and principal_id.
        # Let's use the one that seems more direct from the swagger:
        # POST /iam/2019-12-10/organizations/{organization_id}/service-principal-keys
        # Body: { "principal_id": "string" }
        endpoint = f"/iam/{IAM_API_VERSION}/organizations/{organization_id}/service-principal-keys"
        payload = {"principal_id": principal_id}
        return await self.hcp_client.post(endpoint, data=payload)

    async def create_service_principal_key_project(self, organization_id: str, project_id: str, principal_id: str) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """Creates a key for a project-level service principal."""
        # Path: /iam/2019-12-10/organizations/{organization_id}/projects/{project_id}/service-principal-keys
        # Body: { "principal_id": "string" }
        endpoint = f"/iam/{IAM_API_VERSION}/organizations/{organization_id}/projects/{project_id}/service-principal-keys"
        payload = {"principal_id": principal_id}
        return await self.hcp_client.post(endpoint, data=payload)

    async def list_groups(self, organization_id: str, page_size: int = 50, next_page_token: Optional[str] = None) -> Tuple[Optional[List[Dict[str, Any]]], Optional[str], Optional[str]]:
        """Lists groups in an organization."""
        # Path: /iam/2019-12-10/iam/organization/{organization_id}/groups
        # The swagger has parent_resource_name like /iam/2019-12-10/iam/{parent_resource_name}/groups
        # where parent_resource_name is organization/{org_id}
        endpoint = f"/iam/{IAM_API_VERSION}/iam/organization/{organization_id}/groups"
        params: Dict[str, Any] = {'pagination.page_size': page_size}
        if next_page_token:
            params['pagination.next_page_token'] = next_page_token
        
        response_data, error = await self.hcp_client.get(endpoint, params=params)
        if error:
            return None, None, error
        if response_data:
            return response_data.get("groups", []), response_data.get("pagination", {}).get("next_page_token"), None
        return [], None, "No data received"

    async def create_group(self, organization_id: str, name: str, description: Optional[str] = None, member_principal_ids: Optional[List[str]] = None) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """Creates a group in an organization."""
        endpoint = f"/iam/{IAM_API_VERSION}/iam/organization/{organization_id}/groups"
        payload: Dict[str, Any] = {"name": name}
        if description:
            payload["description"] = description
        if member_principal_ids:
            payload["member_principal_ids"] = member_principal_ids
        return await self.hcp_client.post(endpoint, data=payload)

    async def get_group(self, organization_id: str, group_id: str) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """Gets a group from an organization."""
        # Path: /iam/2019-12-10/{resource_name} where resource_name is iam/organization/{org_id}/group/{group_id}
        resource_name = f"iam/organization/{organization_id}/group/{group_id}"
        endpoint = f"/iam/{IAM_API_VERSION}/{resource_name}"
        return await self.hcp_client.get(endpoint)

    # Add other IAM methods as needed (e.g., delete group, update group, manage group members, invitations, etc.)
