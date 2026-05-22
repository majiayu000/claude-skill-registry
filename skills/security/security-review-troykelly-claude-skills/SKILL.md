---
name: security-review
description: MANDATORY for security-sensitive code changes - OWASP-based security review with dedicated checklist, required before PR for auth, input handling, API, database, or credential code
allowed-tools:
  - Read
  - Grep
  - Glob
  - mcp__github__*
model: opus
---

# Security Review

## Overview

Dedicated security review for code handling authentication, authorization, user input, APIs, databases, or credentials.

**Core principle:** Security issues require specialized attention beyond general code review.

**Trigger:** This review is MANDATORY when changes touch security-sensitive paths.

**Announce at start:** "I'm performing a security review of this code."

## When Required

This skill is MANDATORY when ANY of these files are modified:

| Pattern | Examples |
|---------|----------|
| `**/auth/**` | src/auth/login.ts, lib/auth/session.js |
| `**/security/**` | src/security/encryption.ts |
| `**/middleware/**` | src/middleware/authenticate.ts |
| `**/api/**` | src/api/endpoints.ts |
| `**/*password*` | utils/passwordHash.ts |
| `**/*token*` | services/tokenService.ts |
| `**/*secret*` | config/secrets.ts |
| `**/*credential*` | lib/credentials.js |
| `**/*session*` | middleware/session.ts |
| `**/routes/**` | src/routes/protected.ts |
| `**/*.sql` | migrations/001_users.sql |

Check with:
```bash
git diff --name-only HEAD~1 | grep -E '(auth|security|middleware|api|password|token|secret|credential|session|routes|\.sql)'
```

## OWASP Top 10 Checklist

Review against each category:

### 1. Injection (A03:2021)

| Check | Verify |
|-------|--------|
| SQL Injection | All queries use parameterized statements |
| Command Injection | No user input in shell commands, or properly escaped |
| LDAP Injection | LDAP queries use proper escaping |
| XPath Injection | XPath queries use parameterized approach |
| Template Injection | Template engines configured safely |

```typescript
// VULNERABLE
db.query(`SELECT * FROM users WHERE id = '${userId}'`);

// SECURE
db.query('SELECT * FROM users WHERE id = ?', [userId]);
```

### 2. Broken Authentication (A07:2021)

| Check | Verify |
|-------|--------|
| Password Storage | Passwords hashed with bcrypt/argon2 (not MD5/SHA1) |
| Session Management | Secure, HttpOnly, SameSite cookies |
| Token Handling | JWTs signed, validated, short-lived |
| Brute Force Protection | Rate limiting on auth endpoints |
| Credential Exposure | No credentials in logs, errors, or responses |

### 3. Sensitive Data Exposure (A02:2021)

| Check | Verify |
|-------|--------|
| Data in Transit | HTTPS enforced, TLS 1.2+ |
| Data at Rest | Sensitive data encrypted |
| Secrets in Code | No hardcoded API keys, passwords, tokens |
| Error Messages | No sensitive info in error responses |
| Logging | No sensitive data logged |

```bash
# Check for hardcoded secrets
grep -rE '(password|secret|api_key|token)\s*[:=]\s*["\047][^"\047]+["\047]' src/
```

### 4. XML External Entities (A05:2021)

| Check | Verify |
|-------|--------|
| XML Parsing | External entities disabled |
| DTD Processing | DTD processing disabled if not needed |

### 5. Broken Access Control (A01:2021)

| Check | Verify |
|-------|--------|
| Authorization Checks | Every endpoint verifies permissions |
| Direct Object References | Object access validated against user |
| Privilege Escalation | Cannot elevate own privileges |
| CORS | Properly restricted origins |
| Method Restriction | Only allowed HTTP methods accepted |

### 6. Security Misconfiguration (A05:2021)

| Check | Verify |
|-------|--------|
| Default Credentials | No default passwords in use |
| Error Handling | Stack traces not exposed to users |
| Security Headers | CSP, X-Frame-Options, etc. set |
| Debug Mode | Disabled in production |
| Unnecessary Features | Unused endpoints/features removed |

### 7. Cross-Site Scripting (A03:2021)

| Check | Verify |
|-------|--------|
| Output Encoding | User input encoded before display |
| DOM XSS | innerHTML not used with user input |
| Template Safety | Template engine auto-escapes |
| CSP | Content Security Policy configured |

```typescript
// VULNERABLE
element.innerHTML = userInput;

// SECURE
element.textContent = userInput;
// OR
element.innerHTML = DOMPurify.sanitize(userInput);
```

### 8. Insecure Deserialization (A08:2021)

| Check | Verify |
|-------|--------|
| Object Deserialization | Untrusted data not deserialized |
| JSON Parsing | Safe JSON.parse usage |
| Type Validation | Deserialized objects validated |

