---
name: security-check
description: |
  Automatic OWASP security checks on generated code.
  Use when: any code is generated in the pipeline.
  Triggers: internal use only.
---

# Security Check

OWASP validation on every code generation. User doesn't see.

## Checks

### Input Validation
- [ ] All user inputs sanitized
- [ ] No raw SQL queries (use parameterized)
- [ ] No eval() or dynamic code execution
- [ ] File uploads validated (type, size)

### Authentication
- [ ] Passwords hashed (bcrypt/argon2)
- [ ] Sessions properly managed
- [ ] CSRF protection enabled
- [ ] Rate limiting on auth endpoints

### Authorization
- [ ] Protected routes check auth
- [ ] API endpoints verify permissions
- [ ] No direct object references exposed

### Data Exposure
- [ ] No secrets in code
- [ ] Sensitive data not logged
- [ ] API responses don't leak internals
- [ ] Error messages don't expose stack

### Headers
- [ ] HTTPS enforced
- [ ] Security headers set (CSP, HSTS)
- [ ] Cookies secure + httpOnly

## Auto-Fix

For common issues:

| Issue | Auto-Fix |
|-------|----------|
| Raw SQL | Convert to parameterized |
| Missing sanitization | Add input validation |
| Exposed secrets | Move to env vars |
| Missing auth check | Add middleware |

## Automation Script

Run OWASP checks programmatically:

```bash
python scripts/security_scan.py --path /project/path
python scripts/security_scan.py --path /project/path --json  # JSON output
python scripts/security_scan.py --fail-on high  # Fail on high+ severity
```

Checks: SQL injection, hardcoded secrets, unsafe eval, command injection, insecure HTTP.

## Reporting

| Result | Action |
|--------|--------|
| All pass | Continue silently |
| Auto-fixed | Continue, log internally |
| Can't fix | Block + ask user to clarify |

User sees nothing unless there's an unfixable security issue.
