import httpx
import logging
from hcp.auth import get_access_token

RESOURCE_MANAGER_API_VERSION = "2019-12-10"
RESOURCE_MANAGER_API_URL = f"https://api.hashicorp.cloud/resource-manager/{RESOURCE_MANAGER_API_VERSION}"
hcp_logger = logging.getLogger("hcp_api")

async def list_projects(organization_id: str):
    """
    Lists all projects in the organization.
    """
    token = await get_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{RESOURCE_MANAGER_API_URL}/projects?scope.type=ORGANIZATION&scope.id={organization_id}", headers=headers)
        response.raise_for_status()
        projects = response.json()
        hcp_logger.info(projects)
        return projects

async def get_project(project_id: str, organization_id: str = None):
    """
    Gets a project by its ID.
    """
    token = await get_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{RESOURCE_MANAGER_API_URL}/projects/{project_id}", headers=headers)
        response.raise_for_status()
        project = response.json()
        hcp_logger.info(project)
        return project

async def delete_project(project_id: str, organization_id: str = None):
    """
    Deletes a project by its ID.
    """
    token = await get_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{RESOURCE_MANAGER_API_URL}/projects/{project_id}", headers=headers)
        response.raise_for_status()
        result = response.json()
        hcp_logger.info(result)
        return result

async def create_project(name: str, organization_id: str):
    """
    Creates a new project.
    """
    token = await get_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{RESOURCE_MANAGER_API_URL}/projects",
            headers=headers,
            json={"name": name, "parent": {"type": "ORGANIZATION", "id": organization_id}},
        )
        response.raise_for_status()
        project = response.json()
        hcp_logger.info(project)
        return project

async def get_organization(organization_id: str):
    """
    Gets an organization by its ID.
    """
    token = await get_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{RESOURCE_MANAGER_API_URL}/organizations/{organization_id}", headers=headers)
        response.raise_for_status()
        organization = response.json()
        hcp_logger.info(organization)
        return organization

async def list_organizations():
    """
    Lists all organizations.
    """
    token = await get_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{RESOURCE_MANAGER_API_URL}/organizations", headers=headers)
        response.raise_for_status()
        organizations = response.json().get("organizations", [])
        hcp_logger.info(organizations)
    return {"organizations": organizations}

async def update_project(project_id: str, name: str, organization_id: str = None):
    """
    Updates a project's name.
    """
    token = await get_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        response = await client.put(
            f"{RESOURCE_MANAGER_API_URL}/projects/{project_id}/name",
            headers=headers,
            json={"name": name},
        )
        response.raise_for_status()
        project = response.json()
        hcp_logger.info(project)
        return project

async def update_organization(organization_id: str, name: str):
    """
    Updates an organization's name.
    """
    token = await get_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        response = await client.put(
            f"{RESOURCE_MANAGER_API_URL}/organizations/{organization_id}/name",
            headers=headers,
            json={"name": name},
        )
        response.raise_for_status()
        organization = response.json()
        hcp_logger.info(organization)
        return organization

async def list_resources(project_id: str):
    """
    Lists all resources in a project.
    """
    token = await get_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{RESOURCE_MANAGER_API_URL}/resources?scope.type=PROJECT&scope.id={project_id}",
            headers=headers,
        )
        response.raise_for_status()
        resources = response.json()
        hcp_logger.info(resources)
        return resources
