# Testing MCP Cloud Server

This document outlines how to test the MCP Cloud Server using unit tests, MCP Inspect, and Claude Desktop.

## Prerequisites

- Python 3.8 or higher
- Environment variables set up in `.env` file
- MCP Inspect installed (`pip install mcp-inspect`)
- Claude Desktop or Claude API access

## Running Unit Tests

To run the automated unit tests:

```bash
python src/test_mcp_server.py
```

This will:
1. Start the MCP server
2. Run tests against the API endpoints
3. Shut down the server when tests are complete

## Testing with MCP Inspect

MCP Inspect is a utility to interact with MCP servers directly.

### Starting the Server

First, start the MCP server:

```bash
python src/main.py
```

### Using MCP Inspect

Once the server is running, you can use MCP Inspect to:

1. Check server information:
```bash
mcp-inspect info --url http://localhost:7008
```

2. List available functions:
```bash
mcp-inspect functions --url http://localhost:7008
```

3. Call a specific function (example with list_buckets):
```bash
mcp-inspect call --url http://localhost:7008 --function list_buckets --args '{"provider": "aws"}'
```

## Testing with Claude Desktop

Claude Desktop can be used to test the integration with AI.

### Setup

1. Start the MCP server:
```bash
python src/main.py
```

2. Connect Claude Desktop to your MCP server:
   - Open Claude Desktop
   - Go to Settings > MCP
   - Add a new MCP connection
   - Enter URL: `http://localhost:7008`
   - Name it: `mcp-cloud`
   - Click "Connect"

### Example Prompts for Claude

Try these prompts to test the cloud storage functionality:

1. Basic check:
   ```
   Can you check what cloud providers are available on the MCP server?
   ```

2. List buckets:
   ```
   Could you list all my cloud storage buckets?
   ```

3. Get specific bucket details:
   ```
   Show me details about my bucket named [BUCKET_NAME]
   ```

## Troubleshooting

- If tests fail with connection errors, ensure the server is running on port 7008
- Check environment variables if authentication fails
- Review server logs for more detailed error information 