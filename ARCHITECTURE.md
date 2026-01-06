# AI-Researcher Architecture

This document summarizes the major components and the end-to-end execution flow.

## Core Components
- **CLI entrypoint**: `research_agent/cli.py`
- **Web UI**: `web_ai_researcher.py`
- **Run dispatcher**: `main_ai_researcher.py`
- **Orchestration**: `research_agent/inno/core.py` (MetaChain)
- **Agents**: `research_agent/inno/agents/inno_agent/*.py`
- **Tools**: `research_agent/inno/tools/*`
- **Environments**: `research_agent/inno/environment/*`
- **Paper generation**: `paper_agent/*`
- **Benchmark tasks**: `benchmark/final/*/*.json`

## End-to-End Flow
1. **Task selection**
   - CLI/Web picks a benchmark instance JSON and task level.
2. **Preparation**
   - Prepare Agent locates and evaluates reference repositories.
3. **Survey and planning**
   - Survey/Idea agents generate notes or ideas.
   - Plan Agent converts notes into an implementation plan.
4. **Implementation**
   - ML Agent builds a self-contained project under `/workplace/project`.
5. **Evaluation and refinement**
   - Judge Agent evaluates the implementation.
   - ML Agent iterates on fixes if required.
6. **Experiments**
   - Exp Analyser proposes further experiments and analysis.
7. **Paper writing**
   - Paper agent composes LaTeX sections and compiles PDF.

## Data and Execution
- Docker sandbox is optional and controlled by `USE_DOCKER`.
- `setup_dataset` copies dataset scaffolding into the workspace.
- Metadata for runs is written to `run_metadata.json`.
