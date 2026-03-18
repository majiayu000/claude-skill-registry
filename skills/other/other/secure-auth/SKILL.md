---
name: secure-auth
description: Secure authentication implementation patterns. Use when implementing user login, registration, password reset, session management, JWT authentication, or OAuth integration. Provides production-ready patterns that avoid common tutorial pitfalls like insecure token storage, weak password hashing, and session fixation.
---

# Secure authentication

Production-ready authentication patterns. These aren't the simplest implementations—they're the ones that won't get you sued.

## Authentication architecture decision

### Sessions vs JWTs

**Use sessions when:**
- Server-rendered application
- Need immediate logout/revocation
- Single domain
- Simpler to implement correctly

**Use JWTs when:**
- Multiple services need to verify auth
- Stateless architecture required
- Mobile app + API
- Third-party integrations

**Common mistake:** Using JWTs because a tutorial did, then storing them in localStorage (XSS vulnerable) and having no revocation strategy.

## Session-based authentication

### Complete Express.js implementation

```javascript
const express = require('express');
const session = require('express-session');
const RedisStore = require('connect-redis').default;
const { createClient } = require('redis');
const bcrypt = require('bcrypt');
const crypto = require('crypto');

const app = express();

// Redis client for session storage
const redisClient = createClient({ url: process.env.REDIS_URL });
redisClient.connect();

// Session configuration
app.use(session({
  store: new RedisStore({ client: redisClient }),
  secret: process.env.SESSION_SECRET, // At least 32 random bytes
  name: 'sessionId', // Don't use default 'connect.sid'
  resave: false,
  saveUninitialized: false,
  cookie: {
    secure: process.env.NODE_ENV === 'production', // HTTPS only in prod
    httpOnly: true,  // Not accessible via JavaScript
    sameSite: 'lax', // CSRF protection
    maxAge: 24 * 60 * 60 * 1000 // 24 hours
  }
}));

// Rate limiting for auth endpoints
const loginAttempts = new Map();

function checkRateLimit(ip) {
  const attempts = loginAttempts.get(ip) || { count: 0, resetAt: Date.now() + 900000 };

  if (Date.now() > attempts.resetAt) {
    attempts.count = 0;
    attempts.resetAt = Date.now() + 900000; // 15 minute window
  }

  if (attempts.count >= 5) {
    return false;
  }

  attempts.count++;
  loginAttempts.set(ip, attempts);
  return true;
}

// Registration
app.post('/auth/register', async (req, res) => {
  const { email, password } = req.body;

  // Validate input
  if (!email || !password) {
    return res.status(400).json({ error: 'Email and password required' });
  }

  if (password.length < 12) {
    return res.status(400).json({ error: 'Password must be at least 12 characters' });
  }

  // Check if user exists
  const existingUser = await db.query(
    'SELECT id FROM users WHERE email = $1',
    [email.toLowerCase()]
  );

  if (existingUser.rows.length > 0) {
    // Don't reveal if email exists - use same message/timing
    return res.status(400).json({ error: 'Registration failed' });
  }

  // Hash password
  const hashedPassword = await bcrypt.hash(password, 12);

  // Create user
  const result = await db.query(
    'INSERT INTO users (email, password_hash) VALUES ($1, $2) RETURNING id',
    [email.toLowerCase(), hashedPassword]
  );

  // Create session
  req.session.userId = result.rows[0].id;
  req.session.createdAt = Date.now();

  res.json({ success: true });
});

// Login
app.post('/auth/login', async (req, res) => {
  const { email, password } = req.body;
  const clientIp = req.ip;

  // Rate limiting
  if (!checkRateLimit(clientIp)) {
    return res.status(429).json({ error: 'Too many attempts. Try again later.' });
  }

  // Validate input
  if (!email || !password) {
    return res.status(400).json({ error: 'Email and password required' });
  }

  // Find user
  const result = await db.query(
    'SELECT id, password_hash FROM users WHERE email = $1',
    [email.toLowerCase()]
  );

  if (result.rows.length === 0) {
    // Timing attack prevention: still do bcrypt compare
    await bcrypt.compare(password, '$2b$12$invalidhashtopreventtiming');
    return res.status(401).json({ error: 'Invalid credentials' });
  }

  const user = result.rows[0];

  // Verify password
  const isValid = await bcrypt.compare(password, user.password_hash);

  if (!isValid) {
    return res.status(401).json({ error: 'Invalid credentials' });
  }

  // Regenerate session to prevent fixation
  req.session.regenerate((err) => {
    if (err) {
      return res.status(500).json({ error: 'Session error' });
    }

    req.session.userId = user.id;
    req.session.createdAt = Date.now();

    // Clear rate limit on successful login
    loginAttempts.delete(clientIp);

    res.json({ success: true });
  });
});

// Logout
app.post('/auth/logout', (req, res) => {
  req.session.destroy((err) => {
    if (err) {
      return res.status(500).json({ error: 'Logout failed' });
    }
    res.clearCookie('sessionId');
    res.json({ success: true });
  });
});

// Auth middleware
function requireAuth(req, res, next) {
  if (!req.session.userId) {
    return res.status(401).json({ error: 'Authentication required' });
  }

  // Optional: Check session age
  const maxAge = 24 * 60 * 60 * 1000; // 24 hours
  if (Date.now() - req.session.createdAt > maxAge) {
    req.session.destroy();
    return res.status(401).json({ error: 'Session expired' });
  }

  next();
}

// Protected route
app.get('/api/profile', requireAuth, async (req, res) => {
  const user = await db.query(
    'SELECT id, email, created_at FROM users WHERE id = $1',
    [req.session.userId]
  );
  res.json(user.rows[0]);
});
```

