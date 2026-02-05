# Project Chimera Specs Index & Health Dashboard

## System Mandate (Mission Statement)
Build an autonomous influencer network governed by Spec-Driven Development (SDD), operating on an OpenClaw runtime with MoltBook as the social environment and Coinbase AgentKit for agentic commerce. Reliability, safety, and traceability are enforced via Planner → Worker → Judge, Optimistic Concurrency Control (OCC), and MCP-standardized tools.

## Document Index
- specs/_meta.md (this file): Index, mandate, versioning policy, health.
- specs/functional.md: User stories (Planner, Worker, Judge) and FastRender lifecycle.
- specs/technical.md: API schemas (TaskObject, JudgeReport), DB ERD (Mermaid), OpenClaw JSON-RPC over MCP, OCC.
- Optional: specs/openclaw_integration.md: Availability/Status publishing plan to OpenClaw network and MoltBook.

## Sub-Spec Status
- specs/_meta.md: Ratified
- specs/functional.md: Ratified
- specs/technical.md: Ratified
- specs/openclaw_integration.md: Draft (optional)

## Version Control Policy
- Semantic versions for specs: MAJOR.MINOR.PATCH (e.g., 1.0.0).
- Changes:
  - Patch: editorial or clarifications, no contract change.
  - Minor: additive fields or optional behaviors, backward compatible.
  - Major: breaking changes to schemas, protocol, or governance.
- Every spec change MUST:
  - Update the version at the top of the touched spec.
  - Include a rationale note and migration guidance.
  - Be linked to commits and CI checks; Judges should verify new versions before approving runtime changes.

## Project Health Dashboard
- Spec Fidelity: Executable schemas present; contracts versioned; OCC defined.
- Tooling & Skills: Dev MCP vs Runtime Skills separated; adapters carry attestation.
- Testing Strategy: Failing tests (to be added under tests/) before implementation.
- CI/CD & Governance: Docker + Make + Actions target "test"; Code review policy enforces Spec Alignment.
- MCP Sense Telemetry: Connection evidence tracked in docs/mcp_sense_connection_log.md.
