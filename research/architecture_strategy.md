# Project Chimera: Architecture Strategy (Orchestrator Level)

This document elevates Project Chimera from descriptive planning to executable specifications that can be governed, tested, and extended by agents and humans.

## 1. Swarm Topology & FastRender Implementation

### Topology: Planner → Worker → Judge (Hierarchy)
- **Planner**: decomposes intents from `specs/functional.md` into granular tasks with explicit input/output contracts (JSON Schema), enqueues into **Task Queue**.
- **Worker**: executes tasks via **MCP Tool adapters** (e.g., `twitter.post`, `moltbook.publish`, `coinbase.payment`). Workers are stateless; all state mutations are mediated by queues and DB transactions.
- **Judge**: validates every Worker output against **spec contracts** and **policy rules** before the result can reach the **Task Queue** (for follow-on steps) or **Global State**. The Judge emits pass/fail, confidence score, and a remediation plan.

### FastRender Pattern
- **FastRender**: prioritized, low-latency render of candidate outputs followed by immediate **Judge gating**. If confidence ≥ threshold, the output flows forward; otherwise, the Planner receives a remediation delta (e.g., “missing source_refs”).
- Why this is better than a simple bot: **fragile prompts** are replaced by contract-first tasks and a **Judge** that enforces correctness and policy. Outputs cannot bypass validation, preventing silent drift.

### Optimistic Concurrency Control (OCC)
- **Global State** records a `version` per entity (e.g., `Campaign`, `Thread`, `Wallet`). Workers perform `UPDATE ... WHERE version = v` and set `version = v+1`. If the row was modified by another actor, the update fails and the task is retried with fresh state.
- **Ghost updates prevention**: OCC + idempotent task design (deterministic keys for posts/payments) avoids duplicate effects. All side-effectful actions carry **idempotency keys** and **attestations**.

## 2. Human-in-the-Loop (HITL) & Governance Schema

### Confidence Thresholds
- **Auto-Approve**: score > 0.9 → publish or execute automatically.
- **Async Review**: 0.7–0.9 → enqueue for human approval; proceed on approval, otherwise remediate.
- **Hard Reject**: < 0.7 → block, escalate to Planner with failure reasons.

### Governance Roles and CFO Sub-Agent
- **CFO Judge (Finance)**: acts as a specialized **Judge** for commerce-related actions using **Coinbase AgentKit** via MCP. Enforces spend limits, slippage caps, whitelists/blacklists, time-in-force, and proof-of-funds.
- **Policy Schema**: governance policies are versioned, signed, and attached as **Attestation Headers** to every commerce call. The CFO emits an audit trail (intent, constraints, result, reconciliation).
- Why this is better than a simple bot: all high-risk actions are gated by formal policy, scored by Judges, and traced with attestations. HITL triggers on ambiguous cases.

## 3. Data & Memory Persistence Strategy

### Hybrid Database
- **PostgreSQL**: transactional integrity for wallets, tasks, job runs, OCC versions, and audit logs. Strong consistency for financial and workflow state.
- **Weaviate**: semantic long-term memory (persona, backstory, prior content vectors, reputational signals). Enables recall, personalization, and planning over time.

### SOUL.md Hydration
- **SOUL.md**: the agent’s “DNA” (persona, constraints, brand tone, safety rules). At runtime, **Hydrator** loads SOUL.md, extracts structured fields (JSON frontmatter), and injects them into:
  - **Planner context**: task decomposition aligns with persona constraints.
  - **Worker prompts**: parameterized templates reference persona and safety.
  - **Judge rules**: validation includes persona alignment and safety compliance.
- Why this is better than a simple bot: identity and constraints are explicit, versioned, and applied uniformly to planning, execution, and governance.

## 4. Standardization via MCP (Decoupling & Stability)

- All external actions are **MCP Tools** (Twitter, Coinbase, MoltBook, Midjourney). The core logic calls abstract capabilities, not raw platform APIs.
- **Benefits**: decoupling from API volatility, uniform tracing, sandboxing, and capability-scoped tokens. Tool adapters carry **Attestation Headers** and enforce **spec contracts**.
- Why this is better than a simple bot: portability and resilience; platforms can change without breaking orchestration or governance.

## Strategic Trade-offs

- **Latency vs Quality (Judge)**: stricter validation improves safety but adds latency; mitigate via FastRender and parallel Judges for low-risk checks.
- **Throughput vs Consistency (OCC)**: OCC prevents conflicts but can increase retries; mitigate by fine-grained entities and backoff.
- **Abstraction vs Performance (MCP)**: tool indirection adds overhead; gain stability and auditability. Optimize with connection pooling and batched calls.
- **Recall vs Freshness (Weaviate)**: vector recall may surface old context; mitigate with recency weighting and persona constraints.

## Flow Diagram (Placeholder)

```mermaid
flowchart LR
  P[Planner] -->|Tasks| Q[Task Queue]
  Q --> W[Worker]
  W --> J[Judge]
  J -->|Approved| GS[Global State]
  J -->|Remediate| P
  GS --> P
```

---

## Agentic Orchestration & Routing Protocol

