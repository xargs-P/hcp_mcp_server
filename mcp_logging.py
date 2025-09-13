import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logging():
    """
    Sets up logging to a file.
    """
    log_file = os.environ.get("MCP_LOG_FILE", "mcp_server.log")
    logger = logging.getLogger("mcp_server")
    logger.setLevel(logging.INFO)

    # Create a rotating file handler
    handler = RotatingFileHandler(log_file, maxBytes=1024 * 1024, backupCount=5)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(handler)

    return logger
