# Project Chimera

Autonomous Influencer Factory — Spec-driven, agentic infrastructure.

This repository follows the 3-day challenge guidance. For Feb 4, the focus is:
- Deep research and notes
- Architecture strategy (agent pattern, HITL safety, data store)
- Golden environment setup: initialize git, configure Python (uv), and document MCP Sense connection

## Quick Start (Feb 4)

1. Install uv (Linux):
   - https://astral.sh/uv/ (or run the installer below)

```bash
curl -Ls https://astral.sh/uv/install.sh | sh
```

2. Create a virtual environment and activate:
```bash
uv venv
source .venv/bin/activate
```

3. Verify Python and uv:
```bash
python --version
uv --version
```

4. Fill in research and architecture docs under `research/`.
5. Connect Tenx MCP Sense to your IDE; paste a connection log into `docs/mcp_sense_connection_log.md`.

## repo layout (Feb 4 scope)
- `research/reading_notes.md`: Summaries and answers from the required reading.
- `research/architecture_strategy.md`: Agent pattern, HITL safety, DB choice, optional Mermaid diagrams.
- `docs/mcp_sense_connection_log.md`: Confirmation of IDE <-> MCP Sense connection.
- `pyproject.toml`: Python project metadata and version requirements.
- `.gitignore`: Python defaults.

## Submission (Feb 4)
- Publish a Google Drive link to a report that includes:
  - Research Summary (a16z, OpenClaw, MoltBook, SRS)
  - Architectural Approach (pattern + infra decisions)

## Notes
- Follow Spec-Driven Development: Never implement features before specs are ratified.
- Keep Tenx MCP Sense connected to your IDE for traceability.
