# ADR-0001: Spec-Driven Development

## Status
Accepted

## Context
Agentic systems require deterministic behaviors and auditable contracts.

## Decision
Adopt Spec-Driven Development: all capabilities and IO are defined via JSON Schema in `specs/` prior to implementation.

## Consequences
- Lower drift and safer governance
- Enables TDD goalposts and CI enforcement
