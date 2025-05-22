# tools/iam_tools.py
import logging
from typing import Dict, Any, Tuple, List, Optional

# Imports from the official MCP SDK
from mcp.tools import Tool, ToolParameter
from mcp.common import Resource # For type hinting

from iam_client import IamClient
from resources.hcp_resources import HcpServicePrincipalResource, HcpServicePrincipalKeyResource, HcpGroupResource

logger = logging.getLogger(__name__)

class ListServicePrincipalsOrgTool(Tool):
    name: str = "hcp_list_service_principals_org"
    description: str = "Lists service principals within a specific HCP organization."
    parameters: List[ToolParameter] = [
        ToolParameter(name="organization_id", type="string", is_required=True, description="The UUID of the organization."),
        ToolParameter(name="page_size", type="integer", is_required=False, description="Number of service principals to return per page (default 50)."),
        ToolParameter(name="next_page_token", type="string", is_required=False, description="Token for fetching the next page of results."),
    ]

    def __init__(self, client: IamClient):
        self.client = client

    async def __call__(self, **kwargs: Any) -> Tuple[str, Optional[List[HcpServicePrincipalResource]]]:
        org_id = kwargs.get("organization_id")
        if not org_id: return "Error: organization_id is required.", None
        page_size = kwargs.get("page_size", 50)
        next_page_token = kwargs.get("next_page_token")

        sp_data, new_next_page_token, error = await self.client.list_service_principals_org(org_id, page_size, next_page_token)
        if error: return f"Error listing service principals for org {org_id}: {error}", None
        if sp_data is None: return "Error: No service principal data received.", None
        
        resources = [HcpServicePrincipalResource.from_api_response(sp) for sp in sp_data]
        result_str = f"Found {len(resources)} service principals in organization {org_id}."
        if new_next_page_token: result_str += f" Next page token: {new_next_page_token}"
        return result_str, resources

class CreateServicePrincipalOrgTool(Tool):
    name: str = "hcp_create_service_principal_org"
    description: str = "Creates a new service principal at the organization level."
    parameters: List[ToolParameter] = [
        ToolParameter(name="organization_id", type="string", is_required=True, description="The UUID of the organization."),
        ToolParameter(name="name", type="string", is_required=True, description="The name for the new service principal."),
    ]

    def __init__(self, client: IamClient):
        self.client = client

    async def __call__(self, **kwargs: Any) -> Tuple[str, Optional[List[HcpServicePrincipalResource]]]:
        org_id = kwargs.get("organization_id")
        name = kwargs.get("name")
        if not org_id or not name: return "Error: organization_id and name are required.", None

        sp_data, error = await self.client.create_service_principal_org(org_id, name)
        if error: return f"Error creating service principal in org {org_id}: {error}", None
        if not sp_data or not sp_data.get("service_principal"): return "Error: Service principal data not found in response.", None
        
        resource = HcpServicePrincipalResource.from_api_response(sp_data["service_principal"])
        return f"Successfully created service principal: {resource.name} ({resource.id})", [resource]

class GetServicePrincipalOrgTool(Tool):
    name: str = "hcp_get_service_principal_org"
    description: str = "Retrieves a specific service principal from an organization."
    parameters: List[ToolParameter] = [
        ToolParameter(name="organization_id", type="string", is_required=True, description="The UUID of the organization."),
        ToolParameter(name="principal_id", type="string", is_required=True, description="The ID of the service principal."),
    ]
    def __init__(self, client: IamClient): self.client = client
    async def __call__(self, **kwargs: Any) -> Tuple[str, Optional[List[HcpServicePrincipalResource]]]:
        org_id = kwargs.get("organization_id")
        principal_id = kwargs.get("principal_id")
        if not org_id or not principal_id: return "Error: organization_id and principal_id are required.", None
        data, error = await self.client.get_service_principal_org(org_id, principal_id)
        if error: return f"Error: {error}", None
        if not data or not data.get("service_principal"): return "Service principal not found.", None
        resource = HcpServicePrincipalResource.from_api_response(data["service_principal"])
        return "Service principal retrieved.", [resource]

