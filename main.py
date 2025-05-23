# main.py
import asyncio
import logging
import os
from typing import List, Type, Optional, Dict, Any

# Imports from the official MCP SDK, guided by user's dir(mcp) output
from mcp.server import Server 
from mcp import (
    Tool, 
    Resource,
    Prompt, # Directly from mcp as per dir() output
    ToolCall,
    ToolResult,
    ToolInfo,
    ToolParameter, 
    Context,
    UpdateRequest,
    UpdateType,
    Error,
    ErrorCode,
    SamplingRole, # As per dir() output, likely equivalent to PromptRole
)
# PromptRole from mcp.prompts might not exist if mcp.prompts is not a module
# We will use SamplingRole and can alias it if needed conceptually.
# from mcp.prompts import PromptRole # Keeping this commented based on dir() and help()

from dotenv import load_dotenv

# Import clients (these remain unchanged)
from hcp_client import HcpClient
from iam_client import IamClient, IAM_API_VERSION
from resource_manager_client import ResourceManagerClient, RESOURCE_MANAGER_API_VERSION
from vault_secrets_client import VaultSecretsClient, VAULT_SECRETS_API_VERSION

# Import tools
from tools.resource_manager_tools import (
    ListOrganizationsTool,
    GetOrganizationTool,
    ListProjectsTool,
    GetProjectTool,
    GetOrganizationIamPolicyTool,
    SetOrganizationIamPolicyTool,
    GetProjectIamPolicyTool,
    SetProjectIamPolicyTool,
)
from tools.iam_tools import (
    ListServicePrincipalsOrgTool,
    CreateServicePrincipalOrgTool,
    GetServicePrincipalOrgTool,
    DeleteServicePrincipalOrgTool,
    ListServicePrincipalsProjectTool,
    CreateServicePrincipalProjectTool,
    GetServicePrincipalProjectTool,
    DeleteServicePrincipalProjectTool,
    CreateServicePrincipalKeyOrgTool,
    CreateServicePrincipalKeyProjectTool,
    ListGroupsTool,
    CreateGroupTool,
    GetGroupTool,
)
from tools.vault_secrets_tools import (
    ListVaultAppsTool,
    CreateVaultAppTool,
    GetVaultAppTool,
    DeleteVaultAppTool,
    CreateVaultKvSecretTool,
    OpenVaultKvSecretTool,
    DeleteVaultKvSecretTool,
    ListVaultAppSecretsTool,
)

# Import resources
from resources.hcp_resources import (
    HcpOrganizationResource,
    HcpProjectResource,
    HcpServicePrincipalResource,
    HcpGroupResource,
    HcpVaultAppResource,
    HcpVaultKvSecretResource,
    HcpIamPolicyResource,
)

# Import prompts
from prompts.hcp_prompts import (
    HcpInitialPrompt,
    HcpToolSelectionPrompt,
    HcpClarifyOrgIdPrompt,
    HcpClarifyProjectIdPrompt,
    HcpClarifyAppNamePrompt,
    HcpClarifySecretNamePrompt,
    HcpHandleErrorPrompt,
    HcpSummarizeActionResultPrompt,
    HcpAskForMissingInfoPrompt,
    HcpConfirmActionPrompt,
)

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- Constants ---
HCP_API_BASE_URL = "https://api.cloud.hashicorp.com"
HCP_AUTH_URL = "https://auth.idp.hashicorp.com/oauth/token"

# For clarity, let's use an alias if PromptRole was the intended semantic name
PromptRole = SamplingRole

def create_tool_info_from_tool_instance(tool: Tool) -> ToolInfo:
    """
    Helper function to create ToolInfo from a Tool instance.
    """
    return ToolInfo(
        name=tool.name,
        description=tool.description,
        parameters=tool.parameters 
    )

