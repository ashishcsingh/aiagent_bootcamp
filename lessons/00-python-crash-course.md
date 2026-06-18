# Lesson 0: Python Crash Course for AI Agents

Welcome to the **Python Crash Course for AI Agents**. This introductory guide covers the core Python programming paradigms that form the building blocks of modern agent architectures. 

Whether you are using raw Python or integrating with frameworks like CrewAI, LangGraph, and AutoGen, mastering these four core areas will ensure your agent runs smoothly, safely, and asynchronously.

---

## 1. Type Hinting & Structured Schemas

Modern LLM models communicate using structured data (JSON). To enforce correct parameter schema layouts when agents trigger tool execution calls, we use strict Python **type hints**.

### Type Annotations and `typing`
Standard type hints allow frameworks to automatically build JSON Schemas from your Python functions.

```python
from typing import List, Dict, Optional, Union

# Define a function with clear argument types and a return type hint
def calculate_agent_cost(
    prompt_tokens: int, 
    completion_tokens: int, 
    model_name: str,
    stop_sequences: Optional[List[str]] = None
) -> Dict[str, Union[float, str]]:
    
    # Cost per 1K tokens simulation
    rate = 0.015 if "gpt-4" in model_name else 0.002
    cost = ((prompt_tokens + completion_tokens) / 1000) * rate
    
    return {
        "cost": cost,
        "currency": "USD",
        "model_used": model_name
    }
```

---

## 2. Dictionary & JSON Operations

Agents consistently inspect, parse, and rebuild nested JSON structures received from model outputs or API responses.

### Safe Retrieval and List Comprehensions
Always retrieve properties using safe getters (`.get()`) to prevent `KeyError` crashes in continuous agent loops:

```python
# Raw JSON-like nested response dictionary
agent_response = {
    "choices": [
        {
            "message": {
                "role": "assistant",
                "content": "Thought: I need to query weather.",
                "tool_calls": [
                    {"name": "get_weather", "arguments": '{"location": "San Francisco"}'}
                ]
            }
        }
    ]
}

# 1. Safe extraction with default fallbacks
choices = agent_response.get("choices", [])
first_choice = choices[0] if choices else {}
message = first_choice.get("message", {})
tool_calls = message.get("tool_calls", [])

# 2. Extract tool names using list comprehensions
active_tools = [tool.get("name") for tool in tool_calls if "name" in tool]
print(f"Active tools to call: {active_tools}")
```

---

## 3. Asynchronous Programming (`asyncio`)

AI Agents spend a significant amount of time waiting for network responses (LLM completions, database transactions, web page reads). Using **asynchronous programming** allows agents to execute multiple calls concurrently without freezing execution.

```python
import asyncio
import time

async def fetch_llm_completion(agent_name: str, prompt: str) -> str:
    print(f"[*] [{agent_name}] Sending prompt to model...")
    # Simulate non-blocking network I/O wait
    await asyncio.sleep(2.0) 
    print(f"[✔] [{agent_name}] Completion received.")
    return f"Response to '{prompt}'"

async def main():
    start_time = time.time()
    
    # Execute multiple agent calls concurrently
    tasks = [
        fetch_llm_completion("Researcher", "Find top tech news"),
        fetch_llm_completion("Writer", "Draft introduction summary"),
        fetch_llm_completion("Critic", "Evaluate structural accuracy")
    ]
    
    # Gather results together
    results = await asyncio.gather(*tasks)
    
    end_time = time.time()
    print(f"\nAll tasks finished in {end_time - start_time:.2f} seconds (Sequential wait would be 6.0 seconds).")

# Run the async loop
if __name__ == "__main__":
    asyncio.run(main())
```

---

## 4. Resilient Error Handling (Try-Except)

Because agents are autonomous, a single uncaught exception inside a tool execution can crash the entire planning loop. We must wrap critical processes in robust `try-except` guardrails.

```python
import json

def parse_agent_arguments(raw_json_str: str) -> Dict:
    try:
        # Attempt to parse potentially malformed JSON arguments from model output
        arguments = json.loads(raw_json_str)
        return {"status": "success", "data": arguments}
        
    except json.JSONDecodeError as decode_err:
        # Recover gracefully by returning error context back to the agent's Planning brain
        return {
            "status": "error",
            "error_message": f"Malformed JSON: {str(decode_err)}. Please rewrite the arguments structure."
        }
```

Now that you have mastered these prerequisites, you are ready to explore the **Foundations of Agentic AI** in Lesson 1!
