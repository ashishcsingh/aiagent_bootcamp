# AI Agent Bootcamp | aiagent.org

Welcome to the official **AI Agent Bootcamp**, a premium, self-paced technical curriculum designed to take you from agentic concepts to production-grade deployment.

This repository serves as the learning materials and interactive presentation site for the bootcamp.

---

## 📚 Curriculum Overview

| Module | Topic | Description | Link |
| :--- | :--- | :--- | :--- |
| **01** | **Foundations of Agentic AI** | Discover the core brain, planning, memory, and tool-calling components of agents. | [Lesson 1](lessons/01-agent-foundations.md) |
| **02** | **Single-Agent Design** | Build custom execution and tool-calling loops from scratch in Python. | [Lesson 2](lessons/02-single-agents.md) |
| **03** | **Multi-Agent Collaboration** | Learn agent pipelines, hierarchical manager-worker trees, and state networks. | [Lesson 3](lessons/03-multi-agent-systems.md) |
| **04** | **Model Context Protocol** | Master the open MCP standard, host/client/server roles, and build local servers. | [Lesson 4](lessons/04-model-context-protocol.md) |
| **05** | **Production & Safety** | Implement isolated code sandboxes, guardrails, eval suites, and cost control. | [Lesson 5](lessons/05-production-deployment.md) |

---

## 🛠️ Getting Started

### 1. View the Interactive Site Locally
To run and view the beautifully formatted interactive site in your browser:
1. Initialize the workspace and install dev dependencies:
   ```bash
   npm install
   ```
2. Build or watch the Tailwind styling:
   ```bash
   npm run build
   ```
3. Open `index.html` directly in your browser, or serve it using any local dev server (e.g. `npx serve .`).

### 2. Run the Code Examples
Boilerplate execution files are located in the `examples/` directory.

#### Example 01: ReAct Loop
Demonstrates a manual Reasoning + Action loop in pure Python:
```bash
python examples/01_react_loop.py
```

#### Example 02: MCP Server
Exposes a minimal stdio-based Model Context Protocol (MCP) server:
```bash
python examples/02_mcp_server.py
```
To run the server in a client like Claude Desktop, append its path configuration to your client settings.
