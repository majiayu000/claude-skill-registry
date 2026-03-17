---
name: nean-sec
description: Security policy for NEAN apps. Enforces OWASP Top 10 and CWE Top 25 mitigations.
---

## Purpose

Ensure NEAN code is secure by default. For security output format and core refusal policy, see `/shared-sec-baseline`.

## NEAN-specific security concerns (always check)

1. **SQL injection** — use TypeORM parameterized queries; never interpolate user input into raw SQL
2. **Input validation** — class-validator decorators on all DTOs at every API boundary
3. **XSS** — Angular sanitizes by default; audit `[innerHTML]` and `bypassSecurityTrust*` usage
4. **CSRF** — required when using cookie-based auth; implement CSRF tokens or use SameSite=Strict
5. **Auth/authz gaps** — verify authorization in NestJS guards on every protected endpoint, not just frontend
6. **Token storage** — avoid localStorage for sensitive tokens; prefer httpOnly cookies for refresh tokens
7. **Mass assignment** — use DTOs with explicit properties; never spread request body directly into entities

## Standard security (brief check)

- Error responses: safe exception filters, no stack traces or internal details
- Rate limiting: on auth endpoints, expensive operations, public APIs
- Dependencies: lockfile committed, no known critical vulnerabilities
- Security headers: Helmet middleware configured

## Reference

For detailed OWASP/CWE mitigation patterns, see `reference/nean-sec-reference.md`
