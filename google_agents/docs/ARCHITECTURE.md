# Multi-Agent Analytics Orchestrator Architecture

This project utilizes a multi-agent system to automate and validate dbt data transformations. The environment leverages Google ADK's Workflow Runtime, a graph-based execution engine for composing deterministic execution flows. 

## Dual-Fact Execution Paths
The execution agent handles the transformation sequences for the streaming content advertisement measurement platform. The graph workflow ensures these paths execute strictly:
1.  **Telemetry Metrics Pipeline:** Ingestion and transformation of raw streaming event logs into the `fact_ad_telemetry` dbt model.
2.  **Subscriber Lifecycle Pipeline:** Orchestration of subscription state changes into the `fact_subscriber_lifecycle` dbt model.

## Inter-Agent Communication
*   **Primary Orchestrator:** Maintains user context, identifies the target pipeline, and routes the request. 
*   **Execution Agent:** Triggered by the orchestrator. Executes `dbt run` locally via subprocesses and parses standard output logs to detect SQL compilation failures or DuckDB data test anomalies.