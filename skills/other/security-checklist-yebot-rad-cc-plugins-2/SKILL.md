---
description: Security review checklist for features and changes
disable-model-invocation: false
---

# Security Checklist

Comprehensive security review checklist for new features and changes.

## When to Use

- Before shipping any feature that handles user data
- When implementing authentication or authorization
- When adding new API endpoints
- When integrating third-party services
- During code review for security-sensitive changes

## Used By

- Security Engineer (primary owner)
- Full-Stack Engineer (implementation)
- Backend Engineer (API security)
- DevOps Engineer (infrastructure security)

---

## Security Review Template

```markdown
# Security Review: [Feature/Change Name]

**Reviewer**: [Name]
**Date**: [Date]
**Status**: In Progress | Approved | Needs Changes

---

## Overview

### Feature Description
[Brief description of the feature]

### Data Handled
- [ ] PII (Personal Identifiable Information)
- [ ] Financial data
- [ ] Authentication credentials
- [ ] User-generated content
- [ ] None of the above

### Risk Level
- [ ] High (handles sensitive data, authentication, payments)
- [ ] Medium (user data, API endpoints)
- [ ] Low (display only, no data mutation)

---

## Authentication & Authorization

### Authentication
- [ ] Authentication required for all protected endpoints
- [ ] Session management is secure (httpOnly, secure, sameSite)
- [ ] Token expiration is appropriate
- [ ] Logout properly invalidates session
- [ ] No authentication bypass possible

### Authorization
- [ ] Authorization checked on every request
- [ ] Users can only access their own data
- [ ] Admin functions properly protected
- [ ] Role/permission checks in place
- [ ] No IDOR (Insecure Direct Object Reference) vulnerabilities

### Multi-Factor Authentication (if applicable)
- [ ] MFA enforced for sensitive operations
- [ ] MFA bypass not possible
- [ ] Recovery codes handled securely

---

## Input Validation

### Data Validation
- [ ] All user input validated on server side
- [ ] Input type checked (string, number, etc.)
- [ ] Input length limited appropriately
- [ ] Input format validated (email, URL, etc.)
- [ ] Allowlists preferred over blocklists

### SQL Injection
- [ ] Parameterized queries used (no string concatenation)
- [ ] ORM used correctly
- [ ] Raw queries reviewed for injection

### XSS (Cross-Site Scripting)
- [ ] Output encoded for context (HTML, JS, URL, CSS)
- [ ] User content sanitized before display
- [ ] Content Security Policy configured
- [ ] No dangerous `innerHTML` or `dangerouslySetInnerHTML`

### Command Injection
- [ ] No user input passed to shell commands
- [ ] If necessary, input strictly validated
- [ ] Parameterized execution used

---

## Data Protection

### Data at Rest
- [ ] Sensitive data encrypted in database
- [ ] Encryption keys properly managed
- [ ] PII minimized (don't store what you don't need)
- [ ] Data classified and tagged

### Data in Transit
- [ ] HTTPS enforced everywhere
- [ ] TLS 1.2+ required
- [ ] HSTS enabled
- [ ] Secure cookies (httpOnly, secure, sameSite)

### Data Handling
- [ ] Sensitive data not logged
- [ ] Error messages don't expose internal details
- [ ] Data scrubbed from error reports
- [ ] Secure data deletion implemented

---

## API Security

### Endpoint Security
- [ ] Rate limiting implemented
- [ ] Request size limits set
- [ ] Timeout configured
- [ ] CORS properly configured

### Request Validation
- [ ] Schema validation on all inputs
- [ ] Unexpected fields rejected or ignored
- [ ] Content-type verified
- [ ] File upload restrictions in place

### Response Security
- [ ] Sensitive data not in responses
- [ ] Error codes don't leak information
- [ ] Consistent error format
- [ ] No stack traces in production

---

## Third-Party Security

### Dependencies
- [ ] Dependencies scanned for vulnerabilities
- [ ] Dependencies from trusted sources
- [ ] Dependencies up to date
- [ ] Lock file used (package-lock.json, etc.)

### Integrations
- [ ] Third-party credentials properly managed
- [ ] API keys not in code
- [ ] Webhook signatures verified
- [ ] Third-party responses validated

---

## Infrastructure Security

### Secrets Management
- [ ] No secrets in code
- [ ] Secrets in environment variables or secret manager
- [ ] Secrets rotated regularly
- [ ] Access to secrets logged

### Security Headers
- [ ] Content-Security-Policy
- [ ] X-Content-Type-Options: nosniff
- [ ] X-Frame-Options or CSP frame-ancestors
- [ ] Referrer-Policy
- [ ] Permissions-Policy
- [ ] Strict-Transport-Security

### Error Handling
- [ ] Generic error pages in production
- [ ] No stack traces exposed
- [ ] Errors logged server-side
- [ ] Monitoring for unusual error patterns

---

## Logging & Monitoring

### Security Logging
- [ ] Authentication attempts logged
- [ ] Authorization failures logged
- [ ] Sensitive operations logged
- [ ] Logs don't contain sensitive data
- [ ] Log integrity protected

### Monitoring
- [ ] Alerts for suspicious activity
- [ ] Failed login monitoring
- [ ] Rate limit triggers monitored
- [ ] Error rate monitoring

---

## Threat Model

### Assets
[What data/functionality are we protecting?]

### Threat Actors
- [ ] Anonymous attackers
- [ ] Authenticated users (privilege escalation)
- [ ] Malicious insiders
- [ ] Automated bots/scrapers

### Attack Vectors
| Threat | Likelihood | Impact | Mitigation |
|--------|------------|--------|------------|
| [Threat 1] | H/M/L | H/M/L | [Control] |
| [Threat 2] | H/M/L | H/M/L | [Control] |

### Residual Risks
[Risks that are accepted with justification]

---

## Findings

### Critical (Must Fix)
- [ ] [Finding 1]
- [ ] [Finding 2]

### High (Should Fix)
- [ ] [Finding 1]
- [ ] [Finding 2]

### Medium (Recommend)
- [ ] [Finding 1]

### Informational
- [Note 1]

---

## Sign-Off

| Role | Name | Date | Status |
|------|------|------|--------|
| Security | | | [ ] Approved |
| Dev Lead | | | [ ] Acknowledged |
```

