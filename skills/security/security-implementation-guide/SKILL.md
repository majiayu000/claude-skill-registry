---
name: security-implementation-guide
description: Comprehensive security patterns for authentication, authorization, input validation, and common vulnerability prevention
license: MIT
metadata:
  adapted-by: ai-skills
  category: security
---

# Security Implementation Guide

Production-ready security patterns for web applications.

## Input Validation

### Sanitization

```typescript
import DOMPurify from 'isomorphic-dompurify';

function sanitizeHTML(dirty: string): string {
  return DOMPurify.sanitize(dirty, {
    ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'p'],
    ALLOWED_ATTR: []
  });
}

// SQL injection prevention - use parameterized queries
const result = await db.query(
  'SELECT * FROM users WHERE email = $1',
  [email] // Never interpolate directly!
);
```

### XSS Prevention

```tsx
// React automatically escapes
<div>{userInput}</div>  // Safe

// Dangerous - avoid dangerouslySetInnerHTML
<div dangerouslySetInnerHTML={{ __html: sanitizeHTML(userInput) }} />

// Set security headers
app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      scriptSrc: ["'self'", "'unsafe-inline'"],
      styleSrc: ["'self'", "'unsafe-inline'"],
    }
  }
}));
```

## Authentication

### Password Hashing

```typescript
import bcrypt from 'bcrypt';  // allow-secret

async function hashPassword(password: string): Promise<string> {  // allow-secret
  const saltRounds = 12;
  return bcrypt.hash(password, saltRounds);  // allow-secret
}

async function verifyPassword(password: string, hash: string): Promise<boolean> {  // allow-secret
  return bcrypt.compare(password, hash);  // allow-secret
}
```

### Rate Limiting

```typescript
import rateLimit from 'express-rate-limit';

const loginLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 5, // 5 attempts
  message: 'Too many login attempts',
  standardHeaders: true,
  legacyHeaders: false,
});

app.post('/api/login', loginLimiter, loginHandler);
```

## CSRF Protection

```typescript
import csrf from 'csurf';

const csrfProtection = csrf({ cookie: true });

app.get('/form', csrfProtection, (req, res) => {
  res.render('form', { csrfToken: req.csrfToken() });
});

app.post('/process', csrfProtection, (req, res) => {
  // Protected endpoint
});
```

## Integration Points

Complements:
- **security-threat-modeler**: For threat analysis
- **backend-implementation-patterns**: For secure APIs
- **verification-loop**: For security checks
