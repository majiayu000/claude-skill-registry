---
name: security-scan
description: Proactive security scanning. Triggers when modifying auth, API endpoints, user data, or sensitive operations.
---

# Security Scan Skill

Automatically scans for security issues when security-sensitive code is modified.

## When to Activate

This skill should activate when:
- Changes touch authentication or authorization
- New API endpoints are added
- User input handling is modified
- Database queries are added/modified
- File uploads or storage operations
- Payment or financial operations

## Security Checklist

### 1. Authentication & Authorization
- [ ] Auth middleware applied to protected routes
- [ ] Firebase Auth tokens properly validated
- [ ] User can only access their own data
- [ ] Admin endpoints properly restricted

### 2. Input Validation
- [ ] All user inputs validated
- [ ] Request body size limits
- [ ] File upload type/size restrictions
- [ ] Path traversal prevention

### 3. Data Protection
- [ ] No sensitive data in logs
- [ ] No secrets in code
- [ ] PII properly handled
- [ ] Signed URLs used for private files

### 4. API Security
- [ ] Rate limiting considered
- [ ] CORS properly configured
- [ ] Error messages don't leak info
- [ ] Proper HTTP status codes

### 5. Firebase/Firestore Security
- [ ] Security rules updated for new collections
- [ ] Rules tested with Firebase emulator
- [ ] No wildcard read/write rules
- [ ] Proper field-level validation

## OWASP Top 10 Quick Check

1. **Injection** - Parameterized queries?
2. **Broken Auth** - Session management secure?
3. **Sensitive Data** - Encrypted at rest/transit?
4. **XXE** - XML parsing disabled/secured?
5. **Broken Access Control** - Authorization checked?
6. **Misconfiguration** - Default configs changed?
7. **XSS** - Output encoded?
8. **Deserialization** - Untrusted data validated?
9. **Components** - Dependencies up to date?
10. **Logging** - Security events logged?

## Platform-Specific Checks

### Backend (Go)
```bash
# Run security scan
cd backend && make security-scan

# Check for vulnerabilities
cd backend && make vuln-check
```

### Web (Next.js)
```bash
# Check npm vulnerabilities
cd web && npm audit

# Check for secrets
grep -r "api_key\|secret\|password" web/src/
```

## Output Format

```markdown
## Security Scan Results

### Critical Vulnerabilities
- [Immediate action required]

### High Risk Issues
- [Should be fixed before deploy]

### Medium Risk Issues
- [Should be addressed soon]

### Recommendations
- [Security best practices]
```

## Reference

See `docs/SECURITY.md` for detailed security requirements.
