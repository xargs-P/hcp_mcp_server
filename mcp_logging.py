import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logging():
    """
    Sets up logging to a file.
    """
    log_file = os.environ.get("MCP_LOG_FILE", "mcp_client_calls.log")
    logger = logging.getLogger("mcp_server")
    logger.setLevel(logging.INFO)

    # Create a rotating file handler
    handler = RotatingFileHandler(log_file, maxBytes=1024 * 1024, backupCount=5)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(handler)

    # HCP API response logging
    if os.environ.get("HCP_API_LOGGING_ENABLED", "false").lower() == "true":
        hcp_log_file = os.environ.get("HCP_API_LOG_FILE", "hcp_api_responses.log")
        hcp_logger = logging.getLogger("hcp_api")
        hcp_logger.setLevel(logging.INFO)
        hcp_handler = RotatingFileHandler(hcp_log_file, maxBytes=1024 * 1024, backupCount=5)
        hcp_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        hcp_handler.setFormatter(hcp_formatter)
        hcp_logger.addHandler(hcp_handler)

    return logger
