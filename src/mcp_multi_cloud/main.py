# import httpx
from mcp.server.fastmcp import FastMCP
import sys
from typing import Dict

# Import modules - order is important
from mcp_multi_cloud import cloud
from mcp_multi_cloud import storage
from mcp_multi_cloud import compute
from mcp_multi_cloud.cloud import logger

# Initialize cloud drivers
drivers = cloud.get_all_drivers()
if not drivers:
    logger.error("ERROR: No cloud providers configured. Please set up at least one cloud provider's credentials.")
    sys.exit(1)
else:
    logger.info(f"Successfully initialized drivers for providers: {list(drivers.keys())}")

# Initialize FastMCP server
mcp = FastMCP("mcp_multi_cloud")
logger.info("Initialized MCP server: mcp_multi_cloud")

# Register storage tools and functions for each provider
for provider, driver in drivers.items():
    storage.register_storage(mcp, driver, provider)
    logger.info(f"Registered storage tools for {provider}")

# Register compute tools and functions for each provider
for provider, driver in drivers.items():
    compute.register_compute(mcp, driver, provider)
    logger.info(f"Registered compute tools for {provider}")

# Entry point to run the server
if __name__ == "__main__":
    logger.info("Starting MCP server")
    try:
        mcp.run()
    except Exception as e:
        logger.error(f"Error running MCP server: {str(e)}")
        sys.exit(1) 