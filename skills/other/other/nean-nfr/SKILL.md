---
name: nean-nfr
description: Non-functional requirements checklist for NEAN features
---

## Purpose

Ensure NEAN stories address NFRs. Complements security policies and stack conventions.

## NEAN-specific concerns (always consider)

1. **PostgreSQL efficiency** — query patterns, indexing strategy, pagination for large tables, N+1 query prevention
2. **Schema migrations** — TypeORM migrations need rollback strategy; test migrations in staging first
3. **API resilience** — idempotency keys for mutations, rate limiting on expensive/public endpoints, graceful degradation
4. **Angular rendering** — lazy loading modules, OnPush change detection where appropriate, bundle size monitoring
5. **Caching** — consider caching layer for frequently accessed data (Redis, in-memory); cache invalidation strategy
6. **Operability** — config/env differences, safe rollout/rollback, feature flags if risky, health checks

For standard concerns, output format, and flexibility rules, see `/shared-nfr`.

### NEAN-specific standard concern additions

- Performance: <200ms p95, bundle size budgets
- Reliability: retry logic for external services
- Security/privacy: GDPR considerations
- Observability: structured logging
- Accessibility: ARIA labels on UI changes
