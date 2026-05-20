---
name: security-reviewer
description: Security review wrapper for vibe review flow. Detects OWASP-style risks, secret leaks, auth flaws, and unsafe input handling.
---

# security-reviewer (Codex Compatibility)

Use this skill after code changes that touch input handling, auth, APIs, data access, uploads, payments, or external integrations.

## Security Review Workflow

1. Initial Scan
- Locate auth, API endpoints, DB queries, file handling, and external calls.
- Check for hardcoded secrets and unsafe config defaults.

2. OWASP-Oriented Checks
- Injection: parameterized queries, sanitized inputs.
- AuthZ/AuthN: enforce authorization per route, secure session/token handling.
- Data exposure: secrets/PII protection and safe logging.
- XSS/SSRF: output encoding, URL allowlist, no blind fetch of user URLs.
- Dependency risk: audit vulnerable dependencies.

3. High-Risk Pattern Audit
- Hardcoded secrets/tokens
- Command execution with user input
- SQL string concatenation
- Missing auth check
- Missing rate limiting on sensitive endpoints
- Unsafe crypto/password handling

4. Remediation Output
- Severity (CRITICAL/HIGH/MEDIUM/LOW)
- Evidence (file + line + risk)
- Concrete fix proposal
- Verification steps after fix

## Vibe Integration

- Security gate skill usable at any grade.
- Pair with `security-best-practices` for language/framework-specific guidance.
- Pair with `code-review` for combined correctness + security review.