class DeleteServicePrincipalOrgTool(Tool):
    name: str = "hcp_delete_service_principal_org"
    description: str = "Deletes a service principal from an organization."
    parameters: List[ToolParameter] = [
        ToolParameter(name="organization_id", type="string", is_required=True, description="The UUID of the organization."),
        ToolParameter(name="principal_id", type="string", is_required=True, description="The ID of the service principal to delete."),
    ]
    def __init__(self, client: IamClient): self.client = client
    async def __call__(self, **kwargs: Any) -> Tuple[str, None]: # Returns None for resources
        org_id = kwargs.get("organization_id")
        principal_id = kwargs.get("principal_id")
        if not org_id or not principal_id: return "Error: organization_id and principal_id are required.", None
        _, error = await self.client.delete_service_principal_org(org_id, principal_id)
        if error: return f"Error: {error}", None
        return f"Service principal {principal_id} deleted from organization {org_id}.", None


class ListServicePrincipalsProjectTool(Tool):
    name: str = "hcp_list_service_principals_project"
    description: str = "Lists service principals within a specific HCP project."
    parameters: List[ToolParameter] = [
        ToolParameter(name="organization_id", type="string", is_required=True, description="The UUID of the parent organization."),
        ToolParameter(name="project_id", type="string", is_required=True, description="The UUID of the project."),
        ToolParameter(name="page_size", type="integer", is_required=False, description="Number of service principals to return per page (default 50)."),
        ToolParameter(name="next_page_token", type="string", is_required=False, description="Token for fetching the next page of results."),
    ]
    def __init__(self, client: IamClient): self.client = client
    async def __call__(self, **kwargs: Any) -> Tuple[str, Optional[List[HcpServicePrincipalResource]]]:
        org_id = kwargs.get("organization_id")
        project_id = kwargs.get("project_id")
        if not org_id or not project_id: return "Error: organization_id and project_id are required.", None
        page_size = kwargs.get("page_size", 50)
        next_page_token = kwargs.get("next_page_token")
        sp_data, new_next_page_token, error = await self.client.list_service_principals_project(org_id, project_id, page_size, next_page_token)
        if error: return f"Error: {error}", None
        if sp_data is None: return "Error: No data received.", None
        resources = [HcpServicePrincipalResource.from_api_response(sp) for sp in sp_data]
        result_str = f"Found {len(resources)} service principals in project {project_id}."
        if new_next_page_token: result_str += f" Next page token: {new_next_page_token}"
        return result_str, resources

class CreateServicePrincipalProjectTool(Tool):
    name: str = "hcp_create_service_principal_project"
    description: str = "Creates a new service principal at the project level."
    parameters: List[ToolParameter] = [
        ToolParameter(name="organization_id", type="string", is_required=True, description="The UUID of the parent organization."),
        ToolParameter(name="project_id", type="string", is_required=True, description="The UUID of the project."),
        ToolParameter(name="name", type="string", is_required=True, description="The name for the new service principal."),
    ]
    def __init__(self, client: IamClient): self.client = client
    async def __call__(self, **kwargs: Any) -> Tuple[str, Optional[List[HcpServicePrincipalResource]]]:
        org_id = kwargs.get("organization_id")
        project_id = kwargs.get("project_id")
        name = kwargs.get("name")
        if not all([org_id, project_id, name]): return "Error: organization_id, project_id, and name are required.", None
        sp_data, error = await self.client.create_service_principal_project(org_id, project_id, name)
        if error: return f"Error: {error}", None
        if not sp_data or not sp_data.get("service_principal"): return "Error: Service principal data not found.", None
        resource = HcpServicePrincipalResource.from_api_response(sp_data["service_principal"])
        return f"Service principal {resource.name} created.", [resource]

class GetServicePrincipalProjectTool(Tool):
    name: str = "hcp_get_service_principal_project"
    description: str = "Retrieves a specific service principal from a project."
    parameters: List[ToolParameter] = [
        ToolParameter(name="organization_id", type="string", is_required=True, description="The UUID of the organization."),
        ToolParameter(name="project_id", type="string", is_required=True, description="The UUID of the project."),
        ToolParameter(name="principal_id", type="string", is_required=True, description="The ID of the service principal."),
    ]
    def __init__(self, client: IamClient): self.client = client
    async def __call__(self, **kwargs: Any) -> Tuple[str, Optional[List[HcpServicePrincipalResource]]]:
        org_id = kwargs.get("organization_id")
        project_id = kwargs.get("project_id")
        principal_id = kwargs.get("principal_id")
        if not all([org_id, project_id, principal_id]): return "Error: organization_id, project_id, and principal_id are required.", None
        data, error = await self.client.get_service_principal_project(org_id, project_id, principal_id)
        if error: return f"Error: {error}", None
        if not data or not data.get("service_principal"): return "Service principal not found.", None
        resource = HcpServicePrincipalResource.from_api_response(data["service_principal"])
        return "Service principal retrieved.", [resource]

