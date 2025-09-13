from pydantic import BaseModel
from typing import List, Dict

class Resource(BaseModel):
    """
    A resource that can be exposed by the MCP server.
    """
    name: str
    description: str
    properties: Dict[str, str]

class Project(Resource):
    """
    An HCP project.
    """
    name: str = "Project"
    description: str = "A HashiCorp Cloud Platform project."
    properties: Dict[str, str] = {
        "id": "The project's unique identifier.",
        "name": "The project's name.",
        "organization_id": "The ID of the organization the project belongs to.",
    }

class User(Resource):
    """
    An HCP user.
    """
    name: str = "User"
    description: str = "A HashiCorp Cloud Platform user."
    properties: Dict[str, str] = {
        "email": "The user's email address.",
        "name": "The user's name.",
    }

class Secret(Resource):
    """
    An HCP Vault secret.
    """
    name: str = "Secret"
    description: str = "A secret stored in HCP Vault."
    properties: Dict[str, str] = {
        "name": "The secret's name.",
        "value": "The secret's value.",
    }

class Organization(Resource):
    """
    An HCP organization.
    """
    name: str = "Organization"
    description: str = "A HashiCorp Cloud Platform organization."
    properties: Dict[str, str] = {
        "id": "The organization's unique identifier.",
        "name": "The organization's name.",
    }