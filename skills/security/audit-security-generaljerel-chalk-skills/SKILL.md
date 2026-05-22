---
name: audit-security
description: Perform a security audit when the user asks to check for vulnerabilities, audit security, review OWASP compliance, scan for secrets, or assess application security posture
author: chalk
version: "1.0.0"
metadata-version: "3"
allowed-tools: Read, Glob, Grep, Bash
argument-hint: "[codebase path, component, or specific security concern]"
read-only: false
destructive: false
idempotent: false
open-world: true
user-invocable: true
tags: audit, security, owasp
---

# Audit Security

## Overview

Perform a structured security audit against the OWASP Top 10, scanning the codebase for injection vulnerabilities, broken authentication, sensitive data exposure, security misconfiguration, and broken access control. Combine automated pattern scanning with manual review of business logic and architecture decisions.

## Workflow

1. **Read project context** — Check `.chalk/docs/engineering/` for:
   - Architecture docs (to understand auth patterns, data flow, trust boundaries)
   - Previous security audits (to track remediation progress)
   - API documentation (to identify endpoints requiring auth)
   - Infrastructure docs (to understand deployment security)

2. **Determine audit scope** — From `$ARGUMENTS` and conversation:
   - If a specific component or concern is named, focus there
   - If no scope is given, audit the entire codebase
   - Identify the tech stack to tailor the scan patterns (Node.js, Python, Go, etc.)
   - Note the application type: web API, SPA, mobile backend, CLI tool

3. **Scan for injection vulnerabilities** — Search the codebase for:
   - **SQL Injection**: String concatenation in queries, missing parameterized queries, raw SQL with user input
   - **XSS**: `innerHTML`, `dangerouslySetInnerHTML`, `document.write()`, unescaped template interpolation, `v-html`
   - **Command Injection**: `exec()`, `spawn()`, `system()`, `subprocess.call()` with user-controlled arguments
   - **Template Injection**: User input in template strings evaluated server-side
   - **Path Traversal**: User input in file paths without sanitization (`../` sequences)
   - **LDAP/NoSQL Injection**: Unsanitized input in LDAP or MongoDB queries

4. **Check authentication and session management** — Review:
   - **Password handling**: Hashing algorithm (bcrypt/argon2 = good, MD5/SHA1 = bad), salt usage, minimum complexity
   - **JWT**: Secret strength, algorithm pinning (reject `none`), expiration enforcement, token storage (httpOnly cookies vs. localStorage)
   - **Session**: Session ID entropy, session fixation protection, session timeout, invalidation on logout
   - **MFA**: Is it available? Is it enforced for sensitive operations?
   - **Rate limiting**: Login attempts, password reset, API endpoints

5. **Check for sensitive data exposure** — Scan for:
   - **Hardcoded secrets**: API keys, passwords, tokens, connection strings in source code
   - **Patterns**: `password\s*=`, `api_key`, `secret`, `token`, `AWS_`, `PRIVATE_KEY`, base64-encoded credentials
   - **Logging PII**: User emails, passwords, credit card numbers, SSNs in log statements
   - **Error messages**: Stack traces, database errors, internal paths exposed to users
   - **Git history**: Secrets that were committed and later removed (still in history)
   - **.env files**: Check if `.env` is in `.gitignore`, check for `.env.example` with real values

6. **Review security configuration** — Check:
   - **CORS**: Overly permissive origins (`*`), credentials with wildcard origin
   - **Security headers**: Missing `Content-Security-Policy`, `X-Frame-Options`, `Strict-Transport-Security`, `X-Content-Type-Options`
   - **Debug mode**: Debug flags enabled in production config, verbose error output
   - **HTTPS**: Mixed content, HTTP redirects, certificate validation disabled in code
   - **Cookie security**: Missing `Secure`, `HttpOnly`, `SameSite` attributes
   - **Default credentials**: Default admin accounts, unchanged default passwords

7. **Check access control** — Review:
   - **Authorization on every endpoint**: Are there routes missing auth middleware?
   - **IDOR**: Can users access resources by changing IDs in URLs? Is ownership verified?
   - **Privilege escalation**: Can a regular user access admin endpoints? Is role checking consistent?
   - **Horizontal access**: Can user A access user B's data?
   - **API authorization**: Are all API endpoints protected? Are there unprotected admin routes?
   - **File upload**: Unrestricted file types, missing virus scanning, path traversal in filenames

8. **Review business logic** — Beyond technical vulnerabilities:
   - Race conditions in financial operations (double spending, duplicate orders)
   - Missing validation on state transitions (e.g., order status can skip steps)
   - Insufficient rate limiting on expensive operations
   - Missing audit logging for sensitive actions
   - Insecure direct object references in business workflows

9. **Classify findings** — For each finding:
   - **Severity**: Critical, High, Medium, Low
   - **CWE reference**: Map to Common Weakness Enumeration where applicable
   - **OWASP category**: Which OWASP Top 10 category does this fall under
   - **Exploitability**: How easy is it to exploit? (trivial, moderate, difficult)
   - **Impact**: What could an attacker achieve?
   - **Evidence**: File path, line number, code snippet
   - **Remediation**: Specific fix with code example

10. **Determine the next file number** — List files in `.chalk/docs/engineering/` matching `*_security_audit*`. Find the highest number and increment by 1.

11. **Write the report** — Save to `.chalk/docs/engineering/<n>_security_audit.md`.

12. **Confirm** — Summarize: total findings by severity, most critical items, and overall security posture assessment.

