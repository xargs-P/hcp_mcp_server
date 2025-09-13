from mcp.models import Resource

def organization_resource():
    return Resource(
        name="hcp/organization",
        description="An HCP organization.",
        type="object",
        resource_schema={
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "The ID of the organization."},
                "name": {"type": "string", "description": "The name of the organization."},
                "created_at": {"type": "string", "description": "The timestamp when the organization was created."},
            },
            "required": ["id", "name", "created_at"],
        },
    )

def project_resource():
    return Resource(
        name="hcp/project",
        description="An HCP project.",
        type="object",
        resource_schema={
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "The ID of the project."},
                "name": {"type": "string", "description": "The name of the project."},
                "organization_id": {"type": "string", "description": "The ID of the organization the project belongs to."},
                "created_at": {"type": "string", "description": "The timestamp when the project was created."},
            },
            "required": ["id", "name", "organization_id", "created_at"],
        },
    )

def user_resource():
    return Resource(
        name="hcp/user",
        description="An HCP user.",
        type="object",
        resource_schema={
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "The ID of the user."},
                "name": {"type": "string", "description": "The name of the user."},
                "email": {"type": "string", "description": "The email of the user."},
            },
            "required": ["id", "name", "email"],
        },
    )

def get_resources():
    """
    Returns a list of all available resources.
    """
    return [
        organization_resource().model_dump(),
        project_resource().model_dump(),
        user_resource().model_dump(),
    ]
