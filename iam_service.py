# iam_service.py
"""
HCP IAM Service: MCP resource definitions, tool functions, and tool registrations.
This module provides the MCP interface for interacting with HCP IAM APIs.
"""
from typing import Dict, Any, Optional

# Assuming hcp_client.py and mcp_defs.py are in the same directory or accessible
from hcp_client import HCPClient
from mcp_defs import MCPTool, MCP_TOOLS, MCP_RESOURCES
from config import IAM_API_VERSION # API version for IAM

# --- Define IAM Resource types for MCP ---
# These entries help the LLM understand the types of resources it's dealing with.
MCP_RESOURCES["hcp:iam:user"] = {"description": "An HCP User Principal, representing a human user."}
MCP_RESOURCES["hcp:iam:serviceprincipal"] = {"description": "An HCP Service Principal, representing a machine user or application."}
MCP_RESOURCES["hcp:iam:serviceprincipalkey"] = {"description": "A key associated with an HCP Service Principal, used for authentication."}
MCP_RESOURCES["hcp:iam:group"] = {"description": "An HCP IAM Group, used to manage permissions for multiple principals."}
# Organization and Project are primarily Resource Manager entities but are crucial context for IAM.
MCP_RESOURCES["hcp:iam:context:organization"] = {"description": "An HCP Organization, as a scope for IAM resources."}
MCP_RESOURCES["hcp:iam:context:project"] = {"description": "An HCP Project, as a scope for IAM resources."}


# Initialize a dedicated HCPClient instance for the IAM service.
# This could also be a shared client instance if preferred.
hcp_iam_client = HCPClient()

# --- Tool Functions for IAM Service ---

def list_users_by_organization(organization_id: str, page_size: Optional[int] = None, next_page_token: Optional[str] = None) -> Dict[str, Any]:
    """
    Lists user principals within a given HCP organization.
    Maps to HCP IAM API: GET /iam/{IAM_API_VERSION}/organizations/{organization_id}/user-principals
    (Corresponds to IamService_ListUserPrincipalsByOrganization in Swagger)
    """
    path = f"/iam/{IAM_API_VERSION}/organizations/{organization_id}/user-principals"
    params: Dict[str, Any] = {}
    if page_size is not None: # Ensure page_size=0 is not sent if not intended
        params["pagination.page_size"] = page_size
    if next_page_token:
        params["pagination.next_page_token"] = next_page_token
    
    api_response = hcp_iam_client.get(path, params=params)
    
    if api_response.get("error"):
        return {"success": False, "error": api_response["error"], "status_code": api_response.get("status_code"), "details": api_response.get("details")}
    return {"success": True, "data": api_response.get("data"), "status_code": api_response.get("status_code")}

def get_caller_identity() -> Dict[str, Any]:
    """
    Retrieves the identity (user or service principal) of the current authenticated caller.
    Maps to HCP IAM API: GET /iam/{IAM_API_VERSION}/caller-identity
    (Corresponds to IamService_GetCallerIdentity in Swagger)
    """
    path = f"/iam/{IAM_API_VERSION}/caller-identity"
    api_response = hcp_iam_client.get(path)

    if api_response.get("error"):
        return {"success": False, "error": api_response["error"], "status_code": api_response.get("status_code"), "details": api_response.get("details")}
    return {"success": True, "data": api_response.get("data"), "status_code": api_response.get("status_code")}

def create_organization_service_principal(organization_id: str, name: str) -> Dict[str, Any]:
    """
    Creates a new service principal at the organization level.
    Maps to HCP IAM API: POST /iam/{IAM_API_VERSION}/organizations/{organization_id}/service-principals
    (Corresponds to ServicePrincipalsService_CreateOrganizationServicePrincipal in Swagger)
    """
    path = f"/iam/{IAM_API_VERSION}/organizations/{organization_id}/service-principals"
    payload = {"name": name}
    api_response = hcp_iam_client.post(path, data=payload)

    if api_response.get("error"):
        return {"success": False, "error": api_response["error"], "status_code": api_response.get("status_code"), "details": api_response.get("details")}
    return {"success": True, "data": api_response.get("data"), "status_code": api_response.get("status_code")}

