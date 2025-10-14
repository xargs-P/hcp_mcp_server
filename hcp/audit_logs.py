
from datetime import datetime, timezone
import dateparser
import httpx
import logging
from hcp.auth import get_access_token
from typing import List, Optional

LOGS_API_VERSION = "2022-06-06"
LOGS_API_URL = f"https://api.cloud.hashicorp.com/logs/{LOGS_API_VERSION}"
hcp_logger = logging.getLogger("hcp_api")

async def request_logger(request):
    hcp_logger.info(f"Request: {request.method} {request.url}")
    hcp_logger.info(f"Request Headers: {request.headers}")
    #body = await request.aread()
    #hcp_logger.info(f"Request Body: {body.decode()}")

async def response_logger(response):
    hcp_logger.info(f"INSIDE Response: {LOGS_API_VERSION}")
    hcp_logger.info(f"Response: {response.status_code} {response.url}")
    #hcp_logger.info(f"Response Headers: {response.headers}")
    #body = await response.aread()
    #hcp_logger.info(f"Response Body: {body.decode()}")
    #response.stream = httpx.ByteStream(body)

async def search_logs(
    organization_id: str,
    start_time: str,
    end_time: str,
    query: Optional[str] = None,
    project_id: Optional[str] = None,
    topic: Optional[str] = None,
):
    """
    Searches for logs in the organization.
    """
    token = await get_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    hcp_logger.info(f"headers  {headers}")
    hcp_logger.info(f"query: {query}, topic {topic}, project_id {project_id}")

    if not query and not topic and not project_id:
        topic = "hashicorp.platform.audit"

    selectors = []
    if topic:
        selectors.append(f'topic="{topic}"')
    if project_id:
        selectors.append(f'project_id="{project_id}"')

    hcp_logger.info(f"determine selectors string")

    selector_string = ""
    if selectors:
        selector_string = "{" + ",".join(selectors) + "}"

    final_query = f"{selector_string} {query or ''}".strip()

    if not final_query:
        raise ValueError("A query, project_id, or topic must be provided to search logs.")

    hcp_logger.info(f"Format time for query")
    try:
        start_dt = dateparser.parse(start_time)
        end_dt = dateparser.parse(end_time)
        if start_dt is None or end_dt is None:
            raise ValueError(f"Could not parse time string: start='{start_time}', end='{end_time}'")
    except Exception as e:
        raise ValueError(f"Could not parse time string: {e}")

    start_rfc3339 = start_dt.astimezone(timezone.utc).isoformat().replace('+00:00', 'Z')
    end_rfc3339 = end_dt.astimezone(timezone.utc).isoformat().replace('+00:00', 'Z')

    payload = {
        "organization_id": organization_id,
        "query": final_query,
        "start": start_rfc3339,
        "end": end_rfc3339,
    }

    hcp_logger.info(f"search_logs payload for {organization_id}: {payload}")
    async with httpx.AsyncClient(
          timeout=15,
          event_hooks={
                      "request": [request_logger],
                      "response": [response_logger]
          }
        ) as client:
        response = await client.post(
            f"{LOGS_API_URL}/organizations/{organization_id}/entries/preview/search",
            headers=headers,
            json=payload,
        )
    try:
        hcp_logger.info(f"search_logs response status code: {response.status_code}")
    except Exception as e:
        hcp_logger.error(f"error getting response status code: {str(e)}")

    #hcp_logger.info(f"search_logs response content: {response.text}")
    #response.raise_for_status()
    logs = response.json()
    return logs
