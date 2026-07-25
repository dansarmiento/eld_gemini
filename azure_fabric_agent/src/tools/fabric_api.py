# src/tools/fabric_api.py
import os
import requests
from azure.identity import DefaultAzureCredential
from azure.core.exceptions import ClientAuthenticationError

def get_fabric_access_token() -> str:
    """
    Acquires an Entra ID access token for Microsoft Fabric using a user-managed identity.
    Relies on Azure CLI or VS Code credentials locally, and Managed Identity in the cloud.
    """
    try:
        credential = DefaultAzureCredential()
        # The specific resource scope required for Fabric REST APIs
        token_obj = credential.get_token("https://api.fabric.microsoft.com/.default")
        return token_obj.token
    except ClientAuthenticationError as e:
        raise RuntimeError(f"Failed to authenticate user-managed identity: {e}")

def get_semantic_model_schema(workspace_id: str, semantic_model_id: str) -> str:
    """
    Retrieves the table and column schema for a specific Fabric semantic model.
    The agent will use this tool to validate schema structures before writing T-SQL.
    """
    token = get_fabric_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Fabric REST API endpoint for dataset/semantic model execution
    # Note: In a production scenario, you would query the executeQueries endpoint 
    # with a DMV (Dynamic Management View) query like `SELECT * FROM $SYSTEM.TMSCHEMA_COLUMNS`
    url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/datasets/{semantic_model_id}/executeQueries"
    
    dmv_query = {
        "queries": [
            {
                "query": "SELECT [TableName], [Name] AS [ColumnName], [DataType] FROM $SYSTEM.TMSCHEMA_COLUMNS"
            }
        ],
        "serializerSettings": {"incudeNulls": True}
    }

    response = requests.post(url, headers=headers, json=dmv_query)
    
    if response.status_code != 200:
        return f"Error retrieving schema: {response.status_code} - {response.text}"
    
    # Return the raw JSON string so the agent can parse the schema definitions
    return response.text