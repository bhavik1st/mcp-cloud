# mcp-cloud
[![PyPI version](https://badge.fury.io/py/mcp-cloud.svg)](https://badge.fury.io/py/mcp-cloud)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Model Context Protocol Server for Public Cloud environments like AWS, Azure, and more.
mcp-cloud is a Python MCP server:
- Connects to public cloud to access resources like S3 Buckets, Azure Blobs
- Provides tools performing certain operations like CRUD on resources.

## Overview

mcp-cloud is a Python server implementation of the Model Context Protocol (MCP) designed specifically for public cloud environments. It enables AI models to seamlessly connect with various cloud resources and services.

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
        "<path_to_mcp_cloud>e/mcp-cloud/src",
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


