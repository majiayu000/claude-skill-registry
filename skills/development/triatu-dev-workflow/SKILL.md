---
name: triatu-dev-workflow
description: "Day-to-day development workflow for Triatu. Use when onboarding, running the project, or preparing changes for review."
---

# Triatu Dev Workflow

## Quick start

- Read the core docs before changing architecture.
- Keep docs updated with any flow or structure change.
- Run tests before any PR.

## Workflow

1) Read `README.md`, `guia.md`, and `arquitectura_triatu.md`.
2) Follow Clean Architecture rules for new work.
3) Apply TDD: write tests first.
4) Update docs:
   - `guia.md`
   - `arquitectura_triatu.md`
   - `docs/PROJECT_AUDIT.md` for new risks/tech debt
5) Run:
   - `pnpm test`
   - `pnpm test:e2e` when UI flows change

## References

- `README.md`
- `docs/DEVELOPMENT.md`
- `docs/CONTRIBUTING.md`

