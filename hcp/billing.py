import datetime
import httpx
import logging
import asyncio
from typing import List, Dict, Optional, Any

from hcp.auth import get_access_token

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

def _is_current_month(start_date_str: str, end_date_str: str) -> bool:
    try:
        start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d").date()
        end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d").date()
        today = datetime.date.today()
        return start_date.year == today.year and start_date.month == today.month and end_date.year == today.year and end_date.month == today.month
    except ValueError:
        return False

async def get_hcp_billing_summary(
    organization_id: str,
    start_date: str,
    end_date: str,
) -> Dict[str, Any]:
    """
    Retrieves a summary of billing expenses for an HCP organization over a specified date range.

    Args:
        organization_id: The ID of the HCP organization.
        start_date: The start date of the billing period in YYYY-MM-DD format.
        end_date: The end date of the billing period in YYYY-MM-DD format.
    """
    billing_account_id = "default-account"
    hcp_logger.info(f"Getting billing summary for org '{organization_id}' from {start_date} to {end_date} for account '{billing_account_id}'")

    if _is_current_month(start_date, end_date):
        hcp_logger.info("Fetching running statement for the current cycle.")
        running_statement = await get_running_statement(organization_id, billing_account_id)
        if not running_statement or "running_statement" not in running_statement:
            return {"message": f"No running statement found for billing account '{billing_account_id}' in Org '{organization_id}'."}
        
        stmt = running_statement["running_statement"]
        return {
            "organization_id": organization_id,
            "billing_account_id": billing_account_id,
            "summary_type": "current_cycle",
            "period_start": stmt.get("billing_period_start"),
            "period_end": stmt.get("billing_period_end"),
            "total_cost": stmt.get("total"),
            "statement_details": stmt.get("resources"),
            "message": f"Current billing cycle for account '{billing_account_id}' in Org '{organization_id}'."
        }
    else:
        hcp_logger.info(f"Fetching historical statements from {start_date} to {end_date}")
        
        try:
            start_date_obj = datetime.datetime.strptime(start_date, "%Y-%m-%d").replace(tzinfo=datetime.timezone.utc)
            end_date_obj = datetime.datetime.strptime(end_date, "%Y-%m-%d").replace(tzinfo=datetime.timezone.utc)
        except ValueError:
            return {"error": f"Invalid date format. Please use YYYY-MM-DD."}

        all_statements = await list_statements(organization_id, billing_account_id)
        filtered_statements = []
        total_cost_sum = 0.0

        for statement in all_statements:
            stmt_start_str = statement.get("billing_period_start")
            stmt_end_str = statement.get("billing_period_end")

            if not stmt_start_str or not stmt_end_str:
                continue
            
            stmt_start = datetime.datetime.fromisoformat(stmt_start_str.replace('Z', '+00:00'))
            
            if start_date_obj <= stmt_start < end_date_obj:
                statement_id = statement.get("id")
                detailed_statement = await get_statement(organization_id, billing_account_id, statement_id)
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
            "requested_start_date": start_date,
            "requested_end_date": end_date,
            "number_of_statements": len(filtered_statements),
            "total_cost_sum": f"{total_cost_sum:.2f}",
            "currency": "USD",
            "statements": filtered_statements
        }
