import logging
import os
from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
from typing import Dict, Optional, List

logger = logging.getLogger(__name__)

# Global driver instances
_drivers: Dict[str, object] = {}

def get_available_providers() -> List[str]:
    """Get list of available cloud providers based on environment variables."""
    providers = []
    if os.getenv('AWS_ACCESS_KEY_ID') and os.getenv('AWS_SECRET_ACCESS_KEY'):
        providers.append('aws')
    if os.getenv('AZURE_SUBSCRIPTION_ID') and os.getenv('AZURE_KEY_FILE'):
        providers.append('azure')
    if os.getenv('GCE_EMAIL') and os.getenv('GCE_KEY_FILE') and os.getenv('GCE_PROJECT'):
        providers.append('gcp')
    return providers

def get_driver_for_provider(provider: str) -> Optional[object]:
    """Get or initialize driver for a specific provider."""
    global _drivers
    
    if provider not in _drivers:
        if provider == 'aws':
            _drivers[provider] = initialize_aws_driver()
        elif provider == 'azure':
            _drivers[provider] = initialize_azure_driver()
        elif provider == 'gcp':
            _drivers[provider] = initialize_gcp_driver()
        else:
            logger.error(f"Unsupported cloud provider: {provider}")
            return None
            
    return _drivers[provider]

def get_all_drivers() -> Dict[str, object]:
    """Get or initialize drivers for all available providers."""
    providers = get_available_providers()
    for provider in providers:
        get_driver_for_provider(provider)
    return _drivers

def initialize_aws_driver():
    """Initialize AWS driver."""
    try:
        cls = get_driver(Provider.EC2)
        driver = cls(
            os.getenv('AWS_ACCESS_KEY_ID'),
            os.getenv('AWS_SECRET_ACCESS_KEY'),
            region=os.getenv('AWS_REGION', 'us-east-1')
        )
        logger.info("Successfully initialized AWS driver")
        return driver
    except Exception as e:
        logger.error(f"Failed to initialize AWS driver: {str(e)}")
        return None

def initialize_azure_driver():
    """Initialize Azure driver."""
    try:
        cls = get_driver(Provider.AZURE)
        driver = cls(
            subscription_id=os.getenv('AZURE_SUBSCRIPTION_ID'),
            key_file=os.getenv('AZURE_KEY_FILE')
        )
        logger.info("Successfully initialized Azure driver")
        return driver
    except Exception as e:
        logger.error(f"Failed to initialize Azure driver: {str(e)}")
        return None

def initialize_gcp_driver():
    """Initialize GCP driver."""
    try:
        cls = get_driver(Provider.GCE)
        driver = cls(
            os.getenv('GCE_EMAIL'),
            os.getenv('GCE_KEY_FILE'),
            project=os.getenv('GCE_PROJECT'),
            datacenter=os.getenv('GCE_DATACENTER', 'us-central1-a')
        )
        logger.info("Successfully initialized GCP driver")
        return driver
    except Exception as e:
        logger.error(f"Failed to initialize GCP driver: {str(e)}")
        return None

def reset_drivers():
    """Reset all driver instances. Useful for testing or when credentials change."""
    global _drivers
    _drivers = {}
    logger.info("Reset all cloud drivers") 