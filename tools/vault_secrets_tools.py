# tools/vault_secrets_tools.py
import logging
from typing import Dict, Any, Tuple, List, Optional

# Imports from the official MCP SDK
from mcp.tools import Tool, ToolParameter
from mcp.common import Resource # For type hinting

from vault_secrets_client import VaultSecretsClient
from resources.hcp_resources import HcpVaultAppResource, HcpVaultKvSecretResource

logger = logging.getLogger(__name__)

class ListVaultAppsTool(Tool):
    name: str = "hcp_list_vault_apps"
    description: str = "Lists Vault Secrets applications within a project."
    parameters: List[ToolParameter] = [
        ToolParameter(name="organization_id", type="string", is_required=True, description="The UUID of the organization."),
        ToolParameter(name="project_id", type="string", is_required=True, description="The UUID of the project."),
        ToolParameter(name="page_size", type="integer", is_required=False, description="Number of apps to return per page (default 50)."),
        ToolParameter(name="next_page_token", type="string", is_required=False, description="Token for fetching the next page of results."),
    ]

    def __init__(self, client: VaultSecretsClient):
        self.client = client

    async def __call__(self, **kwargs: Any) -> Tuple[str, Optional[List[HcpVaultAppResource]]]:
        org_id = kwargs.get("organization_id")
        project_id = kwargs.get("project_id")
        if not org_id or not project_id:
            return "Error: organization_id and project_id are required.", None
        page_size = kwargs.get("page_size", 50)
        next_page_token = kwargs.get("next_page_token")

        apps_data, new_next_page_token, error = await self.client.list_apps(org_id, project_id, page_size, next_page_token)
        if error:
            return f"Error listing Vault apps for project {project_id}: {error}", None
        if apps_data is None:
             return "Error: No Vault app data received from API.", None

        resources = [HcpVaultAppResource.from_api_response(app) for app in apps_data]
        result_str = f"Found {len(resources)} Vault apps in project {project_id}."
        if new_next_page_token:
            result_str += f" Next page token: {new_next_page_token}"
        return result_str, resources

class CreateVaultAppTool(Tool):
    name: str = "hcp_create_vault_app"
    description: str = "Creates a new Vault Secrets application."
    parameters: List[ToolParameter] = [
        ToolParameter(name="organization_id", type="string", is_required=True, description="The UUID of the organization."),
        ToolParameter(name="project_id", type="string", is_required=True, description="The UUID of the project."),
        ToolParameter(name="app_name", type="string", is_required=True, description="The name for the new Vault Secrets application."),
        ToolParameter(name="description", type="string", is_required=False, description="Optional description for the application."),
    ]

    def __init__(self, client: VaultSecretsClient):
        self.client = client

    async def __call__(self, **kwargs: Any) -> Tuple[str, Optional[List[HcpVaultAppResource]]]:
        org_id = kwargs.get("organization_id")
        project_id = kwargs.get("project_id")
        app_name = kwargs.get("app_name")
        description = kwargs.get("description")

        if not all([org_id, project_id, app_name]):
            return "Error: organization_id, project_id, and app_name are required.", None
        
        app_data, error = await self.client.create_app(org_id, project_id, app_name, description)
        if error:
            return f"Error creating Vault app '{app_name}': {error}", None
        if not app_data or not app_data.get("app"):
             return f"Failed to create Vault app '{app_name}' or no data returned.", None
        
        resource = HcpVaultAppResource.from_api_response(app_data["app"])
        return f"Successfully created Vault app: {resource.name} ({resource.resource_id})", [resource]

class GetVaultAppTool(Tool):
    name: str = "hcp_get_vault_app"
    description: str = "Retrieves a specific Vault Secrets application."
    parameters: List[ToolParameter] = [
        ToolParameter(name="organization_id", type="string", is_required=True, description="The UUID of the organization."),
        ToolParameter(name="project_id", type="string", is_required=True, description="The UUID of the project."),
        ToolParameter(name="app_name", type="string", is_required=True, description="The name of the Vault Secrets application."),
    ]
    def __init__(self, client: VaultSecretsClient): self.client = client
    async def __call__(self, **kwargs: Any) -> Tuple[str, Optional[List[HcpVaultAppResource]]]:
        org_id = kwargs.get("organization_id")
        project_id = kwargs.get("project_id")
        app_name = kwargs.get("app_name")
        if not all([org_id, project_id, app_name]): return "Error: organization_id, project_id, and app_name are required.", None
        data, error = await self.client.get_app(org_id, project_id, app_name)
        if error: return f"Error: {error}", None
        if not data or not data.get("app"): return f"App {app_name} not found.", None
        resource = HcpVaultAppResource.from_api_response(data["app"])
        return f"Vault App {app_name} retrieved.", [resource]

