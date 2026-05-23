---
name: dev-api-design
description: Production-grade API design patterns for REST, GraphQL, and gRPC. Covers API architecture, OpenAPI/Swagger specs, versioning strategies, authentication flows, rate limiting, pagination, error handling, and documentation best practices for modern API development.
---

# API Development & Design — Quick Reference

This skill provides execution-ready patterns for designing, implementing, and documenting production-grade APIs. Claude should apply these patterns when users need REST API design, GraphQL schemas, OpenAPI specifications, API versioning, authentication flows, or API documentation.

**Modern Best Practices (Dec 2025)**: HTTP semantics and cacheability (RFC 9110), Problem Details error model (RFC 9457), OpenAPI 3.1, API-first + contract testing, strong AuthN/Z boundaries, explicit versioning/deprecation, and operable-by-default APIs (rate limits, idempotency, observability).

---

## When to Use This Skill

Claude should invoke this skill when a user requests:

- REST API design and endpoint structure
- GraphQL schema design and resolver patterns
- gRPC service definitions and protocol buffers
- OpenAPI/Swagger specification creation
- API versioning strategies (URL, header, content negotiation)
- Authentication and authorization flows (JWT, OAuth2, API keys)
- Rate limiting, throttling, and quota management
- API pagination, filtering, and sorting patterns
- Error response standardization
- API documentation and developer portals
- API security best practices (OWASP API Security Top 10)
- API testing strategies (contract testing, mock servers)
- API gateway configuration and management

---

## Quick Reference

| Task | Pattern/Tool | Key Elements | When to Use |
|------|--------------|--------------|-------------|
| **Design REST API** | RESTful Design | Nouns (not verbs), HTTP methods, proper status codes | Resource-based APIs, CRUD operations |
| **Version API** | URL Versioning | `/api/v1/resource`, `/api/v2/resource` | Breaking changes, client migration |
| **Paginate results** | Cursor-Based | `cursor=eyJpZCI6MTIzfQ&limit=20` | Real-time data, large collections |
| **Handle errors** | RFC 9457 Problem Details | `type`, `title`, `status`, `detail`, `errors[]` | Consistent error responses |
| **Authenticate** | JWT Bearer | `Authorization: Bearer <token>` | Stateless auth, microservices |
| **Rate limit** | Token Bucket | `X-RateLimit-*` headers, 429 responses | Prevent abuse, fair usage |
| **Document API** | OpenAPI 3.1 | Swagger UI, Redoc, code samples | Interactive docs, client SDKs |
| **Flexible queries** | GraphQL | Schema-first, resolvers, DataLoader | Client-driven data fetching |
| **High-performance** | gRPC + Protobuf | Binary protocol, streaming | Internal microservices |

---

## Decision Tree: Choosing API Style

```text
User needs: [API Type]
    ├─ Public API for third parties?
    │   └─ REST with OpenAPI docs (broad compatibility)
    │
    ├─ Internal microservices?
    │   ├─ High throughput required? → **gRPC** (binary, fast)
    │   └─ Simple CRUD? → **REST** (easy to debug)
    │
    ├─ Client needs flexible queries?
    │   ├─ Real-time updates? → **GraphQL Subscriptions** or **WebSockets**
    │   └─ Complex data fetching? → **GraphQL** (avoid over-fetching)
    │
    ├─ Mobile/web clients?
    │   ├─ Many entity types? → **GraphQL** (single endpoint)
    │   └─ Simple resources? → **REST** (cacheable)
    │
    └─ Streaming or bidirectional?
        └─ **gRPC** (HTTP/2 streaming) or **WebSockets**
```

---

## Navigation: Core API Patterns

### RESTful API Design

**Resource:** [resources/restful-design-patterns.md](resources/restful-design-patterns.md)

- Resource-based URLs with proper HTTP methods (GET, POST, PUT, PATCH, DELETE)
- HTTP status code semantics (200, 201, 404, 422, 500)
- Idempotency guarantees (GET, PUT, DELETE)
- Stateless design principles
- URL structure best practices (collection vs resource endpoints)
- Nested resources and action endpoints

---

### Pagination, Filtering & Sorting

**Resource:** [resources/pagination-filtering.md](resources/pagination-filtering.md)

- Offset-based pagination (simple, static datasets)
- Cursor-based pagination (real-time feeds, recommended)
- Page-based pagination (UI with page numbers)
- Query parameter filtering with operators (`_gt`, `_contains`, `_in`)
- Multi-field sorting with direction (`-created_at`)
- Performance optimization with indexes

---

### Error Handling

