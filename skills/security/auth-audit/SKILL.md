---
name: auth-audit
description: Audit authentication and authorization patterns. Checks JWT, sessions, OAuth2, PKCE implementations for security best practices and common vulnerabilities.
argument-hint: "[--jwt] [--session] [--oauth]"
user-invocable: true
---

# Auth Audit Skill

## Overview

Comprehensive audit of authentication and authorization implementations.

## Audit Categories

| Category | Checks |
|----------|--------|
| JWT | Signing algo, expiration, refresh, storage |
| Sessions | Storage, expiry, regeneration, fixation |
| OAuth2 | PKCE, state param, redirect validation |
| Passwords | Hashing algo, strength rules, reset flow |
| MFA | Implementation, backup codes, recovery |

## Workflow

1. **Detect** auth implementation (JWT, sessions, OAuth)
2. **Scan** for known anti-patterns
3. **Verify** cryptographic choices
4. **Check** token/session lifecycle
5. **Audit** authorization logic (RBAC, ABAC)

## Common Vulnerabilities

- JWT signed with `none` algorithm
- JWT secret too short (< 256 bits)
- No token expiration or too long
- Refresh tokens stored in localStorage
- Session fixation after login
- Missing CSRF protection
- OAuth without PKCE for public clients
- Missing `state` parameter in OAuth flow

## References

- [Auth Patterns](references/auth-patterns.md)
- [Auth Checklist](references/templates/auth-checklist.md)