class DeleteVaultAppTool(Tool):
    name: str = "hcp_delete_vault_app"
    description: str = "Deletes a Vault Secrets application."
    parameters: List[ToolParameter] = [
        ToolParameter(name="organization_id", type="string", is_required=True, description="The UUID of the organization."),
        ToolParameter(name="project_id", type="string", is_required=True, description="The UUID of the project."),
        ToolParameter(name="app_name", type="string", is_required=True, description="The name of the Vault Secrets application to delete."),
    ]
    def __init__(self, client: VaultSecretsClient): self.client = client
    async def __call__(self, **kwargs: Any) -> Tuple[str, None]:
        org_id = kwargs.get("organization_id")
        project_id = kwargs.get("project_id")
        app_name = kwargs.get("app_name")
        if not all([org_id, project_id, app_name]): return "Error: organization_id, project_id, and app_name are required.", None
        _, error = await self.client.delete_app(org_id, project_id, app_name)
        if error: return f"Error: {error}", None
        return f"Vault App {app_name} deleted.", None

class CreateVaultKvSecretTool(Tool):
    name: str = "hcp_create_vault_kv_secret"
    description: str = "Creates or updates a KV secret in a Vault Secrets application."
    parameters: List[ToolParameter] = [
        ToolParameter(name="organization_id", type="string", is_required=True, description="The UUID of the organization."),
        ToolParameter(name="project_id", type="string", is_required=True, description="The UUID of the project."),
        ToolParameter(name="app_name", type="string", is_required=True, description="The name of the Vault Secrets application."),
        ToolParameter(name="secret_name", type="string", is_required=True, description="The name/key of the secret."),
        ToolParameter(name="secret_value", type="string", is_required=True, description="The value of the secret."),
    ]
    def __init__(self, client: VaultSecretsClient): self.client = client
    async def __call__(self, **kwargs: Any) -> Tuple[str, Optional[List[HcpVaultKvSecretResource]]]:
        org_id = kwargs.get("organization_id")
        project_id = kwargs.get("project_id")
        app_name = kwargs.get("app_name")
        secret_name = kwargs.get("secret_name")
        secret_value = kwargs.get("secret_value")
        if not all([org_id, project_id, app_name, secret_name, secret_value is not None]):
            return "Error: organization_id, project_id, app_name, secret_name, and secret_value are required.", None
        
        secret_data, error = await self.client.create_kv_secret(org_id, project_id, app_name, secret_name, secret_value)
        if error: return f"Error creating secret '{secret_name}' in app '{app_name}': {error}", None
        if not secret_data or not secret_data.get("secret"): return "Error: Secret data not found in response.", None
        
        resource = HcpVaultKvSecretResource.from_api_response_metadata(secret_data["secret"], app_name, project_id, org_id)
        return f"Secret '{secret_name}' created/updated in app '{app_name}'.", [resource]

