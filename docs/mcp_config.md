# MCP Configuration (Concrete Setup)

This document describes the MCP endpoints used by Project Chimera and how to provide credentials via environment variables.

## VS Code MCP Config
- File: `.vscode/mcp.json`
- Servers included:
  - `tenxfeedbackanalytics`: Tenx feedback proxy
  - `moltbook`: MoltBook MCP adapter (`Authorization: Bearer ${MOLTBOOK_API_KEY}`)
  - `coinbase_agentkit`: Coinbase AgentKit MCP (`CB-API-KEY`, `CB-API-SECRET`, `CB-API-PASSPHRASE`)
  - `openai`: LLM access (`Authorization: Bearer ${OPENAI_API_KEY}`)
  - `weaviate`: Vector store endpoint (`X-Api-Key: ${WEAVIATE_API_KEY}`)
  - `twitter`: Social adapter (`Authorization: Bearer ${TWITTER_BEARER_TOKEN}`)

Provide the environment variables in your shell or CI before starting tools.

## Environment Variables (examples)
```bash
export MOLTBOOK_API_KEY=... 
export COINBASE_API_KEY=...
export COINBASE_API_SECRET=...
export COINBASE_API_PASSPHRASE=...
export OPENAI_API_KEY=...
export OPENAI_ORG=...
export WEAVIATE_ENDPOINT=http://localhost:8080
export WEAVIATE_API_KEY=...
export TWITTER_BEARER_TOKEN=...
export POLICY_VERSION=finance.v1
```

## Security Notes
- Never commit real secrets. Use `.env` in local dev and CI secrets in pipelines.
- All calls must include Attestation and Policy headers for traceability.
