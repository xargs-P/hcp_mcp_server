# vault_secrets_service.py
"""
HCP Vault Secrets Service: MCP resource definitions, tool functions, and tool registrations.
Provides the MCP interface for managing applications and secrets in HCP Vault Secrets.
"""
from typing import Dict, Any, Optional, List

from hcp_client import HCPClient
from mcp_defs import MCPTool, MCP_TOOLS, MCP_RESOURCES
from config import VAULT_SECRETS_API_VERSION # API version for Vault Secrets

# --- Define Vault Secrets Resource types for MCP ---
MCP_RESOURCES["hcp:vaultsecrets:app"] = {"description": "An HCP Vault Secrets Application, a container for secrets."}
MCP_RESOURCES["hcp:vaultsecrets:secret:kv"] = {"description": "A Key-Value (static) secret within an HCP Vault Secrets Application."}
MCP_RESOURCES["hcp:vaultsecrets:secret:dynamic"] = {"description": "A dynamic secret configuration within an HCP Vault Secrets Application."}
MCP_RESOURCES["hcp:vaultsecrets:secret:rotating"] = {"description": "A rotating secret configuration within an HCP Vault Secrets Application."}
MCP_RESOURCES["hcp:vaultsecrets:integration"] = {"description": "An integration configuration for HCP Vault Secrets (e.g., AWS, GCP)."}
MCP_RESOURCES["hcp:vaultsecrets:sync"] = {"description": "A secret synchronization configuration in HCP Vault Secrets."}


hcp_vs_client = HCPClient()

# --- Tool Functions for Vault Secrets Service ---

def list_secret_apps(organization_id: str, project_id: str, page_size: Optional[int] = None, next_page_token: Optional[str] = None) -> Dict[str, Any]:
    """
    Lists applications within an HCP Vault Secrets project.
    Maps to HCP Vault Secrets API: GET /secrets/{API_VERSION}/organizations/{org_id}/projects/{proj_id}/apps
    (Corresponds to ListApps in Swagger)
    """
    path = f"/secrets/{VAULT_SECRETS_API_VERSION}/organizations/{organization_id}/projects/{project_id}/apps"
    params: Dict[str, Any] = {}
    if page_size is not None:
        params["pagination.page_size"] = page_size
    if next_page_token:
        params["pagination.next_page_token"] = next_page_token
    
    api_response = hcp_vs_client.get(path, params=params)
    
    if api_response.get("error"):
        return {"success": False, "error": api_response["error"], "status_code": api_response.get("status_code"), "details": api_response.get("details")}
    return {"success": True, "data": api_response.get("data"), "status_code": api_response.get("status_code")}