class HcpMcpServer(Server): 
    """
    MCP Server for interacting with HashiCorp Cloud Platform.
    Adapted to use the official 'mcp' Python SDK.
    """
    def __init__(self, hcp_client_id: str, hcp_client_secret: str):
        self.hcp_client = HcpClient(HCP_API_BASE_URL, HCP_AUTH_URL, hcp_client_id, hcp_client_secret)
        self.iam_client = IamClient(self.hcp_client)
        self.resource_manager_client = ResourceManagerClient(self.hcp_client)
        self.vault_secrets_client = VaultSecretsClient(self.hcp_client)

        self._tools: Dict[str, Tool] = self._register_tools()
        self._prompts: List[Type[Prompt]] = self._register_prompts()
        
        self.current_context: Context = Context(resources=[], tool_infos=self.get_tool_infos())

    def _register_tools(self) -> Dict[str, Tool]:
        """Registers all available HCP tools."""
        tools_list: List[Tool] = [ 
            # Resource Manager Tools
            ListOrganizationsTool(self.resource_manager_client),
            GetOrganizationTool(self.resource_manager_client),
            ListProjectsTool(self.resource_manager_client),
            GetProjectTool(self.resource_manager_client),
            GetOrganizationIamPolicyTool(self.resource_manager_client),
            SetOrganizationIamPolicyTool(self.resource_manager_client),
            GetProjectIamPolicyTool(self.resource_manager_client),
            SetProjectIamPolicyTool(self.resource_manager_client),

            # IAM Tools
            ListServicePrincipalsOrgTool(self.iam_client),
            CreateServicePrincipalOrgTool(self.iam_client),
            GetServicePrincipalOrgTool(self.iam_client),
            DeleteServicePrincipalOrgTool(self.iam_client),
            ListServicePrincipalsProjectTool(self.iam_client),
            CreateServicePrincipalProjectTool(self.iam_client),
            GetServicePrincipalProjectTool(self.iam_client),
            DeleteServicePrincipalProjectTool(self.iam_client),
            CreateServicePrincipalKeyOrgTool(self.iam_client),
            CreateServicePrincipalKeyProjectTool(self.iam_client),
            ListGroupsTool(self.iam_client),
            CreateGroupTool(self.iam_client),
            GetGroupTool(self.iam_client),
            
            # Vault Secrets Tools
            ListVaultAppsTool(self.vault_secrets_client),
            CreateVaultAppTool(self.vault_secrets_client),
            GetVaultAppTool(self.vault_secrets_client),
            DeleteVaultAppTool(self.vault_secrets_client),
            CreateVaultKvSecretTool(self.vault_secrets_client),
            OpenVaultKvSecretTool(self.vault_secrets_client),
            DeleteVaultKvSecretTool(self.vault_secrets_client),
            ListVaultAppSecretsTool(self.vault_secrets_client),
        ]
        return {tool.name: tool for tool in tools_list}

    def _register_prompts(self) -> List[Type[Prompt]]:
        """Registers all available HCP prompts."""
        return [
            HcpInitialPrompt,
            HcpToolSelectionPrompt,
            HcpClarifyOrgIdPrompt,
            HcpClarifyProjectIdPrompt,
            HcpClarifyAppNamePrompt,
            HcpClarifySecretNamePrompt,
            HcpHandleErrorPrompt,
            HcpSummarizeActionResultPrompt,
            HcpAskForMissingInfoPrompt,
            HcpConfirmActionPrompt,
        ]

    async def get_context(self, session_id: Optional[str] = None) -> Context:
        """
        Provides the initial context to the LLM, including available tools and resources.
        """
        logger.info(f"Getting initial context for LLM. Session ID: {session_id}")
        self.current_context.tool_infos = self.get_tool_infos()
        return self.current_context

    async def execute_tool_call(self, call: ToolCall, session_id: Optional[str] = None) -> ToolResult:
        """
        Executes a tool based on the LLM's request.
        Signature matches mcp.server.Server.
        """
        logger.info(f"Executing tool: {call.name} with params: {call.params} for Session ID: {session_id}")
        tool = self._tools.get(call.name)
        if not tool:
            logger.error(f"Tool not found: {call.name}")
            return ToolResult(
                tool_call_id=call.tool_call_id, 
                content_text="Tool not found.", 
                error=Error(code=ErrorCode.TOOL_NOT_FOUND, message=f"Tool '{call.name}' not found.")
            )

        try:
            if not await self.hcp_client.ensure_authenticated():
                 return ToolResult(
                    tool_call_id=call.tool_call_id,
                    content_text="Failed to authenticate with HCP.",
                    error=Error(code=ErrorCode.AUTHENTICATION_ERROR, message="HCP authentication failed.")
                )

            result_content_str, produced_resources_list = await tool(**call.params) 
            
            if produced_resources_list:
                for res in produced_resources_list:
                    if not isinstance(res, Resource):
                        logger.error(f"Tool {call.name} produced a non-Resource object: {type(res)}")
                        continue
                    
                    if not any(existing_res.id == res.id for existing_res in self.current_context.resources):
                         self.current_context.resources.append(res)
                logger.info(f"Context updated with {len(produced_resources_list)} new resource(s).")

            return ToolResult(
                tool_call_id=call.tool_call_id, 
                content_text=result_content_str, 
                resources=produced_resources_list
            )
        except Exception as e:
            logger.exception(f"Error executing tool {call.name}: {e}")
            return ToolResult(
                tool_call_id=call.tool_call_id,
                content_text=f"An error occurred: {str(e)}",
                error=Error(code=ErrorCode.TOOL_EXECUTION_ERROR, message=str(e))
            )

    def get_tool_infos(self) -> List[ToolInfo]:
        """Returns information about all registered tools."""
        return [create_tool_info_from_tool_instance(tool) for tool in self._tools.values()]

    async def process_update(self, update: UpdateRequest, session_id: Optional[str] = None) -> None:
        """
        Handles updates from the client.
        Signature matches mcp.server.Server.
        """
        logger.info(f"Received update: {update.update_type} for resource ID: {update.resource.id if update.resource else 'N/A'}. Session ID: {session_id}")
        if update.update_type == UpdateType.ADD or update.update_type == UpdateType.MODIFY:
            if update.resource:
                if not isinstance(update.resource, Resource):
                    logger.error(f"Received update with non-Resource object: {type(update.resource)}")
                    return
                self.current_context.resources = [res for res in self.current_context.resources if res.id != update.resource.id]
                self.current_context.resources.append(update.resource)
                logger.info(f"Resource {update.resource.id} added/modified in context.")
        elif update.update_type == UpdateType.REMOVE:
            if update.resource_id: 
                self.current_context.resources = [res for res in self.current_context.resources if res.id != update.resource_id]
                logger.info(f"Resource {update.resource_id} removed from context.")

