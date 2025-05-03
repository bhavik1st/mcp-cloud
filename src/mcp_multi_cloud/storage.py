import logging
from libcloud.storage.types import Provider
from libcloud.storage.providers import get_driver
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

def register_storage(mcp, driver, provider: str):
    """Register storage-related tools and functions with MCP server for a specific provider."""
    try:
        # Register storage tools with provider prefix
        mcp.register_tool(f"{provider}_list_buckets", lambda: list_buckets(driver))
        mcp.register_tool(f"{provider}_create_bucket", lambda name: create_bucket(driver, name))
        mcp.register_tool(f"{provider}_delete_bucket", lambda name: delete_bucket(driver, name))
        mcp.register_tool(f"{provider}_upload_file", lambda bucket, file_path, obj_name=None: upload_file(driver, bucket, file_path, obj_name))
        mcp.register_tool(f"{provider}_download_file", lambda bucket, obj_name, dest_path: download_file(driver, bucket, obj_name, dest_path))
        
        logger.info(f"Successfully registered storage tools for {provider}")
    except Exception as e:
        logger.error(f"Failed to register storage tools for {provider}: {str(e)}")

def list_buckets(driver) -> List[str]:
    """List all buckets/containers."""
    try:
        containers = driver.list_containers()
        return [container.name for container in containers]
    except Exception as e:
        logger.error(f"Failed to list buckets: {str(e)}")
        return []

def create_bucket(driver, bucket_name: str) -> Optional[str]:
    """Create a new bucket/container."""
    try:
        container = driver.create_container(bucket_name)
        return container.name
    except Exception as e:
        logger.error(f"Failed to create bucket {bucket_name}: {str(e)}")
        return None

def delete_bucket(driver, bucket_name: str) -> bool:
    """Delete a bucket/container."""
    try:
        container = driver.get_container(bucket_name)
        driver.delete_container(container)
        return True
    except Exception as e:
        logger.error(f"Failed to delete bucket {bucket_name}: {str(e)}")
        return False

def upload_file(driver, bucket_name: str, file_path: str, object_name: Optional[str] = None) -> Optional[str]:
    """Upload a file to a bucket/container."""
    try:
        container = driver.get_container(bucket_name)
        if object_name is None:
            object_name = os.path.basename(file_path)
        extra = {'content_type': 'application/octet-stream'}
        obj = driver.upload_object(file_path, container, object_name, extra=extra)
        return obj.name
    except Exception as e:
        logger.error(f"Failed to upload file {file_path} to {bucket_name}: {str(e)}")
        return None

def download_file(driver, bucket_name: str, object_name: str, destination_path: str) -> Optional[str]:
    """Download a file from a bucket/container."""
    try:
        container = driver.get_container(bucket_name)
        obj = driver.get_object(container.name, object_name)
        driver.download_object(obj, destination_path, overwrite_existing=True)
        return destination_path
    except Exception as e:
        logger.error(f"Failed to download {object_name} from {bucket_name}: {str(e)}")
        return None 