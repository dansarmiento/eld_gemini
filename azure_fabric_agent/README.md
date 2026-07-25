# Enterprise Semantic Model Assistant (Azure AI Foundry)

A secure, goal-oriented multi-agent application deployed on Azure AI Foundry. This assistant is designed to help analytics engineers generate, debug, and optimize complex T-SQL queries against Microsoft Fabric semantic models, adhering to strict enterprise clinical reporting standards.

## Architecture

*   **Azure AI Foundry**: Hosts the stateful agent thread and manages the system persona.
*   **Microsoft Fabric API**: The agent securely retrieves table and column metadata to prevent schema hallucination.
*   **Infrastructure-as-Code (IaC)**: Bicep templates define the AI Hub, Project, and Key Vault for secure, reproducible environments.

## Getting Started

### 1. Environment Setup
Install the necessary Azure SDKs and dependencies:
```bash
pip install -r requirements.txt
```

Create your local `.env` file:
```bash
cp .env.example .env
# Edit .env and populate your Azure Foundry PROJECT_CONNECTION_STRING
```

### 2. Authentication
This project utilizes `DefaultAzureCredential` for a seamless local-to-cloud authentication flow via User-Managed Identities. Before running the agent locally, ensure you are authenticated with the Azure CLI:
```bash
az login
```

### 3. Deploy Infrastructure (Optional)
If you need to stand up a new Azure AI Foundry Hub and Project, run the provided Bicep template:
```bash
az deployment group create --resource-group <Your-Resource-Group> --template-file deploy/infrastructure.bicep
```

### 4. Run the Agent
Execute the main script to initialize the stateful thread and interact with the agent:
```bash
python src/agent.py
```