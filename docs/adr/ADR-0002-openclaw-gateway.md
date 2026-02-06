# ADR-0002: OpenClaw Gateway as Message Broker

## Status
Accepted

## Context
Multi-agent routing needs deterministic dispatch, governance interception, and context injection.

## Decision
Use OpenClaw Gateway as hub-and-spoke message broker for Planner → Workers with Judge middleware.

## Consequences
- Capability-discovery and schema validation at the hub
- Heartbeat and OCC on assignments; fewer ghost updates
