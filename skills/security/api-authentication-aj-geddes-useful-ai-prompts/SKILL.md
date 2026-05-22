---
name: api-authentication
description: Implement secure API authentication with JWT, OAuth 2.0, API keys, and session management. Use when securing APIs, managing tokens, or implementing user authentication flows.
---

# API Authentication

## Overview

Implement comprehensive authentication strategies for APIs including JWT tokens, OAuth 2.0, API keys, and session management with proper security practices.

## When to Use

- Securing API endpoints
- Implementing user login/logout flows
- Managing access tokens and refresh tokens
- Integrating OAuth 2.0 providers
- Protecting sensitive data
- Implementing API key authentication

## Instructions

### 1. **JWT Authentication**

```javascript
// Node.js JWT Implementation
const express = require('express');
const jwt = require('jsonwebtoken');
const bcrypt = require('bcrypt');

const app = express();
const SECRET_KEY = process.env.JWT_SECRET || 'your-secret-key';
const REFRESH_SECRET = process.env.REFRESH_SECRET || 'your-refresh-secret';

// User login endpoint
app.post('/api/auth/login', async (req, res) => {
  try {
    const { email, password } = req.body;

    // Find user in database
    const user = await User.findOne({ email });
    if (!user) {
      return res.status(401).json({ error: 'Invalid credentials' });
    }

    // Verify password
    const isValid = await bcrypt.compare(password, user.password);
    if (!isValid) {
      return res.status(401).json({ error: 'Invalid credentials' });
    }

    // Generate tokens
    const accessToken = jwt.sign(
      { userId: user.id, email: user.email, role: user.role },
      SECRET_KEY,
      { expiresIn: '15m' }
    );

    const refreshToken = jwt.sign(
      { userId: user.id },
      REFRESH_SECRET,
      { expiresIn: '7d' }
    );

    // Store refresh token in database
    await RefreshToken.create({ token: refreshToken, userId: user.id });

    res.json({
      accessToken,
      refreshToken,
      expiresIn: 900,
      user: { id: user.id, email: user.email, role: user.role }
    });
  } catch (error) {
    res.status(500).json({ error: 'Authentication failed' });
  }
});

// Refresh token endpoint
app.post('/api/auth/refresh', (req, res) => {
  const { refreshToken } = req.body;

  if (!refreshToken) {
    return res.status(401).json({ error: 'Refresh token required' });
  }

  try {
    const decoded = jwt.verify(refreshToken, REFRESH_SECRET);

    // Verify token exists in database
    const storedToken = await RefreshToken.findOne({
      token: refreshToken,
      userId: decoded.userId
    });

    if (!storedToken) {
      return res.status(401).json({ error: 'Invalid refresh token' });
    }

    // Generate new access token
    const newAccessToken = jwt.sign(
      { userId: decoded.userId },
      SECRET_KEY,
      { expiresIn: '15m' }
    );

    res.json({ accessToken: newAccessToken, expiresIn: 900 });
  } catch (error) {
    res.status(401).json({ error: 'Invalid refresh token' });
  }
});

// Middleware to verify JWT
const verifyToken = (req, res, next) => {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1]; // Bearer token

  if (!token) {
    return res.status(401).json({ error: 'Access token required' });
  }

  try {
    const decoded = jwt.verify(token, SECRET_KEY);
    req.user = decoded;
    next();
  } catch (error) {
    if (error.name === 'TokenExpiredError') {
      return res.status(401).json({ error: 'Token expired', code: 'TOKEN_EXPIRED' });
    }
    res.status(403).json({ error: 'Invalid token' });
  }
};

// Protected endpoint
app.get('/api/profile', verifyToken, (req, res) => {
  res.json({ user: req.user });
});

// Logout endpoint
app.post('/api/auth/logout', verifyToken, async (req, res) => {
  try {
    await RefreshToken.deleteOne({ userId: req.user.userId });
    res.json({ message: 'Logged out successfully' });
  } catch (error) {
    res.status(500).json({ error: 'Logout failed' });
  }
});
```

### 2. **OAuth 2.0 Implementation**

