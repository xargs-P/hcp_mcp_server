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
    list_users,
    get_user,
    delete_user,
    create_user,
    update_user,
)
from hcp.vault import (
    list_secrets,
    get_secret,
    delete_secret,
    create_secret,
    update_secret,
)
from utils.finders import (
    find_project_by_name,
    find_user_by_email,
    find_organization_by_name,
)

def list_projects_tool():
    return Tool(
        name="list_projects",
        title="List Projects",
        description="Lists all HCP projects for a given organization.",
        inputSchema={
            "type": "object",
            "properties": {
                "organization_id": {"type": "string", "description": "The ID of the organization."},
            },
            "required": ["organization_id"],
        },
        outputSchema={
            "type": "object",
            "properties": {
                "projects": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "string", "description": "The ID of the project."},
                            "name": {"type": "string", "description": "The name of the project."},
                        },
                    },
                },
            },
        },
    )

def get_project_tool():
    return Tool(
        name="get_project",
        title="Get Project",
        description="Gets an HCP project by its ID.",
        inputSchema={
            "type": "object",
            "properties": {
                "organization_id": {"type": "string", "description": "The ID of the organization."},
                "project_id": {"type": "string", "description": "The ID of the project."},
            },
            "required": ["organization_id", "project_id"],
        },
    )

def delete_project_tool():
    return Tool(
        name="delete_project",
        title="Delete Project",
        description="Deletes an HCP project by its ID.",
        inputSchema={
            "type": "object",
            "properties": {
                "organization_id": {"type": "string", "description": "The ID of the organization."},
                "project_id": {"type": "string", "description": "The ID of the project."},
            },
            "required": ["organization_id", "project_id"],
        },
    )

def create_project_tool():
    return Tool(
        name="create_project",
        title="Create Project",
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
        title="Update Project",
        description="Updates an HCP project.",
        inputSchema={
            "type": "object",
            "properties": {
                "organization_id": {"type": "string", "description": "The ID of the organization."},
                "project_id": {"type": "string", "description": "The ID of the project."},
                "name": {"type": "string", "description": "The new name of the project."},
            },
            "required": ["organization_id", "project_id", "name"],
        },
    )

def get_organization_tool():
    return Tool(
        name="get_organization",
        title="Get Organization",
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
        title="List Organizations",
        description="Lists all HCP organizations.",
        inputSchema={"type": "object", "properties": {}},
        outputSchema={
            "type": "object",
            "properties": {
                "organizations": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "string", "description": "The ID of the organization."},
                            "name": {"type": "string", "description": "The name of the organization."},
                            "owner": {
                                "type": "object",
                                "description": "The owner of the organization.",
                                "properties": {
                                    "user": {"type": "string", "description": "The user principal ID of the owner."}
                                },
                            },
                            "created_at": {"type": "string", "format": "date-time", "description": "The time the organization was created."},
                            "state": {"type": "string", "description": "The state of the organization."},
                            "tfc_synced": {"type": "boolean", "description": "Whether the organization is synced with TFC."},
                        },
                    },
                },
            },
        },
    )

def update_organization_tool():
    return Tool(
        name="update_organization",
        title="Update Organization",
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

def list_users_tool():
    return Tool(
        name="list_users",
        title="List Users",
        description="Lists all HCP users.",
        inputSchema={"type": "object", "properties": {}},
        outputSchema={
            "type": "object",
            "properties": {
                "users": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "string", "description": "The ID of the user."},
                            "name": {"type": "string", "description": "The name of the user."},
                            "email": {"type": "string", "description": "The email of the user."},
                        },
                    },
                },
            },
        },
    )

def get_user_tool():
    return Tool(
        name="get_user",
        title="Get User",
        description="Gets an HCP user by their ID.",
        inputSchema={
            "type": "object",
            "properties": {
                "user_id": {"type": "string", "description": "The ID of the user."},
            },
            "required": ["user_id"],
        },
    )

