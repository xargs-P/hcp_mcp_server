import httpx
from hcp.auth import get_access_token

RESOURCE_MANAGER_API_VERSION = "2023-06-27"
RESOURCE_MANAGER_API_URL = f"https://api.hashicorp.cloud/resource-manager/{RESOURCE_MANAGER_API_VERSION}"

async def list_projects(organization_id: str):
    """
    Lists all projects in the organization.
    """
    token = await get_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{RESOURCE_MANAGER_API_URL}/organizations/{organization_id}/projects", headers=headers)
        response.raise_for_status()
        return response.json()

async def get_project(organization_id: str, project_id: str):
    """
    Gets a project by its ID.
    """
    token = await get_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{RESOURCE_MANAGER_API_URL}/organizations/{organization_id}/projects/{project_id}", headers=headers)
        response.raise_for_status()
        return response.json()

async def delete_project(organization_id: str, project_id: str):
    """
    Deletes a project by its ID.
    """
    token = await get_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{RESOURCE_MANAGER_API_URL}/organizations/{organization_id}/projects/{project_id}", headers=headers)
        response.raise_for_status()
        return response.json()

async def create_project(name: str, organization_id: str):
    """
    Creates a new project.
    """
    token = await get_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{RESOURCE_MANAGER_API_URL}/organizations/{organization_id}/projects",
            headers=headers,
            json={"name": name},
        )
        response.raise_for_status()
        return response.json()

async def get_organization(organization_id: str):
    """
    Gets an organization by its ID.
    """
    token = await get_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{RESOURCE_MANAGER_API_URL}/organizations/{organization_id}", headers=headers)
        response.raise_for_status()
        return response.json()

async def list_organizations():
    """
    Lists all organizations.
    """
    token = await get_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{RESOURCE_MANAGER_API_URL}/organizations", headers=headers)
        response.raise_for_status()
        return response.json()

async def update_project(organization_id: str, project_id: str, name: str):
    """
    Updates a project's name.
    """
    token = await get_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        response = await client.put(
            f"{RESOURCE_MANAGER_API_URL}/organizations/{organization_id}/projects/{project_id}",
            headers=headers,
            json={"name": name},
        )
        response.raise_for_status()
        return response.json()

async def update_organization(organization_id: str, name: str):
    """
    Updates an organization's name.
    """
    token = await get_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        response = await client.put(
            f"{RESOURCE_MANAGER_API_URL}/organizations/{organization_id}",
            headers=headers,
            json={"name": name},
        )
        response.raise_for_status()
        return response.json()
