---
name: session-management
description: Implements secure session management with JWT tokens, Redis storage, refresh flows, and proper cookie configuration. Use when building authentication systems, managing user sessions, or implementing secure logout functionality.
---

# Session Management

Implement secure session management with proper token handling and storage.

## Token-Based Sessions

```javascript
const jwt = require('jsonwebtoken');

function generateTokens(user) {
  const accessToken = jwt.sign(
    { userId: user.id, role: user.role, type: 'access' },
    process.env.JWT_SECRET,
    { expiresIn: '1h' }
  );

  const refreshToken = jwt.sign(
    { userId: user.id, type: 'refresh' },
    process.env.REFRESH_SECRET,
    { expiresIn: '7d' }
  );

  return { accessToken, refreshToken };
}
```

## Redis Session Storage

```javascript
const redis = require('redis');
const client = redis.createClient();

class SessionStore {
  async create(userId, sessionData) {
    const sessionId = crypto.randomUUID();
    await client.hSet(`sessions:${userId}`, sessionId, JSON.stringify({
      ...sessionData,
      createdAt: Date.now()
    }));
    await client.expire(`sessions:${userId}`, 86400 * 7);
    return sessionId;
  }

  async invalidateAll(userId) {
    await client.del(`sessions:${userId}`);
  }
}
```

## Cookie Configuration

```javascript
app.use(session({
  name: 'session',
  secret: process.env.SESSION_SECRET,
  cookie: {
    httpOnly: true,
    secure: process.env.NODE_ENV === 'production',
    sameSite: 'strict',
    maxAge: 3600000, // 1 hour
    domain: '.example.com'
  },
  resave: false,
  saveUninitialized: false
}));
```

## Token Refresh Flow

```javascript
app.post('/auth/refresh', async (req, res) => {
  const { refreshToken } = req.cookies;

  try {
    const payload = jwt.verify(refreshToken, process.env.REFRESH_SECRET);
    if (payload.type !== 'refresh') throw new Error('Invalid token type');

    const user = await User.findById(payload.userId);
    const tokens = generateTokens(user);

    res.cookie('accessToken', tokens.accessToken, cookieOptions);
    res.json({ success: true });
  } catch (err) {
    res.status(401).json({ error: 'Invalid refresh token' });
  }
});
```

## Security Requirements

- Use HTTPS exclusively
- Set httpOnly and sameSite on cookies
- Implement proper token expiration
- Use strong, unique secrets per environment
- Validate signatures on every request

## Never Do

- Store sensitive data in tokens
- Transmit tokens via URL parameters
- Use weak or shared secrets
- Skip signature validation
