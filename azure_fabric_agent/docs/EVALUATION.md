# Agent Evaluation Methodology

## Overview
The Fabric Semantic Assistant is evaluated using a hill-climbing methodology combined with human-in-the-loop feedback. Because the agent generates T-SQL for highly sensitive and structured semantic models, evaluation prioritizes structural compliance over mere query execution.

## Evaluation Metrics
1. **Schema Adherence:** Does the generated query exclusively reference tables and columns confirmed by the `get_fabric_metadata` tool?
2. **Deduplication Compliance:** Does the query utilize window functions for deduplication rather than `DISTINCT`?
3. **Execution Success:** Does the generated T-SQL execute cleanly against the target Fabric SQL endpoint without compilation errors?

## Core Test Cases

*   **Test Case 1: Ambulatory Visit Deduplication**
    *   *Input:* "Pull the latest ambulatory visit records for this month and ensure there are no duplicate encounter IDs."
    *   *Expected Behavior:* Agent generates a CTE utilizing `ROW_NUMBER() OVER(PARTITION BY encounter_id ORDER BY visit_date DESC)` to filter the most recent record.

*   **Test Case 2: Medication Order Aggregation**
    *   *Input:* "Generate a script to group our recent medication orders by the generic drug name and count the volume."
    *   *Expected Behavior:* Agent correctly maps the aggregation field, ensuring the query groups on `simplegenericname` instead of `genericname` as per the clinical data reporting standards.

## Human-in-the-Loop Feedback
When the agent fails a test case, the erroneous output and the corrected T-SQL are appended as few-shot examples into the next version of `prompts/system_instructions.yaml`. This ensures the model climbs the gradient toward perfect enterprise compliance.