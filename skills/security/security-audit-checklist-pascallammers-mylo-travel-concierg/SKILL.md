---
name: security-audit-checklist
description: Auto-activates when user mentions security audit, security review, vulnerabilities, or OWASP. Comprehensive security checklist based on OWASP Top 10.
category: security
---

# Security Audit Checklist

OWASP Top 10 based security audit with actionable fixes.

## When This Activates

- User says: "security audit", "check for vulnerabilities", "security review"
- Before production deployment
- Periodic security reviews

## OWASP Top 10 (2025) Checklist

### 1. Injection Attacks
**Check for:**
- [ ] SQL injection (use parameterized queries)
- [ ] NoSQL injection (validate/sanitize input)
- [ ] Command injection (avoid shell execution with user input)
- [ ] LDAP injection (escape LDAP queries)

**Scan code for:**
```javascript
// ❌ VULNERABLE
db.query(`SELECT * FROM users WHERE id = '${userId}'`);
exec(`rm ${filename}`);

// ✅ SAFE
db.query('SELECT * FROM users WHERE id = $1', [userId]);
```

### 2. Broken Authentication
**Check for:**
- [ ] Password requirements enforced (min 8 chars, complexity)
- [ ] Passwords hashed with bcrypt/Argon2 (not MD5/SHA1)
- [ ] JWT tokens properly validated
- [ ] Session timeout implemented
- [ ] No credentials in logs/errors
- [ ] MFA available for sensitive operations

### 3. Sensitive Data Exposure
**Check for:**
- [ ] HTTPS enforced (no HTTP endpoints)
- [ ] Secrets in environment variables (not hardcoded)
- [ ] No API keys/tokens in client-side code
- [ ] Sensitive data encrypted at rest
- [ ] No sensitive data in URLs/query params
- [ ] Proper error messages (no stack traces in production)

**Scan for secrets:**
```bash
git grep -i "api[_-]key\\|password\\|secret\\|token" | grep -v ".env"
```

### 4. XML/XXE Attacks
**Check for:**
- [ ] XML parsing disabled external entities
- [ ] File uploads validated (type, size, content)
- [ ] No XML deserialization of untrusted data

### 5. Broken Access Control
**Check for:**
- [ ] Authorization checked on every endpoint
- [ ] User can't access other users' data
- [ ] Admin endpoints require admin role
- [ ] Object-level access control (can't guess IDs)
- [ ] Rate limiting on sensitive endpoints

**Test:**
```bash
# Try accessing other user's data
curl -H "Authorization: Bearer user1_token" /api/users/user2/profile
# Should return 403 Forbidden
```

### 6. Security Misconfiguration
**Check for:**
- [ ] No default credentials
- [ ] Unnecessary features disabled
- [ ] Security headers set (CSP, X-Frame-Options, etc.)
- [ ] Error messages don't leak info
- [ ] Dependencies updated (no known vulnerabilities)

**Required Headers:**
```javascript
res.setHeader('X-Frame-Options', 'DENY');
res.setHeader('X-Content-Type-Options', 'nosniff');
res.setHeader('Strict-Transport-Security', 'max-age=31536000');
res.setHeader('Content-Security-Policy', "default-src 'self'");
```

### 7. XSS (Cross-Site Scripting)
**Check for:**
- [ ] User input sanitized before display
- [ ] HTML entities escaped
- [ ] Content-Security-Policy header set
- [ ] React/Vue auto-escaping not bypassed (no dangerouslySetInnerHTML)

**Scan for:**
```javascript
// ❌ VULNERABLE
element.innerHTML = userInput;
dangerouslySetInnerHTML={{ __html: userComment }}

// ✅ SAFE
element.textContent = userInput;
DOMPurify.sanitize(userComment)
```

### 8. Insecure Deserialization
**Check for:**
- [ ] No deserialization of untrusted data
- [ ] Type validation on API inputs
- [ ] Use JSON, not pickle/marshal/eval

### 9. Using Components with Known Vulnerabilities
**Check for:**
- [ ] Run `npm audit` or `yarn audit`
- [ ] All dependencies up to date
- [ ] No critical vulnerabilities
- [ ] Automated dependency updates (Dependabot, Renovate)

**Run:**
```bash
npm audit --production
# Fix high/critical: npm audit fix
```

### 10. Insufficient Logging & Monitoring
**Check for:**
- [ ] Authentication failures logged
- [ ] Access control failures logged
- [ ] Input validation failures logged
- [ ] Logs don't contain sensitive data
- [ ] Monitoring/alerting for suspicious activity

## Security Scan Commands

```bash
# 1. Dependency vulnerabilities
npm audit

# 2. Secret scanning
git secrets --scan

# 3. Static analysis
npm run lint:security  # ESLint security rules

# 4. Container scanning (if using Docker)
trivy image your-image:latest

# 5. SAST (Static Application Security Testing)
semgrep --config auto .
```

## Findings Report

```markdown
## 🔒 Security Audit Report

**Date:** 2025-11-20
**Scope:** Full application

### 🚨 Critical (MUST FIX)
1. **SQL Injection** (src/api/users.ts:45)
   - Risk: Database compromise
   - Fix: Use parameterized query

2. **Hardcoded API Key** (src/lib/stripe.ts:12)
   - Risk: Key exposure in git history
   - Fix: Move to environment variable

### ⚠️ High
3. **Missing Authentication** (src/api/admin.ts:23)
   - Risk: Unauthorized admin access
   - Fix: Add auth middleware

### ℹ️ Medium
4. **Outdated Dependencies** (package.json)
   - Risk: Known vulnerabilities
   - Fix: Run `npm audit fix`

### ✅ Passed
- Input validation
- Password hashing (bcrypt)
- HTTPS enforced
- Security headers present
- Logging implemented

### 📊 Score: 7/10 (Good)

**Priority:** Fix critical and high issues before production.
```

## Quick Fixes

| Vulnerability | Quick Fix |
|---------------|-----------|
| SQL Injection | `db.query('SELECT * FROM users WHERE id = $1', [id])` |
| XSS | `DOMPurify.sanitize(input)` or use `textContent` |
| Secrets | Move to `.env`, add to `.gitignore` |
| Missing Auth | Add middleware: `app.use('/api', authMiddleware)` |
| No HTTPS | Force HTTPS: `if (!req.secure) return res.redirect('https://...')` |

**Use TodoWrite to track fixing each vulnerability. Present report when complete.**
