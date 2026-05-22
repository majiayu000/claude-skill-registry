---
name: application-security
description: Secure applications against common vulnerabilities. Use when reviewing code for security, implementing security controls, or hardening applications. Covers OWASP Top 10.
allowed-tools: Read, Glob, Grep
---

# Application Security

## OWASP Top 10 (2021)

### 1. Broken Access Control
**Risk**: Users accessing unauthorized resources.

**Prevention**:
- Deny by default
- Implement RBAC/ABAC
- Validate permissions server-side
- Log access failures

### 2. Cryptographic Failures
**Risk**: Sensitive data exposure.

**Prevention**:
- Encrypt data at rest and in transit
- Use strong algorithms (AES-256, RSA-2048+)
- Never store passwords in plaintext
- Use secure key management

### 3. Injection
**Risk**: Malicious input executed as code.

**Prevention**:
```typescript
// BAD - SQL injection
const query = `SELECT * FROM users WHERE id = ${userId}`;

// GOOD - Parameterized query
const query = 'SELECT * FROM users WHERE id = $1';
db.query(query, [userId]);
```

### 4. Insecure Design
**Risk**: Missing security controls by design.

**Prevention**:
- Threat modeling
- Security requirements
- Defense in depth

### 5. Security Misconfiguration
**Risk**: Default or weak configuration.

**Prevention**:
- Disable unnecessary features
- Remove default credentials
- Keep software updated
- Harden server configuration

### 6. Vulnerable Components
**Risk**: Using libraries with known vulnerabilities.

**Prevention**:
- Regular dependency audits
- Keep dependencies updated
- Monitor CVE databases

### 7. Authentication Failures
**Risk**: Weak or broken authentication.

**Prevention**:
- Multi-factor authentication
- Strong password policies
- Secure session management
- Rate limiting on login

### 8. Software & Data Integrity
**Risk**: Untrusted sources for updates.

**Prevention**:
- Verify code signatures
- Use SRI for CDN resources
- Secure CI/CD pipeline

### 9. Logging & Monitoring Failures
**Risk**: Attacks go undetected.

**Prevention**:
- Log security events
- Monitor for anomalies
- Alert on suspicious activity

### 10. Server-Side Request Forgery
**Risk**: Server makes requests to unintended destinations.

**Prevention**:
- Validate URLs
- Use allowlists
- Block internal IPs
