FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the configuration and the data interface logic
COPY config/pipeline.yaml ./config/
COPY src/microservices/data_interface/duckdb_agent.py .

CMD ["python", "duckdb_agent.py"]