---
name: session-management
description: Implement secure session management systems with JWT tokens, session storage, token refresh, logout handling, and CSRF protection. Use when managing user authentication state, handling token lifecycle, and securing sessions.
---

# Session Management

## Overview

Implement comprehensive session management systems with secure token handling, session persistence, token refresh mechanisms, proper logout procedures, and CSRF protection across different backend frameworks.

## When to Use

- Implementing user authentication systems
- Managing session state and user context
- Handling JWT token refresh cycles
- Implementing logout functionality
- Protecting against CSRF attacks
- Managing session expiration and cleanup

## Instructions

### 1. **JWT Token Generation and Validation**

```python
# Python/Flask Example
from flask import current_app
from datetime import datetime, timedelta
import jwt
import os

class TokenManager:
    def __init__(self, secret_key=None):
        self.secret_key = secret_key or os.getenv('JWT_SECRET')
        self.algorithm = 'HS256'
        self.access_token_expires_hours = 1
        self.refresh_token_expires_days = 7

    def generate_tokens(self, user_id, email, role='user'):
        """Generate both access and refresh tokens"""
        now = datetime.utcnow()

        # Access token
        access_payload = {
            'user_id': user_id,
            'email': email,
            'role': role,
            'type': 'access',
            'iat': now,
            'exp': now + timedelta(hours=self.access_token_expires_hours)
        }
        access_token = jwt.encode(access_payload, self.secret_key, algorithm=self.algorithm)

        # Refresh token
        refresh_payload = {
            'user_id': user_id,
            'type': 'refresh',
            'iat': now,
            'exp': now + timedelta(days=self.refresh_token_expires_days)
        }
        refresh_token = jwt.encode(refresh_payload, self.secret_key, algorithm=self.algorithm)

        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'expires_in': self.access_token_expires_hours * 3600,
            'token_type': 'Bearer'
        }

    def verify_token(self, token, token_type='access'):
        """Verify and decode JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])

            # Check token type matches
            if payload.get('type') != token_type:
                return None, 'Invalid token type'

            return payload, None
        except jwt.ExpiredSignatureError:
            return None, 'Token expired'
        except jwt.InvalidTokenError:
            return None, 'Invalid token'

    def refresh_access_token(self, refresh_token):
        """Generate new access token from refresh token"""
        payload, error = self.verify_token(refresh_token, token_type='refresh')
        if error:
            return None, error

        new_access_token = self.generate_tokens(
            payload['user_id'],
            payload.get('email', ''),
            payload.get('role', 'user')
        )

        return new_access_token, None
```

### 2. **Node.js/Express JWT Implementation**

```javascript
// Node.js/Express Example
const jwt = require('jsonwebtoken');
const crypto = require('crypto');
const redis = require('redis');

class SessionManager {
    constructor() {
        this.secretKey = process.env.JWT_SECRET || 'dev-secret';
        this.algorithm = 'HS256';
        this.accessTokenExpiry = '1h';
        this.refreshTokenExpiry = '7d';
        this.redisClient = redis.createClient();
    }

    generateTokens(userId, email, role = 'user') {
        const now = new Date();
        const jti = crypto.randomBytes(16).toString('hex');

        const accessToken = jwt.sign(
            {
                userId,
                email,
                role,
                type: 'access',
                jti,
                iat: Math.floor(now.getTime() / 1000)
            },
            this.secretKey,
            { algorithm: this.algorithm, expiresIn: this.accessTokenExpiry }
        );

        const refreshToken = jwt.sign(
            {
                userId,
                type: 'refresh',
                jti,
                iat: Math.floor(now.getTime() / 1000)
            },
            this.secretKey,
            { algorithm: this.algorithm, expiresIn: this.refreshTokenExpiry }
        );

        return {
            accessToken,
            refreshToken,
            expiresIn: 3600,
            tokenType: 'Bearer'
        };
    }

    verifyToken(token, tokenType = 'access') {
        try {
            const decoded = jwt.verify(token, this.secretKey, {
                algorithms: [this.algorithm]
            });

            if (decoded.type !== tokenType) {
                return { payload: null, error: 'Invalid token type' };
            }

            return { payload: decoded, error: null };
        } catch (err) {
            if (err.name === 'TokenExpiredError') {
                return { payload: null, error: 'Token expired' };
            }
            return { payload: null, error: 'Invalid token' };
        }
    }

    async isTokenBlacklisted(jti) {
        const result = await this.redisClient.get(`blacklist:${jti}`);
        return result !== null;
    }

    async blacklistToken(jti, expiresIn) {
        await this.redisClient.setex(`blacklist:${jti}`, expiresIn, '1');
    }

    async logout(token) {
        const decoded = jwt.decode(token);
        if (decoded && decoded.jti) {
            const expiresIn = decoded.exp - Math.floor(Date.now() / 1000);
            await this.blacklistToken(decoded.jti, expiresIn);
        }
    }

    refreshAccessToken(refreshToken) {
        const { payload, error } = this.verifyToken(refreshToken, 'refresh');
        if (error) {
            return { tokens: null, error };
        }

        return {
            tokens: this.generateTokens(payload.userId, payload.email, payload.role),
            error: null
        };
    }
}

// Middleware
const authMiddleware = (req, res, next) => {
    const authHeader = req.headers['authorization'];
    const token = authHeader && authHeader.split(' ')[1];

    if (!token) {
        return res.status(401).json({ error: 'No token provided' });
    }

    const sessionManager = new SessionManager();
    const { payload, error } = sessionManager.verifyToken(token);

    if (error) {
        return res.status(401).json({ error });
    }

    req.user = payload;
    next();
};
```

