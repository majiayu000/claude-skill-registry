---
name: pmtl-runbook-cms-runtime-errors
description: "⛔ DEPRECATED. This skill referenced apps/cms (Payload CMS) runtime which is no longer the target architecture. The project now uses NestJS (apps/api) as backend authority. See AGENTS.md Design-First Direction. Do NOT use this skill for new issues."
---

# ⛔ DEPRECATED — PMTL Runbook CMS Runtime Errors

> **Status**: Deprecated as of 2026-03-20.
> **Reason**: Project architecture migrated from Payload CMS (`apps/cms`) to NestJS (`apps/api`).
> **See**: `design/DECISIONS.md`, `AGENTS.md` Design-First Direction section.

This skill referenced `apps/cms/` file paths that no longer exist in the target architecture.

For runtime incident debugging in the new NestJS backend:
- Check `apps/api/src/` for route and service files
- Auth issues: `apps/api/src/modules/auth/`
- Search issues: `apps/api/src/modules/search/`
- Health/monitoring: `apps/api/src/platform/health/`
- Follow `design/baseline/infra.md` for infrastructure components
