from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict, Any, Callable

class Tool(BaseModel):
    """
    A tool that can be exposed by the MCP server.
    """
    name: str
    description: Optional[str] = None
    inputSchema: Optional[Dict[str, Any]] = None

class Prompt(BaseModel):
    """
    A prompt that can be exposed by the MCP server.
    """
    name: str
    title: Optional[str] = None
    description: Optional[str] = None
    arguments: List[Dict[str, Any]] = Field(default_factory=list)

class Resource(BaseModel):
    """
    A resource that can be exposed by the MCP server.
    """
    uri: str
    name: str
    description: Optional[str] = None
    mimeType: Optional[str] = None
    size: Optional[int] = None
