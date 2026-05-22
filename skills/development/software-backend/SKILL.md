---
name: software-backend
description: Production-grade backend API development with Node.js 24 LTS/25 Current (Express 5.x/Fastify 5.2/NestJS 11.x), Python 3.14+ (FastAPI 0.115+), Go 1.25+, Rust 1.92+ (Axum 0.8+), Prisma 6.x ORM, PostgreSQL 18. Includes GraphQL, TypeScript 5.9+ strict mode, modern logging (Pino/Winston), secret managers, PM2 process management, and Prisma Accelerate for serverless/edge deployments.
---

# Backend Engineering Skill — Quick Reference

This skill equips backend engineers with execution-ready patterns for modern API development, database design, authentication, caching, observability, error handling, testing, and deployment. Apply these patterns when you need REST/GraphQL API design, database schema modeling, authentication flows, performance optimization, or production-grade backend architectures.

**Modern Best Practices (December 2025)**: GraphQL adoption, TypeScript 5.9+ strict mode, TypeScript 7 native preview (Project Corsa) for faster tooling https://devblogs.microsoft.com/typescript/progress-on-typescript-7-december-2025/, `unknown` over `any`, structured logging, secret managers, and secure defaults (rate limiting, headers, input validation).

---

## Quick Reference

| Task | Tool/Framework | Command | When to Use |
|------|----------------|---------|-------------|
| REST API | Express 5.x / Fastify 5.2 / NestJS 11.x | `npm create express-app` | Traditional CRUD APIs, public APIs |
| GraphQL API | Apollo Server/Pothos | `npm install @apollo/server` | Flexible data fetching, avoiding over-fetching |
| Database ORM | Prisma 6.x / Drizzle | `npx prisma init` | Type-safe database access, migrations |
| Authentication | JWT/NextAuth.js/Passport | `npm install jsonwebtoken` | User sessions, API authentication |
| Validation | Zod/Joi | `npm install zod` | Runtime type validation at API boundaries |
| Caching | Redis/Upstash | `npm install ioredis` | Read-heavy operations, session storage |
| Background Jobs | BullMQ/Agenda | `npm install bullmq` | Email sending, async processing |
| Testing | Vitest/Jest/Supertest | `vitest run` | Unit, integration, E2E testing |
| Logging | Pino/Winston | `npm install pino` | Structured logging, observability |
| API Documentation | Swagger/OpenAPI | `@nestjs/swagger` | Auto-generated API docs |

# When to Use This Skill

Use this skill when you need:

- REST or GraphQL API design and implementation (GraphQL adoption increasing)
- Database schema design and migrations (Prisma schema-first approach, Prisma Accelerate for serverless)
- Authentication and authorization patterns (JWT, OAuth2, sessions, NextAuth.js)
- Error handling and validation strategies (Zod/Joi TypeScript-first validation)
- API security best practices (Helmet.js headers, OWASP API Security Top 10, rate limiting)
- Performance optimization and caching (Redis, Prisma connection pooling, singleton pattern)
- Testing strategies (Vitest, Jest, Playwright for E2E, supertest for API testing)
- Background job processing (BullMQ, Agenda)
- API documentation and versioning (Swagger/OpenAPI auto-generation)
- Deployment and production readiness (PM2 process management, Docker, secret managers)
- Monitoring and observability (structured logging with Pino/Winston, Sentry, OpenTelemetry)

## Decision Tree: Backend Technology Selection

```text
Backend project needs: [API Type]
    ├─ REST API?
    │   ├─ Simple CRUD → Express 5.x + Prisma 6.x
    │   ├─ Enterprise features → NestJS 11.x (built-in DI, modules)
    │   └─ High performance → Fastify 5.2 (faster than Express)
    │
    ├─ GraphQL API?
    │   ├─ Code-first → Pothos GraphQL (TypeScript)
    │   └─ Schema-first → Apollo Server + GraphQL Codegen
    │
    ├─ Authentication Strategy?
    │   ├─ JWT tokens → jsonwebtoken + httpOnly cookies
    │   ├─ OAuth/Social → NextAuth.js or Passport.js
    │   └─ Magic links → Custom implementation + email service
    │
    ├─ Database Layer?
    │   ├─ Type-safe ORM → Prisma 6.x (best for TypeScript)
    │   ├─ SQL-first → Drizzle ORM or Kysely
    │   └─ Raw SQL → pg (PostgreSQL 18 driver)
    │
    ├─ Caching Strategy?
    │   ├─ Distributed cache → Redis (multi-server)
    │   ├─ Serverless cache → Upstash Redis
    │   └─ In-memory cache → Node.js Map (single server)
    │
    └─ Background Jobs?
        ├─ Complex workflows → BullMQ (Redis-backed, retries)
        └─ Simple scheduling → node-cron or Agenda
```

**Language Alternatives:**