**Resource:** [resources/error-handling-patterns.md](resources/error-handling-patterns.md)

- RFC 9457 Problem Details standard
- HTTP status code reference (4xx client errors, 5xx server errors)
- Field-level validation errors
- Trace IDs for debugging
- Consistent error format across endpoints
- Security-safe error messages (no stack traces in production)

---

### Authentication & Authorization

**Resource:** [resources/authentication-patterns.md](resources/authentication-patterns.md)

- JWT (JSON Web Tokens) with refresh token rotation
- OAuth2 Authorization Code Flow for third-party auth
- API Key authentication for server-to-server
- RBAC (Role-Based Access Control)
- ABAC (Attribute-Based Access Control)
- Resource-based authorization (user-owned resources)

---

### Rate Limiting & Throttling

**Resource:** [resources/rate-limiting-patterns.md](resources/rate-limiting-patterns.md)

- Token Bucket algorithm (recommended, allows bursts)
- Fixed Window vs Sliding Window
- Rate limit headers (`X-RateLimit-*`)
- Tiered rate limits (free, paid, enterprise)
- Redis-based distributed rate limiting
- Per-user, per-endpoint, and per-API-key strategies

---

## Navigation: Extended Resources

### API Design & Best Practices

- **[api-design-best-practices.md](resources/api-design-best-practices.md)** - Comprehensive API design principles
- **[versioning-strategies.md](resources/versioning-strategies.md)** - URL, header, and query parameter versioning
- **[api-security-checklist.md](resources/api-security-checklist.md)** - OWASP API Security Top 10

### GraphQL & gRPC

- **[graphql-patterns.md](resources/graphql-patterns.md)** - Schema design, resolvers, N+1 queries, DataLoader
- **gRPC patterns** - See [software-backend](../software-backend/SKILL.md) for Protocol Buffers and service definitions

### OpenAPI & Documentation

- **[openapi-guide.md](resources/openapi-guide.md)** - OpenAPI 3.1 specifications, Swagger UI, Redoc
- **Templates:** [templates/openapi-template.yaml](templates/openapi-template.yaml) - Complete OpenAPI spec example

### Optional: AI/Automation (LLM/Agent APIs)

- **[llm-agent-api-contracts.md](resources/llm-agent-api-contracts.md)** - Streaming, long-running jobs, safety guardrails, observability

---

## Navigation: Templates

Production-ready, copy-paste API implementations with authentication, database, validation, and docs.

### Framework-Specific Templates

- **FastAPI (Python)**: [templates/fastapi/fastapi-complete-api.md](templates/fastapi/fastapi-complete-api.md)
  - Async/await, Pydantic v2, JWT auth, SQLAlchemy 2.0, pagination, OpenAPI docs

- **Express.js (Node/TypeScript)**: [templates/express-nodejs/express-complete-api.md](templates/express-nodejs/express-complete-api.md)
  - TypeScript, Zod validation, Prisma ORM, JWT refresh tokens, rate limiting

- **Django REST Framework**: [templates/django-rest/django-rest-complete-api.md](templates/django-rest/django-rest-complete-api.md)
  - ViewSets, serializers, Simple JWT, permissions, DRF filtering/pagination

- **Spring Boot (Java)**: [templates/spring-boot/spring-boot-complete-api.md](templates/spring-boot/spring-boot-complete-api.md)
  - Spring Security JWT, Spring Data JPA, Bean Validation, Springdoc OpenAPI

### Cross-Platform Patterns

- **[api-patterns-universal.md](templates/cross-platform/api-patterns-universal.md)** - Universal patterns for all frameworks
  - Authentication strategies, pagination, caching, versioning, validation
- **[template-api-governance.md](templates/cross-platform/template-api-governance.md)** - **NEW** API governance, deprecation, multi-tenancy
  - Deprecation policy (90-day timeline), backward compatibility rules, error model templates
- **[template-api-design-review-checklist.md](templates/cross-platform/template-api-design-review-checklist.md)** - Production API review checklist (security, reliability, operability)
- **[template-api-error-model.md](templates/cross-platform/template-api-error-model.md)** - RFC 9457 Problem Details + stable error code registry

---

## Do / Avoid

### GOOD: Do

- Version APIs from day one
- Document deprecation policy before first deprecation
- Use semantic versioning for API versions
- Include trace IDs in all error responses
- Return appropriate HTTP status codes
- Implement rate limiting with clear headers
- Use RFC 9457 Problem Details for errors

### BAD: Avoid

