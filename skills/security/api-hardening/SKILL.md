---
name: api-hardening
description: API security hardening patterns. Use when implementing rate limiting, input validation, CORS configuration, API key management, request throttling, or protecting endpoints from abuse. Covers defense-in-depth strategies for REST APIs with practical implementations for Express, FastAPI, and serverless.
---

# API hardening

Defense-in-depth patterns for protecting APIs from abuse, injection attacks, and data leakage.

## Rate limiting

### Why it matters

Without rate limiting:
- Brute force attacks succeed
- APIs get DDoS'd by accident or intent
- One bad actor affects all users
- You get a surprise bill from your cloud provider

### Express.js with express-rate-limit

```javascript
const rateLimit = require('express-rate-limit');
const RedisStore = require('rate-limit-redis').default;
const { createClient } = require('redis');

const redisClient = createClient({ url: process.env.REDIS_URL });
redisClient.connect();

// General API rate limit
const apiLimiter = rateLimit({
  store: new RedisStore({ sendCommand: (...args) => redisClient.sendCommand(args) }),
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // 100 requests per window
  standardHeaders: true,
  legacyHeaders: false,
  message: { error: 'Too many requests, please try again later' },
  skip: (req) => {
    // Skip rate limiting for health checks
    return req.path === '/health';
  }
});

// Strict limit for auth endpoints
const authLimiter = rateLimit({
  store: new RedisStore({ sendCommand: (...args) => redisClient.sendCommand(args) }),
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 5, // 5 attempts
  message: { error: 'Too many login attempts, please try again in 15 minutes' },
  keyGenerator: (req) => {
    // Rate limit by IP + email to prevent distributed attacks
    return `${req.ip}-${req.body?.email || 'unknown'}`;
  }
});

// Very strict limit for password reset
const passwordResetLimiter = rateLimit({
  store: new RedisStore({ sendCommand: (...args) => redisClient.sendCommand(args) }),
  windowMs: 60 * 60 * 1000, // 1 hour
  max: 3, // 3 requests per hour
  message: { error: 'Too many password reset requests' }
});

// Apply limiters
app.use('/api/', apiLimiter);
app.use('/auth/login', authLimiter);
app.use('/auth/forgot-password', passwordResetLimiter);
```

### Sliding window implementation (custom)

```javascript
// Redis-based sliding window rate limiter
class SlidingWindowRateLimiter {
  constructor(redisClient, options = {}) {
    this.redis = redisClient;
    this.windowMs = options.windowMs || 60000; // 1 minute default
    this.maxRequests = options.maxRequests || 100;
    this.keyPrefix = options.keyPrefix || 'ratelimit';
  }

  async isAllowed(identifier) {
    const now = Date.now();
    const windowStart = now - this.windowMs;
    const key = `${this.keyPrefix}:${identifier}`;

    // Remove old entries and count recent ones
    const multi = this.redis.multi();
    multi.zRemRangeByScore(key, 0, windowStart);
    multi.zCard(key);
    multi.zAdd(key, { score: now, value: `${now}-${Math.random()}` });
    multi.expire(key, Math.ceil(this.windowMs / 1000));

    const results = await multi.exec();
    const requestCount = results[1];

    return {
      allowed: requestCount < this.maxRequests,
      remaining: Math.max(0, this.maxRequests - requestCount - 1),
      resetAt: now + this.windowMs
    };
  }
}

// Express middleware
function createRateLimitMiddleware(limiter) {
  return async (req, res, next) => {
    const identifier = req.ip;
    const result = await limiter.isAllowed(identifier);

    res.setHeader('X-RateLimit-Limit', limiter.maxRequests);
    res.setHeader('X-RateLimit-Remaining', result.remaining);
    res.setHeader('X-RateLimit-Reset', result.resetAt);

    if (!result.allowed) {
      return res.status(429).json({ error: 'Rate limit exceeded' });
    }

    next();
  };
}
```

### Per-user rate limiting with API keys

```javascript
// Different limits based on tier
const tierLimits = {
  free: { windowMs: 60000, max: 10 },
  pro: { windowMs: 60000, max: 100 },
  enterprise: { windowMs: 60000, max: 1000 }
};

async function apiKeyRateLimiter(req, res, next) {
  const apiKey = req.headers['x-api-key'];

  if (!apiKey) {
    return res.status(401).json({ error: 'API key required' });
  }

  // Look up API key
  const keyData = await db.query(
    'SELECT user_id, tier, revoked FROM api_keys WHERE key_hash = $1',
    [hashApiKey(apiKey)]
  );

  if (keyData.rows.length === 0 || keyData.rows[0].revoked) {
    return res.status(401).json({ error: 'Invalid API key' });
  }

  const { user_id, tier } = keyData.rows[0];
  const limits = tierLimits[tier] || tierLimits.free;

  // Rate limit by user, not by key (prevents key rotation abuse)
  const limiter = new SlidingWindowRateLimiter(redisClient, {
    ...limits,
    keyPrefix: 'apikey'
  });

  const result = await limiter.isAllowed(user_id);

  res.setHeader('X-RateLimit-Limit', limits.max);
  res.setHeader('X-RateLimit-Remaining', result.remaining);
  res.setHeader('X-RateLimit-Reset', result.resetAt);

  if (!result.allowed) {
    return res.status(429).json({ error: 'Rate limit exceeded' });
  }

  req.userId = user_id;
  next();
}
```

