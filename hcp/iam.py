import httpx
import logging
from hcp.auth import get_access_token

IAM_API_VERSION = "2023-06-27"
IAM_API_URL = f"https://api.hashicorp.cloud/iam/{IAM_API_VERSION}"
hcp_logger = logging.getLogger("hcp_api")

async def list_users():
    """
    Lists all users in the organization.
    """
    token = await get_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{IAM_API_URL}/users", headers=headers)
        response.raise_for_status()
        users = response.json()
        hcp_logger.info(users)
        return users

async def get_user(user_id: str):
    """
    Gets a user by their ID.
    """
    token = await get_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{IAM_API_URL}/users/{user_id}", headers=headers)
        response.raise_for_status()
        user = response.json()
        hcp_logger.info(user)
        return user

async def delete_user(user_id: str):
    """
    Deletes a user by their ID.
    """
    token = await get_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{IAM_API_URL}/users/{user_id}", headers=headers)
        response.raise_for_status()
        result = response.json()
        hcp_logger.info(result)
        return result

async def create_user(name: str, email: str):
    """
    Creates a new user.
    """
    token = await get_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{IAM_API_URL}/users",
            headers=headers,
            json={"name": name, "email": email},
        )
        response.raise_for_status()
        user = response.json()
        hcp_logger.info(user)
        return user

async def update_user(user_id: str, name: str):
    """
    Updates a user's name.
    """
    token = await get_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        response = await client.put(
            f"{IAM_API_URL}/users/{user_id}",
            headers=headers,
            json={"name": name},
        )
        response.raise_for_status()
        user = response.json()
        hcp_logger.info(user)
        return user
