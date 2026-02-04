# Project Chimera: Strategic Research Summary

## Section 1: Synthesis of Ecosystems

### OpenClaw as the Body (Runtime) and MoltBook as the Stage (Social Field)
- OpenClaw provides an **agent runtime/router with Heartbeat** and **local memory**, enabling persistent, proactive operation rather than request/response scripts. Why this makes Chimera better than a simple bot: a simple bot reacts statically; Heartbeat + memory allows Chimera to self-schedule research, content ideation, and engagement loops with continuity across sessions.
- MoltBook functions as a **social substrate (“Reddit for Bots”)** where agents create posts, join sub-communities (“sub-molts”), and interact with other agents. Why this makes Chimera better than a simple bot: Chimera participates in multi-agent ecosystems where discovery, virality, and feedback loops emerge from agent-to-agent dynamics, not only human prompts.
- a16z’s thesis on **“Agents with Environments”** and the shift from **Repos → Semantic Intent** aligns with Chimera’s SDD approach: the repository encodes executable specs, contracts, and governance, while the runtime (OpenClaw) executes behaviors derived from those specs against an environment (MoltBook + skills). Why this makes Chimera better than a simple bot: intent is governed by specs and enforced by infrastructure, reducing drift and hallucination.
- The Project Chimera SRS mandates **Swarm Architecture**, **MCP standard connectivity**, and **Coinbase AgentKit commerce**. OpenClaw is the swarm coordinator; MCP provides uniform tool connectivity; Coinbase AgentKit enables safe, governed financial operations. Why this makes Chimera better than a simple bot: capabilities are modular, verifiable, and auditable across compute, social, and finance layers.

## Section 2: The Social Protocol (Technical Design)

### Messaging Model and Transport
- Protocol: **JSON-RPC over MCP** with a well-defined method registry (e.g., `moltbk.post.create`, `moltbk.comment.create`, `moltbk.thread.subscribe`, `presence.heartbeat`, `social.attach-proof`). Why this makes Chimera better than a simple bot: a typed, versioned interface prevents brittle prompt scraping and ensures interoperable behaviors across agents and runtimes.
- Envelope: messages include `id`, `method`, `params`, `ts`, and **Attestation Headers**. Attestations carry cryptographic proofs of identity/policy (e.g., key-bound DID, policy hash, spec version) and optional **capability tokens** for scope-limited actions (e.g., posting vs. commerce). Why this makes Chimera better than a simple bot: identity and policy are first-class, enabling trust, rate limits, and governance at the protocol layer.

### Semantic Interoperability
- All payloads conform to **machine-readable schemas** (JSON Schema) for topics, posts, comments, and reputational signals; schemas are versioned and pinned by content-addressed hashes. Why this makes Chimera better than a simple bot: structured semantics allow validation, indexing, analytics, and safe automated transformations by other agents.
- Content fields support dual-mode: `text` (LLM-friendly) and `semantics` (structured fields such as `topic_id`, `stance`, `source_refs`, `risk_flags`). Why this makes Chimera better than a simple bot: agents can reason over intent and provenance, not only tokens.

### Presence, Memory, and Context
- Presence: **Heartbeat** broadcasts (`presence.heartbeat`) with status (`idle`, `researching`, `publishing`) and load hints. Why this makes Chimera better than a simple bot: other agents can coordinate with Chimera’s availability, enabling true swarm behaviors.
- Memory: OpenClaw local memory stores short-horizon dialog state; long-term memory persists via MCP storage servers (e.g., vector or SQL). Why this makes Chimera better than a simple bot: stateful context lets Chimera sustain campaigns and adapt across threads and time.

### Commerce Hooks (SRS: Coinbase AgentKit)
- Commerce methods are exposed via **MCP skill adapters** to Coinbase AgentKit (e.g., `commerce.payment.create`, `commerce.tip.send`). All calls carry Attestation Headers and policy claims (spend limits, whitelists). Why this makes Chimera better than a simple bot: economic actions are gated by explicit capabilities, rate-limited, and audited.

## Section 3: Strategic Risks (and Mitigations)

### Risk 1: Indirect Prompt Injection via MoltBook Threads
- Vector: hostile agents publish content with embedded instructions, data exfiltration bait, or model-targeted perturbations. Why this makes Chimera better than a simple bot: Chimera employs a **spec-first content interpreter** that parses MoltBook objects via schema, strips free-text directives from untrusted sources, and routes only the allowed fields to LLM tools; untrusted text is sandboxed and scored by a safety classifier. Mitigations: schema validation, allowlist method routing, content sandboxing, provenance scoring, and adjudication via Human-in-the-Loop for elevated-risk actions.

### Risk 2: Economic Slippage in Agentic Commerce
- Vector: price movement between quote and execution, hostile front-running, or erroneous repeated retries in volatile markets. Why this makes Chimera better than a simple bot: commerce calls are wrapped with **bounded intents** (max slippage bps, time-in-force, amount caps) enforced by the Coinbase AgentKit adapter. Mitigations: pre-trade risk checks, on-chain or exchange attestation of fills, replay protection nonces, and post-trade reconciliation against the spec’s accounting model.

## Section 4: a16z Implications — Software Disrupting Itself

### Agents with Environments, from Repos to Semantic Intent
- The repo codifies **executable specs** (contracts, schemas, policies), while OpenClaw executes against a live social environment (MoltBook). Why this makes Chimera better than a simple bot: implementation is generated or orchestrated from intent; tests and governance enforce behavior, enabling rapid, safe iteration.
- **Agent-specific runtimes**: OpenClaw provides scheduling, memory, and routing as platform primitives instead of ad-hoc scripts. Why this makes Chimera better than a simple bot: reliability, composability, and multi-agent coordination become defaults rather than bespoke.

### SDD and Governance as Competitive Moat
- SDD ensures the spec is the source of truth; MCP provides **traceable tool calls**, and CI/CD enforces contracts. Why this makes Chimera better than a simple bot: fewer regressions, reduced hallucination surface, and better parallelization by human and AI contributors.

---

### Appendix: Implementation Pointers (from SRS and today’s scope)
- **Swarm Architecture**: orchestrator-worker topology in OpenClaw; workers implement skills via MCP. Spec to define roles, queues, and backoff policies.
- **MCP Connectivity**: filesystem, git, storage/vector, Coinbase AgentKit adapters; all calls signed and logged; rules forbid direct free-form execution without spec match.
- **MoltBook Schema Draft**: `Post`, `Comment`, `Thread`, `Reaction`, `Topic`, with JSON Schema and content hashes for immutable referencing.
