# import httpx
from mcp.server.fastmcp import FastMCP
import sys

# Import modules - order is important
import cloud
import storage
from cloud import logger

# Initialize cloud driver before starting the server
driver = cloud.initialize_cloud_driver_from_env()
if driver is None:
    logger.error("ERROR: Failed to initialize cloud driver. Exiting.")
    sys.exit(1)
else:
    logger.info("Successfully initialized cloud driver")

# Initialize FastMCP server
mcp = FastMCP("mcp-cloud")
logger.info("Initialized MCP server: mcp-cloud")

# Register storage tools and functions
storage.register_storage(mcp)
logger.info("Registered all storage tools and functions")

# Entry point to run the server
if __name__ == "__main__":
    logger.info("Starting MCP server")
    mcp.run()
