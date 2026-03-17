---
name: software-backend
description: Production-grade backend service development across Node.js (Express/Fastify/NestJS/Hono), Bun, Python (FastAPI), Go, and Rust (Axum), with PostgreSQL and common ORMs (Prisma/Drizzle/SQLAlchemy/GORM/SeaORM). Use for REST/GraphQL/tRPC APIs, auth (OIDC/OAuth), caching, background jobs, observability (OpenTelemetry), testing, deployment readiness, and zero-trust defaults.
---

# Software Backend Engineering

Use this skill to design, implement, and review production-grade backend services: API boundaries, data layer, auth, caching, observability, error handling, testing, and deployment.

Defaults to bias toward: type-safe boundaries (validation at the edge), OpenTelemetry for observability, zero-trust assumptions, idempotency for retries, RFC 9457 errors, Postgres + pooling, structured logs, timeouts, and rate limiting.

---

## Quick Reference

| Task | Default Picks | Notes |
|------|---------------|-------|
| REST API | Fastify / Express / NestJS | Prefer typed boundaries + explicit timeouts |
| Edge API | Hono / platform-native handlers | Keep work stateless, CPU-light |
| Type-Safe API | tRPC | Prefer for TS monorepos and internal APIs |
| GraphQL API | Apollo Server / Pothos | Prefer for complex client-driven queries |
| Database | PostgreSQL | Use pooling + migrations + query budgets |
| ORM / Query Layer | Prisma / Drizzle / SQLAlchemy / GORM / SeaORM | Prefer explicit transactions |
| Authentication | OIDC/OAuth + sessions/JWT | Prefer httpOnly cookies for browsers |
| Validation | Zod / Pydantic / validator libs | Validate at the boundary, not deep inside |
| Caching | Redis (or managed) | Use TTLs + invalidation strategy |
| Background Jobs | BullMQ / platform queues | Make jobs idempotent + retry-safe |
| Testing | Unit + integration + contract/E2E | Keep most tests below the UI layer |
| Observability | Structured logs + OpenTelemetry | Correlation IDs end-to-end |

## Scope

Use this skill to:

- Design and implement REST/GraphQL/tRPC APIs
- Model data schemas and run safe migrations
- Implement authentication/authorization (OIDC/OAuth, sessions/JWT)
- Add validation, error handling, rate limiting, caching, and background jobs
- Ship production readiness (timeouts, observability, deploy/runbooks)

## When NOT to Use This Skill

Use a different skill when:

- **Frontend-only concerns** -> See [software-frontend](../software-frontend/SKILL.md)
- **Infrastructure provisioning (Terraform, K8s manifests)** -> See [ops-devops-platform](../ops-devops-platform/SKILL.md)
- **API design patterns only (no implementation)** -> See [dev-api-design](../dev-api-design/SKILL.md)
- **SQL query optimization and indexing** -> See [data-sql-optimization](../data-sql-optimization/SKILL.md)
- **Security audits and threat modeling** -> See [software-security-appsec](../software-security-appsec/SKILL.md)
- **System architecture (beyond single service)** -> See [software-architecture-design](../software-architecture-design/SKILL.md)

## Decision Tree: Backend Technology Selection

```text
Backend project needs: [API Type]
  - REST API?
    - Simple CRUD -> Express/Fastify + Prisma/Drizzle
    - Enterprise features -> NestJS (DI, modules)
    - High performance -> Fastify (tight request lifecycle)
    - Edge/Serverless -> Hono (Cloudflare Workers, Vercel Edge)

  - Type-Safe API?
    - Full-stack TypeScript monorepo -> tRPC (no schema, no codegen)
    - Public API with docs -> REST + OpenAPI
    - Flexible data fetching -> GraphQL + Pothos/Apollo

  - GraphQL API?
    - Code-first -> Pothos GraphQL (TypeScript)
    - Schema-first -> Apollo Server + GraphQL Codegen

  - Runtime Selection?
    - Enterprise stable -> Node.js (current LTS)
    - Performance-critical -> Bun (verify runtime constraints)
    - Security-focused -> Deno (verify platform support)

  - Authentication Strategy?
    - Browser sessions -> httpOnly cookies + server-side session store
    - OAuth/Social -> OIDC/OAuth library (or platform auth)
    - Service-to-service -> short-lived JWT + mTLS where possible

  - Database Layer?
    - Type-safe ORM -> Prisma (migrations, Studio)
    - SQL-first/perf -> Drizzle (SQL-like API)
    - Raw SQL -> driver + query builder (Kysely/sqlc/SQLx)
    - Edge-compatible -> driver/ORM + Neon/Turso/D1

  - Caching Strategy?
    - Distributed cache -> Redis (multi-server)
    - Serverless cache -> managed Redis (e.g., Upstash)
    - In-memory cache -> process memory (single instance only)

  - Edge Deployment?
    - Global low-latency -> Cloudflare Workers
    - Next.js integration -> Vercel Edge Functions
    - AWS ecosystem -> Lambda@Edge

  - Background Jobs?
    - Complex workflows -> BullMQ (Redis-backed, retries)
    - Serverless workflows -> AWS Step Functions
    - Simple scheduling -> cron + durable storage
```

