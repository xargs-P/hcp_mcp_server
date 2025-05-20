# hcp_mcp_server/models/__init__.py
# Pydantic models for request/response validation if needed.
# For now, MCP is flexible, so we might not need strict models here,
# but this is a good place for them if schemas become more defined.

from pydantic import BaseModel
from typing import List, Optional, Dict, Any

# Example: If MCP responses were standardized
class MCPResponse(BaseModel):
    resource_uri: str
    context_data: Dict[str, Any]
    error: Optional[str] = None

class HCPOrganization(BaseModel):
    id: str
    display_name: Optional[str] = None
    created_at: Optional[str] = None # Consider datetime type
    resource_name: str
    # Add other fields as per actual API response

class HCPProject(BaseModel):
    id: str
    display_name: Optional[str] = None
    organization_id: str
    created_at: Optional[str] = None # Consider datetime type
    resource_name: str
    # Add other fields

# These are illustrative. The actual data returned from HCP APIs will be directly passed through
# or lightly transformed into the MCP JSON response.