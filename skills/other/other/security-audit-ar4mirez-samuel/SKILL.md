---
name: security-audit
description: Security assessment workflow. Use when reviewing code for vulnerabilities, performing OWASP checks, auditing authentication/authorization logic, or validating security controls before deployment.
license: MIT
metadata:
  author: samuel
  version: "1.0"
  category: workflow
---

# Security Audit Skill

Proactive security assessment covering OWASP Top 10, dependency vulnerabilities, secrets detection, and security best practices.

---

## When to Use

| Trigger | Priority | Description |
|---------|----------|-------------|
| **Pre-Production** | Critical | Before any production deployment |
| **Monthly Review** | High | Regular security hygiene |
| **Auth Changes** | Critical | After adding/modifying authentication |
| **External Integration** | High | When adding third-party services |
| **Dependency Updates** | Medium | After major dependency changes |
| **Security Incident** | Critical | Post-incident review |

---

## Audit Scope

### Full Audit
Complete security review across all categories. Time: 2-4 hours.

### Focused Audit
Target specific area (e.g., authentication only). Time: 30-60 minutes.

### Quick Scan
Automated checks only (dependencies, secrets). Time: 5-10 minutes.

---

## Prerequisites

Before starting audit:

- [ ] Access to codebase and dependencies
- [ ] Access to environment configuration (sanitized)
- [ ] List of external services/APIs used
- [ ] Authentication flow documentation (if exists)
- [ ] Previous audit reports (if available)

---

## Audit Process

```
Phase 1: OWASP Top 10 Review
    ↓
Phase 2: Dependency Vulnerability Scan
    ↓
Phase 3: Secrets Detection
    ↓
Phase 4: Input Validation Audit
    ↓
Phase 5: Authentication & Authorization
    ↓
Phase 6: API Security
    ↓
Phase 7: Report & Remediation
```

---

## Phase 1: OWASP Top 10 Review

### Quick Reference

| ID | Category | Key Check |
|----|----------|-----------|
| A01 | Broken Access Control | Authorization on all endpoints |
| A02 | Cryptographic Failures | TLS, password hashing, encryption |
| A03 | Injection | Parameterized queries, input escaping |
| A04 | Insecure Design | Defense in depth, trust boundaries |
| A05 | Security Misconfiguration | Headers, defaults, error messages |
| A06 | Vulnerable Components | Dependency scanning |
| A07 | Authentication Failures | Password policy, session security |
| A08 | Data Integrity | Checksums, secure CI/CD |
| A09 | Logging Failures | Security event logging |
| A10 | SSRF | URL validation, network restrictions |

**For detailed patterns and examples**: See `references/process.md`

### Critical Checks

**A01 - Broken Access Control**:
```
- [ ] All endpoints have authorization checks
- [ ] RBAC implemented
- [ ] No direct object reference vulnerabilities
- [ ] Privilege escalation prevented
```

**A02 - Cryptographic Failures**:
```
- [ ] Passwords hashed with bcrypt/argon2 (cost 10+)
- [ ] TLS 1.2+ enforced
- [ ] Sensitive data encrypted at rest
- [ ] Cryptographically random tokens
```

**A03 - Injection**:
```
- [ ] SQL queries use parameterized statements
- [ ] Template engines auto-escape output
- [ ] No shell command execution with user input
- [ ] NoSQL queries sanitized
```

**A05 - Security Misconfiguration**:
```
Required Headers:
- X-Content-Type-Options: nosniff
- X-Frame-Options: DENY
- Content-Security-Policy: default-src 'self'
- Strict-Transport-Security: max-age=31536000
```

---

## Phase 2: Dependency Vulnerability Scan

### Run Audit Commands

```bash
# Node.js
npm audit
npm audit --audit-level=moderate

# Python
pip-audit
# Or: safety check --json > audit-report.json

# Go
govulncheck ./...

# Rust
cargo audit

# Ruby
bundle audit check
```

### Severity Response

| Severity | Action | Timeline |
|----------|--------|----------|
| Critical | Immediate fix or remove | Hours |
| High | Fix in current sprint | Days |
| Moderate | Schedule fix | Weeks |
| Low | Track for update | Next release |

---

## Phase 3: Secrets Detection

### Automated Scanning

```bash
# Using gitleaks (recommended)
gitleaks detect --source . --verbose

# Using git-secrets
git secrets --scan
git secrets --scan-history

# Using truffleHog
trufflehog filesystem .
```

### Common Secret Patterns

| Pattern | Example | Risk |
|---------|---------|------|
| API Keys | `sk_live_`, `AKIA` | High |
| Passwords | `password=`, `passwd` | Critical |
| Tokens | `token=`, `bearer` | High |
| Private Keys | `-----BEGIN RSA` | Critical |
| AWS Credentials | `aws_access_key_id` | Critical |

### Environment Variables

```
Checklist:
- [ ] All secrets in environment variables (not code)
- [ ] .env files in .gitignore
- [ ] No .env files in git history
- [ ] Secure defaults for all variables
```

---

## Phase 4: Input Validation Audit

