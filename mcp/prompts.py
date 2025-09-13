from typing import List, Dict

def format_prompt(prompt: str, inputs: Dict[str, str]) -> str:
    """
    Formats a prompt with the given inputs.
    """
    for key, value in inputs.items():
        prompt = prompt.replace(f"{{{key}}}", value)
    return prompt

# Prompts for single-step workflows
LIST_PROJECTS_PROMPT = "List all HCP projects."
LIST_USERS_PROMPT = "List all HCP users."
LIST_SECRETS_PROMPT = "List all secrets for the application '{app_name}' in project '{project_id}'."
DELETE_PROJECT_PROMPT = "Are you sure you want to delete the project '{project_name}' ({project_id})? This action cannot be undone."
DELETE_USER_PROMPT = "Are you sure you want to delete the user '{user_name}' ({user_id})? This action cannot be undone."
DELETE_SECRET_PROMPT = "Are you sure you want to delete the secret '{secret_name}' from the application '{app_name}' in project '{project_id}'? This action cannot be undone."
CREATE_PROJECT_PROMPT = "Create a new HCP project with the name '{project_name}' in the organization '{organization_id}'."
CREATE_USER_PROMPT = "Create a new HCP user with the name '{user_name}' and email '{user_email}'."
CREATE_SECRET_PROMPT = "Create a new secret with the name '{secret_name}' and value '{secret_value}' in the application '{app_name}' in project '{project_id}'."
LIST_ORGANIZATIONS_PROMPT = "List all HCP organizations."
GET_ORGANIZATION_PROMPT = "Get the HCP organization with the ID '{organization_id}'."
GET_PROJECT_PROMPT = "Get the HCP project with the ID '{project_id}' in the organization '{organization_id}'."
GET_USER_PROMPT = "Get the HCP user with the ID '{user_id}'."
GET_SECRET_PROMPT = "Get the secret with the name '{secret_name}' from the application '{app_name}' in project '{project_id}'."
UPDATE_USER_PROMPT = "Update the user with the ID '{user_id}' to have the name '{user_name}'."
UPDATE_PROJECT_PROMPT = "Update the project with the ID '{project_id}' to have the name '{project_name}'."
UPDATE_SECRET_PROMPT = "Update the secret with the name '{secret_name}' to have the value '{secret_value}'."
UPDATE_ORGANIZATION_PROMPT = "Update the organization with the ID '{organization_id}' to have the name '{organization_name}'."

# Prompts for multi-step workflows
# Example: Find a project by name, then list its secrets.
FIND_PROJECT_AND_LIST_SECRETS_PROMPT = """
1. Find the project with the name '{project_name}'.
2. List all secrets for the application '{app_name}' in that project.
"""

# Example: Find a project by name, then delete it.
FIND_PROJECT_AND_DELETE_PROJECT_PROMPT = """
1. Find the project with the name '{project_name}'.
2. {DELETE_PROJECT_PROMPT}
"""

# Example: Find a user by name, then delete them.
FIND_USER_AND_DELETE_USER_PROMPT = """
1. Find the user with the name '{user_name}'.
2. {DELETE_USER_PROMPT}
"""

# Example: Find a secret by name, then delete it.
FIND_SECRET_AND_DELETE_SECRET_PROMPT = """
1. Find the secret with the name '{secret_name}' in the application '{app_name}' in project '{project_id}'.
2. {DELETE_SECRET_PROMPT}
"""

# Example: Find an organization by name, then list its projects.
FIND_ORGANIZATION_AND_LIST_PROJECTS_PROMPT = """
1. Find the organization with the name '{organization_name}'.
2. List all projects in that organization.
"""

# Example: Find an organization by name, then create a new project in it.
FIND_ORGANIZATION_AND_CREATE_PROJECT_PROMPT = """
1. Find the organization with the name '{organization_name}'.
2. Create a new project with the name '{project_name}' in that organization.
"""

# Example: Find a project by name, then create a new secret in it.
FIND_PROJECT_AND_CREATE_SECRET_PROMPT = """
1. Find the project with the name '{project_name}'.
2. Create a new secret with the name '{secret_name}' and value '{secret_value}' in the application '{app_name}' in that project.
"""

# Example: Find a user by name, then create a new project for them.
FIND_USER_AND_CREATE_PROJECT_PROMPT = """
1. Find the user with the name '{user_name}'.
2. Create a new project with the name '{project_name}' for that user.
"""