**Runtime & Language Alternatives:**

- **Node.js (current LTS)** (Express/Fastify/NestJS + Prisma/Drizzle): default for broad ecosystem + mature tooling
- **Bun** (Hono/Elysia + Drizzle): consider for perf-sensitive workloads (verify runtime constraints)
- **Python** (FastAPI + SQLAlchemy): strong for data-heavy services and ML integration
- **Go** (Fiber/Gin + GORM/sqlc): strong for concurrency and simple deploys
- **Rust** (Axum + SeaORM/SQLx): strong for safety/performance-critical services

See [assets/](assets/) for language-specific starter templates and [references/edge-deployment-guide.md](references/edge-deployment-guide.md) for edge computing patterns.

---

## API Design Patterns (Dec 2025)

### Idempotency Patterns

All mutating operations MUST support idempotency for retry safety.

**Implementation:**

```typescript
// Idempotency key header
const idempotencyKey = request.headers['idempotency-key'];
const cached = await redis.get(`idem:${idempotencyKey}`);
if (cached) return JSON.parse(cached);

const result = await processOperation();
await redis.set(`idem:${idempotencyKey}`, JSON.stringify(result), 'EX', 86400);
return result;
```

| Do | Avoid |
|----|-------|
| Store idempotency keys with TTL (24h typical) | Processing duplicate requests |
| Return cached response for duplicate keys | Different responses for same key |
| Use client-generated UUIDs | Server-generated keys |

### Pagination Patterns

| Pattern | Use When | Example |
|---------|----------|---------|
| Cursor-based | Large datasets, real-time data | `?cursor=abc123&limit=20` |
| Offset-based | Small datasets, random access | `?page=3&per_page=20` |
| Keyset | Sorted data, high performance | `?after_id=1000&limit=20` |

**Prefer cursor-based pagination** for APIs with frequent inserts.

### Error Response Standard (Problem Details)

Use a consistent machine-readable error format (RFC 9457 Problem Details): https://www.rfc-editor.org/rfc/rfc9457

```json
{
  "type": "https://example.com/problems/invalid-request",
  "title": "Invalid request",
  "status": 400,
  "detail": "email is required",
  "instance": "/v1/users"
}
```

### Health Check Patterns

```typescript
// Liveness: Is the process running?
app.get('/health/live', (req, res) => {
  res.status(200).json({ status: 'ok' });
});

// Readiness: Can the service handle traffic?
app.get('/health/ready', async (req, res) => {
  const dbOk = await checkDatabase();
  const cacheOk = await checkRedis();
  if (dbOk && cacheOk) {
    res.status(200).json({ status: 'ready', db: 'ok', cache: 'ok' });
  } else {
    res.status(503).json({ status: 'not ready', db: dbOk, cache: cacheOk });
  }
});
```

### Migration Rollback Strategies

| Strategy | Description | Use When |
|----------|-------------|----------|
| Backward-compatible | New code works with old schema | Zero-downtime deployments |
| Expand-contract | Add new, migrate, remove old | Schema changes |
| Shadow tables | Write to both during transition | High-risk migrations |

---

### Common Backend Mistakes to Avoid

| FAIL Avoid | PASS Instead | Why |
|----------|-----------|-----|
| Storing sessions in memory | Use Redis/Upstash | Memory lost on restart, no horizontal scaling |
| Synchronous file I/O | Use `fs.promises` or streams | Blocks event loop, kills throughput |
| Unbounded queries | Always use `LIMIT` + cursor pagination | Memory exhaustion, slow responses |
| Trusting client input | Validate with Zod at API boundaries | Injection attacks, type coercion bugs |
| Hardcoded secrets | Use env vars + secret manager (Vault, AWS SM) | Security breach on repo exposure |
| N+1 database queries | Use `include`/`select` or DataLoader | 10-100x performance degradation |
| `console.log` in production | Use structured logging (Pino/Winston) | No correlation IDs, unqueryable logs |
| Catching errors silently | Log + rethrow or handle explicitly | Hidden failures, debugging nightmares |
| Missing connection pooling | Use Prisma connection pool or PgBouncer | Connection exhaustion under load |
| No request timeouts | Set timeouts on HTTP clients and DB queries | Resource leaks, cascading failures |

**Security anti-patterns:**

