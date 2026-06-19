# Lesson 2: Single-Agent Design & Tool Integration

In this module, we will explore the design of a single-agent system and learn how to integrate external tools into an agent's execution loop using standard Python code.

## 1. Defining Tools

To make tools discoverable by an LLM, we must declare them using a structured schema (typically a JSON Schema) that specifies:
- The function **name**
- A detailed **description** of what it does
- The **parameters** it accepts (with types and descriptions)

For example, a calculator tool function and its corresponding schema:

```python
# The actual Python implementation
def calculate(expression: str) -> str:
    try:
        # Secure evaluation (in production, use a safe sandboxed engine)
        return str(eval(expression, {"__builtins__": None}, {}))
    except Exception as e:
        return f"Error: {str(e)}"

# The schema exposed to the LLM
tool_schema = {
    "name": "calculate",
    "description": "Evaluate mathematical expressions. Input must be a valid Python expression (e.g. '2 + 2' or '15 * 3.14').",
    "parameters": {
        "type": "object",
        "properties": {
            "expression": {
                "type": "string",
                "description": "The math expression to evaluate."
            }
        },
        "required": ["expression"]
    }
}
```

---

## 2. The Agent Loop Lifecycle

An autonomous single-agent loop runs sequentially through these phases:

```mermaid
graph TD
    Start([Start]) --> Prompt[Prompt Construction]
    Prompt --> Inference[LLM Inference]
    Inference --> Decision{Is Tool Call Requested?}
    
    Decision -->|Yes| Execute[Execute Tool]
    Execute --> Observe[Observation]
    Observe --> Prompt
    
    Decision -->|No| Respond[Return Final Answer]
    Respond --> End([End])
```

1.  **System Prompting:** Injecting instructions telling the model it has access to tools and must output a specific format (e.g., JSON or special block tags like `Thought:` and `Action:`).
2.  **Inference:** The LLM generates text.
3.  **Parsing:** The wrapper extracts the tool name and arguments.
4.  **Execution:** The system runs the function locally and gets the output.
5.  **Feedback:** The system appends the observation to the context history and invokes the LLM again.

---

## 3. Handling Errors & Failures

In real-world environments, things go wrong. Agents must be resilient to:
*   **JSON Parsing Failures:** When the LLM generates malformed JSON tool calls. The wrapper should catch this error and feed the parser error back to the model, asking it to correct its output.
*   **Infinite Loops:** When the agent repeatedly calls the same tool with the same inputs. We prevent this by setting a strict limit on the number of iterations (e.g., `max_iterations = 5`).
*   **Tool Execution Errors:** If the API or tool throws an exception, we pass the exception description back to the agent as an observation so it can attempt to correct its parameters.

In the code examples folder, you can run `examples/01_react_loop.py` to see a full implementation of this architecture in action.

---

## 4. Hands-on Playground

Run and inspect the ReAct agent design pattern script directly in your browser:

<div class="my-6 p-5 glass-panel rounded-2xl border-blue-500/20 bg-blue-950/10 flex flex-col sm:flex-row justify-between items-center gap-4">
    <div class="flex items-center gap-3">
        <span class="text-2xl">⚡</span>
        <div>
            <h4 class="text-sm font-bold text-white uppercase tracking-wider font-mono">ReAct Loop Interactive Sandbox</h4>
            <p class="text-xs text-slate-400 mt-0.5">Explore how the agent parses prompts, invokes search, and executes iterations.</p>
        </div>
    </div>
    <button onclick="runLiveCode('01_react_loop.py', 'ReAct (Reason + Action) Loop')" class="text-center py-2 px-4 rounded-xl bg-blue-600 hover:bg-blue-500 text-white text-xs font-bold shadow-lg shadow-blue-500/20 transition-all cursor-pointer whitespace-nowrap">
        Access Sandbox
    </button>
</div>

### 💻 Production Implementation Guide

To run a production-ready ReAct loop locally using the official `google-genai` SDK, configure your system and run the code below. Unlike the simplified browser sandbox simulation, this uses the real Gemini API client and official SDK models.

#### Prerequisites
```bash
pip install google-genai
export GEMINI_API_KEY="your-api-key"
```

```python
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
```

