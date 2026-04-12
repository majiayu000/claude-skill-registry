---
name: security-review
description: "OWASP secure design review for code and architecture. Checks input validation, authentication, authorization, data protection."
---

# Security Review

Language-agnostic security review based on OWASP Secure by Design.

## Checklist (OWASP Top 10)

### 1. Injection Prevention
- [ ] All user input validated (type, length, range, format)
- [ ] Parameterized queries for ALL data access (never string concatenation)
- [ ] Input allowlisting preferred over denylisting

### 2. Authentication
- [ ] Passwords hashed with bcrypt/argon2 (never MD5/SHA1)
- [ ] Session IDs regenerated on login
- [ ] Multi-factor authentication available for sensitive operations

### 3. Sensitive Data
- [ ] Data encrypted at rest and in transit (TLS 1.2+)
- [ ] No secrets in code, logs, or error messages
- [ ] PII identified and classified in threat model

### 4. Access Control
- [ ] Least privilege enforced (users get minimum permissions needed)
- [ ] Authorization checked on EVERY request (not just the first)
- [ ] CORS restrictive (not `*`)

### 5. Security Misconfiguration
- [ ] Default credentials changed
- [ ] Unnecessary features/ports disabled
- [ ] Security headers set (CSP, HSTS, X-Frame-Options, X-Content-Type-Options)

### 6. XSS Prevention
- [ ] Output encoded based on context (HTML, JS, URL, CSS)
- [ ] Content Security Policy configured
- [ ] User-generated content sanitized

### 7. Dependencies
- [ ] Dependency audit run (no known critical vulnerabilities)
- [ ] Dependencies pinned to specific versions
- [ ] Automated scanning in CI

### 8. Logging & Monitoring
- [ ] Security events logged (login attempts, auth failures, access denials)
- [ ] No sensitive data in logs
- [ ] Alerting on anomalous patterns

## Stack-Specific Tools
Consult `.claude/jit-tooling/security-scanning.md` for tool selection per stack.
