import httpx
from hcp.auth import get_access_token

VAULT_API_VERSION = "2023-06-27"
VAULT_API_URL = f"https://api.hashicorp.cloud/vault/{VAULT_API_VERSION}"

async def list_secrets(project_id: str, app_name: str):
    """
    Lists all secrets for a given application.
    """
    token = await get_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{VAULT_API_URL}/projects/{project_id}/apps/{app_name}/secrets", headers=headers
        )
        response.raise_for_status()
        return response.json()

async def get_secret(project_id: str, app_name: str, secret_name: str):
    """
    Gets a secret by its name.
    """
    token = await get_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{VAULT_API_URL}/projects/{project_id}/apps/{app_name}/secrets/{secret_name}", headers=headers
        )
        response.raise_for_status()
        return response.json()

async def delete_secret(project_id: str, app_name: str, secret_name: str):
    """
    Deletes a secret by its name.
    """
    token = await get_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        response = await client.delete(
            f"{VAULT_API_URL}/projects/{project_id}/apps/{app_name}/secrets/{secret_name}", headers=headers
        )
        response.raise_for_status()
        return response.json()

async def create_secret(project_id: str, app_name: str, secret_name: str, secret_value: str):
    """
    Creates a new secret.
    """
    token = await get_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{VAULT_API_URL}/projects/{project_id}/apps/{app_name}/secrets",
            headers=headers,
            json={"name": secret_name, "value": secret_value},
        )
        response.raise_for_status()
        return response.json()

async def update_secret(project_id: str, app_name: str, secret_name: str, secret_value: str):
    """
    Updates a secret's value.
    """
    token = await get_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        response = await client.put(
            f"{VAULT_API_URL}/projects/{project_id}/apps/{app_name}/secrets/{secret_name}",
            headers=headers,
            json={"value": secret_value},
        )
        response.raise_for_status()
        return response.json()
