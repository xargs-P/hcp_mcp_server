from mcp.models import Resource

def organization_resource():
    return Resource(
        uri="hcp://cloud.hashicorp.com/organizations/{organization_id}",
        name="hcp/organization",
        title="HCP Organization",
        description="An HCP organization.",
        mimeType="application/json",
    )

def project_resource():
    return Resource(
        uri="hcp://cloud.hashicorp.com/organizations/{organization_id}/projects/{project_id}",
        name="hcp/project",
        title="HCP Project",
        description="An HCP project.",
        mimeType="application/json",
    )

def user_resource():
    return Resource(
        uri="hcp://cloud.hashicorp.com/users/{user_id}",
        name="hcp/user",
        title="HCP User",
        description="An HCP user.",
        mimeType="application/json",
    )

def get_resources():
    """
    Returns a list of all available resources.
    """
    return [
        organization_resource(),
        project_resource(),
        user_resource(),
    ]
