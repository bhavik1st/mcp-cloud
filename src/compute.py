import os
from typing import Any, List, Dict, Optional
import cloud
from mcp.server.fastmcp import FastMCP
from libcloud.compute.types import Provider, NodeState
from libcloud.compute.providers import get_driver
from libcloud.common.types import LibcloudError

# Reference to the MCP server instance from main.py
mcp = None

def register_compute(mcp_instance):
    """Register all compute-related tools and functions with the MCP instance"""
    global mcp
    mcp = mcp_instance
    
    # Register all tool functions
    mcp.tool(name="list_instances")(list_instances)
    mcp.tool(name="get_instance_details")(get_instance_details)
    mcp.tool(name="create_instance")(create_instance)
    mcp.tool(name="start_instance")(start_instance)
    mcp.tool(name="stop_instance")(stop_instance)
    mcp.tool(name="reboot_instance")(reboot_instance)
    mcp.tool(name="destroy_instance")(destroy_instance)
    mcp.tool(name="list_images")(list_images)
    mcp.tool(name="list_sizes")(list_sizes)
    mcp.tool(name="list_locations")(list_locations)
    
    return True

# Tool functions
def initialize_compute_driver(provider: str, credentials: Dict[str, str]) -> Dict[str, Any]:
    """Initialize compute driver with provided credentials"""
    try:
        # Get the appropriate driver class
        driver_class = get_driver(cloud.SUPPORTED_PROVIDERS[provider])
        
        # Initialize the driver with credentials
        driver = driver_class(
            key=credentials.get('access_key'),
            secret=credentials.get('secret_key'),
            region=credentials.get('region', 'us-east-1')
        )
        
        if driver:
            return {
                "status": "success",
                "provider": provider,
                "message": "Compute driver initialized successfully"
            }
        else:
            return {
                "status": "error",
                "provider": provider,
                "message": "Failed to initialize compute driver"
            }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error: {str(e)}"
        }

async def list_instances() -> List[Dict[str, Any]]:
    """List all compute instances from the initialized cloud driver"""
    try:
        if not cloud.driver:
            return [{"error": "Cloud driver not initialized"}]
        
        # Get the compute driver
        compute_driver = get_driver(cloud.SUPPORTED_PROVIDERS[cloud.provider])
        driver = compute_driver(
            key=cloud.key,
            secret=cloud.secret,
            region=cloud.region
        )
        
        # List all nodes (instances)
        nodes = driver.list_nodes()
        
        # Convert nodes to dictionary format
        return [{
            "id": node.id,
            "name": node.name,
            "state": node.state,
            "public_ips": node.public_ips,
            "private_ips": node.private_ips,
            "provider": cloud.provider,
            "region": cloud.region,
            "extra": node.extra
        } for node in nodes]
    except Exception as e:
        return [{"error": f"Failed to list instances: {str(e)}"}]

async def get_instance_details(instance_id: str) -> Dict[str, Any]:
    """Get details about a specific compute instance"""
    try:
        if not cloud.driver:
            return {"error": "Cloud driver not initialized"}
            
        # Get the compute driver
        compute_driver = get_driver(cloud.SUPPORTED_PROVIDERS[cloud.provider])
        driver = compute_driver(
            key=cloud.key,
            secret=cloud.secret,
            region=cloud.region
        )
        
        # Get the node (instance)
        node = driver.get_node(instance_id)
        
        return {
            "id": node.id,
            "name": node.name,
            "state": node.state,
            "public_ips": node.public_ips,
            "private_ips": node.private_ips,
            "provider": cloud.provider,
            "region": cloud.region,
            "extra": node.extra
        }
    except Exception as e:
        return {"error": f"Failed to get instance details: {str(e)}"}

