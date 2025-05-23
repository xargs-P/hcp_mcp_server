# mcp_server.py
"""
Main MCP Server application using FastAPI.
This server exposes MCP-compliant endpoints for an LLM to interact with
HashiCorp Cloud Platform (HCP) services.
"""
import uvicorn
from fastapi import FastAPI, HTTPException, Body
from fastapi.responses import JSONResponse
from pydantic import BaseModel # For request/response body validation
from typing import List, Dict, Any, Optional

# Import configurations, definitions, and service modules
# Order of imports can matter if modules register things upon import.
import config # Load config first to make variables available
import mcp_defs # Core MCP class definitions
import prompts # Load and register prompts
import iam_service # Loads and registers IAM tools and resources
import resource_manager_service # Loads and registers Resource Manager tools and resources
import vault_secrets_service # Loads and registers Vault Secrets tools and resources

# Initialize FastAPI application
app = FastAPI(
    title="HCP Model Context Protocol Server",
    version="0.1.1", # Incremented version
    description=(
        "A Model Context Protocol (MCP) server that enables Large Language Models (LLMs) "
        "to interact with HashiCorp Cloud Platform (HCP) APIs for services like IAM, "
        "Resource Manager, and Vault Secrets. The server handles authentication with HCP "
        "using environment variables HCP_CLIENT_ID and HCP_CLIENT_SECRET."
    ),
    # MCP information as per spec (optional but good practice)
    # Based on: https://github.com/modelcontextprotocol/modelcontextprotocol/blob/2025-03-26/docs/specification/2025-03-26/basic/lifecycle.md#server-information
    openapi_tags=[
        {"name": "MCP Endpoints", "description": "Standard Model Context Protocol endpoints."},
        {"name": "HCP Tools", "description": "Endpoints related to executing HCP-specific tools."}
    ]
)

# --- Pydantic Models for Request/Response Bodies ---
class ToolExecutionRequest(BaseModel):
    tool_name: str
    parameters: Dict[str, Any] = {}

class ToolExecutionResponse(BaseModel):
    success: bool
    result: Optional[Any] = None # Can be dict, list, string, etc. based on tool output
    error: Optional[str] = None
    error_details: Optional[Any] = None # Further details, could be a dict or string
    status_code: Optional[int] = None # HTTP status code from the underlying API call or internal processing

# --- Server Lifecycle Events ---
@app.on_event("startup")
async def startup_event():
    """
    Actions to perform when the server starts.
    Checks for HCP credentials and logs tool/prompt registration.
    """
    print("MCP Server starting up...")
    if not config.HCP_CLIENT_ID or not config.HCP_CLIENT_SECRET:
        print("CRITICAL WARNING: HCP_CLIENT_ID and/or HCP_CLIENT_SECRET are not set.")
        print("The server will run, but calls to HCP APIs will fail authentication.")
    else:
        print("HCP Client ID and Secret are configured.")
        # Optionally, you could try an initial token fetch here to validate credentials
        # from hcp_client import HCPClient
        # test_client = HCPClient()
        # if not test_client._ensure_token():
        #     print("Warning: Initial attempt to fetch HCP token failed. Check credentials or network.")
        # else:
        #     print("Successfully pre-fetched an HCP token (for testing).")


    print(f"Registered Tools: {len(mcp_defs.MCP_TOOLS)} -> {list(mcp_defs.MCP_TOOLS.keys())}")
    print(f"Registered Prompts: {len(mcp_defs.MCP_PROMPTS)} -> {list(mcp_defs.MCP_PROMPTS.keys())}")
    print(f"Registered Resource Types: {len(mcp_defs.MCP_RESOURCES)} -> {list(mcp_defs.MCP_RESOURCES.keys())}")
    print("MCP Server startup complete.")

# --- Standard MCP Endpoints ---
@app.get("/mcp/v1/tools",
         summary="List Available Tools",
         response_description="A list of tools the LLM can request to execute.",
         tags=["MCP Endpoints"])
async def list_tools_endpoint() -> Dict[str, List[Dict[str, Any]]]:
    """
    Provides a list of all tools registered with the MCP server.
    Each tool includes its name, description, and input schema.
    """
    if not mcp_defs.MCP_TOOLS:
        return {"tools": []}
    return {"tools": [tool.to_dict() for tool in mcp_defs.MCP_TOOLS.values()]}

@app.get("/mcp/v1/prompts",
         summary="List Available Prompts",
         response_description="A list of predefined prompts to guide LLM interactions.",
         tags=["MCP Endpoints"])
async def list_prompts_endpoint() -> Dict[str, List[Dict[str, Any]]]:
    """
    Provides a list of all prompts registered with the MCP server.
    Each prompt includes its name, description, system message, and user message template.
    """
    if not mcp_defs.MCP_PROMPTS:
        return {"prompts": []}
    return {"prompts": [prompt.to_dict() for prompt in mcp_defs.MCP_PROMPTS.values()]}

