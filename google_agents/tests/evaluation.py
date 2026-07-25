# tests/evaluation.py
"""
Evaluation suite for testing ADK execution trajectories against the dual-fact data engineering model.
"""
from google.adk import AgentEvaluator #
from src.orchestration.agent import primary_orchestrator

def test_telemetry_pipeline_routing():
    """Validates that the orchestrator correctly routes telemetry pipeline requests."""
    test_case = {
        "input": "Trigger a refresh on the ad telemetry metrics.",
        "expected_sub_agent": "dbt_execution_agent",
        "expected_model_target": "fact_ad_telemetry"
    }
    
    # Run the evaluation check programmatically to test execution paths
    result = AgentEvaluator.evaluate(
        agent=primary_orchestrator,
        input=test_case["input"]
    )
    
    # Validate the trajectory hit the correct sub-agent and passed the right model
    assert any(step.agent_name == test_case["expected_sub_agent"] for step in result.trajectory)
    assert test_case["expected_model_target"] in str(result.trajectory)

def test_subscriber_pipeline_routing():
    """Validates routing for the subscriber lifecycle model."""
    result = AgentEvaluator.evaluate(
        agent=primary_orchestrator,
        input="Update the subscriber lifecycle data."
    )
    assert "fact_subscriber_lifecycle" in str(result.trajectory)