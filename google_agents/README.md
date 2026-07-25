# Multi-Agent Analytics Orchestrator (Google ADK)

A collaborative multi-agent system designed to automate, execute, and validate `dbt` data transformations using Google's Agent Development Kit (ADK) and a local DuckDB analytical pipeline.

## Overview
This repository structures a production-ready multi-agent system:
*   **Primary Orchestrator Agent**: Intercepts natural language requests and delegates tasks using ADK's native hierarchical routing.
*   **Execution Agent**: A specialized sub-agent that triggers `dbt run` commands via a local tool, securely interfaces with DuckDB, and parses standard output for SQL compilation or testing errors.

## Getting Started

### 1. Environment Setup
Install the required dependencies using Poetry:
```bash
poetry install
```

Set up your local environment variables:
```bash
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

### 2. Initialize dbt & DuckDB
The agents execute against a local DuckDB instance. Ensure your `profiles.yml` (located by default in `~/.dbt/profiles.yml`) is configured to point to this project:
```yaml
streaming_content_ads:
  target: dev
  outputs:
    dev:
      type: duckdb
      path: streaming_ads_metrics.duckdb
```

### 3. Run the Agent
Use the ADK CLI to spin up the orchestrator locally:
```bash
adk run src/orchestration
```

### 4. Running Evaluations
ADK's integrated evaluation tools allow systematic testing of the routing paths. Run the test suite programmatically:
```bash
pytest tests/evaluation.py
```