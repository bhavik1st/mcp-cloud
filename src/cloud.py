import logging
import os
import sys

# Try to import libcloud, install it if not available
try:
    from libcloud.storage.types import Provider
    from libcloud.storage.providers import get_driver
    from libcloud.common.types import LibcloudError
except ImportError:
    logging.error("Apache Libcloud not found. Installing...")
    import subprocess
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "apache-libcloud==3.8.0"])
        # Now import after installation
        from libcloud.storage.types import Provider
        from libcloud.storage.providers import get_driver
        from libcloud.common.types import LibcloudError
        logging.info("Successfully installed apache-libcloud")
    except Exception as e:
        logging.error(f"Failed to install apache-libcloud: {str(e)}")
        sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Environment variable names
ENV_CLOUD_PROVIDER = "CLOUD_PROVIDER"
ENV_CLOUD_KEY = "CLOUD_ACCESS_KEY"
ENV_CLOUD_SECRET = "CLOUD_SECRET_KEY"
ENV_CLOUD_REGION = "CLOUD_REGION"
DEFAULT_CLOUD_REGION = "us-east-1"

DEFAULT_CLOUD_PROVIDER = "aws"

SUPPORTED_PROVIDERS = {
    'aws': Provider.S3,
    'azure': Provider.AZURE_BLOBS,
    'google': Provider.GOOGLE_STORAGE,
}

# Global variables for cloud configuration
provider = None
driver = None
key = None
secret = None
region = None
driver_class = None
# mcp = None

# Initialize from environment variables if available
provider = os.environ.get(ENV_CLOUD_PROVIDER, "aws")
key = os.environ.get(ENV_CLOUD_KEY)
secret = os.environ.get(ENV_CLOUD_SECRET)
region = os.environ.get(ENV_CLOUD_REGION, "us-east-1")

def initialize_cloud_driver_internal(in_provider, in_key, in_secret, in_region):
    """Internal function to initialize cloud driver with given credentials"""
    global driver
    global driver_class
    
    try:
        if in_provider not in SUPPORTED_PROVIDERS:
            logger.error(f"Unsupported provider: {in_provider}")
            return None
            
        driver_class = get_driver(SUPPORTED_PROVIDERS[in_provider])
        driver = driver_class(
            key=in_key,
            secret=in_secret,
            region=in_region
        )
        logger.info(f"Successfully initialized cloud driver for {in_provider}")
        return driver
    except LibcloudError as e:
        logger.error(f"LibCloud Error: Failed to initialize cloud driver: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Exception: Failed to initialize cloud driver: {str(e)}")
        return None

def initialize_cloud_driver_from_env(in_provider=None, in_key=None, in_secret=None, in_region=None):
    """Initialize cloud driver from environment variables"""
    global driver
    global provider
    global key
    global secret
    global region
    global driver_class

    # Check if any parameters are None, use environment variables as fallback
    if in_provider is None:
        provider = os.environ.get(ENV_CLOUD_PROVIDER, DEFAULT_CLOUD_PROVIDER)
        logger.info(f"Using provider from environment/default: {provider}")
    else:
        provider = in_provider
        logger.info(f"Using provided provider: {provider}")
        
    if in_key is None:
        key = os.environ.get(ENV_CLOUD_KEY)
        logger.debug("Using access key from environment")
    else:
        key = in_key
        logger.debug("Using provided access key")
        
    if in_secret is None:
        secret = os.environ.get(ENV_CLOUD_SECRET)
        logger.debug("Using secret key from environment")
    else:
        secret = in_secret
        logger.debug("Using provided secret key")
        
    if in_region is None:
        region = os.environ.get(ENV_CLOUD_REGION, DEFAULT_CLOUD_REGION)
        logger.info(f"Using region from environment/default: {region}")
    else:
        region = in_region
        logger.info(f"Using provided region: {region}")

    if provider not in SUPPORTED_PROVIDERS:
        logger.error(f"Exiting: Unsupported provider: {provider}")
        sys.exit(1) 
        return None 
    
    if key is None or secret is None:
            logger.error("Exiting: Missing required credentials (access key or secret key)")
            sys.exit(1)
            return None
    
    logger.info(f"Attempting to initialize cloud driver for {provider} in {region}")
    if provider and key and secret and region:
        driver = initialize_cloud_driver_internal(provider, key, secret, region)
        logger.info(f"Successfully initialized cloud driver for {provider}")
        return driver
    else:
        logger.error("Error: Missing 1 or more required parameters (provider, access key, secret key, region)")
        driver = None
        sys.exit(1) 
        return None         

    return driver
    pass



