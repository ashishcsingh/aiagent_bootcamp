# AI Agent Developer Bootcamp

Welcome to the **aiagent.org Developer Bootcamp**, the canonical self-paced technical curriculum designed to take you from a standard software engineer to a specialized AI Agent developer. 

## 🎥 Introduction Video
Below is an introductory overview of the bootcamp curriculum and objectives:

<div class="relative w-full aspect-video rounded-2xl overflow-hidden border border-slate-800 shadow-2xl my-8">
    <iframe class="absolute inset-0 w-full h-full" src="https://www.youtube.com/embed/shqDkXOtgUk" title="AI Agent Bootcamp Introduction" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
</div>

---

## 🛠️ Summary of Offerings

This bootcamp contains **7 complete modules** ranging from prerequisites up to production deployment and safety guardrails:

### 🐍 [0. Python Crash Course](#00-python-crash-course)
Ensure your scripting foundation is robust. This module covers environment setup, data structures, list comprehensions, error handling, asynchronous programming (`asyncio`), and preparing script pipelines for AI integrations.

### 🧠 [1. Foundations of Agentic AI](#01-agent-foundations)
Understand the shift from passive LLM chat boxes to active agent systems. Explore the ReAct loop design pattern (Reasoning and Acting), thought-action-observation cycles, and standard prompting topologies.

### 🤖 [2. Single-Agent Design](#02-single-agents)
Build a complete autonomous single-agent tool-execution loop from scratch using the official `google-genai` SDK. Learn how to define schemas, invoke functions securely, and feed output results back to the model.

### 👥 [3. Multi-Agent Systems](#03-multi-agent-systems)
Design and orchestrate multi-agent collaboration networks. Learn and compare three distinct paradigms:
- **CrewAI**: Sequential task execution using persona-based role-playing agents.
- **LangGraph**: Stateful, cyclic workflows using blackboard memory and routing nodes.
- **Microsoft AutoGen**: Conversational agents collaborating via automated multi-actor dialogue.
- **Self-Reflection**: Coding agents running their own output and fixing traceback errors iteratively.

### 🔌 [4. Model Context Protocol (MCP)](#04-model-context-protocol)
Master the new universal connectivity standard for AI. Learn how to write customized stdio-based MCP servers using the `FastMCP` Python library, expose tools and resources, and connect them to Claude Desktop, Cursor, or your custom hosts.

### 🔒 [5. Production & Safety](#05-production-deployment)
Prepare your agents for real-world interactions. Learn best practices for rate-limiting, error isolation, defensive tool execution, and Firestore security rules auditing.

### 📖 [6. Key Agent Concepts](#06-agent-concepts)
Review cognitive architectures, transparency models (Reasoning Trails), security sandboxing, and algorithmic humility (knowing when to escalate to a human).

---

## 🚀 How to Get Started
1. Click on **0. Python Crash Course** in the sidebar to start setting up your environment.
2. Run any sandbox simulation inside the browser by clicking the **Access Sandbox** button.
3. Reference the **Production Implementation Guide** under each sandbox to build locally in your preferred IDE.
