# hcp_mcp_server/main.py
# Main FastAPI application for the HCP Model Context Protocol Server.

import logging
import httpx
from fastapi import FastAPI, HTTPException, Depends, Request
from contextlib import asynccontextmanager
from typing import Optional

from . import hcp_auth
from .hcp_api_clients import iam_client, resource_manager_client, vault_secrets_client
# from .models import MCPResponse # If using standardized MCP response models

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Global HTTP Client ---
# Using a global client is often more efficient for multiple requests.
# It should be managed with lifespan events in FastAPI.
shared_http_client: Optional[httpx.AsyncClient] = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize the HTTP client
    global shared_http_client
    shared_http_client = httpx.AsyncClient(timeout=30.0) # Set a reasonable timeout
    logger.info("HTTPX AsyncClient started.")
    yield
    # Shutdown: Close the HTTP client
    if shared_http_client:
        await shared_http_client.aclose()
        logger.info("HTTPX AsyncClient closed.")

app = FastAPI(
    title="HCP Model Context Protocol Server",
    description="Provides context from HashiCorp Cloud Platform APIs via MCP.",
    version="0.1.0",
    lifespan=lifespan # Manage lifespan of shared_http_client
)

# --- Dependency for HCP Access Token ---
async def get_valid_hcp_token() -> str:
    """Dependency to get a valid HCP access token."""
    token = await hcp_auth.get_hcp_access_token()
    if not token:
        logger.error("Failed to obtain HCP access token for request.")
        raise HTTPException(status_code=503, detail="Could not authenticate with HCP. Token unavailable.")
    return token

# --- Helper for API calls ---
async def execute_api_call(api_function, *args, **kwargs):
    """Helper to execute an API client function and handle common exceptions."""
    if not shared_http_client: # Should not happen with lifespan management
        raise HTTPException(status_code=500, detail="HTTP client not initialized.")
    try:
        # Pass the shared_http_client as the first argument
        return await api_function(shared_http_client, *args, **kwargs)
    except httpx.HTTPStatusError as e:
        logger.error(f"HCP API call failed with status {e.response.status_code}: {e.response.text}")
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"HCP API Error: {e.response.text}"
        )
    except httpx.RequestError as e:
        logger.error(f"HCP API request failed: {e}")
        raise HTTPException(status_code=504, detail=f"HCP API Request Error: {e}") # 504 Gateway Timeout
    except Exception as e:
        logger.exception("An unexpected error occurred during API call execution.") # Log full stack trace
        raise HTTPException(status_code=500, detail=f"An internal server error occurred: {str(e)}")


# --- MCP Endpoint Definitions ---
# The Model Context Protocol typically uses GET requests where the URI path
# identifies the resource for which context is being requested.
# The response is a JSON object.

@app.get("/")
async def read_root():
    return {"message": "HCP Model Context Protocol Server is running. "
                     "Access context via specific GET endpoints like /mcp/hcp/organizations"}

# --- Resource Manager MCP Endpoints ---
@app.get("/mcp/hcp/organizations")
async def mcp_list_organizations(token: str = Depends(get_valid_hcp_token)):
    """MCP: Get a list of HCP organizations."""
    logger.info("MCP request: /mcp/hcp/organizations")
    return await execute_api_call(resource_manager_client.list_organizations, token)

@app.get("/mcp/hcp/organizations/{organization_id}")
async def mcp_get_organization_details(organization_id: str, token: str = Depends(get_valid_hcp_token)):
    """MCP: Get details for a specific HCP organization."""
    logger.info(f"MCP request: /mcp/hcp/organizations/{organization_id}")
    return await execute_api_call(resource_manager_client.get_organization, token, organization_id)

@app.get("/mcp/hcp/organizations/{organization_id}/projects")
async def mcp_list_projects(organization_id: str, token: str = Depends(get_valid_hcp_token)):
    """MCP: Get a list of projects within an HCP organization."""
    logger.info(f"MCP request: /mcp/hcp/organizations/{organization_id}/projects")
    return await execute_api_call(resource_manager_client.list_projects, token, organization_id)

@app.get("/mcp/hcp/organizations/{organization_id}/projects/{project_id}")
async def mcp_get_project_details(organization_id: str, project_id: str, token: str = Depends(get_valid_hcp_token)):
    """MCP: Get details for a specific HCP project."""
    logger.info(f"MCP request: /mcp/hcp/organizations/{organization_id}/projects/{project_id}")
    return await execute_api_call(resource_manager_client.get_project, token, organization_id, project_id)


# --- IAM MCP Endpoints ---
@app.get("/mcp/hcp/organizations/{organization_id}/iam/users")
async def mcp_list_iam_users(organization_id: str, token: str = Depends(get_valid_hcp_token)):
    """MCP: Get a list of IAM users in an HCP organization."""
    logger.info(f"MCP request: /mcp/hcp/organizations/{organization_id}/iam/users")
    return await execute_api_call(iam_client.list_organization_users, token, organization_id)

# Actually calls resource manager. Not sure why it made a function within IAM area
@app.get("/mcp/hcp/organizations/{organization_id}/iam/roles")
async def mcp_list_iam_roles(organization_id: str, token: str = Depends(get_valid_hcp_token)):
    """MCP: Get a list of IAM roles in an HCP organization."""
    logger.info(f"MCP request: /mcp/hcp/organizations/{organization_id}/iam/roles")
    return await execute_api_call(iam_client.list_organization_roles, token, organization_id)

