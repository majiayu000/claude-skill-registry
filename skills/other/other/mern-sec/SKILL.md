---
name: mern-sec
description: Security policy for MERN apps. Enforces OWASP Top 10 and CWE Top 25 mitigations.
---

## Purpose

Ensure MERN code is secure by default. For security output format and core refusal policy, see `/shared-sec-baseline`.

## MERN-specific security concerns (always check)

1. **NoSQL injection** — reject `$`-prefixed and dot-notation keys from user input
2. **Input validation** — schema validation (Zod/Joi) at every API boundary
3. **XSS** — React escapes by default; audit `dangerouslySetInnerHTML` and raw HTML rendering
4. **CSRF** — required when using cookie-based auth; use tokens or SameSite=Strict
5. **Auth/authz gaps** — verify authorization on every protected route handler, not just frontend
6. **Token storage** — avoid localStorage for sensitive tokens without justification; prefer httpOnly cookies

## Standard security (brief check)

- Error responses: safe envelopes, no stack traces or internal details
- Rate limiting: on auth endpoints, expensive operations, public APIs
- Dependencies: lockfile committed, no known critical vulnerabilities

## Reference

For detailed OWASP/CWE mitigation patterns, see `reference/mern-sec-reference.md`
