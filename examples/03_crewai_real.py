#!/usr/bin/env python3
"""
Example 03: Real-World CrewAI Collaboration Workflow

This script demonstrates how to assemble a multi-agent team using the real CrewAI framework
connecting to the Gemini API via standard environment configuration.
"""

import os
import sys

try:
    from crewai import Agent, Crew, Process, Task
except ImportError:
    print("ERROR: 'crewai' package not found.")
    print("Please run: pip install crewai")
    sys.exit(1)

def main():
    # 1. Check for API key
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: GEMINI_API_KEY environment variable is not set.")
        print("Please run: export GEMINI_API_KEY='your-key'")
        sys.exit(1)

    print("[*] Initializing CrewAI Agents with Gemini...")

    # We configure the model setting. CrewAI supports 'gemini/gemini-2.5-flash' out of the box.
    model_name = "gemini/gemini-2.5-flash"

    # 2. Define specialized Agents
    researcher = Agent(
        role="Senior Technology Researcher",
        goal="Gather and compile the latest trends in autonomous AI agent frameworks.",
        backstory="A detail-oriented analyst expert at scanning repository releases and standard updates.",
        verbose=True,
        llm=model_name
    )

    writer = Agent(
        role="Lead Technical Writer",
        goal="Synthesize raw research notes into a clear, executive intelligence briefing.",
        backstory="A communications specialist who converts complex technical details into readable articles.",
        verbose=True,
        llm=model_name
    )

    # 3. Define the Tasks
    research_task = Task(
        description="Identify the top 3 agentic developments in 2026, specifically looking at protocol standards like MCP.",
        expected_output="A list of 3 bullet points with brief technical descriptions.",
        agent=researcher
    )

    writing_task = Task(
        description="Review the researcher's bullet points and write a polished 2-paragraph briefing for an executive newsletter.",
        expected_output="A two-paragraph Markdown briefing.",
        agent=writer
    )

    # 4. Assemble and Run the Crew
    crew = Crew(
        agents=[researcher, writer],
        tasks=[research_task, writing_task],
        process=Process.sequential
    )

    print("\n[*] Starting sequential Crew task kickoff...")
    result = crew.kickoff()

    print("\n" + "="*50 + "\n[Crew Final Result]:\n" + "="*50)
    print(result)

if __name__ == "__main__":
    main()
