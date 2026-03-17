---
name: csrf-protection
description: Implement Cross-Site Request Forgery (CSRF) protection using tokens, SameSite cookies, and origin validation. Use when building forms and state-changing operations.
---

# CSRF Protection

## Overview

Implement comprehensive Cross-Site Request Forgery protection using synchronizer tokens, double-submit cookies, SameSite cookie attributes, and custom headers.

## When to Use

- Form submissions
- State-changing operations
- Authentication systems
- Payment processing
- Account management
- Any POST/PUT/DELETE requests

## Implementation Examples

### 1. **Node.js/Express CSRF Protection**

```javascript
// csrf-protection.js
const crypto = require('crypto');
const csrf = require('csurf');

class CSRFProtection {
  constructor() {
    this.tokens = new Map();
    this.tokenExpiry = 3600000; // 1 hour
  }

  /**
   * Generate CSRF token
   */
  generateToken() {
    return crypto.randomBytes(32).toString('hex');
  }

  /**
   * Create token for session
   */
  createToken(sessionId) {
    const token = this.generateToken();
    const expiry = Date.now() + this.tokenExpiry;

    this.tokens.set(sessionId, {
      token,
      expiry
    });

    return token;
  }

  /**
   * Validate CSRF token
   */
  validateToken(sessionId, token) {
    const stored = this.tokens.get(sessionId);

    if (!stored) {
      return false;
    }

    if (Date.now() > stored.expiry) {
      this.tokens.delete(sessionId);
      return false;
    }

    return crypto.timingSafeEqual(
      Buffer.from(stored.token),
      Buffer.from(token)
    );
  }

  /**
   * Express middleware
   */
  middleware() {
    return (req, res, next) => {
      // Skip GET, HEAD, OPTIONS
      if (['GET', 'HEAD', 'OPTIONS'].includes(req.method)) {
        return next();
      }

      const token = req.headers['x-csrf-token'] || req.body._csrf;
      const sessionId = req.session?.id;

      if (!token) {
        return res.status(403).json({
          error: 'csrf_token_missing',
          message: 'CSRF token is required'
        });
      }

      if (!this.validateToken(sessionId, token)) {
        return res.status(403).json({
          error: 'csrf_token_invalid',
          message: 'Invalid or expired CSRF token'
        });
      }

      next();
    };
  }
}

// Express setup with csurf package
const express = require('express');
const session = require('express-session');
const cookieParser = require('cookie-parser');

const app = express();

// Session configuration
app.use(cookieParser());
app.use(session({
  secret: process.env.SESSION_SECRET,
  resave: false,
  saveUninitialized: false,
  cookie: {
    httpOnly: true,
    secure: true,
    sameSite: 'strict',
    maxAge: 3600000
  }
}));

// CSRF protection middleware
const csrfProtection = csrf({
  cookie: {
    httpOnly: true,
    secure: true,
    sameSite: 'strict'
  }
});

app.use(csrfProtection);

// Provide token to templates
app.use((req, res, next) => {
  res.locals.csrfToken = req.csrfToken();
  next();
});

// API endpoint to get CSRF token
app.get('/api/csrf-token', (req, res) => {
  res.json({
    csrfToken: req.csrfToken()
  });
});

// Protected route
app.post('/api/transfer', csrfProtection, (req, res) => {
  const { amount, toAccount } = req.body;

  // Process transfer
  res.json({
    message: 'Transfer successful',
    amount,
    toAccount
  });
});

// Error handler for CSRF errors
app.use((err, req, res, next) => {
  if (err.code === 'EBADCSRFTOKEN') {
    return res.status(403).json({
      error: 'csrf_error',
      message: 'Invalid CSRF token'
    });
  }

  next(err);
});

module.exports = { CSRFProtection, csrfProtection };
```

### 2. **Double Submit Cookie Pattern**

