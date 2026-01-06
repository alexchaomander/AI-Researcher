import json
import os
from pathlib import Path
from typing import Iterable, List, Dict, Any


REQUIRED_INSTANCE_KEYS = {
    "target",
    "instance_id",
    "authors",
    "year",
    "url",
    "abstract",
    "source_papers",
    "task1",
    "task2",
}

REQUIRED_SOURCE_PAPER_KEYS = {"reference", "rank", "type", "justification", "usage"}


def _ensure_non_empty(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (list, tuple, dict)):
        return bool(value)
    return True


def validate_benchmark_instance_payload(payload: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    missing = REQUIRED_INSTANCE_KEYS - payload.keys()
    if missing:
        errors.append(f"missing keys: {sorted(missing)}")

    source_papers = payload.get("source_papers")
    if not isinstance(source_papers, list) or not source_papers:
        errors.append("source_papers must be a non-empty list")
    else:
        for idx, paper in enumerate(source_papers):
            if not isinstance(paper, dict):
                errors.append(f"source_papers[{idx}] must be an object")
                continue
            paper_missing = REQUIRED_SOURCE_PAPER_KEYS - paper.keys()
            if paper_missing:
                errors.append(
                    f"source_papers[{idx}] missing keys: {sorted(paper_missing)}"
                )

    if not _ensure_non_empty(payload.get("task1")):
        errors.append("task1 must be non-empty")
    if not _ensure_non_empty(payload.get("task2")):
        errors.append("task2 must be non-empty")
    return errors


def load_and_validate_instance(instance_path: str | Path) -> Dict[str, Any]:
    path = Path(instance_path)
    if not path.exists():
        raise FileNotFoundError(f"Instance not found: {path}")
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    errors = validate_benchmark_instance_payload(payload)
    if errors:
        raise ValueError(f"Invalid benchmark instance {path}: {errors}")
    return payload


def validate_prepare_agent_output(payload: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    paper_list = payload.get("reference_papers")
    if not isinstance(paper_list, list) or not paper_list:
        errors.append("reference_papers must be a non-empty list")
    else:
        for idx, paper in enumerate(paper_list):
            if not isinstance(paper, str) or not paper.strip():
                errors.append(f"reference_papers[{idx}] must be a non-empty string")
    return errors


def validate_non_empty_agent_output(agent_name: str, content: Any) -> List[str]:
    errors: List[str] = []
    if not _ensure_non_empty(content):
        errors.append(f"{agent_name} output must be non-empty")
    return errors


def _extract_json_objects(text: str) -> List[Dict[str, Any]]:
    objects: List[Dict[str, Any]] = []
    if not text:
        return objects
    stack = []
    start = None
    for idx, char in enumerate(text):
        if char == "{":
            if not stack:
                start = idx
            stack.append(char)
        elif char == "}":
            if stack:
                stack.pop()
                if not stack and start is not None:
                    blob = text[start:idx + 1]
                    try:
                        parsed = json.loads(blob)
                        if isinstance(parsed, dict):
                            objects.append(parsed)
                    except json.JSONDecodeError:
                        pass
                    start = None
    return objects


def validate_judge_output(content: Any) -> List[str]:
    errors: List[str] = []
    if not _ensure_non_empty(content):
        errors.append("Judge Agent output must be non-empty")
        return errors

    if not isinstance(content, str):
        return errors

    json_objects = _extract_json_objects(content)
    if not json_objects:
        return errors

    for obj in json_objects:
        if "fully_correct" in obj:
            fully_correct = obj.get("fully_correct")
            if fully_correct not in (True, False):
                errors.append("Judge Agent JSON fully_correct must be boolean")
            suggestion = obj.get("suggestion")
            if fully_correct is False:
                if suggestion is None or not isinstance(suggestion, dict) or not suggestion:
                    errors.append("Judge Agent JSON suggestion must be a non-empty object when fully_correct is false")
                else:
                    for key, value in suggestion.items():
                        if not _ensure_non_empty(key) or not _ensure_non_empty(value):
                            errors.append("Judge Agent JSON suggestion entries must be non-empty")
    return errors


def validate_plan_output(content: Any, strict: bool = False) -> List[str]:
    errors: List[str] = []
    if not _ensure_non_empty(content):
        errors.append("Plan Agent output must be non-empty")
        return errors
    if not isinstance(content, str):
        return errors
    objects = _extract_json_objects(content)
    plan_obj = None
    for obj in objects:
        if "dataset_plan" in obj and "training_plan" in obj and "testing_plan" in obj:
            plan_obj = obj
            break
    if strict and plan_obj is None:
        errors.append("Plan Agent output missing PLAN_JSON block")
        return errors
    if plan_obj is not None:
        required = {"dataset_plan", "model_plan", "training_plan", "testing_plan"}
        missing = required - plan_obj.keys()
        if missing:
            errors.append(f"Plan Agent JSON missing keys: {sorted(missing)}")
    return errors


def validate_ml_output(content: Any, strict: bool = False) -> List[str]:
    errors: List[str] = []
    if not _ensure_non_empty(content):
        errors.append("ML Agent output must be non-empty")
        return errors
    if not isinstance(content, str):
        return errors
    objects = _extract_json_objects(content)
    ml_obj = None
    for obj in objects:
        if "status" in obj and "summary" in obj:
            ml_obj = obj
            break
    if strict and ml_obj is None:
        errors.append("ML Agent output missing ML_JSON block")
        return errors
    if ml_obj is not None:
        if ml_obj.get("status") != "completed":
            errors.append("ML Agent JSON status must be 'completed'")
        if not _ensure_non_empty(ml_obj.get("summary")):
            errors.append("ML Agent JSON summary must be non-empty")
    return errors


def strict_agent_outputs_enabled() -> bool:
    return os.getenv("STRICT_AGENT_OUTPUTS", "false").lower() in {"1", "true", "yes", "on"}


def format_validation_errors(errors: Iterable[str]) -> str:
    return "; ".join(errors)
