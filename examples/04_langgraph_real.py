#!/usr/bin/env python3
"""
Example 04: Real-World LangGraph Stateful Workflow

This script demonstrates how to build a stateful, cyclic agent workflow
using the official LangGraph library and the Gemini API.
"""

import os
import sys
from typing import TypedDict

try:
    from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langgraph.graph import StateGraph, START, END
except ImportError:
    print("ERROR: 'langchain-google-genai' or 'langgraph' package not found.")
    print("Please run: pip install langchain-google-genai langgraph")
    sys.exit(1)

# 1. Define the Graph State structure
class GraphState(TypedDict):
    document: str
    feedback: str
    revisions: int

def main():
    # Check for API key
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: GEMINI_API_KEY environment variable is not set.")
        print("Please run: export GEMINI_API_KEY='your-key'")
        sys.exit(1)

    print("[*] Initializing Gemini LangGraph workflow...")
    # Initialize the Gemini model via LangChain integration
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=api_key)

    # 2. Define Node Functions
    def writer_node(state: GraphState) -> dict:
        revisions = state.get("revisions", 0)
        feedback = state.get("feedback", "")
        print(f"\n[*] [Node: Writer] Drafting/editing document (Revision: {revisions})...")

        prompt = "Write a one-sentence technical introduction to building AI agents."
        if feedback:
            prompt += f"\n\nPlease edit this draft based on the critic feedback: '{feedback}'"

        response = llm.invoke([HumanMessage(content=prompt)])
        return {
            "document": response.content,
            "revisions": revisions + 1
        }

    def critic_node(state: GraphState) -> dict:
        print("[*] [Node: Critic] Evaluating document quality...")
        doc = state.get("document", "")

        prompt = (
            f"Review this draft text: '{doc}'\n"
            "If the draft contains the phrase 'Model Context Protocol' or 'MCP', reply with the word 'Approved' followed by a short comment.\n"
            "If it does not contain 'MCP' or 'Model Context Protocol', reply with 'Feedback: You must mention the Model Context Protocol (MCP) as the standard tool connection layer.'"
        )

        response = llm.invoke([HumanMessage(content=prompt)])
        return {"feedback": response.content}

    # 3. Define the routing conditional edge logic
    def should_continue(state: GraphState) -> str:
        feedback = state.get("feedback", "")
        print(f"\n[*] [Router] Analyzing feedback: '{feedback}'")
        if "Approved" in feedback:
            print("[Router] Action: Draft approved! Routing to [END].")
            return "end"
        else:
            print("[Router] Action: Draft rejected. Routing back to [Writer] node.")
            return "writer"

    # 4. Compile the Graph
    workflow = StateGraph(GraphState)

    # Add Nodes
    workflow.add_node("writer", writer_node)
    workflow.add_node("critic", critic_node)

    # Set Entry Point
    workflow.add_edge(START, "writer")

    # Connect Nodes
    workflow.add_edge("writer", "critic")

    # Add Conditional Edges
    workflow.add_conditional_edges(
        "critic",
        should_continue,
        {
            "writer": "writer",
            "end": END
        }
    )

    app = workflow.compile()

    # 5. Run the Workflow
    initial_state = {
        "document": "",
        "feedback": "",
        "revisions": 0
    }

    print("\n[*] Starting LangGraph workflow execution...")
    final_output = app.invoke(initial_state)

    print("\n" + "="*50 + "\n[LangGraph Final State Output]:\n" + "="*50)
    print(f"Revisions: {final_output.get('revisions')}")
    print(f"Final Document: {final_output.get('document')}")
    print(f"Final Feedback: {final_output.get('feedback')}")

if __name__ == "__main__":
    main()
