# tools/resource_manager_tools.py
import logging
from typing import Dict, Any, Tuple, List, Optional

# Imports from the official MCP SDK
# Corrected: Common classes like ToolParameter and Resource are re-exported at top-level mcp
from mcp import Tool, Resource, ToolParameter  

from resource_manager_client import ResourceManagerClient
from resources.hcp_resources import HcpOrganizationResource, HcpProjectResource, HcpIamPolicyResource

logger = logging.getLogger(__name__)

class ListOrganizationsTool(Tool): 
    name: str = "hcp_list_organizations"
    description: str = "Lists HashiCorp Cloud Platform (HCP) organizations accessible to the caller."
    parameters: List[ToolParameter] = [
        ToolParameter(name="page_size", type="integer", is_required=False, description="Number of organizations to return per page (default 50)."),
        ToolParameter(name="next_page_token", type="string", is_required=False, description="Token for fetching the next page of results."),
    ]

    def __init__(self, client: ResourceManagerClient):
        self.client = client

    async def __call__(self, **kwargs: Any) -> Tuple[str, Optional[List[HcpOrganizationResource]]]:
        page_size = kwargs.get("page_size", 50)
        next_page_token = kwargs.get("next_page_token")
        orgs_data, new_next_page_token, error = await self.client.list_organizations(page_size, next_page_token)
        if error:
            return f"Error listing organizations: {error}", None
        if orgs_data is None: 
             return "Error: No data received from API.", None

        resources = [HcpOrganizationResource.from_api_response(org) for org in orgs_data]
        result_str = f"Found {len(resources)} organizations."
        if new_next_page_token:
            result_str += f" Next page token: {new_next_page_token}"
        return result_str, resources

class GetOrganizationTool(Tool):
    name: str = "hcp_get_organization"
    description: str = "Retrieves details for a specific HCP organization by its ID."
    parameters: List[ToolParameter] = [
        ToolParameter(name="organization_id", type="string", is_required=True, description="The UUID of the organization."),
    ]

    def __init__(self, client: ResourceManagerClient):
        self.client = client

    async def __call__(self, **kwargs: Any) -> Tuple[str, Optional[List[HcpOrganizationResource]]]:
        org_id = kwargs.get("organization_id")
        if not org_id:
            return "Error: organization_id is required.", None
        
        org_data, error = await self.client.get_organization(org_id)
        if error:
            return f"Error getting organization {org_id}: {error}", None
        if not org_data or not org_data.get("organization"): 
            return f"Organization {org_id} not found or no data.", None
        
        resource = HcpOrganizationResource.from_api_response(org_data["organization"])
        return f"Successfully retrieved organization: {resource.name} ({resource.id})", [resource]

class ListProjectsTool(Tool):
    name: str = "hcp_list_projects"
    description: str = "Lists HCP projects within a specified organization."
    parameters: List[ToolParameter] = [
        ToolParameter(name="organization_id", type="string", is_required=True, description="The UUID of the parent organization."),
        ToolParameter(name="page_size", type="integer", is_required=False, description="Number of projects to return per page (default 50)."),
        ToolParameter(name="next_page_token", type="string", is_required=False, description="Token for fetching the next page of results."),
    ]

    def __init__(self, client: ResourceManagerClient):
        self.client = client

    async def __call__(self, **kwargs: Any) -> Tuple[str, Optional[List[HcpProjectResource]]]:
        org_id = kwargs.get("organization_id")
        if not org_id:
            return "Error: organization_id is required.", None
        page_size = kwargs.get("page_size", 50)
        next_page_token = kwargs.get("next_page_token")

        projects_data, new_next_page_token, error = await self.client.list_projects(org_id, page_size, next_page_token)
        if error:
            return f"Error listing projects for organization {org_id}: {error}", None
        if projects_data is None:
            return "Error: No project data received from API.", None

        resources = [HcpProjectResource.from_api_response(proj) for proj in projects_data]
        result_str = f"Found {len(resources)} projects in organization {org_id}."
        if new_next_page_token:
            result_str += f" Next page token: {new_next_page_token}"
        return result_str, resources

class GetProjectTool(Tool):
    name: str = "hcp_get_project"
    description: str = "Retrieves details for a specific HCP project by its ID."
    parameters: List[ToolParameter] = [
        ToolParameter(name="project_id", type="string", is_required=True, description="The UUID of the project."),
    ]

    def __init__(self, client: ResourceManagerClient):
        self.client = client

    async def __call__(self, **kwargs: Any) -> Tuple[str, Optional[List[HcpProjectResource]]]:
        project_id = kwargs.get("project_id")
        if not project_id:
            return "Error: project_id is required.", None
        
        project_data, error = await self.client.get_project(project_id)
        if error:
            return f"Error getting project {project_id}: {error}", None
        if not project_data or not project_data.get("project"): 
            return f"Project {project_id} not found or no data.", None
        
        resource = HcpProjectResource.from_api_response(project_data["project"])
        return f"Successfully retrieved project: {resource.name} ({resource.id})", [resource]

class GetOrganizationIamPolicyTool(Tool):
    name: str = "hcp_get_organization_iam_policy"
    description: str = "Retrieves the IAM policy for a specific HCP organization."
    parameters: List[ToolParameter] = [
        ToolParameter(name="organization_id", type="string", is_required=True, description="The UUID of the organization."),
    ]

    def __init__(self, client: ResourceManagerClient):
        self.client = client

    async def __call__(self, **kwargs: Any) -> Tuple[str, Optional[List[HcpIamPolicyResource]]]:
        org_id = kwargs.get("organization_id")
        if not org_id:
            return "Error: organization_id is required.", None
        
        policy_data, error = await self.client.get_organization_iam_policy(org_id)
        if error:
            return f"Error getting IAM policy for organization {org_id}: {error}", None
        if not policy_data or not policy_data.get("policy"):
            return f"No IAM policy found for organization {org_id} or no data.", None
        
        resource = HcpIamPolicyResource.from_api_response(policy_data["policy"], f"organizations/{org_id}")
        return f"Successfully retrieved IAM policy for organization {org_id}.", [resource]

