import httpx
import logging
from hcp.auth import get_access_token

IAM_API_VERSION = "2019-12-10"
IAM_API_URL = f"https://api.hashicorp.cloud/iam/{IAM_API_VERSION}"
hcp_logger = logging.getLogger("hcp_api")

async def search_principals(organization_id: str, filter_str: str = None):
    """
    Searches for principals in the organization.
    """
    token = await get_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    params = {}
    if filter_str:
        params["filter"] = filter_str
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{IAM_API_URL}/organizations/{organization_id}/principals/search",
            headers=headers,
            json={"filter": filter_str} if filter_str else {},
        )
        response.raise_for_status()
        principals = response.json()
        hcp_logger.info(principals)
        return principals

async def get_principals(organization_id: str, principal_ids: list[str]):
    """
    Gets principals by their IDs.
    """
    token = await get_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    params = [("principal_ids", pid) for pid in principal_ids]
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{IAM_API_URL}/organizations/{organization_id}/principals",
            headers=headers,
            params=params,
        )
        response.raise_for_status()
        principals = response.json()
        hcp_logger.info(principals)
        return principals

async def delete_service_principal(organization_id: str, principal_id: str):
    """
    Deletes a service principal by its ID.
    """
    token = await get_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        response = await client.delete(
            f"{IAM_API_URL}/iam/organization/{organization_id}/service-principal/{principal_id}",
            headers=headers,
        )
        response.raise_for_status()
        result = response.json()
        hcp_logger.info(result)
        return result

async def create_service_principal(organization_id: str, name: str):
    """
    Creates a new service principal.
    """
    token = await get_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{IAM_API_URL}/iam/organization/{organization_id}/service-principals",
            headers=headers,
            json={"name": name},
        )
        response.raise_for_status()
        principal = response.json()
        hcp_logger.info(principal)
        return principal

async def update_service_principal(organization_id: str, principal_id: str, name: str):
    """
    Updates a service principal's name.
    """
    # The spec does not define an update endpoint for service principals.
    # This is a placeholder.
    raise NotImplementedError("Update service principal is not defined in the spec.")