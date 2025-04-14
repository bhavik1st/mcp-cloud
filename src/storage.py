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
    mcp.tool(name="list_buckets")(list_buckets)
    mcp.tool(name="get_bucket_details")(get_bucket_details)
    mcp.tool(name="list_objects")(list_objects)
    mcp.tool(name="list_all_objects")(list_all_objects)
    mcp.tool(name="get_object")(get_object)
    mcp.tool(name="download_object")(download_object)
    mcp.tool(name="upload_object")(upload_object)
    #mcp.tool(name="delete_object")(delete_object)
    
    # Register resource endpoints
    mcp.resource("/storage/objects/{bucket_name}/{object_name}")(get_object_resource)
    mcp.resource("/storage/download/{bucket_name}/{object_name}")(download_object_resource)
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

async def list_objects(bucket_name: str) -> List[Dict[str, Any]]:
    """
    List all objects in a specific bucket.
    
    Args:
        bucket_name (str): Name of the bucket to list objects from
        
    Returns:
        List[Dict[str, Any]]: List of objects in the bucket
    """
    try:
        if not cloud.driver:
            return [{"error": "Cloud driver not initialized"}]
            
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
        return [{"error": f"Error listing objects: {str(e)}"}]
    except Exception as e:
        return [{"error": f"Unexpected error: {str(e)}"}]

async def list_all_objects(bucket_name: str, prefix: str = None, delimiter: str = None) -> List[Dict[str, Any]]:
    """
    List all objects in a bucket, including those in folders.
    
    Args:
        bucket_name (str): Name of the bucket to list objects from
        prefix (str, optional): Filter results to objects whose names begin with this prefix
        delimiter (str, optional): Group common prefixes into a single result
        
    Returns:
        List[Dict[str, Any]]: List of objects and common prefixes in the bucket
    """
    try:
        if not cloud.driver:
            return [{"error": "Cloud driver not initialized"}]
            
        container = cloud.driver.get_container(bucket_name)
        
        # Get objects with optional prefix and delimiter
        objects = container.list_objects(prefix=prefix, delimiter=delimiter)
        
        # Process results
        result = []
        
        # Add objects
        for obj in objects:
            result.append({
                'name': obj.name,
                'size': obj.size,
                'hash': obj.hash,
                'container': obj.container.name,
                'extra': obj.extra,
                'type': 'object'
            })
            
        # Add common prefixes (folders)
        if hasattr(objects, 'prefixes') and objects.prefixes:
            for prefix in objects.prefixes:
                result.append({
                    'name': prefix,
                    'type': 'folder',
                    'container': bucket_name
                })
                
        return result
        
    except LibcloudError as e:
        return [{"error": f"Error listing all objects: {str(e)}"}]
    except Exception as e:
        return [{"error": f"Unexpected error: {str(e)}"}]

async def get_object(bucket_name: str, object_name: str) -> Dict[str, Any]:
    """
    Get details about a specific object in a bucket.
    
    Args:
        bucket_name (str): Name of the bucket containing the object
        object_name (str): Name of the object to retrieve
        
    Returns:
        Dict[str, Any]: Object details
    """
    try:
        if not cloud.driver:
            return {"error": "Cloud driver not initialized"}
            
        container = cloud.driver.get_container(bucket_name)
        obj = container.get_object(object_name)
        
        return {
            'name': obj.name,
            'size': obj.size,
            'hash': obj.hash,
            'container': obj.container.name,
            'extra': obj.extra,
            'driver': cloud.provider
        }
        
    except LibcloudError as e:
        return {"error": f"Error getting object: {str(e)}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

async def download_object(bucket_name: str, object_name: str, destination_path: str) -> Dict[str, Any]:
    """
    Download an object from a bucket to a local file.
    
    Args:
        bucket_name (str): Name of the bucket containing the object
        object_name (str): Name of the object to download
        destination_path (str): Local path where the object should be saved
        
    Returns:
        Dict[str, Any]: Download result
    """
    try:
        if not cloud.driver:
            return {"error": "Cloud driver not initialized"}
            
        # Ensure the destination directory exists
        os.makedirs(os.path.dirname(os.path.abspath(destination_path)), exist_ok=True)
            
        container = cloud.driver.get_container(bucket_name)
        obj = container.get_object(object_name)
        
        # Download the object
        result = container.download_object(obj, destination_path, overwrite_existing=True)
        
        if result:
            return {
                'status': 'success',
                'message': f'Object {object_name} downloaded successfully',
                'destination': destination_path,
                'size': obj.size,
                'object_name': object_name,
                'bucket_name': bucket_name
            }
        else:
            return {"error": f"Failed to download object {object_name}"} 
        
    except LibcloudError as e:
        return {"error": f"Error downloading object: {str(e)}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

async def upload_object(bucket_name: str, object_name: str, file_path: str) -> Dict[str, Any]:
    """
    Upload a local file to a bucket as an object.
    
    Args:
        bucket_name (str): Name of the bucket to upload to
        object_name (str): Name to give the uploaded object
        file_path (str): Local path of the file to upload
        
    Returns:
        Dict[str, Any]: Upload result
    """
    try:
        if not cloud.driver:
            return {"error": "Cloud driver not initialized"}
            
        # Check if file exists
        if not os.path.exists(file_path):
            return {"error": f"File not found: {file_path}"}
            
        container = cloud.driver.get_container(bucket_name)
        
        # Upload the file
        with open(file_path, 'rb') as file_obj:
            obj = container.upload_object_via_stream(iterator=file_obj, object_name=object_name)
        
        return {
            'status': 'success',
            'message': f'Object {object_name} uploaded successfully',
            'name': obj.name,
            'size': obj.size,
            'hash': obj.hash,
            'container': obj.container.name
        }
        
    except LibcloudError as e:
        return {"error": f"Error uploading object: {str(e)}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

async def delete_object(bucket_name: str, object_name: str) -> Dict[str, Any]:
    """
    Delete an object from a bucket.
    
    Args:
        bucket_name (str): Name of the bucket containing the object
        object_name (str): Name of the object to delete
        
    Returns:
        Dict[str, Any]: Deletion result
    """
    try:
        if not cloud.driver:
            return {"error": "Cloud driver not initialized"}
            
        container = cloud.driver.get_container(bucket_name)
        obj = container.get_object(object_name)
        
        # Delete the object
        result = container.delete_object(obj)
        
        if result:
            return {
                'status': 'success',
                'message': f'Object {object_name} deleted successfully',
                'object_name': object_name,
                'bucket_name': bucket_name
            }
        else:
            return {"error": f"Failed to delete object {object_name}"}
        
    except LibcloudError as e:
        return {"error": f"Error deleting object: {str(e)}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

# Resource endpoints
async def get_object_resource(bucket_name: str, object_name: str) -> Dict[str, Any]:
    """Resource endpoint to get object details"""
    return await get_object(bucket_name, object_name)

async def download_object_resource(bucket_name: str, object_name: str) -> Dict[str, Any]:
    """Resource endpoint to download an object"""
    # Use a default download path since we can't access request parameters
    destination_path = f'./downloads/{object_name}'
    
    return await download_object(bucket_name, object_name, destination_path)