---

## OWASP Top 10 Quick Reference

### 1. Broken Access Control
- Enforce access control on server
- Deny by default
- Verify ownership of resources

### 2. Cryptographic Failures
- Encrypt sensitive data
- Use strong algorithms
- Manage keys securely

### 3. Injection
- Use parameterized queries
- Validate and sanitize input
- Escape output for context

### 4. Insecure Design
- Threat model new features
- Defense in depth
- Secure defaults

### 5. Security Misconfiguration
- Disable unnecessary features
- Secure default configs
- Remove default credentials

### 6. Vulnerable Components
- Scan dependencies
- Keep updated
- Monitor for vulnerabilities

### 7. Authentication Failures
- Strong password requirements
- Secure session management
- Multi-factor authentication

### 8. Software/Data Integrity Failures
- Verify dependencies
- Sign releases
- Secure CI/CD

### 9. Security Logging Failures
- Log security events
- Protect log integrity
- Monitor for anomalies

### 10. Server-Side Request Forgery (SSRF)
- Validate URLs
- Use allowlists
- Limit outbound requests

---

## Quick Security Checks

### Before Every PR
- [ ] No secrets in code
- [ ] Input validation present
- [ ] Auth checks in place
- [ ] No obvious injection vectors

### Before Every Release
- [ ] Dependency scan clean
- [ ] Security headers configured
- [ ] Authentication tested
- [ ] Authorization tested

### Quarterly
- [ ] Full security review
- [ ] Penetration testing
- [ ] Dependency update
- [ ] Access review
