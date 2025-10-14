from mcp.models import Prompt

LIST_PROJECTS_PROMPT = Prompt(
    name="list_projects",
    title="List Projects",
    description="Lists all HCP projects for a given organization.",
    arguments=[
        {
            "name": "organization_id",
            "description": "The ID of the organization.",
            "required": True,
        }
    ],
)

GET_PROJECT_PROMPT = Prompt(
    name="get_project",
    title="Get Project",
    description="Gets an HCP project by its ID.",
    arguments=[
        {
            "name": "project_id",
            "description": "The ID of the project.",
            "required": True,
        },
    ],
)

DELETE_PROJECT_PROMPT = Prompt(
    name="delete_project",
    title="Delete Project",
    description="Deletes an HCP project by its ID.",
    arguments=[
        {
            "name": "project_id",
            "description": "The ID of the project.",
            "required": True,
        },
    ],
)

CREATE_PROJECT_PROMPT = Prompt(
    name="create_project",
    title="Create Project",
    description="Creates a new HCP project.",
    arguments=[
        {
            "name": "name",
            "description": "The name of the new project.",
            "required": True,
        },
        {
            "name": "organization_id",
            "description": "The ID of the organization.",
            "required": True,
        },
    ],
)

UPDATE_PROJECT_PROMPT = Prompt(
    name="update_project",
    title="Update Project",
    description="Updates an HCP project.",
    arguments=[
        {
            "name": "project_id",
            "description": "The ID of the project.",
            "required": True,
        },
        {
            "name": "name",
            "description": "The new name for the project.",
            "required": True,
        },
        {
            "name": "organization_id",
            "description": "The ID of the organization.",
            "required": True,
        },
    ],
)

GET_ORGANIZATION_PROMPT = Prompt(
    name="get_organization",
    title="Get Organization",
    description="Gets an HCP organization by its ID.",
    arguments=[
        {
            "name": "organization_id",
            "description": "The ID of the organization.",
            "required": True,
        }
    ],
)

LIST_ORGANIZATIONS_PROMPT = Prompt(
    name="list_organizations",
    title="List Organizations",
    description="Lists all HCP organizations.",
)

UPDATE_ORGANIZATION_PROMPT = Prompt(
    name="update_organization",
    title="Update Organization",
    description="Updates an HCP organization.",
    arguments=[
        {
            "name": "organization_id",
            "description": "The ID of the organization.",
            "required": True,
        },
        {
            "name": "name",
            "description": "The new name for the organization.",
            "required": True,
        },
    ],
)



LIST_SECRETS_PROMPT = Prompt(
    name="list_secrets",
    title="List Secrets",
    description="Lists all secrets for a given application.",
    arguments=[
        {
            "name": "project_id",
            "description": "The ID of the project.",
            "required": True,
        },
        {
            "name": "app_name",
            "description": "The name of the application.",
            "required": True,
        },
    ],
)

GET_SECRET_PROMPT = Prompt(
    name="get_secret",
    title="Get Secret",
    description="Gets a secret by its name.",
    arguments=[
        {
            "name": "secret_name",
            "description": "The name of the secret.",
            "required": True,
        },
        {
            "name": "project_id",
            "description": "The ID of the project.",
            "required": True,
        },
        {
            "name": "app_name",
            "description": "The name of the application.",
            "required": True,
        },
    ],
)

DELETE_SECRET_PROMPT = Prompt(
    name="delete_secret",
    title="Delete Secret",
    description="Deletes a secret by its name.",
    arguments=[
        {
            "name": "secret_name",
            "description": "The name of the secret.",
            "required": True,
        },
        {
            "name": "project_id",
            "description": "The ID of the project.",
            "required": True,
        },
        {
            "name": "app_name",
            "description": "The name of the application.",
            "required": True,
        },
    ],
)

CREATE_SECRET_PROMPT = Prompt(
    name="create_secret",
    title="Create Secret",
    description="Creates a new secret.",
    arguments=[
        {
            "name": "secret_name",
            "description": "The name of the new secret.",
            "required": True,
        },
        {
            "name": "secret_value",
            "description": "The value of the new secret.",
            "required": True,
        },
        {
            "name": "project_id",
            "description": "The ID of the project.",
            "required": True,
        },
        {
            "name": "app_name",
            "description": "The name of the application.",
            "required": True,
        },
    ],
)



FIND_PROJECT_AND_LIST_SECRETS_PROMPT = Prompt(
    name="find_project_and_list_secrets",
    title="Find Project and List Secrets",
    description="Finds a project by name and lists its secrets.",
    arguments=[
        {
            "name": "project_name",
            "description": "The name of the project.",
            "required": True,
        },
        {
            "name": "organization_id",
            "description": "The ID of the organization.",
            "required": True,
        },
        {
            "name": "app_name",
            "description": "The name of the application.",
            "required": True,
        },
    ],
)

LIST_RESOURCES_PROMPT = Prompt(
    name="list_resources",
    title="List Resources",
    description="Lists all resources in a project.",
    arguments=[
        {
            "name": "project_id",
            "description": "The ID of the project.",
            "required": True,
        }
    ],
)

SEARCH_LOGS_PROMPT = Prompt(
    name="search_logs",
    title="Search Logs",
    description=(
        "Searches for audit logs in an organization using LogQL. "
        "The LLM should determine the best topic to use based on the user's query, or default to 'hashicorp.platform.audit' if the user is not specific. "
        "For advanced filtering, use the `query` parameter with LogQL syntax. "
        "To filter on specific JSON fields in the log entries, use the `| json` parser in your query. "
        'For example: `query=\'| json | control_plane_event_action="CREATE"\'`'
    ),
    arguments=[
        {
            "name": "organization_id",
            "description": "The ID of the organization.",
            "required": True,
        },
        {
            "name": "query",
            "description": (
                "The LogQL query string for advanced filtering. "
                "Can be combined with `project_id` and `topic`. "
                "Example: '| json | resource_uuid=\"some-uuid\"'"
            ),
            "required": False,
        },
        {
            "name": "project_id",
            "description": "A project ID to filter by.",
            "required": False,
        },
        {
            "name": "topic",
            "description": (
                "A log topic to search. Example topics: 'hashicorp.platform.audit', 'hashicorp.packer.registry.audit', "
                "'hashicorp.boundary.cluster.audit', 'hashicorp.consul.cluster.audit'"
            ),
            "required": False,
        },
        {
            "name": "start_time",
            "description": "The start time for the search. Accepts formats like '24 hours ago', 'yesterday at 5pm', or 'Oct 1, 2025'.",
            "required": True,
        },
        {
            "name": "end_time",
            "description": "The end time for the search. Accepts formats like 'now', 'today', or 'Oct 3, 2025'.",
            "required": True,
        }
    ],
)