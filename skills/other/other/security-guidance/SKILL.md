---
name: security-guidance
description: Security guidance and best practices for code development. Use when writing authentication code, handling sensitive data, validating user input, designing APIs, or reviewing code for security issues.
license: See original LICENSE
---

# Security Guidance

Security guidance and best practices for code development.

This skill provides security-focused guidance to help identify and prevent common security vulnerabilities.

## When to Use This Skill

Use this skill when:
- Writing code that handles sensitive data
- Implementing authentication or authorization
- Working with user input or external data
- Designing APIs or network services
- Reviewing code for security issues
- Learning security best practices

## Common Security Concerns

### Input Validation
- SQL injection prevention
- Cross-site scripting (XSS) protection
- Command injection avoidance
- Path traversal prevention

### Authentication & Authorization
- Secure password handling
- Session management
- Role-based access control
- Token security

### Data Protection
- Encryption at rest and in transit
- Secure storage of secrets
- Data minimization principles
- Privacy by design

### API Security
- Rate limiting
- Input validation
- Error handling (avoid information leakage)
- Secure headers and CORS

## Usage Example

```
# General security check:
"Review this code for security issues"

# Specific concerns:
"Check for SQL injection vulnerabilities"
"Validate the authentication implementation"
"Review API security headers"
```

## Security Mindset

1. **Principle of least privilege** - Only grant necessary permissions
2. **Defense in depth** - Multiple layers of security
3. **Fail securely** - Default to secure state on failure
4. **Keep it simple** - Complexity breeds vulnerabilities
5. **Assume breach** - Design for detection and containment

## Implementation Guidance

- Use established libraries for security functions
- Keep dependencies updated
- Implement proper logging and monitoring
- Regular security testing and code review
- Stay informed about new vulnerabilities

## Resources

- OWASP Top 10
- CWE/SANS Top 25
- Platform-specific security guides
- Security framework documentation

---

## Quick Checklist

Before deploying code, verify:
- [ ] All user inputs are validated and sanitized
- [ ] No hardcoded secrets or credentials
- [ ] Proper error handling without information leakage
- [ ] Authentication and authorization checks in place
- [ ] HTTPS/TLS for all network communications
- [ ] Dependencies are up-to-date and scanned for vulnerabilities