### 9. Using Components with Known Vulnerabilities (A06:2021)

| Check | Verify |
|-------|--------|
| Dependency Audit | `pnpm audit` / `pip audit` clean |
| Outdated Packages | No critically outdated dependencies |
| CVE Check | No known CVEs in dependencies |

```bash
# Run dependency audit
pnpm audit --prod
# or
pip-audit
```

### 10. Insufficient Logging & Monitoring (A09:2021)

| Check | Verify |
|-------|--------|
| Auth Events | Login success/failure logged |
| Access Control | Permission denials logged |
| Input Validation | Validation failures logged |
| Sensitive Actions | Admin actions logged |
| Log Integrity | Logs protected from tampering |

## Review Process

### Step 1: Identify Security-Sensitive Changes

```bash
# List changed files matching security patterns
git diff --name-only HEAD~1 | grep -E '(auth|security|middleware|api|password|token|secret|session)'
```

### Step 2: Review Each File

For each security-sensitive file:
1. Read the entire file (not just diff)
2. Check against all 10 OWASP categories
3. Note any findings with severity

### Step 3: Check Dependencies

```bash
# Audit dependencies
pnpm audit --prod

# Check for outdated
pnpm outdated
```

### Step 4: Document Findings

Use severity levels:

| Severity | Description | Action |
|----------|-------------|--------|
| CRITICAL | Exploitable vulnerability, data breach risk | MUST fix before merge |
| HIGH | Significant security weakness | MUST fix before merge |
| MEDIUM | Defense-in-depth issue | SHOULD fix before merge |
| LOW | Minor improvement | MAY fix in future issue |

### Step 5: Add Security Section to Review Artifact

Add to the main review artifact:

```markdown
### Security Review

**Security-Sensitive:** YES
**Reviewed By:** [WORKER_ID or security-reviewer subagent]
**OWASP Categories Checked:** 10/10

#### Security Findings

| # | OWASP Category | Severity | Finding | Status |
|---|----------------|----------|---------|--------|
| 1 | A03 Injection | CRITICAL | SQL injection in findUser() | FIXED |
| 2 | A02 Sensitive Data | HIGH | API key in config.ts | DEFERRED #456 |
| 3 | A01 Access Control | MEDIUM | Missing auth on /admin | FIXED |

#### Dependency Audit

```
pnpm audit: 0 vulnerabilities
```

**Security Review Status:** [PASS|ISSUES_FIXED|ISSUES_DEFERRED]
```

## Security Review Artifact (Standalone)

If security review is extensive, post as separate comment:

```markdown
<!-- SECURITY_REVIEW:START -->
## Security Review

| Property | Value |
|----------|-------|
| Issue | #123 |
| Reviewer | `security-reviewer` subagent |
| Reviewed | 2025-12-29T10:30:00Z |

### Files Reviewed

- src/auth/login.ts
- src/middleware/authenticate.ts
- src/api/users.ts

### OWASP Checklist Results

| # | Category | Status | Notes |
|---|----------|--------|-------|
| A01 | Broken Access Control | PASS | Auth middleware on all protected routes |
| A02 | Cryptographic Failures | PASS | bcrypt for passwords, TLS enforced |
| A03 | Injection | FIXED | Parameterized SQL queries now |
| A04 | Insecure Design | PASS | - |
| A05 | Security Misconfiguration | PASS | - |
| A06 | Vulnerable Components | PASS | pnpm audit clean |
| A07 | Auth Failures | PASS | Rate limiting, secure sessions |
| A08 | Data Integrity Failures | PASS | - |
| A09 | Logging Failures | NOTE | Consider adding auth failure logging |
| A10 | SSRF | N/A | No server-side requests |

### Dependency Audit

```
found 0 vulnerabilities
```

**Security Review Status:** PASS
<!-- SECURITY_REVIEW:END -->
```

## Checklist

Before completing security review:

- [ ] All changed security-sensitive files reviewed
- [ ] All 10 OWASP categories checked
- [ ] Dependency audit run
- [ ] All CRITICAL/HIGH findings fixed
- [ ] Any deferred findings have tracking issues
- [ ] Security section added to review artifact
- [ ] Security-Sensitive marked YES in main artifact

## Integration

This skill is triggered by:
- Changes to security-sensitive file patterns
- Explicit invocation
- `security-reviewer` subagent

This skill integrates with:
- `comprehensive-review` - Security is criterion #4
- `review-gate` - Verifies security review for sensitive changes

This skill is enforced by:
- `.claude/rules/security-sensitive.md` conditional rules
- `PreToolUse` hook (PR blocked if security-sensitive without review)
