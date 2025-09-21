import inspect
from mcp.models import Tool
from hcp.resource_manager import (
    list_projects,
    get_project,
    delete_project,
    create_project,
    update_project,
    get_organization,
    list_organizations,
    update_organization,
)
from hcp.iam import (
    search_principals,
    get_principals,
    delete_service_principal,
    create_service_principal,
    update_service_principal,
)
from hcp.vault import (
    list_secrets,
    get_secret,
    delete_secret,
    create_secret,
)
from utils.finders import (
    find_project_by_name,
    find_user_by_email,
    find_organization_by_name,
)

def list_projects_tool():
    return Tool(
        name="list_projects",
        description="Lists all HCP projects for a given organization.",
        inputSchema={
            "type": "object",
            "properties": {
                "organization_id": {"type": "string", "description": "The ID of the organization."},
            },
            "required": ["organization_id"],
        },
    )

def get_project_tool():
    return Tool(
        name="get_project",
        description="Gets an HCP project by its ID.",
        inputSchema={
            "type": "object",
            "properties": {
                "project_id": {"type": "string", "description": "The ID of the project."},
            },
            "required": ["project_id"],
        },
    )

def delete_project_tool():
    return Tool(
        name="delete_project",
        description="Deletes an HCP project by its ID.",
        inputSchema={
            "type": "object",
            "properties": {
                "project_id": {"type": "string", "description": "The ID of the project."},
            },
            "required": ["project_id"],
        },
    )

def create_project_tool():
    return Tool(
        name="create_project",
        description="Creates a new HCP project.",
        inputSchema={
            "type": "object",
            "properties": {
                "organization_id": {"type": "string", "description": "The ID of the organization."},
                "name": {"type": "string", "description": "The name of the new project."},
            },
            "required": ["organization_id", "name"],
        },
    )

def update_project_tool():
    return Tool(
        name="update_project",
        description="Updates an HCP project.",
        inputSchema={
            "type": "object",
            "properties": {
                "project_id": {"type": "string", "description": "The ID of the project."},
                "name": {"type": "string", "description": "The new name of the project."},
            },
            "required": ["project_id", "name"],
        },
    )

def get_organization_tool():
    return Tool(
        name="get_organization",
        description="Gets an HCP organization by its ID.",
        inputSchema={
            "type": "object",
            "properties": {
                "organization_id": {"type": "string", "description": "The ID of the organization."},
            },
            "required": ["organization_id"],
        },
    )

def list_organizations_tool():
    return Tool(
        name="list_organizations",
        description="Lists all HCP organizations.",
        inputSchema={"type": "object", "properties": {}},
    )

def update_organization_tool():
    return Tool(
        name="update_organization",
        description="Updates an HCP organization.",
        inputSchema={
            "type": "object",
            "properties": {
                "organization_id": {"type": "string", "description": "The ID of the organization."},
                "name": {"type": "string", "description": "The new name of the organization."},
            },
            "required": ["organization_id", "name"],
        },
    )

def search_principals_tool():
    return Tool(
        name="search_principals",
        description="Searches for principals in an organization.",
        inputSchema={
            "type": "object",
            "properties": {
                "organization_id": {"type": "string", "description": "The ID of the organization."},
                "filter_str": {"type": "string", "description": "The filter string to use for the search."},
            },
            "required": ["organization_id"],
        },
    )

def get_principals_tool():
    return Tool(
        name="get_principals",
        description="Gets principals by their IDs.",
        inputSchema={
            "type": "object",
            "properties": {
                "organization_id": {"type": "string", "description": "The ID of the organization."},
                "principal_ids": {"type": "array", "items": {"type": "string"}, "description": "The IDs of the principals to get."},
            },
            "required": ["organization_id", "principal_ids"],
        },
    )

def delete_service_principal_tool():
    return Tool(
        name="delete_service_principal",
        description="Deletes a service principal by its ID.",
        inputSchema={
            "type": "object",
            "properties": {
                "organization_id": {"type": "string", "description": "The ID of the organization."},
                "principal_id": {"type": "string", "description": "The ID of the service principal."},
            },
            "required": ["organization_id", "principal_id"],
        },
    )

