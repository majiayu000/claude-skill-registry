---
name: security
description: Protect your SaaS app from common vulnerabilities. Use when building auth, handling user data, or deploying features. Covers authentication, data protection, API security, and OWASP Top 10 for non-technical founders using AI tools.
---

# Security

## Security Checklist

```
Security Basics:
- [ ] Authentication required for protected routes
- [ ] Passwords hashed (bcrypt/argon2), never stored plain text
- [ ] API keys in environment variables, not code
- [ ] HTTPS only in production
- [ ] Input validated on server side
- [ ] SQL injection prevented (use parameterized queries)
- [ ] XSS prevented (sanitize user input)
- [ ] CSRF tokens on forms
- [ ] Rate limiting on API endpoints
- [ ] User sessions expire (30min-1hr typical)
```

See [COMMON-VULNS.md](COMMON-VULNS.md) for detailed checks.

---

## Critical: Never Store These in Code

**Move to environment variables:**
- Database passwords
- API keys (Stripe, SendGrid, etc)
- JWT secrets
- OAuth client secrets
- Encryption keys

**Tell AI:**
```
Store API keys in .env file, not in code.
Add .env to .gitignore.
Access via process.env.API_KEY
```

---

## Authentication Basics

**Minimum requirements:**
- Passwords: 8+ chars, require number/symbol
- Hash passwords (bcrypt with 10+ rounds)
- Email verification for signups
- Password reset via email only
- Sessions expire (30-60 min idle)
- Logout clears session completely

**Tell AI:**
```
Add authentication:
- bcrypt for password hashing (12 rounds)
- Email verification required
- Session timeout: 30 minutes
- Password requirements: 8+ chars, 1 number, 1 symbol
```

See [SECURITY-PROMPTS.md](SECURITY-PROMPTS.md) for implementation details.

---

## Data Protection

**Always encrypt:**
- Passwords (hashed, not encrypted)
- Payment info (use Stripe, don't store cards)
- Personal identifiable information (PII)

**Never log:**
- Passwords (even hashed)
- Credit card numbers
- API keys
- Session tokens

**Tell AI:**
```
Never log sensitive data.
Replace passwords/tokens with "[REDACTED]" in logs.
```

---

## API Security

**Required for all API endpoints:**
- Authentication check
- Rate limiting (prevent abuse)
- Input validation
- Error messages don't leak info

**Tell AI:**
```
Add to all API routes:
- Require valid auth token
- Rate limit: 100 requests/minute per IP
- Validate all inputs (reject invalid)
- Generic error messages (no stack traces to users)
```

---

## Common Vulnerabilities

**Most common in AI-built apps:**

1. **Exposed API keys** - In code instead of .env
2. **No rate limiting** - APIs can be spammed
3. **Missing auth checks** - Routes accessible without login
4. **SQL injection** - Raw SQL with user input
5. **XSS attacks** - Unescaped user content displayed

See [COMMON-VULNS.md](COMMON-VULNS.md) for how to check.

---

## Security Prompts for AI

**Adding authentication:**
```
Add authentication to this route.
Require valid JWT token.
Return 401 if missing/invalid.
Don't expose error details.
```

**Rate limiting:**
```
Add rate limiting:
- 100 requests/minute per IP
- Return 429 "Too many requests" if exceeded
- Use sliding window, not fixed
```

**Input validation:**
```
Validate all user inputs:
- Email: valid format
- Password: 8+ chars, 1 number, 1 symbol
- Username: alphanumeric only, 3-20 chars
Reject invalid input with clear error message
```

See [SECURITY-PROMPTS.md](SECURITY-PROMPTS.md) for more.

---

## Pre-Launch Security Review

**Before deploying:**

```
Production Security:
- [ ] All secrets in environment variables
- [ ] HTTPS enforced (no HTTP)
- [ ] Database backups configured
- [ ] Rate limiting on all APIs
- [ ] Error pages don't show stack traces
- [ ] Admin routes protected
- [ ] File uploads validated (type, size)
- [ ] CORS configured (not wildcard "*")
```

---

## When to Get Security Audit

**Signs you need expert review:**
- Handling payments directly (not Stripe)
- Storing health/financial data
- Multi-tenant with data isolation
- Over 1,000 users
- Processing sensitive PII

**For most MVPs:** Following this checklist is sufficient.

---

## Common Founder Mistakes

| Mistake | Fix |
|---------|-----|
| API keys in code | Move to .env |
| No rate limiting | Add to all endpoints |
| Plain text passwords | Use bcrypt |
| HTTP in production | Force HTTPS |
| Accepting all CORS | Whitelist domains |
| No input validation | Validate server-side |
| Detailed error messages | Generic messages only |

---

## Quick Wins

**Easy security improvements:**

1. Add Helmet.js (Node) - Sets security headers
2. Use HTTPS everywhere - Force in production
3. Add rate limiting - Prevents abuse
4. Environment variables - Keep secrets safe
5. Update dependencies - Fix known vulnerabilities

**Tell AI:**
```
Add helmet.js for security headers.
Configure for production (HTTPS, CSP, XSS protection).
```

---

## Testing Security

**Quick checks:**

**Exposed secrets:**
```bash
grep -r "api_key" src/
grep -r "password" src/
# Should only find references to env vars
```

**No auth bypass:**
- Try accessing protected routes without login
- Should redirect to login or return 401

**Rate limiting works:**
- Hit API endpoint 100 times quickly
- Should get 429 error

---

## Success Looks Like

✅ No secrets in code (all in .env)  
✅ Can't access protected routes without auth  
✅ Passwords hashed, never stored plain text  
✅ Rate limiting prevents abuse  
✅ HTTPS enforced in production  
✅ Input validated on server side