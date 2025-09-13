from pydantic import BaseModel
from typing import List, Callable, Optional

class Tool(BaseModel):
    """
    A tool that can be exposed by the MCP server.
    """
    name: str
    description: str
    function: Callable
    tool_code: Optional[str] = None

def list_projects_tool():
    """
    A tool for listing all HCP projects.
    """
    from hcp.resource_manager import list_projects
    return Tool(
        name="list_projects",
        description="Lists all HCP projects for a given organization.",
        function=list_projects,
        tool_code="""
import httpx
from hcp.auth import get_access_token

async def list_projects(organization_id: str):
    token = await get_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://api.hashicorp.cloud/resource-manager/2023-06-27/organizations/{organization_id}/projects", headers=headers)
        response.raise_for_status()
        return response.json()
"""
    )

def get_project_tool():
    """
    A tool for getting an HCP project by its ID.
    """
    from hcp.resource_manager import get_project
    return Tool(
        name="get_project",
        description="Gets an HCP project by its ID.",
        function=get_project,
        tool_code="""
import httpx
from hcp.auth import get_access_token

async def get_project(organization_id: str, project_id: str):
    token = await get_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://api.hashicorp.cloud/resource-manager/2023-06-27/organizations/{organization_id}/projects/{project_id}", headers=headers)
        response.raise_for_status()
        return response.json()
"""
    )

def delete_project_tool():
    """
    A tool for deleting an HCP project by its ID.
    """
    from hcp.resource_manager import delete_project
    return Tool(
        name="delete_project",
        description="Deletes an HCP project by its ID.",
        function=delete_project,
        tool_code="""
import httpx
from hcp.auth import get_access_token

async def delete_project(organization_id: str, project_id: str):
    token = await get_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"https://api.hashicorp.cloud/resource-manager/2023-06-27/organizations/{organization_id}/projects/{project_id}", headers=headers)
        response.raise_for_status()
        return response.json()
"""
    )

def create_project_tool():
    """
    A tool for creating a new HCP project.
    """
    from hcp.resource_manager import create_project
    return Tool(
        name="create_project",
        description="Creates a new HCP project.",
        function=create_project,
        tool_code="""
import httpx
from hcp.auth import get_access_token

async def create_project(name: str, organization_id: str):
    token = await get_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"https://api.hashicorp.cloud/resource-manager/2023-06-27/organizations/{organization_id}/projects",
            headers=headers,
            json={"name": name},
        )
        response.raise_for_status()
        return response.json()
"""
    )

def update_project_tool():
    """
    A tool for updating an HCP project.
    """
    from hcp.resource_manager import update_project
    return Tool(
        name="update_project",
        description="Updates an HCP project.",
        function=update_project,
        tool_code="""
import httpx
from hcp.auth import get_access_token

async def update_project(organization_id: str, project_id: str, name: str):
    token = await get_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        response = await client.put(
            f"https://api.hashicorp.cloud/resource-manager/2023-06-27/organizations/{organization_id}/projects/{project_id}",
            headers=headers,
            json={"name": name},
        )
        response.raise_for_status()
        return response.json()
"""
    )

def get_organization_tool():
    """
    A tool for getting an HCP organization by its ID.
    """
    from hcp.resource_manager import get_organization
    return Tool(
        name="get_organization",
        description="Gets an HCP organization by its ID.",
        function=get_organization,
        tool_code="""
import httpx
from hcp.auth import get_access_token

async def get_organization(organization_id: str):
    token = await get_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://api.hashicorp.cloud/resource-manager/2023-06-27/organizations/{organization_id}", headers=headers)
        response.raise_for_status()
        return response.json()
"""
    )

def list_organizations_tool():
    """
    A tool for listing all HCP organizations.
    """
    from hcp.resource_manager import list_organizations
    return Tool(
        name="list_organizations",
        description="Lists all HCP organizations.",
        function=list_organizations,
        tool_code="""
import httpx
from hcp.auth import get_access_token

async def list_organizations():
    token = await get_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://api.hashicorp.cloud/resource-manager/2023-06-27/organizations", headers=headers)
        response.raise_for_status()
        return response.json()
"""
    )

