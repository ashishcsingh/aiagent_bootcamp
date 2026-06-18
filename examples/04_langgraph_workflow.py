#!/usr/bin/env python3
"""
Example 04: Simulated LangGraph Workflow

This script demonstrates the core concepts of LangGraph:
1. Maintaining a centralized, shared State dictionary (Blackboard).
2. Creating Nodes (Python functions that receive state and return state updates).
3. Defining Edges and Conditional routing (deciding next steps based on state).
4. Running a cyclic graph execution loop (Writer -> Critic -> Writer loop).
"""

import time

# =====================================================================
# 1. State Definition
# =====================================================================
# In LangGraph, the State dictionary is the single source of truth.

class State:
    def __init__(self, document: str = "", feedback: str = "", revisions: int = 0):
        self.data = {
            "document": document,
            "feedback": feedback,
            "revisions": revisions
        }

    def update(self, updates: dict):
        self.data.update(updates)

# =====================================================================
# 2. Define Nodes (Steps in the Workflow Graph)
# =====================================================================

def writer_node(state: dict) -> dict:
    """Writes or edits the document based on the critic's feedback."""
    revisions = state.get("revisions", 0)
    print(f"\n[*] [Node: Writer] Drafting/editing document (Revision: {revisions})...")
    time.sleep(1.0)

    if revisions == 0:
        doc = "Draft: AI Agents will automate everything in VS Code using basic REST APIs."
    else:
        doc = f"Revised Draft: AI Agents connect locally using the Model Context Protocol (MCP) to access tools and context securely."

    return {
        "document": doc,
        "revisions": revisions + 1
    }

def critic_node(state: dict) -> dict:
    """Evaluates the draft and provides structured feedback."""
    print("[*] [Node: Critic] Evaluating document quality...")
    time.sleep(1.0)
    doc = state.get("document", "")

    if "REST APIs" in doc:
        feedback = "Critique: The draft misses the new industry standard. Re-write to mention Model Context Protocol (MCP)."
    else:
        feedback = "Approved: The draft looks technically accurate and modern."

    return {"feedback": feedback}

# =====================================================================
# 3. Define Conditional Edges (Router)
# =====================================================================

def should_continue(state: dict) -> str:
    """Evaluates the state and routes to the next node or exits."""
    feedback = state.get("feedback", "")
    print(f"\n[*] [Router] Analyzing feedback: '{feedback}'")
    
    if "Approved" in feedback:
        print("[Router] Action: Draft approved! Routing to [END].")
        return "END"
    else:
        print("[Router] Action: Draft rejected. Routing back to [Writer] node.")
        return "writer"

# =====================================================================
# 4. Compiled Graph Runner
# =====================================================================

def run_workflow():
    # Initialize shared state
    state = State()
    
    # Define active execution pointer
    current_node = "writer"
    
    print("[*] Compiling Graph: [Writer Node] <--> [Critic Node] --> Conditional Edge")
    print("*"*50)
    
    # Run execution loop manually to simulate compiled LangGraph traversal
    steps = 0
    while steps < 10:
        steps += 1
        
        if current_node == "writer":
            # Execute node and merge output updates back into state
            updates = writer_node(state.data)
            state.update(updates)
            print(f"[State Update]: document='{state.data['document']}'")
            
            # Go to next linear edge
            current_node = "critic"
            
        elif current_node == "critic":
            updates = critic_node(state.data)
            state.update(updates)
            print(f"[State Update]: feedback='{state.data['feedback']}'")
            
            # Evaluate conditional edge router
            route = should_continue(state.data)
            if route == "END":
                break
            else:
                current_node = "writer"
                
    print("\n" + "="*50 + "\n[Success] Graph execution finished!\nFinal Document:\n")
    print(state.data["document"])

if __name__ == "__main__":
    run_workflow()