@app.get("/mcp/v1/resources",
         summary="List Resource Definitions",
         response_description="A list of resource types and their descriptions/schemas understood by this server.",
         tags=["MCP Endpoints"])
async def list_resource_definitions_endpoint() -> Dict[str, Dict[str, Any]]:
    """
    Provides definitions for resource types this server can interact with.
    This can include descriptions and, optionally, JSON schemas for each resource type.
    """
    return {"resource_types": mcp_defs.MCP_RESOURCES}

# --- Tool Execution Endpoint ---
@app.post("/mcp/v1/execute_tool",
          summary="Execute a Specified Tool",
          response_model=ToolExecutionResponse, # FastAPI will validate the response against this model
          response_description="The outcome of the requested tool execution.",
          tags=["HCP Tools"])
async def execute_tool_endpoint(request: ToolExecutionRequest = Body(...)) -> ToolExecutionResponse:
    """
    Receives a tool execution request from an LLM, executes the specified tool
    with the provided parameters, and returns the result.
    """
    tool = mcp_defs.MCP_TOOLS.get(request.tool_name)
    if not tool:
        # Return a structured error response
        return ToolExecutionResponse(
            success=False,
            error=f"Tool '{request.tool_name}' not found.",
            status_code=404
        )

    print(f"Executing tool: {request.tool_name} with parameters: {request.parameters}")
    try:
        # Tool functions are expected to return a dictionary with:
        # 'success': bool
        # 'data': result_data (if success)
        # 'error': error_message (if failure)
        # 'status_code': http_status_code_from_api_or_internal
        # 'details': additional_error_info (optional)
        
        # Validate parameters against tool's input_schema (basic check here, can be more robust)
        # For now, we rely on the function signature and type hints.
        # A more robust implementation would use jsonschema library to validate request.parameters against tool.input_schema

        tool_result = tool.func(**request.parameters)
        
        # Ensure the tool_result is a dictionary as expected
        if not isinstance(tool_result, dict):
            print(f"Tool '{request.tool_name}' returned an unexpected type: {type(tool_result)}. Expected dict.")
            return ToolExecutionResponse(
                success=False,
                error=f"Tool '{request.tool_name}' internal error: returned unexpected response type.",
                status_code=500
            )

        return ToolExecutionResponse(
            success=tool_result.get("success", False), # Default to False if 'success' key is missing
            result=tool_result.get("data"), # 'data' key for successful results
            error=tool_result.get("error"),   # 'error' key for failed results
            error_details=tool_result.get("details"),
            status_code=tool_result.get("status_code")
        )
    except TypeError as e:
        # This typically happens if parameters are missing or of the wrong type for the tool function
        print(f"TypeError during tool execution for '{request.tool_name}': {e}")
        return ToolExecutionResponse(
            success=False,
            error=f"Invalid parameters for tool '{request.tool_name}'.",
            error_details=str(e),
            status_code=400 # Bad Request
        )
    except Exception as e:
        # Catch-all for other unexpected errors during tool execution
        print(f"Unhandled exception during tool execution for '{request.tool_name}': {e}")
        # In a production environment, log the full traceback here.
        return ToolExecutionResponse(
            success=False,
            error="An unexpected internal error occurred during tool execution.",
            error_details=str(e), # Provide some detail, but be cautious about exposing sensitive info
            status_code=500 # Internal Server Error
        )

# --- Health Check Endpoint ---
@app.get("/health",
         summary="Health Check",
         response_description="Indicates the operational status of the server.",
         tags=["MCP Endpoints"])
async def health_check():
    """
    A simple health check endpoint. Can be expanded to check connectivity
    to downstream services like HCP if needed.
    """
    # Basic check:
    health_status = {"status": "ok", "hcp_credentials_configured": False}
    if config.HCP_CLIENT_ID and config.HCP_CLIENT_SECRET:
        health_status["hcp_credentials_configured"] = True
        # Could add a quick token fetch test here for a deeper health check, but be mindful of rate limits.
    return JSONResponse(content=health_status)

# --- Main Entry Point for Running the Server ---
if __name__ == "__main__":
    # This block allows running the server directly using `python mcp_server.py`
    
    # Final check before starting, reiterating the warning if creds are missing.
    if not config.HCP_CLIENT_ID or not config.HCP_CLIENT_SECRET:
        print("\n" + "="*50)
        print("CRITICAL STARTUP WARNING:")
        print("HCP_CLIENT_ID and/or HCP_CLIENT_SECRET environment variables are NOT set.")
        print("The MCP server will start, but it WILL NOT be able to make authenticated calls to HCP.")
        print("Please set these environment variables and restart the server for full functionality.")
        print("="*50 + "\n")
    
    print(f"Attempting to start MCP server on {config.MCP_SERVER_HOST}:{config.MCP_SERVER_PORT}")
    uvicorn.run(app, host=config.MCP_SERVER_HOST, port=config.MCP_SERVER_PORT)


