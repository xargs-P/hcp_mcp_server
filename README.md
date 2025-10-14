# HCP MCP Server

This server implements the Model Context Protocol (MCP) to provide a natural language interface to the HashiCorp Cloud Platform (HCP).

## Architecture

The server is built to support the Model Context Protocol (MCP) and follows a modular structure:

-   **`main.py`**: The main entry point for the application. It runs as a stdio-based MCP transport, handles incoming requests, and maps them to the appropriate tools.
-   **`hcp/`**: This directory contains modules for interacting with the HCP API.
    -   `auth.py`: Handles OAuth2 authentication with HCP to retrieve access tokens.
    -   `iam.py`: Contains functions for interacting with the HCP IAM API (users, roles, etc.).
    -   `resource_manager.py`: Contains functions for interacting with the HCP Resource Manager API (organizations, projects).
    -   `vault.py`: Contains functions for interacting with the HCP Vault Secrets API.
-   **`mcp/`**: This directory contains modules that define the MCP-specific components.
    -   `models.py`: Defines the data models for the resources exposed by the server (e.g., Project, User, Secret).
    -   `tools.py`: Defines the tools that the LLM can use to interact with the HCP API.
    -   `prompts.py`: Contains predefined prompts for single and multi-step workflows.
-   **`utils/`**: This directory contains helper functions.
    -   `finders.py`: Includes functions to resolve resource names (e.g., project name) to their corresponding IDs, which is often required by the HCP API.

## Core Features

-   **HCP API Integration**: The server connects directly to the official HCP APIs for IAM, Resource Manager, and Vault Secrets.
-   **Authentication**: Securely authenticates with HCP using a client ID and secret to obtain a bearer token for API calls.
-   **Resource Management**:
    -   **Organizations**: List and retrieve organization details.
    -   **Projects**: Create, read, update, and delete projects.
    -   **Users**: Create, read, update, and delete users.
    -   **Vault Secrets**: Create, read, update, and delete secrets within HCP Vault applications.
-   **Name-to-ID Resolution**: Provides utility functions to find resources like organizations, projects, and users by name or email, simplifying the user experience for the LLM.
-   **Comprehensive Prompts**: Includes a wide range of prompts to guide LLMs in performing both simple (e.g., "list all projects") and complex multi-step (e.g., "find a project by name and then create a secret in it") workflows.
-   **Gemini CLI Compatibility**: Configurable as a local MCP server for the Gemini CLI.

## Setup

1.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Set up environment variables:**
    Export the following variables in the shell for the HCP MCP server OR create a `.env` file in the root of the project and add the following:
    ```
    HCP_CLIENT_ID="your_hcp_client_id"
    HCP_CLIENT_SECRET="your_hcp_client_secret"
    ```
    
4.  **Configure with Gemini CLI:**
    Update your `settings.json` for the Gemini CLI to include the following:
    ```json
    {
      "mcp_server": {
        "enabled": true,
        "path": "/path/to/your/hcp_mcp_server/main.py"
      }
    }
    ```

5.  **Run the server:**
    The server is designed to be run as a stdio-based MCP transport. When the Gemini CLI starts, it will automatically run the server.
