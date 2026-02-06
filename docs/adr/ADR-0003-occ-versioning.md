# ADR-0003: Optimistic Concurrency Control (OCC)

## Status
Accepted

## Context
Concurrent tasks risk ghost updates and double-spending.

## Decision
All mutable entities carry `version` and updates use `WHERE version = v` then `v+1`.

## Consequences
- Retry on conflict with fresh state
- Deterministic idempotency across side effects
