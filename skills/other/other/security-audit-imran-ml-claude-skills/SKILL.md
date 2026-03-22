---
name: security-audit
description: |
  Use this skill to perform a security audit, scan for vulnerabilities,
  check OWASP Top 10 issues, or review code for security problems.
  Triggered by "security audit", "check security", "find vulnerabilities".
argument-hint: "[path or component]"
allowed-tools: "Read, Grep, Glob, Bash"
context: fork
agent: Explore
---

# Security Audit

Perform a comprehensive security review using OWASP Top 10 as a framework.

## Scope

Target: `$ARGUMENTS` (or entire codebase if not specified)

## Checklist

### A01 — Broken Access Control
- [ ] Authorization checks on every protected route/endpoint
- [ ] Horizontal privilege escalation (can user A access user B's data?)
- [ ] IDOR (insecure direct object references) in API endpoints
- [ ] Missing authentication middleware

### A02 — Cryptographic Failures
- [ ] Sensitive data stored/transmitted in plaintext
- [ ] Weak hash algorithms (MD5, SHA1 for passwords)
- [ ] Hardcoded secrets, API keys, or passwords in source
- [ ] TLS not enforced in production config

### A03 — Injection
- [ ] SQL injection (raw queries with user input)
- [ ] Command injection (shell exec with user data)
- [ ] XSS (unsanitized HTML output)
- [ ] LDAP, NoSQL, XML injection

### A04 — Insecure Design
- [ ] Missing rate limiting on auth endpoints
- [ ] No brute-force protection on login
- [ ] Sensitive operations lack confirmation step

### A05 — Security Misconfiguration
- [ ] Debug mode enabled in production config
- [ ] Verbose error messages exposing internals
- [ ] Default credentials not changed
- [ ] Unnecessary services/ports exposed
- [ ] Missing security headers (CSP, HSTS, X-Frame-Options)

### A06 — Vulnerable Components
```bash
npm audit
# or: pip-audit / safety check / snyk test
```

### A07 — Authentication Failures
- [ ] Weak password policy
- [ ] Session tokens not invalidated on logout
- [ ] Missing MFA for sensitive operations
- [ ] JWT: algorithm confusion, weak secret, no expiry

### A08 — Software Integrity Failures
- [ ] Subresource Integrity (SRI) for external scripts
- [ ] CI/CD pipeline integrity

### A09 — Logging Failures
- [ ] Sensitive data logged (passwords, tokens, PII)
- [ ] Failed auth attempts not logged
- [ ] No audit trail for admin actions

### A10 — Server-Side Request Forgery (SSRF)
- [ ] Unvalidated URL parameters used in server requests
- [ ] Internal network accessible via user-controlled URLs

## Output Format

```
## Security Audit Report

### Critical (fix immediately)
- [file:line] VULN_TYPE — description + remediation

### High (fix before next release)
- [file:line] VULN_TYPE — description + remediation

### Medium (fix in next sprint)
- [file:line] VULN_TYPE — description

### Low / Informational
- [finding] — recommendation

### Dependency Vulnerabilities
[npm audit / pip-audit output summary]

### Score: X/10 critical issues found
```

$ARGUMENTS