class OpenVaultKvSecretTool(Tool):
    name: str = "hcp_open_vault_kv_secret"
    description: str = "Retrieves the value of a KV secret from a Vault Secrets application."
    parameters: List[ToolParameter] = [
        ToolParameter(name="organization_id", type="string", is_required=True, description="The UUID of the organization."),
        ToolParameter(name="project_id", type="string", is_required=True, description="The UUID of the project."),
        ToolParameter(name="app_name", type="string", is_required=True, description="The name of the Vault Secrets application."),
        ToolParameter(name="secret_name", type="string", is_required=True, description="The name/key of the secret to retrieve."),
    ]
    def __init__(self, client: VaultSecretsClient): self.client = client
    async def __call__(self, **kwargs: Any) -> Tuple[str, Optional[List[HcpVaultKvSecretResource]]]:
        org_id = kwargs.get("organization_id")
        project_id = kwargs.get("project_id")
        app_name = kwargs.get("app_name")
        secret_name = kwargs.get("secret_name")
        if not all([org_id, project_id, app_name, secret_name]):
            return "Error: organization_id, project_id, app_name, and secret_name are required.", None

        secret_data, error = await self.client.open_kv_secret(org_id, project_id, app_name, secret_name)
        if error: return f"Error opening secret '{secret_name}' in app '{app_name}': {error}", None
        if not secret_data or not secret_data.get("secret"): return f"Secret '{secret_name}' not found or no data in app '{app_name}'.", None
        
        resource = HcpVaultKvSecretResource.from_api_response_open(secret_data["secret"], app_name, project_id, org_id)
        return f"Secret '{secret_name}' retrieved from app '{app_name}'. Value: [REDACTED]", [resource]


class DeleteVaultKvSecretTool(Tool):
    name: str = "hcp_delete_vault_kv_secret"
    description: str = "Deletes a KV secret from a Vault Secrets application."
    parameters: List[ToolParameter] = [
        ToolParameter(name="organization_id", type="string", is_required=True, description="The UUID of the organization."),
        ToolParameter(name="project_id", type="string", is_required=True, description="The UUID of the project."),
        ToolParameter(name="app_name", type="string", is_required=True, description="The name of the Vault Secrets application."),
        ToolParameter(name="secret_name", type="string", is_required=True, description="The name/key of the secret to delete."),
    ]
    def __init__(self, client: VaultSecretsClient): self.client = client
    async def __call__(self, **kwargs: Any) -> Tuple[str, None]:
        org_id = kwargs.get("organization_id")
        project_id = kwargs.get("project_id")
        app_name = kwargs.get("app_name")
        secret_name = kwargs.get("secret_name")
        if not all([org_id, project_id, app_name, secret_name]):
            return "Error: organization_id, project_id, app_name, and secret_name are required.", None
        
        _, error = await self.client.delete_kv_secret(org_id, project_id, app_name, secret_name)
        if error: return f"Error deleting secret '{secret_name}' in app '{app_name}': {error}", None
        return f"Secret '{secret_name}' deleted from app '{app_name}'.", None

class ListVaultAppSecretsTool(Tool):
    name: str = "hcp_list_vault_app_secrets"
    description: str = "Lists secrets within a Vault Secrets application."
    parameters: List[ToolParameter] = [
        ToolParameter(name="organization_id", type="string", is_required=True, description="The UUID of the organization."),
        ToolParameter(name="project_id", type="string", is_required=True, description="The UUID of the project."),
        ToolParameter(name="app_name", type="string", is_required=True, description="The name of the Vault Secrets application."),
        ToolParameter(name="page_size", type="integer", is_required=False, description="Number of secrets to return per page (default 50)."),
        ToolParameter(name="next_page_token", type="string", is_required=False, description="Token for fetching the next page of results."),
    ]
    def __init__(self, client: VaultSecretsClient): self.client = client
    async def __call__(self, **kwargs: Any) -> Tuple[str, Optional[List[HcpVaultKvSecretResource]]]:
        org_id = kwargs.get("organization_id")
        project_id = kwargs.get("project_id")
        app_name = kwargs.get("app_name")
        if not all([org_id, project_id, app_name]):
            return "Error: organization_id, project_id, and app_name are required.", None
        page_size = kwargs.get("page_size", 50)
        next_page_token = kwargs.get("next_page_token")

        secrets_data, new_next_page_token, error = await self.client.list_app_secrets(org_id, project_id, app_name, page_size, next_page_token)
        if error: return f"Error listing secrets for app '{app_name}': {error}", None
        if secrets_data is None: return "Error: No secret data received.", None
        
        resources = [HcpVaultKvSecretResource.from_api_response_metadata(s, app_name, project_id, org_id) for s in secrets_data]
        result_str = f"Found {len(resources)} secrets in app '{app_name}'."
        if new_next_page_token: result_str += f" Next page token: {new_next_page_token}"
        return result_str, resources