```javascript
const passport = require('passport');
const GoogleStrategy = require('passport-google-oauth20').Strategy;

passport.use(new GoogleStrategy(
  {
    clientID: process.env.GOOGLE_CLIENT_ID,
    clientSecret: process.env.GOOGLE_CLIENT_SECRET,
    callbackURL: '/api/auth/google/callback'
  },
  async (accessToken, refreshToken, profile, done) => {
    try {
      let user = await User.findOne({ googleId: profile.id });

      if (!user) {
        user = await User.create({
          googleId: profile.id,
          email: profile.emails[0].value,
          firstName: profile.name.givenName,
          lastName: profile.name.familyName
        });
      }

      return done(null, user);
    } catch (error) {
      return done(error);
    }
  }
));

// OAuth routes
app.get('/api/auth/google',
  passport.authenticate('google', { scope: ['profile', 'email'] })
);

app.get('/api/auth/google/callback',
  passport.authenticate('google', { failureRedirect: '/login' }),
  (req, res) => {
    const token = jwt.sign(
      { userId: req.user.id, email: req.user.email },
      SECRET_KEY,
      { expiresIn: '7d' }
    );
    res.redirect(`/dashboard?token=${token}`);
  }
);
```

### 3. **API Key Authentication**

```javascript
// API Key middleware
const verifyApiKey = (req, res, next) => {
  const apiKey = req.headers['x-api-key'];

  if (!apiKey) {
    return res.status(401).json({ error: 'API key required' });
  }

  try {
    // Verify API key format and existence
    const keyHash = crypto.createHash('sha256').update(apiKey).digest('hex');
    const apiKeyRecord = await ApiKey.findOne({ key_hash: keyHash, active: true });

    if (!apiKeyRecord) {
      return res.status(401).json({ error: 'Invalid API key' });
    }

    req.apiKey = apiKeyRecord;
    next();
  } catch (error) {
    res.status(500).json({ error: 'Authentication failed' });
  }
};

// Generate API key endpoint
app.post('/api/apikeys/generate', verifyToken, async (req, res) => {
  try {
    const apiKey = crypto.randomBytes(32).toString('hex');
    const keyHash = crypto.createHash('sha256').update(apiKey).digest('hex');

    const record = await ApiKey.create({
      userId: req.user.userId,
      key_hash: keyHash,
      name: req.body.name,
      active: true
    });

    res.json({ apiKey, message: 'Save this key securely' });
  } catch (error) {
    res.status(500).json({ error: 'Failed to generate API key' });
  }
});

// Protected endpoint with API key
app.get('/api/data', verifyApiKey, (req, res) => {
  res.json({ data: 'sensitive data for API key holder' });
});
```

### 4. **Python Authentication Implementation**

```python
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'secret-key'
jwt = JWTManager(app)

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()

    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({'error': 'Invalid credentials'}), 401

    access_token = create_access_token(
        identity=user.id,
        additional_claims={'email': user.email, 'role': user.role}
    )

    return jsonify({
        'accessToken': access_token,
        'user': {'id': user.id, 'email': user.email}
    }), 200

@app.route('/api/protected', methods=['GET'])
@jwt_required()
def protected():
    from flask_jwt_extended import get_jwt_identity
    user_id = get_jwt_identity()
    return jsonify({'userId': user_id}), 200

def require_role(role):
    def decorator(fn):
        @wraps(fn)
        @jwt_required()
        def wrapper(*args, **kwargs):
            from flask_jwt_extended import get_jwt
            claims = get_jwt()
            if claims.get('role') != role:
                return jsonify({'error': 'Forbidden'}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator

@app.route('/api/admin', methods=['GET'])
@require_role('admin')
def admin_endpoint():
    return jsonify({'message': 'Admin data'}), 200
```

## Best Practices

### ✅ DO
- Use HTTPS for all authentication
- Store tokens securely (HttpOnly cookies)
- Implement token refresh mechanism
- Set appropriate token expiration times
- Hash and salt passwords
- Use strong secret keys
- Validate tokens on every request
- Implement rate limiting on auth endpoints
- Log authentication attempts
- Rotate secrets regularly

### ❌ DON'T
- Store passwords in plain text
- Send tokens in URL parameters
- Use weak secret keys
- Store sensitive data in JWT payload
- Ignore token expiration
- Disable HTTPS in production
- Log sensitive tokens
- Reuse API keys across services
- Store credentials in code

## Security Headers

```javascript
app.use((req, res, next) => {
  res.setHeader('X-Content-Type-Options', 'nosniff');
  res.setHeader('X-Frame-Options', 'DENY');
  res.setHeader('X-XSS-Protection', '1; mode=block');
  res.setHeader('Strict-Transport-Security', 'max-age=31536000; includeSubDomains');
  next();
});
```