## JWT authentication

### Complete implementation with refresh tokens

```javascript
const jwt = require('jsonwebtoken');
const crypto = require('crypto');

// Token configuration
const ACCESS_TOKEN_SECRET = process.env.ACCESS_TOKEN_SECRET;
const REFRESH_TOKEN_SECRET = process.env.REFRESH_TOKEN_SECRET;
const ACCESS_TOKEN_EXPIRY = '15m';
const REFRESH_TOKEN_EXPIRY = '7d';

// Store refresh tokens (use Redis in production)
const refreshTokens = new Map();

function generateAccessToken(userId) {
  return jwt.sign(
    { userId, type: 'access' },
    ACCESS_TOKEN_SECRET,
    { expiresIn: ACCESS_TOKEN_EXPIRY }
  );
}

function generateRefreshToken(userId) {
  const tokenId = crypto.randomBytes(32).toString('hex');
  const token = jwt.sign(
    { userId, tokenId, type: 'refresh' },
    REFRESH_TOKEN_SECRET,
    { expiresIn: REFRESH_TOKEN_EXPIRY }
  );

  // Store token ID for revocation
  refreshTokens.set(tokenId, {
    userId,
    createdAt: Date.now(),
    revoked: false
  });

  return token;
}

// Login - returns both tokens
app.post('/auth/login', async (req, res) => {
  const { email, password } = req.body;

  // ... validation and password check ...

  const accessToken = generateAccessToken(user.id);
  const refreshToken = generateRefreshToken(user.id);

  // Set refresh token as httpOnly cookie
  res.cookie('refreshToken', refreshToken, {
    httpOnly: true,
    secure: process.env.NODE_ENV === 'production',
    sameSite: 'strict',
    maxAge: 7 * 24 * 60 * 60 * 1000 // 7 days
  });

  // Return access token in response body
  res.json({ accessToken });
});

// Refresh endpoint
app.post('/auth/refresh', (req, res) => {
  const refreshToken = req.cookies.refreshToken;

  if (!refreshToken) {
    return res.status(401).json({ error: 'Refresh token required' });
  }

  try {
    const decoded = jwt.verify(refreshToken, REFRESH_TOKEN_SECRET);

    // Check if token was revoked
    const storedToken = refreshTokens.get(decoded.tokenId);
    if (!storedToken || storedToken.revoked) {
      return res.status(401).json({ error: 'Token revoked' });
    }

    // Generate new access token
    const accessToken = generateAccessToken(decoded.userId);
    res.json({ accessToken });

  } catch (err) {
    return res.status(401).json({ error: 'Invalid refresh token' });
  }
});

// Logout - revoke refresh token
app.post('/auth/logout', (req, res) => {
  const refreshToken = req.cookies.refreshToken;

  if (refreshToken) {
    try {
      const decoded = jwt.verify(refreshToken, REFRESH_TOKEN_SECRET);
      const storedToken = refreshTokens.get(decoded.tokenId);
      if (storedToken) {
        storedToken.revoked = true;
      }
    } catch (err) {
      // Token invalid, no action needed
    }
  }

  res.clearCookie('refreshToken');
  res.json({ success: true });
});

// Auth middleware for protected routes
function requireAuth(req, res, next) {
  const authHeader = req.headers.authorization;

  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return res.status(401).json({ error: 'Access token required' });
  }

  const token = authHeader.substring(7);

  try {
    const decoded = jwt.verify(token, ACCESS_TOKEN_SECRET);

    if (decoded.type !== 'access') {
      return res.status(401).json({ error: 'Invalid token type' });
    }

    req.userId = decoded.userId;
    next();

  } catch (err) {
    if (err.name === 'TokenExpiredError') {
      return res.status(401).json({ error: 'Token expired', code: 'TOKEN_EXPIRED' });
    }
    return res.status(401).json({ error: 'Invalid token' });
  }
}
```

