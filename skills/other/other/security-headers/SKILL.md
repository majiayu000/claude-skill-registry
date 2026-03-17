---
name: security-headers
description: Verify and configure HTTP security headers (CSP, HSTS, CORS, X-Frame-Options, etc). Checks current configuration and generates framework-specific fixes.
argument-hint: "[framework]"
user-invocable: true
---

# Security Headers Skill

## Overview

Audit and configure HTTP security headers for web applications.

## Required Headers

| Header | Purpose | Severity if Missing |
|--------|---------|-------------------|
| Content-Security-Policy | Prevent XSS/injection | HIGH |
| Strict-Transport-Security | Force HTTPS | HIGH |
| X-Content-Type-Options | Prevent MIME sniffing | MEDIUM |
| X-Frame-Options | Prevent clickjacking | MEDIUM |
| Referrer-Policy | Control referrer info | LOW |
| Permissions-Policy | Control browser features | LOW |
| X-XSS-Protection | Legacy XSS filter | LOW |

## Workflow

1. **Detect** framework (Next.js, Laravel, Express, etc.)
2. **Check** current header configuration
3. **Compare** against security best practices
4. **Generate** framework-specific configuration
5. **Validate** headers are properly set

## Detection Points

| Framework | Config Location |
|-----------|----------------|
| Next.js | `next.config.js` headers, `middleware.ts` |
| Laravel | `SecurityHeaders` middleware |
| Express | `helmet` middleware |
| Django | `SECURE_*` settings |

## References

- [Headers Reference](references/headers-reference.md)
- [Config Templates](references/templates/headers-config.md)
