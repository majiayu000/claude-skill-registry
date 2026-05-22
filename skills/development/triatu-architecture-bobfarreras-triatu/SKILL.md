---
name: triatu-architecture
description: "Clean Architecture guidance for Triatu: layering, dependencies, and where code belongs. Use when adding new modules, moving code across layers, or updating architecture decisions and docs."
---

# Triatu Architecture

## Quick start

- Follow dependency direction: UI -> Application -> Domain <- Infrastructure.
- Keep use cases framework-agnostic (no Next.js or Supabase types in core use cases).
- Validate inputs with Zod before touching infrastructure.
- Update architecture docs on any structural change.

## Workflow

1) Read `arquitectura_triatu.md` for the current model.
2) Identify the layer for new logic (Domain, Application, Infrastructure, UI).
3) Add interfaces/ports in Domain when infrastructure is involved.
4) Implement adapters in Infrastructure and wire them in Application.
5) Keep UI thin: call Application use cases and map view models.
6) Add tests first (TDD), then code.
7) Update docs: `guia.md`, `arquitectura_triatu.md`, `docs/PROJECT_AUDIT.md`.

## Guardrails

- No direct infrastructure access from Domain.
- Avoid global state unless justified (Zustand only for ephemeral UI).
- Avoid logs with PII; use `lib/logger` and `debug` in dev only.

## References

- `arquitectura_triatu.md`
- `docs/CORE.md`
- `guia.md`
- `docs/DEVELOPMENT.md`
- `docs/PROJECT_AUDIT.md`