### Input Sources by Risk

| Source | Examples | Risk |
|--------|----------|------|
| File uploads | Images, documents | Critical |
| Request body | JSON, form data | High |
| URL parameters | `/users/:id` | High |
| Query strings | `?search=term` | High |
| Headers | Custom headers | Medium |
| Cookies | Session cookies | Medium |

### Validation Checklist

For each input:

- [ ] Schema validation (Zod, Pydantic, etc.)
- [ ] Type checking enforced
- [ ] Length/size limits
- [ ] Format validation (email, URL)
- [ ] Allowlist when possible
- [ ] Sanitized for output context

### File Upload Requirements

```
- [ ] Magic bytes validation (not just extension)
- [ ] Size limits enforced
- [ ] Virus/malware scanning
- [ ] Storage outside web root
- [ ] Randomized filenames
- [ ] No executable permissions
```

---

## Phase 5: Authentication & Authorization

### Password Security

```
- [ ] Min length: 12+ characters
- [ ] Bcrypt (cost 10+) or argon2
- [ ] No passwords in logs/errors
- [ ] Rate limiting on login
- [ ] Account lockout policy
```

### Session Security

```
- [ ] HttpOnly cookie flag
- [ ] Secure cookie flag (HTTPS)
- [ ] SameSite attribute
- [ ] Session timeout
- [ ] Invalidation on logout
- [ ] Regenerate on privilege change
```

### Authorization

```
- [ ] Check on every endpoint
- [ ] RBAC implemented
- [ ] Least privilege
- [ ] Deny by default
- [ ] Server-side validation
```

### Token Security (JWT/OAuth)

```
- [ ] Strong algorithm (RS256, ES256)
- [ ] Token expiration
- [ ] Refresh mechanism
- [ ] Revocation capability
- [ ] No sensitive data in payload
```

---

## Phase 6: API Security

### Rate Limiting

```
- [ ] Enabled on all endpoints
- [ ] Stricter on auth endpoints
- [ ] Per-user and per-IP
- [ ] Graduated response
```

### CORS

```javascript
// Secure configuration
{
  origin: ['https://app.example.com'],  // Not '*'
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE']
}
```

### Error Handling

```
- [ ] Generic messages to clients
- [ ] Details in logs only
- [ ] No stack traces in production
- [ ] Consistent format
```

---

## Phase 7: Report & Remediation

### Report Template

```markdown
# Security Audit Report

**Date**: YYYY-MM-DD
**Auditor**: [Name]
**Scope**: [Full/Focused/Quick]
**Duration**: [Hours]

## Executive Summary

| Severity | Count | Status |
|----------|-------|--------|
| Critical | N | [Status] |
| High | N | [Status] |
| Medium | N | [Status] |
| Low | N | [Status] |

**Overall Risk**: [Low/Medium/High/Critical]

## Findings

### [Severity]: [Issue Title]
**Location**: [File:Line]
**Description**: [Brief description]
**Impact**: [Potential impact]
**Remediation**: [How to fix]
**Timeline**: [When to fix]

## Recommendations

1. [Recommendation 1]
2. [Recommendation 2]

## Tools Used

- [Tool 1]
- [Tool 2]
```

### Priority Matrix

| Finding | Severity | Effort | Priority |
|---------|----------|--------|----------|
| SQL Injection | Critical | Low | Immediate |
| Missing Auth | High | Medium | Sprint 1 |
| Weak Hash | High | Low | Sprint 1 |
| Missing Headers | Medium | Low | Sprint 2 |
| Old Dependency | Low | Low | Backlog |

### Follow-up

- [ ] Create tickets for findings
- [ ] Schedule remediation
- [ ] Plan re-audit
- [ ] Update documentation
- [ ] Brief team

---

## Quick Scan Commands

```bash
# Node.js
npm audit && npx gitleaks detect

# Python
pip-audit && gitleaks detect

# Go
govulncheck ./... && gitleaks detect

# Rust
cargo audit && gitleaks detect
```

---

## Summary Checklist

### OWASP Top 10
- [ ] A01: Broken Access Control
- [ ] A02: Cryptographic Failures
- [ ] A03: Injection
- [ ] A04: Insecure Design
- [ ] A05: Security Misconfiguration
- [ ] A06: Vulnerable Components
- [ ] A07: Authentication Failures
- [ ] A08: Data Integrity Failures
- [ ] A09: Logging Failures
- [ ] A10: SSRF

### Core Security
- [ ] Dependencies scanned
- [ ] Secrets detection run
- [ ] Input validation checked
- [ ] Auth/authz reviewed
- [ ] API security validated
- [ ] Security headers set

---

## Additional Resources

**Extended Content**:
- `references/process.md` - Detailed vulnerability patterns, code examples, language-specific guidance

**Related Workflows**:
- code-review.md - Includes security checks
- dependency-update.md - Safe dependency updates
- troubleshooting.md - Security incident response

---

**Remember**: Security is continuous. Integrate automated scanning into CI/CD, conduct regular reviews, and maintain security-first development practices.
