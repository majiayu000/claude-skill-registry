---
name: security-review
description: Conduct security code reviews. Use when reviewing code for vulnerabilities, assessing security posture, or auditing applications. Covers security review checklist.
allowed-tools: Read, Glob, Grep
---

# Security Review

## Review Checklist

### Authentication
- [ ] Strong password requirements enforced
- [ ] MFA implemented for sensitive operations
- [ ] Session tokens are cryptographically secure
- [ ] Session timeout is appropriate
- [ ] Logout properly invalidates session

### Authorization
- [ ] Access controls checked server-side
- [ ] Least privilege principle applied
- [ ] Role-based access properly implemented
- [ ] Direct object references validated

### Input Validation
- [ ] All input validated server-side
- [ ] Input type and length checked
- [ ] Special characters properly handled
- [ ] File uploads validated and restricted

### Output Encoding
- [ ] HTML output properly encoded
- [ ] JSON responses use proper content type
- [ ] Error messages don't leak information

### Cryptography
- [ ] Strong algorithms used (AES-256, RSA-2048+)
- [ ] No custom crypto implementations
- [ ] Keys properly managed
- [ ] TLS 1.2+ enforced

### Error Handling
- [ ] Exceptions handled gracefully
- [ ] Error messages don't expose internals
- [ ] Failed operations logged

### Logging
- [ ] Security events logged
- [ ] Sensitive data not logged
- [ ] Logs protected from tampering

## Code Patterns to Flag

### SQL Injection
```typescript
// DANGER
db.query(`SELECT * FROM users WHERE id = ${id}`);
```

### XSS
```typescript
// DANGER
element.innerHTML = userInput;
```

### Hardcoded Secrets
```typescript
// DANGER
const API_KEY = "sk-abc123...";
```

### Insecure Random
```typescript
// DANGER
Math.random(); // For security purposes
```

## Security Review Report

```markdown
## Security Review: [Component]

### Summary
- Critical: [X]
- High: [X]
- Medium: [X]
- Low: [X]

### Findings

#### [CRITICAL] SQL Injection in UserService
**Location**: src/services/user.ts:47
**Description**: User input concatenated into SQL query
**Remediation**: Use parameterized queries
**Code**:
```typescript
// Current (vulnerable)
// Recommended fix
```
```
