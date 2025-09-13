import json
import uvicorn
import httpx
import importlib.util
import asyncio
import logging.config
from fastapi import FastAPI, Request, Response
from mcp import prompts, resources, tools
from hcp.resource_manager import list_projects, get_project, delete_project, create_project, get_organization, list_organizations, update_project, update_organization
from hcp.iam import list_users, get_user, delete_user, create_user, update_user
from hcp.vault import list_secrets, get_secret, delete_secret, create_secret, update_secret
from utils.finders import find_project_by_name, find_user_by_email, find_organization_by_name

app = FastAPI()

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "%(asctime)s [%(name)s] %(levelprefix)s %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "use_colors": True,
        },
        "access": {
            "()": "uvicorn.logging.AccessFormatter",
            "fmt": '%(asctime)s [%(name)s] %(levelprefix)s %(client_addr)s - "%(request_line)s" %(status_code)s',
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "use_colors": True,
        },
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
        "access": {
            "formatter": "access",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
        "file_handler": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "default",
            "filename": "mcp_server.log",
            "maxBytes": 10485760,  # 10 MB
            "backupCount": 5,
            "encoding": "utf8",
        },
    },
    "loggers": {
        "uvicorn": {"handlers": ["default", "file_handler"], "level": "INFO", "propagate": False},
        "uvicorn.error": {"level": "INFO", "handlers": ["default", "file_handler"], "propagate": False},
        "uvicorn.access": {"handlers": ["access", "file_handler"], "level": "INFO", "propagate": False},
    },
    "root": {
        "level": "INFO",
        "handlers": ["default", "file_handler"],
    },
}

def get_tools():
    """
    Returns a list of all available tools.
    """
    return [
        tools.list_projects_tool().model_dump(exclude=["function"]),
        tools.get_project_tool().model_dump(exclude=["function"]),
        tools.delete_project_tool().model_dump(exclude=["function"]),
        tools.create_project_tool().model_dump(exclude=["function"]),
        tools.update_project_tool().model_dump(exclude=["function"]),
        tools.get_organization_tool().model_dump(exclude=["function"]),
        tools.list_organizations_tool().model_dump(exclude=["function"]),
        tools.update_organization_tool().model_dump(exclude=["function"]),
        tools.list_users_tool().model_dump(exclude=["function"]),
        tools.get_user_tool().model_dump(exclude=["function"]),
        tools.delete_user_tool().model_dump(exclude=["function"]),
        tools.create_user_tool().model_dump(exclude=["function"]),
        tools.update_user_tool().model_dump(exclude=["function"]),
        tools.list_secrets_tool().model_dump(exclude=["function"]),
        tools.get_secret_tool().model_dump(exclude=["function"]),
        tools.delete_secret_tool().model_dump(exclude=["function"]),
        tools.create_secret_tool().model_dump(exclude=["function"]),
        tools.update_secret_tool().model_dump(exclude=["function"]),
        tools.get_project_by_name_tool().model_dump(exclude=["function"]),
        tools.get_user_by_email_tool().model_dump(exclude=["function"]),
        tools.get_organization_by_name_tool().model_dump(exclude=["function"]),
    ]