class DeleteServicePrincipalProjectTool(Tool):
    name: str = "hcp_delete_service_principal_project"
    description: str = "Deletes a service principal from a project."
    parameters: List[ToolParameter] = [
        ToolParameter(name="organization_id", type="string", is_required=True, description="The UUID of the organization."),
        ToolParameter(name="project_id", type="string", is_required=True, description="The UUID of the project."),
        ToolParameter(name="principal_id", type="string", is_required=True, description="The ID of the service principal to delete."),
    ]
    def __init__(self, client: IamClient): self.client = client
    async def __call__(self, **kwargs: Any) -> Tuple[str, None]:
        org_id = kwargs.get("organization_id")
        project_id = kwargs.get("project_id")
        principal_id = kwargs.get("principal_id")
        if not all([org_id, project_id, principal_id]): return "Error: organization_id, project_id, and principal_id are required.", None
        _, error = await self.client.delete_service_principal_project(org_id, project_id, principal_id)
        if error: return f"Error: {error}", None
        return f"Service principal {principal_id} deleted from project {project_id}.", None

class CreateServicePrincipalKeyOrgTool(Tool):
    name: str = "hcp_create_service_principal_key_org"
    description: str = "Creates a new key for an organization-level service principal. The secret is returned only once."
    parameters: List[ToolParameter] = [
        ToolParameter(name="organization_id", type="string", is_required=True, description="The UUID of the organization."),
        ToolParameter(name="principal_id", type="string", is_required=True, description="The ID of the service principal."),
    ]
    def __init__(self, client: IamClient): self.client = client
    async def __call__(self, **kwargs: Any) -> Tuple[str, Optional[List[HcpServicePrincipalKeyResource]]]:
        org_id = kwargs.get("organization_id")
        principal_id = kwargs.get("principal_id")
        if not org_id or not principal_id: return "Error: organization_id and principal_id are required.", None
        key_data, error = await self.client.create_service_principal_key_org(org_id, principal_id)
        if error: return f"Error creating key for service principal {principal_id} in org {org_id}: {error}", None
        if not key_data or not key_data.get("key") or "client_secret" not in key_data:
            return "Error: Key data or client_secret not found in response.", None
        
        key_info = key_data["key"]
        client_secret = key_data["client_secret"]
        resource = HcpServicePrincipalKeyResource.from_api_response(key_info, principal_id, f"organizations/{org_id}", client_secret)
        
        return f"Successfully created key for service principal {principal_id}. Client ID: {resource.client_id}, Client Secret: {client_secret}. Store the secret securely, it will not be shown again.", [resource]

class CreateServicePrincipalKeyProjectTool(Tool):
    name: str = "hcp_create_service_principal_key_project"
    description: str = "Creates a new key for a project-level service principal. The secret is returned only once."
    parameters: List[ToolParameter] = [
        ToolParameter(name="organization_id", type="string", is_required=True, description="The UUID of the organization."),
        ToolParameter(name="project_id", type="string", is_required=True, description="The UUID of the project."),
        ToolParameter(name="principal_id", type="string", is_required=True, description="The ID of the service principal."),
    ]
    def __init__(self, client: IamClient): self.client = client
    async def __call__(self, **kwargs: Any) -> Tuple[str, Optional[List[HcpServicePrincipalKeyResource]]]:
        org_id = kwargs.get("organization_id")
        project_id = kwargs.get("project_id")
        principal_id = kwargs.get("principal_id")
        if not all([org_id, project_id, principal_id]): return "Error: organization_id, project_id, and principal_id are required.", None
        key_data, error = await self.client.create_service_principal_key_project(org_id, project_id, principal_id)
        if error: return f"Error creating key for service principal {principal_id} in project {project_id}: {error}", None
        if not key_data or not key_data.get("key") or "client_secret" not in key_data:
            return "Error: Key data or client_secret not found in response.", None
        
        key_info = key_data["key"]
        client_secret = key_data["client_secret"]
        resource = HcpServicePrincipalKeyResource.from_api_response(key_info, principal_id, f"projects/{project_id}", client_secret)
        
        return f"Successfully created key for service principal {principal_id} in project {project_id}. Client ID: {resource.client_id}, Client Secret: {client_secret}. Store the secret securely, it will not be shown again.", [resource]

