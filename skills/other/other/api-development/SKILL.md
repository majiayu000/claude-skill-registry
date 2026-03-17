---
name: api-development
model: reasoning
description: Meta-skill that orchestrates the full API development lifecycle — from design through documentation — by coordinating specialized skills, agents, and commands into a seamless build workflow.
---

# API Development

Orchestrate the full API development lifecycle by coordinating design, implementation, testing, and documentation into a single workflow.

## When to Use This Skill

- Building a new API from scratch
- Adding endpoints to an existing API
- Redesigning or refactoring an API
- Planning API versioning and migration
- Running a complete API development cycle (design → build → test → document → deploy)


## Installation

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install api-development
```


---

## Orchestration Flow

Follow these steps in order. Each step routes to the appropriate skill or tool.

### 1. Design the API

Load the `api-design` skill to establish resource models, URL structure, HTTP method semantics, error formats, and pagination strategy.

**Deliverables:** Resource list, endpoint map, request/response schemas, error format

### 2. Generate OpenAPI Spec

Produce a machine-readable OpenAPI 3.x specification from the design. Use the OpenAPI template in `api-design/assets/openapi-template.yaml` as a starting point.

**Deliverables:** `openapi.yaml` with all endpoints, schemas, auth schemes, and examples

### 3. Scaffold Endpoints

Generate route files, request/response types, and validation schemas for each endpoint. Group routes by resource.

**Deliverables:** Route files, type definitions, validation schemas per resource

### 4. Implement Business Logic

Write service-layer logic with input validation, authorization checks, database queries, and proper error propagation. Keep controllers thin — business logic lives in the service layer.

**Deliverables:** Service modules, repository layer, middleware (auth, rate limiting, CORS)

### 5. Test

Write tests at three levels:
- **Unit tests** — service logic, validation, error handling
- **Integration tests** — endpoint behavior with real DB
- **Contract tests** — response shapes match OpenAPI spec

**Deliverables:** Test suite with coverage for happy paths, error cases, edge cases, and auth

### 6. Document

Generate human-readable API documentation with usage examples and SDK snippets. Ensure every endpoint has description, parameters, request/response examples, and error codes.

**Deliverables:** API docs, changelog, authentication guide

### 7. Version and Deploy

Apply a versioning strategy, tag the release, update changelogs, and deploy through the pipeline. Follow the `api-versioning` skill for deprecation and migration guidance.

**Deliverables:** Version tag, changelog entry, deployment confirmation

---

## API Design Decision Table

Choose the right paradigm for your use case.

| Criteria | REST | GraphQL | gRPC |
|----------|------|---------|------|
| **Best for** | CRUD-heavy public APIs | Complex relational data, client-driven queries | Internal microservices, high-throughput |
| **Data fetching** | Fixed response shape per endpoint | Client specifies exact fields | Strongly typed protobuf messages |
| **Over/under-fetching** | Common problem | Solved by design | Minimal — schema is explicit |
| **Caching** | Native HTTP caching (ETags, Cache-Control) | Requires custom caching | No built-in HTTP caching |
| **Real-time** | Polling or WebSockets | Subscriptions (built-in) | Bidirectional streaming |
| **Tooling** | Mature — OpenAPI, Postman, curl | Growing — Apollo, Relay, GraphiQL | Mature — protoc, grpcurl, Buf |
| **Learning curve** | Low | Medium | Medium-High |
| **Versioning** | URL or header versioning | Schema evolution with `@deprecated` | Package versioning in `.proto` |

**Rule of thumb:** Default to REST for public APIs. Use GraphQL when clients need flexible queries across related data. Use gRPC for internal service-to-service communication.

---

## API Checklist

Run through this checklist before marking any API work as complete.

### Authentication & Authorization

- [ ] Authentication mechanism chosen (JWT, OAuth2, API key)
- [ ] Authorization rules enforced at every endpoint
- [ ] Tokens validated and scoped correctly
- [ ] Secrets stored securely (never in code or logs)

### Rate Limiting

- [ ] Rate limits configured per endpoint or consumer tier
- [ ] `RateLimit-*` headers included in responses
- [ ] `429 Too Many Requests` returned with `Retry-After` header
- [ ] Rate limit strategy documented for consumers

### Pagination

- [ ] All collection endpoints paginated
- [ ] Pagination style chosen (cursor-based or offset-based)
- [ ] `page_size` bounded with a sensible maximum
- [ ] Total count or `hasNextPage` indicator included

### Filtering & Sorting

- [ ] Filter parameters validated and sanitized
- [ ] Sort fields allow-listed (no arbitrary column sorting)
- [ ] Default sort order defined and documented

### Error Handling

- [ ] Consistent error response schema across all endpoints
- [ ] Correct HTTP status codes (4xx for client, 5xx for server)
- [ ] Validation errors return field-level detail
- [ ] Internal errors never leak stack traces or sensitive data

### Versioning

- [ ] Versioning strategy selected and applied uniformly
- [ ] Breaking vs non-breaking change policy documented
- [ ] Deprecation timeline communicated via `Sunset` header

### CORS

- [ ] Allowed origins configured (no wildcard `*` in production with credentials)
- [ ] Allowed methods and headers explicitly listed
- [ ] Preflight (`OPTIONS`) requests handled correctly

### Documentation

- [ ] OpenAPI / Swagger spec generated and up to date
- [ ] Every endpoint has description, parameters, and example responses
- [ ] Authentication requirements documented
- [ ] Error codes and meanings listed
- [ ] Changelog maintained for each version

### Security

- [ ] Input validation on all fields
- [ ] SQL injection prevention
- [ ] HTTPS enforced
- [ ] Sensitive data never in URLs or logs
- [ ] CORS configured correctly

### Monitoring

- [ ] Structured logging with request IDs
- [ ] Error tracking configured (Sentry, Datadog, etc.)
- [ ] Performance metrics collected (latency, error rate)
- [ ] Health check endpoint available (`/health`)
- [ ] Alerts configured for error rate spikes

---

## Skill Routing Table

| Need | Skill | Purpose |
|------|-------|---------|
| API design principles | `api-design` | Resource modeling, HTTP semantics, pagination, error formats |
| Versioning strategy | `api-versioning` | Version lifecycle, deprecation, migration patterns |
| Authentication | `auth-patterns` | JWT, OAuth2, sessions, RBAC, MFA |
| Error handling | `error-handling` | Error types, retry patterns, circuit breakers, HTTP errors |
| Rate limiting | `rate-limiting` | Algorithms, HTTP headers, tiered limits, distributed limiting |
| Caching | `caching` | Cache strategies, HTTP caching, invalidation, Redis patterns |
| Database migrations | `database-migrations` | Schema evolution, zero-downtime patterns, rollback strategies |

---

## NEVER Do

1. **NEVER skip the design phase** — jumping straight to code produces inconsistent APIs that are expensive to fix
2. **NEVER expose database schema directly** — API resources are not database tables; design around consumer use cases
3. **NEVER ship without authentication** — every production endpoint must have an auth strategy
4. **NEVER return inconsistent error formats** — every error response must follow the same schema
5. **NEVER break a published API without a versioning plan** — breaking changes require a new version, migration guide, and deprecation timeline
6. **NEVER deploy without tests and documentation** — untested APIs ship bugs, undocumented APIs frustrate developers