def get_prompts():
    """
    Returns a dictionary of all available prompts.
    """
    return {
        "list_projects": prompts.LIST_PROJECTS_PROMPT,
        "list_users": prompts.LIST_USERS_PROMPT,
        "list_secrets": prompts.LIST_SECRETS_PROMPT,
        "delete_project": prompts.DELETE_PROJECT_PROMPT,
        "delete_user": prompts.DELETE_USER_PROMPT,
        "delete_secret": prompts.DELETE_SECRET_PROMPT,
        "create_project": prompts.CREATE_PROJECT_PROMPT,
        "create_user": prompts.CREATE_USER_PROMPT,
        "create_secret": prompts.CREATE_SECRET_PROMPT,
        "update_user": prompts.UPDATE_USER_PROMPT,
        "update_project": prompts.UPDATE_PROJECT_PROMPT,
        "update_secret": prompts.UPDATE_SECRET_PROMPT,
        "update_organization": prompts.UPDATE_ORGANIZATION_PROMPT,
        "list_organizations": prompts.LIST_ORGANIZATIONS_PROMPT,
        "get_organization": prompts.GET_ORGANIZATION_PROMPT,
        "get_project": prompts.GET_PROJECT_PROMPT,
        "get_user": prompts.GET_USER_PROMPT,
        "get_secret": prompts.GET_SECRET_PROMPT,
        "find_project_and_list_secrets": prompts.FIND_PROJECT_AND_LIST_SECRETS_PROMPT,
        "find_project_and_delete_project": prompts.FIND_PROJECT_AND_DELETE_PROJECT_PROMPT,
        "find_user_and_delete_user": prompts.FIND_USER_AND_DELETE_USER_PROMPT,
        "find_secret_and_delete_secret": prompts.FIND_SECRET_AND_DELETE_SECRET_PROMPT,
        "find_organization_and_list_projects": prompts.FIND_ORGANIZATION_AND_LIST_PROJECTS_PROMPT,
        "find_organization_and_create_project": prompts.FIND_ORGANIZATION_AND_CREATE_PROJECT_PROMPT,
        "find_project_and_create_secret": prompts.FIND_PROJECT_AND_CREATE_SECRET_PROMPT,
        "find_user_and_create_project": prompts.FIND_USER_AND_CREATE_PROJECT_PROMPT,
        "find_user_and_create_secret": prompts.FIND_USER_AND_CREATE_SECRET_PROMPT,
        "find_organization_and_create_user": prompts.FIND_ORGANIZATION_AND_CREATE_USER_PROMPT,
        "find_project_and_create_user": prompts.FIND_PROJECT_AND_CREATE_USER_PROMPT,
        "find_organization_and_delete_project": prompts.FIND_ORGANIZATION_AND_DELETE_PROJECT_PROMPT,
        "find_organization_and_delete_user": prompts.FIND_ORGANIZATION_AND_DELETE_USER_PROMPT,
        "find_project_and_delete_user": prompts.FIND_PROJECT_AND_DELETE_USER_PROMPT,
        "find_organization_and_delete_secret": prompts.FIND_ORGANIZATION_AND_DELETE_SECRET_PROMPT,
        "find_project_and_delete_secret": prompts.FIND_PROJECT_AND_DELETE_SECRET_PROMPT,
        "find_user_and_delete_project": prompts.FIND_USER_AND_DELETE_PROJECT_PROMPT,
        "find_user_and_delete_secret": prompts.FIND_USER_AND_DELETE_SECRET_PROMPT,
        "find_organization_and_get_project": prompts.FIND_ORGANIZATION_AND_GET_PROJECT_PROMPT,
        "find_organization_and_get_user": prompts.FIND_ORGANIZATION_AND_GET_USER_PROMPT,
        "find_organization_and_get_secret": prompts.FIND_ORGANIZATION_AND_GET_SECRET_PROMPT,
        "find_project_and_get_user": prompts.FIND_PROJECT_AND_GET_USER_PROMPT,
        "find_project_and_get_secret": prompts.FIND_PROJECT_AND_GET_SECRET_PROMPT,
        "find_user_and_get_project": prompts.FIND_USER_AND_GET_PROJECT_PROMPT,
        "find_user_and_get_secret": prompts.FIND_USER_AND_GET_SECRET_PROMPT,
        "find_organization_and_list_users": prompts.FIND_ORGANIZATION_AND_LIST_USERS_PROMPT,
        "find_project_and_list_users": prompts.FIND_PROJECT_AND_LIST_USERS_PROMPT,
        "find_user_and_list_projects": prompts.FIND_USER_AND_LIST_PROJECTS_PROMPT,
        "find_user_and_list_secrets": prompts.FIND_USER_AND_LIST_SECRETS_PROMPT,
        "find_organization_and_list_secrets": prompts.FIND_ORGANIZATION_AND_LIST_SECRETS_PROMPT,
        "find_user_and_list_organizations": prompts.FIND_USER_AND_LIST_ORGANIZATIONS_PROMPT,
        "find_organization_and_get_organization": prompts.FIND_ORGANIZATION_AND_GET_ORGANIZATION_PROMPT,
        "find_project_and_get_project": prompts.FIND_PROJECT_AND_GET_PROJECT_PROMPT,
        "find_user_and_get_user": prompts.FIND_USER_AND_GET_USER_PROMPT,
        "find_secret_and_get_secret": prompts.FIND_SECRET_AND_GET_SECRET_PROMPT,
        "find_organization_and_update_organization": prompts.FIND_ORGANIZATION_AND_UPDATE_ORGANIZATION_PROMPT,
        "find_project_and_update_project": prompts.FIND_PROJECT_AND_UPDATE_PROJECT_PROMPT,
        "find_user_and_update_user": prompts.FIND_USER_AND_UPDATE_USER_PROMPT,
        "find_organization_and_update_project": prompts.FIND_ORGANIZATION_AND_UPDATE_PROJECT_PROMPT,
        "find_project_and_update_user": prompts.FIND_PROJECT_AND_UPDATE_USER_PROMPT,
        "find_organization_and_update_secret": prompts.FIND_ORGANIZATION_AND_UPDATE_SECRET_PROMPT,
        "find_project_and_update_secret": prompts.FIND_PROJECT_AND_UPDATE_SECRET_PROMPT,
        "find_user_and_update_project": prompts.FIND_USER_AND_UPDATE_PROJECT_PROMPT,
        "find_user_and_update_secret": prompts.FIND_USER_AND_UPDATE_SECRET_PROMPT,
    }

