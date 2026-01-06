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

    prompt_snapshot = payload.get("execution", {}).get("prompt_snapshot_path")
    if prompt_snapshot:
        _safe_copy(prompt_snapshot, bundle_dir)

    log_path = payload.get("execution", {}).get("log_path")
    if log_path:
        _safe_copy(log_path, bundle_dir)

    registry_path = Path.cwd() / "workplace_paper" / "run_registry.jsonl"
    _safe_copy(registry_path, bundle_dir)

    return bundle_dir
