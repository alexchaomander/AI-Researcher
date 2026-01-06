# Plugin and Extension Guide

This guide describes how to add new agents, tools, and workflows.

## Add a New Tool
1. Implement the tool function in `research_agent/inno/tools/`.
2. Ensure the function signature is JSON-serializable.
3. If the tool needs the Docker env, wrap it with `with_env` when registering.

## Add a New Agent
1. Create a new agent factory in `research_agent/inno/agents/inno_agent/`.
2. Decorate with `@register_agent("get_your_agent")`.
3. Return an `Agent` with:
   - `name`
   - `model`
   - `instructions`
   - `functions`
4. Verify the agent is discoverable via `research_agent/inno/agents/__init__.py`.

## Add a New Workflow Step
1. Update `InnoFlow` in `research_agent/run_infer_plan.py` or
   `research_agent/run_infer_idea.py`.
2. Add an `AgentModule` or `ToolModule` to the flow.
3. Define input and output expectations in `AGENT_IO_SCHEMAS.md`.

## Add a New Benchmark Task
1. Create a JSON instance in `benchmark/final/<category>/`.
2. Validate it with `pytest tests/test_benchmark_instances.py`.
3. Preview it with `ai-researcher preview -c <category> -i <instance_id>`.
