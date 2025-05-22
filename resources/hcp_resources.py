# resources/hcp_resources.py
from dataclasses import dataclass, field, asdict
from typing import Optional, Dict, Any, List

# Imports from the official MCP SDK
from mcp.common import Resource # Base class for resources

# Removed convert_to_dict as mcp.common.Resource is a dataclass,
# and asdict can be used if a dict representation is needed externally.
# Internally, the SDK should handle Resource objects.

@dataclass
class HcpOrganizationResource(Resource): # Inherits from mcp.common.Resource
    # MCP Resource requires 'id' and 'type'
    # 'data' field will hold all other specific attributes.
    id: str # HCP Organization ID
    type: str = field(default="hcp_organization", init=False) # MCP type
    data: Dict[str, Any] = field(default_factory=dict)

    # Convenience properties to access common fields from data
    @property
    def name(self) -> str: return self.data.get("name", "Unknown Organization")
    @property
    def created_at(self) -> str: return self.data.get("created_at", "")
    @property
    def state(self) -> str: return self.data.get("state", "UNKNOWN")

    @classmethod
    def from_api_response(cls, api_data: Dict[str, Any]) -> "HcpOrganizationResource":
        org_id = api_data.get("id", "")
        # Store all relevant API data in the 'data' field
        resource_data = {
            "name": api_data.get("name", "Unknown Organization"),
            "created_at": api_data.get("created_at", ""),
            "state": api_data.get("state", {}).get("state", "UNKNOWN") if isinstance(api_data.get("state"), dict) else api_data.get("state", "UNKNOWN"),
            "raw_api_response": api_data # Store the full response if needed
        }
        return cls(id=org_id, data=resource_data)

    # to_dict is not strictly needed if the SDK handles Resource objects,
    # but can be useful for other purposes.
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class HcpProjectResource(Resource):
    id: str # HCP Project ID
    type: str = field(default="hcp_project", init=False)
    data: Dict[str, Any] = field(default_factory=dict)

    @property
    def name(self) -> str: return self.data.get("name", "Unknown Project")
    @property
    def organization_id(self) -> str: return self.data.get("organization_id", "")
    @property
    def created_at(self) -> str: return self.data.get("created_at", "")
    @property
    def state(self) -> str: return self.data.get("state", "UNKNOWN")
    @property
    def description(self) -> Optional[str]: return self.data.get("description")


    @classmethod
    def from_api_response(cls, api_data: Dict[str, Any]) -> "HcpProjectResource":
        project_id = api_data.get("id", "")
        parent = api_data.get("parent", {})
        resource_data = {
            "name": api_data.get("name", "Unknown Project"),
            "organization_id": parent.get("id", "") if parent.get("type") == "ORGANIZATION" else "",
            "created_at": api_data.get("created_at", ""),
            "state": api_data.get("state", {}).get("state", "UNKNOWN") if isinstance(api_data.get("state"), dict) else api_data.get("state", "UNKNOWN"),
            "description": api_data.get("description"),
            "raw_api_response": api_data
        }
        return cls(id=project_id, data=resource_data)
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class HcpIamPolicyResource(Resource):
    id: str # Composite ID like "iam_policy_for_organizations_org-id"
    type: str = field(default="hcp_iam_policy", init=False)
    data: Dict[str, Any] = field(default_factory=dict)

    @property
    def bindings(self) -> List[Dict[str, Any]]: return self.data.get("bindings", [])
    @property
    def etag(self) -> str: return self.data.get("etag", "")
    @property
    def resource_path(self) -> str: return self.data.get("resource_path", "")


    @classmethod
    def from_api_response(cls, api_data: Dict[str, Any], resource_path: str) -> "HcpIamPolicyResource":
        # resource_path is like "organizations/org-id" or "projects/project-id"
        mcp_id = f"iam_policy_for_{resource_path.replace('/', '_')}"
        resource_data = {
            "bindings": api_data.get("bindings", []),
            "etag": api_data.get("etag", ""),
            "resource_path": resource_path, # Store the original path for context
            "raw_api_response": api_data
        }
        return cls(id=mcp_id, data=resource_data)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class HcpServicePrincipalResource(Resource):
    id: str # HCP SP ID
    type: str = field(default="hcp_service_principal", init=False)
    data: Dict[str, Any] = field(default_factory=dict)

    @property
    def name(self) -> str: return self.data.get("name", "Unknown SP")
    @property
    def resource_name(self) -> str: return self.data.get("resource_name", "") # HCP's full resource name
    @property
    def organization_id(self) -> Optional[str]: return self.data.get("organization_id")
    @property
    def project_id(self) -> Optional[str]: return self.data.get("project_id")
    @property
    def created_at(self) -> str: return self.data.get("created_at", "")

    @classmethod
    def from_api_response(cls, api_data: Dict[str, Any]) -> "HcpServicePrincipalResource":
        sp_id = api_data.get("id") or api_data.get("principal_id") or api_data.get("resource_id", "")
        resource_data = {
            "name": api_data.get("name", "Unknown Service Principal"),
            "resource_name": api_data.get("resource_name", ""),
            "organization_id": api_data.get("organization_id"),
            "project_id": api_data.get("project_id"),
            "created_at": api_data.get("created_at", ""),
            "raw_api_response": api_data
        }
        return cls(id=sp_id, data=resource_data)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class HcpServicePrincipalKeyResource(Resource):
    id: str # client_id of the key
    type: str = field(default="hcp_service_principal_key", init=False)
    data: Dict[str, Any] = field(default_factory=dict)

    @property
    def resource_name(self) -> str: return self.data.get("resource_name", "")
    @property
    def service_principal_id(self) -> str: return self.data.get("service_principal_id", "")
    @property
    def parent_scope_id(self) -> str: return self.data.get("parent_scope_id", "")
    @property
    def created_at(self) -> str: return self.data.get("created_at", "")
    @property
    def state(self) -> str: return self.data.get("state", "UNKNOWN")
    @property
    def client_secret(self) -> Optional[str]: return self.data.get("client_secret") # Sensitive

    @classmethod
    def from_api_response(cls, api_data: Dict[str, Any], sp_id: str, parent_scope: str, secret: Optional[str] = None) -> "HcpServicePrincipalKeyResource":
        key_id = api_data.get("client_id", "")
        resource_data = {
            "resource_name": api_data.get("resource_name", ""),
            "service_principal_id": sp_id,
            "parent_scope_id": parent_scope,
            "created_at": api_data.get("created_at", ""),
            "state": api_data.get("state", {}).get("state", "UNKNOWN") if isinstance(api_data.get("state"), dict) else api_data.get("state", "UNKNOWN"),
            "client_secret": secret, # Store if provided, be mindful of exposure
            "raw_api_response": api_data
        }
        return cls(id=key_id, data=resource_data)

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        # Potentially redact client_secret if this dict is broadly used
        # if "client_secret" in d["data"] and d["data"]["client_secret"] is not None:
        #     d["data"]["client_secret"] = "[REDACTED]"
        return d