# Example: Find a user by name, then create a new secret for them.
FIND_USER_AND_CREATE_SECRET_PROMPT = """
1. Find the user with the name '{user_name}'.
2. Create a new secret with the name '{secret_name}' and value '{secret_value}' for that user.
"""

# Example: Find an organization by name, then create a new user in it.
FIND_ORGANIZATION_AND_CREATE_USER_PROMPT = """
1. Find the organization with the name '{organization_name}'.
2. Create a new user with the name '{user_name}' and email '{user_email}' in that organization.
"""

# Example: Find a project by name, then create a new user in it.
FIND_PROJECT_AND_CREATE_USER_PROMPT = """
1. Find the project with the name '{project_name}'.
2. Create a new user with the name '{user_name}' and email '{user_email}' in that project.
"""

# Example: Find an organization by name, then delete a project in it.
FIND_ORGANIZATION_AND_DELETE_PROJECT_PROMPT = """
1. Find the organization with the name '{organization_name}'.
2. Delete the project with the name '{project_name}' in that organization.
"""

# Example: Find an organization by name, then delete a user in it.
FIND_ORGANIZATION_AND_DELETE_USER_PROMPT = """
1. Find the organization with the name '{organization_name}'.
2. Delete the user with the name '{user_name}' in that organization.
"""

# Example: Find a project by name, then delete a user in it.
FIND_PROJECT_AND_DELETE_USER_PROMPT = """
1. Find the project with the name '{project_name}'.
2. Delete the user with the name '{user_name}' in that project.
"""

# Example: Find an organization by name, then delete a secret in it.
FIND_ORGANIZATION_AND_DELETE_SECRET_PROMPT = """
1. Find the organization with the name '{organization_name}'.
2. Delete the secret with the name '{secret_name}' in that organization.
"""

# Example: Find a project by name, then delete a secret in it.
FIND_PROJECT_AND_DELETE_SECRET_PROMPT = """
1. Find the project with the name '{project_name}'.
2. Delete the secret with the name '{secret_name}' in that project.
"""

# Example: Find a user by name, then delete a project for them.
FIND_USER_AND_DELETE_PROJECT_PROMPT = """
1. Find the user with the name '{user_name}'.
2. Delete the project with the name '{project_name}' for that user.
"""

# Example: Find a user by name, then delete a secret for them.
FIND_USER_AND_DELETE_SECRET_PROMPT = """
1. Find the user with the name '{user_name}'.
2. Delete the secret with the name '{secret_name}' for that user.
"""

# Example: Find an organization by name, then get a project in it.
FIND_ORGANIZATION_AND_GET_PROJECT_PROMPT = """
1. Find the organization with the name '{organization_name}'.
2. Get the project with the name '{project_name}' in that organization.
"""

# Example: Find an organization by name, then get a user in it.
FIND_ORGANIZATION_AND_GET_USER_PROMPT = """
1. Find the organization with the name '{organization_name}'.
2. Get the user with the name '{user_name}' in that organization.
"""

# Example: Find an organization by name, then get a secret in it.
FIND_ORGANIZATION_AND_GET_SECRET_PROMPT = """
1. Find the organization with the name '{organization_name}'.
2. Get the secret with the name '{secret_name}' in that organization.
"""

# Example: Find a project by name, then get a user in it.
FIND_PROJECT_AND_GET_USER_PROMPT = """
1. Find the project with the name '{project_name}'.
2. Get the user with the name '{user_name}' in that project.
"""

# Example: Find a project by name, then get a secret in it.
FIND_PROJECT_AND_GET_SECRET_PROMPT = """
1. Find the project with the name '{project_name}'.
2. Get the secret with the name '{secret_name}' in that project.
"""

# Example: Find a user by name, then get a project for them.
FIND_USER_AND_GET_PROJECT_PROMPT = """
1. Find the user with the name '{user_name}'.
2. Get the project with the name '{project_name}' for that user.
"""

# Example: Find a user by name, then get a secret for them.
FIND_USER_AND_GET_SECRET_PROMPT = """
1. Find the user with the name '{user_name}'.
2. Get the secret with the name '{secret_name}' for that user.
"""

# Example: Find an organization by name, then list its users.
FIND_ORGANIZATION_AND_LIST_USERS_PROMPT = """
1. Find the organization with the name '{organization_name}'.
2. List all users in that organization.
"""

# Example: Find a project by name, then list its users.
FIND_PROJECT_AND_LIST_USERS_PROMPT = """
1. Find the project with the name '{project_name}'.
2. List all users in that project.
"""