## Input validation

### Validation with Zod (TypeScript/JavaScript)

```javascript
const { z } = require('zod');

// Define schemas
const createUserSchema = z.object({
  email: z.string().email().max(255),
  password: z.string().min(12).max(128),
  name: z.string().min(1).max(100).optional()
});

const updateProfileSchema = z.object({
  name: z.string().min(1).max(100).optional(),
  bio: z.string().max(500).optional(),
  website: z.string().url().optional().or(z.literal(''))
});

const paginationSchema = z.object({
  page: z.coerce.number().int().min(1).default(1),
  limit: z.coerce.number().int().min(1).max(100).default(20)
});

// Middleware factory
function validate(schema) {
  return (req, res, next) => {
    const result = schema.safeParse(req.body);

    if (!result.success) {
      return res.status(400).json({
        error: 'Validation failed',
        details: result.error.issues.map(issue => ({
          field: issue.path.join('.'),
          message: issue.message
        }))
      });
    }

    req.validated = result.data;
    next();
  };
}

// Usage
app.post('/users', validate(createUserSchema), async (req, res) => {
  const { email, password, name } = req.validated;
  // Data is validated and typed
});
```

### Sanitization

```javascript
const createDOMPurify = require('dompurify');
const { JSDOM } = require('jsdom');
const validator = require('validator');

const window = new JSDOM('').window;
const DOMPurify = createDOMPurify(window);

// HTML sanitization (when you MUST allow some HTML)
function sanitizeHtml(dirty) {
  return DOMPurify.sanitize(dirty, {
    ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'a', 'p', 'br'],
    ALLOWED_ATTR: ['href'],
    ALLOW_DATA_ATTR: false
  });
}

// String sanitization
function sanitizeString(str) {
  if (typeof str !== 'string') return '';

  return str
    .trim()
    .slice(0, 10000) // Max length
    .replace(/[\x00-\x1F\x7F]/g, ''); // Remove control characters
}

// SQL-safe identifier (for dynamic column names)
function sanitizeIdentifier(str) {
  // Only allow alphanumeric and underscores
  if (!/^[a-zA-Z_][a-zA-Z0-9_]*$/.test(str)) {
    throw new Error('Invalid identifier');
  }
  return str;
}

// Filename sanitization
function sanitizeFilename(filename) {
  return filename
    .replace(/[^a-zA-Z0-9._-]/g, '_')
    .replace(/\.{2,}/g, '.')
    .slice(0, 255);
}
```

### Preventing SQL injection

```javascript
// BAD: String interpolation
const query = `SELECT * FROM users WHERE id = ${userId}`;

// BAD: String concatenation
const query = 'SELECT * FROM users WHERE id = ' + userId;

// BAD: Template literals with user input
const query = `SELECT * FROM users WHERE name = '${name}'`;

// GOOD: Parameterized queries (PostgreSQL)
const result = await db.query(
  'SELECT * FROM users WHERE id = $1',
  [userId]
);

// GOOD: Parameterized queries (MySQL)
const result = await db.query(
  'SELECT * FROM users WHERE id = ?',
  [userId]
);

// GOOD: Query builders (Knex)
const users = await knex('users')
  .where('id', userId)
  .first();

// GOOD: ORMs (Prisma)
const user = await prisma.user.findUnique({
  where: { id: userId }
});

// When you need dynamic column names (rare)
const allowedColumns = ['name', 'email', 'created_at'];
const sortColumn = allowedColumns.includes(req.query.sort)
  ? req.query.sort
  : 'created_at';

const query = `SELECT * FROM users ORDER BY ${sortColumn}`; // Safe because allowlisted
```

### Preventing XSS

```javascript
// BAD: Directly inserting user content
res.send(`<h1>Hello ${userName}</h1>`);

// GOOD: Use a template engine with auto-escaping
// EJS (auto-escapes by default with <%= %>)
res.render('greeting', { name: userName });

// GOOD: Escape manually when needed
const escapeHtml = require('escape-html');
res.send(`<h1>Hello ${escapeHtml(userName)}</h1>`);

// GOOD: Set Content-Type for JSON responses
res.json({ name: userName }); // Express sets correct headers

// In React/Vue/Angular: Framework handles escaping by default
// Just don't use dangerouslySetInnerHTML / v-html / [innerHTML]
```

