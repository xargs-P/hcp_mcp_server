# utils.py
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

def extract_id_from_resource_name(resource_name: str) -> Optional[str]:
    """
    Extracts the last segment (usually the ID) from an HCP resource name.
    Example: "iam/organization/org-uuid/service-principal/sp-uuid" -> "sp-uuid"
    Example: "organization/org-uuid" -> "org-uuid"
    """
    if not resource_name:
        return None
    return resource_name.split('/')[-1]

def format_iam_policy_for_api(bindings_json_str: str, etag: str) -> Optional[Dict[str, Any]]:
    """
    Formats the IAM policy from a JSON string of bindings and an etag
    into the structure expected by the HCP API.
    """
    import json
    try:
        bindings = json.loads(bindings_json_str)
        if not isinstance(bindings, list):
            logger.error("Policy bindings must be a list.")
            return None
        # Basic validation of binding structure (can be more comprehensive)
        for binding in bindings:
            if not isinstance(binding, dict) or "role_id" not in binding or "members" not in binding:
                logger.error(f"Invalid binding structure: {binding}")
                return None
            if not isinstance(binding["members"], list):
                 logger.error(f"Members in binding must be a list: {binding}")
                 return None
            for member in binding["members"]:
                 if not isinstance(member, dict) or "member_type" not in member or "member_id" not in member:
                    logger.error(f"Invalid member structure: {member}")
                    return None
        return {"bindings": bindings, "etag": etag}
    except json.JSONDecodeError:
        logger.error("Invalid JSON format for policy bindings.")
        return None
    except Exception as e:
        logger.error(f"Error processing policy bindings: {e}")
        return None