def create_secret_app(organization_id: str, project_id: str, name: str, description: Optional[str] = None, sync_names: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Creates a new application in HCP Vault Secrets.
    Maps to HCP Vault Secrets API: POST /secrets/{API_VERSION}/organizations/{org_id}/projects/{proj_id}/apps
    (Corresponds to CreateApp in Swagger)
    """
    path = f"/secrets/{VAULT_SECRETS_API_VERSION}/organizations/{organization_id}/projects/{project_id}/apps"
    payload: Dict[str, Any] = {"name": name}
    if description:
        payload["description"] = description
    if sync_names: # Optional list of sync configurations to associate with the app
        payload["sync_names"] = sync_names
        
    api_response = hcp_vs_client.post(path, data=payload)
    
    if api_response.get("error"):
        return {"success": False, "error": api_response["error"], "status_code": api_response.get("status_code"), "details": api_response.get("details")}
    return {"success": True, "data": api_response.get("data"), "status_code": api_response.get("status_code")}

def create_app_kv_secret(organization_id: str, project_id: str, app_name: str, name: str, value: str) -> Dict[str, Any]:
    """
    Creates a new Key/Value (static) secret for a specified application.
    Maps to HCP Vault Secrets API: POST /secrets/{API_VERSION}/organizations/{org_id}/projects/{proj_id}/apps/{app_name}/secret/kv
    (Corresponds to CreateAppKVSecret in Swagger)
    """
    path = f"/secrets/{VAULT_SECRETS_API_VERSION}/organizations/{organization_id}/projects/{project_id}/apps/{app_name}/secret/kv"
    payload = {"name": name, "value": value} # Based on CreateAppKVSecretBody
    api_response = hcp_vs_client.post(path, data=payload)

    if api_response.get("error"):
        return {"success": False, "error": api_response["error"], "status_code": api_response.get("status_code"), "details": api_response.get("details")}
    return {"success": True, "data": api_response.get("data"), "status_code": api_response.get("status_code")}

def open_app_secret(organization_id: str, project_id: str, app_name: str, secret_name: str) -> Dict[str, Any]:
    """
    Retrieves the value of the latest version of a specific secret for an application. This reveals sensitive data.
    Maps to HCP Vault Secrets API: GET /secrets/{API_VERSION}/organizations/{org_id}/projects/{proj_id}/apps/{app_name}/secrets/{secret_name}:open
    (Corresponds to OpenAppSecret in Swagger)
    """
    path = f"/secrets/{VAULT_SECRETS_API_VERSION}/organizations/{organization_id}/projects/{project_id}/apps/{app_name}/secrets/{secret_name}:open"
    api_response = hcp_vs_client.get(path)

    if api_response.get("error"):
        return {"success": False, "error": api_response["error"], "status_code": api_response.get("status_code"), "details": api_response.get("details")}
    
    # Add a specific message about the sensitive nature of the data
    response_data = api_response.get("data", {})
    if response_data.get("secret"): # Check if secret data is present
         response_data["_message_to_user"] = "IMPORTANT: The secret value is displayed below. This is sensitive information."
    
    return {"success": True, "data": response_data, "status_code": api_response.get("status_code")}

# --- Register Tools with MCP ---
MCP_TOOLS["vaultsecrets_list_apps"] = MCPTool(
    name="vaultsecrets_list_apps",
    description="Lists applications within an HCP Vault Secrets project, identified by organization and project UUIDs.",
    input_schema={
        "type": "object",
        "properties": {
            "organization_id": {"type": "string", "description": "The UUID of the HCP organization."},
            "project_id": {"type": "string", "description": "The UUID of the HCP project."},
            "page_size": {"type": "integer", "description": "Optional. Maximum number of results per page."},
            "next_page_token": {"type": "string", "description": "Optional. Token to retrieve the next page of results."},
        },
        "required": ["organization_id", "project_id"],
    },
    func=list_secret_apps,
)

MCP_TOOLS["vaultsecrets_create_app"] = MCPTool(
    name="vaultsecrets_create_app",
    description="Creates a new application in HCP Vault Secrets within a specified organization and project.",
    input_schema={
        "type": "object",
        "properties": {
            "organization_id": {"type": "string", "description": "The UUID of the HCP organization."},
            "project_id": {"type": "string", "description": "The UUID of the HCP project."},
            "name": {"type": "string", "description": "The name for the new application."},
            "description": {"type": "string", "description": "Optional. A description for the application."},
            "sync_names": {"type": "array", "items": {"type": "string"}, "description": "Optional. List of sync configuration names to associate with this app."},
        },
        "required": ["organization_id", "project_id", "name"],
    },
    func=create_secret_app,
)

MCP_TOOLS["vaultsecrets_create_app_kv_secret"] = MCPTool(
    name="vaultsecrets_create_app_kv_secret",
    description="Creates a new Key/Value (static) secret within a specified application in HCP Vault Secrets.",
    input_schema={
        "type": "object",
        "properties": {
            "organization_id": {"type": "string", "description": "The UUID of the HCP organization."},
            "project_id": {"type": "string", "description": "The UUID of the HCP project."},
            "app_name": {"type": "string", "description": "The name of the application where the secret will be created."},
            "name": {"type": "string", "description": "The name (key) of the secret to create."},
            "value": {"type": "string", "description": "The sensitive value of the secret."},
        },
        "required": ["organization_id", "project_id", "app_name", "name", "value"],
    },
    func=create_app_kv_secret,
)

MCP_TOOLS["vaultsecrets_open_app_secret"] = MCPTool(
    name="vaultsecrets_open_app_secret",
    description="Retrieves and reveals the value of the latest version of a specific secret for an application. This action exposes sensitive data.",
    input_schema={
        "type": "object",
        "properties": {
            "organization_id": {"type": "string", "description": "The UUID of the HCP organization."},
            "project_id": {"type": "string", "description": "The UUID of the HCP project."},
            "app_name": {"type": "string", "description": "The name of the application containing the secret."},
            "secret_name": {"type": "string", "description": "The name of the secret to open/retrieve."},
        },
        "required": ["organization_id", "project_id", "app_name", "secret_name"],
    },
    func=open_app_secret,
)

print("HCP Vault Secrets Service: Resources and Tools registered.")