def create_service_principal_tool():
    return Tool(
        name="create_service_principal",
        description="Creates a new service principal.",
        inputSchema={
            "type": "object",
            "properties": {
                "organization_id": {"type": "string", "description": "The ID of the organization."},
                "name": {"type": "string", "description": "The name of the new service principal."},
            },
            "required": ["organization_id", "name"],
        },
    )

def update_service_principal_tool():
    return Tool(
        name="update_service_principal",
        description="Updates a service principal.",
        inputSchema={
            "type": "object",
            "properties": {
                "organization_id": {"type": "string", "description": "The ID of the organization."},
                "principal_id": {"type": "string", "description": "The ID of the service principal."},
                "name": {"type": "string", "description": "The new name of the service principal."},
            },
            "required": ["organization_id", "principal_id", "name"],
        },
    )

def list_secrets_tool():
    return Tool(
        name="list_secrets",
        description="Lists all secrets for a given application.",
        inputSchema={
            "type": "object",
            "properties": {
                "organization_id": {"type": "string", "description": "The ID of the organization."},
                "project_id": {"type": "string", "description": "The ID of the project."},
                "app_name": {"type": "string", "description": "The name of the application."},
            },
            "required": ["organization_id", "project_id", "app_name"],
        },
    )

def get_secret_tool():
    return Tool(
        name="get_secret",
        description="Gets a secret by its name.",
        inputSchema={
            "type": "object",
            "properties": {
                "organization_id": {"type": "string", "description": "The ID of the organization."},
                "project_id": {"type": "string", "description": "The ID of the project."},
                "app_name": {"type": "string", "description": "The name of the application."},
                "secret_name": {"type": "string", "description": "The name of the secret."},
            },
            "required": ["organization_id", "project_id", "app_name", "secret_name"],
        },
    )

def delete_secret_tool():
    return Tool(
        name="delete_secret",
        description="Deletes a secret by its name.",
        inputSchema={
            "type": "object",
            "properties": {
                "organization_id": {"type": "string", "description": "The ID of the organization."},
                "project_id": {"type": "string", "description": "The ID of the project."},
                "app_name": {"type": "string", "description": "The name of the application."},
                "secret_name": {"type": "string", "description": "The name of the secret."},
            },
            "required": ["organization_id", "project_id", "app_name", "secret_name"],
        },
    )

def create_secret_tool():
    return Tool(
        name="create_secret",
        description="Creates a new secret.",
        inputSchema={
            "type": "object",
            "properties": {
                "organization_id": {"type": "string", "description": "The ID of the organization."},
                "project_id": {"type": "string", "description": "The ID of the project."},
                "app_name": {"type": "string", "description": "The name of the application."},
                "secret_name": {"type": "string", "description": "The name of the new secret."},
                "secret_value": {"type": "string", "description": "The value of the new secret."},
            },
            "required": ["organization_id", "project_id", "app_name", "secret_name", "secret_value"],
        },
    )

def find_project_by_name_tool():
    return Tool(
        name="find_project_by_name",
        description="Finds a project by its name.",
        inputSchema={
            "type": "object",
            "properties": {
                "organization_id": {"type": "string", "description": "The ID of the organization."},
                "name": {"type": "string", "description": "The name of the project."},
            },
            "required": ["organization_id", "name"],
        },
    )

def find_user_by_email_tool():
    return Tool(
        name="find_user_by_email",
        description="Finds a user by their email.",
        inputSchema={
            "type": "object",
            "properties": {
                "organization_id": {"type": "string", "description": "The ID of the organization."},
                "email": {"type": "string", "description": "The email of the user."},
            },
            "required": ["organization_id", "email"],
        },
    )

def find_organization_by_name_tool():
    return Tool(
        name="find_organization_by_name",
        description="Finds an organization by its name.",
        inputSchema={
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "The name of the organization."},
            },
            "required": ["name"],
        },
    )