### Frontend token handling

```javascript
// auth.js - Frontend token management

class AuthManager {
  constructor() {
    this.accessToken = null;
  }

  async login(email, password) {
    const response = await fetch('/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include', // Important for cookies
      body: JSON.stringify({ email, password })
    });

    if (!response.ok) {
      throw new Error('Login failed');
    }

    const { accessToken } = await response.json();
    this.accessToken = accessToken;

    return true;
  }

  async refreshToken() {
    const response = await fetch('/auth/refresh', {
      method: 'POST',
      credentials: 'include'
    });

    if (!response.ok) {
      this.accessToken = null;
      throw new Error('Session expired');
    }

    const { accessToken } = await response.json();
    this.accessToken = accessToken;

    return accessToken;
  }

  async fetchWithAuth(url, options = {}) {
    if (!this.accessToken) {
      throw new Error('Not authenticated');
    }

    const response = await fetch(url, {
      ...options,
      headers: {
        ...options.headers,
        'Authorization': `Bearer ${this.accessToken}`
      }
    });

    // If token expired, try to refresh and retry
    if (response.status === 401) {
      const body = await response.json();

      if (body.code === 'TOKEN_EXPIRED') {
        await this.refreshToken();

        // Retry original request
        return fetch(url, {
          ...options,
          headers: {
            ...options.headers,
            'Authorization': `Bearer ${this.accessToken}`
          }
        });
      }
    }

    return response;
  }

  async logout() {
    await fetch('/auth/logout', {
      method: 'POST',
      credentials: 'include'
    });

    this.accessToken = null;
  }
}

export const auth = new AuthManager();
```

## Password reset flow

### Secure implementation

