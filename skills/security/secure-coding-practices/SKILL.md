---
name: secure-coding-practices
description: Secure coding practices and defensive programming patterns for building security-first applications. Use when implementing authentication, handling user input, managing sensitive data, or conducting secure code reviews.
---

# Secure Coding Practices

Comprehensive guidance for implementing security-first development patterns with defensive programming techniques and proactive threat mitigation strategies.

## When to Use This Skill

- Implementing authentication and authorization systems
- Processing user input or external data
- Handling sensitive data (PII, credentials, financial information)
- Building APIs and web services
- Managing cryptographic operations (hashing, encryption)
- Conducting security-focused code reviews
- Establishing secure development standards for teams
- Evaluating third-party dependencies and libraries
- Designing error handling and logging strategies
- Implementing session management and token handling

## Core Security Principles

### Defense in Depth
Apply multiple layers of security controls - never rely on a single protection mechanism.

### Fail Securely
When errors occur, default to the secure state (deny access, reject input, log event).

### Least Privilege
Grant minimum necessary permissions - users, services, and databases should have only required access.

### Trust Nothing
Validate all input, encode all output, verify all sources, authenticate all requests.

## Quick Reference

| Task | Load reference |
| --- | --- |
| Input validation & sanitization | `skills/secure-coding-practices/references/input-validation.md` |
| Output encoding & XSS prevention | `skills/secure-coding-practices/references/output-encoding.md` |
| Authentication & sessions | `skills/secure-coding-practices/references/authentication.md` |
| Cryptography & key management | `skills/secure-coding-practices/references/cryptography.md` |
| Dependencies & supply chain | `skills/secure-coding-practices/references/dependencies.md` |
| Error handling & logging | `skills/secure-coding-practices/references/error-handling.md` |
| Secure defaults & configuration | `skills/secure-coding-practices/references/secure-defaults.md` |

## Workflow

1. **Identify security requirements** - Authentication, authorization, data protection, compliance
2. **Load relevant references** - Use Quick Reference table to find specific guidance
3. **Implement security controls** - Apply patterns from references with proper context
4. **Validate implementation** - Test with security scanners, penetration testing, code review
5. **Monitor and maintain** - Regular security audits, dependency updates, vulnerability scanning

## Security Checklist

**Input Validation:**
- [ ] Validate all user input server-side with allowlists
- [ ] Use schema validation libraries (Joi, Yup, Zod)
- [ ] Implement strict type checking
- [ ] Sanitize file paths and prevent traversal

**Output Encoding:**
- [ ] Apply context-aware encoding (HTML, JS, URL, SQL)
- [ ] Use templating engines with auto-escaping
- [ ] Implement Content Security Policy (CSP)
- [ ] Set secure HTTP headers (Helmet.js)

**Authentication & Authorization:**
- [ ] Hash passwords with bcrypt/Argon2 (salt rounds ≥12)
- [ ] Implement secure session management
- [ ] Use HTTPS-only cookies with HttpOnly and SameSite
- [ ] Apply rate limiting on authentication endpoints
- [ ] Verify authorization on every request

**Cryptography:**
- [ ] Use AES-256-GCM for encryption
- [ ] Generate keys with crypto.randomBytes()
- [ ] Store secrets in environment variables or KMS
- [ ] Never roll your own crypto

**Dependencies:**
- [ ] Run npm audit regularly
- [ ] Lock dependency versions in package.json
- [ ] Use Snyk/Dependabot for monitoring
- [ ] Verify package integrity (SRI for CDN)

**Error Handling & Logging:**
- [ ] Return generic error messages to users
- [ ] Log errors with correlation IDs
- [ ] Never log passwords, tokens, or PII
- [ ] Monitor security events and alerts

## Common Mistakes

- Using client-side validation as sole defense (always validate server-side)
- Blocklisting instead of allowlisting (define what's allowed, not forbidden)
- Exposing stack traces or internal errors to users
- Hardcoding secrets in source code
- Using Math.random() for security-critical operations
- Not implementing rate limiting on authentication endpoints
- Loose equality comparisons allowing type coercion attacks
- Trusting user input in database queries (SQL injection)
- Missing output encoding based on context (XSS vulnerabilities)
- Insufficient password hashing (weak algorithms or low work factor)

## High-Risk Code Patterns

Watch for these patterns in code reviews:
1. String concatenation in SQL queries (injection risk)
2. Direct file path construction from user input (traversal risk)
3. eval(), Function(), or exec() with user input (code injection)
4. Deserialization of untrusted data (RCE risk)
5. Hardcoded secrets or credentials (exposure risk)
6. Missing authentication/authorization checks (access control)
7. Weak cryptography (MD5, SHA1, ECB mode)
8. Verbose error messages in production (information disclosure)
9. Missing input validation (injection, DoS)
10. Insecure session configuration (hijacking risk)

## Resources

**OWASP Resources:**
- **OWASP Top 10**: https://owasp.org/Top10/
- **OWASP Cheat Sheet Series**: https://cheatsheetseries.owasp.org/
- **OWASP ASVS**: Application Security Verification Standard
- **OWASP Dependency-Check**: https://owasp.org/www-project-dependency-check/

**Standards & Guidelines:**
- **NIST Cybersecurity Framework**: https://www.nist.gov/cyberframework
- **NIST SP 800-63B**: Digital Identity Guidelines (Authentication)
- **CWE Top 25**: https://cwe.mitre.org/top25/

**Tools:**
- **SAST**: SonarQube, Semgrep, CodeQL
- **DAST**: OWASP ZAP, Burp Suite
- **SCA**: Snyk, npm audit, Dependabot
- **Secrets Detection**: TruffleHog, git-secrets
