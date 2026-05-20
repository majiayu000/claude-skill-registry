---
name: security-review
description: Security review checklist for web applications. Use when reviewing code for security vulnerabilities, auth issues, input validation, or any security-sensitive code.
---

# Security Review Checklist

## Authentication & Authorization
- [ ] Passwords hashed with bcrypt/argon2 (NEVER md5/sha1/plain)
- [ ] JWT tokens have expiry (access: 15min, refresh: 7d)
- [ ] JWT secret is long (32+ chars), loaded from env var
- [ ] Refresh token rotation implemented (old token invalidated on use)
- [ ] Rate limiting on login (max 5 attempts, then lockout/slowdown)
- [ ] CSRF protection on state-changing endpoints (cookies)
- [ ] Auth check on EVERY protected route (not just the frontend)
- [ ] Admin endpoints have separate, stricter auth check

## Input Validation
- [ ] ALL user input validated server-side (never trust client)
- [ ] File uploads: check MIME type, extension, size limit, scan for malware
- [ ] URL parameters parsed and validated (no direct string concat in SQL)
- [ ] JSON bodies have max size limit (e.g., 1MB)
- [ ] HTML/Markdown user content sanitized before rendering (XSS)

## SQL & Data
- [ ] ALL queries use parameterized statements (no f-string SQL)
- [ ] ORM used for CRUD — raw SQL only for complex analytics
- [ ] Database user has minimum required permissions (not superuser)
- [ ] Sensitive fields (password, SSN, CC) never returned in API responses
- [ ] PII encrypted at rest for sensitive columns

## API Security
- [ ] CORS: explicit allowed origins (never `*` in production)
- [ ] Security headers: X-Content-Type-Options, X-Frame-Options, CSP
- [ ] HTTPS enforced (redirect HTTP → HTTPS)
- [ ] API keys/secrets never logged or included in error messages
- [ ] 4xx errors don't reveal internal details (stack traces, file paths)

## Dependency Security
- [ ] No known CVEs in dependencies (run: pip audit / npm audit)
- [ ] Dependencies pinned to exact versions
- [ ] Secrets never in code or git history (use env vars / secrets manager)
- [ ] .env files in .gitignore

## Common Vulnerabilities to Check
```
OWASP Top 10:
1. Broken Access Control — can user A see/edit user B's data?
2. Cryptographic Failures — are secrets/passwords properly protected?
3. Injection — SQL, command, LDAP injection possible?
4. Insecure Design — is auth logic correct by design?
5. Security Misconfiguration — debug mode on? default credentials?
6. Vulnerable Components — any known CVEs in deps?
7. Auth Failures — session fixation? weak tokens?
8. Data Integrity — deserialization attacks? tampered JWTs?
9. Logging Failures — are attacks logged? are secrets in logs?
10. SSRF — can attacker make server fetch internal URLs?
```

## Issue Format
For each finding:
[CRITICAL|HIGH|MEDIUM|LOW] file.py:line — description — exact fix recommendation
