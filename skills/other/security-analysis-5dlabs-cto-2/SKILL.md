---
name: security-analysis
description: Security audit patterns including OWASP Top 10, secret scanning, and language-specific vulnerabilities.
agents: [cipher]
triggers: [security, vulnerability, owasp, secrets, audit]
---

# Security Analysis

Security audit patterns for identifying and remediating vulnerabilities.

## Core Specialization

- **Vulnerability Management**: Dependabot, CodeQL, Trivy, Semgrep
- **Secret Management**: External Secrets Operator, OpenBao (Vault)
- **Auth**: OAuth2, JWT, OIDC, BetterAuth
- **Crypto**: Proper key management, secure algorithms
- **Compliance**: OWASP Top 10, CIS Benchmarks
- **Supply Chain**: SBOM, signed images, provenance

## Execution Rules

1. **Defense in depth.** Multiple layers of security
2. **Principle of least privilege.** Minimal permissions always
3. **No secrets in code.** Ever. Use secret managers
4. **Input validation.** Trust nothing from outside
5. **Secure defaults.** Opt-in to less secure, not opt-out

## Security Checklist

For every security review, verify:

- [ ] No hardcoded secrets or API keys
- [ ] Input validation on all user data
- [ ] Output encoding to prevent XSS
- [ ] Parameterized queries (no SQL injection)
- [ ] HTTPS enforced everywhere
- [ ] CORS properly configured
- [ ] Rate limiting on sensitive endpoints
- [ ] Audit logging for security events
- [ ] Dependencies scanned and updated
- [ ] Auth/authz checks on all endpoints

## Language-Specific Security

### Rust

```bash
cargo audit
cargo deny check advisories
```

**Memory Safety Checks:**
- Verify no `unsafe` blocks without proper documentation
- Check for proper lifetime annotations
- Ensure no use-after-free patterns
- Verify bounds checking on array/slice access

**Common Rust Vulnerabilities:**
- Panic in production (use `Result` instead of `unwrap()`)
- Integer overflow (use `checked_*` methods)
- Race conditions (verify `Send`/`Sync` bounds)
- Improper error disclosure (don't expose internal errors)

**Input Validation Pattern:**
```rust
use validator::Validate;

#[derive(Validate)]
struct UserInput {
    #[validate(email)]
    email: String,
    #[validate(length(min = 8, max = 100))]
    password: String,
}
```

### TypeScript

```bash
pnpm audit
npm audit --audit-level=high
```

**XSS Prevention:**
- Verify proper output encoding
- Check for dangerouslySetInnerHTML usage
- Ensure Content-Security-Policy headers

**Effect Schema Validation (Required):**
```typescript
import { Schema } from "effect"

// Use Schema.decodeUnknown for ALL external input
const validateUser = Schema.decodeUnknown(UserSchema)

// Define allowed values with Schema.Literal
const RoleSchema = Schema.Literal("user", "admin")
```

**Security Headers (Next.js):**
```typescript
const securityHeaders = [
  { key: 'Strict-Transport-Security', value: 'max-age=63072000' },
  { key: 'X-Content-Type-Options', value: 'nosniff' },
  { key: 'X-Frame-Options', value: 'DENY' },
];
```

### Go

```bash
govulncheck ./...
go list -m all | nancy sleuth
```

**Common Go Vulnerabilities:**
- Goroutine leaks (verify context cancellation)
- Race conditions (run `go test -race`)
- SQL injection (use parameterized queries)
- Path traversal (validate file paths)

**Input Validation:**
```go
func validateEmail(email string) error {
    if !emailRegex.MatchString(email) {
        return errors.New("invalid email format")
    }
    return nil
}
```

**Secure Defaults:**
- Set timeouts on HTTP clients/servers
- Validate TLS certificates
- Use secure random number generation

## General Security Scans

```bash
# Scan for secrets
trufflehog git file://. --since-commit HEAD~10

# Run Semgrep
semgrep scan --config auto
```

## OWASP Top 10 Mitigations

| Vulnerability | Mitigation |
|---------------|------------|
| Injection | Parameterized queries, input validation |
| Broken Auth | Strong passwords, MFA, session management |
| Sensitive Data | Encryption at rest and transit |
| XXE | Disable external entities |
| Broken Access | Role-based access control |
| Security Misconfig | Secure defaults, minimal exposure |
| XSS | Output encoding, CSP |
| Insecure Deserial | Input validation, type checking |
| Known Vulns | Dependency scanning, updates |
| Logging | Audit logs, monitoring |

## Guidelines

- Follow OWASP Top 10 mitigations
- Use parameterized queries (no raw SQL)
- Validate and sanitize all inputs
- Use secure defaults
- Minimize attack surface
- Log security events (without sensitive data)