def update_organization_tool():
    """
    A tool for updating an HCP organization.
    """
    from hcp.resource_manager import update_organization
    return Tool(
        name="update_organization",
        description="Updates an HCP organization.",
        function=update_organization,
        tool_code="""
import httpx
from hcp.auth import get_access_token

async def update_organization(organization_id: str, name: str):
    token = await get_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        response = await client.put(
            f"https://api.hashicorp.cloud/resource-manager/2023-06-27/organizations/{organization_id}",
            headers=headers,
            json={"name": name},
        )
        response.raise_for_status()
        return response.json()
"""
    )

def list_users_tool():
    """
    A tool for listing all HCP users.
    """
    from hcp.iam import list_users
    return Tool(
        name="list_users",
        description="Lists all HCP users.",
        function=list_users,
        tool_code="""
import httpx
from hcp.auth import get_access_token

async def list_users():
    token = await get_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://api.hashicorp.cloud/iam/2023-06-27/users", headers=headers)
        response.raise_for_status()
        return response.json()
"""
    )

def get_user_tool():
    """
    A tool for getting an HCP user by their ID.
    """
    from hcp.iam import get_user
    return Tool(
        name="get_user",
        description="Gets an HCP user by their ID.",
        function=get_user,
        tool_code="""
import httpx
from hcp.auth import get_access_token

async def get_user(user_id: str):
    token = await get_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://api.hashicorp.cloud/iam/2023-06-27/users/{user_id}", headers=headers)
        response.raise_for_status()
        return response.json()
"""
    )

def delete_user_tool():
    """
    A tool for deleting an HCP user by their ID.
    """
    from hcp.iam import delete_user
    return Tool(
        name="delete_user",
        description="Deletes an HCP user by their ID.",
        function=delete_user,
        tool_code="""
import httpx
from hcp.auth import get_access_token

async def delete_user(user_id: str):
    token = await get_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"https://api.hashicorp.cloud/iam/2023-06-27/users/{user_id}", headers=headers)
        response.raise_for_status()
        return response.json()
"""
    )

def create_user_tool():
    """
    A tool for creating a new HCP user.
    """
    from hcp.iam import create_user
    return Tool(
        name="create_user",
        description="Creates a new HCP user.",
        function=create_user,
        tool_code="""
import httpx
from hcp.auth import get_access_token

async def create_user(name: str, email: str):
    token = await get_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"https://api.hashicorp.cloud/iam/2023-06-27/users",
            headers=headers,
            json={"name": name, "email": email},
        )
        response.raise_for_status()
        return response.json()
"""
    )

def update_user_tool():
    """
    A tool for updating an HCP user.
    """
    from hcp.iam import update_user
    return Tool(
        name="update_user",
        description="Updates an HCP user.",
        function=update_user,
        tool_code="""
import httpx
from hcp.auth import get_access_token

async def update_user(user_id: str, name: str):
    token = await get_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        response = await client.put(
            f"https://api.hashicorp.cloud/iam/2023-06-27/users/{user_id}",
            headers=headers,
            json={"name": name},
        )
        response.raise_for_status()
        return response.json()
"""
    )

def list_secrets_tool():
    """
    A tool for listing all secrets for a given application.
    """
    from hcp.vault import list_secrets
    return Tool(
        name="list_secrets",
        description="Lists all secrets for a given application.",
        function=list_secrets,
        tool_code="""
import httpx
from hcp.auth import get_access_token

async def list_secrets(project_id: str, app_name: str):
    token = await get_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.hashicorp.cloud/vault/2023-06-27/projects/{project_id}/apps/{app_name}/secrets", headers=headers
        )
        response.raise_for_status()
        return response.json()
"""
    )

