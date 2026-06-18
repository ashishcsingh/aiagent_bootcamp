#!/usr/bin/env python3
"""
Example 06 (Real): Self-Reflection Coding Agent
This script uses the official Google GenAI SDK to draft python code,
runs it locally, intercepts any traceback errors, and sends the errors
back to Gemini to automatically correct the code.
"""

import os
import sys
import traceback
from google import genai
from google.genai import types

def run_user_code(code_str: str) -> str:
    """Safely executes the function in isolation and validates it."""
    local_scope = {}
    try:
        # Compile and execute the function definition
        exec(code_str, {}, local_scope)
    except Exception as e:
        return f"Compilation Error:\n{traceback.format_exc()}"

    # Verify function exists
    func = local_scope.get("divide_and_sum")
    if not func:
        return "Error: function 'divide_and_sum' was not defined in the namespace."

    # Validate with assertions
    try:
        # Test Case 1: Normal math
        res1 = func([10, 20, 30], 2)
        assert res1 == 30.0, f"Expected 30.0, got {res1}"

        # Test Case 2: Division by zero
        res2 = func([10, 20, 30], 0)
        assert res2 == 0, f"Expected 0 for division by zero, got {res2}"
        
        return "SUCCESS"
    except Exception as e:
        return f"Validation / Runtime Error:\n{traceback.format_exc()}"

def main():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: GEMINI_API_KEY environment variable is not set.")
        print("Please run: export GEMINI_API_KEY='your-key'")
        sys.exit(1)

    print("[*] Initializing Gemini Client...")
    client = genai.Client(api_key=api_key)

    prompt = """
    Write a Python function named `divide_and_sum(numbers: list, divisor: float) -> float`.
    It sum the numbers list and divide it by the divisor.
    If the divisor is zero, it must return 0.
    
    Provide ONLY the raw Python code block, nothing else. Do not wrap in backticks or markdown formats.
    """

    print(f"\n[*] Prompting Gemini to write the function...")
    
    # We construct the conversation history
    history = [
        types.Content(role="user", parts=[types.Part.from_text(text=prompt)])
    ]

    max_attempts = 3
    for attempt in range(1, max_attempts + 1):
        print(f"\n--- Attempt {attempt} ---")
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=history,
            config=types.GenerateContentConfig(
                temperature=0.2,
                system_instruction="You are an expert Python developer. Generate raw python code only. No comments or descriptions."
            )
        )
        
        code_output = response.text.strip()
        # Clean any accidental markdown code formatting
        if code_output.startswith("```"):
            lines = code_output.split("\n")
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines[-1].startswith("```"):
                lines = lines[:-1]
            code_output = "\n".join(lines).strip()

        print(f"[Gemini Drafted Code]:\n{code_output}")
        
        # Append response to history
        history.append(types.Content(role="model", parts=[types.Part.from_text(text=code_output)]))
        
        # Test it
        validation_result = run_user_code(code_output)
        
        if validation_result == "SUCCESS":
            print("\n[SUCCESS] Code passed all validation checks!")
            print("="*60)
            print("Final validated code:\n" + code_output)
            break
        else:
            print(f"\n[FAILURE] Code failed validation tests.")
            print(f"[Error Feedback]:\n{validation_result}")
            
            # Feed the error back to the model
            feedback_prompt = f"""
            The code you generated failed validation with the following error message:
            {validation_result}
            
            Please reflect on this traceback, locate the bug, and write the corrected code.
            Provide ONLY the raw python function.
            """
            history.append(types.Content(role="user", parts=[types.Part.from_text(text=feedback_prompt)]))
    else:
        print("\n[ERROR] Failed to compile and validate the code within iteration limits.")

if __name__ == "__main__":
    main()
