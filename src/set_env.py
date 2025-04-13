import os
from dotenv import load_dotenv

def create_env_file():
    # Default values
    env_vars = {
        'CLOUD_PROVIDER': '',
        'CLOUD_ACCESS_KEY': '',
        'CLOUD_SECRET_KEY': '',
        'CLOUD_REGION': 'us-east-1'
    }
    
    # Get user input for each variable
    print("\n=== Cloud Storage Environment Setup ===")
    print("Supported providers: aws, azure, google")
    
    env_vars['CLOUD_PROVIDER'] = input("\nEnter cloud provider (aws/azure/google): ").strip().lower()
    env_vars['CLOUD_ACCESS_KEY'] = input("Enter access key: ").strip()
    env_vars['CLOUD_SECRET_KEY'] = input("Enter secret key: ").strip()
    env_vars['CLOUD_REGION'] = input("Enter region (default: us-east-1): ").strip() or 'us-east-1'
    
    # Write to .env file
    with open('.env', 'w') as f:
        for key, value in env_vars.items():
            f.write(f"{key}={value}\n")
    
    print("\nEnvironment variables have been saved to .env file")
    
    # Load the environment variables
    load_dotenv()
    
    # Verify the variables were set
    print("\nVerifying environment variables:")
    for key in env_vars:
        value = os.getenv(key)
        masked_value = '********' if key in ['CLOUD_ACCESS_KEY', 'CLOUD_SECRET_KEY'] else value
        print(f"{key}: {masked_value}")

if __name__ == "__main__":
    create_env_file() 