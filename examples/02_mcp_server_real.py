#!/usr/bin/env python3
"""
Example 02: Real-World Model Context Protocol (MCP) Server

This script demonstrates how to build a standard MCP server using the official FastMCP SDK.
It exposes a real tool and resource that can be integrated with MCP clients (like Claude Desktop or Cursor).
"""

import os
import sys

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    print("ERROR: 'mcp' package not found.")
    print("Please run: pip install mcp")
    sys.exit(1)

# Initialize FastMCP Server
mcp = FastMCP("Bootcamp Weather Service")

# 1. Define a tool that returns weather information
@mcp.tool()
def get_weather(city: str) -> str:
    """Retrieves the current weather report for a given city.
    
    Args:
        city: The name of the city.
    """
    city_lower = city.lower()
    if "london" in city_lower:
        return "Rainy, 14°C"
    elif "san francisco" in city_lower:
        return "Foggy, 16°C"
    else:
        return "Sunny, 22°C"

# 2. Define a resource (static content)
@mcp.resource("weather://alerts")
def get_weather_alerts() -> str:
    """Returns currently active weather alerts."""
    return "ALERT: High wind advisory active for the Pacific Northwest."

if __name__ == "__main__":
    print("[*] Starting FastMCP Server on stdio...")
    mcp.run()
