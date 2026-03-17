---
name: csrf-protection
description: Implements CSRF protection using synchronizer tokens, double-submit cookies, and SameSite attributes. Use when securing web forms, protecting state-changing endpoints, or implementing defense-in-depth authentication.
---

# CSRF Protection

Defend against Cross-Site Request Forgery attacks using multiple protection layers.

## Protection Methods

| Method | How It Works | Browser Support |
|--------|--------------|-----------------|
| Synchronizer Token | Hidden form field validated server-side | All |
| Double Submit | Cookie + header must match | All |
| SameSite Cookie | Browser blocks cross-origin requests | Modern |

## Token-Based Protection (Express)

```javascript
const crypto = require('crypto');

function generateToken() {
  return crypto.randomBytes(32).toString('hex');
}

// Middleware
app.use((req, res, next) => {
  if (!req.session.csrfToken) {
    req.session.csrfToken = generateToken();
  }
  res.locals.csrfToken = req.session.csrfToken;
  next();
});

// Validation
app.post('*', (req, res, next) => {
  const token = req.body._csrf || req.headers['x-csrf-token'];
  if (!token || !crypto.timingSafeEqual(
    Buffer.from(token),
    Buffer.from(req.session.csrfToken)
  )) {
    return res.status(403).json({ error: 'Invalid CSRF token' });
  }
  next();
});
```

## SameSite Cookies

```javascript
app.use(session({
  cookie: {
    httpOnly: true,
    secure: true,
    sameSite: 'strict', // or 'lax'
    maxAge: 3600000
  }
}));
```

## HTML Form Integration

```html
<form method="POST" action="/transfer">
  <input type="hidden" name="_csrf" value="<%= csrfToken %>">
  <button type="submit">Submit</button>
</form>
```

## Best Practices

- Apply to all state-changing requests (POST, PUT, DELETE)
- Use SameSite=Strict for sensitive cookies
- Validate Origin/Referer headers
- Never use GET for modifications
- Implement token expiration (1 hour typical)
- Combine multiple defense layers

## Additional Implementations

See [references/python-react.md](references/python-react.md) for:
- Flask-WTF complete CSRF setup
- React hooks for CSRF token management
- Double submit cookie pattern

## Common Mistakes

- Assuming authentication prevents CSRF
- Reusing tokens across sessions
- Storing tokens in localStorage
- Missing token expiration
