import datetime
import dateparser
import httpx
import logging
import asyncio
from typing import List, Dict, Optional, Any

from hcp.auth import get_access_token
#from utils.finders import find_organization_by_name

BILLING_API_VERSION = "2020-11-05"
BILLING_API_URL = f"https://api.cloud.hashicorp.com/billing/{BILLING_API_VERSION}"
hcp_logger = logging.getLogger("hcp_api")

async def request_logger(request):
    hcp_logger.info(f"Request: {request.method} {request.url}")
    hcp_logger.info(f"Request Headers: {request.headers}")

async def response_logger(response):
    hcp_logger.info(f"Response: {response.status_code} {response.url}")

async def list_statements(organization_id: str, billing_account_id: str) -> List[Dict]:
    hcp_logger.info("list_statements function") 
    token = await get_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    url = f"{BILLING_API_URL}/organizations/{organization_id}/accounts/{billing_account_id}/statements"
    
    all_statements = []
    params = {"pagination.page_size": 20}

    async with httpx.AsyncClient(event_hooks={"request": [request_logger], "response": [response_logger]}) as client:
        while True:
            response = await client.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            hcp_logger.info(f"the response json: {data}") 
            all_statements.extend(data.get("statement_overviews", []))

            pagination_data = data.get("pagination", {})
            next_page_token = pagination_data.get("next_page_token")

            if not next_page_token:
                break
            
            params["pagination.next_page_token"] = next_page_token
            # The API doesn't seem to use the previous page token, but we'll clear it just in case
            params.pop("pagination.previous_page_token", None)

    return all_statements

async def get_running_statement(organization_id: str, billing_account_id: str) -> Dict:
    token = await get_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    url = f"{BILLING_API_URL}/organizations/{organization_id}/accounts/{billing_account_id}/running-statement"
    async with httpx.AsyncClient(event_hooks={"request": [request_logger], "response": [response_logger]}) as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        hcp_logger.info(f"the response json: {response.json()}") 
        return response.json()

async def get_statement(organization_id: str, billing_account_id: str, statement_id: str) -> Dict:
    token = await get_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    url = f"{BILLING_API_URL}/organizations/{organization_id}/accounts/{billing_account_id}/statements/{statement_id}"
    async with httpx.AsyncClient(event_hooks={"request": [request_logger], "response": [response_logger]}) as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        hcp_logger.info(f"the response json: {response.json()}") 
        return response.json()

async def get_hcp_billing_summary(
    organization_id: str,
    time_range: str,
) -> Dict[str, Any]:
    """
    Retrieves a summary of billing expenses for an HCP organization over a specified time range.
    The time range can be natural language (e.g., 'last month', 'last 3 months', 'current cycle').

    Args:
        organization_id: The ID of the HCP organization.
        time_range: The desired time range for the billing summary (e.g., 'current cycle', 'last month', 'last 3 months', 'November 2025').
    """
    billing_account_id = "default-account"
    hcp_logger.info(f"Getting billing summary for org '{organization_id}' with time range '{time_range}' and hardcoded account '{billing_account_id}'")

    org_id = organization_id

    # Parse time_range
    if time_range.lower() == "current cycle":
        hcp_logger.info("Fetching running statement for current cycle.")
        running_statement = await get_running_statement(org_id, billing_account_id)
        if not running_statement:
            return {"message": f"No running statement found for billing account '{billing_account_id}' in Org '{organization_id}'."}
        
        return {
            "organization_id": organization_id,
            "billing_account_id": billing_account_id,
            "summary_type": "current_cycle",
            "period_start": running_statement["running_statement"]["billing_period_start"],
            "period_end": running_statement["running_statement"]["billing_period_end"],
            "total_cost": running_statement["running_statement"]["total"],
            "statement_details": running_statement["running_statement"]["resources"],
            "message": f"Current billing cycle for account '{billing_account_id}' in Org '{organization_id}'."
        }
    else:
        hcp_logger.info(f"Fetching historical statements for time range: {time_range}")
        parsed_date_range = dateparser.parse(time_range, settings={'RETURN_AS_TIMEZONE_AWARE': True, 'TIMEZONE': 'UTC'})
        
        if not parsed_date_range:
            return {"error": f"Could not parse time range '{time_range}'."}

        start_date, end_date = None, None
        if isinstance(parsed_date_range, tuple):
            start_date, end_date = parsed_date_range
        elif isinstance(parsed_date_range, datetime.datetime):
            start_date = parsed_date_range.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            next_month = (start_date.replace(day=1) + datetime.timedelta(days=32)).replace(day=1) - datetime.timedelta(days=1)
            end_date = next_month.replace(hour=23, minute=59, second=59, microsecond=999999)

        if not start_date or not end_date:
             return {"error": f"Could not determine a valid date range from '{time_range}'."}
        
        hcp_logger.info(f"Parsed date range: {start_date.isoformat()} to {end_date.isoformat()}")

        all_statements = await list_statements(org_id, billing_account_id)
        filtered_statements = []
        total_cost_sum = 0.0

        hcp_logger.info("look through statement(s)")
        for statement in all_statements:
            stmt_start_str = statement.get("billing_period_start")
            stmt_end_str = statement.get("billing_period_end")
            
            if not stmt_start_str or not stmt_end_str:
                continue

            stmt_start = dateparser.parse(stmt_start_str)
            stmt_end = dateparser.parse(stmt_end_str)

            if start_date <= stmt_start < end_date:
                #Grab details statement details
                statement_id = statement.get("id")
                detailed_statement = await get_statement(org_id, billing_account_id, statement_id)

                filtered_statements.append(detailed_statement)
                try:
                    total_cost_sum += float(detailed_statement.get("total", "0"))
                except (ValueError, TypeError):
                    pass
        
        if not filtered_statements:
            return {"message": f"No billing statements found for the specified time range for account '{billing_account_id}' in Org '{organization_id}'."}

        return {
            "organization_id": organization_id,
            "billing_account_id": billing_account_id,
            "summary_type": "historical",
            "requested_time_range": time_range,
            "parsed_start_date": start_date.isoformat(),
            "parsed_end_date": end_date.isoformat(),
            "number_of_statements": len(filtered_statements),
            "total_cost_sum": f"{total_cost_sum:.2f}",
            "currency":  "USD",
            "statements": filtered_statements
        }