- FAIL Don't use MD5/SHA1 for passwords -> Use Argon2id
- FAIL Don't store JWTs in localStorage -> Use httpOnly cookies
- FAIL Don't trust `X-Forwarded-For` without validation -> Configure trusted proxies
- FAIL Don't skip rate limiting -> Use sliding window (Redis) or token bucket
- FAIL Don't log sensitive data -> Redact PII, tokens, passwords

---

### Optional: AI/Automation Extensions

> **Note**: AI-assisted backend patterns. Skip if not using AI tooling.

#### AI-Assisted Code Generation

| Tool | Use Case |
|------|----------|
| GitHub Copilot | Inline suggestions, boilerplate |
| Cursor | AI-first IDE, context-aware |
| Claude Code | CLI-based development |

**Review requirements for AI-generated code:**

- All imports verified against package.json
- Type checker passes (strict mode)
- Security scan passes
- Tests cover generated code

---

## Infrastructure Economics and Business Impact

**Why this matters**: Backend decisions directly impact revenue. A 100ms latency increase can reduce conversions by 7%. A poorly chosen architecture can cost 10x more in cloud spend. Performance SLAs are revenue commitments.

### Cost Modeling Quick Reference

| Decision | Cost Impact | Revenue Impact |
|----------|-------------|----------------|
| Edge vs. Origin | 60-80% latency reduction | +2-5% conversion rate |
| Serverless vs. Containers | Variable cost, scales to zero | Better unit economics at low scale |
| Reserved vs. On-Demand | 30-60% cost savings | Predictable COGS |
| Connection pooling | 50-70% fewer DB connections | Lower database costs |
| Caching layer | 80-95% fewer origin requests | Reduced compute costs |

### Performance SLA -> Revenue Mapping

```text
SLA Target -> Business Metric

P50 latency < 100ms -> Baseline user experience
P95 latency < 500ms -> 95% users satisfied
P99 latency < 1000ms -> Enterprise SLA compliance
Uptime 99.9% (43.8m downtime/month) -> Standard SLA tier
Uptime 99.99% (4.4m downtime/month) -> Enterprise tier ($$$)
```

### Unit Economics Checklist

Before deploying any backend service, calculate:

- [ ] **Cost per request**: Total infra cost / monthly requests
- [ ] **Cost per user**: Total infra cost / MAU
- [ ] **Gross margin impact**: How does infra cost affect product margin?
- [ ] **Scale economics**: At 10x traffic, does cost scale linearly or worse?
- [ ] **Break-even point**: At what traffic level does this architecture pay for itself?

### Architecture Decision -> Business Impact

| Architecture Choice | Technical Benefit | Business Impact |
|---------------------|-------------------|-----------------|
| CDN + Edge caching | Lower latency | Higher conversion, better SEO |
| Read replicas | Scale reads | Handle traffic spikes without degradation |
| Queue-based processing | Decouple services | Smoother UX during high load |
| Multi-region deployment | Fault tolerance | Enterprise SLA compliance |
| Auto-scaling | Right-sized infra | Lower COGS, better margins |

### FinOps Practices for Backend Teams

1. **Tag all resources** - Every resource tagged with `team`, `service`, `environment`
2. **Set billing alerts** - Alert at 50%, 80%, 100% of budget
3. **Review weekly** - 15-minute weekly cost review meeting
4. **Right-size monthly** - Check CPU/memory utilization, downsize overprovisioned
5. **Spot/Preemptible for non-prod** - 60-90% savings on dev/staging

See [references/infrastructure-economics.md](references/infrastructure-economics.md) for detailed cost modeling, cloud provider comparisons, and ROI calculators.

---

## Navigation

**Resources**
- [references/backend-best-practices.md](references/backend-best-practices.md) - Template authoring guide, quality checklist, and shared utilities pointers
- [references/edge-deployment-guide.md](references/edge-deployment-guide.md) - Edge computing patterns, Cloudflare Workers vs Vercel Edge, tRPC, Hono, Bun
- [references/infrastructure-economics.md](references/infrastructure-economics.md) - Cost modeling, performance SLAs -> revenue, FinOps practices, cloud optimization
- [references/go-best-practices.md](references/go-best-practices.md) - Go idioms, concurrency, error handling, GORM usage, testing, profiling
- [references/rust-best-practices.md](references/rust-best-practices.md) - Ownership, async, Axum, SeaORM, error handling, testing
- [references/python-best-practices.md](references/python-best-practices.md) - FastAPI, SQLAlchemy, async patterns, validation, testing, performance
- [data/sources.json](data/sources.json) - External references per language/runtime
- Shared checklists: [../software-clean-code-standard/assets/checklists/backend-api-review-checklist.md](../software-clean-code-standard/assets/checklists/backend-api-review-checklist.md), [../software-clean-code-standard/assets/checklists/secure-code-review-checklist.md](../software-clean-code-standard/assets/checklists/secure-code-review-checklist.md)