def create_organization_service_principal_key(organization_id: str, principal_id: str) -> Dict[str, Any]:
    """
    Creates a key for an organization-level service principal.
    The client_secret is returned ONLY upon creation and is highly sensitive.
    Maps to HCP IAM API: POST /iam/{IAM_API_VERSION}/organizations/{organization_id}/service-principal-keys
    (Corresponds to ServicePrincipalsService_CreateOrganizationServicePrincipalKey in Swagger)
    """
    path = f"/iam/{IAM_API_VERSION}/organizations/{organization_id}/service-principal-keys"
    payload = {"principal_id": principal_id} # As per CreateOrganizationServicePrincipalKeyRequest
    api_response = hcp_iam_client.post(path, data=payload)

    if api_response.get("error"):
        return {"success": False, "error": api_response["error"], "status_code": api_response.get("status_code"), "details": api_response.get("details")}
    
    # Add a specific message about the client_secret
    response_data = api_response.get("data", {})
    if "client_secret" in response_data:
        response_data["_message_to_user"] = "IMPORTANT: The 'client_secret' for the service principal key is displayed now and will NOT be shown again. Please copy and store it securely."
    
    return {"success": True, "data": response_data, "status_code": api_response.get("status_code")}

# --- Register Tools with MCP ---
MCP_TOOLS["iam_list_users_by_organization"] = MCPTool(
    name="iam_list_users_by_organization",
    description="Lists user principals (human users) within a specified HCP organization.",
    input_schema={
        "type": "object",
        "properties": {
            "organization_id": {"type": "string", "description": "The UUID of the HCP organization."},
            "page_size": {"type": "integer", "description": "Optional. Maximum number of results to return per page."},
            "next_page_token": {"type": "string", "description": "Optional. Token to retrieve the next page of results."},
        },
        "required": ["organization_id"],
    },
    func=list_users_by_organization,
)

MCP_TOOLS["iam_get_caller_identity"] = MCPTool(
    name="iam_get_caller_identity",
    description="Retrieves details about the identity (user or service principal) currently making requests via this MCP server.",
    input_schema={"type": "object", "properties": {}}, # No input parameters needed
    func=get_caller_identity,
)

MCP_TOOLS["iam_create_organization_service_principal"] = MCPTool(
    name="iam_create_organization_service_principal",
    description="Creates a new service principal (machine user) at the organization level.",
    input_schema={
        "type": "object",
        "properties": {
            "organization_id": {"type": "string", "description": "The UUID of the HCP organization where the service principal will be created."},
            "name": {"type": "string", "description": "A descriptive name for the new service principal."},
        },
        "required": ["organization_id", "name"],
    },
    func=create_organization_service_principal,
)

MCP_TOOLS["iam_create_organization_service_principal_key"] = MCPTool(
    name="iam_create_organization_service_principal_key",
    description="Creates an authentication key (client ID and client secret) for an existing organization-level service principal. The client_secret is highly sensitive and shown only once upon creation.",
    input_schema={
        "type": "object",
        "properties": {
            "organization_id": {"type": "string", "description": "The UUID of the HCP organization."},
            "principal_id": {"type": "string", "description": "The ID (UUID) of the service principal for which to create the key."},
        },
        "required": ["organization_id", "principal_id"],
    },
    func=create_organization_service_principal_key,
)

# Placeholder for a tool that might be needed for name-to-ID resolution.
# The actual implementation would involve listing organizations and filtering by name.
# MCP_TOOLS["iam_find_organization_id_by_name"] = MCPTool(
#     name="iam_find_organization_id_by_name",
#     description="Finds an organization's UUID by its display name. (Conceptual - requires listing and filtering)",
#     input_schema={
#         "type": "object",
#         "properties": {"organization_name": {"type": "string", "description": "The display name of the organization."}},
#         "required": ["organization_name"],
#     },
#     func=lambda organization_name: {"success": False, "error": "Not yet implemented. Use resourcemanager_list_organizations and filter manually."}
# )

print("HCP IAM Service: Resources and Tools registered.")

