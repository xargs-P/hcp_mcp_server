import httpx
import logging
from hcp.auth import get_access_token

VAULT_API_VERSION = "2023-06-13"
VAULT_API_URL = f"https://api.hashicorp.cloud/secrets/{VAULT_API_VERSION}"
hcp_logger = logging.getLogger("hcp_api")

async def list_secrets(organization_id: str, project_id: str, app_name: str):
    """
    Lists all secrets for a given application.
    """
    token = await get_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{VAULT_API_URL}/organizations/{organization_id}/projects/{project_id}/apps/{app_name}/secrets", headers=headers
        )
        response.raise_for_status()
        secrets = response.json()
        hcp_logger.info(secrets)
        return secrets

async def get_secret(organization_id: str, project_id: str, app_name: str, secret_name: str):
    """
    Gets a secret by its name.
    """
    token = await get_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{VAULT_API_URL}/organizations/{organization_id}/projects/{project_id}/apps/{app_name}/secrets/{secret_name}", headers=headers
        )
        response.raise_for_status()
        secret = response.json()
        hcp_logger.info(secret)
        return secret

async def delete_secret(organization_id: str, project_id: str, app_name: str, secret_name: str):
    """
    Deletes a secret by its name.
    """
    token = await get_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        response = await client.delete(
            f"{VAULT_API_URL}/organizations/{organization_id}/projects/{project_id}/apps/{app_name}/secrets/{secret_name}", headers=headers
        )
        response.raise_for_status()
        result = response.json()
        hcp_logger.info(result)
        return result

async def create_secret(organization_id: str, project_id: str, app_name: str, secret_name: str, secret_value: str):
    """
    Creates a new secret.
    """
    token = await get_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{VAULT_API_URL}/organizations/{organization_id}/projects/{project_id}/apps/{app_name}/kv",
            headers=headers,
            json={"name": secret_name, "value": secret_value},
        )
        response.raise_for_status()
        secret = response.json()
        hcp_logger.info(secret)
        return secret