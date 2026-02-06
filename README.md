# Project Chimera

Autonomous Influencer Network — Spec-Driven, Agentic Orchestration with Governance.

Project Chimera operationalizes a Planner–Worker–Judge swarm over the OpenClaw Gateway, executing capabilities via MCP Tools (MoltBook, Twitter, Coinbase AgentKit, image generation) with strict contracts, OCC consistency, and audit-grade governance.

**Ethiopian Analogies (to clarify architecture):**
- **Merkato Teff Bag (OCC):** In Addis Ababa’s Merkato, a shopkeeper counts and seals teff bags. If two buyers try to change the same bag at once, the second one is rejected until the first seal is registered. Our Optimistic Concurrency Control does the same: each entity carries a version; updates require the current version; conflicts are retried with fresh state. This prevents “ghost updates” and double-spending.
- **Buna Ceremony (Governance & Judge):** Like a coffee ceremony with roles and etiquette, the Judge enforces persona tone, safety, and policy before the “pour” (publish/execute). Only approved brews flow; misaligned flavors trigger remediation.
- **Minibus Hub (Routing):** Taxis depart from a central hub to specific destinations. The OpenClaw Gateway is that hub, doing deterministic dispatch by capability tag (`skill_required`) to the correct worker line.

**High-Level Architecture**
- **Planner:** Decomposes intent into JSON Schema–bound tasks and enqueues them with a Task Manifest (skill, priority, timeout, idempotency, trace).
- **OpenClaw Gateway:** Hub-and-spoke message broker. Performs capability-discovery, schema validation, governance interception (Judge), context injection, and deterministic dispatch to workers.
- **Workers (Skills):** Specialized executors (trend hunting, image generation, wallet ops) that call external platforms via MCP adapters with Attestation Headers.
- **Judge:** Middleware for pre-execution policy compliance and post-execution audit. Emits status (`APPROVED`, `REMEDIATION`, `REJECTED`), score, and remediation deltas.
- **Data:** PostgreSQL for workflow/audit/OCC; Weaviate for semantic persona memory.

See the routing protocol details in [research/architecture_strategy.md](research/architecture_strategy.md) and Task Manifest schema in [specs/technical.md](specs/technical.md).

**Skills (Contracts)**
- [skills/trend_hunter/README.md](skills/trend_hunter/README.md): Search-based trend discovery with volume/sentiment outputs.
- [skills/image_generator/README.md](skills/image_generator/README.md): Image generation with aspect ratio enums and model selection.
- [skills/wallet_manager/README.md](skills/wallet_manager/README.md): Coinbase AgentKit operations with slippage tolerance (bps) and idempotency.

**Specs & Tests (Goalposts)**
- Specs: [specs/functional.md](specs/functional.md), [specs/technical.md](specs/technical.md), [specs/_meta.md](specs/_meta.md).
- Tests (ready-to-fail TDD):
  - Judge governance: [tests/test_judge_logic.py](tests/test_judge_logic.py).
  - OCC consistency (“Merkato teff bag”): [tests/test_occ_consistency.py](tests/test_occ_consistency.py).
  - Deterministic routing: [tests/test_routing_dispatch.py](tests/test_routing_dispatch.py).

**Governance**
- Codebase Law: [GOVERNANCE.md](GOVERNANCE.md) enforces Spec-First, mandatory TDD, CFO-gated finance, idempotency, and OCC.
- CFO Sub-Agent: Validates spend caps, slippage, whitelists, and attests financial calls before committing state.
 - Agent Rules: [SOUL.md](SOUL.md) formalizes persona, thresholds, and role-specific instructions.

**CI/CD (Customs Inspector)**
- GitHub Actions: Security Scan (gitleaks, pip-audit) and Quality Gate (ruff + pytest coverage). Pipeline fails on lint/test errors to block corrupted merges.
- Workflow: [.github/workflows/main.yml](.github/workflows/main.yml).

**Addressing 10x Rubric Gaps**
- Frontend: Minimal examiner dashboard in [frontend/](frontend/) with `make ui` to serve locally at http://localhost:8080.
- Concrete MCP Config: Expanded entries in [.vscode/mcp.json](.vscode/mcp.json) and documentation in [docs/mcp_config.md](docs/mcp_config.md) with environment-driven auth headers.
- Agent Rules File: Runtime rules codified in [SOUL.md](SOUL.md) with persona, thresholds, and CFO safety constraints for hydration.
 - Acceptance Criteria: Formalized in [docs/acceptance_criteria.md](docs/acceptance_criteria.md) and referenced by Planner/Judge.
 - Frontend Security: `make ui-secure` serves the dashboard with basic security headers.

**Quick Start**
- Python venv:
```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
make setup
```
- Run checks:
```bash
make lint
make test
```
- Build container:
```bash
make build
```

- Serve frontend:
```bash
make ui
```

**Docker (Secure Factory)**
- Multi-stage build with non-root `appuser`, orchestrator deps, and env placeholders.
- See [Dockerfile](Dockerfile).

**Folder Map**
- research/: strategy and synthesis (routing, governance, memory, diagrams).
- specs/: functional and technical contracts (IO schemas, OCC, envelopes).
- skills/: skill folders with README contracts.
- tests/: TDD goalposts (Judge, OCC, Routing).
- .github/workflows/: CI pipeline.
- ide-chat-history/: daily conversation summaries for traceability.

**Why Chimera is better than a simple bot**
- Contract-first tasks with JSON Schema and attestation replace fragile prompts.
- Deterministic dispatch via Gateway avoids loops and miscues.
- Judge gating + OCC prevent ghost updates, unsafe outputs, and double effects.
- Hybrid memory blends persona recall with transactional integrity.

**References**
- a16z: The Trillion Dollar AI Code Stack.
- OpenClaw runtime/router concepts.
- MoltBook social substrate analysis.
- Local SRS: see [research/](research/).

**Public Report**
- https://docs.google.com/document/d/1ANX4qwCp80fx3_cPv04Yg3916gFh3t3cracAG-a6hp8/edit?usp=sharing
