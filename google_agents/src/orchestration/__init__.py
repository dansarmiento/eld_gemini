"""
src/orchestration/__init__.py

Marks the directory as a Python package and exposes the core agents 
for easier importing across the broader application.
"""

from .agent import primary_orchestrator, dbt_execution_agent

# Explicitly define what gets imported when someone uses `from src.orchestration import *`
__all__ = [
    "primary_orchestrator", 
    "dbt_execution_agent"
]