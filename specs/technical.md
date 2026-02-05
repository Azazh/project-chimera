# Project Chimera Technical Specification

Version: 1.0.0

## API Schemas

### TaskObject (JSON Schema)
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://chimera/specs/taskobject.schema.json",
  "title": "TaskObject",
  "type": "object",
  "additionalProperties": false,
  "properties": {
    "id": { "type": "string", "format": "uuid" },
    "agent_role": { "type": "string", "enum": ["PLANNER", "WORKER", "JUDGE"] },
    "payload": { "type": "object" },
    "deadline": { "type": "string", "format": "date-time" },
    "priority": { "type": "integer", "minimum": 0, "maximum": 10 },
    "version": { "type": "integer", "minimum": 0 }
  },
  "required": ["id", "agent_role", "payload", "deadline", "priority", "version"]
}
```

### JudgeReport (JSON Schema)
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://chimera/specs/judgereport.schema.json",
  "title": "JudgeReport",
  "type": "object",
  "additionalProperties": false,
  "properties": {
    "score": { "type": "number", "minimum": 0, "maximum": 1 },
    "feedback_delta": { "type": "object" },
    "status": { "type": "string", "enum": ["APPROVED", "REJECTED"] },
    "task_id": { "type": "string", "format": "uuid" },
    "policy_version": { "type": "string" },
    "persona_version": { "type": "string" }
  },
  "required": ["score", "feedback_delta", "status", "task_id", "policy_version", "persona_version"]
}
```

## Database ERD (Mermaid)
```mermaid
erDiagram
  Campaigns ||--o{ Threads : contains
  Threads ||--o{ Posts : includes
  Wallets ||--o{ Transactions : records
  Wallets ||--o{ GasTracking : tracks
  Posts ||--o{ WeaviateVectors : embeds

  Campaigns {
    uuid id PK
    string name
    int version
    datetime created_at
  }
  Threads {
    uuid id PK
    uuid campaign_id FK
    string topic
    int version
    datetime created_at
  }
  Posts {
    uuid id PK
    uuid thread_id FK
    string platform  
    string content_hash
    int version
    datetime created_at
  }
  Wallets {
    uuid id PK
    string provider
    string account_ref
    int version
    datetime created_at
  }
  Transactions {
    uuid id PK
    uuid wallet_id FK
    string type
    numeric amount
    string currency
    numeric slippage_bps
    datetime created_at
  }
  GasTracking {
    uuid id PK
    uuid wallet_id FK
    numeric gas_units
    numeric gas_cost
    datetime created_at
  }
  WeaviateVectors {
    uuid pg_uuid PK
    string weaviate_id
    string embedding_ref
    datetime created_at
  }
```

## OpenClaw Communication Protocols

### JSON-RPC over MCP
- Transport: JSON-RPC 2.0 messages carried via MCP tool adapters.
- Required Attestation Headers on every call:
  - `DID`: decentralized identifier of the agent.
  - `Policy_Version`: version string of active governance policy.
  - `Signature`: cryptographic signature over `{method, params, ts}`.
- Standard fields:
  - `id`: unique request id (UUID).
  - `jsonrpc`: "2.0".
  - `method`: e.g., `moltbk.post.create`, `presence.heartbeat`, `commerce.payment.create`.
  - `params`: strictly typed per JSON Schema (referenced by version hash).
  - `ts`: ISO datetime.

Example (create post):
```json
{
  "id": "8f7d2c3a-1b7e-4f0a-9a1a-123456789abc",
  "jsonrpc": "2.0",
  "method": "moltbk.post.create",
  "params": {
    "thread_id": "c2f1b7e2-3af9-4c4b-8c5b-abcdef123456",
    "text": "Trend insight:...",
    "semantics": { "topic_id": "T-42", "stance": "NEUTRAL", "source_refs": ["..."], "risk_flags": [] }
  },
  "ts": "2026-02-05T10:00:00Z",
  "headers": { "DID": "did:key:z...", "Policy_Version": "1.0.0", "Signature": "MEUCIQ..." }
}
```

### Presence & Memory
- `presence.heartbeat` broadcasts status (`idle`, `researching`, `publishing`) and load hints.
- Local memory: OpenClaw short-horizon state; long-term memory via storage MCP (Weaviate/SQL) keyed by UUIDs.

## Consistency Logic (OCC)
- Every mutable entity includes `version`.
- Update pattern: `UPDATE table SET ... , version = version + 1 WHERE id = :id AND version = :version`.
- On conflict: Worker retries with fresh state from Global State; Planner may re-issue task with updated `version`.
- Side effects: All external posts/payments carry **idempotency keys** derived from `{entity_id, version, method}`.

## Cross-References
- See specs/functional.md for lifecycle and role behaviors.
- See specs/_meta.md for versioning and health.