### 3. **Session Storage with Redis**

```python
# Python/Flask with Redis
import redis
import json
from datetime import timedelta
from functools import wraps

class RedisSessionManager:
    def __init__(self, redis_url='redis://localhost:6379'):
        self.redis = redis.from_url(redis_url, decode_responses=True)
        self.prefix = 'session:'

    def create_session(self, user_id, data, expire_hours=24):
        """Create a session for user"""
        session_data = {
            'user_id': user_id,
            'data': data,
            'created_at': datetime.utcnow().isoformat(),
            'last_activity': datetime.utcnow().isoformat()
        }

        session_id = secrets.token_urlsafe(32)
        key = f'{self.prefix}{session_id}'

        self.redis.setex(
            key,
            timedelta(hours=expire_hours),
            json.dumps(session_data)
        )

        return session_id

    def get_session(self, session_id):
        """Retrieve session data"""
        key = f'{self.prefix}{session_id}'
        data = self.redis.get(key)

        if not data:
            return None

        session_data = json.loads(data)

        # Update last activity
        session_data['last_activity'] = datetime.utcnow().isoformat()
        self.redis.setex(key, timedelta(hours=24), json.dumps(session_data))

        return session_data

    def destroy_session(self, session_id):
        """Destroy a session"""
        key = f'{self.prefix}{session_id}'
        self.redis.delete(key)

    def update_session(self, session_id, updates):
        """Update session data"""
        session_data = self.get_session(session_id)
        if not session_data:
            return False

        session_data['data'].update(updates)
        key = f'{self.prefix}{session_id}'
        self.redis.setex(
            key,
            timedelta(hours=24),
            json.dumps(session_data)
        )
        return True

    def get_user_sessions(self, user_id):
        """Get all sessions for a user"""
        cursor = 0
        sessions = []

        while True:
            cursor, keys = self.redis.scan(cursor, match=f'{self.prefix}*')
            for key in keys:
                data = json.loads(self.redis.get(key))
                if data['user_id'] == user_id:
                    sessions.append({
                        'session_id': key.replace(self.prefix, ''),
                        'created_at': data['created_at'],
                        'last_activity': data['last_activity']
                    })

            if cursor == 0:
                break

        return sessions

    def invalidate_all_user_sessions(self, user_id):
        """Logout user from all devices"""
        sessions = self.get_user_sessions(user_id)
        for session in sessions:
            self.destroy_session(session['session_id'])
```

### 4. **CSRF Protection**

```python
# Flask CSRF Protection
from flask_wtf.csrf import CSRFProtect
from flask import session, request

csrf = CSRFProtect()

@app.route('/login', methods=['POST'])
@csrf.protect
def login():
    # CSRF token is automatically verified
    email = request.json.get('email')
    password = request.json.get('password')

    user = User.query.filter_by(email=email).first()
    if user and user.verify_password(password):
        session['user_id'] = user.id
        session['csrf_token'] = csrf.generate_csrf()
        return jsonify({'success': True}), 200

    return jsonify({'error': 'Invalid credentials'}), 401

# JavaScript client
async function login(email, password) {
    const response = await fetch('/csrf-token');
    const { csrfToken } = await response.json();

    return fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRF-Token': csrfToken
        },
        body: JSON.stringify({ email, password })
    });
}
```

### 5. **Session Middleware Chain**

