---
name: api-authentication
description: Secure API authentication with JWT, OAuth 2.0, API keys. Use for authentication systems, third-party integrations, service-to-service communication, or encountering token management, security headers, auth flow errors.
---

# API Authentication

Implement secure authentication mechanisms for APIs using modern standards and best practices.

## Authentication Methods

| Method | Use Case | Security Level |
|--------|----------|----------------|
| JWT | Stateless auth, SPAs | High |
| OAuth 2.0 | Third-party integration | High |
| API Keys | Service-to-service | Medium |
| Session | Traditional web apps | High |

## JWT Implementation (Node.js)

```javascript
const jwt = require('jsonwebtoken');

const generateTokens = (user) => ({
  accessToken: jwt.sign(
    { userId: user.id, role: user.role },
    process.env.JWT_SECRET,
    { expiresIn: '15m' }
  ),
  refreshToken: jwt.sign(
    { userId: user.id, type: 'refresh' },
    process.env.REFRESH_SECRET,
    { expiresIn: '7d' }
  )
});

const authMiddleware = (req, res, next) => {
  const authHeader = req.headers.authorization;

  // Validate authorization header format
  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return res.status(401).json({ error: 'Malformed authorization header' });
  }

  const parts = authHeader.split(' ');
  if (parts.length !== 2) {
    return res.status(401).json({ error: 'Malformed authorization header' });
  }

  const token = parts[1];
  if (!token) {
    return res.status(401).json({ error: 'No token provided' });
  }

  try {
    req.user = jwt.verify(token, process.env.JWT_SECRET);
    next();
  } catch (err) {
    res.status(401).json({ error: 'Invalid token' });
  }
};
```

## Security Requirements

- Always use HTTPS
- Store tokens in HttpOnly cookies (not localStorage)
- Hash passwords with bcrypt (cost factor 12+)
- Implement rate limiting on auth endpoints
- Rotate secrets regularly
- Never transmit tokens in URLs

## Security Headers

```javascript
app.use((req, res, next) => {
  res.setHeader('X-Content-Type-Options', 'nosniff');
  res.setHeader('X-Frame-Options', 'DENY');
  res.setHeader('Strict-Transport-Security', 'max-age=31536000');
  next();
});
```

## Additional Implementations

See [references/python-flask.md](references/python-flask.md) for:
- Flask JWT with role-based access control decorators
- OAuth 2.0 Google integration with Authlib
- API key authentication with secure hashing

## Common Mistakes to Avoid

- Storing plain-text passwords
- Using weak JWT secrets
- Ignoring token expiration
- Disabling HTTPS in production
- Logging sensitive tokens
