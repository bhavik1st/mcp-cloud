import logging
from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

def register_compute(mcp, driver, provider: str):
    """Register compute-related tools and functions with MCP server for a specific provider."""
    try:
        # Register compute tools with provider prefix
        mcp.register_tool(f"{provider}_list_instances", lambda: list_instances(driver))
        mcp.register_tool(f"{provider}_create_instance", lambda name, size, image, location=None: create_instance(driver, name, size, image, location))
        mcp.register_tool(f"{provider}_delete_instance", lambda instance_id: delete_instance(driver, instance_id))
        mcp.register_tool(f"{provider}_start_instance", lambda instance_id: start_instance(driver, instance_id))
        mcp.register_tool(f"{provider}_stop_instance", lambda instance_id: stop_instance(driver, instance_id))
        
        logger.info(f"Successfully registered compute tools for {provider}")
    except Exception as e:
        logger.error(f"Failed to register compute tools for {provider}: {str(e)}")

def list_instances(driver) -> List[Dict]:
    """List all compute instances."""
    try:
        nodes = driver.list_nodes()
        return [{"id": node.id, "name": node.name, "state": node.state} for node in nodes]
    except Exception as e:
        logger.error(f"Failed to list instances: {str(e)}")
        return []

def create_instance(driver, name: str, size: str, image: str, location: Optional[str] = None) -> Optional[Dict]:
    """Create a new compute instance."""
    try:
        if location is None:
            location = driver.list_locations()[0]
        node = driver.create_node(name=name, size=size, image=image, location=location)
        return {"id": node.id, "name": node.name, "state": node.state}
    except Exception as e:
        logger.error(f"Failed to create instance {name}: {str(e)}")
        return None

def delete_instance(driver, instance_id: str) -> bool:
    """Delete a compute instance."""
    try:
        node = driver.get_node(instance_id)
        driver.destroy_node(node)
        return True
    except Exception as e:
        logger.error(f"Failed to delete instance {instance_id}: {str(e)}")
        return False

def start_instance(driver, instance_id: str) -> bool:
    """Start a compute instance."""
    try:
        node = driver.get_node(instance_id)
        driver.start_node(node)
        return True
    except Exception as e:
        logger.error(f"Failed to start instance {instance_id}: {str(e)}")
        return False

def stop_instance(driver, instance_id: str) -> bool:
    """Stop a compute instance."""
    try:
        node = driver.get_node(instance_id)
        driver.stop_node(node)
        return True
    except Exception as e:
        logger.error(f"Failed to stop instance {instance_id}: {str(e)}")
        return False 