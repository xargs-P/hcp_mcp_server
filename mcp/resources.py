from mcp.models import Resource

def organization_resource():
    return Resource(
        uri="hcp://resource-manager.hashicorp.cloud/organization/{organization_id}",
        name="hcp/organization",
        description="An HCP organization.",
        mimeType="application/json",
    )

def project_resource():
    return Resource(
        uri="hcp://resource-manager.hashicorp.cloud/project/{project_id}",
        name="hcp/project",
        description="An HCP project.",
        mimeType="application/json",
    )

def get_resources():
    """
    Returns a list of all available resources.
    """
    return [
        organization_resource(),
        project_resource(),
    ]
