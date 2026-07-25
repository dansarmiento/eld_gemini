"""
src/orchestration/agent.py

This script defines the Primary Orchestrator and the dbt Execution Agent using 
Google ADK. It can be run locally using the `adk run src/orchestration` command.
"""

import subprocess
from google.adk import Agent, Tool

# ==========================================
# 1. Tool Definition for dbt Execution
# ==========================================

def execute_dbt_run(models: str) -> str:
    """
    Executes a dbt run command for the specified models and captures the output.
    This tool allows the execution agent to interact with the local dbt environment.
    """
    try:
        # Executes the transformation via subprocess to capture raw logs
        result = subprocess.run(
            ["dbt", "run", "--select", models],
            capture_output=True,
            text=True,
            check=False
        )
        
        # Return both stdout and stderr so the agent can parse logs for errors
        if result.returncode != 0:
            return f"Execution Failed. Error: {result.stderr}\nLogs: {result.stdout}"
        
        return f"Execution Successful. Logs: {result.stdout}"
    except Exception as e:
        return f"Failed to invoke dbt subprocess: {str(e)}"

# Register the Python function as an ADK Tool
dbt_tool = Tool.from_function(execute_dbt_run)


# ==========================================
# 2. Sub-Agent: dbt Execution Agent
# ==========================================

dbt_execution_agent = Agent(
    name="dbt_execution_agent",
    model="gemini-1.5-pro",
    instruction=(
        "You are a specialized execution agent responsible for running dbt data transformations. "
        "When assigned a model or path, use the execute_dbt_run tool to trigger the transformation. "
        "Crucially, you must parse the raw output logs returned by the tool. Identify any SQL "
        "compilation errors, data test failures, or warnings, and return a structured summary "
        "of the execution status to the orchestrator."
    ),
    tools=[dbt_tool]
)


# ==========================================
# 3. Primary Agent: Orchestrator
# ==========================================

primary_orchestrator = Agent(
    name="primary_orchestrator",
    model="gemini-1.5-pro",
    instruction=(
        "You are the Primary Orchestrator Agent for an enterprise analytics data pipeline. "
        "You receive natural language requests from users regarding data transformations, "
        "determine which dbt models need to be refreshed, and delegate the actual execution "
        "to the 'dbt_execution_agent'. Do not attempt to run dbt yourself. "
        "Once the execution agent returns the parsed logs, format a final executive summary "
        "for the user detailing what was run and if any upstream bottlenecks occurred."
    ),
    # Hierarchical routing: passing the sub-agent directly allows the orchestrator 
    # to delegate tasks to it natively.
    agents=[dbt_execution_agent] 
)