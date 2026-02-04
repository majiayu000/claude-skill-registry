---
name: security-auditor
version: 1.0.0
category: technical
aliases: [security, sec-audit]
---

# Security Auditor Skill

## Activation Triggers
- Keywords: security, vulnerability, audit, OWASP, injection, XSS, CSRF
- File patterns: `*.auth.*`, `*middleware*`, `*api/*`

## Capabilities
1. OWASP Top 10 vulnerability scanning
2. Authentication/authorization review
3. Input validation assessment
4. Secrets detection
5. Dependency vulnerability check

## Security Checklist

### Input Validation
- [ ] All user inputs sanitized
- [ ] SQL injection prevention (parameterized queries)
- [ ] XSS prevention (output encoding)
- [ ] Command injection prevention

### Authentication
- [ ] Strong password requirements
- [ ] Session management secure
- [ ] JWT/token handling proper
- [ ] Rate limiting on auth endpoints

### Authorization
- [ ] RBAC/ABAC implemented correctly
- [ ] No privilege escalation paths
- [ ] API endpoints protected

### Data Protection
- [ ] Sensitive data encrypted at rest
- [ ] HTTPS enforced
- [ ] No secrets in code/logs
- [ ] PII handling compliant

## Instructions
When activated, scan the codebase for:
1. Hardcoded secrets (API keys, passwords)
2. SQL string concatenation
3. Unvalidated user input
4. Missing authentication checks
5. Insecure dependencies

Report findings with severity levels: CRITICAL, HIGH, MEDIUM, LOW
