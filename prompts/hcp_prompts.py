# prompts/hcp_prompts.py
from dataclasses import dataclass

# Imports from the official MCP SDK
# Corrected: Prompt is from mcp (re-exported from mcp.types as per dir() output)
from mcp import Prompt 
from mcp.prompts import PromptRole # PromptRole is in mcp.prompts as per README

# --- General Prompts ---
@dataclass
class HcpInitialPrompt(Prompt): 
    role: PromptRole = PromptRole.SYSTEM 
    content: str = (
        "You are an AI assistant for managing HashiCorp Cloud Platform (HCP) resources. "
        "You can list, get, create, and delete resources like organizations, projects, "
        "service principals, IAM groups, Vault Secrets applications, and KV secrets. "
        "Please specify the action you want to perform and provide necessary identifiers "
        "like organization_id, project_id, app_name, or secret_name when prompted. "
        "If you provide a name instead of an ID, I may need to list resources first to find the ID. "
        "API versions used: IAM & Resource Manager - 2019-12-10, Vault Secrets - 2023-11-28."
    )

@dataclass
class HcpToolSelectionPrompt(Prompt):
    role: PromptRole = PromptRole.SYSTEM
    content: str = (
        "Based on the user's request, select the most appropriate HCP tool. "
        "Ensure you have all required parameters. If critical IDs (like organization_id, project_id) "
        "are missing, use a clarification prompt to ask for them or suggest listing resources to find them."
    )

# --- Clarification Prompts ---
@dataclass
class HcpClarifyOrgIdPrompt(Prompt):
    role: PromptRole = PromptRole.ASSISTANT
    organization_name: str = ""
    # content is dynamically generated in __post_init__
    
    def __post_init__(self):
        if self.organization_name:
             self.content = (
                f"I found an organization named '{self.organization_name}', but I need its ID. "
                "Could you please provide the Organization ID? "
                "Alternatively, I can list your organizations if you'd like to choose from a list."
            )
        else:
            self.content = (
                "I need an Organization ID to perform this action. "
                "Please provide the Organization ID, or I can list your organizations."
            )


@dataclass
class HcpClarifyProjectIdPrompt(Prompt):
    role: PromptRole = PromptRole.ASSISTANT
    project_name: str = ""
    organization_id: str = "" 
    
    def __post_init__(self):
        org_context = f" within organization '{self.organization_id}'" if self.organization_id else ""
        if self.project_name:
            self.content = (
                f"I found a project named '{self.project_name}'{org_context}, but I need its ID. "
                "Could you please provide the Project ID? "
                f"Alternatively, I can list projects{org_context} if you'd like to choose."
            )
        else:
            self.content = (
                f"I need a Project ID{org_context} to perform this action. "
                "Please provide the Project ID, or I can list projects."
            )

@dataclass
class HcpClarifyAppNamePrompt(Prompt):
    role: PromptRole = PromptRole.ASSISTANT
    app_name_suggestion: str = ""
    project_id: str = "" 
    
    def __post_init__(self):
        proj_context = f" within project '{self.project_id}'" if self.project_id else ""
        if self.app_name_suggestion:
            self.content = (
                f"You mentioned an application like '{self.app_name_suggestion}'{proj_context}. "
                "Could you please confirm the exact Application Name? "
                f"Alternatively, I can list applications{proj_context}."
            )
        else:
            self.content = (
                f"I need a Vault Secrets Application Name{proj_context} to perform this action. "
                "Please provide the Application Name, or I can list applications."
            )

@dataclass
class HcpClarifySecretNamePrompt(Prompt):
    role: PromptRole = PromptRole.ASSISTANT
    secret_name_suggestion: str = ""
    app_name: str = "" 
    project_id: str = "" 
    
    def __post_init__(self):
        app_context = f" within application '{self.app_name}' (project '{self.project_id}')" if self.app_name and self.project_id else ""
        if self.secret_name_suggestion:
            self.content = (
                f"You mentioned a secret like '{self.secret_name_suggestion}'{app_context}. "
                "Could you please confirm the exact Secret Name? "
                f"Alternatively, I can list secrets{app_context}."
            )
        else:
            self.content = (
                f"I need a Secret Name{app_context} to perform this action. "
                "Please provide the Secret Name, or I can list secrets."
            )


# --- Action/Result Prompts ---
@dataclass
class HcpHandleErrorPrompt(Prompt):
    role: PromptRole = PromptRole.SYSTEM
    error_message: str
    
    def __post_init__(self):
        self.content = f"An error occurred: {self.error_message}. How should I proceed? " \
                       "I can try again, or you can provide different parameters."

@dataclass
class HcpSummarizeActionResultPrompt(Prompt):
    role: PromptRole = PromptRole.SYSTEM
    action_description: str
    result_summary: str
    
    def __post_init__(self):
        self.content = f"Action '{self.action_description}' completed. Result: {self.result_summary}. What would you like to do next?"

@dataclass
class HcpAskForMissingInfoPrompt(Prompt):
    role: PromptRole = PromptRole.ASSISTANT
    missing_parameter_name: str
    tool_name: str
    
    def __post_init__(self):
        self.content = f"To use the tool '{self.tool_name}', I need the parameter: '{self.missing_parameter_name}'. Please provide it."

@dataclass
class HcpConfirmActionPrompt(Prompt):
    role: PromptRole = PromptRole.ASSISTANT
    action_description: str 
    
    def __post_init__(self):
        self.content = f"Are you sure you want to {self.action_description}? This action might be irreversible."

