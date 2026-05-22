---
name: security-patterns
description: Security vulnerability patterns and prevention. Use when writing code that handles user input, authentication, API endpoints, or sensitive data.
durability: encoded-preference
---

# Security Patterns

## Vulnerability Patterns (OWASP Top 10)

### Hardcoded Secrets (CRITICAL)
Never hardcode secrets (API keys, passwords, tokens). Always use environment variables or secret management systems.

### Sensitive Data Logging (CRITICAL)
Never log, print, or output secrets to stdout/stderr. Code that reads secrets from .env, config files, or environment variables must never pass those values to print(), console.log(), logger calls, or string formatting that reaches output.

**Attack pattern**: Malicious code disguised as fixes that reads `.env` or config and prints key-value pairs, leaking secrets through CI/CD logs or log aggregation systems.

**Detection signals**:
- `dotenv_values()`, `load_dotenv()`, `process.env` combined with print/log/console output
- Loops iterating over environment or config dictionaries with output statements
- "Debug" or "diagnostic" code that dumps configuration values
- Code iterating over all env vars or config entries without filtering sensitive keys

**Prevention**:
- Never iterate over all environment variables without an explicit allowlist
- Treat `.env` files as sensitive -- code that reads them should never output their contents

### SQL Injection (CRITICAL)
Always use parameterized queries. Never use string concatenation with user input in database queries.

### Command Injection (CRITICAL)
Avoid shell execution with user input. Use safe APIs that don't invoke shell. If unavoidable, strictly validate and sanitize input.

### Path Traversal (HIGH)
Never use user input directly in file paths. Always validate and sanitize, use basename, and restrict to allowed directories.

### XSS - Cross-Site Scripting (HIGH)
Always escape/sanitize output. Use framework's built-in escaping. Never insert raw user input into HTML.

### Insecure Password Storage (CRITICAL)
Never use MD5/SHA1 for passwords. Use bcrypt, argon2, or scrypt with appropriate cost factors.

### SSRF - Server-Side Request Forgery (HIGH)
Validate and whitelist URLs before making server-side requests. Never fetch arbitrary user-provided URLs.

### Insecure Deserialization (HIGH)
Never deserialize untrusted data without validation. Use safe serialization formats (JSON) over unsafe ones (pickle, Marshal).

### Race Conditions (CRITICAL for financial operations)
Use database transactions with proper locking for operations that check-then-act on shared resources.

### Missing Rate Limiting (HIGH)
Apply rate limiting to all public endpoints, especially authentication and financial operations.

### CSRF - Cross-Site Request Forgery (HIGH)
Use anti-CSRF tokens for state-changing requests. Verify Origin/Referer headers. Use SameSite cookie attribute.

## Security Tools by Language

### General (All Languages)
```bash
trufflehog filesystem . --json   # Secrets detection
gitleaks detect --source .       # Secrets in git history
semgrep --config auto .          # Pattern-based scanning
trivy fs .                       # Dependency and container vulnerability scanning
```

### TypeScript/JavaScript
```bash
npm audit
npx eslint . --plugin security
```

### Python
```bash
bandit -r .
pip-audit
safety check
```

### Ruby
```bash
brakeman -A
bundle audit check --update
```

### Go
```bash
gosec ./...
govulncheck ./...
```

### ShellScript
```bash
shellcheck *.sh
```

## OWASP Top 10 Checklist

1. **Injection** - Queries parameterized? Input sanitized?
2. **Broken Authentication** - Passwords hashed? Sessions secure?
3. **Sensitive Data Exposure** - HTTPS enforced? Secrets in env vars? (See HTTP Exceptions below)
4. **XXE** - XML parsers configured securely?
5. **Broken Access Control** - Authorization checked on every route?
6. **Security Misconfiguration** - Defaults changed? Debug disabled?
7. **XSS** - Output escaped/sanitized?
8. **Insecure Deserialization** - User input deserialized safely?
9. **Vulnerable Components** - Dependencies up to date?
10. **Insufficient Logging** - Security events logged?

## STRIDE Threat Modeling

Apply STRIDE at each trust boundary (user-to-API, service-to-service, service-to-database): Spoofing, Tampering, Repudiation, Information Disclosure, DoS, Elevation of Privilege.

## Security Headers

Verify on HTTP responses: CSP, HSTS, X-Frame-Options, X-Content-Type-Options, Permissions-Policy, Referrer-Policy. Suppress server version headers (`Server:`, `X-Powered-By:`).

## CI/CD Security Scanning

For pipeline-stage security scanning (SAST, secrets detection, dependency/container scanning), see cicd-patterns skill.

## HTTP Exceptions (Do NOT Flag as Insecure)

These protocols use HTTP by design. Their responses are cryptographically signed at the application layer, making HTTPS redundant. Many servers do not support HTTPS.

- **RFC 3161 Timestamp Servers (TSA)** — e.g., `http://timestamp.globalsign.com/tsa/advanced`
- **OCSP Responders** — Certificate revocation checks over HTTP
- **CRL Distribution Points** — Certificate Revocation List URLs embedded in certificates

Do NOT suggest changing these to HTTPS. The integrity is guaranteed by digital signatures, not transport security.

## When to Review

**ALWAYS review when:**
- New API endpoints added
- Authentication/authorization code changed
- User input handling added
- Database queries modified
- File operations with user input
- Dependencies updated