class ListGroupsTool(Tool):
    name: str = "hcp_list_groups"
    description: str = "Lists groups within a specific HCP organization."
    parameters: List[ToolParameter] = [
        ToolParameter(name="organization_id", type="string", is_required=True, description="The UUID of the organization."),
        ToolParameter(name="page_size", type="integer", is_required=False, description="Number of groups to return per page (default 50)."),
        ToolParameter(name="next_page_token", type="string", is_required=False, description="Token for fetching the next page of results."),
    ]
    def __init__(self, client: IamClient): self.client = client
    async def __call__(self, **kwargs: Any) -> Tuple[str, Optional[List[HcpGroupResource]]]:
        org_id = kwargs.get("organization_id")
        if not org_id: return "Error: organization_id is required.", None
        page_size = kwargs.get("page_size", 50)
        next_page_token = kwargs.get("next_page_token")
        group_data, new_next_page_token, error = await self.client.list_groups(org_id, page_size, next_page_token)
        if error: return f"Error: {error}", None
        if group_data is None: return "Error: No data received.", None
        resources = [HcpGroupResource.from_api_response(g) for g in group_data]
        result_str = f"Found {len(resources)} groups in organization {org_id}."
        if new_next_page_token: result_str += f" Next page token: {new_next_page_token}"
        return result_str, resources

class CreateGroupTool(Tool):
    name: str = "hcp_create_group"
    description: str = "Creates a new group in an organization."
    parameters: List[ToolParameter] = [
        ToolParameter(name="organization_id", type="string", is_required=True, description="The UUID of the organization."),
        ToolParameter(name="name", type="string", is_required=True, description="The name for the new group."),
        ToolParameter(name="description", type="string", is_required=False, description="Optional description for the group."),
        ToolParameter(name="member_principal_ids_json", type="string", is_required=False, description="Optional JSON string of a list of principal IDs to add as members. E.g., '[\"user-uuid1\", \"sp-uuid2\"]'"),
    ]
    def __init__(self, client: IamClient): self.client = client
    async def __call__(self, **kwargs: Any) -> Tuple[str, Optional[List[HcpGroupResource]]]:
        import json
        org_id = kwargs.get("organization_id")
        name = kwargs.get("name")
        description = kwargs.get("description")
        member_principal_ids_json = kwargs.get("member_principal_ids_json")
        member_principal_ids: Optional[List[str]] = None

        if not org_id or not name: return "Error: organization_id and name are required.", None
        
        if member_principal_ids_json:
            try:
                member_principal_ids = json.loads(member_principal_ids_json)
                if not isinstance(member_principal_ids, list) or not all(isinstance(item, str) for item in member_principal_ids):
                    return "Error: member_principal_ids_json must be a JSON array of strings.", None
            except json.JSONDecodeError:
                return "Error: Invalid JSON format for member_principal_ids_json.", None

        group_data, error = await self.client.create_group(org_id, name, description, member_principal_ids)
        if error: return f"Error: {error}", None
        if not group_data or not group_data.get("group"): return "Error: Group data not found in response.", None
        resource = HcpGroupResource.from_api_response(group_data["group"])
        return f"Group {resource.display_name} created.", [resource]

class GetGroupTool(Tool):
    name: str = "hcp_get_group"
    description: str = "Retrieves a specific group from an organization."
    parameters: List[ToolParameter] = [
        ToolParameter(name="organization_id", type="string", is_required=True, description="The UUID of the organization."),
        ToolParameter(name="group_id", type="string", is_required=True, description="The ID of the group."),
    ]
    def __init__(self, client: IamClient): self.client = client
    async def __call__(self, **kwargs: Any) -> Tuple[str, Optional[List[HcpGroupResource]]]:
        org_id = kwargs.get("organization_id")
        group_id = kwargs.get("group_id")
        if not org_id or not group_id: return "Error: organization_id and group_id are required.", None
        data, error = await self.client.get_group(org_id, group_id)
        if error: return f"Error: {error}", None
        if not data or not data.get("group"): return "Group not found.", None
        resource = HcpGroupResource.from_api_response(data["group"])
        return "Group retrieved.", [resource]

