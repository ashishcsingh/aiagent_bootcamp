#!/usr/bin/env python3
"""
Example 05: Simulated Microsoft AutoGen Conversational Chat

This script demonstrates conversational multi-agent communication:
1. Creating Conversational Agents (UserProxy, Assistant).
2. Implementing Message Passing (agents sending text logs to each other).
3. Simulating dynamic feedback delegation loops to debug a script.
"""

import time

# =====================================================================
# 1. Define Conversational Agent base
# =====================================================================

class ConversationalAgent:
    def __init__(self, name: str, system_message: str):
        self.name = name
        self.system_message = system_message

    def receive_message(self, sender_name: str, message: str) -> str:
        print(f"\n[{sender_name} -> {self.name}]:")
        print(f"Message: {message}")
        time.sleep(1.2)  # Simulate model thinking time
        return self.generate_response(message)

    def generate_response(self, message: str) -> str:
        # Override in child classes
        return ""

# =====================================================================
# 2. Define Assistant and UserProxy specialized classes
# =====================================================================

class AssistantAgent(ConversationalAgent):
    """Generates solutions, writes code, and resolves bugs."""
    def __init__(self, name: str, system_message: str):
        super().__init__(name, system_message)
        self.attempts = 0

    def generate_response(self, message: str) -> str:
        if "syntax error" in message.lower() or "bug" in message.lower():
            self.attempts += 1
            return (
                "Assistant Code Update:\n"
                "```python\n"
                "# Fixed the division by zero condition\n"
                "def divide(a, b):\n"
                "    return a / b if b != 0 else 0\n"
                "```"
            )
        else:
            return (
                "Assistant Code Draft:\n"
                "```python\n"
                "# Initial division logic\n"
                "def divide(a, b):\n"
                "    return a / b\n"
                "```"
            )

class UserProxyAgent(ConversationalAgent):
    """Simulates a human supervisor, executes code locally, and returns outputs."""
    def __init__(self, name: str, system_message: str):
        super().__init__(name, system_message)
        self.step = 0

    def generate_response(self, message: str) -> str:
        self.step += 1
        if self.step == 1:
            # First draft verification: proxy simulates running the draft code and catching a crash
            print(f"\n[*] [UserProxy Execution]: Running script divide(10, 0)...")
            time.sleep(0.8)
            return "Execution Error: ZeroDivisionError: division by zero found. Please correct the bug."
        else:
            # Second draft verification: runs the revised code and verifies it works
            print(f"\n[*] [UserProxy Execution]: Running script divide(10, 0)...")
            time.sleep(0.8)
            print("[UserProxy Result]: Returned 0. Success.")
            return "Execution Output: Tests passed successfully. TERMINATE"

# =====================================================================
# 3. Conversational Session Runner
# =====================================================================

def start_dialogue():
    # Instantiate agents
    coder = AssistantAgent(
        name="CoderAssistant",
        system_message="You write clean Python scripts based on task queries."
    )
    
    user_proxy = UserProxyAgent(
        name="UserProxy",
        system_message="You initiate tasks and verify Python script outputs locally."
    )

    print("[*] Initializing Conversational Session between CoderAssistant and UserProxy...")
    print("*"*60)

    # UserProxy starts the chat
    current_message = "Task: Write a python function to divide a by b."
    sender = "UserProxy"
    receiver = coder

    # Message-passing loop
    while True:
        # Sender sends message to receiver
        response = receiver.receive_message(sender, current_message)
        
        # Check for termination keyword
        if "TERMINATE" in response:
            print(f"\n" + "="*50 + "\n[Success] Conversational chat terminated cleanly.")
            break
            
        # Swap sender and receiver for next turn
        if receiver == coder:
            sender = "CoderAssistant"
            receiver = user_proxy
        else:
            sender = "UserProxy"
            receiver = coder
            
        current_message = response

if __name__ == "__main__":
    start_dialogue()
