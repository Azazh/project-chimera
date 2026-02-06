# Project Chimera Governance (The Codebase Law)

This document defines binding engineering rules and agent instructions that apply across all contributors and automated agents. It encodes Spec-First discipline, mandatory TDD, and financial safety under a CFO Sub-Agent.

## Agent Instructions
- **Spec-First**: Never write, generate, or commit code that violates any file under `specs/`. Contracts (JSON Schema), policies, and interfaces are the source of truth.
- **Contract Enforcement**: All external actions (Twitter, MoltBook, Coinbase, Midjourney) must be invoked via MCP adapters that enforce Attestation Headers and JSON Schema IO contracts.
- **Idempotency & OCC**: Side-effectful actions (posts, payments) require idempotency keys. All state mutations must use Optimistic Concurrency Control (versioned updates).
- **Traceability**: Every task must carry a `trace_id`; tool calls must emit telemetry sufficient for audit.

## Rules of Development
- **TDD Mandatory**: New features must have a failing test in `tests/` before implementation. Tests define the goalposts; code changes are not permitted without matching tests.
- **Spec-First Rule**: "Never write code that violates a file in `/specs`." If a spec gap exists, update `specs/` and commit that change before any code.
- **Review Gates**: Governance changes (policy, persona SOUL.md) must be versioned and attested; CI must pass security and quality gates before merge.

## Financial Safety (CFO Sub-Agent)
- **CFO Gate**: All wallet operations (transfer, payment, balance checks) must be routed through the CFO Sub-Agent as Judge.
- **Bounded Intents**: Commerce calls must include slippage tolerance (bps), spend caps, whitelists/blacklists, and time-in-force.
- **Audit & Reconciliation**: The CFO Judge must produce an audit trail (intent, constraints, execution result) and reconcile against accounting models.

## Governance Interception
- **Judge Middleware**: The Judge Agent intercepts low-compliance tasks before Worker execution and audits side-effectful results after execution.
- **Persona & Safety**: The Judge enforces persona alignment and safety rules (prompt-injection detection, prohibited content checks). Outputs must include status, score, and remediation deltas.

## CI/CD Requirements
- **Fail Fast**: The pipeline fails if tests or security scans fail, blocking corrupted code from reaching `main`.
- **Non-Root Runtime**: Containers must run as non-root users. Secrets are injected via environment variables; no hardcoded secrets.

## Change Management
- **Commit Messages**: Use descriptive commit messages that reference specs and tests affected.
- **Versioning**: Policies and specs are versioned; changes require attestation and communication to affected agents.

## References
- `specs/technical.md`: Task Manifest, JSON-RPC/MCP envelopes, OCC, Attestations.
- `specs/functional.md`: Lifecycle and role behaviors.
- `tests/`: Judge gating, OCC consistency, deterministic dispatch.
