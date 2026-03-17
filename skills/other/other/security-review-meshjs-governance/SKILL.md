---
name: security-review
updated: 2026-02-20
description: Deep security audit for web applications. Checks secrets, input validation, XSS, API security, and dependency vulnerabilities.
argument-hint: [quick|full] (default: full)
allowed-tools: Bash, Read, Grep, Glob, TodoWrite
---

# Security Review

Comprehensive security audit for web applications. Adapt checks to the project's tech stack.

## Domains

Review each domain. Use Grep to scan files, Read to inspect suspicious findings.

### 1. Secrets Management

**Check for exposed secrets:**
- Grep source files for hardcoded strings matching: `api[_-]?key`, `secret`, `password`, `token`, `private[_-]?key`, `credentials` (case insensitive)
- Verify `.env` is in `.gitignore`
- Verify server-only secrets are never imported in client/frontend code
- Check framework config for public/client-exposed variables containing secrets

**Expected pattern:**
```
# SERVER ONLY
API_KEY=...  (in .env, never in source)

# CLIENT OK
NEXT_PUBLIC_API_URL=...  (URLs are OK, keys are NOT)
VITE_API_URL=...
```

### 2. API/Endpoint Security

**Scan all API route handlers:**

| Check | What to Look For |
|-------|-----------------|
| Method validation | Every handler should check request method |
| Input validation | Query params and body should be validated before use |
| Error handling | All routes should have try-catch with generic error messages |
| Status codes | Appropriate codes (400 for bad input, 500 for server errors) |
| Auth proxy | Server-side API keys should be added in proxy layer, not client |
| Rate limiting | Consider for expensive operations |

**Anti-pattern to flag:**
```
# BAD — leaks internal error details
return { error: error.message, stack: error.stack }

# GOOD — generic error
return { error: 'Internal server error' }
```

### 3. Injection Prevention

**Scan for:**
- **SQL injection**: String concatenation in SQL queries → use parameterized queries
- **XSS**: `dangerouslySetInnerHTML`, `innerHTML`, `v-html`, `[innerHTML]` with user data
- **Command injection**: User input in `exec()`, `spawn()`, `system()`, `os.popen()`
- **Template injection**: User input in template strings rendered as HTML
- **Path traversal**: User input in file paths without sanitization

**Special attention to:**
- User-submitted content (comments, descriptions, bios)
- URL parameters rendered in the page
- Data from external APIs that may contain untrusted content

### 4. Dependency Security

```bash
npm audit --production 2>&1    # Node.js
pip audit 2>&1                 # Python
cargo audit 2>&1               # Rust
```

- Flag any HIGH or CRITICAL vulnerabilities
- Check that lock file is committed (prevents supply chain attacks)
- Verify no suspicious `postinstall` scripts from untrusted packages

### 5. Data Exposure

**Check for sensitive data leaks:**
- API responses returning more data than needed (over-fetching)
- Server-side rendering props containing server secrets
- Client-side state stores visible in DevTools containing sensitive data
- Debug statements that could leak data in production
- Error messages that reveal internal structure

### 6. CORS and Headers

**Check config files and API routes for:**
- CORS headers — should be restrictive, not `Access-Control-Allow-Origin: *`
- Security headers — CSP, X-Frame-Options, X-Content-Type-Options
- Cookie settings — HttpOnly, Secure, SameSite flags

### 7. Authentication & Authorization

**If the project has auth:**
- Verify session tokens are HttpOnly cookies (not localStorage)
- Check for broken access control (can users access other users' data?)
- Verify password hashing (bcrypt/argon2, not MD5/SHA1)
- Check for rate limiting on login endpoints
- Verify CSRF protection on state-changing requests

### 8. Client-Side Validation

**Anywhere user input is processed:**
- Form inputs (validate type, length, format)
- URL parameters (validate before using as API keys, IDs, etc.)
- localStorage/sessionStorage reads (can be tampered with)
- File uploads (validate type, size, content)

## Report Format

```
SECURITY AUDIT
═══════════════════════════════════════

CRITICAL (must fix immediately)
  [S1] Description — file:line

HIGH (fix before deployment)
  [S2] Description — file:line

MEDIUM (fix when convenient)
  [S3] Description — file:line

INFO (recommendations)
  [S4] Description

═══════════════════════════════════════
Dependencies: X high, Y critical
Overall: [SECURE / AT RISK / CRITICAL]
```

## Quick Mode

For `quick` argument, only check:
1. Secrets management (hardcoded credentials)
2. API/endpoint security (method validation, error handling)
3. Dependency audit

Skip injection deep scan, CORS review, auth review, and client-side validation review.
