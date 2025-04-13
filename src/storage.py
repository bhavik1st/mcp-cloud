import os
from typing import Any, List, Dict
import cloud
from mcp.server.fastmcp import FastMCP
from libcloud.common.types import LibcloudError

# Reference to the MCP server instance from main.py
mcp = None

def register_storage(mcp_instance):
    """Register all storage-related tools and functions with the MCP instance"""
    global mcp
    mcp = mcp_instance
    
    # Register all tool functions
    mcp.tool(name="initialize_cloud_driver")(initialize_cloud_driver)
    mcp.tool(name="list_buckets")(list_buckets)
    mcp.tool(name="get_bucket_details")(get_bucket_details)
    mcp.tool(name="list_objects")(list_objects)
    
    return True

# Tool functions
def initialize_cloud_driver(provider: str, credentials: Dict[str, str]) -> Dict[str, Any]:
    """Initialize cloud driver with provided credentials"""
    try:
        driver = cloud.initialize_cloud_driver_internal(
            provider,
            credentials.get('access_key'),
            credentials.get('secret_key'),
            credentials.get('region', 'us-east-1')
        )
        
        if driver:
            return {
                "status": "success",
                "provider": provider,
                "message": "Cloud driver initialized successfully"
            }
        else:
            return {
                "status": "error",
                "provider": provider,
                "message": "Failed to initialize cloud driver"
            }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error: {str(e)}"
        }

async def list_buckets() -> List[Dict[str, Any]]:
    """List all buckets from the initialized cloud driver"""
    try:
        if not cloud.driver:
            return [{"error": "Cloud driver not initialized"}]
        
        containers = cloud.driver.list_containers()
        return [{
            "name": container.name,
            "provider": cloud.provider,
            "region": cloud.region
        } for container in containers]
    except Exception as e:
        return [{"error": f"Failed to list buckets: {str(e)}"}]

async def get_bucket_details(bucket_name: str) -> Dict[str, Any]:
    """Get details about a specific bucket"""
    try:
        if not cloud.driver:
            return {"error": "Cloud driver not initialized"}
            
        container = cloud.driver.get_container(bucket_name)
        return {
            "name": container.name,
            "provider": cloud.provider,
            "region": cloud.region,
            "extra": container.extra
        }
    except Exception as e:
        return {"error": f"Failed to get bucket details: {str(e)}"}    

# Async API functions
async def list_buckets_async(provider: str = None, credentials: Dict[str, str] = None) -> List[Dict[str, Any]]:
    """
    List all buckets/containers from the specified cloud provider.
    
    Args:
        provider (str): Cloud provider name (aws, google, azure, digitalocean)
        credentials (Dict[str, str]): Provider-specific credentials
        
    Returns:
        List[Dict[str, Any]]: List of buckets with their details
    """

    try:
        # List all containers/buckets
        containers = cloud.driver.list_containers()
        
        # Convert containers to dictionary format
        return [{
            'name': container.name,
            'provider': cloud.provider,
            'status': 'connected'
        } for container in containers]
        
    except LibcloudError as e:
        raise Exception(f"Error listing buckets: {str(e)}")
    except Exception as e:
        raise Exception(f"Unexpected error: {str(e)}")

async def get_bucket_details_async(provider: str, credentials: Dict[str, str], bucket_name: str) -> Dict[str, Any]:
    """
    Get detailed information about a specific bucket.
    
    Args:
        provider (str): Cloud provider name
        credentials (Dict[str, str]): Provider-specific credentials
        bucket_name (str): Name of the bucket to get details for
        
    Returns:
        Dict[str, Any]: Bucket details
    """
    try:
        container = cloud.driver.get_container(bucket_name)
        
        return {
            'name': container.name,
            'provider': cloud.provider,
            'objects_count': len(list(container.list_objects()))
        }
        
    except LibcloudError as e:
        raise Exception(f"Error getting bucket details: {str(e)}")
    except Exception as e:
        raise Exception(f"Unexpected error: {str(e)}")

async def list_objects(provider: str, credentials: Dict[str, str], bucket_name: str) -> List[Dict[str, Any]]:
    """
    List all objects in a specific bucket.
    
    Args:
        provider (str): Cloud provider name
        credentials (Dict[str, str]): Provider-specific credentials
        bucket_name (str): Name of the bucket to list objects from
        
    Returns:
        List[Dict[str, Any]]: List of objects in the bucket
    """
    try:
        container = cloud.driver.get_container(bucket_name)
        objects = container.list_objects()
        
        # Convert objects to dictionary format
        return [{
            'name': obj.name,
            'size': obj.size,
            'hash': obj.hash,
            'container': obj.container.name,
            'extra': obj.extra
        } for obj in objects]
        
    except LibcloudError as e:
        raise Exception(f"Error listing objects: {str(e)}")
    except Exception as e:
        raise Exception(f"Unexpected error: {str(e)}")