# Example: Find a user by name, then list their projects.
FIND_USER_AND_LIST_PROJECTS_PROMPT = """
1. Find the user with the name '{user_name}'.
2. List all projects for that user.
"""

# Example: Find a user by name, then list their secrets.
FIND_USER_AND_LIST_SECRETS_PROMPT = """
1. Find the user with the name '{user_name}'.
2. List all secrets for that user.
"""

# Example: Find an organization by name, then list its secrets.
FIND_ORGANIZATION_AND_LIST_SECRETS_PROMPT = """
1. Find the organization with the name '{organization_name}'.
2. List all secrets in that organization.
"""

# Example: Find a user by name, then list their organizations.
FIND_USER_AND_LIST_ORGANIZATIONS_PROMPT = """
1. Find the user with the name '{user_name}'.
2. List all organizations for that user.
"""

# Example: Find an organization by name, then get its details.
FIND_ORGANIZATION_AND_GET_ORGANIZATION_PROMPT = """
1. Find the organization with the name '{organization_name}'.
2. Get the details for that organization.
"""

# Example: Find a project by name, then get its details.
FIND_PROJECT_AND_GET_PROJECT_PROMPT = """
1. Find the project with the name '{project_name}'.
2. Get the details for that project.
"""

# Example: Find a user by name, then get their details.
FIND_USER_AND_GET_USER_PROMPT = """
1. Find the user with the name '{user_name}'.
2. Get the details for that user.
"""

# Example: Find a secret by name, then get its details.
FIND_SECRET_AND_GET_SECRET_PROMPT = """
1. Find the secret with the name '{secret_name}'.
2. Get the details for that secret.
"""

# Example: Find an organization by name, then update it.
FIND_ORGANIZATION_AND_UPDATE_ORGANIZATION_PROMPT = """
1. Find the organization with the name '{organization_name}'.
2. Update the organization to have the name '{new_organization_name}'.
"""

# Example: Find a project by name, then update it.
FIND_PROJECT_AND_UPDATE_PROJECT_PROMPT = """
1. Find the project with the name '{project_name}'.
2. Update the project to have the name '{new_project_name}'.
"""

# Example: Find a user by name, then update them.
FIND_USER_AND_UPDATE_USER_PROMPT = """
1. Find the user with the name '{user_name}'.
2. Update the user to have the name '{new_user_name}'.
"""

# Example: Find a secret by name, then update it.
FIND_SECRET_AND_UPDATE_SECRET_PROMPT = """
1. Find the secret with the name '{secret_name}'.
2. Update the secret to have the value '{new_secret_value}'.
"""

# Example: Find an organization by name, then update a project in it.
FIND_ORGANIZATION_AND_UPDATE_PROJECT_PROMPT = """
1. Find the organization with the name '{organization_name}'.
2. Update the project with the name '{project_name}' to have the name '{new_project_name}'.
"""

# Example: Find an organization by name, then update a user in it.
FIND_ORGANIZATION_AND_UPDATE_USER_PROMPT = """
1. Find the organization with the name '{organization_name}'.
2. Update the user with the name '{user_name}' to have the name '{new_user_name}'.
"""

# Example: Find a project by name, then update a user in it.
FIND_PROJECT_AND_UPDATE_USER_PROMPT = """
1. Find the project with the name '{project_name}'.
2. Update the user with the name '{user_name}' to have the name '{new_user_name}'.
"""

# Example: Find an organization by name, then update a secret in it.
FIND_ORGANIZATION_AND_UPDATE_SECRET_PROMPT = """
1. Find the organization with the name '{organization_name}'.
2. Update the secret with the name '{secret_name}' to have the value '{new_secret_value}'.
"""

# Example: Find a project by name, then update a secret in it.
FIND_PROJECT_AND_UPDATE_SECRET_PROMPT = """
1. Find the project with the name '{project_name}'.
2. Update the secret with the name '{secret_name}' to have the value '{new_secret_value}'.
"""

# Example: Find a user by name, then update a project for them.
FIND_USER_AND_UPDATE_PROJECT_PROMPT = """
1. Find the user with the name '{user_name}'.
2. Update the project with the name '{project_name}' to have the name '{new_project_name}'.
"""

# Example: Find a user by name, then update a secret for them.
FIND_USER_AND_UPDATE_SECRET_PROMPT = """
1. Find the user with the name '{user_name}'.
2. Update the secret with the name '{secret_name}' to have the value '{new_secret_value}'.
"""
