import requests
from app.mcp.config import MCP_SERVER_URL

class MCPClient:
    def call(self, tool, args):
        r = requests.post(f"{MCP_SERVER_URL}/call", json={
            "tool": tool,
            "args": args
        })
        return r.json()

mcp_client = MCPClient()