class SetOrganizationIamPolicyTool(Tool):
    name: str = "hcp_set_organization_iam_policy"
    description: str = "Sets the IAM policy for a specific HCP organization. Replaces the entire policy. Requires etag from existing policy."
    parameters: List[ToolParameter] = [
        ToolParameter(name="organization_id", type="string", is_required=True, description="The UUID of the organization."),
        ToolParameter(name="policy_bindings_json", type="string", is_required=True, description="JSON string of the policy bindings array. E.g., '[{\"role_id\": \"roles/admin\", \"members\": [{\"member_type\": \"USER\", \"member_id\": \"user-uuid\"}]}]'"),
        ToolParameter(name="etag", type="string", is_required=True, description="The etag of the current policy. Use an empty string if no policy exists."),
    ]

    def __init__(self, client: ResourceManagerClient):
        self.client = client

    async def __call__(self, **kwargs: Any) -> Tuple[str, Optional[List[HcpIamPolicyResource]]]:
        import json 
        org_id = kwargs.get("organization_id")
        policy_bindings_json = kwargs.get("policy_bindings_json")
        etag = kwargs.get("etag")

        if not all([org_id, policy_bindings_json, etag is not None]): 
            return "Error: organization_id, policy_bindings_json, and etag are required.", None
        
        try:
            bindings = json.loads(policy_bindings_json)
        except json.JSONDecodeError:
            return "Error: Invalid JSON format for policy_bindings_json.", None

        policy_payload = {"bindings": bindings, "etag": etag}
        updated_policy_data, error = await self.client.set_organization_iam_policy(org_id, policy_payload)
        
        if error:
            return f"Error setting IAM policy for organization {org_id}: {error}", None
        if not updated_policy_data or not updated_policy_data.get("policy"):
            return f"Failed to set IAM policy for organization {org_id} or no data returned.", None
        
        resource = HcpIamPolicyResource.from_api_response(updated_policy_data["policy"], f"organizations/{org_id}")
        return f"Successfully set IAM policy for organization {org_id}.", [resource]


class GetProjectIamPolicyTool(Tool):
    name: str = "hcp_get_project_iam_policy"
    description: str = "Retrieves the IAM policy for a specific HCP project."
    parameters: List[ToolParameter] = [
        ToolParameter(name="project_id", type="string", is_required=True, description="The UUID of the project."),
    ]

    def __init__(self, client: ResourceManagerClient):
        self.client = client

    async def __call__(self, **kwargs: Any) -> Tuple[str, Optional[List[HcpIamPolicyResource]]]:
        project_id = kwargs.get("project_id")
        if not project_id:
            return "Error: project_id is required.", None
        
        policy_data, error = await self.client.get_project_iam_policy(project_id)
        if error:
            return f"Error getting IAM policy for project {project_id}: {error}", None
        if not policy_data or not policy_data.get("policy"):
            return f"No IAM policy found for project {project_id} or no data.", None
        
        resource = HcpIamPolicyResource.from_api_response(policy_data["policy"], f"projects/{project_id}")
        return f"Successfully retrieved IAM policy for project {project_id}.", [resource]

class SetProjectIamPolicyTool(Tool):
    name: str = "hcp_set_project_iam_policy"
    description: str = "Sets the IAM policy for a specific HCP project. Replaces the entire policy. Requires etag from existing policy."
    parameters: List[ToolParameter] = [
        ToolParameter(name="project_id", type="string", is_required=True, description="The UUID of the project."),
        ToolParameter(name="policy_bindings_json", type="string", is_required=True, description="JSON string of the policy bindings array. E.g., '[{\"role_id\": \"roles/viewer\", \"members\": [{\"member_type\": \"SERVICE_PRINCIPAL\", \"member_id\": \"sp-uuid\"}]}]'"),
        ToolParameter(name="etag", type="string", is_required=True, description="The etag of the current policy. Use an empty string if no policy exists."),
    ]
    def __init__(self, client: ResourceManagerClient):
        self.client = client

    async def __call__(self, **kwargs: Any) -> Tuple[str, Optional[List[HcpIamPolicyResource]]]:
        import json
        project_id = kwargs.get("project_id")
        policy_bindings_json = kwargs.get("policy_bindings_json")
        etag = kwargs.get("etag")

        if not all([project_id, policy_bindings_json, etag is not None]):
            return "Error: project_id, policy_bindings_json, and etag are required.", None
        
        try:
            bindings = json.loads(policy_bindings_json)
        except json.JSONDecodeError:
            return "Error: Invalid JSON format for policy_bindings_json.", None

        policy_payload = {"bindings": bindings, "etag": etag}
        updated_policy_data, error = await self.client.set_project_iam_policy(project_id, policy_payload)
        
        if error:
            return f"Error setting IAM policy for project {project_id}: {error}", None
        if not updated_policy_data or not updated_policy_data.get("policy"):
            return f"Failed to set IAM policy for project {project_id} or no data returned.", None
        
        resource = HcpIamPolicyResource.from_api_response(updated_policy_data["policy"], f"projects/{project_id}")
        return f"Successfully set IAM policy for project {project_id}.", [resource]

