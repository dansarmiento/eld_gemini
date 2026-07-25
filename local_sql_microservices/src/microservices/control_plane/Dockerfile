FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the control plane logic
COPY src/microservices/control_plane/orchestrator.py .

# Expose the API port
EXPOSE 8000

CMD ["python", "orchestrator.py"]