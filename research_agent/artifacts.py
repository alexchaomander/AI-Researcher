from __future__ import annotations

import json
import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import Optional


def _safe_copy(src: str | Path, dest_dir: Path) -> None:
    src_path = Path(src)
    if not src_path.exists():
        return
    dest_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src_path, dest_dir / src_path.name)


def _redact_env_line(line: str) -> str:
    if "=" not in line or line.lstrip().startswith("#"):
        return line
    key, value = line.split("=", 1)
    key_upper = key.strip().upper()
    if any(token in key_upper for token in ("KEY", "TOKEN", "SECRET", "PASSWORD")):
        return f"{key}=***REDACTED***\n"
    return line


def redact_env_file(source: Path, dest: Path) -> None:
    if not source.exists():
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    with source.open("r", encoding="utf-8") as handle, dest.open("w", encoding="utf-8") as out:
        for line in handle:
            out.write(_redact_env_line(line))


def build_run_summary(payload: dict) -> str:
    instance = payload.get("instance", {})
    execution = payload.get("execution", {})
    models = payload.get("models", {})
    dataset = payload.get("dataset_integrity", {})
    lines = [
        "# Run Summary",
        "",
        f"- Timestamp: {payload.get('timestamp')}",
        f"- Instance ID: {instance.get('id')}",
        f"- Target: {instance.get('target')}",
        f"- Task Level: {instance.get('task_level')}",
        f"- Category: {instance.get('category')}",
        f"- Model: {models.get('completion_model')}",
        f"- Dry Run: {execution.get('dry_run')}",
        f"- Log Path: {execution.get('log_path')}",
        f"- Prompt Snapshot: {execution.get('prompt_snapshot_path')}",
        "",
        "## Dataset Integrity",
        f"- Exists: {dataset.get('exists')}",
        f"- Files: {dataset.get('files')}",
        f"- Total Bytes: {dataset.get('total_bytes')}",
        f"- Has metaprompt.py: {dataset.get('has_metaprompt')}",
    ]
    return "\n".join(lines) + "\n"


def create_artifact_bundle(metadata_path: str | Path, output_dir: Optional[str | Path] = None) -> Path:
    metadata_path = Path(metadata_path)
    if not metadata_path.exists():
        raise FileNotFoundError(f"Metadata not found: {metadata_path}")

    with metadata_path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)

    base_dir = metadata_path.parent
    artifacts_dir = Path(output_dir) if output_dir else base_dir / "artifacts"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    bundle_dir = artifacts_dir / f"bundle_{timestamp}"
    bundle_dir.mkdir(parents=True, exist_ok=True)

    _safe_copy(metadata_path, bundle_dir)
    summary_path = bundle_dir / "run_summary.md"
    summary_path.write_text(build_run_summary(payload), encoding="utf-8")

    redact_env_file(Path.cwd() / ".env", bundle_dir / ".env.redacted")

    prompt_snapshot = payload.get("execution", {}).get("prompt_snapshot_path")
    if prompt_snapshot:
        _safe_copy(prompt_snapshot, bundle_dir)

    log_path = payload.get("execution", {}).get("log_path")
    if log_path:
        _safe_copy(log_path, bundle_dir)

    registry_path = Path.cwd() / "workplace_paper" / "run_registry.jsonl"
    _safe_copy(registry_path, bundle_dir)

    zip_base = artifacts_dir / f"bundle_{timestamp}"
    shutil.make_archive(str(zip_base), "zip", root_dir=bundle_dir)
    return zip_base.with_suffix(".zip")


def create_artifact_folder(metadata_path: str | Path, output_dir: Optional[str | Path] = None) -> Path:
    metadata_path = Path(metadata_path)
    if not metadata_path.exists():
        raise FileNotFoundError(f"Metadata not found: {metadata_path}")

    with metadata_path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)

    base_dir = metadata_path.parent
    artifacts_dir = Path(output_dir) if output_dir else base_dir / "artifacts"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    bundle_dir = artifacts_dir / f"bundle_{timestamp}"
    bundle_dir.mkdir(parents=True, exist_ok=True)

    _safe_copy(metadata_path, bundle_dir)
    summary_path = bundle_dir / "run_summary.md"
    summary_path.write_text(build_run_summary(payload), encoding="utf-8")

    redact_env_file(Path.cwd() / ".env", bundle_dir / ".env.redacted")

    prompt_snapshot = payload.get("execution", {}).get("prompt_snapshot_path")
    if prompt_snapshot:
        _safe_copy(prompt_snapshot, bundle_dir)

    log_path = payload.get("execution", {}).get("log_path")
    if log_path:
        _safe_copy(log_path, bundle_dir)

    registry_path = Path.cwd() / "workplace_paper" / "run_registry.jsonl"
    _safe_copy(registry_path, bundle_dir)

    return bundle_dir
