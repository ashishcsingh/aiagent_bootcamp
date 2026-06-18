#!/usr/bin/env python3
"""
Example 06 (Sandbox): Self-Reflection Coding Agent
This script illustrates the self-reflection and error-correction loop.
It executes code, intercepts failures/tracebacks, and feeds them back to the
agent to automatically repair bugs.
"""

import sys
import traceback

# Simulated LLM that behaves like a coding agent
class MockCodingAgent:
    def __init__(self):
        self.iteration = 0

    def generate_code(self, prompt: str, traceback_msg: str = None) -> str:
        self.iteration += 1
        if self.iteration == 1:
            print("\n[Agent] Initial draft of the function:")
            # Has a bug: division by zero and undefined variable typo
            return """def divide_and_sum(numbers, divisor):
    # Bug: Forgot to check if divisor is 0
    # Bug: Using undefined variable 'total_sum' (typo: tot_sum)
    tot_sum = sum(numbers)
    return total_sum / divisor
"""
        elif self.iteration == 2:
            print("\n[Agent] Reflecting on the error traceback:")
            print(f"Error observed: {traceback_msg.strip()}")
            print("[Agent] Identifying bugs: 1. 'total_sum' is undefined (should be 'tot_sum'). 2. Need guardrail for division by zero.")
            print("[Agent] Generating corrected code...")
            return """def divide_and_sum(numbers, divisor):
    if divisor == 0:
        return 0
    tot_sum = sum(numbers)
    return tot_sum / divisor
"""
        else:
            return ""

def execute_and_test(code_str: str) -> str:
    """Executes the agent's code in a local namespace and runs test assertions."""
    local_scope = {}
    try:
        # Compile and execute code string in local scope
        exec(code_str, {}, local_scope)
    except Exception as e:
        return f"Compilation Error:\n{traceback.format_exc()}"

    # Get the function
    func = local_scope.get("divide_and_sum")
    if not func:
        return "Error: function 'divide_and_sum' not found in namespace."

    # Run Test Cases
    try:
        # Test Case 1: normal execution
        res = func([1, 2, 3], 2)
        if res != 3.0:
            return f"Assertion Error: expected 3.0, got {res}"
            
        # Test Case 2: division by zero
        res_zero = func([1, 2, 3], 0)
        # If no error guardrail, this will raise ZeroDivisionError
        
        return "SUCCESS"
    except Exception as e:
        return f"Runtime Execution Error:\n{traceback.format_exc()}"

def main():
    print("[*] Starting Self-Correction Coding Agent...")
    agent = MockCodingAgent()
    prompt = "Write a Python function 'divide_and_sum(numbers, divisor)' that sums a list and divides it by the divisor."
    
    code = agent.generate_code(prompt)
    traceback_msg = None
    
    for attempt in range(1, 4):
        print(f"\n--- Attempt {attempt} ---")
        print("[System] Compiling and running function...")
        
        result = execute_and_test(code)
        
        if result == "SUCCESS":
            print("\n[System] Verification succeeded! All tests passed.")
            print("[System] Final working code:\n" + code.strip())
            break
        else:
            print(f"\n[System] Test verification failed!")
            traceback_msg = result
            # Ask agent to fix
            code = agent.generate_code(prompt, traceback_msg)
    else:
        print("\n[System] Agent failed to solve the problem within iteration limits.")

if __name__ == "__main__":
    main()
