---
name: saas-architecture-advisor
description: >-
  Advises on multi-tenant SaaS architecture decisions including tenancy
  models, data isolation strategies, tenant routing, and scaling patterns.
  Use when someone is building a SaaS product, converting single-tenant to
  multi-tenant, or evaluating isolation strategies. Trigger words: multi-tenant,
  SaaS architecture, tenant isolation, shared database, per-tenant database,
  row-level security, tenant routing, SaaS patterns.
license: Apache-2.0
compatibility: "Language and database agnostic; examples default to PostgreSQL and Node.js"
metadata:
  author: terminal-skills
  version: "1.0.0"
  category: development
  tags: ["saas", "multi-tenant", "architecture", "database-design"]
---

# SaaS Architecture Advisor

## Overview

This skill helps teams design and implement multi-tenant SaaS architectures by evaluating isolation strategies, generating tenant routing patterns, and recommending the right tradeoffs based on scale, compliance requirements, and budget constraints.

## Instructions

### Step 1: Gather Context

Before recommending anything, establish:
- **Scale**: Expected tenant count (year 1 and year 3)
- **Tenant size**: Users per tenant (range and distribution)
- **Compliance**: SOC2, HIPAA, GDPR, or contractual isolation requirements
- **Stack**: Database, language, framework, hosting
- **Budget**: Monthly infrastructure budget
- **Data sensitivity**: What kind of data tenants store
- **Customization needs**: Do tenants need custom fields, workflows, or branding?

### Step 2: Evaluate Tenancy Models

Present trade-offs for these models:

**Shared Everything** (single DB, shared tables, tenant_id column):
- Best for: <1,000 tenants, uniform data model, no strict isolation requirements
- Cost: Lowest ($1 DB serves all tenants)
- Risk: Query bugs can leak data; noisy neighbor issues
- Mitigation: Row-level security (PostgreSQL RLS), application-layer checks

**Schema per Tenant** (single DB, separate schemas):
- Best for: 50-500 tenants, moderate isolation needs
- Cost: Low (single DB instance, logical separation)
- Risk: Migration complexity scales with tenant count; catalog bloat
- Mitigation: Automated migration tooling, connection pooling with schema switching

**Database per Tenant** (dedicated DB per tenant):
- Best for: <100 tenants, strict compliance, large enterprise clients
- Cost: Highest ($274+/mo per tenant on RDS)
- Risk: Operational overhead managing N databases
- Mitigation: Infrastructure-as-code templates, centralized monitoring

**Hybrid** (shared for standard, dedicated for enterprise):
- Best for: Mixed tenant base with some requiring isolation
- Cost: Moderate (shared DB + N dedicated for premium)
- Trade-off: Two code paths, but repository pattern abstracts them

### Step 3: Design Tenant Routing

Recommend routing strategy based on the application type:
- **Subdomain routing**: `tenant.app.com` — best for B2B SaaS
- **Path routing**: `app.com/tenant/` — simpler SSL, good for internal tools
- **Header routing**: `X-Tenant-ID` — API-first products
- **JWT claim**: `tenant_id` in token — serverless/stateless architectures

### Step 4: Address Cross-Cutting Concerns

For each recommendation, cover:
- **Rate limiting**: Per-tenant to prevent noisy neighbors
- **Billing metering**: How to track usage per tenant
- **Background jobs**: Tenant context propagation to workers/queues
- **Caching**: Tenant-namespaced cache keys
- **Search**: Filtered indices or per-tenant indices
- **Audit logging**: Tenant-scoped audit trails

### Step 5: Generate Implementation Artifacts

Produce:
- Database schema with tenant isolation mechanisms
- Middleware/interceptor code for tenant context
- Repository pattern that abstracts tenancy
- Tenant provisioning/deprovisioning scripts
- Migration strategy for existing single-tenant apps

## Examples

### Example 1: Early-Stage SaaS

**User prompt:**
```
We have 30 tenants and expect 200 in a year. PostgreSQL, no compliance needs yet. What tenancy model?
```

**Agent output:**
```
Recommendation: Shared database with RLS

At 200 tenants with no compliance requirements, a single PostgreSQL database
with row-level security gives you the best simplicity-to-isolation ratio.

Implementation:
1. Add tenant_id UUID column to all tenant-scoped tables
2. Enable RLS: ALTER TABLE <table> ENABLE ROW LEVEL SECURITY;
3. Create policies: USING (tenant_id = current_setting('app.tenant_id')::UUID)
4. Set tenant context per request in middleware via SET LOCAL

Cost: Single db.t3.medium handles this easily at ~$50/month.
Migration path: If you later need dedicated DBs for enterprise clients,
the repository pattern lets you route specific tenants without changing app code.
```

### Example 2: Healthcare SaaS Requiring HIPAA

**User prompt:**
```
Building a patient records SaaS. 50 clinic tenants, HIPAA required. Budget: $5k/month infra.
```

**Agent output:**
```
Recommendation: Database per tenant

HIPAA requires demonstrable data isolation. At 50 tenants, per-tenant databases
are operationally feasible and satisfy compliance auditors.

Architecture:
- Tenant registry DB (shared): Stores tenant metadata + routing config
- Per-tenant RDS instances: db.t3.medium ($50/mo each) = $2,500/mo for 50
- Connection routing: Middleware resolves tenant → connection string from registry
- Encryption: RDS encryption at rest + tenant-specific KMS keys

Budget fit: $2,500 for DBs + $1,000 compute + $500 other = $4,000/mo ✅

Key HIPAA controls addressed:
- Physical data isolation (separate DB instances)
- Per-tenant encryption keys (KMS)
- Tenant-scoped audit logs
- Independent backup/restore per tenant
```

## Guidelines

- **No one-size-fits-all** — always evaluate against the specific context before recommending
- **Start simple, migrate up** — recommend the simplest model that meets requirements; overengineering multi-tenancy is expensive
- **RLS is not optional for shared databases** — application-layer filtering alone is insufficient; one missed WHERE clause = data breach
- **Test tenant isolation** — always recommend integration tests that verify queries cannot access other tenants' data
- **Plan for the migration path** — even if starting with shared DB, design the data access layer so switching to dedicated DBs later is feasible
- **Background jobs are the blind spot** — tenant context often gets lost in async flows; always address this explicitly
