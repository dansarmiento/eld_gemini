import json
import duckdb
import chromadb
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

# Define the shared state passed between agents
class GraphState(TypedDict):
    incident_query: str
    telemetry_data: str
    runbook_context: str
    final_rca: str
    trace_log: list[dict]

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def log_analyst_node(state: GraphState):
    state["trace_log"].append({"agent": "Log Analyst (DuckDB)", "action": "Querying operational metrics for 500-level errors..."})
    conn = duckdb.connect('telemetry.db')
    df = conn.execute("SELECT service, status_code, avg(latency_ms) as avg_latency FROM server_logs GROUP BY service, status_code HAVING status_code >= 500").df()
    state["telemetry_data"] = df.to_string()
    state["trace_log"].append({"agent": "Log Analyst (DuckDB)", "action": f"Identified anomalies:\n{state['telemetry_data']}"})
    return state

def context_agent_node(state: GraphState):
    state["trace_log"].append({"agent": "Context Agent (RAG)", "action": "Searching vector store for corresponding runbooks..."})
    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_collection(name="netflix_runbooks")
    results = collection.query(query_texts=["streaming-svc 500 error latency"], n_results=1)
    state["runbook_context"] = results['documents'][0][0]
    state["trace_log"].append({"agent": "Context Agent (RAG)", "action": f"Retrieved procedural context:\n{state['runbook_context']}"})
    return state

def orchestrator_node(state: GraphState):
    state["trace_log"].append({"agent": "Orchestrator", "action": "Synthesizing root cause analysis..."})
    prompt = f"""
    Write a brief Root Cause Analysis (RCA) Slack update based on:
    Telemetry: {state['telemetry_data']}
    Runbook: {state['runbook_context']}
    """
    response = llm.invoke([SystemMessage(content="You are a Netflix SRE."), HumanMessage(content=prompt)])
    state["final_rca"] = response.content
    state["trace_log"].append({"agent": "Orchestrator", "action": f"RCA Generated:\n{state['final_rca']}"})
    return state

# Compile the multi-agent graph
workflow = StateGraph(GraphState)
workflow.add_node("log_analyst", log_analyst_node)
workflow.add_node("context_agent", context_agent_node)
workflow.add_node("orchestrator", orchestrator_node)

workflow.add_edge(START, "log_analyst")
workflow.add_edge("log_analyst", "context_agent")
workflow.add_edge("context_agent", "orchestrator")
workflow.add_edge("orchestrator", END)

app = workflow.compile()

if __name__ == "__main__":
    initial_state = {
        "incident_query": "Investigate recent PagerDuty latency alerts.",
        "telemetry_data": "",
        "runbook_context": "",
        "final_rca": "",
        "trace_log": []
    }
    
    # Execute the workflow
    final_state = app.invoke(initial_state)
    
    # Export the decision trace to the Flutter web assets directory
    with open("../frontend/assets/incident_trace.json", "w") as f:
        json.dump(final_state["trace_log"], f, indent=2)
    print("Agentic workflow complete. Traces exported to frontend.")