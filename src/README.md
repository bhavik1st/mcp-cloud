# mcp-cloud
[![PyPI version](https://badge.fury.io/py/mcp_multi_cloud.svg)](https://badge.fury.io/py/mcp_multi_cloud)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Model Context Protocol Server for Public Cloud environments like AWS, Azure, and more.
mcp-cloud is a Python MCP server that:
- Connects to public cloud services to access resources like S3 Buckets and Azure Blobs
- Provides tools for performing CRUD operations on cloud resources
- Enables AI models to interact with cloud infrastructure securely

## Installation

You can install mcp-cloud using pip:

```bash
pip install mcp-cloud
```

Or install from source:

```bash
git clone https://github.com/yourusername/mcp_multi_cloud.git
cd mcp-cloud
pip install -e .
```

## Quick Start

1. Set up your environment variables (see Configuration section below)
2. Start the MCP server:
   ```bash
   python -m mcp_cloud.main
   ```
   or using uv:
   ```bash
   uv run --with mcp mcp run main.py
   ```

3. The server will start on `http://localhost:7008` by default

## Configuration

### Environment Variables

Create a `.env` file in your project root with your cloud credentials:

```env
CLOUD_PROVIDER=aws  # or azure, google
CLOUD_ACCESS_KEY=your_access_key
CLOUD_SECRET_KEY=your_secret_key
CLOUD_REGION=us-east-1  # or your preferred region
```

You can use the provided setup script to configure your environment:

```bash
python set_env.py
```

### Loading Environment Variables

#### Unix/Linux/MacOS
```bash
source .env
```

#### Windows
PowerShell:
```powershell
Get-Content .env | ForEach-Object {
    if ($_ -match '^([^=]+)=(.*)$') {
        $name = $matches[1]
        $value = $matches[2]
        Set-Item -Path "Env:$name" -Value $value
    }
}
```

## Usage

### Basic Usage

1. Start the MCP server:
   ```bash
   python -m mcp_cloud.main
   ```

2. Verify the server is running:
   ```bash
   mcp inspect info --url http://localhost:7008
   ```

### Integration with Claude Desktop

Add the following configuration to your Claude Desktop settings:

```json
{
  "mcpServers": {
    "mcp-cloud": {
      "command": "path/to/uv",
      "args": [
        "--directory",
        "path/to/mcp_multi_cloud/src",
        "run",
        "--with",
        "mcp",
        "mcp",
        "run",
        "main.py"
      ],
      "env": {
        "CLOUD_PROVIDER": "aws",
        "CLOUD_ACCESS_KEY": "your_access_key",
        "CLOUD_SECRET_KEY": "your_secret_key",
        "CLOUD_REGION": "us-east-1"
      }
    }
  }
}
```

### Available Features

#### Cloud Storage Operations
- List buckets/containers
- Create/delete buckets/containers
- Upload files
- Download files
- List files in a bucket/container
- Delete files

#### Coming Soon
- Cloud Compute operations
- Additional cloud providers
- Enhanced security features

## Testing

### Running Tests

1. Unit Tests:
   ```bash
   python -m unittest test_mcp_server.py
   ```

2. Integration Tests:
   ```bash
   # Terminal 1: Start the server
   python -m mcp_cloud.main

   # Terminal 2: Run integration tests
   mcp inspect test --url http://localhost:7008
   ```

For detailed testing instructions, see [TESTING.md](TESTING.md).

## Security Considerations

1. Never commit your `.env` file or expose your cloud credentials
2. Use IAM roles and minimal permissions when possible
3. Regularly rotate your access keys
4. Monitor your cloud resources for unexpected usage

## Troubleshooting

### Common Issues

1. Connection refused:
   - Ensure the server is running
   - Check if the port 7008 is available
   - Verify firewall settings

2. Authentication failures:
   - Verify your cloud credentials are correct
   - Ensure environment variables are properly set
   - Check if your access keys are active

3. Permission denied:
   - Verify IAM roles and permissions
   - Check resource-specific access policies

### Getting Help

- File an issue on GitHub
- Check the [documentation](https://your-docs-url.com)
- Join our [community Discord](https://your-discord-url.com)

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

# mcp-cloud
Model Context Protocol Server for Public Cloud
mcp-cloud is designed to run a MCP Server for Public Cloud like AWS, Azure etc.

# Mode Context Protocol

MCP Protocol for GenAI agents has been created by Anthropic.
MCP is an open protocol that standardizes how applications provide context to LLMs. 
Think of MCP like a USB-C port for AI applications. MCP provides a standardized way to connect AI models to different data sources and tools.
Refer Anthopic's [MCP Protocol Introduction](https://modelcontextprotocol.io/introduction).
Refer to the [MCP Quickstart Guide for Users](https://modelcontextprotocol.io/quickstart/user) to learn how to use MCP

# Concepts
MCP servers can provide three main types of capabilities:
Resources: File-like data that can be read by clients (like API responses or file contents)
Tools: Functions that can be called by the LLM (with user approval)
Prompts: Pre-written templates that help users accomplish specific tasks

Initial version of MCP Server will focus on resources available of Public Clouds e.g S3 Buckets, Azure for now.

MCP Primitives
The MCP protocol defines three core primitives that servers can implement:

Primitive	Control	Description	Example Use
Prompts	User-controlled	Interactive templates invoked by user choice	Slash commands, menu options
Resources	Application-controlled	Contextual data managed by the client application	File contents, API responses
Tools	Model-controlled	Functions exposed to the LLM to take actions	API calls, data updates

Running MCP Server

```bash
python src/main.py
```
or
```bash
uv run --with mcp mcp run main.py
```

Using mcp commands  & mcp inspector
```bash
mcp install main.py 
mcp dev main.py
```

# Features
0.1 
[x] Cloud Storage
[ ] Cloud Compute
    .. Coming Soon ..

# Steps to Install 
TODO: Update

# Steps to Use
TODO:   

## Environment Setup

To set up your cloud storage credentials, you can use the provided environment setup script:

```bash
python src/set_env.py
```

This will:
1. Prompt you for your cloud provider credentials
2. Create a `.env` file with your settings
3. Verify that the environment variables are set correctly

The script will ask for:
- Cloud Provider (aws/azure/google)
- Access Key
- Secret Key
- Region (defaults to us-east-1)

Alternatively, you can manually create a `.env` file with the following variables:
```
CLOUD_PROVIDER=your_provider
CLOUD_ACCESS_KEY=your_access_key
CLOUD_SECRET_KEY=your_secret_key
CLOUD_REGION=your_region
```

## Loading Environment Variables in System

### Unix/Linux/MacOS
Using `source` command:
```bash
source .env
```

Or using `export` command:
```bash
export $(cat .env | xargs)
```

### Windows
Command Prompt:
```cmd
for /f "tokens=*" %a in (.env) do set %a
```

PowerShell:
```powershell
Get-Content .env | ForEach-Object {
    if ($_ -match '^([^=]+)=(.*)$') {
        $name = $matches[1]
        $value = $matches[2]
        Set-Item -Path "Env:$name" -Value $value
    }
}
```

### Verifying Environment Variables
- Unix/Linux/MacOS: `printenv | grep CLOUD_`
- Windows: `set | findstr CLOUD_`

### Important Notes
1. The .env file should be in your project root directory
2. Each variable should be on a new line
3. No spaces around the = sign
4. No quotes around values unless they're part of the value

Example .env file format:
```
CLOUD_PROVIDER=aws
CLOUD_ACCESS_KEY=your_access_key
CLOUD_SECRET_KEY=your_secret_key
CLOUD_REGION=us-east-1
```

## Testing

The MCP Cloud Server includes comprehensive testing options to ensure everything is working correctly.

### Quick Start Testing

```bash
# Run unit tests
python src/test_mcp_server.py

# Test with MCP Inspect
python src/main.py  # In one terminal
mcp-inspect info --url http://localhost:7008  # In another terminal
```

For detailed testing instructions, including how to test with Claude Desktop, see [TESTING.md](TESTING.md).

# Testing with Claude Desktop


```json
{
  "mcpServers": {
    "mcp-cloud": {
      "command": "<path to uv>/uv", 
      "args": [
        "--directory",
        "<path_to_mcp_cloud>e/mcp_multi_cloud/src",
        "run",
        "--with",
        "mcp",
        "mcp",
        "run",
        "main.py"
      ],
      "env": {
        "CLOUD_PROVIDER": "aws",
        "CLOUD_ACCESS_KEY": "*******",
        "CLOUD_SECRET_KEY": "*******",
        "CLOUD_REGION": "us-east-1"
      }
    }
  }
}
```


