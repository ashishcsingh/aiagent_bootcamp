#!/usr/bin/env python3
"""
Example 01: ReAct (Reason + Action) Loop Implementation

This script demonstrates a simple, self-contained ReAct loop from scratch.
It simulates how an AI agent uses tools by analyzing user input, planning,
calling a math tool, observing the result, and formulating a final response.
"""

import json
import re

# =====================================================================
# 1. Tool Definition & Mock Database
# =====================================================================

def calculate(expression: str) -> str:
    """Evaluate mathematical expressions securely."""
    try:
        # Strip unsafe characters
        clean_expression = re.sub(r'[^0-9+\-*/().\s]', '', expression)
        # Evaluate safely
        result = eval(clean_expression, {"__builtins__": None}, {})
        return str(result)
    except Exception as e:
        return f"Error evaluating expression: {str(e)}"

# Register tools in a lookup dictionary
TOOLS = {
    "calculate": calculate
}

# Define the tool description schema exposed to the model
TOOLS_SCHEMA = [
    {
        "name": "calculate",
        "description": "Evaluates math expressions. Input must be a valid Python expression (e.g. '2 + 2' or '(10 * 3) / 5').",
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {"type": "string"}
            },
            "required": ["expression"]
        }
    }
]

# =====================================================================
# 2. Mock LLM Response Engine
# =====================================================================

class MockLLM:
    """
    Simulates an LLM that understands the ReAct prompt.
    For demonstration, we hardcode responses based on the question.
    """
    def __init__(self):
        self.step = 0

    def generate_response(self, prompt: str) -> str:
        # Determine the user query from the prompt history
        if "What is 15 * 8 plus 42?" in prompt:
            if self.step == 0:
                self.step += 1
                # The model thinks and decides to call the calculate tool for the first part
                return (
                    "Thought: The user wants to calculate 15 * 8 + 42. I should calculate 15 * 8 first.\n"
                    "Action: calculate\n"
                    "Action Input: 15 * 8"
                )
            elif self.step == 1:
                self.step += 1
                # The model sees the observation of the first calculation (120) and plans next steps
                return (
                    "Thought: The result of 15 * 8 is 120. Now I need to add 42 to this result.\n"
                    "Action: calculate\n"
                    "Action Input: 120 + 42"
                )
            elif self.step == 2:
                # The model sees the final calculation (162) and formulates the final answer
                return (
                    "Thought: The result is 162. I have completed all calculations and can now reply to the user.\n"
                    "Final Answer: The calculation (15 * 8) + 42 equals 162."
                )
        return "Thought: I don't know how to process this.\nFinal Answer: I'm sorry, I cannot answer that."

# =====================================================================
# 3. Core ReAct Execution Loop
# =====================================================================

def run_agent(user_query: str):
    llm = MockLLM()
    max_steps = 5
    
    # Construct initial context
    history = (
        f"System: You are an autonomous AI Agent. Solve the query using the ReAct loop.\n"
        f"Available Tools: {json.dumps(TOOLS_SCHEMA, indent=2)}\n\n"
        f"User: {user_query}\n"
    )
    
    print(f"[*] Starting ReAct Agent...")
    print(f"[*] Goal: {user_query}\n" + "="*50)
    
    for i in range(max_steps):
        print(f"\n--- Iteration {i+1} ---")
        
        # Get LLM decision
        response = llm.generate_response(history)
        print(f"[Agent Response]:\n{response}")
        
        # Append response to history
        history += f"\nAgent:\n{response}"
        
        # Parse output for Action and Action Input
        action_match = re.search(r"Action:\s*(\w+)", response)
        action_input_match = re.search(r"Action Input:\s*(.+)", response)
        final_answer_match = re.search(r"Final Answer:\s*(.+)", response)
        
        if final_answer_match:
            print("\n" + "="*50 + f"\n[Success] Goal Achieved!\nResult: {final_answer_match.group(1)}")
            break
            
        if action_match and action_input_match:
            tool_name = action_match.group(1).strip()
            tool_input = action_input_match.group(1).strip()
            
            print(f"\n[Tool Execution]: Invoking '{tool_name}' with parameter '{tool_input}'...")
            
            if tool_name in TOOLS:
                observation = TOOLS[tool_name](tool_input)
            else:
                observation = f"Error: Tool '{tool_name}' not found."
                
            print(f"[Observation]: {observation}")
            history += f"\nObservation: {observation}"
        else:
            print("\n[Error]: Parser could not read intermediate steps or action input.")
            break
    else:
        print("\n[Error]: Reached maximum iterations without achieving goal.")

if __name__ == "__main__":
    run_agent("What is 15 * 8 plus 42?")