```javascript
// double-submit-csrf.js
const crypto = require('crypto');

class DoubleSubmitCSRF {
  /**
   * Generate CSRF token and set cookie
   */
  static generateAndSetToken(res) {
    const token = crypto.randomBytes(32).toString('hex');

    // Set CSRF cookie
    res.cookie('XSRF-TOKEN', token, {
      httpOnly: false, // Allow JS to read for double submit
      secure: true,
      sameSite: 'strict',
      maxAge: 3600000
    });

    return token;
  }

  /**
   * Middleware to validate double submit
   */
  static middleware() {
    return (req, res, next) => {
      // Skip GET, HEAD, OPTIONS
      if (['GET', 'HEAD', 'OPTIONS'].includes(req.method)) {
        return next();
      }

      const cookieToken = req.cookies['XSRF-TOKEN'];
      const headerToken = req.headers['x-xsrf-token'];

      if (!cookieToken || !headerToken) {
        return res.status(403).json({
          error: 'csrf_token_missing'
        });
      }

      // Compare tokens (timing-safe)
      if (!crypto.timingSafeEqual(
        Buffer.from(cookieToken),
        Buffer.from(headerToken)
      )) {
        return res.status(403).json({
          error: 'csrf_token_mismatch'
        });
      }

      next();
    };
  }
}

// Express setup
const app = express();
const cookieParser = require('cookie-parser');

app.use(cookieParser());
app.use(express.json());

// Generate token on login
app.post('/api/login', async (req, res) => {
  // Authenticate user
  const token = DoubleSubmitCSRF.generateAndSetToken(res);

  res.json({
    message: 'Login successful',
    csrfToken: token
  });
});

// Protected routes
app.use('/api/*', DoubleSubmitCSRF.middleware());

app.post('/api/update-profile', (req, res) => {
  // Update profile
  res.json({ message: 'Profile updated' });
});
```

### 3. **Python Flask CSRF Protection**

```python
# csrf_protection.py
from flask import Flask, session, request, jsonify
from flask_wtf.csrf import CSRFProtect, generate_csrf, validate_csrf
from functools import wraps
import secrets

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['WTF_CSRF_TIME_LIMIT'] = 3600  # 1 hour
app.config['WTF_CSRF_SSL_STRICT'] = True

csrf = CSRFProtect(app)

# Cookie configuration
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Strict'
)

@app.before_request
def csrf_protect():
    """Validate CSRF token for state-changing methods"""
    if request.method in ['POST', 'PUT', 'DELETE', 'PATCH']:
        token = request.headers.get('X-CSRF-Token') or request.form.get('csrf_token')

        if not token:
            return jsonify({'error': 'CSRF token missing'}), 403

        try:
            validate_csrf(token)
        except:
            return jsonify({'error': 'Invalid CSRF token'}), 403

@app.route('/api/csrf-token', methods=['GET'])
def get_csrf_token():
    """Provide CSRF token to clients"""
    token = generate_csrf()
    return jsonify({'csrfToken': token})

@app.route('/api/transfer', methods=['POST'])
def transfer_funds():
    """Protected endpoint"""
    data = request.get_json()

    return jsonify({
        'message': 'Transfer successful',
        'amount': data.get('amount')
    })

# Custom CSRF decorator
def require_csrf(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.method in ['POST', 'PUT', 'DELETE']:
            token = request.headers.get('X-CSRF-Token')

            if not token:
                return jsonify({'error': 'CSRF token required'}), 403

            try:
                validate_csrf(token)
            except:
                return jsonify({'error': 'Invalid CSRF token'}), 403

        return f(*args, **kwargs)

    return decorated_function

@app.route('/api/sensitive-action', methods=['POST'])
@require_csrf
def sensitive_action():
    return jsonify({'message': 'Action completed'})

if __name__ == '__main__':
    app.run(ssl_context='adhoc')
```

### 4. **Frontend CSRF Implementation**

