"""
Global state module for AI-Researcher.

DEPRECATED: This module is maintained for backward compatibility.
New code should use the ResearcherState class in main_ai_researcher.py instead.

The global state pattern is discouraged because:
- Makes testing difficult
- Can cause race conditions in concurrent execution
- Makes code harder to reason about
"""

# Logging path (set by MetaChainLogger)
LOG_PATH = ""

# Execution flags
START_FLAG = False
FIRST_MAIN = False
EXIT_FLAG = False
INIT_FLAG = False