async def create_instance(
    name: str,
    image_id: str,
    size_id: str,
    location_id: Optional[str] = None,
    ex_keyname: Optional[str] = None,
    ex_security_groups: Optional[List[str]] = None,
    ex_userdata: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create a new compute instance.
    
    Args:
        name (str): Name for the new instance
        image_id (str): ID of the image to use
        size_id (str): ID of the size (flavor) to use
        location_id (str, optional): ID of the location (region/zone) to create the instance in
        ex_keyname (str, optional): Name of the SSH key to use
        ex_security_groups (List[str], optional): List of security group names
        ex_userdata (str, optional): User data script to run on instance creation
        
    Returns:
        Dict[str, Any]: Details of the created instance
    """
    try:
        if not cloud.driver:
            return {"error": "Cloud driver not initialized"}
            
        # Get the compute driver
        compute_driver = get_driver(cloud.SUPPORTED_PROVIDERS[cloud.provider])
        driver = compute_driver(
            key=cloud.key,
            secret=cloud.secret,
            region=cloud.region
        )
        
        # Get the image
        image = driver.get_image(image_id)
        
        # Get the size
        size = driver.get_size(size_id)
        
        # Get the location if provided
        location = None
        if location_id:
            location = driver.get_location(location_id)
        
        # Create the node (instance)
        node = driver.create_node(
            name=name,
            image=image,
            size=size,
            location=location,
            ex_keyname=ex_keyname,
            ex_security_groups=ex_security_groups,
            ex_userdata=ex_userdata
        )
        
        return {
            "id": node.id,
            "name": node.name,
            "state": node.state,
            "public_ips": node.public_ips,
            "private_ips": node.private_ips,
            "provider": cloud.provider,
            "region": cloud.region,
            "message": "Instance created successfully"
        }
    except Exception as e:
        return {"error": f"Failed to create instance: {str(e)}"}

async def start_instance(instance_id: str) -> Dict[str, Any]:
    """Start a compute instance"""
    try:
        if not cloud.driver:
            return {"error": "Cloud driver not initialized"}
            
        # Get the compute driver
        compute_driver = get_driver(cloud.SUPPORTED_PROVIDERS[cloud.provider])
        driver = compute_driver(
            key=cloud.key,
            secret=cloud.secret,
            region=cloud.region
        )
        
        # Get the node (instance)
        node = driver.get_node(instance_id)
        
        # Start the node
        result = driver.start_node(node)
        
        if result:
            return {
                "id": node.id,
                "name": node.name,
                "state": node.state,
                "message": "Instance started successfully"
            }
        else:
            return {"error": f"Failed to start instance {instance_id}"}
    except Exception as e:
        return {"error": f"Failed to start instance: {str(e)}"}

async def stop_instance(instance_id: str) -> Dict[str, Any]:
    """Stop a compute instance"""
    try:
        if not cloud.driver:
            return {"error": "Cloud driver not initialized"}
            
        # Get the compute driver
        compute_driver = get_driver(cloud.SUPPORTED_PROVIDERS[cloud.provider])
        driver = compute_driver(
            key=cloud.key,
            secret=cloud.secret,
            region=cloud.region
        )
        
        # Get the node (instance)
        node = driver.get_node(instance_id)
        
        # Stop the node
        result = driver.stop_node(node)
        
        if result:
            return {
                "id": node.id,
                "name": node.name,
                "state": node.state,
                "message": "Instance stopped successfully"
            }
        else:
            return {"error": f"Failed to stop instance {instance_id}"}
    except Exception as e:
        return {"error": f"Failed to stop instance: {str(e)}"}

async def reboot_instance(instance_id: str) -> Dict[str, Any]:
    """Reboot a compute instance"""
    try:
        if not cloud.driver:
            return {"error": "Cloud driver not initialized"}
            
        # Get the compute driver
        compute_driver = get_driver(cloud.SUPPORTED_PROVIDERS[cloud.provider])
        driver = compute_driver(
            key=cloud.key,
            secret=cloud.secret,
            region=cloud.region
        )
        
        # Get the node (instance)
        node = driver.get_node(instance_id)
        
        # Reboot the node
        result = driver.reboot_node(node)
        
        if result:
            return {
                "id": node.id,
                "name": node.name,
                "state": node.state,
                "message": "Instance rebooted successfully"
            }
        else:
            return {"error": f"Failed to reboot instance {instance_id}"}
    except Exception as e:
        return {"error": f"Failed to reboot instance: {str(e)}"}

async def destroy_instance(instance_id: str) -> Dict[str, Any]:
    """Destroy (delete) a compute instance"""
    try:
        if not cloud.driver:
            return {"error": "Cloud driver not initialized"}
            
        # Get the compute driver
        compute_driver = get_driver(cloud.SUPPORTED_PROVIDERS[cloud.provider])
        driver = compute_driver(
            key=cloud.key,
            secret=cloud.secret,
            region=cloud.region
        )
        
        # Get the node (instance)
        node = driver.get_node(instance_id)
        
        # Destroy the node
        result = driver.destroy_node(node)
        
        if result:
            return {
                "id": node.id,
                "name": node.name,
                "message": "Instance destroyed successfully"
            }
        else:
            return {"error": f"Failed to destroy instance {instance_id}"}
    except Exception as e:
        return {"error": f"Failed to destroy instance: {str(e)}"}

async def list_images() -> List[Dict[str, Any]]:
    """List all available images"""
    try:
        if not cloud.driver:
            return [{"error": "Cloud driver not initialized"}]
            
        # Get the compute driver
        compute_driver = get_driver(cloud.SUPPORTED_PROVIDERS[cloud.provider])
        driver = compute_driver(
            key=cloud.key,
            secret=cloud.secret,
            region=cloud.region
        )
        
        # List all images
        images = driver.list_images()
        
        # Convert images to dictionary format
        return [{
            "id": image.id,
            "name": image.name,
            "provider": cloud.provider,
            "region": cloud.region,
            "extra": image.extra
        } for image in images]
    except Exception as e:
        return [{"error": f"Failed to list images: {str(e)}"}]

async def list_sizes() -> List[Dict[str, Any]]:
    """List all available sizes (flavors)"""
    try:
        if not cloud.driver:
            return [{"error": "Cloud driver not initialized"}]
            
        # Get the compute driver
        compute_driver = get_driver(cloud.SUPPORTED_PROVIDERS[cloud.provider])
        driver = compute_driver(
            key=cloud.key,
            secret=cloud.secret,
            region=cloud.region
        )
        
        # List all sizes
        sizes = driver.list_sizes()
        
        # Convert sizes to dictionary format
        return [{
            "id": size.id,
            "name": size.name,
            "ram": size.ram,
            "disk": size.disk,
            "bandwidth": size.bandwidth,
            "price": size.price,
            "provider": cloud.provider,
            "region": cloud.region,
            "extra": size.extra
        } for size in sizes]
    except Exception as e:
        return [{"error": f"Failed to list sizes: {str(e)}"}]

async def list_locations() -> List[Dict[str, Any]]:
    """List all available locations (regions/zones)"""
    try:
        if not cloud.driver:
            return [{"error": "Cloud driver not initialized"}]
            
        # Get the compute driver
        compute_driver = get_driver(cloud.SUPPORTED_PROVIDERS[cloud.provider])
        driver = compute_driver(
            key=cloud.key,
            secret=cloud.secret,
            region=cloud.region
        )
        
        # List all locations
        locations = driver.list_locations()
        
        # Convert locations to dictionary format
        return [{
            "id": location.id,
            "name": location.name,
            "country": location.country,
            "provider": cloud.provider,
            "extra": location.extra
        } for location in locations]
    except Exception as e:
        return [{"error": f"Failed to list locations: {str(e)}"}] 