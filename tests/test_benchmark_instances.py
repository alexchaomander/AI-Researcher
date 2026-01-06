import json
from pathlib import Path


REQUIRED_KEYS = {
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


def _load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def test_benchmark_instances_have_required_fields():
    root = Path(__file__).resolve().parent.parent
    instances = list((root / "benchmark" / "final").rglob("*.json"))
    assert instances, "No benchmark instances found under benchmark/final"

    for instance_path in instances:
        payload = _load_json(instance_path)
        missing = REQUIRED_KEYS - payload.keys()
        assert not missing, f"{instance_path} missing keys: {sorted(missing)}"

        assert isinstance(payload["source_papers"], list), f"{instance_path} source_papers must be a list"
        assert payload["source_papers"], f"{instance_path} source_papers must not be empty"
        for paper in payload["source_papers"]:
            missing_paper = REQUIRED_SOURCE_PAPER_KEYS - paper.keys()
            assert not missing_paper, (
                f"{instance_path} source_paper missing keys: {sorted(missing_paper)}"
            )

        assert str(payload["task1"]).strip(), f"{instance_path} task1 must not be empty"
        assert str(payload["task2"]).strip(), f"{instance_path} task2 must not be empty"
