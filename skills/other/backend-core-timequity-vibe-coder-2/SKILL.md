---
name: backend-core
description: |
  Language-agnostic backend patterns: API design, authentication, security, databases.
  Use when: designing APIs, implementing auth, securing endpoints, modeling data.
  Triggers: "api design", "rest api", "graphql", "authentication", "jwt", "oauth",
  "security", "owasp", "database schema", "migrations", "sql".
---

# Backend Core Patterns

## Quick Reference

| Topic | When to Use | Reference |
|-------|-------------|-----------|
| API Design | REST/GraphQL/gRPC endpoints | [api-design.md](references/api-design.md) |
| Authentication | JWT, OAuth, sessions, magic links | [authentication.md](references/authentication.md) |
| Security | Input validation, OWASP, rate limiting | [security.md](references/security.md) |
| Databases | Schema design, migrations, queries | [databases.md](references/databases.md) |

## API Design Decision Tree

```
What type of API?
├─ Public API → REST + OpenAPI spec
├─ Internal microservices → gRPC (performance) or REST (simplicity)
├─ Real-time → WebSocket or SSE
└─ Complex queries → GraphQL
```

## Auth Decision Tree

```
Auth method?
├─ SPA/Mobile → JWT (access + refresh tokens)
├─ Server-rendered → Session cookies
├─ Third-party login → OAuth 2.0 / OIDC
├─ Passwordless → Magic link (email) or WebAuthn
└─ API-to-API → API keys or mTLS
```

## Security Essentials

**Always:**
- Validate all inputs at boundaries
- Use parameterized queries (never string concat SQL)
- Hash passwords with bcrypt/argon2 (cost ≥ 10)
- HTTPS everywhere, HSTS headers
- Rate limit auth endpoints

**Never:**
- Store secrets in code or git
- Trust client-side validation alone
- Log sensitive data (passwords, tokens, PII)
- Use MD5/SHA1 for passwords

## Database Patterns

```
Schema design:
├─ Start normalized (3NF)
├─ Denormalize only for proven bottlenecks
├─ Always have created_at, updated_at
├─ Use UUIDs for public IDs, integers for internal FKs
└─ Soft delete (deleted_at) for important data
```

## Anti-patterns

| Don't | Do Instead |
|-------|------------|
| N+1 queries | Eager load / batch queries |
| SELECT * | Select only needed columns |
| No indexes on WHERE/JOIN columns | Add indexes |
| Storing files in DB | Use object storage (S3, R2) |
| God objects | Bounded contexts, single responsibility |