**Shared Utilities** (Centralized patterns - extract, don't duplicate)
- [../software-clean-code-standard/utilities/auth-utilities.md](../software-clean-code-standard/utilities/auth-utilities.md) - Argon2id, jose JWT, OAuth 2.1/PKCE
- [../software-clean-code-standard/utilities/error-handling.md](../software-clean-code-standard/utilities/error-handling.md) - Effect Result types, correlation IDs
- [../software-clean-code-standard/utilities/config-validation.md](../software-clean-code-standard/utilities/config-validation.md) - Zod 3.24+, Valibot, secrets management
- [../software-clean-code-standard/utilities/resilience-utilities.md](../software-clean-code-standard/utilities/resilience-utilities.md) - p-retry v6, opossum v8, OTel spans
- [../software-clean-code-standard/utilities/logging-utilities.md](../software-clean-code-standard/utilities/logging-utilities.md) - pino v9 + OpenTelemetry integration
- [../software-clean-code-standard/utilities/testing-utilities.md](../software-clean-code-standard/utilities/testing-utilities.md) - Vitest, MSW v2, factories, fixtures
- [../software-clean-code-standard/utilities/observability-utilities.md](../software-clean-code-standard/utilities/observability-utilities.md) - OpenTelemetry SDK, tracing, metrics
- [../software-clean-code-standard/references/clean-code-standard.md](../software-clean-code-standard/references/clean-code-standard.md) - Canonical clean code rules (`CC-*`) for citation

**Templates**
- [assets/nodejs/template-nodejs-prisma-postgres.md](assets/nodejs/template-nodejs-prisma-postgres.md) - Node.js + Prisma + PostgreSQL
- [assets/go/template-go-fiber-gorm.md](assets/go/template-go-fiber-gorm.md) - Go + Fiber + GORM + PostgreSQL
- [assets/rust/template-rust-axum-seaorm.md](assets/rust/template-rust-axum-seaorm.md) - Rust + Axum + SeaORM + PostgreSQL
- [assets/python/template-python-fastapi-sqlalchemy.md](assets/python/template-python-fastapi-sqlalchemy.md) - Python + FastAPI + SQLAlchemy + PostgreSQL

**Related Skills**
- [../software-architecture-design/SKILL.md](../software-architecture-design/SKILL.md) - System decomposition, SLAs, and data flows
- [../software-security-appsec/SKILL.md](../software-security-appsec/SKILL.md) - Authentication/authorization and secure API design
- [../ops-devops-platform/SKILL.md](../ops-devops-platform/SKILL.md) - CI/CD, infrastructure, and deployment safety
- [../qa-resilience/SKILL.md](../qa-resilience/SKILL.md) - Resilience, retries, and failure playbooks
- [../software-code-review/SKILL.md](../software-code-review/SKILL.md) - Review checklists and standards for backend changes
- [../qa-testing-strategy/SKILL.md](../qa-testing-strategy/SKILL.md) - Testing strategies, test pyramids, and coverage goals
- [../dev-api-design/SKILL.md](../dev-api-design/SKILL.md) - RESTful design, GraphQL, and API versioning patterns
- [../data-sql-optimization/SKILL.md](../data-sql-optimization/SKILL.md) - SQL optimization, indexing, and query tuning patterns

---

## Freshness Protocol

When users ask version-sensitive recommendation questions, do a quick freshness check before asserting "best" choices or quoting versions.

### Trigger Conditions

- "What's the best backend framework for [use case]?"
- "What should I use for [API design/auth/database]?"
- "What's the latest in Node.js/Go/Rust?"
- "Current best practices for [REST/GraphQL/tRPC]?"
- "Is [framework/runtime] still relevant in 2026?"
- "[Express] vs [Fastify] vs [Hono]?"
- "Best ORM for [database/use case]?"

### How to Freshness-Check

1. Start from `data/sources.json` (official docs, release notes, support policies).
2. Run a targeted web search for the specific component and open release notes/support policy pages.
3. Prefer official sources over blogs for versions and support windows.

### What to Report

- **Current landscape**: what is stable and widely used now
- **Emerging trends**: what is gaining traction (and why)
- **Deprecated/declining**: what is falling out of favor (and why)
- **Recommendation**: default choice + 1-2 alternatives, with trade-offs

### Example Topics (verify with fresh search)

- Node.js LTS support window and major changes
- Bun vs Deno vs Node.js
- Hono, Elysia, and edge-first frameworks
- Drizzle vs Prisma for TypeScript
- tRPC and end-to-end type safety
- Edge computing and serverless patterns

---

## Operational Playbooks
- [references/operational-playbook.md](references/operational-playbook.md) - Full backend architecture patterns, checklists, TypeScript notes, and decision tables