```javascript
// csrf-client.js
class CSRFClient {
  constructor() {
    this.token = null;
    this.tokenExpiry = null;
  }

  /**
   * Fetch CSRF token from server
   */
  async fetchToken() {
    const response = await fetch('/api/csrf-token', {
      credentials: 'include'
    });

    const data = await response.json();
    this.token = data.csrfToken;
    this.tokenExpiry = Date.now() + 3600000; // 1 hour

    return this.token;
  }

  /**
   * Get valid token (fetch if needed)
   */
  async getToken() {
    if (!this.token || Date.now() > this.tokenExpiry) {
      await this.fetchToken();
    }

    return this.token;
  }

  /**
   * Make protected request
   */
  async request(url, options = {}) {
    const token = await this.getToken();

    const headers = {
      'Content-Type': 'application/json',
      'X-CSRF-Token': token,
      ...options.headers
    };

    return fetch(url, {
      ...options,
      headers,
      credentials: 'include'
    });
  }

  /**
   * POST request with CSRF token
   */
  async post(url, data) {
    return this.request(url, {
      method: 'POST',
      body: JSON.stringify(data)
    });
  }

  /**
   * PUT request with CSRF token
   */
  async put(url, data) {
    return this.request(url, {
      method: 'PUT',
      body: JSON.stringify(data)
    });
  }

  /**
   * DELETE request with CSRF token
   */
  async delete(url) {
    return this.request(url, {
      method: 'DELETE'
    });
  }
}

// Usage
const client = new CSRFClient();

async function transferFunds() {
  try {
    const response = await client.post('/api/transfer', {
      amount: 1000,
      toAccount: '123456'
    });

    const result = await response.json();
    console.log('Transfer successful:', result);
  } catch (error) {
    console.error('Transfer failed:', error);
  }
}

// React hook for CSRF
function useCSRF() {
  const [token, setToken] = React.useState(null);

  React.useEffect(() => {
    async function fetchToken() {
      const response = await fetch('/api/csrf-token');
      const data = await response.json();
      setToken(data.csrfToken);
    }

    fetchToken();
  }, []);

  return token;
}

// Usage in React form
function TransferForm() {
  const csrfToken = useCSRF();

  const handleSubmit = async (e) => {
    e.preventDefault();

    await fetch('/api/transfer', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRF-Token': csrfToken
      },
      body: JSON.stringify({
        amount: 1000,
        toAccount: '123456'
      })
    });
  };

  return (
    <form onSubmit={handleSubmit}>
      <input type="hidden" name="_csrf" value={csrfToken} />
      {/* form fields */}
      <button type="submit">Transfer</button>
    </form>
  );
}
```

### 5. **Origin and Referer Validation**

```javascript
// origin-validation.js
function validateOrigin(req, res, next) {
  const allowedOrigins = [
    'https://example.com',
    'https://app.example.com'
  ];

  const origin = req.headers.origin;
  const referer = req.headers.referer;

  // Check Origin header
  if (origin && !allowedOrigins.includes(origin)) {
    return res.status(403).json({
      error: 'invalid_origin'
    });
  }

  // Check Referer header as fallback
  if (!origin && referer) {
    const refererUrl = new URL(referer);
    if (!allowedOrigins.includes(refererUrl.origin)) {
      return res.status(403).json({
        error: 'invalid_referer'
      });
    }
  }

  next();
}

// Apply to state-changing routes
app.use('/api/*', validateOrigin);
```

## Best Practices

### ✅ DO
- Use CSRF tokens for all state-changing operations
- Set SameSite=Strict on cookies
- Validate Origin/Referer headers
- Use secure, random tokens
- Implement token expiration
- Use HTTPS only
- Include tokens in AJAX requests
- Test CSRF protection

### ❌ DON'T
- Skip CSRF for authenticated requests
- Use GET for state changes
- Trust Origin header alone
- Reuse tokens
- Store tokens in localStorage
- Allow credentials in CORS without validation

## CSRF Protection Methods

1. **Synchronizer Token**: Server-generated tokens
2. **Double Submit Cookie**: Cookie and header match
3. **SameSite Cookies**: Browser-level protection
4. **Custom Headers**: X-Requested-With
5. **Origin Validation**: Check request origin

## Defense Layers

- [ ] CSRF tokens implemented
- [ ] SameSite cookies configured
- [ ] Origin/Referer validation
- [ ] Custom request headers
- [ ] Token expiration
- [ ] Secure cookie flags
- [ ] HTTPS enforced

## Resources

- [OWASP CSRF Prevention](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html)
- [SameSite Cookie Spec](https://tools.ietf.org/html/draft-ietf-httpbis-rfc6265bis-05)
- [Double Submit Cookies](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html#double-submit-cookie)
