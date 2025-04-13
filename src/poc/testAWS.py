from pprint import pprint
import libcloud
from libcloud.storage.types import Provider
from libcloud.storage.providers import get_driver
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

print(f"Cloud provider: {cloud_provider}")
print(f"Cloud access key: {cloud_key}")
print(f"Cloud secret key: {cloud_secret}")
print(f"Cloud region: {cloud_region}")

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
else:
    print("Failed to initialize cloud driver: Missing required environment variables")

# Test listing buckets
if cloud_driver:
    try:
        buckets = cloud_driver.list_containers()
        print("\nList of buckets:")
        pprint([b.name for b in buckets])
        pprint([{
            'name': b.name,
            'provider': cloud_provider,
            'status': 'connected'
        } for b in buckets])
    except Exception as e:
        print(f"Failed to list buckets: {str(e)}")