```javascript
const crypto = require('crypto');

// Request password reset
app.post('/auth/forgot-password', async (req, res) => {
  const { email } = req.body;

  // Always return success to prevent email enumeration
  res.json({ message: 'If an account exists, a reset link has been sent.' });

  // Find user (async, after response)
  const result = await db.query(
    'SELECT id FROM users WHERE email = $1',
    [email.toLowerCase()]
  );

  if (result.rows.length === 0) {
    return; // User doesn't exist, but don't reveal that
  }

  const user = result.rows[0];

  // Generate secure token
  const token = crypto.randomBytes(32).toString('hex');
  const tokenHash = crypto.createHash('sha256').update(token).digest('hex');
  const expiresAt = new Date(Date.now() + 3600000); // 1 hour

  // Store hashed token (not plain token)
  await db.query(
    'INSERT INTO password_resets (user_id, token_hash, expires_at) VALUES ($1, $2, $3)',
    [user.id, tokenHash, expiresAt]
  );

  // Send email with plain token
  const resetUrl = `https://yourapp.com/reset-password?token=${token}`;
  await sendEmail(email, 'Password Reset', `Reset your password: ${resetUrl}`);
});

// Reset password
app.post('/auth/reset-password', async (req, res) => {
  const { token, newPassword } = req.body;

  if (!token || !newPassword) {
    return res.status(400).json({ error: 'Token and new password required' });
  }

  if (newPassword.length < 12) {
    return res.status(400).json({ error: 'Password must be at least 12 characters' });
  }

  // Hash the provided token to compare with stored hash
  const tokenHash = crypto.createHash('sha256').update(token).digest('hex');

  // Find valid reset token
  const result = await db.query(
    `SELECT user_id FROM password_resets
     WHERE token_hash = $1 AND expires_at > NOW() AND used = false`,
    [tokenHash]
  );

  if (result.rows.length === 0) {
    return res.status(400).json({ error: 'Invalid or expired token' });
  }

  const userId = result.rows[0].user_id;

  // Hash new password
  const hashedPassword = await bcrypt.hash(newPassword, 12);

  // Update password and invalidate token
  await db.query('UPDATE users SET password_hash = $1 WHERE id = $2', [hashedPassword, userId]);
  await db.query('UPDATE password_resets SET used = true WHERE token_hash = $1', [tokenHash]);

  // Invalidate all existing sessions for this user
  await db.query('DELETE FROM sessions WHERE user_id = $1', [userId]);

  res.json({ success: true });
});
```

## OAuth integration (Google example)

### Server-side flow (recommended)

```javascript
const { OAuth2Client } = require('google-auth-library');

const oauth2Client = new OAuth2Client(
  process.env.GOOGLE_CLIENT_ID,
  process.env.GOOGLE_CLIENT_SECRET,
  process.env.GOOGLE_REDIRECT_URI
);

// Step 1: Redirect to Google
app.get('/auth/google', (req, res) => {
  // Generate state for CSRF protection
  const state = crypto.randomBytes(32).toString('hex');
  req.session.oauthState = state;

  const authUrl = oauth2Client.generateAuthUrl({
    access_type: 'offline',
    scope: ['email', 'profile'],
    state: state,
    prompt: 'consent'
  });

  res.redirect(authUrl);
});

// Step 2: Handle callback
app.get('/auth/google/callback', async (req, res) => {
  const { code, state } = req.query;

  // Verify state to prevent CSRF
  if (state !== req.session.oauthState) {
    return res.status(400).send('Invalid state parameter');
  }

  delete req.session.oauthState;

  try {
    // Exchange code for tokens
    const { tokens } = await oauth2Client.getToken(code);
    oauth2Client.setCredentials(tokens);

    // Get user info
    const ticket = await oauth2Client.verifyIdToken({
      idToken: tokens.id_token,
      audience: process.env.GOOGLE_CLIENT_ID
    });

    const payload = ticket.getPayload();
    const { sub: googleId, email, name, picture } = payload;

    // Find or create user
    let user = await db.query(
      'SELECT id FROM users WHERE google_id = $1',
      [googleId]
    );

    if (user.rows.length === 0) {
      // Create new user
      user = await db.query(
        `INSERT INTO users (google_id, email, name, avatar_url)
         VALUES ($1, $2, $3, $4) RETURNING id`,
        [googleId, email, name, picture]
      );
    }

    // Create session
    req.session.regenerate((err) => {
      if (err) {
        return res.status(500).send('Session error');
      }

      req.session.userId = user.rows[0].id;
      res.redirect('/dashboard');
    });

  } catch (error) {
    console.error('OAuth error:', error);
    res.status(400).send('Authentication failed');
  }
});
```

## Multi-factor authentication (TOTP)

### Server implementation

```javascript
const speakeasy = require('speakeasy');
const QRCode = require('qrcode');

