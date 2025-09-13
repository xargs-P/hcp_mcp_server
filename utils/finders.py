from hcp.resource_manager import list_organizations, list_projects
from hcp.iam import list_users

async def find_organization_by_name(name: str):
    """
    Finds an organization by its name.
    """
    organizations = await list_organizations()
    for org in organizations.get("organizations", []):
        if org.get("name") == name:
            return org
    return None

async def find_project_by_name(organization_id: str, name: str):
    """
    Finds a project by its name within a given organization.
    """
    projects = await list_projects(organization_id)
    for proj in projects.get("projects", []):
        if proj.get("name") == name:
            return proj
    return None

async def find_user_by_email(email: str):
    """
    Finds a user by their email address.
    """
    users = await list_users()
    for user in users.get("users", []):
        if user.get("email") == email:
            return user
    return None
