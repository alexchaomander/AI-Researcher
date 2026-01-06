# Agent IO Schemas

This document captures the expected input/output shapes for core agents so that
downstream steps can validate and fail fast.

## Prepare Agent (required JSON output)
### Output
```json
{
  "reference_codebases": ["repo/name", "..."],
  "reference_paths": ["/workplace/repo", "..."],
  "reference_papers": ["Paper Title", "..."]
}
```
Constraints:
- `reference_codebases`, `reference_paths`, `reference_papers` must be non-empty lists.
- Each entry must be a non-empty string.

## Survey Agent (free-text output)
### Output
- Long-form notes covering the idea, key methods, and references.

## Plan Agent (free-text output)
### Output
- Implementation plan with components, datasets, metrics, and steps.
- Should include a JSON block labeled `PLAN_JSON`:
```json
{
  "dataset_plan": "...",
  "model_plan": "...",
  "training_plan": "...",
  "testing_plan": "..."
}
```

## ML Agent (free-text output)
### Output
- Description of project implementation and how it satisfies the plan.
- Should include a JSON block labeled `ML_JSON`:
```json
{
  "status": "completed",
  "summary": "..."
}
```

## Judge Agent (free-text output with optional flags)
### Output
- Evaluation summary and actionable fixes.
- Optional JSON flag inside text:
```json
{"fully_correct": true}
```
- If `fully_correct` is `false`, include a `suggestion` object with non-empty keys/values.

## Strict Mode
- Set `STRICT_AGENT_OUTPUTS=true` to require the JSON blocks above.