def delete_user_tool():
    return Tool(
        name="delete_user",
        title="Delete User",
        description="Deletes an HCP user by their ID.",
        inputSchema={
            "type": "object",
            "properties": {
                "user_id": {"type": "string", "description": "The ID of the user."},
            },
            "required": ["user_id"],
        },
    )

def create_user_tool():
    return Tool(
        name="create_user",
        title="Create User",
        description="Creates a new HCP user.",
        inputSchema={
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "The name of the new user."},
                "email": {"type": "string", "description": "The email of the new user."},
            },
            "required": ["name", "email"],
        },
    )

def update_user_tool():
    return Tool(
        name="update_user",
        title="Update User",
        description="Updates an HCP user.",
        inputSchema={
            "type": "object",
            "properties": {
                "user_id": {"type": "string", "description": "The ID of the user."},
                "name": {"type": "string", "description": "The new name of the user."},
            },
            "required": ["user_id", "name"],
        },
    )

def list_secrets_tool():
    return Tool(
        name="list_secrets",
        title="List Secrets",
        description="Lists all secrets for a given application.",
        inputSchema={
            "type": "object",
            "properties": {
                "project_id": {"type": "string", "description": "The ID of the project."},
                "app_name": {"type": "string", "description": "The name of the application."},
            },
            "required": ["project_id", "app_name"],
        },
        outputSchema={
            "type": "object",
            "properties": {
                "secrets": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string", "description": "The name of the secret."},
                            "value": {"type": "string", "description": "The value of the secret."},
                        },
                    },
                },
            },
        },
    )

def get_secret_tool():
    return Tool(
        name="get_secret",
        title="Get Secret",
        description="Gets a secret by its name.",
        inputSchema={
            "type": "object",
            "properties": {
                "project_id": {"type": "string", "description": "The ID of the project."},
                "app_name": {"type": "string", "description": "The name of the application."},
                "secret_name": {"type": "string", "description": "The name of the secret."},
            },
            "required": ["project_id", "app_name", "secret_name"],
        },
    )

def delete_secret_tool():
    return Tool(
        name="delete_secret",
        title="Delete Secret",
        description="Deletes a secret by its name.",
        inputSchema={
            "type": "object",
            "properties": {
                "project_id": {"type": "string", "description": "The ID of the project."},
                "app_name": {"type": "string", "description": "The name of the application."},
                "secret_name": {"type": "string", "description": "The name of the secret."},
            },
            "required": ["project_id", "app_name", "secret_name"],
        },
    )

def create_secret_tool():
    return Tool(
        name="create_secret",
        title="Create Secret",
        description="Creates a new secret.",
        inputSchema={
            "type": "object",
            "properties": {
                "project_id": {"type": "string", "description": "The ID of the project."},
                "app_name": {"type": "string", "description": "The name of the application."},
                "secret_name": {"type": "string", "description": "The name of the new secret."},
                "secret_value": {"type": "string", "description": "The value of the new secret."},
            },
            "required": ["project_id", "app_name", "secret_name", "secret_value"],
        },
    )

def update_secret_tool():
    return Tool(
        name="update_secret",
        title="Update Secret",
        description="Updates a secret.",
        inputSchema={
            "type": "object",
            "properties": {
                "project_id": {"type": "string", "description": "The ID of the project."},
                "app_name": {"type": "string", "description": "The name of the application."},
                "secret_name": {"type": "string", "description": "The name of the secret."},
                "secret_value": {"type": "string", "description": "The new value of the secret."},
            },
            "required": ["project_id", "app_name", "secret_name", "secret_value"],
        },
    )

def find_project_by_name_tool():
    return Tool(
        name="find_project_by_name",
        title="Find Project by Name",
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
        title="Find User by Email",
        description="Finds a user by their email.",
        inputSchema={
            "type": "object",
            "properties": {
                "email": {"type": "string", "description": "The email of the user."},
            },
            "required": ["email"],
        },
    )

def find_organization_by_name_tool():
    return Tool(
        name="find_organization_by_name",
        title="Find Organization by Name",
        description="Finds an organization by its name.",
        inputSchema={
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "The name of the organization."},
            },
            "required": ["name"],
        },
    )
