# config.py
"""
Configuration for HCP API versions, base URLs, and MCP server settings.
"""
import os

# HCP Authentication
HCP_AUTH_URL = "https://auth.idp.hashicorp.com/oauth/token"
HCP_CLIENT_ID = os.getenv("HCP_CLIENT_ID")
HCP_CLIENT_SECRET = os.getenv("HCP_CLIENT_SECRET")
HCP_TOKEN_AUDIENCE = "https://api.hashicorp.cloud" # Audience for HCP API tokens

# HCP API Base URL
HCP_API_BASE_URL = "https://api.cloud.hashicorp.com"

# API Versions (derived from the provided Swagger files and HCP documentation)
# These versions are part of the URL path for API calls.
IAM_API_VERSION = "2019-12-10"
RESOURCE_MANAGER_API_VERSION = "2019-12-10"
VAULT_SECRETS_API_VERSION = "2023-11-28"

# MCP Server Configuration
MCP_SERVER_HOST = os.getenv("MCP_SERVER_HOST", "127.0.0.1")
MCP_SERVER_PORT = int(os.getenv("MCP_SERVER_PORT", "8000"))

# Initial check for critical environment variables
if not HCP_CLIENT_ID:
    print("Warning: HCP_CLIENT_ID environment variable is not set.")
if not HCP_CLIENT_SECRET:
    print("Warning: HCP_CLIENT_SECRET environment variable is not set.")
if not HCP_CLIENT_ID or not HCP_CLIENT_SECRET:
    print("Warning: Without HCP_CLIENT_ID and HCP_CLIENT_SECRET, the MCP server cannot authenticate with HCP and API calls will fail.")