def get_secret_tool():
    """
    A tool for getting a secret by its name.
    """
    from hcp.vault import get_secret
    return Tool(
        name="get_secret",
        description="Gets a secret by its name.",
        function=get_secret,
        tool_code="""
import httpx
from hcp.auth import get_access_token

async def get_secret(project_id: str, app_name: str, secret_name: str):
    token = await get_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.hashicorp.cloud/vault/2023-06-27/projects/{project_id}/apps/{app_name}/secrets/{secret_name}", headers=headers
        )
        response.raise_for_status()
        return response.json()
"""
    )

def delete_secret_tool():
    """
    A tool for deleting a secret by its name.
    """
    from hcp.vault import delete_secret
    return Tool(
        name="delete_secret",
        description="Deletes a secret by its name.",
        function=delete_secret,
        tool_code="""
import httpx
from hcp.auth import get_access_token

async def delete_secret(project_id: str, app_name: str, secret_name: str):
    token = await get_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        response = await client.delete(
            f"https://api.hashicorp.cloud/vault/2023-06-27/projects/{project_id}/apps/{app_name}/secrets/{secret_name}", headers=headers
        )
        response.raise_for_status()
        return response.json()
"""
    )

def create_secret_tool():
    """
    A tool for creating a new secret.
    """
    from hcp.vault import create_secret
    return Tool(
        name="create_secret",
        description="Creates a new secret.",
        function=create_secret,
        tool_code="""
import httpx
from hcp.auth import get_access_token

async def create_secret(project_id: str, app_name: str, secret_name: str, secret_value: str):
    token = await get_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"https://api.hashicorp.cloud/vault/2023-06-27/projects/{project_id}/apps/{app_name}/secrets",
            headers=headers,
            json={"name": secret_name, "value": secret_value},
        )
        response.raise_for_status()
        return response.json()
"""
    )

def update_secret_tool():
    """
    A tool for updating a secret.
    """
    from hcp.vault import update_secret
    return Tool(
        name="update_secret",
        description="Updates a secret.",
        function=update_secret,
        tool_code="""
import httpx
from hcp.auth import get_access_token

async def update_secret(project_id: str, app_name: str, secret_name: str, secret_value: str):
    token = await get_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        response = await client.put(
            f"https://api.hashicorp.cloud/vault/2023-06-27/projects/{project_id}/apps/{app_name}/secrets/{secret_name}",
            headers=headers,
            json={"value": secret_value},
        )
        response.raise_for_status()
        return response.json()
"""
    )

def get_project_by_name_tool():
    """
    A tool for getting an HCP project by its name.
    """
    from utils.finders import find_project_by_name
    return Tool(
        name="get_project_by_name",
        description="Gets an HCP project by its name.",
        function=find_project_by_name,
        tool_code="""
from hcp.resource_manager import list_projects

async def find_project_by_name(organization_id: str, name: str):
    projects = await list_projects(organization_id)
    for proj in projects.get("projects", []):
        if proj.get("name") == name:
            return proj
    return None
"""
    )

def get_user_by_email_tool():
    """
    A tool for getting an HCP user by their email.
    """
    from utils.finders import find_user_by_email
    return Tool(
        name="get_user_by_email",
        description="Gets an HCP user by their email.",
        function=find_user_by_email,
        tool_code="""
from hcp.iam import list_users

async def find_user_by_email(email: str):
    users = await list_users()
    for user in users.get("users", []):
        if user.get("email") == email:
            return user
    return None
"""
    )

def get_organization_by_name_tool():
    """
    A tool for getting an HCP organization by its name.
    """
    from utils.finders import find_organization_by_name
    return Tool(
        name="get_organization_by_name",
        description="Gets an HCP organization by its name.",
        function=find_organization_by_name,
        tool_code="""
from hcp.resource_manager import list_organizations

async def find_organization_by_name(name: str):
    organizations = await list_organizations()
    for org in organizations.get("organizations", []):
        if org.get("name") == name:
            return org
    return None
"""
    )