- **Node.js 24 LTS / 25 Current** (Express 5.x / Fastify 5.2 / NestJS 11.x + Prisma 6.x): TypeScript-first, async/await, Web Storage API
- **Python 3.14+** (FastAPI 0.115+ + SQLAlchemy 2.0+): Data-heavy services, async support, evolving concurrency model, modern typing
- **Go 1.25+** (Fiber 2.x + GORM 1.25+): High concurrency, native performance, experimental encoding/json/v2
- **Rust 1.92+** (Axum 0.8+ + SeaORM 1.1+): Memory safety, zero-cost abstractions, Rust 2024 edition

See [templates/](templates/) for language-specific starter templates.

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

## Navigation

**Resources**
- [resources/backend-best-practices.md](resources/backend-best-practices.md) — Node.js patterns for auth, error handling, database, performance, testing, observability
- [resources/go-best-practices.md](resources/go-best-practices.md) — Go idioms, concurrency, error handling, GORM usage, testing, profiling
- [resources/rust-best-practices.md](resources/rust-best-practices.md) — Ownership, async, Axum, SeaORM, error handling, testing
- [resources/python-best-practices.md](resources/python-best-practices.md) — FastAPI, SQLAlchemy, async patterns, validation, testing, performance
- [README.md](README.md) — Folder overview and usage notes
- [data/sources.json](data/sources.json) — External references per language/runtime
- Shared checklists: [../software-clean-code-standard/templates/checklists/backend-api-review-checklist.md](../software-clean-code-standard/templates/checklists/backend-api-review-checklist.md), [../software-clean-code-standard/templates/checklists/secure-code-review-checklist.md](../software-clean-code-standard/templates/checklists/secure-code-review-checklist.md)

**Shared Utilities** (Centralized patterns — extract, don't duplicate)
- [../software-clean-code-standard/utilities/auth-utilities.md](../software-clean-code-standard/utilities/auth-utilities.md) — Argon2id, jose JWT, OAuth 2.1/PKCE
- [../software-clean-code-standard/utilities/error-handling.md](../software-clean-code-standard/utilities/error-handling.md) — Effect Result types, correlation IDs
- [../software-clean-code-standard/utilities/config-validation.md](../software-clean-code-standard/utilities/config-validation.md) — Zod 3.24+, Valibot, secrets management
- [../software-clean-code-standard/utilities/resilience-utilities.md](../software-clean-code-standard/utilities/resilience-utilities.md) — p-retry v6, opossum v8, OTel spans
- [../software-clean-code-standard/utilities/logging-utilities.md](../software-clean-code-standard/utilities/logging-utilities.md) — pino v9 + OpenTelemetry integration
- [../software-clean-code-standard/utilities/testing-utilities.md](../software-clean-code-standard/utilities/testing-utilities.md) — Vitest, MSW v2, factories, fixtures
- [../software-clean-code-standard/utilities/observability-utilities.md](../software-clean-code-standard/utilities/observability-utilities.md) — OpenTelemetry SDK, tracing, metrics
- [../software-clean-code-standard/resources/clean-code-standard.md](../software-clean-code-standard/resources/clean-code-standard.md) — Canonical clean code rules (`CC-*`) for citation

**Templates**
- [templates/nodejs/template-nodejs-prisma-postgres.md](templates/nodejs/template-nodejs-prisma-postgres.md) — Node.js + Prisma + PostgreSQL
- [templates/go/template-go-fiber-gorm.md](templates/go/template-go-fiber-gorm.md) — Go + Fiber + GORM + PostgreSQL
- [templates/rust/template-rust-axum-seaorm.md](templates/rust/template-rust-axum-seaorm.md) — Rust + Axum + SeaORM + PostgreSQL
- [templates/python/template-python-fastapi-sqlalchemy.md](templates/python/template-python-fastapi-sqlalchemy.md) — Python + FastAPI + SQLAlchemy + PostgreSQL

**Related Skills**
- [../software-architecture-design/SKILL.md](../software-architecture-design/SKILL.md) — System decomposition, SLAs, and data flows
- [../software-security-appsec/SKILL.md](../software-security-appsec/SKILL.md) — Authentication/authorization and secure API design
- [../ops-devops-platform/SKILL.md](../ops-devops-platform/SKILL.md) — CI/CD, infrastructure, and deployment safety
- [../qa-resilience/SKILL.md](../qa-resilience/SKILL.md) — Resilience, retries, and failure playbooks
- [../software-code-review/SKILL.md](../software-code-review/SKILL.md) — Review checklists and standards for backend changes
- [../qa-testing-strategy/SKILL.md](../qa-testing-strategy/SKILL.md) — Testing strategies, test pyramids, and coverage goals
- [../dev-api-design/SKILL.md](../dev-api-design/SKILL.md) — RESTful design, GraphQL, and API versioning patterns
- [../data-sql-optimization/SKILL.md](../data-sql-optimization/SKILL.md) — SQL optimization, indexing, and query tuning patterns

---

## Operational Playbooks
- [resources/operational-playbook.md](resources/operational-playbook.md) — Full backend architecture patterns, checklists, TypeScript notes, and decision tables
