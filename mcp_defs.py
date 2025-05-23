# mcp_defs.py
"""
Core definitions for Model Context Protocol (MCP) Resources, Tools, and Prompts.
These structures are used by service-specific modules to define their capabilities.
"""
from typing import List, Dict, Any, Callable, Optional

# --- MCP Resource Definitions ---
# This dictionary will store information about resource types the server understands.
# The value can be a simple description or a more complex schema.
# Example: MCP_RESOURCES["hcp:iam:user"] = {"description": "An HCP User Principal", "schema": { ... }}
MCP_RESOURCES: Dict[str, Any] = {}

# --- MCP Tool Definition ---
class MCPTool:
    """
    Represents a tool that an LLM can use, as defined by the MCP specification.
    """
    def __init__(self, name: str, description: str, input_schema: Dict[str, Any], func: Callable):
        """
        Initializes an MCPTool.
        Args:
            name (str): The unique name of the tool (e.g., "iam_list_users").
            description (str): A human-readable description of what the tool does.
            input_schema (Dict[str, Any]): A JSON schema describing the expected input parameters for the tool.
            func (Callable): The Python function that implements the tool's logic.
                             This function should accept parameters as defined in input_schema
                             and return a dictionary (typically with 'success', 'data'/'error' keys).
        """
        self.name = name
        self.description = description
        self.input_schema = input_schema
        self.func = func

    def to_dict(self) -> Dict[str, Any]:
        """
        Returns a dictionary representation of the tool, suitable for the /tools MCP endpoint.
        """
        return {
            "name": self.name,
            "description": self.description,
            "input_schema": self.input_schema,
        }

# Global registry for all tools available on the server.
MCP_TOOLS: Dict[str, MCPTool] = {}

# --- MCP Prompt Definition ---
class MCPPrompt:
    """
    Represents a prompt that can guide an LLM's interaction with the MCP server,
    as defined by the MCP specification.
    """
    def __init__(self, name: str, system_message: str, user_message_template: str, description: Optional[str] = None):
        """
        Initializes an MCPPrompt.
        Args:
            name (str): The unique name of the prompt.
            description (Optional[str]): A human-readable description of the prompt's purpose.
            system_message (str): The system message to provide context to the LLM.
            user_message_template (str): A template for the user message, potentially with placeholders.
                                         (Placeholders are for documentation; actual formatting is up to the LLM client).
        """
        self.name = name
        self.description = description
        self.system_message = system_message
        self.user_message_template = user_message_template

    def to_dict(self) -> Dict[str, Any]:
        """
        Returns a dictionary representation of the prompt, suitable for the /prompts MCP endpoint.
        """
        data = {
            "name": self.name,
            "system_message": self.system_message,
            "user_message_template": self.user_message_template,
        }
        if self.description:
            data["description"] = self.description
        return data

# Global registry for all prompts available on the server.
MCP_PROMPTS: Dict[str, MCPPrompt] = {}


