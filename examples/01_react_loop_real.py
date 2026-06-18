#!/usr/bin/env python3
"""
Example 01 (Real): ReAct Loop using the Gemini API

This script demonstrates how to write a real ReAct (Reason + Action) loop 
from scratch using the Google GenAI SDK.
"""

import os
import sys
import re
from google import genai
from google.genai import types

# Define our calculation tool
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

def main():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: GEMINI_API_KEY environment variable is not set.")
        print("Please run: export GEMINI_API_KEY='your-key'")
        sys.exit(1)

    print("[*] Initializing Gemini Client...")
    client = genai.Client(api_key=api_key)

    user_query = "What is 15 * 8 plus 42?"
    
    # We instruct the model to follow a ReAct format:
    # Thought: ...
    # Action: tool_name
    # Action Input: parameter
    # Observation: ... (provided by developer execution)
    # Final Answer: ...
    
    system_instruction = """
    You are an autonomous AI Agent. Solve the query using the ReAct loop.
    You only have access to this tool:
    - name: calculate
      description: Evaluates math expressions. Input must be a valid Python expression (e.g. '2 + 2' or '(10 * 3) / 5').
    
    Follow these exact formatting rules for your thoughts and actions:
    Thought: your reasoning about what to do next.
    Action: calculate
    Action Input: the math expression to solve.
    
    When you have calculated the final answer, reply with:
    Final Answer: the final value.
    """

    history = [
        types.Content(role="user", parts=[types.Part.from_text(text=user_query)])
    ]
    
    print(f"[*] Starting Real ReAct Agent...")
    print(f"[*] Goal: {user_query}\n" + "="*50)
    
    max_steps = 5
    for i in range(max_steps):
        print(f"\n--- Iteration {i+1} ---")
        
        # We query the model with the system instruction and context
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=history,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.1
            )
        )
        
        response_text = response.text.strip()
        print(f"[Agent Response]:\n{response_text}")
        
        # Append agent response to context
        history.append(types.Content(role="model", parts=[types.Part.from_text(text=response_text)]))
        
        # Parse output
        action_match = re.search(r"Action:\s*(\w+)", response_text)
        action_input_match = re.search(r"Action Input:\s*(.+)", response_text)
        final_answer_match = re.search(r"Final Answer:\s*(.+)", response_text)
        
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
            # Feed observation back as user input
            history.append(types.Content(role="user", parts=[types.Part.from_text(text=f"Observation: {observation}")]))
        else:
            print("\n[Error]: Parser could not read intermediate steps or action input.")
            break
    else:
        print("\n[Error]: Reached maximum iterations without achieving goal.")

if __name__ == "__main__":
    main()
