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
        tools.list_projects_tool().model_dump(),
        tools.get_project_tool().model_dump(),
        tools.delete_project_tool().model_dump(),
        tools.create_project_tool().model_dump(),
        tools.update_project_tool().model_dump(),
        tools.get_organization_tool().model_dump(),
        tools.list_organizations_tool().model_dump(),
        tools.update_organization_tool().model_dump(),
        tools.list_users_tool().model_dump(),
        tools.get_user_tool().model_dump(),
        tools.delete_user_tool().model_dump(),
        tools.create_user_tool().model_dump(),
        tools.update_user_tool().model_dump(),
        tools.list_secrets_tool().model_dump(),
        tools.get_secret_tool().model_dump(),
        tools.delete_secret_tool().model_dump(),
        tools.create_secret_tool().model_dump(),
        tools.update_secret_tool().model_dump(),
        tools.find_project_by_name_tool().model_dump(),
        tools.find_user_by_email_tool().model_dump(),
        tools.find_organization_by_name_tool().model_dump(),
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
    "hcp://cloud.hashicorp.com/organizations/{organization_id}": get_organization,
    "hcp://cloud.hashicorp.com/organizations/{organization_id}/projects/{project_id}": get_project,
    "hcp://cloud.hashicorp.com/users/{user_id}": get_user,
}

async def process_mcp_request(body: dict):
    """
    Processes an MCP request and returns a response dictionary.
    """
    request_id = body.get("id")
    method = body.get("method")
    params = body.get("params")

    # Log client calls
    if method in ["tools/call", "prompts/get", "resources/read"]:
        logger.info(f"Client call: {json.dumps(body)}")
    else:
        logger.info(f"Received request: {json.dumps(body)}")

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "result": {
                "protocolVersion": "2024-11-05",
                "serverInfo": {
                    "name": "HCP",
                    "version": "0.0.1",
                },
                "capabilities": {
                    "tools": {"listChanged": True},
                    "prompts": {"listChanged": True},
                    "resources": {"listChanged": True},
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
    elif method == "tools/call":
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        if tool_name in TOOL_MAP:
            try:
                result = await TOOL_MAP[tool_name](**arguments)
                logger.info(f"Tool request data: {result}")
                return {
                    "jsonrpc": "2.0",
                    "result": {
                        "content": [{"type": "text", "text": json.dumps(result)}],
                        "isError": False,
                    },
                    "id": request_id,
                }
            except ValueError as e:
                return {
                    "jsonrpc": "2.0",
                    "error": {"code": -32000, "message": "Server error", "data": str(e)},
                    "id": request_id,
                }
            except TypeError as e:
                return {
                    "jsonrpc": "2.0",
                    "error": {"code": -32602, "message": "Invalid params", "data": str(e)},
                    "id": request_id,
                }
            except Exception as e:
                logger.error(f"An unexpected error occurred: {e}", exc_info=True)
                return {
                    "jsonrpc": "2.0",
                    "error": {"code": -32000, "message": "Server error", "data": "An unexpected error occurred. See logs for details."},
                    "id": request_id,
                }
        else:
            return {
                "jsonrpc": "2.0",
                "error": {"code": -32601, "message": f"Method not found: Tool '{tool_name}' not found."},
                "id": request_id,
            }
    elif method == "prompts/get":
        prompt_name = params.get("name")
        if prompt_name in get_prompts():
            return {
                "jsonrpc": "2.0",
                "result": get_prompts()[prompt_name].model_dump(),
                "id": request_id,
            }
        else:
            return {
                "jsonrpc": "2.0",
                "error": {"code": -32601, "message": f"Method not found: Prompt '{prompt_name}' not found."},
                "id": request_id,
            }
    elif method == "prompts/list":
        return {
            "jsonrpc": "2.0",
            "result": {"prompts": [p.model_dump() for p in get_prompts().values()]},
            "id": request_id,
        }
    elif method == "resources/list":
        return {
            "jsonrpc": "2.0",
            "result": {"resources": [r.model_dump() for r in resources.get_resources()]},
            "id": request_id,
        }
    elif method == "resources/read":
        resource_uri = params.get("uri")
        parameters = params.get("parameters", {})
        if resource_uri in RESOURCE_MAP:
            try:
                result = await RESOURCE_MAP[resource_uri](**parameters)
                return {
                    "jsonrpc": "2.0",
                    "result": result,
                    "id": request_id,
                }
            except ValueError as e:
                return {
                    "jsonrpc": "2.0",
                    "error": {"code": -32000, "message": "Server error", "data": str(e)},
                    "id": request_id,
                }
            except TypeError as e:
                return {
                    "jsonrpc": "2.0",
                    "error": {"code": -32602, "message": "Invalid params", "data": str(e)},
                    "id": request_id,
                }
            except Exception as e:
                logger.error(f"An unexpected error occurred: {e}", exc_info=True)
                return {
                    "jsonrpc": "2.0",
                    "error": {"code": -32000, "message": "Server error", "data": "An unexpected error occurred. See logs for details."},
                    "id": request_id,
                }
        else:
            return {
                "jsonrpc": "2.0",
                "error": {"code": -32601, "message": f"Method not found: Resource '{resource_uri}' not found."},
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
                    logger.info(f"Request data: stdio_main: {response_json}")
                    logger.info(f"Request data: stdio_main json: {json.dumps(response_json)}")
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