// Enable MFA for user
app.post('/auth/mfa/enable', requireAuth, async (req, res) => {
  // Generate secret
  const secret = speakeasy.generateSecret({
    name: `YourApp:${req.user.email}`,
    issuer: 'YourApp'
  });

  // Store secret (encrypted) temporarily until verified
  await db.query(
    'UPDATE users SET mfa_secret_temp = $1 WHERE id = $2',
    [encrypt(secret.base32), req.userId]
  );

  // Generate QR code
  const qrCode = await QRCode.toDataURL(secret.otpauth_url);

  res.json({
    secret: secret.base32, // Show this as backup
    qrCode: qrCode
  });
});

// Verify and activate MFA
app.post('/auth/mfa/verify', requireAuth, async (req, res) => {
  const { code } = req.body;

  const result = await db.query(
    'SELECT mfa_secret_temp FROM users WHERE id = $1',
    [req.userId]
  );

  const secret = decrypt(result.rows[0].mfa_secret_temp);

  const verified = speakeasy.totp.verify({
    secret: secret,
    encoding: 'base32',
    token: code,
    window: 1 // Allow 1 step tolerance
  });

  if (!verified) {
    return res.status(400).json({ error: 'Invalid code' });
  }

  // Move secret from temp to permanent
  await db.query(
    'UPDATE users SET mfa_secret = mfa_secret_temp, mfa_secret_temp = NULL, mfa_enabled = true WHERE id = $1',
    [req.userId]
  );

  res.json({ success: true });
});

// Login with MFA
app.post('/auth/login', async (req, res) => {
  const { email, password, mfaCode } = req.body;

  // ... verify email/password first ...

  if (user.mfa_enabled) {
    if (!mfaCode) {
      return res.status(401).json({
        error: 'MFA code required',
        requiresMfa: true
      });
    }

    const verified = speakeasy.totp.verify({
      secret: decrypt(user.mfa_secret),
      encoding: 'base32',
      token: mfaCode,
      window: 1
    });

    if (!verified) {
      return res.status(401).json({ error: 'Invalid MFA code' });
    }
  }

  // ... create session/token ...
});
```

## Security considerations checklist

### Password storage
- [ ] Using bcrypt/scrypt/Argon2 with cost factor 12+
- [ ] Never storing plain text passwords
- [ ] Never logging passwords

### Session management
- [ ] Sessions stored server-side (not just in cookies)
- [ ] Session IDs are cryptographically random
- [ ] Sessions regenerated on login (prevent fixation)
- [ ] Sessions invalidated on logout
- [ ] Sessions have maximum lifetime

### JWT security
- [ ] Short access token lifetime (15 min or less)
- [ ] Refresh tokens stored as httpOnly cookies
- [ ] Refresh token rotation implemented
- [ ] Token revocation mechanism exists
- [ ] Secrets are at least 256 bits

### Rate limiting
- [ ] Login attempts limited per IP
- [ ] Account lockout after N failures
- [ ] Password reset requests limited
- [ ] MFA verification attempts limited

### CSRF protection
- [ ] SameSite cookie attribute set
- [ ] CSRF tokens for state-changing operations
- [ ] OAuth state parameter verified

### Information disclosure
- [ ] Same error messages for valid/invalid users
- [ ] Timing attacks mitigated
- [ ] No user enumeration via registration/reset
