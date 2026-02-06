# Contributing Guide

## Branch Strategy
- Use feature branches: `feature/<short-name>` for new capabilities or docs.
- Use `fix/<short-name>` for hotfixes.
- Submit PRs to `main`; CI must pass (security + quality + container tests).

## Process
- Spec-First: Update `specs/` and ADRs before implementation.
- TDD Mandatory: Add failing tests under `tests/` defining goalposts.
- Governance: Changes to SOUL or policies must include version bumps and notes.

## Commit Hygiene
- Use descriptive messages referencing affected specs/tests.
- Link ADRs when making architectural decisions.

## Code Quality
- Run `make lint` and `make test` locally.
- Prefer `make ui-secure` to preview frontend and `make api` to test API.