This section specifies the deterministic routing, capability-discovery, and governance interception patterns used by Project Chimera to ensure tasks reach the correct Worker without ghost updates or logic loops.

### Routing Topology: Hub-and-Spoke via OpenClaw Gateway
- **Gateway (Message Broker)**: OpenClaw acts as the central broker, receiving Planner task envelopes and dispatching them to the appropriate Worker queues.
- **Deterministic Dispatch**: Tasks are routed by capability tags and policy, not by ad-hoc prompts. The Gateway performs schema validation and attaches attestation headers.
- **Spokes (Workers)**: Specialized Worker agents subscribe to queues mapped to their skills (e.g., `trend_hunter`, `image_generator`, `wallet_manager`). Workers are stateless; state synchronization is mediated through queues and storage.

### Handoff Mechanism: JSON-RPC over MCP
- **Transport**: Planner wraps each task as a JSON-RPC 2.0 call over MCP (e.g., `skill.exec`). The envelope carries uniform telemetry and attestation.
- **Task Manifest (Metadata)**: Each task includes:
  - `skill_required`: string (matches entry in Skill Registry under `skills/`)
  - `priority`: enum [`LOW`, `NORMAL`, `HIGH`, `URGENT`]
  - `timeout_ms`: integer (max execution time)
  - `idempotency_key`: string (deduplication key to prevent duplicate side effects)
  - `trace_id`: string (end-to-end correlation)
  - `policy_version`: string (governance policy binding)

Example manifest (excerpt):

```json
{
  "jsonrpc": "2.0",
  "method": "skill.exec",
  "params": {
    "task_manifest": {
      "skill_required": "wallet_manager",
      "priority": "HIGH",
      "timeout_ms": 15000,
      "idempotency_key": "pay-20260205-abc123",
      "trace_id": "trace-7f2c",
      "policy_version": "finance.v1"
    },
    "input": { "action": "payment", "amount": 100, "currency": "USDC", "to_address": "0x..." }
  },
  "id": "rpc-001"
}
```

- **Capability-Discovery**: The Gateway matches `skill_required` against the **Skill Registry** (materialized from `skills/` directory contracts). If no exact match or schema mismatch is detected, the task is rejected with `SCHEMA_VIOLATION` rather than misrouted.

### Heartbeat & State Persistence
- **Heartbeat Loop**: The Gateway runs a heartbeat every X seconds (configurable, e.g., 5–15s) to poll `TASK_QUEUE` for:
  - `stale_assigned`: tasks assigned but not started within `grace_period_ms` → auto-unassign and requeue.
  - `stalled_running`: tasks running beyond `timeout_ms` → emit remediation event; Planner may re-plan.
- **State Synchronization**: Assignment and progress transitions are written atomically with OCC (`UPDATE ... WHERE version = v` → `v+1`). This prevents ghost updates when multiple dispatchers attempt changes.
- **Context Injection (Thread Hydration)**: On assignment, the Worker receives the full thread context (prior messages, persona SOUL.md constraints, policy bindings). This avoids forgetting the original goal and enables consistent behavior across retries.

### Governance Interception: Judge as Middleware
- **Pre-Execution Gate**: If the Planner’s preliminary `policy_compliance` score is below threshold, the Gateway routes the envelope through the **Judge Agent** before any Worker execution.
- **Middleware Contract**: The Judge validates persona alignment, safety (prompt injection, prohibited content), and policy adherence (e.g., finance slippage caps). Outputs include `status` (`APPROVED`, `REMEDIATION`, `REJECTED`), `score`, and optional `remediation_delta` for the Planner.
- **Post-Execution Audit**: For side-effectful tasks (posts, payments), the Judge verifies outputs and reconciles against idempotency keys and attestations prior to committing global state.

### Sequence Flow (Mermaid)

```mermaid
sequenceDiagram
  participant U as User
  participant P as Planner
  participant G as OpenClaw Gateway
  participant W as Worker (Skill)
  participant J as Judge

  U->>P: Submit Intent (Spec-bound)
  P->>G: JSON-RPC/MCP (Task Manifest + Input)
  G->>J: Governance Interception (if low compliance)
  J-->>G: Decision (APPROVED/REMEDIATION/REJECTED)
  alt Approved
    G->>W: Deterministic Dispatch (skill_required)
    W-->>G: Result (with attestation)
    G->>J: Post-Execution Audit (if side-effectful)
    J-->>G: Audit OK
    G-->>P: Deliver Result
    P-->>U: Outcome
  else Remediation/Rejected
    G-->>P: Remediation Delta / Reject
    P-->>U: Guidance / Blocked
  end
```

This protocol eliminates ad-hoc routing and logic loops by binding every dispatch to explicit capabilities, centralized governance interception, and OCC-backed state transitions. Duplicate or conflicting requests are neutralized via idempotency keys and deterministic envelopes, ensuring reliable multi-agent orchestration.

### Implementation Notes (pointers to specs/tests)
- Define contracts in `specs/technical.md` (JSON Schema; IO for Planner/Worker/Judge).
- Add failing tests in `tests/` to assert Judge gating and OCC semantics before implementation.
- Configure MCP tool adapters for Twitter, MoltBook, Coinbase, and Midjourney with attestation and idempotency.