```javascript
// Node.js middleware chain
const express = require('express');
const app = express();

// 1. Parse cookies
app.use(express.json());
app.use(cookieParser(process.env.COOKIE_SECRET));

// 2. Session middleware
app.use(session({
    secret: process.env.SESSION_SECRET,
    resave: false,
    saveUninitialized: false,
    cookie: {
        httpOnly: true,
        secure: process.env.NODE_ENV === 'production',
        sameSite: 'strict',
        maxAge: 24 * 60 * 60 * 1000
    },
    store: new RedisStore({ client: redisClient })
}));

// 3. CSRF protection
const csrfProtection = csrf({ cookie: false });

// 4. Rate limiting per session
const sessionRateLimit = rateLimit({
    store: new RedisStore({ client: redisClient }),
    keyGenerator: (req) => req.sessionID,
    windowMs: 15 * 60 * 1000,
    max: 100
});

app.use(sessionRateLimit);

// 5. Authentication check
const requireAuth = (req, res, next) => {
    if (!req.session.user) {
        return res.status(401).json({ error: 'Unauthorized' });
    }
    req.user = req.session.user;
    next();
};

app.post('/api/login', csrfProtection, async (req, res) => {
    // Verify credentials
    const user = await User.findOne({ email: req.body.email });
    if (user && await user.verifyPassword(req.body.password)) {
        req.session.user = { id: user.id, email: user.email, role: user.role };
        req.session.regenerate((err) => {
            if (err) return res.status(500).json({ error: 'Server error' });
            res.json({ success: true });
        });
    } else {
        res.status(401).json({ error: 'Invalid credentials' });
    }
});

app.post('/api/logout', requireAuth, (req, res) => {
    req.session.destroy((err) => {
        if (err) return res.status(500).json({ error: 'Logout failed' });
        res.clearCookie('connect.sid');
        res.json({ success: true });
    });
});
```

### 6. **Token Refresh Endpoint**

```python
# Flask token refresh endpoint
from flask import request, jsonify
from functools import wraps

@app.route('/api/auth/refresh', methods=['POST'])
def refresh_token():
    data = request.get_json()
    refresh_token = data.get('refresh_token')

    if not refresh_token:
        return jsonify({'error': 'Refresh token required'}), 400

    token_manager = TokenManager()
    tokens, error = token_manager.refresh_access_token(refresh_token)

    if error:
        return jsonify({'error': error}), 401

    return jsonify(tokens), 200

@app.route('/api/auth/logout', methods=['POST'])
@require_auth
def logout():
    token = request.headers['Authorization'].split(' ')[1]
    session_manager = RedisSessionManager()
    session_manager.destroy_session(token)

    return jsonify({'message': 'Logged out successfully'}), 200
```

### 7. **Session Cleanup and Maintenance**

```python
# Scheduled cleanup task with APScheduler
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

class SessionCleanup:
    def __init__(self, redis_client, cleanup_interval_minutes=60):
        self.redis = redis_client
        self.cleanup_interval = cleanup_interval_minutes
        self.scheduler = BackgroundScheduler()

    def start(self):
        self.scheduler.add_job(
            func=self.cleanup_expired_sessions,
            trigger='interval',
            minutes=self.cleanup_interval,
            id='cleanup_expired_sessions',
            replace_existing=True
        )
        self.scheduler.start()
        atexit.register(lambda: self.scheduler.shutdown())

    def cleanup_expired_sessions(self):
        """Remove expired sessions from Redis"""
        cursor = 0
        removed_count = 0

        while True:
            cursor, keys = self.redis.scan(cursor, match='session:*')
            for key in keys:
                ttl = self.redis.ttl(key)
                if ttl == -2:  # Key doesn't exist
                    removed_count += 1
                elif ttl < 300:  # Less than 5 minutes left
                    self.redis.delete(key)
                    removed_count += 1

            if cursor == 0:
                break

        return removed_count

# Initialize on app startup
cleanup = SessionCleanup(redis_client)
cleanup.start()
```

## Best Practices

### ✅ DO
- Use HTTPS for all session transmission
- Implement secure cookies (httpOnly, sameSite, secure flags)
- Use JWT with proper expiration times
- Implement token refresh mechanism
- Store refresh tokens securely
- Validate tokens on every request
- Use strong secret keys
- Implement session timeout
- Log authentication events
- Clear session data on logout
- Use CSRF tokens for state-changing requests

### ❌ DON'T
- Store sensitive data in tokens
- Use short secret keys
- Transmit tokens in URLs
- Ignore token expiration
- Reuse token secrets across environments
- Store tokens in localStorage (use httpOnly cookies)
- Implement session without HTTPS
- Forget to validate token signatures
- Expose session IDs in logs
- Use predictable session IDs

## Complete Example

```python
from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import jwt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'

TOKEN_MANAGER = TokenManager()

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()

    if user and user.verify_password(data['password']):
        tokens = TOKEN_MANAGER.generate_tokens(user.id, user.email, user.role)
        return jsonify(tokens), 200

    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/refresh', methods=['POST'])
def refresh():
    refresh_token = request.json.get('refresh_token')
    tokens, error = TOKEN_MANAGER.refresh_access_token(refresh_token)

    if error:
        return jsonify({'error': error}), 401

    return jsonify(tokens), 200
```