@dataclass
class HcpGroupResource(Resource):
    id: str # resource_id of the group
    type: str = field(default="hcp_group", init=False)
    data: Dict[str, Any] = field(default_factory=dict)

    @property
    def resource_name(self) -> str: return self.data.get("resource_name", "")
    @property
    def display_name(self) -> str: return self.data.get("display_name", "Unknown Group")
    @property
    def description(self) -> Optional[str]: return self.data.get("description")
    @property
    def organization_id(self) -> Optional[str]: return self.data.get("organization_id")
    @property
    def created_at(self) -> str: return self.data.get("created_at", "")
    @property
    def updated_at(self) -> str: return self.data.get("updated_at", "")
    @property
    def member_count(self) -> Optional[int]: return self.data.get("member_count")

    @classmethod
    def from_api_response(cls, api_data: Dict[str, Any]) -> "HcpGroupResource":
        group_id = api_data.get("resource_id", "")
        org_id_from_rn = ""
        rn = api_data.get("resource_name","")
        if rn.startswith("iam/organization/"):
            parts = rn.split('/')
            if len(parts) > 2:
                org_id_from_rn = parts[2]
        
        resource_data = {
            "resource_name": rn,
            "display_name": api_data.get("display_name", "Unknown Group"),
            "description": api_data.get("description"),
            "organization_id": org_id_from_rn,
            "created_at": api_data.get("created_at", ""),
            "updated_at": api_data.get("updated_at", ""),
            "member_count": api_data.get("member_count"),
            "raw_api_response": api_data
        }
        return cls(id=group_id, data=resource_data)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class HcpVaultAppResource(Resource):
    id: str # resource_id of the app
    type: str = field(default="hcp_vault_app", init=False)
    data: Dict[str, Any] = field(default_factory=dict)

    @property
    def name(self) -> str: return self.data.get("name", "Unknown Vault App")
    @property
    def organization_id(self) -> str: return self.data.get("organization_id", "")
    @property
    def project_id(self) -> str: return self.data.get("project_id", "")
    @property
    def resource_name(self) -> str: return self.data.get("resource_name", "")
    @property
    def description(self) -> Optional[str]: return self.data.get("description")
    @property
    def created_at(self) -> str: return self.data.get("created_at", "")

    @classmethod
    def from_api_response(cls, api_data: Dict[str, Any]) -> "HcpVaultAppResource":
        app_id = api_data.get("resource_id", "")
        resource_data = {
            "name": api_data.get("name", "Unknown Vault App"),
            "organization_id": api_data.get("organization_id", ""),
            "project_id": api_data.get("project_id", ""),
            "resource_name": api_data.get("resource_name", ""),
            "description": api_data.get("description"),
            "created_at": api_data.get("created_at", ""),
            "raw_api_response": api_data
        }
        return cls(id=app_id, data=resource_data)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class HcpVaultKvSecretResource(Resource):
    id: str # Composite ID: app_name + secret_name
    type: str = field(default="hcp_vault_kv_secret", init=False)
    data: Dict[str, Any] = field(default_factory=dict)

    @property
    def name(self) -> str: return self.data.get("name", "Unknown Secret") # Secret's own name
    @property
    def app_name(self) -> str: return self.data.get("app_name", "")
    @property
    def project_id(self) -> str: return self.data.get("project_id", "")
    @property
    def organization_id(self) -> str: return self.data.get("organization_id", "")
    @property
    def version(self) -> Optional[int]: return self.data.get("version")
    @property
    def value(self) -> Optional[str]: return self.data.get("value") # Sensitive
    @property
    def created_at(self) -> Optional[str]: return self.data.get("created_at")

    @classmethod
    def from_api_response_metadata(cls, api_data: Dict[str, Any], app_name: str, project_id: str, org_id: str) -> "HcpVaultKvSecretResource":
        secret_name = api_data.get("name", "Unknown Secret")
        mcp_id = f"{app_name}_{secret_name}"
        resource_data = {
            "name": secret_name,
            "app_name": app_name,
            "project_id": project_id,
            "organization_id": org_id,
            "version": api_data.get("latest_version") or api_data.get("version"),
            "created_at": api_data.get("created_at"),
            "raw_api_response": api_data
        }
        return cls(id=mcp_id, data=resource_data)

    @classmethod
    def from_api_response_open(cls, api_data: Dict[str, Any], app_name: str, project_id: str, org_id: str) -> "HcpVaultKvSecretResource":
        secret_name = api_data.get("name", "Unknown Secret")
        mcp_id = f"{app_name}_{secret_name}"
        
        secret_version_data = api_data.get("static_version") or api_data.get("rotating_version") or {}
        value = None
        if api_data.get("type") == "STATIC" and api_data.get("static_version"):
            value = api_data["static_version"].get("value")
        elif api_data.get("type") == "ROTATING" and api_data.get("rotating_version"):
            value = str(api_data.get("rotating_version", {}).get("values", {}))


        resource_data = {
            "name": secret_name,
            "app_name": app_name,
            "project_id": project_id,
            "organization_id": org_id,
            "version": secret_version_data.get("version"),
            "value": value,
            "created_at": secret_version_data.get("created_at"),
            "raw_api_response": api_data
        }
        return cls(id=mcp_id, data=resource_data)

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        # Potentially redact value if this dict is broadly used
        # if "value" in d["data"] and d["data"]["value"] is not None:
        #    d["data"]["value"] = "[REDACTED]"
        return d
