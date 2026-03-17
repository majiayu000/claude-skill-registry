---
name: Multi-Tenancy & SaaS Architecture
description: Patterns for building B2B SaaS multi-tenancy: tenant identification, data isolation (RLS/schema/db), quotas, billing/metering, onboarding, and tenant-safe operations
---

# Multi-Tenancy & SaaS Architecture

## Overview

Multi-tenancy lets one product serve many customers safely. The hard parts are enforcing isolation everywhere (API, DB, cache, jobs), preventing noisy-neighbor issues, and keeping operations (migrations, billing, support) tenant-aware.

## Why This Matters

- **Security**: prevent cross-tenant data leaks (the #1 existential risk for SaaS)
- **Scalability**: serve thousands of tenants without exploding ops overhead
- **Cost efficiency**: shared infra with fair resource allocation
- **Velocity**: one codebase and deployment model, still customizable per tenant

---

## Core Concepts

### 1. Tenancy Models

- **Single-tenant**: strongest isolation, higher cost/ops; good for regulated/large enterprise.
- **Multi-tenant**: shared everything with logical isolation; best for scale and cost.
- **Hybrid**: default shared, premium tenants isolated (by schema or database) when needed.

Decision drivers: compliance, data residency, tenant size skew, customization needs, and ops maturity.

### 2. Data Isolation Strategies

- **Row-level** (shared DB): add `tenant_id` to every table; enforce with DB policies (Postgres RLS) + app-layer scoping.
- **Schema-per-tenant**: better isolation and per-tenant maintenance, but more migrations/connection management complexity.
- **Database-per-tenant**: strongest blast-radius control; easiest per-tenant restore; hardest to operate at high tenant counts.

Rule: protect against “forgotten filters” by making isolation enforceable at the lowest layer possible (DB).

### 3. Tenant Identification & Propagation

- Identify tenant via **subdomain**, **custom domain**, **header**, or **JWT claim**.
- Validate tenant membership at auth time; never trust a raw header alone.
- Propagate `tenant_id` into logs, metrics labels (carefully), and traces for supportability.

### 4. Resource Quotas & Noisy-Neighbor Controls

- Rate limits per tenant (requests/sec, concurrency, burst).
- Usage limits per tenant (seats, storage, feature entitlements).
- Background work budgets (queue priority, per-tenant concurrency caps, fair scheduling).

### 5. Tenant Configuration & Customization

- Config store keyed by `tenant_id` (limits, features, integrations, branding).
- Feature flags support per-tenant overrides and staged rollouts.
- Avoid tenant-specific branches in core logic; prefer configuration + extension points.

### 6. Database & App Patterns

- **Single source of tenant context**: a request-scoped context object; forbid ad-hoc tenant lookups.
- Query scoping: require `tenant_id` in repository APIs; add composite indexes like `(tenant_id, id)`.
- Migrations: choose global vs per-tenant scheduling; for large tenants, support phased backfills.
- Connection pooling: consider per-tenant routing; guard against tenant explosion (pool thrash).

### 7. Billing & Metering

- Emit tenant-scoped usage events (idempotent, deduplicated) to a ledger.
- Separate “raw events” from “billable aggregates”; recompute aggregates from source of truth.
- Align entitlements (plans) with enforcement points (API limits, feature flags, job budgets).

### 8. Tenant Onboarding & Lifecycle

- Provision: create tenant record, defaults, admin user, and initial data (idempotent).
- Verify: “smoke tests” per tenant (login, create project, run core flow).
- Offboarding: export, deletion/retention policy, key rotation, and access revocation.

## Quick Start (Tenant Context Middleware)

```typescript
import type { Request, Response, NextFunction } from "express";

declare global {
  namespace Express {
    interface Request {
      tenantId?: string;
    }
  }
}

export function tenantContext(req: Request, res: Response, next: NextFunction) {
  const tenantId = req.header("x-tenant-id") ?? req.subdomains?.[0];
  if (!tenantId) return res.status(400).json({ error: "Missing tenant" });

  // IMPORTANT: verify tenantId is allowed for the authenticated principal.
  req.tenantId = tenantId;
  next();
}
```

## Production Checklist

- [ ] Tenant isolation enforced at DB layer where possible (e.g., Postgres RLS)
- [ ] Tenant context is required for all reads/writes (API, jobs, CLI tools)
- [ ] Caches/queues/storage are tenant-aware (namespacing, prefixes, partitioning)
- [ ] Quotas/rate limits implemented and monitored per tenant
- [ ] Tenant-aware observability (logs/traces) and support tooling exist
- [ ] Onboarding/offboarding are automated and idempotent
- [ ] Billing/metering events are tenant-scoped with dedupe/idempotency keys

## Tools & Libraries

| Tool | Purpose |
|------|---------|
| PostgreSQL RLS | Enforce row-level isolation in the database |
| Prisma / SQLAlchemy / TypeORM | Tenant-scoped data access patterns |
| Cerbos / OPA | Authorization and policy evaluation |
| Stripe | Billing, plans, and invoicing |
| LaunchDarkly / Unleash | Tenant feature flags and rollouts |
| Redis | Tenant-aware caching and rate limiting |

## Anti-patterns

1. **“Filter in app only”**: no DB enforcement; one missed `tenant_id` filter becomes a breach
2. **Shared resources without limits**: one tenant degrades everyone
3. **Global caches**: cached objects without tenant namespace
4. **Tenant-unaware jobs**: background workers processing cross-tenant data accidentally

## Real-World Examples

### Example: Postgres RLS

- Add `tenant_id` to tables; enable RLS; use a session variable (e.g., `SET app.tenant_id = ...`) and policies like `tenant_id = current_setting('app.tenant_id')::uuid`.

### Example: Tenant-Aware Caching

- Redis keys: `tenant:{tenantId}:users:{userId}`; avoid sharing computed results across tenants unless explicitly safe.

### Example: Tiered Isolation

- Start with row-level isolation; migrate large tenants to schema-per-tenant later using a dual-write/cutover approach.

## Common Mistakes

1. Forgetting tenant scoping in admin tools and internal scripts
2. Mixing tenant data in logs/traces or exporting tenant IDs without access controls
3. Building “customization” as divergent code paths instead of config/extension points
4. Applying global migrations/backfills without controlling per-tenant impact

## Integration Points

- Authentication/SSO (tenant mapping, domain verification, SCIM)
- Database layer (RLS, migrations, backups, restores)
- Caching + queues (namespacing, fairness)
- Billing + CRM (tenant lifecycle, usage ledger, entitlement enforcement)

## Further Reading

- [Multi-Tenant SaaS Patterns (AWS)](https://aws.amazon.com/partners/programs/saas/)
- [Azure Multi-Tenant Guidance](https://learn.microsoft.com/azure/architecture/guide/multitenant/)
- [PostgreSQL Row Level Security](https://www.postgresql.org/docs/current/ddl-rowsecurity.html)
