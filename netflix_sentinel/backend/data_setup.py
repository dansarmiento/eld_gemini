import duckdb
import chromadb

def setup_mock_infrastructure():
    # 1. Setup DuckDB (Telemetry)
    conn = duckdb.connect('telemetry.db')
    conn.execute("""
        CREATE TABLE IF NOT EXISTS server_logs (
            timestamp TIMESTAMP, service VARCHAR, endpoint VARCHAR, status_code INT, latency_ms INT
        )
    """)
    conn.execute("""
        INSERT INTO server_logs VALUES 
        (current_timestamp, 'streaming-svc', '/video/manifest', 500, 1250),
        (current_timestamp, 'streaming-svc', '/video/manifest', 503, 1400),
        (current_timestamp, 'auth-svc', '/login', 200, 45)
    """)
    conn.commit()

    # 2. Setup ChromaDB (Runbooks)
    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_or_create_collection(name="netflix_runbooks")
    collection.add(
        documents=["If streaming-svc returns 500s on /video/manifest, check the regional CDN cache layer. Latency over 1000ms indicates a cache miss storm."],
        metadatas=[{"source": "runbook-streaming-latency"}],
        ids=["doc1"]
    )
    print("Mock context layer initialized in DuckDB and ChromaDB.")

if __name__ == "__main__":
    setup_mock_infrastructure()