async def main():
    """Main function to run the server."""
    hcp_client_id = os.getenv("HCP_CLIENT_ID")
    hcp_client_secret = os.getenv("HCP_CLIENT_SECRET")

    if not hcp_client_id or not hcp_client_secret:
        logger.error("HCP_CLIENT_ID and HCP_CLIENT_SECRET environment variables must be set.")
        return

    server = HcpMcpServer(hcp_client_id, hcp_client_secret)
    
    logger.info("HCP MCP Server initialized and ready (adapted for official 'mcp' Python SDK).")
    logger.info(f"Registered tools: {[tool_name for tool_name in server._tools.keys()]}")
    logger.info(f"Registered prompts: {[prompt_type.__name__ for prompt_type in server._prompts]}")
    logger.info(f"IAM API Version: {IAM_API_VERSION}")
    logger.info(f"Resource Manager API Version: {RESOURCE_MANAGER_API_VERSION}")
    logger.info(f"Vault Secrets API Version: {VAULT_SECRETS_API_VERSION}")

    # Example: Simulate getting context
    test_session_id = "test-session-123"
    initial_context = await server.get_context(session_id=test_session_id) 
    logger.info(f"Initial context for session '{test_session_id}' has {len(initial_context.tool_infos)} tools and {len(initial_context.resources)} resources.")

if __name__ == "__main__":
    asyncio.run(main())