# Actually calls resource manager. Not sure why it made a function within IAM area
# Not working yet. 
@app.get("/mcp/hcp/organizations/{organization_id}/iam/roles/{role_id}")
async def mcp_get_iam_role_details(organization_id: str, role_id: str, token: str = Depends(get_valid_hcp_token)):
    """MCP: Get details for a specific IAM role in an HCP organization."""
    logger.info(f"MCP request: /mcp/hcp/organizations/{organization_id}/iam/roles/{role_id}")
    return await execute_api_call(iam_client.get_organization_role, token, organization_id, role_id)

@app.get("/mcp/hcp/organizations/{organization_id}/iam/service-principals")
async def mcp_list_service_principals(organization_id: str, token: str = Depends(get_valid_hcp_token)):
    """MCP: Get a list of service principals in an HCP organization."""
    logger.info(f"MCP request: /mcp/hcp/organizations/{organization_id}/iam/service-principals")
    return await execute_api_call(iam_client.list_service_principals, token, organization_id)

# --- HCP Vault Secrets MCP Endpoints ---
@app.get("/mcp/hcp/organizations/{organization_id}/projects/{project_id}/vault/apps")
async def mcp_list_vault_apps(organization_id: str, project_id: str, token: str = Depends(get_valid_hcp_token)):
    """MCP: List secret applications in an HCP Vault project."""
    logger.info(f"MCP request: /mcp/hcp/organizations/{organization_id}/projects/{project_id}/vault/apps")
    return await execute_api_call(vault_secrets_client.list_apps, token, organization_id, project_id)

@app.get("/mcp/hcp/organizations/{organization_id}/projects/{project_id}/vault/apps/{app_name}")
async def mcp_get_vault_app_details(organization_id: str, project_id: str, app_name: str, token: str = Depends(get_valid_hcp_token)):
    """MCP: Get details for a specific secret application in HCP Vault."""
    logger.info(f"MCP request: /mcp/hcp/organizations/{organization_id}/projects/{project_id}/vault/apps/{app_name}")
    return await execute_api_call(vault_secrets_client.get_app, token, organization_id, project_id, app_name)

@app.get("/mcp/hcp/organizations/{organization_id}/projects/{project_id}/vault/apps/{app_name}/secrets")
async def mcp_list_vault_secrets_metadata(
    organization_id: str, project_id: str, app_name: str, token: str = Depends(get_valid_hcp_token)
):
    """MCP: List secrets (metadata) in an HCP Vault application."""
    logger.info(f"MCP request: /mcp/hcp/organizations/{organization_id}/projects/{project_id}/vault/apps/{app_name}/secrets")
    return await execute_api_call(vault_secrets_client.list_secrets, token, organization_id, project_id, app_name)

@app.get("/mcp/hcp/organizations/{organization_id}/projects/{project_id}/vault/apps/{app_name}/secrets/{secret_name}")
async def mcp_get_vault_secret_value(
    organization_id: str, project_id: str, app_name: str, secret_name: str, token: str = Depends(get_valid_hcp_token)
):
    """MCP: Get the value of a specific secret from HCP Vault."""
    logger.info(f"MCP request: /mcp/hcp/organizations/{organization_id}/projects/{project_id}/vault/apps/{app_name}/secrets/{secret_name}")
    return await execute_api_call(
        vault_secrets_client.get_secret_value, token, organization_id, project_id, app_name, secret_name
    )

# To run this application:
# 1. Save the files in the structure:
#    hcp_mcp_server/
#    ├── main.py
#    ├── hcp_auth.py
#    ├── hcp_api_clients/
#    │   ├── __init__.py
#    │   ├── base_client.py
#    │   ├── iam_client.py
#    │   ├── resource_manager_client.py
#    │   └── vault_secrets_client.py
#    ├── models/
#    │   └── __init__.py
#    ├── .env (copied from .env_example and filled)
#    └── requirements.txt
#
# 2. Install requirements: pip install -r requirements.txt
# 3. Set HCP_CLIENT_ID and HCP_CLIENT_SECRET in a .env file in the hcp_mcp_server directory.
# 4. Run with Uvicorn from the directory containing `hcp_mcp_server`:
#    uvicorn hcp_mcp_server.main:app --reload --port 8000
#
# Example MCP URIs to test (replace placeholders):
# http://localhost:8000/mcp/hcp/organizations
# http://localhost:8000/mcp/hcp/organizations/{your_org_id}
# http://localhost:8000/mcp/hcp/organizations/{your_org_id}/projects
# http://localhost:8000/mcp/hcp/organizations/{your_org_id}/projects/{your_project_id}
# http://localhost:8000/mcp/hcp/organizations/{your_org_id}/iam/users
# http://localhost:8000/mcp/hcp/organizations/{your_org_id}/projects/{your_project_id}/vault/apps
# http://localhost:8000/mcp/hcp/organizations/{your_org_id}/projects/{your_project_id}/vault/apps/{your_app_name}/secrets/{your_secret_name}

if __name__ == "__main__":
    # This part is for running with `python -m hcp_mcp_server.main`
    # However, uvicorn is the recommended way to run FastAPI apps.
    import uvicorn
    # Ensure .env is in the same directory as this script if running this way,
    # or that the hcp_mcp_server package is in PYTHONPATH.
    # Best to run with: uvicorn hcp_mcp_server.main:app --reload
    logger.warning("Running directly with __main__. Recommended: uvicorn hcp_mcp_server.main:app --reload")
    uvicorn.run(app, host="0.0.0.0", port=8000)
