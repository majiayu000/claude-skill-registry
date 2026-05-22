---
name: api-security-hardening
description: REST API security hardening with authentication, rate limiting, input validation, security headers. Use for production APIs, security audits, defense-in-depth, or encountering vulnerabilities, injection attacks, CORS issues.
---

# API Security Hardening

Protect REST APIs against common vulnerabilities with multiple security layers.

## Security Middleware Stack (Express)

```javascript
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');
const mongoSanitize = require('express-mongo-sanitize');
const xss = require('xss-clean');

app.use(helmet());
app.use(mongoSanitize());
app.use(xss());

app.use('/api/', rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 100
}));

app.use('/api/auth/', rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 5
}));
```

## Input Validation

```javascript
const { body, validationResult } = require('express-validator');

app.post('/users',
  body('email').isEmail().normalizeEmail(),
  body('password').isLength({ min: 8 }).matches(/[A-Z]/).matches(/[0-9]/),
  body('name').trim().escape().isLength({ max: 100 }),
  (req, res) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }
    // Process request
  }
);
```

## Security Headers

```javascript
app.use((req, res, next) => {
  res.setHeader('Content-Security-Policy', "default-src 'self'");
  res.setHeader('X-Frame-Options', 'DENY');
  res.setHeader('X-Content-Type-Options', 'nosniff');
  res.setHeader('Strict-Transport-Security', 'max-age=31536000; includeSubDomains');
  res.setHeader('X-XSS-Protection', '1; mode=block');
  next();
});
```

## Security Checklist

- [ ] HTTPS everywhere
- [ ] Authentication on all protected routes
- [ ] Input validation and sanitization
- [ ] Rate limiting enabled
- [ ] Security headers configured
- [ ] CORS restricted to allowed origins
- [ ] No stack traces in production errors
- [ ] Audit logging enabled
- [ ] Dependencies regularly updated

## Additional Implementations

See [references/python-nginx.md](references/python-nginx.md) for:
- Python FastAPI security middleware
- Pydantic input validation with password rules
- Nginx SSL/TLS and security headers configuration
- HTTP Parameter Pollution prevention

## Never Do

- Trust user input without validation
- Return detailed errors in production
- Store secrets in code
- Use GET for state-changing operations
- Disable security for convenience