- Removing fields without deprecation period
- Changing field types in existing versions
- Using verbs in resource names (nouns only)
- Returning 500 for client errors
- Breaking changes without major version bump
- Mixing tenant data without explicit isolation
- Action endpoints everywhere (/doSomething)

---

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| **Instant deprecation** | Breaks clients | 90-day minimum sunset period |
| **Action endpoints** | Inconsistent API | Use resources + HTTP verbs |
| **Version in body** | Hard to route, debug | Version in URL or header |
| **Generic errors** | Poor DX | Specific error codes + messages |
| **No rate limit headers** | Clients can't back off | Include X-RateLimit-* |
| **Tenant ID in URL only** | Forgery risk | Validate against auth token |
| **Leaky abstractions** | Tight coupling | Design stable contracts |

---

## Optional: AI/Automation

> **Note**: AI tools assist but contracts need human review.

- **OpenAPI linting** — Spectral, Redocly in CI/CD
- **Breaking change detection** — oasdiff automated checks
- **SDK generation** — From OpenAPI spec on changes
- **Contract testing** — Pact, Dredd automation

### Bounded Claims

- AI-generated OpenAPI specs require human review
- Automated deprecation detection needs manual confirmation
- SDK generation requires type verification

---

## External Resources

See [data/sources.json](data/sources.json) for:

- Official REST, GraphQL, gRPC documentation
- OpenAPI/Swagger tools and validators
- API design style guides (Google, Microsoft, Stripe)
- Security standards (OWASP API Security Top 10)
- Testing tools (Postman, Insomnia, Paw)

---

## Quick Decision Matrix

| Scenario | Recommendation |
|----------|----------------|
| Public API for third parties | REST with OpenAPI docs |
| Internal microservices | gRPC for performance, REST for simplicity |
| Client needs flexible queries | GraphQL |
| Real-time updates | GraphQL Subscriptions or WebSockets |
| Simple CRUD operations | REST |
| Complex data fetching | GraphQL |
| High throughput required | gRPC |
| Mobile/web clients | REST or GraphQL |

---

## Anti-Patterns to Avoid

- **Verbs in URLs**: `/getUserById` → `/users/:id`
- **Ignoring HTTP methods**: Using GET for mutations
- **No versioning**: Breaking changes without version bump
- **Inconsistent error format**: Different error structures per endpoint
- **Missing pagination**: Returning unbounded lists
- **No rate limiting**: Allowing unlimited requests
- **Poor documentation**: Missing examples, outdated specs
- **Security by obscurity**: Not using HTTPS, weak auth

---

## Related Skills

This skill works best when combined with other specialized skills:

### Backend Development

- **[software-backend](../software-backend/SKILL.md)** - Production backend patterns (Node.js, Python, Java frameworks)
  - Use when implementing API server infrastructure
  - Covers database integration, middleware, error handling

### Security & Authentication

- **[software-security-appsec](../software-security-appsec/SKILL.md)** - Application security patterns
  - Critical for securing API endpoints
  - Covers OWASP vulnerabilities, authentication flows, input validation

### Database & Data Layer

- **[data-sql-optimization](../data-sql-optimization/SKILL.md)** - SQL optimization and database patterns
  - Essential for API performance (query optimization, indexing)
  - Use when APIs interact with relational databases

### Testing & Quality

- **[qa-testing-strategy](../qa-testing-strategy/SKILL.md)** - Test strategy and automation
  - Contract testing for API specifications
  - Integration testing for API endpoints

### DevOps & Deployment

- **[ops-devops-platform](../ops-devops-platform/SKILL.md)** - Platform engineering and deployment
  - API gateway configuration
  - CI/CD pipelines for API deployments

### Documentation

- **[docs-codebase](../docs-codebase/SKILL.md)** - Technical documentation standards
  - API reference documentation structure
  - Complements OpenAPI auto-generated docs

### Architecture

- **[software-architecture-design](../software-architecture-design/SKILL.md)** - System design patterns
  - Microservices architecture with APIs
  - API gateway patterns, service mesh integration

### Performance & Observability

- **[qa-observability](../qa-observability/SKILL.md)** - Performance optimization and monitoring
  - API latency monitoring, distributed tracing
  - Performance budgets for API endpoints

---

## Usage Notes

**For Claude:**

- Apply RESTful principles by default unless user requests GraphQL/gRPC
- Always include pagination for list endpoints
- Use RFC 9457 format for error responses
- Include authentication in all templates (JWT or API keys)
- Reference framework-specific templates for complete implementations
- Link to relevant resources for deep-dive guidance

**Success Criteria:** APIs are discoverable, consistent, well-documented, secure, and follow HTTP/GraphQL semantics correctly.
