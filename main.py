import json
import asyncio
import sys
from mcp import tools, prompts, resources
from hcp.resource_manager import (
    list_projects,
    get_project,
    delete_project,
    create_project,
    update_project,
    get_organization,
    list_organizations,
    update_organization,
)
from hcp.iam import (
    list_users,
    get_user,
    delete_user,
    create_user,
    update_user,
)
from hcp.vault import (
    list_secrets,
    get_secret,
    delete_secret,
    create_secret,
    update_secret,
)
from utils.finders import (
    find_project_by_name,
    find_user_by_email,
    find_organization_by_name,
)
from mcp_logging import setup_logging

# Set up logging
logger = setup_logging()

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
        tools.find_project_by_name_tool().model_dump(exclude=["function"]),
        tools.find_user_by_email_tool().model_dump(exclude=["function"]),
        tools.find_organization_by_name_tool().model_dump(exclude=["function"]),
    ]

def get_prompts():
    """
    Returns a dictionary of all available prompts.
    """
    return {
        "list_projects": prompts.LIST_PROJECTS_PROMPT,
        "get_project": prompts.GET_PROJECT_PROMPT,
        "delete_project": prompts.DELETE_PROJECT_PROMPT,
        "create_project": prompts.CREATE_PROJECT_PROMPT,
        "update_project": prompts.UPDATE_PROJECT_PROMPT,
        "get_organization": prompts.GET_ORGANIZATION_PROMPT,
        "list_organizations": prompts.LIST_ORGANIZATIONS_PROMPT,
        "update_organization": prompts.UPDATE_ORGANIZATION_PROMPT,
        "list_users": prompts.LIST_USERS_PROMPT,
        "get_user": prompts.GET_USER_PROMPT,
        "delete_user": prompts.DELETE_USER_PROMPT,
        "create_user": prompts.CREATE_USER_PROMPT,
        "update_user": prompts.UPDATE_USER_PROMPT,
        "list_secrets": prompts.LIST_SECRETS_PROMPT,
        "get_secret": prompts.GET_SECRET_PROMPT,
        "delete_secret": prompts.DELETE_SECRET_PROMPT,
        "create_secret": prompts.CREATE_SECRET_PROMPT,
        "update_secret": prompts.UPDATE_SECRET_PROMPT,
        "find_project_and_list_secrets": prompts.FIND_PROJECT_AND_LIST_SECRETS_PROMPT,
        "find_project_and_delete_project": prompts.FIND_PROJECT_AND_DELETE_PROJECT_PROMPT,
        "find_user_and_delete_user": prompts.FIND_USER_AND_DELETE_USER_PROMPT,
    }

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
    "find_project_by_name": find_project_by_name,
    "find_user_by_email": find_user_by_email,
    "find_organization_by_name": find_organization_by_name,
}

RESOURCE_MAP = {
    "hcp/organization": get_organization,
    "hcp/project": get_project,
    "hcp/user": get_user,
}

async def process_mcp_request(body: dict):
    """
    Processes an MCP request and returns a response dictionary.
    """
    logger.info(f"Received request: {json.dumps(body)}")
    request_id = body.get("id")
    method = body.get("method")
    params = body.get("params")

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "result": {
                "protocolVersion": "2025-06-18",
                "serverInfo": {
                    "name": "HCP",
                    "version": "0.0.1",
                },
                "capabilities": {
                    "tool_provider": {},
                    "prompt_provider": {},
                    "resource_provider": {},
                },
            },
            "id": request_id,
        }
    elif method == "mcp/shutdown":
        # No response is required for shutdown
        return None
    elif method == "mcp/exit":
        sys.exit(0)
    elif method == "notifications/initialized":
        logger.info("Client initialized.")
        return None
    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "result": {"tools": get_tools()},
            "id": request_id,
        }
    elif method == "tools/invoke":
        tool_name = params.get("name")
        parameters = params.get("parameters", {})
        if tool_name in TOOL_MAP:
            try:
                result = await TOOL_MAP[tool_name](**parameters)
                return {
                    "jsonrpc": "2.0",
                    "result": result,
                    "id": request_id,
                }
            except TypeError as e:
                return {
                    "jsonrpc": "2.0",
                    "error": {"code": -32602, "message": "Invalid params", "data": str(e)},
                    "id": request_id,
                }
            except Exception as e:
                return {
                    "jsonrpc": "2.0",
                    "error": {"code": -32000, "message": "Server error", "data": str(e)},
                    "id": request_id,
                }
        else:
            return {
                "jsonrpc": "2.0",
                "error": {"code": -32601, "message": f"Method not found: Tool '{tool_name}' not found."},
                "id": request_id,
            }
    elif method == "prompts/discover":
        return {
            "jsonrpc": "2.0",
            "result": {"prompts": get_prompts()},
            "id": request_id,
        }
    elif method == "resources/discover":
        return {
            "jsonrpc": "2.0",
            "result": {"resources": resources.get_resources()},
            "id": request_id,
        }
    elif method == "resources/get":
        resource_name = params.get("name")
        parameters = params.get("parameters", {})
        if resource_name in RESOURCE_MAP:
            try:
                result = await RESOURCE_MAP[resource_name](**parameters)
                return {
                    "jsonrpc": "2.0",
                    "result": result,
                    "id": request_id,
                }
            except TypeError as e:
                return {
                    "jsonrpc": "2.0",
                    "error": {"code": -32602, "message": "Invalid params", "data": str(e)},
                    "id": request_id,
                }
            except Exception as e:
                return {
                    "jsonrpc": "2.0",
                    "error": {"code": -32000, "message": "Server error", "data": str(e)},
                    "id": request_id,
                }
        else:
            return {
                "jsonrpc": "2.0",
                "error": {"code": -32601, "message": f"Method not found: Resource '{resource_name}' not found."},
                "id": request_id,
            }
    else:
        return {
            "jsonrpc": "2.0",
            "error": {"code": -32601, "message": "Method not found"},
            "id": request_id,
        }

async def stdio_main():
    """
    Runs the server in stdio mode.
    """
    while True:
        line = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
        if not line:
            break
        try:
            request_json = json.loads(line)
            response_json = await process_mcp_request(request_json)
            if response_json:
                try:
                    print(json.dumps(response_json), flush=True)
                except TypeError:
                    response_json["result"] = str(response_json["result"])
                    print(json.dumps(response_json), flush=True)
        except json.JSONDecodeError:
            error_response = {
                "jsonrpc": "2.0",
                "error": {"code": -32700, "message": "Parse error"},
                "id": None,
            }
            print(json.dumps(error_response), flush=True)

if __name__ == "__main__":
    asyncio.run(stdio_main())
