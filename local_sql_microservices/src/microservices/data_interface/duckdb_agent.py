# src/microservices/data_interface/duckdb_agent.py
import os
import yaml
import duckdb
import pandas as pd
from llama_index.core.tools import FunctionTool
from llama_index.llms.ollama import Ollama
from llama_index.core.agent import ReActAgent
from llama_agents import (
    AgentService,
    RabbitMQMessageQueue
)
from llama_agents.launchers import ServerLauncher

def load_config() -> dict:
    with open("config/pipeline.yaml", "r") as f:
        return yaml.safe_load(f)

def execute_duckdb_query(sql_query: str) -> str:
    """
    Executes a generated SQL query against the local DuckDB instance.
    Returns the Pandas dataframe serialized as a JSON string for queue transmission.
    """
    config = load_config()
    db_path = config["database"]["path"]
    
    try:
        # Connect, execute, and fetch as Pandas DataFrame
        conn = duckdb.connect(db_path)
        df = conn.execute(sql_query).df()
        conn.close()
        
        # Serialize Pandas DataFrame to JSON string for the message broker
        return df.to_json(orient="records")
    except Exception as e:
        return f"Error executing query: {str(e)}"

def main():
    config = load_config()
    
    # 1. Initialize Jet Nemotron via local Ollama
    llm = Ollama(
        model=config["llm"]["model"],
        base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
        request_timeout=config["llm"]["timeout"]
    )

    # 2. Create the DuckDB interface tool
    duckdb_tool = FunctionTool.from_defaults(fn=execute_duckdb_query)

    # 3. Initialize the ReAct Agent
    agent = ReActAgent.from_tools(
        tools=[duckdb_tool],
        llm=llm,
        system_prompt=(
            "You are a specialized Data Interface Agent. Convert natural language "
            "questions into optimized SQL queries for DuckDB, execute them using "
            "your tool, and summarize the returned data."
        )
    )

    # 4. Connect to Message Queue and Register Service
    rabbitmq_url = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/")
    message_queue = RabbitMQMessageQueue(url=rabbitmq_url)

    agent_service = AgentService(
        agent=agent,
        message_queue=message_queue,
        description="Data Interface Agent for querying local DuckDB",
        service_name="duckdb_interface_service"
    )

    print("Starting Data Interface Microservice...")
    launcher = ServerLauncher([agent_service], message_queue)
    launcher.launch_servers()

if __name__ == "__main__":
    main()