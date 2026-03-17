---
name: mern-nfr
description: Non-functional requirements checklist for MERN features
---

## Purpose

Ensure MERN stories address NFRs. Complements security policies and stack conventions.

## MERN-specific concerns (always consider)

1. **MongoDB efficiency** — query patterns, indexing assumptions, pagination for large collections
2. **Schema migrations** — Mongoose schema changes need migration/compatibility strategy
3. **API resilience** — idempotency for mutations, rate limiting on expensive/public endpoints, graceful degradation
4. **Next.js rendering** — appropriate rendering strategy (SSR/SSG/client) for the use case
5. **Operability** — config/env differences, safe rollout/rollback, feature flags if risky

For standard concerns, output format, and flexibility rules, see `/shared-nfr`.
