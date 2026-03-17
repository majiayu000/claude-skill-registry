---
name: Security Audit
description: Identify and fix security vulnerabilities in code and infrastructure
triggers:
  - "security audit"
  - "vulnerability scan"
  - "security check"
  - "pen test"
---

# Security Audit Skill

Identify security vulnerabilities and implement fixes.

## Check List

### Code Security
- [ ] No hardcoded credentials/API keys
- [ ] Input validation on all user inputs
- [ ] SQL injection prevention (parameterized queries)
- [ ] XSS prevention (sanitize outputs)
- [ ] CSRF tokens where needed
- [ ] Rate limiting on APIs
- [ ] Authentication on sensitive routes
- [ ] Authorization checks (user permissions)

### Database Security
- [ ] RLS enabled on ALL tables
- [ ] Service role key never exposed to client
- [ ] Policies prevent data leaks
- [ ] Encrypted connections (SSL/TLS)

### Environment Security
- [ ] `.env.local` in `.gitignore`
- [ ] Secrets in environment variables only
- [ ] No secrets in logs
- [ ] HTTPS in production

### Dependencies
- [ ] Run `npm audit`
- [ ] Update vulnerable packages
- [ ] Review package permissions

## Common Vulnerabilities

### SQL Injection
```typescript
// BAD
const query = `SELECT * FROM users WHERE id = ${userId}`;

// GOOD
const { data } = await supabase
  .from('users')
  .select('*')
  .eq('id', userId);
```

### XSS
```typescript
// BAD
<div dangerouslySetInnerHTML={{__html: userInput}} />

// GOOD
<div>{userInput}</div>  // Auto-escaped by React
```

### Credential Leaks
```typescript
// BAD
const apiKey = "sk-1234567890abcdef";

// GOOD
const apiKey = process.env.API_KEY;
```

## Quick Audit
```bash
"Run security audit:
 1. Search for hardcoded secrets (grep for 'sk-', 'api_key', etc.)
 2. Check .gitignore includes .env*
 3. Verify RLS on all tables
 4. Run npm audit
 5. Check CORS config
 Output: temp/security/audit-{timestamp}.md"
```

---

**Remember**: Security is not optional. Audit regularly!
