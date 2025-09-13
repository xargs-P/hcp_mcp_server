from mcp.models import Prompt

LIST_PROJECTS_PROMPT = Prompt(
    name="list_projects",
    description="Lists all HCP projects for a given organization.",
    template="List all projects for organization {organization_id}.",
)

GET_PROJECT_PROMPT = Prompt(
    name="get_project",
    description="Gets an HCP project by its ID.",
    template="Get project {project_id} for organization {organization_id}.",
)

DELETE_PROJECT_PROMPT = Prompt(
    name="delete_project",
    description="Deletes an HCP project by its ID.",
    template="Delete project {project_id} for organization {organization_id}.",
)

CREATE_PROJECT_PROMPT = Prompt(
    name="create_project",
    description="Creates a new HCP project.",
    template="Create a new project named {name} for organization {organization_id}.",
)

UPDATE_PROJECT_PROMPT = Prompt(
    name="update_project",
    description="Updates an HCP project.",
    template="Update project {project_id} with name {name} for organization {organization_id}.",
)

GET_ORGANIZATION_PROMPT = Prompt(
    name="get_organization",
    description="Gets an HCP organization by its ID.",
    template="Get organization {organization_id}.",
)

LIST_ORGANIZATIONS_PROMPT = Prompt(
    name="list_organizations",
    description="Lists all HCP organizations.",
    template="List all organizations.",
)

UPDATE_ORGANIZATION_PROMPT = Prompt(
    name="update_organization",
    description="Updates an HCP organization.",
    template="Update organization {organization_id} with name {name}.",
)

LIST_USERS_PROMPT = Prompt(
    name="list_users",
    description="Lists all HCP users.",
    template="List all users.",
)

GET_USER_PROMPT = Prompt(
    name="get_user",
    description="Gets an HCP user by their ID.",
    template="Get user {user_id}.",
)

DELETE_USER_PROMPT = Prompt(
    name="delete_user",
    description="Deletes an HCP user by their ID.",
    template="Delete user {user_id}.",
)

CREATE_USER_PROMPT = Prompt(
    name="create_user",
    description="Creates a new HCP user.",
    template="Create a new user with name {name} and email {email}.",
)

UPDATE_USER_PROMPT = Prompt(
    name="update_user",
    description="Updates an HCP user.",
    template="Update user {user_id} with name {name}.",
)

LIST_SECRETS_PROMPT = Prompt(
    name="list_secrets",
    description="Lists all secrets for a given application.",
    template="List all secrets for project {project_id} and application {app_name}.",
)

GET_SECRET_PROMPT = Prompt(
    name="get_secret",
    description="Gets a secret by its name.",
    template="Get secret {secret_name} for project {project_id} and application {app_name}.",
)

DELETE_SECRET_PROMPT = Prompt(
    name="delete_secret",
    description="Deletes a secret by its name.",
    template="Delete secret {secret_name} for project {project_id} and application {app_name}.",
)

CREATE_SECRET_PROMPT = Prompt(
    name="create_secret",
    description="Creates a new secret.",
    template="Create a new secret named {secret_name} with value {secret_value} for project {project_id} and application {app_name}.",
)

UPDATE_SECRET_PROMPT = Prompt(
    name="update_secret",
    description="Updates a secret.",
    template="Update secret {secret_name} with value {secret_value} for project {project_id} and application {app_name}.",
)

FIND_PROJECT_AND_LIST_SECRETS_PROMPT = Prompt(
    name="find_project_and_list_secrets",
    description="Finds a project by name and lists its secrets.",
    template="Find project {project_name} for organization {organization_id} and list its secrets for application {app_name}.",
)

FIND_PROJECT_AND_DELETE_PROJECT_PROMPT = Prompt(
    name="find_project_and_delete_project",
    description="Finds a project by name and deletes it.",
    template="Find project {project_name} for organization {organization_id} and delete it.",
)

FIND_USER_AND_DELETE_USER_PROMPT = Prompt(
    name="find_user_and_delete_user",
    description="Finds a user by email and deletes them.",
    template="Find user with email {email} and delete them.",
)