## Filename Convention

```
<number>_security_audit.md
```

Examples:
- `7_security_audit.md`
- `14_security_audit.md`

## Security Audit Format

```markdown
# Security Audit Report

Last updated: <YYYY-MM-DD>
Scope: <what was audited>
Tech stack: <languages, frameworks, infrastructure>

## Executive Summary

<2-3 sentences: overall security posture, most critical findings, and top recommendation.>

## Findings Summary

| Severity | Count | Remediation Urgency |
|----------|-------|-------------------|
| Critical | <n> | Immediate — block release |
| High | <n> | Fix within 1 week |
| Medium | <n> | Fix within 1 month |
| Low | <n> | Fix in next maintenance cycle |

## OWASP Coverage

| OWASP Category | Findings | Status |
|---------------|----------|--------|
| A01: Broken Access Control | <n> | Issues found / Clear |
| A02: Cryptographic Failures | <n> | Issues found / Clear |
| A03: Injection | <n> | Issues found / Clear |
| A04: Insecure Design | <n> | Issues found / Clear |
| A05: Security Misconfiguration | <n> | Issues found / Clear |
| A06: Vulnerable and Outdated Components | <n> | Issues found / Clear |
| A07: Identification and Authentication Failures | <n> | Issues found / Clear |
| A08: Software and Data Integrity Failures | <n> | Issues found / Clear |
| A09: Security Logging and Monitoring Failures | <n> | Issues found / Clear |
| A10: Server-Side Request Forgery (SSRF) | <n> | Issues found / Clear |

## Critical Findings

### FINDING-1: <Title>

| Field | Value |
|-------|-------|
| Severity | Critical |
| OWASP | A03: Injection |
| CWE | CWE-89: SQL Injection |
| Exploitability | Trivial |
| File | `<file path>:<line number>` |

**Description**: <What the vulnerability is and why it matters>

**Evidence**:
```<language>
// Vulnerable code
<code snippet>
```

**Impact**: <What an attacker could achieve by exploiting this>

**Remediation**:
```<language>
// Fixed code
<code snippet>
```

## High Findings

### FINDING-<n>: <Title>
<Same structure as Critical>

## Medium Findings

| ID | Title | OWASP | CWE | File | Remediation Summary |
|----|-------|-------|-----|------|-------------------|
| F-<n> | <title> | A05 | CWE-<n> | `<file>` | <one-line fix> |

## Low Findings

| ID | Title | OWASP | CWE | File | Remediation Summary |
|----|-------|-------|-----|------|-------------------|
| F-<n> | <title> | A05 | CWE-<n> | `<file>` | <one-line fix> |

## Positive Findings

<List security practices that are done well. This encourages good behavior and prevents regression.>

- <Good practice observed with evidence>

## Recommendations

### Immediate Actions
1. <Most critical fix>

### Short-Term (1-4 weeks)
1. <High-priority improvements>

### Long-Term (1-3 months)
1. <Architectural security improvements>
```

## Common Scan Patterns by Language

### JavaScript / TypeScript
| Vulnerability | Pattern to Search |
|--------------|-------------------|
| SQL Injection | `query(` with template literals, string concatenation in SQL |
| XSS | `innerHTML`, `dangerouslySetInnerHTML`, `document.write` |
| Command Injection | `exec(`, `execSync(`, `spawn(` with variables |
| Hardcoded Secrets | `password`, `apiKey`, `secret`, `token` in assignments |
| Eval | `eval(`, `Function(`, `setTimeout(` with strings |
| Prototype Pollution | `Object.assign`, recursive merge without safeguards |

### Python
| Vulnerability | Pattern to Search |
|--------------|-------------------|
| SQL Injection | `cursor.execute(` with f-strings or `.format()` |
| Command Injection | `os.system(`, `subprocess` with `shell=True` |
| Deserialization | `pickle.loads(`, `yaml.load(` without `Loader` |
| Path Traversal | `open(` with user input, missing `os.path.abspath` check |
| SSRF | `requests.get(` with user-controlled URL |

## Anti-patterns

- **Only automated scanning, no manual review** — Automated tools catch pattern-based vulnerabilities (hardcoded secrets, known CVEs) but miss business logic flaws (race conditions in payments, broken authorization workflows). A security audit requires both.
- **Ignoring business logic flaws** — The most damaging vulnerabilities are often in business logic: can a user manipulate prices? Can they skip payment verification? Can they access another tenant's data? These are not detectable by pattern matching.
- **Not checking auth on every endpoint** — A single unprotected admin endpoint is a complete compromise. Systematically verify that every route has appropriate authentication and authorization middleware. Do not assume the framework handles it.
- **Reporting without remediation** — A finding without a fix is frustrating and unhelpful. Every finding must include a specific remediation with a code example, not just "fix the SQL injection."
- **Ignoring the git history** — Secrets removed from the current codebase may still be in git history. If a password was committed and then deleted, it is still compromised. Check `git log -p` for sensitive patterns.
- **Only checking direct dependencies** — Transitive dependencies are equally exploitable. A vulnerability in a sub-dependency of a sub-dependency can be used to compromise the application. Use `npm audit`, `pip audit`, or equivalent.
- **Treating low-severity findings as ignorable** — Low-severity findings in combination can enable a high-severity attack chain. Information disclosure plus IDOR plus missing rate limiting can add up to a full compromise.
- **Not documenting positive findings** — Security audits that only list problems demoralize teams. Acknowledging good practices reinforces them and prevents regression.
