#!/usr/bin/env python3
"""
Example 02: Minimal Model Context Protocol (MCP) Server

This script demonstrates a raw stdio-based MCP server.
It processes incoming JSON-RPC 2.0 messages from stdin and outputs responses to stdout,
adhering to the core mechanics of Anthropic's Model Context Protocol.
"""

import sys
import json

def log_debug(message: str):
    """Write log messages to stderr so they don't corrupt JSON-RPC stdout communication."""
    sys.stderr.write(f"[DEBUG] {message}\n")
    sys.stderr.flush()

# =====================================================================
# 1. Define Exposed Tools
# =====================================================================

def tool_get_weather(city: str) -> dict:
    """Mock weather tool."""
    city_lower = city.lower()
    if "london" in city_lower:
        return {"weather": "Rainy, 14°C"}
    elif "san francisco" in city_lower:
        return {"weather": "Foggy, 16°C"}
    else:
        return {"weather": "Sunny, 22°C"}

TOOL_LIST = [
    {
        "name": "get_weather",
        "description": "Retrieves the current weather report for a given city.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "The city name."}
            },
            "required": ["city"]
        }
    }
]

# =====================================================================
# 2. JSON-RPC Protocol Dispatcher
# =====================================================================

def handle_request(req: dict) -> dict:
    req_id = req.get("id")
    method = req.get("method")
    params = req.get("params", {})

    log_debug(f"Received request: method='{method}', id={req_id}")

    # Standard MCP capability listing
    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {"tools": TOOL_LIST}
        }

    # Tool invocation
    elif method == "tools/call":
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        
        log_debug(f"Invoking tool: name='{tool_name}' arguments={arguments}")
        
        if tool_name == "get_weather":
            city = arguments.get("city", "London")
            result = tool_get_weather(city)
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [
                        {"type": "text", "text": f"Weather in {city}: {result['weather']}"}
                    ]
                }
            }
        else:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32601, "message": f"Tool '{tool_name}' not found."}
            }

    # Fallback for unsupported methods
    return {
        "jsonrpc": "2.0",
        "id": req_id,
        "error": {"code": -32601, "message": f"Method '{method}' not found."}
    }

# =====================================================================
# 3. Main Loop
# =====================================================================

def main():
    log_debug("MCP Server started. Waiting for stdio messages...")
    
    # Read line-by-line from stdin
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            request = json.loads(line)
            response = handle_request(request)
            
            # Write JSON-RPC response to stdout
            sys.stdout.write(json.dumps(response) + "\n")
            sys.stdout.flush()
        except json.JSONDecodeError:
            err_resp = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32700, "message": "Parse error: invalid JSON input."}
            }
            sys.stdout.write(json.dumps(err_resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            log_debug(f"Unhandled error: {str(e)}")

if __name__ == "__main__":
    main()
