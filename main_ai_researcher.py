"""
Main entry point for AI-Researcher web interface.

This module is used by web_ai_researcher.py (Gradio UI).
For CLI usage, prefer `python -m research_agent.cli`.
"""
import argparse
import asyncio
import logging
import os
from contextlib import contextmanager
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Project root directory
PROJECT_ROOT = Path(__file__).parent


class ResearcherState:
    """Manages execution state for the AI Researcher.

    Uses a context manager pattern instead of global mutable state.
    """
    def __init__(self):
        self._running = False
        self._lock = False

    @property
    def is_running(self) -> bool:
        return self._running

    @contextmanager
    def execution_context(self):
        """Context manager for safe execution state management."""
        if self._lock:
            logger.warning("Execution already in progress, skipping")
            yield False
            return

        self._lock = True
        self._running = True
        try:
            yield True
        finally:
            self._running = False
            self._lock = False


# Global state instance (thread-safe for single-threaded Gradio)
_state = ResearcherState()


def get_config() -> dict:
    """Load configuration from environment variables with defaults."""
    load_dotenv()
    return {
        "category": os.getenv("CATEGORY", "vq"),
        "instance_id": os.getenv("INSTANCE_ID", "one_layer_vq"),
        "task_level": os.getenv("TASK_LEVEL", "task1"),
        "container_name": os.getenv("CONTAINER_NAME", "ai_researcher"),
        "workplace_name": os.getenv("WORKPLACE_NAME", "workplace"),
        "cache_path": os.getenv("CACHE_PATH", "cache"),
        "port": int(os.getenv("PORT", "12380")),
        "max_iter_times": int(os.getenv("MAX_ITER_TIMES", "0")),
    }


def create_args(config: dict) -> argparse.Namespace:
    """Create an argparse Namespace from config dict."""
    args = argparse.Namespace()
    args.instance_path = str(PROJECT_ROOT / "benchmark" / "final" / config["category"] / f"{config['instance_id']}.json")
    args.container_name = config["container_name"]
    args.task_level = config["task_level"]
    args.workplace_name = config["workplace_name"]
    args.cache_path = config["cache_path"]
    args.port = config["port"]
    args.max_iter_times = config["max_iter_times"]
    args.category = config["category"]
    return args


def main_ai_researcher(input_text: str, reference: str, mode: str) -> Optional[str]:
    """Run AI Researcher task based on mode.

    Args:
        input_text: User input/ideas for the research task.
        reference: Reference papers or materials.
        mode: One of 'Detailed Idea Description', 'Reference-Based Ideation',
              or 'Paper Generation Agent'.

    Returns:
        Result string or None if execution was skipped.
    """
    config = get_config()

    with _state.execution_context() as can_execute:
        if not can_execute:
            logger.warning("Skipping execution - already running")
            return None

        # Import here to avoid circular imports and allow lazy loading
        from research_agent.constant import COMPLETION_MODEL

        args = create_args(config)
        args.model = COMPLETION_MODEL

        if mode == 'Detailed Idea Description':
            logger.info(f"Starting Detailed Idea task: {config['category']}/{config['instance_id']}")
            from research_agent import run_infer_plan
            run_infer_plan.main(args, input_text, reference)

        elif mode == 'Reference-Based Ideation':
            logger.info(f"Starting Reference-Based task: {config['category']}/{config['instance_id']}")
            from research_agent import run_infer_idea
            run_infer_idea.main(args, reference)

        elif mode == 'Paper Generation Agent':
            logger.info(f"Starting Paper Generation: {config['category']}/{config['instance_id']}")
            from paper_agent import writing
            asyncio.run(writing.writing(config["category"], config["instance_id"]))

        else:
            logger.error(f"Unknown mode: {mode}")
            return None

    logger.info("Task completed successfully")
    return "Task completed"
