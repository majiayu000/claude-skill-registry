---
name: security-scan
description: Use when the user wants a security audit, vulnerability scan, or asks about potential security issues.
disable-model-invocation: true
allowed-tools: Read, Grep, Glob, Bash
context: fork
agent: Explore
---

Run a comprehensive security scan on the codebase.

## Iron Law

> **No "probably safe." Verify or flag.**
> If you cannot confirm a pattern is secure, flag it. False positives are cheap. Missed vulnerabilities are not.

## Scan Checklist

### 1. Hardcoded Secrets (CRITICAL)
```
grep -rn "password\s*=\|api_key\s*=\|secret\s*=\|token\s*=" src/
grep -rn "BEGIN.*PRIVATE KEY" .
grep -rn "sk-\|pk_\|ghp_\|gho_\|AKIA" src/
```
Also check for:
- Base64-encoded secrets (long random strings in config)
- Secrets in comments ("// old password was...")
- Secrets in test fixtures that match production patterns

### 2. SQL Injection
- String concatenation in SQL queries (`"SELECT * FROM " + table`)
- Raw queries without parameterization
- ORM bypass with raw SQL
- Dynamic table/column names from user input

### 3. XSS (Cross-Site Scripting)
- `dangerouslySetInnerHTML`, `innerHTML`, `document.write`
- Template rendering with unescaped user input (`{!! !!}`, `| safe`, `<%- %>`)
- URL parameters reflected in page without encoding
- SVG/image uploads that could contain scripts

### 4. Command Injection
- `exec()`, `spawn()`, `system()` with user-controlled input
- Template strings in shell commands
- Unsanitized filenames in file operations

### 5. Authentication & Authorization
- Routes/endpoints missing auth middleware
- Role checks that can be bypassed (client-side only)
- Password hashing (must be bcrypt/argon2/scrypt — NOT md5/sha1/sha256)
- JWT: check expiry validation, algorithm confusion, secret strength
- Session fixation or missing session regeneration on login

### 6. Input Validation
- API endpoints accepting unvalidated input
- Missing type checks, length limits, format validation
- File upload: missing type restrictions, size limits, path traversal
- Regex DoS (ReDoS) — catastrophic backtracking patterns

### 7. Sensitive Data Exposure
- Sensitive data in logs (passwords, tokens, PII)
- Stack traces or internal paths in error responses
- `.env` files not in `.gitignore`
- Sensitive data in URL query parameters (logged by proxies)
- Missing HTTPS enforcement

### 8. Dependency Vulnerabilities
```
npm audit 2>/dev/null || pip audit 2>/dev/null || true
```
Check for known CVEs in dependencies.

### 9. Insecure Configuration
- CORS: overly permissive (`Access-Control-Allow-Origin: *`)
- Missing security headers (CSP, HSTS, X-Frame-Options)
- Cookie settings: missing httpOnly, secure, sameSite flags
- Debug mode enabled in production config
- Default credentials in config files

## Anti-Rationalization

| Excuse | Rebuttal |
|--------|----------|
| "This is internal/admin-only code" | Internal code gets exposed via SSRF, insider threats, and supply chain attacks. Secure it. |
| "We're behind a firewall" | Firewalls fail. Defense in depth means every layer is secure. |
| "This secret is only in development" | Dev secrets leak to production. Use env vars and secret managers. |
| "Nobody would find this endpoint" | Security through obscurity is not security. Assume attackers find everything. |
| "The framework handles this automatically" | Verify. Frameworks have defaults, and defaults get overridden. |
| "This is a low-priority app" | Low-priority apps are pivot points. Attackers use them to reach high-priority systems. |
| "We'll fix it later" | Later never comes. Flag it now with severity. |

## Pre-Delivery Checklist

Before presenting the report, verify:

- [ ] All 9 scan categories were checked (not skipped)
- [ ] Every finding has a file:line reference
- [ ] Severity levels are justified (not guessed)
- [ ] No "probably safe" — each item is verified or flagged
- [ ] Dependency audit command was actually run
- [ ] .env and .gitignore were checked
- [ ] Auth middleware coverage was mapped to routes
- [ ] Passed checks section acknowledges secure patterns found
- [ ] Recommendations are prioritized by actual risk, not alphabetical

## Output Format

```
## Security Scan Report

### Critical (exploit risk — fix immediately)
- [file:line] [vulnerability] — [impact] — [fix]

### High (significant risk)
- [file:line] [vulnerability] — [impact] — [fix]

### Medium (moderate risk)
- [file:line] [vulnerability] — [impact] — [fix]

### Low (minor risk / hardening)
- [file:line] [issue] — [recommendation]

### Passed Checks
- [what looks good — acknowledge secure patterns]

### Prioritized Recommendations
1. [most urgent fix]
2. [next priority]
3. [etc.]
```

<!-- Skill by Huzefa Nalkheda Wala | github.com/huzaifa525 | claude-code-optimizer -->
