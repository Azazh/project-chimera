# Project Chimera Functional Specification (Planner → Worker → Judge)

Version: 1.0.0

## Roles & User Stories

### Planner
- As the Planner, I transform the high-level SOUL intent into a typed task graph so that Workers can execute deterministically.
- Acceptance:
  - Inputs: SOUL.md (persona, constraints), specs/technical.md contract references.
  - Outputs: `TaskObject` instances (see technical.md) enqueued with deadlines and priorities.

### Worker
- As a Worker, I execute MCP Tools (Twitter, MoltBook, Coinbase) using strictly typed inputs and produce structured outputs.
- Acceptance:
  - Inputs: `TaskObject` payloads validated against JSON Schemas.
  - Execution: Calls via JSON-RPC over MCP with Attestation Headers.
  - Outputs: Structured results intended for Judge validation.

### Judge
- As the Judge, I evaluate Worker outputs against safety policies and persona constraints and emit a `JudgeReport`.
- Acceptance:
  - Inputs: Worker outputs + policy context (safety, persona, platform rules).
  - Outputs: `JudgeReport` with score, feedback_delta, status (APPROVED/REJECTED).
  - Routing: APPROVED → publish/state update; REJECTED → remediation to Planner.

## FastRender Lifecycle

1. Planner decomposes intent into `TaskObject` and enqueues (deadline/priority).
2. Worker performs a low-latency render (FastRender) to produce a candidate output.
3. Judge validates candidate against contracts and policies:
   - If score > threshold (see HITL in architecture_strategy.md), status = APPROVED.
   - Else status = REJECTED with `feedback_delta` to remediate.
4. APPROVED flows to publish/state update via MCP tool; REJECTED routes back to Planner with a delta to refine the task.
5. OCC ensures state writes succeed only if the current `version` matches; otherwise tasks are retried.

## Cross-References
- See specs/technical.md for JSON Schemas and protocol details.
- See research/architecture_strategy.md for Judge thresholds and OCC.
