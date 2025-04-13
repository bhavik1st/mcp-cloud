from typing import Any, List, Dict
import httpx
from mcp.server.fastmcp import FastMCP
from libcloud.storage.types import Provider, Container
from libcloud.storage.providers import get_driver
from libcloud.common.types import LibcloudError

# Environment variable names
ENV_CLOUD_PROVIDER = "CLOUD_PROVIDER"
ENV_CLOUD_KEY = "CLOUD_ACCESS_KEY"
ENV_CLOUD_SECRET = "CLOUD_SECRET_KEY"
ENV_CLOUD_REGION = "CLOUD_REGION"

SUPPORTED_PROVIDERS = {
    'aws': Provider.S3,
    'azure': Provider.AZURE_BLOBS,
    'google': Provider.GOOGLE_STORAGE,
    # 'digitalocean': Provider.DIGITALOCEAN_SPACES
}

# Initialize FastMCP server
mcp = FastMCP("mcp-cloud")
cloud_provider = None
cloud_driver = None
cloud_key = None
cloud_secret = None
cloud_region = None

# Constants
import os

# Initialize from environment variables if available
cloud_provider = os.environ.get(ENV_CLOUD_PROVIDER)
cloud_key = os.environ.get(ENV_CLOUD_KEY)
cloud_secret = os.environ.get(ENV_CLOUD_SECRET)
cloud_region = os.environ.get(ENV_CLOUD_REGION, "us-east-1")

# Auto-initialize driver if all required environment variables are present
if cloud_provider and cloud_provider in SUPPORTED_PROVIDERS and cloud_key and cloud_secret and cloud_region:
    try:
        driver_class = get_driver(SUPPORTED_PROVIDERS[cloud_provider])
        cloud_driver = driver_class(
            key=cloud_key,
            secret=cloud_secret,
            region=cloud_region
        )
        print(f"Automatically initialized cloud driver for {cloud_provider} from environment variables")
    except Exception as e:
        print(f"Failed to auto-initialize cloud driver: {str(e)}")
        cloud_driver = None


@mcp.function(name="initialize_cloud_driver")
async def initialize_cloud_driver(provider: str, credentials: Dict[str, str]) -> List[Dict[str, Any]]:
    """
    Initialize the driver for the specified cloud provider.
    """
    if provider not in SUPPORTED_PROVIDERS:
        raise ValueError(f"Unsupported provider: {provider}. Supported providers: {list(SUPPORTED_PROVIDERS.keys())}")
    
    # Get the appropriate driver class
    driver_class = get_driver(SUPPORTED_PROVIDERS[provider])
    
    # Store the driver in the global variable
    global cloud_driver
    global cloud_key
    global cloud_secret
    global cloud_region
    
    cloud_key = credentials.get('access_key')
    cloud_secret = credentials.get('secret_key')
    cloud_region = credentials.get('region', 'us-east-1')
    
    # Initialize the driver with credentials
    cloud_driver = driver_class(
        key=cloud_key,
        secret=cloud_secret,
        region=cloud_region
    )
    
    # Validate that the driver was initialized correctly
    if cloud_driver is None:
        raise ValueError("Failed to initialize cloud driver. Please check your credentials.")
    
    # Log successful initialization
    print(f"Successfully initialized cloud driver for {provider}")
    # List all containers/buckets to verify connection
    try:
        containers = cloud_driver.list_containers()
        return [{
            'name': container.name,
            'provider': provider,
            'status': 'connected'
        } for container in containers]
    except LibcloudError as e:
        raise Exception(f"Error initializing cloud driver: {str(e)}")
    except Exception as e:
        raise Exception(f"Unexpected error: {str(e)}")
    pass


@mcp.function()
async def list_buckets(provider: str = None, credentials: Dict[str, str] = None) -> List[Dict[str, Any]]:
    """
    List all buckets/containers from the specified cloud provider.
    
    Args:
        provider (str): Cloud provider name (aws, google, azure, digitalocean)
        credentials (Dict[str, str]): Provider-specific credentials
        
    Returns:
        List[Dict[str, Any]]: List of buckets with their details
    """

    try:
        if provider not in SUPPORTED_PROVIDERS:
            raise ValueError(f"Unsupported provider: {provider}. Supported providers: {list(SUPPORTED_PROVIDERS.keys())}")
        
        # Get the appropriate driver class
        driver_class = get_driver(SUPPORTED_PROVIDERS[provider])
        
        # Initialize the driver with credentials
        driver = driver_class(
            key=credentials.get('access_key'),
            secret=credentials.get('secret_key'),
            region=credentials.get('region', 'us-east-1')
        )
        
        # List all containers/buckets
        containers = driver.list_containers()
        
        # Convert containers to dictionary format
        return [{
            'name': container.name,
            'size': container.size,
            'created_at': container.created_at,
            'driver': container.driver.name
        } for container in containers]
        
    except LibcloudError as e:
        raise Exception(f"Error listing buckets: {str(e)}")
    except Exception as e:
        raise Exception(f"Unexpected error: {str(e)}")

@mcp.function()
async def get_bucket_details(provider: str, credentials: Dict[str, str], bucket_name: str) -> Dict[str, Any]:
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
        if provider not in SUPPORTED_PROVIDERS:
            raise ValueError(f"Unsupported provider: {provider}")
            
        driver_class = get_driver(SUPPORTED_PROVIDERS[provider])
        driver = driver_class(
            key=credentials.get('access_key'),
            secret=credentials.get('secret_key'),
            region=credentials.get('region', 'us-east-1')
        )
        
        container = driver.get_container(bucket_name)
        
        return {
            'name': container.name,
            'size': container.size,
            'created_at': container.created_at,
            'driver': container.driver.name,
            'objects_count': len(list(container.list_objects()))
        }
        
    except LibcloudError as e:
        raise Exception(f"Error getting bucket details: {str(e)}")
    except Exception as e:
        raise Exception(f"Unexpected error: {str(e)}")
    

@mcp.function()
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
        if provider not in SUPPORTED_PROVIDERS:
            raise ValueError(f"Unsupported provider: {provider}")
            
        driver_class = get_driver(SUPPORTED_PROVIDERS[provider])
        driver = driver_class(
            key=credentials.get('access_key'),
            secret=credentials.get('secret_key'),
            region=credentials.get('region', 'us-east-1')
        )
        
        container = driver.get_container(bucket_name)
        objects = container.list_objects()
        
        return [{
            'name': obj.name,
            'size': obj.size,
            'hash': obj.hash,
            'extra': obj.extra
        } for obj in objects]
        
    except LibcloudError as e:
        raise Exception(f"Error listing objects: {str(e)}")
    except Exception as e:
        raise Exception(f"Unexpected error: {str(e)}")

# Entry point to run the server
if __name__ == "__main__":
    mcp.run()


# def main():
#     print("Hello from mcp-cloud!")

# if __name__ == "__main__":
#     main()
