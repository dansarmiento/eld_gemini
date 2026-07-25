# Sentinel: Agentic Developer & Ops Orchestrator 🚀

Sentinel is an interactive portfolio project demonstrating production-grade, multi-agent AI workflows designed for Internal Developer Platforms (IDPs). 

It showcases the architecture and orchestration required to automate the full software development lifecycle (SDLC) and operational incident triage, utilizing an autonomous multi-agent Python backend and a decoupled Flutter web frontend for visualization.

## 🎯 Project Overview

This project was built to demonstrate applied AI system engineering, specifically focusing on:
*   **Multi-Agent Orchestration:** Coordinating parallel AI agents using LangGraph for cyclic, stateful workflows.
*   **Centralized Context Engineering (Hybrid RAG):** Combining unstructured document retrieval (ChromaDB) with structured telemetry querying (DuckDB) to ground LLM responses in factual, team-specific knowledge.
*   **Operational Workflows:** Automating root cause analysis (RCA) by correlating logs, metrics, and incident runbooks.
*   **Decoupled Architecture:** Separating the heavy Python LLM execution engine from the static Flutter Web visualization layer.

## 🏗️ System Architecture

Because GitHub Pages hosts static sites, Sentinel uses a decoupled trace-based architecture. 

1.  **The Agentic Backend (Python):** Autonomous agents query local databases, synthesize data, and execute tasks. Their reasoning steps, tool calls, and final outputs are logged into structured JSON traces.
2.  **The Visualization Layer (Flutter/Web):** A web dashboard built with Dart and Riverpod that parses the JSON traces and visually replays the multi-agent workflow for the user in real-time.

### Tech Stack
| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **Orchestration** | LangGraph | Stateful multi-agent cyclic graph execution |
| **LLM Engine** | OpenAI API | GPT-4o-mini for reasoning and function calling |
| **Structured Context** | DuckDB | Blazing fast analytical querying of mock server telemetry |
| **Vector Context** | ChromaDB | Embedding and retrieval of operational runbooks |
| **Frontend UI** | Flutter & Riverpod | Interactive, state-driven dashboard deployed to WASM/Web |

## 🧠 Core Agentic Workflows

### 1. Incident Triage & Root Cause Analysis
Simulates an automated response to a PagerDuty latency alert.
*   **Log Analyst Agent:** Translates natural language into SQL, queries DuckDB for 500-level error anomalies, and summarizes the telemetry.
*   **Context Agent:** Takes the identified endpoints and searches ChromaDB for the corresponding service runbooks and historical Jira tickets.
*   **Orchestrator Agent:** Synthesizes the telemetry anomalies with the runbook procedures to generate a concise, actionable Slack RCA update.

### 2. SDLC Pull Request Validation *(Roadmap)*
*   **Code Review Agent:** Scans PR diffs for architectural anti-patterns.
*   **Test Generation Agent:** Automatically generates missing unit tests for modified functions.

## 🚀 Local Setup & Execution

### Prerequisites
*   Python 3.10+
*   Flutter SDK (3.0+)
*   OpenAI API Key

### 1. Run the Python Backend
Initialize the context databases and generate the agent execution traces:
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Export your API key
export OPENAI_API_KEY="sk-your-key-here"

# Seed the DuckDB and ChromaDB instances
python data_setup.py

# Run the LangGraph orchestration (generates JSON trace)
python agent_workflow.py
```

### 2. Run the Flutter Frontend
Launch the UI to visualize the generated agent traces:
```bash
cd frontend
flutter pub get
flutter run -d chrome
```

## 🧪 Evaluations & Guardrails

To ensure production readiness, Sentinel employs several evaluation methodologies (simulated in this MVP):
*   **Tool Determinism:** DuckDB forces the LLM to rely on deterministic SQL aggregations rather than hallucinating metrics.
*   **Context Grounding:** The Orchestrator agent utilizes a strict system prompt preventing it from recommending remediation steps outside of those explicitly retrieved by the Context Agent.
*   **Traceability:** Every LLM generation and tool call is logged to a central state dictionary, allowing for continuous feedback loops and hill-climbing optimization of the prompts.

---
