---
name: security-audit
description: Deep security audit of the codebase (Janet Moore's workflow)
---

Perform a security audit following Janet Moore's standards.

## Audit Checklist

### 1. Authentication & Authorization
- Read the dependencies/DI file — verify timing-safe comparison (see stack concepts) is used, not equality operator
- Verify health/readiness endpoints bypass auth via the public DI dependency
- Verify ALL state-changing endpoints require auth when API key is configured
- Check error messages are uniform — no enumeration clues

### 2. Input Validation
- Read the models/schemas file — verify all fields have type constraints
- Check identifier parameters use appropriate validation constraints
- Check state parameters use enum types — no raw strings
- Verify typed schemas (see stack concepts) are used on every endpoint (no raw object parsing)

### 3. Information Leakage
- Search for `traceback`, `stack`, `__file__`, `__name__` in API responses
- Verify all error responses use the error response model
- Check no internal paths, class names, or implementation details in 4xx/5xx responses
- Verify logging never outputs API keys or secrets

### 4. Audit Trail
- Verify ALL state-changing operations produce audit log entries
- Check audit entries include: action, identifier, state, timestamp
- Verify all state-changing service methods produce audit entries

### 5. Rate Limiting
- Read the middleware file — verify per-client IP rate limiting
- Check `429` response includes `Retry-After` header
- Verify rate limit is configurable via the project's env vars

### 6. CORS & Headers
- Check CORS origins come from config, not hardcoded
- Verify CORS is configurable via the project's env vars

### 7. Dependencies
- Run dependency audit command if available to check for known CVEs
- Review the requirements file for outdated or vulnerable packages

## Output Format
Group findings by severity: **Critical**, **High**, **Medium**, **Low**, **Info**
Include specific file:line references and remediation steps for each finding.