---
name: pmtl-scaffold-payload-collection
description: "⛔ DEPRECATED. This skill referenced Payload CMS collection scaffolding which is no longer the target architecture. The project now uses NestJS (apps/api) as backend authority. See AGENTS.md Design-First Direction and design/DECISIONS.md for current architecture. Do NOT use this skill."
---

# ⛔ DEPRECATED — PMTL Scaffold Payload Collection

> **Status**: Deprecated as of 2026-03-20.
> **Reason**: Project architecture migrated from Payload CMS to NestJS (`apps/api`) as backend authority.
> **See**: `design/DECISIONS.md`, `AGENTS.md` Design-First Direction section.

This skill is no longer valid. The Payload CMS 5-file collection pattern has been replaced by NestJS module scaffolding:
- `apps/api/src/modules/{module-name}/`
  - `{module-name}.module.ts` — NestJS module definition
  - `{module-name}.controller.ts` — route handlers
  - `{module-name}.service.ts` — business logic
  - `dto/` — input/output DTOs with Zod validation
  - `entities/` — Prisma entity types

For scaffolding new NestJS modules, follow patterns in `design/baseline/` and existing modules in `apps/api/src/modules/`.
