# Skill: wallet_manager

## Service Description
The `wallet_manager` skill enables Worker agents to perform on-chain transactions and manage wallets using the Coinbase AgentKit. It supports payments, transfers, and balance checks with strict policy enforcement.

**Business Value:**
- Automates secure, auditable crypto transactions for campaigns and payouts.
- Enforces risk controls (slippage, spend caps) and provides full traceability for compliance.

## Input Schema (JSON Schema)
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "WalletManagerInput",
  "type": "object",
  "properties": {
    "action": { "type": "string", "enum": ["transfer", "balance_check", "payment"], "description": "Type of wallet operation." },
    "amount": { "type": "number", "minimum": 0, "description": "Amount to transfer or pay (required for transfer/payment)." },
    "currency": { "type": "string", "pattern": "^[A-Z]{3,5}$", "description": "Currency code (e.g., BTC, ETH, USDC)." },
    "to_address": { "type": "string", "pattern": "^0x[a-fA-F0-9]{40}$", "description": "Destination wallet address (for transfer/payment)." },
    "slippage_tolerance_bps": { "type": "integer", "minimum": 0, "maximum": 1000, "description": "Max slippage in basis points (0-1000)." },
    "time_in_force": { "type": "string", "enum": ["IOC", "FOK", "GTD"], "description": "Execution policy: Immediate-Or-Cancel, Fill-Or-Kill, Good-Till-Date." },
    "network": { "type": "string", "enum": ["ethereum", "base", "polygon"], "description": "Blockchain network to use." },
    "whitelist_required": { "type": "boolean", "default": true, "description": "If true, destination must be whitelisted." },
    "idempotency_key": { "type": "string", "description": "Unique key for idempotency enforcement." }
  },
  "required": ["action", "currency", "idempotency_key"],
  "if": { "properties": { "action": { "const": "transfer" } } },
  "then": { "required": ["amount", "to_address"] },
  "additionalProperties": false
}
```

## Output Schema (JSON Schema)
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "WalletManagerOutput",
  "type": "object",
  "properties": {
    "status": { "type": "string", "enum": ["success", "failed", "pending"] },
    "tx_hash": { "type": "string", "description": "Transaction hash (if applicable)." },
    "balance": { "type": "number", "description": "Wallet balance (for balance_check)." },
    "currency": { "type": "string" },
    "timestamp": { "type": "string", "format": "date-time" },
    "network": { "type": "string" },
    "time_in_force": { "type": "string" },
    "error_code": { "type": "string" }
  },
  "required": ["status", "currency", "timestamp"],
  "additionalProperties": false
}
```

## Error Codes
| Code                  | Description                                 | Agent Handling                |
|-----------------------|---------------------------------------------|-------------------------------|
| INSUFFICIENT_FUNDS    | Not enough balance for transaction           | Halt, notify Planner          |
| RATE_LIMIT_EXCEEDED   | API rate limit hit                          | Retry with backoff            |
| SCHEMA_VIOLATION      | Input does not match schema                  | Halt, notify Planner          |
| SLIPPAGE_EXCEEDED     | Actual slippage > allowed tolerance          | Abort, log, notify CFO agent  |
| ADDRESS_INVALID       | Wallet address format invalid                | Return error, request fix     |
| TIF_VIOLATION         | Time-in-force cannot be honored              | Abort, retry with adjusted TIF|
| NETWORK_UNSUPPORTED   | Network not supported                        | Reject, request supported net |

## Idempotency Policy
- All requests must include a unique `idempotency_key`.
- Duplicate requests with the same key return the original result, preventing double spending or duplicate transactions.
 - Idempotency scope includes (`action`, `amount`, `currency`, `to_address`, `network`, `time_in_force`).