#!/usr/bin/env python3
"""
Example 02_client: Querying the FastMCP Weather Server via stdio

This script demonstrates how a client connects to and interacts with an MCP server
over stdio using the official python-mcp client SDK.
"""

import asyncio
import os
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Define parameters to start the server process
# We use the relative path to the real FastMCP server python file
script_dir = os.path.dirname(os.path.abspath(__file__))
server_script = os.path.join(script_dir, "02_mcp_server_real.py")

server_params = StdioServerParameters(
    command="python3",
    args=[server_script],
    env=None
)

async def main():
    print("[*] Connecting to FastMCP Server...")
    
    # Establish standard input/output streams
    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            # Initialize connection handshake
            await session.initialize()
            print("[✔] Session initialized successfully.")
            
            # List available tools from server
            tools = await session.list_tools()
            print(f"[Client] Available Tools: {[t.name for t in tools.tools]}")
            
            # Execute tool call
            print("[Client] Calling tool 'get_weather' for 'San Francisco'...")
            response = await session.call_tool("get_weather", arguments={"city": "San Francisco"})
            
            print("\n" + "="*40 + "\n[Server Tool Output]:\n" + "="*40)
            print(response.content[0].text)

if __name__ == "__main__":
    asyncio.run(main())