## CORS configuration

### Express.js

```javascript
const cors = require('cors');

// Development: Allow localhost
const developmentOrigins = [
  'http://localhost:3000',
  'http://localhost:5173',
  'http://127.0.0.1:3000'
];

// Production: Specific domains only
const productionOrigins = [
  'https://yourapp.com',
  'https://www.yourapp.com',
  'https://app.yourapp.com'
];

const allowedOrigins = process.env.NODE_ENV === 'production'
  ? productionOrigins
  : [...productionOrigins, ...developmentOrigins];

const corsOptions = {
  origin: (origin, callback) => {
    // Allow requests with no origin (mobile apps, curl, etc.)
    if (!origin) {
      return callback(null, true);
    }

    if (allowedOrigins.includes(origin)) {
      callback(null, true);
    } else {
      callback(new Error('Not allowed by CORS'));
    }
  },
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'PATCH'],
  allowedHeaders: ['Content-Type', 'Authorization', 'X-API-Key'],
  exposedHeaders: ['X-RateLimit-Limit', 'X-RateLimit-Remaining'],
  credentials: true, // Allow cookies
  maxAge: 86400 // Cache preflight for 24 hours
};

app.use(cors(corsOptions));

// Handle CORS errors
app.use((err, req, res, next) => {
  if (err.message === 'Not allowed by CORS') {
    return res.status(403).json({ error: 'CORS not allowed' });
  }
  next(err);
});
```

### Common CORS mistakes

```javascript
// BAD: Allow all origins
app.use(cors()); // Defaults to '*'

// BAD: Allow all origins with credentials
app.use(cors({ origin: '*', credentials: true })); // Browsers will reject this

// BAD: Reflecting Origin header (allows any origin)
app.use(cors({
  origin: (origin, cb) => cb(null, origin) // Never do this
}));

// BAD: Regex that's too permissive
const origin = /yourapp\.com/; // Matches evilyourapp.com too!

// GOOD: Exact match or strict regex
const origin = /^https:\/\/(www\.)?yourapp\.com$/;
```

## API key management

### Secure key generation and storage

```javascript
const crypto = require('crypto');

// Generate API key
function generateApiKey() {
  // Format: prefix_randomBytes
  // Prefix helps identify key type and makes it recognizable
  const prefix = 'sk_live';
  const randomPart = crypto.randomBytes(24).toString('base64url');
  return `${prefix}_${randomPart}`;
}

// Hash for storage (never store plain keys)
function hashApiKey(key) {
  return crypto.createHash('sha256').update(key).digest('hex');
}

// Create new API key
app.post('/api-keys', requireAuth, async (req, res) => {
  const { name } = req.body;

  // Generate key
  const plainKey = generateApiKey();
  const keyHash = hashApiKey(plainKey);

  // Store only the hash
  await db.query(
    `INSERT INTO api_keys (user_id, key_hash, name, created_at)
     VALUES ($1, $2, $3, NOW())`,
    [req.userId, keyHash, name]
  );

  // Return plain key ONCE - user must save it
  res.json({
    key: plainKey,
    message: 'Save this key now. It will not be shown again.'
  });
});

// Verify API key
async function verifyApiKey(key) {
  const keyHash = hashApiKey(key);

  const result = await db.query(
    `SELECT id, user_id, revoked, last_used_at
     FROM api_keys WHERE key_hash = $1`,
    [keyHash]
  );

  if (result.rows.length === 0) {
    return null;
  }

  const keyData = result.rows[0];

  if (keyData.revoked) {
    return null;
  }

  // Update last used timestamp
  await db.query(
    'UPDATE api_keys SET last_used_at = NOW() WHERE id = $1',
    [keyData.id]
  );

  return keyData;
}

// Revoke API key
app.delete('/api-keys/:id', requireAuth, async (req, res) => {
  // Users can only revoke their own keys
  await db.query(
    'UPDATE api_keys SET revoked = true, revoked_at = NOW() WHERE id = $1 AND user_id = $2',
    [req.params.id, req.userId]
  );

  res.json({ success: true });
});
```

### API key middleware

```javascript
async function apiKeyAuth(req, res, next) {
  // Check multiple locations for API key
  const apiKey = req.headers['x-api-key']
    || req.headers['authorization']?.replace('Bearer ', '')
    || req.query.api_key;

  if (!apiKey) {
    return res.status(401).json({
      error: 'API key required',
      hint: 'Pass API key in X-API-Key header'
    });
  }

  const keyData = await verifyApiKey(apiKey);

  if (!keyData) {
    // Don't reveal if key exists but is revoked
    return res.status(401).json({ error: 'Invalid API key' });
  }

  req.apiKeyId = keyData.id;
  req.userId = keyData.user_id;

  next();
}
```

