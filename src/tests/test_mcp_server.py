import os
import unittest
import json
import httpx
import time
import subprocess
import signal
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class MCPServerTest(unittest.TestCase):
    """Test cases for MCP Cloud Server"""
    
    @classmethod
    def setUpClass(cls):
        """Start the MCP server before running tests"""
        print("Starting MCP server for testing...")
        # Start server in background
        cls.server_process = subprocess.Popen(
            ["python", "src/main.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        # Give server time to start
        time.sleep(2)
        cls.mcp_url = "http://localhost:7008"
    
    @classmethod
    def tearDownClass(cls):
        """Stop the MCP server after tests"""
        print("Stopping MCP server...")
        cls.server_process.send_signal(signal.SIGTERM)
        cls.server_process.wait()
    
    def test_server_health(self):
        """Test that server is running and responding"""
        response = httpx.get(f"{self.mcp_url}/health")
        self.assertEqual(response.status_code, 200)
    
    def test_mcp_info(self):
        """Test server info endpoint"""
        response = httpx.get(f"{self.mcp_url}/mcp/info")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data.get("name"), "mcp-cloud")
    
    def test_functions_list(self):
        """Test that we can list available functions"""
        response = httpx.get(f"{self.mcp_url}/mcp/functions")
        self.assertEqual(response.status_code, 200)
        functions = response.json()
        # Check that at least one function is available
        self.assertGreater(len(functions), 0)
        
if __name__ == "__main__":
    unittest.main() 