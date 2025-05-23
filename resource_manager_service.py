# resource_manager_service.py
"""
HCP Resource Manager Service: MCP resource definitions, tool functions, and tool registrations.
Provides the MCP interface for managing HCP organizations and projects.
"""
from typing import Dict, Any, Optional

from hcp_client import HCPClient
from mcp_defs import MCPTool, MCP_TOOLS, MCP_RESOURCES
from config import RESOURCE_MANAGER_API_VERSION # API version for Resource Manager

# --- Define Resource Manager Resource types for MCP ---
MCP_RESOURCES["hcp:resourcemanager:organization"] = {"description": "An HCP Organization, the root of the resource hierarchy."}
MCP_RESOURCES["hcp:resourcemanager:project"] = {"description": "An HCP Project, a container for cloud resources within an organization."}
MCP_RESOURCES["hcp:resourcemanager:policy"] = {"description": "An IAM Policy document associated with an organization or project."}
MCP_RESOURCES["hcp:resourcemanager:role"] = {"description": "An IAM Role definition."}

hcp_rm_client = HCPClient()

# --- Tool Functions for Resource Manager Service ---

def list_organizations(page_size: Optional[int] = None, next_page_token: Optional[str] = None) -> Dict[str, Any]:
    """
    Lists all HCP organizations that the authenticated principal has access to.
    Maps to HCP Resource Manager API: GET /resource-manager/{API_VERSION}/organizations
    (Corresponds to OrganizationService_List in Swagger)
    """
    path = f"/resource-manager/{RESOURCE_MANAGER_API_VERSION}/organizations"
    params: Dict[str, Any] = {}
    if page_size is not None:
        params["pagination.page_size"] = page_size
    if next_page_token:
        params["pagination.next_page_token"] = next_page_token
    
    api_response = hcp_rm_client.get(path, params=params)

    if api_response.get("error"):
        return {"success": False, "error": api_response["error"], "status_code": api_response.get("status_code"), "details": api_response.get("details")}
    return {"success": True, "data": api_response.get("data"), "status_code": api_response.get("status_code")}

def get_organization_by_id(id: str) -> Dict[str, Any]:
    """
    Retrieves details for a specific HCP organization by its UUID.
    Maps to HCP Resource Manager API: GET /resource-manager/{API_VERSION}/organizations/{id}
    (Corresponds to OrganizationService_Get in Swagger)
    """
    path = f"/resource-manager/{RESOURCE_MANAGER_API_VERSION}/organizations/{id}"
    api_response = hcp_rm_client.get(path)

    if api_response.get("error"):
        return {"success": False, "error": api_response["error"], "status_code": api_response.get("status_code"), "details": api_response.get("details")}
    return {"success": True, "data": api_response.get("data"), "status_code": api_response.get("status_code")}

def list_projects(organization_id: Optional[str] = None, page_size: Optional[int] = None, next_page_token: Optional[str] = None) -> Dict[str, Any]:
    """
    Lists HCP projects. Can be scoped to an organization or list all accessible projects.
    Maps to HCP Resource Manager API: GET /resource-manager/{API_VERSION}/projects
    (Corresponds to ProjectService_List in Swagger)
    The 'scope.type' and 'scope.id' parameters are used if organization_id is provided.
    """
    path = f"/resource-manager/{RESOURCE_MANAGER_API_VERSION}/projects"
    params: Dict[str, Any] = {}
    if organization_id:
        params["scope.type"] = "ORGANIZATION" # As per ProjectListRequest in Swagger
        params["scope.id"] = organization_id
    if page_size is not None:
        params["pagination.page_size"] = page_size
    if next_page_token:
        params["pagination.next_page_token"] = next_page_token
        
    api_response = hcp_rm_client.get(path, params=params)

    if api_response.get("error"):
        return {"success": False, "error": api_response["error"], "status_code": api_response.get("status_code"), "details": api_response.get("details")}
    return {"success": True, "data": api_response.get("data"), "status_code": api_response.get("status_code")}


def get_project_by_id(id: str) -> Dict[str, Any]:
    """
    Retrieves details for a specific HCP project by its UUID.
    Maps to HCP Resource Manager API: GET /resource-manager/{API_VERSION}/projects/{id}
    (Corresponds to ProjectService_Get in Swagger)
    """
    path = f"/resource-manager/{RESOURCE_MANAGER_API_VERSION}/projects/{id}"
    api_response = hcp_rm_client.get(path)

    if api_response.get("error"):
        return {"success": False, "error": api_response["error"], "status_code": api_response.get("status_code"), "details": api_response.get("details")}
    return {"success": True, "data": api_response.get("data"), "status_code": api_response.get("status_code")}

# --- Register Tools with MCP ---
MCP_TOOLS["resourcemanager_list_organizations"] = MCPTool(
    name="resourcemanager_list_organizations",
    description="Lists all HCP organizations the authenticated caller has access to.",
    input_schema={
        "type": "object",
        "properties": {
            "page_size": {"type": "integer", "description": "Optional. Maximum number of results per page."},
            "next_page_token": {"type": "string", "description": "Optional. Token for the next page of results."},
        },
    },
    func=list_organizations,
)

MCP_TOOLS["resourcemanager_get_organization_by_id"] = MCPTool(
    name="resourcemanager_get_organization_by_id",
    description="Retrieves details for a specific HCP organization using its UUID.",
    input_schema={
        "type": "object",
        "properties": {
            "id": {"type": "string", "description": "The UUID of the organization."},
        },
        "required": ["id"],
    },
    func=get_organization_by_id,
)

MCP_TOOLS["resourcemanager_list_projects"] = MCPTool(
    name="resourcemanager_list_projects",
    description="Lists HCP projects. If organization_id is provided, lists projects within that organization; otherwise, lists all accessible projects.",
    input_schema={
        "type": "object",
        "properties": {
            "organization_id": {"type": "string", "description": "Optional. The UUID of the organization to scope the project listing."},
            "page_size": {"type": "integer", "description": "Optional. Maximum number of results per page."},
            "next_page_token": {"type": "string", "description": "Optional. Token for the next page of results."},
        },
    },
    func=list_projects,
)

MCP_TOOLS["resourcemanager_get_project_by_id"] = MCPTool(
    name="resourcemanager_get_project_by_id",
    description="Retrieves details for a specific HCP project using its UUID.",
    input_schema={
        "type": "object",
        "properties": {
            "id": {"type": "string", "description": "The UUID of the project."},
        },
        "required": ["id"],
    },
    func=get_project_by_id,
)

# Placeholder for finding a project by name - would require listing projects in an org and filtering.
# MCP_TOOLS["resourcemanager_find_project_by_name"] = MCPTool(
# name="resourcemanager_find_project_by_name",
# description="Finds a project's UUID by its name within a specific organization. (Conceptual - requires listing and filtering)",
#     input_schema={
#         "type": "object",
#         "properties": {
# "organization_id": {"type": "string", "description": "The UUID of the organization containing the project."},
# "project_name": {"type": "string", "description": "The display name of the project."}
#         },
#         "required": ["organization_id", "project_name"],
#     },
# func=lambda organization_id, project_name: {"success": False, "error": "Not yet implemented. Use resourcemanager_list_projects and filter manually."}
# )


print("HCP Resource Manager Service: Resources and Tools registered.")

