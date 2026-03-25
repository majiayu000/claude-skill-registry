---
name: security-scan
description: Scan codebase for OWASP top 10, hardcoded secrets, injection vulnerabilities, and security issues
disable-model-invocation: true
allowed-tools: Read, Grep, Glob, Bash
context: fork
agent: Explore
---

Run a comprehensive security scan on the codebase.

## Scan Checklist

### 1. Hardcoded Secrets
```
grep -rn "password\s*=\|api_key\s*=\|secret\s*=\|token\s*=" src/
grep -rn "BEGIN.*PRIVATE KEY" .
grep -rn "sk-\|pk_\|ghp_\|gho_\|AKIA" src/
```

### 2. SQL Injection
- Search for string concatenation in SQL queries
- Check for raw queries without parameterization
- Verify ORM usage is safe

### 3. XSS (Cross-Site Scripting)
- Search for `dangerouslySetInnerHTML`, `innerHTML`, `document.write`
- Check template rendering for unescaped user input
- Verify output encoding

### 4. Authentication & Authorization
- Check auth middleware coverage on routes
- Look for endpoints missing auth checks
- Verify password hashing (bcrypt/argon2, NOT md5/sha1)
- Check JWT token validation and expiry

### 5. Input Validation
- Check API endpoints for input validation
- Look for missing type checks on user input
- Verify file upload restrictions

### 6. Sensitive Data Exposure
- Check for sensitive data in logs
- Verify .env files are in .gitignore
- Check error messages don't leak internals
- Verify HTTPS enforcement

### 7. Dependency Vulnerabilities
```
npm audit 2>/dev/null || pip audit 2>/dev/null || true
```

### 8. Insecure Configuration
- Check CORS settings
- Verify security headers (helmet, CSP)
- Check cookie settings (httpOnly, secure, sameSite)

## Output Format

```
## Security Scan Report

### Critical
- [file:line] [vulnerability] [impact]

### High
- [file:line] [vulnerability] [impact]

### Medium
- [file:line] [vulnerability] [impact]

### Low
- [file:line] [vulnerability] [impact]

### Passed Checks
- [what looks good]

### Recommendations
- [prioritized action items]
```

<!-- Skill by Huzefa Nalkheda Wala | github.com/huzaifa525 | claude-code-optimizer -->