## Request size limits

```javascript
const express = require('express');

// Global body size limit
app.use(express.json({ limit: '100kb' }));
app.use(express.urlencoded({ limit: '100kb', extended: true }));

// Per-route limits
app.post('/api/upload', express.json({ limit: '10mb' }), (req, res) => {
  // Handle large upload
});

// File upload limits
const multer = require('multer');
const upload = multer({
  limits: {
    fileSize: 5 * 1024 * 1024, // 5MB
    files: 5 // Max 5 files
  },
  fileFilter: (req, file, cb) => {
    const allowedTypes = ['image/jpeg', 'image/png', 'image/gif', 'application/pdf'];
    if (allowedTypes.includes(file.mimetype)) {
      cb(null, true);
    } else {
      cb(new Error('Invalid file type'));
    }
  }
});

app.post('/upload', upload.single('file'), (req, res) => {
  // Handle upload
});
```

## Response security

### Don't leak information

```javascript
// BAD: Leaking stack traces
app.use((err, req, res, next) => {
  res.status(500).json({
    error: err.message,
    stack: err.stack // Never in production!
  });
});

// GOOD: Generic error in production
app.use((err, req, res, next) => {
  console.error(err); // Log full error server-side

  if (process.env.NODE_ENV === 'production') {
    res.status(500).json({ error: 'Internal server error' });
  } else {
    res.status(500).json({ error: err.message, stack: err.stack });
  }
});

// BAD: Revealing database structure
res.status(400).json({
  error: 'duplicate key value violates unique constraint "users_email_key"'
});

// GOOD: User-friendly error
res.status(400).json({
  error: 'An account with this email already exists'
});
```

### Security headers

```javascript
const helmet = require('helmet');

app.use(helmet());

// Or configure individually
app.use(helmet.contentSecurityPolicy({
  directives: {
    defaultSrc: ["'self'"],
    scriptSrc: ["'self'"],
    styleSrc: ["'self'", "'unsafe-inline'"],
    imgSrc: ["'self'", "data:", "https:"],
    connectSrc: ["'self'", "https://api.yourapp.com"],
    fontSrc: ["'self'", "https://fonts.gstatic.com"],
    objectSrc: ["'none'"],
    upgradeInsecureRequests: []
  }
}));

app.use(helmet.hsts({
  maxAge: 31536000,
  includeSubDomains: true,
  preload: true
}));
```

## Timeout protection

```javascript
// Request timeout middleware
function timeout(ms) {
  return (req, res, next) => {
    res.setTimeout(ms, () => {
      res.status(408).json({ error: 'Request timeout' });
    });
    next();
  };
}

app.use(timeout(30000)); // 30 second default

// External API call timeout
async function fetchWithTimeout(url, options = {}, timeoutMs = 5000) {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeoutMs);

  try {
    const response = await fetch(url, {
      ...options,
      signal: controller.signal
    });
    return response;
  } finally {
    clearTimeout(timeoutId);
  }
}

// Database query timeout
const result = await db.query({
  text: 'SELECT * FROM large_table WHERE condition = $1',
  values: [value],
  timeout: 5000 // 5 second query timeout
});
```

## FastAPI (Python) equivalents

```python
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter
from slowapi.util import get_remote_address
from pydantic import BaseModel, EmailStr, Field
import hashlib
import secrets

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourapp.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Rate limiting
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/api/login")
@limiter.limit("5/minute")
async def login(request: Request, credentials: LoginRequest):
    # Handle login
    pass

# Input validation with Pydantic
class CreateUserRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=12, max_length=128)
    name: str = Field(max_length=100, default=None)

@app.post("/users")
async def create_user(user: CreateUserRequest):
    # Data is already validated
    pass

# API key generation
def generate_api_key() -> str:
    return f"sk_live_{secrets.token_urlsafe(24)}"

def hash_api_key(key: str) -> str:
    return hashlib.sha256(key.encode()).hexdigest()
```

## Security checklist for APIs

- [ ] Rate limiting on all endpoints
- [ ] Stricter limits on auth endpoints
- [ ] Input validation with schema library
- [ ] Parameterized database queries
- [ ] CORS configured for specific origins
- [ ] API keys hashed before storage
- [ ] Request size limits configured
- [ ] Timeouts on all external calls
- [ ] Security headers via Helmet or equivalent
- [ ] Error messages don't leak system info
- [ ] All auth via HTTPS only
- [ ] API versioning for breaking changes
