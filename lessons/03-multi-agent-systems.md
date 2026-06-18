# Lesson 3: Multi-Agent Collaboration

As systems grow in complexity, a single agent can quickly become overwhelmed by too many tools, a large context window, or competing tasks. In this module, we will explore multi-agent architectures and collaboration frameworks.

## 1. Why Multi-Agent?

Single agents suffer from "tool bloat" and context dilution. By splitting tasks among specialized agents, we can:
*   **Encapsulate State:** Each agent only focuses on its specific task and has access to a tailored subset of tools.
*   **Improve Accuracy:** An agent designed strictly as a "Code Reviewer" performs better than a generalist agent trying to write, review, and deploy code in a single step.
*   **Scale Execution:** Agents can operate in parallel to solve complex workflows.

---

## 2. Multi-Agent Topologies

There are three primary collaboration structures:

### A. Sequential (Pipeline)
Tasks flow in a fixed, linear order from one agent to the next.
```
[User] -> [Researcher Agent] -> [Writer Agent] -> [Editor Agent] -> [Output]
```

### B. Hierarchical (Manager-Worker)
A manager agent delegates sub-tasks to worker agents, gathers their observations, and reports the final answer.
```
                +-------------------+
                |   Manager Agent   |
                +----+---------+----+
                     |         |
         +-----------+         +-----------+
         v                                 v
+--------+--------+               +--------+--------+
|  Writer Agent   |               | Researcher Agent|
+-----------------+               +-----------------+
```

### C. Graph (Conversational / Networked)
Agents talk to each other dynamically based on state changes. This is the most flexible topology, allowing loops, conditional branching, and human-in-the-loop validation.

---

## 3. Shared State & Context

For agents to cooperate, they must share information. There are two primary mechanisms:
1.  **Message Passing:** Agents send messages to one another directly.
2.  **Shared Memory (State Blackboard):** A centralized database or state graph (like in LangGraph) stores the global state. Every agent reads from and writes updates to this shared blackboard.

---

## 4. Multi-Agent Frameworks

Depending on your design requirements, you can choose from several standard frameworks:

| Framework | Topology Style | State Model | Ideal For |
| :--- | :--- | :--- | :--- |
| **CrewAI** | Role-based / Sequential | Shared memory & Tasks | Structured sequential business workflows |
| **LangGraph** | Cyclic Graphs | Shared state graph (Redux-style) | Complex, cyclic multi-agent software engineering loops |
| **AutoGen** | Conversational / Dynamic | Message passing | Multi-party debates, interactive simulations |
| **smolagents** | Code-first | In-context Python execution | Fast execution using LLMs that output Python directly |