async def execute_tool_code(code: str, parameters: dict):
    """
    Executes a tool's code with the given parameters.
    """
    # Create a mock module to execute the code in
    spec = importlib.util.spec_from_loader("tool_module", loader=None)
    tool_module = importlib.util.module_from_spec(spec)

    # Execute the provided Python code in the mock module's namespace
    exec(code, tool_module.__dict__)

    # The function to execute should be the last function defined in the code
    func_name = [name for name, obj in tool_module.__dict__.items() if callable(obj)][-1]
    func = getattr(tool_module, func_name)

    # Execute the function with the provided parameters
    result = await func(**parameters)
    return result

TOOL_MAP = {
    "list_projects": list_projects,
    "get_project": get_project,
    "delete_project": delete_project,
    "create_project": create_project,
    "update_project": update_project,
    "get_organization": get_organization,
    "list_organizations": list_organizations,
    "update_organization": update_organization,
    "list_users": list_users,
    "get_user": get_user,
    "delete_user": delete_user,
    "create_user": create_user,
    "update_user": update_user,
    "list_secrets": list_secrets,
    "get_secret": get_secret,
    "delete_secret": delete_secret,
    "create_secret": create_secret,
    "update_secret": update_secret,
    "get_project_by_name": find_project_by_name,
    "get_user_by_email": find_user_by_email,
    "get_organization_by_name": find_organization_by_name,
    "execute_tool_code": execute_tool_code,
}

@app.get("/")
async def health_check():
    """
    Health check endpoint.
    """
    return {"status": "ok"}

@app.post("/mcp")
async def mcp_server(request: Request):
    """
    Main endpoint for the MCP server.
    """
    body = await request.json()

    # Basic JSON-RPC validation
    if "jsonrpc" not in body or body["jsonrpc"] != "2.0" or "method" not in body or "id" not in body:
        return Response(content=json.dumps({
            "jsonrpc": "2.0",
            "error": {"code": -32600, "message": "Invalid Request"},
            "id": body.get("id")
        }), status_code=400, media_type="application/json")

    request_id = body["id"]
    method = body["method"]
    params = body.get("params", {})

    if method != "tools/call":
        return Response(content=json.dumps({
            "jsonrpc": "2.0",
            "error": {"code": -32601, "message": "Method not found"},
            "id": request_id
        }), status_code=404, media_type="application/json")

    tool_name = None
    parameters = {}

    if "code" in params:
        tool_name = "execute_tool_code"
        parameters = {"code": params.get("code"), "parameters": params.get("parameters", {})}
    elif "name" in params:
        tool_name = params.get("name")
        parameters = params.get("parameters", {})
    else:
        return Response(content=json.dumps({
            "jsonrpc": "2.0",
            "error": {"code": -32602, "message": "Invalid params: missing 'name' or 'code'"},
            "id": request_id
        }), status_code=400, media_type="application/json")


    if tool_name in TOOL_MAP:
        try:
            result = await TOOL_MAP[tool_name](**parameters)
            response_data = {
                "jsonrpc": "2.0",
                "result": result,
                "id": request_id
            }
            return Response(content=json.dumps(response_data), media_type="application/json")
        except httpx.HTTPStatusError as e:
            error_data = {
                "jsonrpc": "2.0",
                "error": {"code": -32000, "message": "Server error", "data": f"HCP API Error: {e.response.text}"},
                "id": request_id
            }
            return Response(content=json.dumps(error_data), status_code=500, media_type="application/json")
        except Exception as e:
            error_data = {
                "jsonrpc": "2.0",
                "error": {"code": -32000, "message": "Server error", "data": str(e)},
                "id": request_id
            }
            return Response(content=json.dumps(error_data), status_code=500, media_type="application/json")
    else:
        error_data = {
            "jsonrpc": "2.0",
            "error": {"code": -32601, "message": f"Method not found: Tool '{tool_name}' not found."},
            "id": request_id
        }
        return Response(content=json.dumps(error_data), status_code=404, media_type="application/json")

@app.get("/tools/list")
async def list_tools():
    """
    Returns the list of available tools.
    """
    return get_tools()

@app.get("/prompts/list")
async def list_prompts():
    """
    Returns the list of available prompts.
    """
    return get_prompts()

@app.get("/.well-known/mcp.json")
async def get_mcp_spec():
    """
    Returns the MCP specification for this server.
    """
    spec = {
        "name": "HCP MCP Server",
        "version": "0.1.0",
        "documentation": "https://github.com/hashicorp/hcp-mcp-server-py",
        "capabilities": {
            "tool_code": True,
            "tools": True,
            "prompts": True,
        },
        "resources": [
            resources.Project().model_dump(),
            resources.User().model_dump(),
            resources.Secret().model_dump(),
            resources.Organization().model_dump(),
        ],
        "tools": get_tools(),
        "prompts": get_prompts(),
    }
    return Response(content=json.dumps(spec, indent=2), media_type="application/json")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_config=LOGGING_CONFIG)
