---
name: security-review
description: Security audit patterns and OWASP Top 10 vulnerability detection. Auto-triggers when reviewing code for security, handling authentication, or processing user input.
---

# Security Review Skill

## OWASP Top 10 (2021) Checklist

### A01: Broken Access Control
- [ ] Authorization checks on every endpoint
- [ ] Deny by default policy
- [ ] CORS properly configured
- [ ] Directory listing disabled
- [ ] JWT tokens validated server-side

### A02: Cryptographic Failures
- [ ] No sensitive data in URLs
- [ ] HTTPS enforced everywhere
- [ ] Strong encryption algorithms (AES-256, RSA-2048+)
- [ ] Passwords hashed with bcrypt/argon2
- [ ] No hardcoded secrets

### A03: Injection
- [ ] Parameterized queries for SQL
- [ ] Input validation and sanitization
- [ ] Output encoding for context
- [ ] No eval() or dynamic code execution
- [ ] Command arguments properly escaped

### A04: Insecure Design
- [ ] Threat modeling completed
- [ ] Rate limiting implemented
- [ ] Resource quotas enforced
- [ ] Fail securely (deny on error)

### A05: Security Misconfiguration
- [ ] Default credentials changed
- [ ] Debug mode disabled in production
- [ ] Error messages don't leak info
- [ ] Security headers configured
- [ ] Unnecessary features disabled

### A06: Vulnerable Components
- [ ] Dependencies up to date
- [ ] No known CVEs in dependencies
- [ ] Dependency audit in CI/CD
- [ ] License compliance checked

### A07: Authentication Failures
- [ ] Multi-factor authentication available
- [ ] Strong password policy
- [ ] Account lockout after failures
- [ ] Secure session management
- [ ] Password reset is secure

### A08: Data Integrity Failures
- [ ] Code signing in place
- [ ] CI/CD pipeline secured
- [ ] Deserialization validated
- [ ] Update mechanisms secure

### A09: Logging & Monitoring
- [ ] Security events logged
- [ ] Logs don't contain sensitive data
- [ ] Alerting on suspicious activity
- [ ] Log integrity protected

### A10: SSRF
- [ ] URL validation for external requests
- [ ] Allowlist for permitted hosts
- [ ] No raw URL from user input
- [ ] Metadata endpoints blocked

## Code Patterns to Flag

```python
# DANGEROUS: SQL Injection
cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")

# SAFE: Parameterized query
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
```

```javascript
// DANGEROUS: XSS
element.innerHTML = userInput;

// SAFE: Text content
element.textContent = userInput;
```

```bash
# DANGEROUS: Command injection
os.system(f"ping {hostname}")

# SAFE: Use subprocess with list
subprocess.run(["ping", hostname], check=True)
```

## Security Headers

```
Content-Security-Policy: default-src 'self'
X-Frame-Options: DENY
X-Content-Type-Options: nosniff
Strict-Transport-Security: max-age=31536000; includeSubDomains
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: geolocation=(), microphone=()
```

## Severity Classification

| Level | Description | Response Time |
|-------|-------------|---------------|
| **CRITICAL** | Exploitable, high impact | Immediate |
| **HIGH** | Exploitable, medium impact | 24 hours |
| **MEDIUM** | Limited exploitability | 1 week |
| **LOW** | Defense in depth | Next sprint |
