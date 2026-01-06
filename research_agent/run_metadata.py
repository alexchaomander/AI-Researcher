from __future__ import annotations

import json
import os
import platform
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict


def _git_commit(project_root: Path) -> str | None:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=project_root,
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip()
    except Exception:
        return None


def _git_dirty(project_root: Path) -> bool | None:
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=project_root,
            check=True,
            capture_output=True,
            text=True,
        )
        return bool(result.stdout.strip())
    except Exception:
        return None


def build_run_metadata(args, eval_instance: Dict[str, Any]) -> Dict[str, Any]:
    project_root = Path(__file__).resolve().parent.parent
    log_path = None
    try:
        from research_agent.inno.logger import LoggerManager
        logger = LoggerManager.get_logger()
        if logger:
            log_path = logger.log_path
    except Exception:
        log_path = None
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "instance": {
            "path": str(getattr(args, "instance_path", "")),
            "id": eval_instance.get("instance_id"),
            "target": eval_instance.get("target"),
            "task_level": getattr(args, "task_level", None),
            "category": getattr(args, "category", None),
        },
        "models": {
            "completion_model": getattr(args, "model", None),
            "cheap_model": os.getenv("CHEEP_MODEL"),
            "embedding_model": os.getenv("EMBEDDING_MODEL"),
            "api_base_url": os.getenv("API_BASE_URL") or os.getenv("OPENROUTER_API_BASE"),
        },
        "execution": {
            "dry_run": bool(getattr(args, "dry_run", False)),
            "use_docker": os.getenv("USE_DOCKER", "false"),
            "container_name": getattr(args, "container_name", None),
            "workplace_name": getattr(args, "workplace_name", None),
            "seed": os.getenv("AI_RESEARCHER_SEED"),
            "log_path": log_path,
            "prompt_snapshot_path": None,
        },
        "environment": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "git_commit": _git_commit(project_root),
            "git_dirty": _git_dirty(project_root),
        },
        "dataset_setup": {},
    }


def write_run_metadata(output_dir: str | Path, payload: Dict[str, Any]) -> Path:
    output_path = Path(output_dir) / "run_metadata.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=True)
    return output_path


def _deep_merge(base: Dict[str, Any], updates: Dict[str, Any]) -> Dict[str, Any]:
    merged = dict(base)
    for key, value in updates.items():
        if (
            key in merged
            and isinstance(merged[key], dict)
            and isinstance(value, dict)
        ):
            merged[key] = _deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


def update_run_metadata(output_dir: str | Path, updates: Dict[str, Any]) -> Path:
    output_path = Path(output_dir) / "run_metadata.json"
    if output_path.exists():
        with output_path.open("r", encoding="utf-8") as handle:
            payload = json.load(handle)
    else:
        payload = {}
    payload = _deep_merge(payload, updates)
    return write_run_metadata(output_dir, payload)


def append_run_registry(payload: Dict[str, Any]) -> Path:
    registry_path = Path.cwd() / "workplace_paper" / "run_registry.jsonl"
    registry_path.parent.mkdir(parents=True, exist_ok=True)
    with registry_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=True) + "\n")
    return registry_path


def resolve_run_metadata_path(
    instance_id: str,
    task_level: str,
    model_name: str,
    workplace_name: str = "workplace",
) -> Path:
    if task_level == "task2" and instance_id and not instance_id.endswith("_idea"):
        instance_id = f"{instance_id}_idea"
    model_safe = model_name.replace("/", "__").replace(":", "__")
    local_root = Path.cwd() / "workplace_paper" / f"task_{instance_id}_{model_safe}" / workplace_name
    return local_root / "run_metadata.json"
