# Acceptance Criteria — Agentic Orchestrator

Formal pass conditions for Planner, Gateway, Workers, and Judge to ensure consistent outcomes and reviewer clarity.

## Planner
- Task Manifest includes: `skill_required`, `priority`, `timeout_ms`, `idempotency_key`, `trace_id`, `policy_version`.
- Acceptance Criteria attached per task with measurable thresholds (e.g., trend min_volume >= N, sentiment mix, image aspect ratio, finance slippage_bps <= policy).

## Gateway (OpenClaw)
- Deterministic dispatch: `skill_required` resolves to Skill Registry entry; unknown skill → DispatchError.
- Heartbeat detects stale_assigned and stalled_running; OCC enforced on assignment transitions.
- Context injection delivers full thread (persona and policy).

## Workers
- Strict IO contract validation against skill schemas; SCHEMA_VIOLATION on mismatches.
- Idempotent execution: identical inputs return identical outputs or references.

## Judge
- Pre-execution: block or remediate if compliance score < thresholds.
- Post-execution audit for side-effectful tasks; reject if attestations or idempotency mismatch.

## Finance (CFO)
- Enforce network and time_in_force.
- Slippage within bounds; spend within cap; whitelist enforced when required.

## Evidence
- Tests in `tests/` must assert OCC, governance, and routing.
- CI must fail on lint/test/security violations.
