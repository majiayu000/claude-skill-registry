---
name: security-basics
description: >
  Essential security checklist and patterns for web applications.
  Use when reviewing code for security issues, implementing authentication,
  or hardening an application. Covers OWASP top 10, input validation,
  and secure coding practices.
---

# Security Basics

## OWASP Top 10 Quick Reference

1. **Injection** - SQL, NoSQL, OS, LDAP injection
2. **Broken Authentication** - Weak session management
3. **Sensitive Data Exposure** - Missing encryption
4. **XML External Entities (XXE)** - XML parser attacks
5. **Broken Access Control** - Missing authorization
6. **Security Misconfiguration** - Default configs, verbose errors
7. **XSS** - Cross-Site Scripting
8. **Insecure Deserialization** - Untrusted data execution
9. **Vulnerable Components** - Outdated dependencies
10. **Insufficient Logging** - Missing audit trails

## Input Validation

### Always Validate
- User input (forms, query params)
- File uploads (type, size, content)
- API request bodies
- URL parameters

### Validation Patterns
```typescript
// Whitelist approach (preferred)
const allowedFields = ['name', 'email', 'age'];
const sanitized = pick(input, allowedFields);

// Schema validation
const schema = z.object({
  email: z.string().email(),
  age: z.number().min(0).max(150),
  name: z.string().min(1).max(100)
});
```

## SQL Injection Prevention

```typescript
// BAD - SQL Injection vulnerable
const query = `SELECT * FROM users WHERE id = ${userId}`;

// GOOD - Parameterized query
const query = 'SELECT * FROM users WHERE id = ?';
db.query(query, [userId]);

// GOOD - ORM
await User.findOne({ where: { id: userId } });
```

## XSS Prevention

```typescript
// BAD - Direct HTML insertion
element.innerHTML = userInput;

// GOOD - Text content
element.textContent = userInput;

// GOOD - Sanitize HTML if needed
import DOMPurify from 'dompurify';
element.innerHTML = DOMPurify.sanitize(userInput);

// React handles this automatically
<div>{userInput}</div>  // Safe

// But not this
<div dangerouslySetInnerHTML={{__html: userInput}} />  // DANGEROUS
```

## Authentication Checklist

- [ ] Hash passwords with bcrypt/argon2 (cost factor >= 10)
- [ ] Implement rate limiting on login
- [ ] Use secure session tokens (random, sufficient length)
- [ ] Set secure cookie flags (HttpOnly, Secure, SameSite)
- [ ] Implement proper logout (invalidate session)
- [ ] Consider 2FA for sensitive operations

## Authorization Checklist

- [ ] Check permissions on every request
- [ ] Use role-based access control (RBAC)
- [ ] Validate resource ownership
- [ ] Don't rely on hidden fields/URLs for security
- [ ] Log authorization failures

## Security Headers

```
Content-Security-Policy: default-src 'self'
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Strict-Transport-Security: max-age=31536000; includeSubDomains
X-XSS-Protection: 1; mode=block
Referrer-Policy: strict-origin-when-cross-origin
```

## Secrets Management

- Never commit secrets to version control
- Use environment variables
- Rotate secrets regularly
- Use secrets managers (AWS Secrets Manager, Vault)
- Different secrets per environment

## Dependency Security

```bash
# Check for vulnerabilities
npm audit
pip-audit
bundler-audit

# Keep dependencies updated
npm update
dependabot/renovate for automation
```

## Code Review Security Checklist

- [ ] No hardcoded secrets
- [ ] Input validation present
- [ ] Parameterized queries used
- [ ] Proper error handling (no stack traces)
- [ ] Authorization checks in place
- [ ] Sensitive data not logged
