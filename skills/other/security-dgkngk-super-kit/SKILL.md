---
name: security
description: Security audit, vulnerability scanning, and secure coding practices. Use when reviewing code for OWASP vulnerabilities, implementing auth, securing APIs, or handling sensitive data.
---

# Security Skill

## Overview
Security audit, vulnerability scanning, and secure coding practices.

## OWASP Top 10 Checks

### 1. Injection (SQL, NoSQL, Command)
```typescript
// ❌ Vulnerable
const query = `SELECT * FROM users WHERE id = ${userId}`;

// ✅ Safe - Parameterized query
const query = 'SELECT * FROM users WHERE id = $1';
await db.query(query, [userId]);
```

### 2. Authentication Flaws
```typescript
// Password hashing
import bcrypt from 'bcrypt';

async function hashPassword(password: string) {
  return bcrypt.hash(password, 12);
}

async function verifyPassword(password: string, hash: string) {
  return bcrypt.compare(password, hash);
}
```

### 3. XSS Prevention
```typescript
// ❌ Dangerous
element.innerHTML = userInput;

// ✅ Safe - Escape output
element.textContent = userInput;

// React auto-escapes, but avoid dangerouslySetInnerHTML
```

### 4. CSRF Protection
```typescript
// Use CSRF tokens
import csrf from 'csurf';
const csrfProtection = csrf({ cookie: true });

app.use(csrfProtection);

// In form
<input type="hidden" name="_csrf" value={csrfToken} />
```

### 5. Security Headers
```typescript
// helmet middleware
import helmet from 'helmet';

app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      scriptSrc: ["'self'", "'unsafe-inline'"],
      styleSrc: ["'self'", "'unsafe-inline'"],
    },
  },
}));
```

## JWT Security

```typescript
import jwt from 'jsonwebtoken';

// ✅ Best practices
const token = jwt.sign(
  { userId: user.id },
  process.env.JWT_SECRET,
  {
    algorithm: 'HS256',
    expiresIn: '15m',  // Short expiry
    issuer: 'my-app',
    audience: 'my-app-users',
  }
);

// Verify with options
jwt.verify(token, process.env.JWT_SECRET, {
  algorithms: ['HS256'],  // Prevent algorithm switching
  issuer: 'my-app',
});
```

## Secrets Management
```bash
# Never commit secrets
.env
.env.local
*.pem
*.key
```

## Security Audit Commands
```bash
# NPM audit
npm audit --audit-level=high

# Check for leaked secrets
npx secretlint "**/*"

# Dependency vulnerabilities
npx snyk test
```
