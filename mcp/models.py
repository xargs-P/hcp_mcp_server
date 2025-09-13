from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict, Any, Callable

class Tool(BaseModel):
    """
    A tool that can be exposed by the MCP server.
    """
    model_config = ConfigDict(arbitrary_types_allowed=True)

    name: str
    description: str
    parameters: Dict[str, Any]
    function: Callable

class Prompt(BaseModel):
    """
    A prompt that can be exposed by the MCP server.
    """
    name: str
    description: str
    template: str

class Resource(BaseModel):
    """
    A resource that can be exposed by the MCP server.
    """
    name: str
    description: str
    type: str
    resource_schema: Dict[str, Any]
