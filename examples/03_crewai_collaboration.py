#!/usr/bin/env python3
"""
Example 03: Simulated CrewAI Collaboration Workflow

This script demonstrates the core concepts of CrewAI:
1. Defining specialized Agents with Roles, Backstories, and Goals.
2. Creating specific Tasks with Descriptions and assigned Agents.
3. Assembling them into a sequential Crew to complete a research project.
"""

import time

# =====================================================================
# 1. Define Agent Class (Simulated CrewAI Agent)
# =====================================================================

class Agent:
    def __init__(self, role: str, goal: str, backstory: str):
        self.role = role
        self.goal = goal
        self.backstory = backstory

    def execute_task(self, task_description: str, context: str = "") -> str:
        print(f"\n[*] Active Agent: [{self.role}]")
        print(f"[*] Backstory: {self.backstory}")
        print(f"[*] Goal: {self.goal}")
        print(f"[*] Working on Task: {task_description}...")
        
        time.sleep(1.5)  # Simulate analytical processing
        
        # Simulated LLM generation based on the agent's specialty
        if "Research" in self.role:
            return (
                "Research Findings:\n"
                "- Model Context Protocol (MCP) downloads reached 97M SDK installs in Q2 2026.\n"
                "- Akamai launched a dedicated 'Know Your Agent' (KYA) security standard.\n"
                "- Multi-agent orchestration is shifting from static pipes to state-based graphs."
            )
        elif "Writer" in self.role:
            return (
                f"Draft Summary (Based on Context):\n"
                f"==================================\n"
                f"The agentic ecosystem in 2026 is rapidly standardizing. Key updates:\n"
                f"1. Standard Protocols: MCP has emerged as a cornerstone of interoperability.\n"
                f"2. Security: Akamai's KYA framework addresses verification challenges.\n"
                f"3. Architecture: State-based workflow graph systems dominate enterprise design.\n\n"
                f"Source context: {context[:60]}..."
            )
        return "Simulated result completed."

# =====================================================================
# 2. Define Task Class (Simulated CrewAI Task)
# =====================================================================

class Task:
    def __init__(self, description: str, agent: Agent):
        self.description = description
        self.agent = agent
        self.output = ""

    def run(self, input_context: str = "") -> str:
        self.output = self.agent.execute_task(self.description, input_context)
        return self.output

# =====================================================================
# 3. Define Crew Orchestrator (Simulated Sequential Crew)
# =====================================================================

class Crew:
    def __init__(self, agents: list, tasks: list):
        self.agents = agents
        self.tasks = tasks

    def kickoff(self) -> str:
        print("[*] Kickoff: Starting Crew Execution Pipeline...")
        context = ""
        for index, task in enumerate(self.tasks):
            print(f"\n" + "="*50 + f"\n[Task {index+1}/{len(self.tasks)}]: {task.description}")
            context = task.run(context)
            print(f"[Task Result]:\n{context}")
        return context

# =====================================================================
# 4. Assembling and Running the Crew
# =====================================================================

def main():
    # Define specialized agents
    researcher = Agent(
        role="Senior Technology Researcher",
        goal="Gather and compile the latest trends in autonomous AI agent frameworks for 2026.",
        backstory="A detail-oriented analyst expert at scanning repository releases and standard updates."
    )

    writer = Agent(
        role="Lead Technical Writer",
        goal="Synthesize raw research notes into a clear, executive intelligence briefing.",
        backstory="A communications specialist who converts complex technical details into readable articles."
    )

    # Define sequential tasks
    task_research = Task(
        description="Search for breakthroughs in MCP and agent security standards.",
        agent=researcher
    )

    task_write = Task(
        description="Write a 3-point briefing outlining the major trends.",
        agent=writer
    )

    # Assemble the Crew
    tech_brief_crew = Crew(
        agents=[researcher, writer],
        tasks=[task_research, task_write]
    )

    # Execute
    final_output = tech_brief_crew.kickoff()
    print("\n" + "="*50 + "\n[Success] Crew finished!\nFinal Briefing Output:\n")
    print(final_output)

if __name__ == "__main__":
    main()
