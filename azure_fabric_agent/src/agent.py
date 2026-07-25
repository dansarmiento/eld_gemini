# src/agent.py
import os
import yaml
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.projects.models import FunctionTool, ToolSet
from src.tools.fabric_api import get_semantic_model_schema

def load_system_prompt(file_path: str = "prompts/system_instructions.yaml") -> dict:
    """Loads the agent persona and constraints from the YAML configuration."""
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def main():
    # 1. Initialize the Foundry Project Client using user-managed identity
    project_connection_string = os.environ.get("PROJECT_CONNECTION_STRING")
    if not project_connection_string:
        raise ValueError("PROJECT_CONNECTION_STRING environment variable is missing.")

    project_client = AIProjectClient.from_connection_string(
        credential=DefaultAzureCredential(),
        conn_str=project_connection_string
    )

    # 2. Load constraints and define tools
    agent_config = load_system_prompt()
    
    # Register the Fabric schema retrieval function as a tool
    fabric_schema_tool = FunctionTool(get_semantic_model_schema)
    toolset = ToolSet()
    toolset.add(fabric_schema_tool)

    # 3. Create the Agent in Azure AI Foundry
    print(f"Deploying {agent_config['name']} to Azure AI Foundry...")
    agent = project_client.agents.create_agent(
        model=agent_config['model'],
        name=agent_config['name'],
        instructions=agent_config['system_prompt'],
        toolset=toolset,
        temperature=agent_config['temperature']
    )

    # 4. Create a stateful thread for context management
    thread = project_client.agents.create_thread()
    print(f"Thread created with ID: {thread.id}")

    # 5. Example Interaction
    user_request = (
        "Generate a T-SQL query to group our recent medication orders by the generic drug name "
        "and count the volume. Please check the schema first."
    )
    
    message = project_client.agents.create_message(
        thread_id=thread.id,
        role="user",
        content=user_request
    )

    # Execute the run and allow the agent to use tools
    run = project_client.agents.create_and_poll_run(
        thread_id=thread.id,
        assistant_id=agent.id
    )

    if run.status == "completed":
        messages = project_client.agents.list_messages(thread_id=thread.id)
        # The latest response is at the beginning of the list
        print("\nAgent Response:")
        print(messages.data[0].content[0].text.value)
    else:
        print(f"Run failed with status: {run.status}")

if __name__ == "__main__":
    main()  