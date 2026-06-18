#!/usr/bin/env python3
"""
Example 05: Real-World Microsoft AutoGen Conversational Session

This script demonstrates conversational agent communication using the Microsoft AutoGen framework
integrated with the Gemini API to collaboratively write and test code.
"""

import os
import sys

try:
    from autogen import AssistantAgent, UserProxyAgent
except ImportError:
    print("ERROR: 'pyautogen' package not found.")
    print("Please run: pip install pyautogen")
    sys.exit(1)

def main():
    # Check for API key
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: GEMINI_API_KEY environment variable is not set.")
        print("Please run: export GEMINI_API_KEY='your-key'")
        sys.exit(1)

    print("[*] Initializing AutoGen Agents with Gemini API...")

    # Configure Gemini connection for AutoGen
    llm_config = {
        "config_list": [
            {
                "model": "gemini-2.5-flash",
                "api_key": api_key,
                "api_type": "google"
            }
        ],
        "temperature": 0.2
    }

    # 1. Create the Coder Assistant Agent
    assistant = AssistantAgent(
        name="assistant",
        llm_config=llm_config,
        system_message="You are a helpful AI assistant. Write clean Python code blocks. When you receive execution results showing errors, correct the code."
    )

    # 2. Create the User Proxy Agent (representing the user & executing code)
    # Note: we disable actual code execution to prevent running arbitrary commands locally,
    # or set it to mock execution responses, or use safe Docker.
    # To keep it simple and safe for local run:
    user_proxy = UserProxyAgent(
        name="user_proxy",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=3,
        is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
        code_execution_config={
            "work_dir": "coding",
            "use_docker": False  # Use local environment for simple local runs
        }
    )

    # 3. Start the dialogue session
    task_query = "Write a python function `divide(a, b)` that divides a by b, and test it with divide(10, 0)."
    
    print(f"\n[User Query]: {task_query}")
    print("="*60)

    user_proxy.initiate_chat(
        recipient=assistant,
        message=task_query
    )

if __name__ == "__main__":
    main()
