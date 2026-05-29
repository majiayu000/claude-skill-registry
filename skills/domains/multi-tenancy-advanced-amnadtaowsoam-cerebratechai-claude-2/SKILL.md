---
name: Multi-Tenancy Advanced Patterns
description: Advanced patterns for building scalable multi-tenant SaaS applications.
---

# Multi-Tenancy Advanced Patterns

## Overview

Advanced multi-tenancy focuses on isolation, scaling, and operational maturity
for SaaS platforms serving many tenants with varying needs and compliance
requirements.

## Table of Contents

1. [Architectures](#architectures)
2. [Tenant Isolation](#tenant-isolation)
3. [Tenant Identification](#tenant-identification)
4. [Database Strategies](#database-strategies)
5. [Caching](#caching)
6. [Background Jobs](#background-jobs)
7. [Rate Limiting](#rate-limiting)
8. [Feature Flags](#feature-flags)
9. [Branding and Theming](#branding-and-theming)
10. [Tenant Onboarding](#tenant-onboarding)
11. [Tenant Migrations](#tenant-migrations)
12. [Cross-Tenant Operations](#cross-tenant-operations)
13. [Compliance and Residency](#compliance-and-residency)
14. [Scaling Strategies](#scaling-strategies)
15. [Cost Allocation](#cost-allocation)
16. [Monitoring](#monitoring)
17. [Security Considerations](#security-considerations)

---

## Architectures

- **Shared DB, shared schema**: Lowest cost, highest risk.
- **Shared DB, separate schema**: Better isolation, moderate ops.
- **Separate DB per tenant**: Strong isolation, higher overhead.
- **Hybrid**: Mix tiers based on tenant size or compliance.

## Tenant Isolation

- **Data**: RLS, schema separation, or separate DB.
- **Compute**: Dedicated worker pools for large tenants.
- **Network**: VPC isolation or private endpoints when needed.

## Tenant Identification

Common approaches:
- Subdomain (`tenant.example.com`)
- Path (`/t/tenant`)
- Header (`X-Tenant-ID`)
- JWT claims (`tenant_id`)

Prefer JWT claims + middleware validation.

## Database Strategies

- Row-level security with tenant_id predicates.
- Tenant ID columns with indexed filters.
- Per-tenant connection pools for heavy tenants.

## Caching

Use tenant-scoped cache keys:
```
cacheKey = f"{tenantId}:user:{userId}"
```

Avoid cache pollution across tenants.

## Background Jobs

Isolate queues per tenant or per tier:
- Separate queues for premium tenants
- Dedicated workers for heavy tenants

## Rate Limiting

Apply per-tenant quotas:
- Requests per minute
- Concurrency limits
- Burst allowances

## Feature Flags

Use tenant-scoped flags for:
- Staged rollout
- Premium features
- Compliance-specific behavior

## Branding and Theming

Support tenant-specific assets:
- Theme variables
- Logo storage and CDN
- White-label domains

## Tenant Onboarding

Automate:
- DB provisioning or schema setup
- Default roles and permissions
- Initial data seeds

## Tenant Migrations

Use migration tooling that supports:
- Online migrations
- Backfill jobs
- Tenant-by-tenant rollout

## Cross-Tenant Operations

Define admin-only tools for:
- Support access
- Data export and audits
- Global reporting

Log all cross-tenant access.

## Compliance and Residency

Match tenants to regions:
- Data residency per country
- Regulated industries (HIPAA, PCI)

## Scaling Strategies

- Shard tenants by size or region.
- Split heavy tenants into dedicated clusters.
- Use read replicas for large tenants.

## Cost Allocation

Track usage per tenant:
- Storage
- Compute
- Requests

Use cost tags and billing reports.

## Monitoring

Monitor per-tenant:
- Error rates
- Latency
- Resource usage

Alert on noisy neighbor issues.

## Security Considerations

- Enforce tenant boundaries at every layer.
- Use least-privilege access.
- Encrypt tenant data at rest and in transit.

## Related Skills
- `17-domain-specific/multi-tenancy`
- `04-database/database-optimization`
- `10-authentication-authorization/rbac-design`
