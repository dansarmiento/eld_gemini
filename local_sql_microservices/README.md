# Privacy-First Text-to-SQL Microservices

A fully local, microservice-based multi-agent application. This architecture uses `llama-agents` and `docker-compose` to isolate intent orchestration from database execution. Natural language is translated into SQL queries against DuckDB using Nvidia's Jet Nemotron, running entirely offline via Ollama.

## Architecture

1.  **RabbitMQ Message Queue:** Handles asynchronous parameter passing (including serialized Pandas dataframes) between microservices.
2.  **Control Plane Orchestrator:** An API server that receives requests and routes them to the appropriate execution agent.
3.  **Data Interface Agent:** An isolated worker service equipped with DuckDB execution tools.

## Setup Instructions

### 1. Initialize Ollama and Jet Nemotron
Ensure Ollama is installed on your host machine. Pull the specified local model:
```bash
ollama pull jet-nemotron
```
*Note: Make sure the Ollama server is running locally (`ollama serve`) so the Docker containers can reach it via `host.docker.internal`.*

### 2. Prepare the DuckDB Environment
Ensure your DuckDB database file is placed in the `./data` directory relative to the repository root. The configuration in `config/pipeline.yaml` expects `local_analytics.duckdb` to be present.

### 3. Spin Up the Microservices
Build and launch the Control Plane, Data Interface, and RabbitMQ broker using Docker Compose:
```bash
docker-compose up --build
```

### 4. Interact with the System
Once the services are healthy, you can send tasks to the Control Plane API (running on port 8000) using the `llama-agents` client or standard HTTP POST requests to trigger the Text-to-SQL pipeline.