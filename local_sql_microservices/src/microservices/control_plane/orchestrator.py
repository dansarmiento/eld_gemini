# src/microservices/control_plane/orchestrator.py
import os
from llama_agents import (
    ControlPlaneServer,
    RabbitMQMessageQueue,
    AgentService
)
from llama_agents.launchers import ServerLauncher

def main():
    # 1. Connect to the standardized Message Queue
    rabbitmq_url = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/")
    message_queue = RabbitMQMessageQueue(url=rabbitmq_url)

    # 2. Initialize the Control Plane
    control_plane = ControlPlaneServer(
        message_queue=message_queue,
        orchestrator=None, # Default orchestrator handles basic routing
        host="0.0.0.0",
        port=8000
    )

    # 3. Launch the server
    print("Starting Control Plane Orchestrator...")
    launcher = ServerLauncher([control_plane], message_queue)
    launcher.launch_servers()

if __name__ == "__main__":
    main()