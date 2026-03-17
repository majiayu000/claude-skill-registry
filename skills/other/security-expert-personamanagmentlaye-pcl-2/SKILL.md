---
name: security-expert
version: 1.0.0
description: Expert-level application security, OWASP Top 10, penetration testing, and security best practices
category: security
tags: [security, owasp, pentest, appsec, vulnerability, encryption, authentication]
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash(nmap:*, burpsuite:*, zap:*)
---

# Security Expert

Expert guidance for application security, vulnerability assessment, penetration testing, OWASP Top 10, secure coding practices, and security architecture.

## Core Concepts

### Security Principles
- Defense in depth
- Least privilege
- Secure by default
- Fail securely
- Complete mediation
- Separation of duties
- Zero trust architecture

### OWASP Top 10 (2021)
1. Broken Access Control
2. Cryptographic Failures
3. Injection
4. Insecure Design
5. Security Misconfiguration
6. Vulnerable and Outdated Components
7. Identification and Authentication Failures
8. Software and Data Integrity Failures
9. Security Logging and Monitoring Failures
10. Server-Side Request Forgery (SSRF)

### Security Domains
- Authentication & Authorization
- Cryptography
- Input validation
- Session management
- Error handling
- Secure communications
- Data protection

## OWASP Top 10 Vulnerabilities

### 1. Broken Access Control
```javascript
// ❌ Vulnerable: No authorization check
app.get('/api/users/:id/profile', async (req, res) => {
  const profile = await db.users.findById(req.params.id);
  res.json(profile);
});

// ✅ Secure: Verify user owns the resource
app.get('/api/users/:id/profile', authenticate, async (req, res) => {
  if (req.user.id !== req.params.id && !req.user.isAdmin) {
    return res.status(403).json({ error: 'Forbidden' });
  }

  const profile = await db.users.findById(req.params.id);
  res.json(profile);
});

// ✅ Better: Use middleware
const authorizeResource = (resourceType) => async (req, res, next) => {
  const resourceId = req.params.id;
  const resource = await db[resourceType].findById(resourceId);

  if (!resource) {
    return res.status(404).json({ error: 'Not found' });
  }

  if (resource.userId !== req.user.id && !req.user.isAdmin) {
    return res.status(403).json({ error: 'Forbidden' });
  }

  req.resource = resource;
  next();
};

app.delete('/api/posts/:id', authenticate, authorizeResource('posts'), async (req, res) => {
  await req.resource.delete();
  res.status(204).send();
});
```

### 2. Injection (SQL, NoSQL, Command)
```javascript
// ❌ SQL Injection vulnerability
app.get('/users', (req, res) => {
  const query = `SELECT * FROM users WHERE name = '${req.query.name}'`;
  db.query(query, (err, results) => {
    res.json(results);
  });
});
// Attack: ?name=' OR '1'='1

// ✅ Secure: Use parameterized queries
app.get('/users', async (req, res) => {
  const results = await db.query(
    'SELECT * FROM users WHERE name = ?',
    [req.query.name]
  );
  res.json(results);
});

// ❌ Command Injection
const { exec } = require('child_process');
app.post('/convert', (req, res) => {
  exec(`convert ${req.body.filename} output.pdf`, (err, stdout) => {
    res.send(stdout);
  });
});
// Attack: filename="; rm -rf / #"

// ✅ Secure: Use safe APIs, validate input
const { spawn } = require('child_process');
app.post('/convert', (req, res) => {
  const filename = path.basename(req.body.filename); // Remove path traversal
  if (!/^[a-zA-Z0-9_-]+\.(jpg|png)$/.test(filename)) {
    return res.status(400).json({ error: 'Invalid filename' });
  }

  const process = spawn('convert', [filename, 'output.pdf']);
  // Handle process output safely
});

// ❌ NoSQL Injection (MongoDB)
app.post('/login', async (req, res) => {
  const user = await User.findOne({
    username: req.body.username,
    password: req.body.password
  });
});
// Attack: {"username": {"$ne": null}, "password": {"$ne": null}}

// ✅ Secure: Sanitize input, use proper types
app.post('/login', async (req, res) => {
  const { username, password } = req.body;

  if (typeof username !== 'string' || typeof password !== 'string') {
    return res.status(400).json({ error: 'Invalid input' });
  }

  const user = await User.findOne({ username });
  if (!user || !(await bcrypt.compare(password, user.passwordHash))) {
    return res.status(401).json({ error: 'Invalid credentials' });
  }

  // Create session
});
```

### 3. Cross-Site Scripting (XSS)
```javascript
// ❌ Reflected XSS
app.get('/search', (req, res) => {
  res.send(`<h1>Results for: ${req.query.q}</h1>`);
});
// Attack: ?q=<script>alert(document.cookie)</script>

// ✅ Secure: Escape output
const escapeHtml = (unsafe) => {
  return unsafe
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
};

app.get('/search', (req, res) => {
  res.send(`<h1>Results for: ${escapeHtml(req.query.q)}</h1>`);
});

// ✅ Better: Use templating engine with auto-escaping
app.get('/search', (req, res) => {
  res.render('search', { query: req.query.q }); // Automatically escaped
});

// ✅ Content Security Policy
app.use((req, res, next) => {
  res.setHeader(
    'Content-Security-Policy',
    "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:;"
  );
  next();
});
```

### 4. Cross-Site Request Forgery (CSRF)
```javascript
// ❌ Vulnerable: No CSRF protection
app.post('/api/transfer', authenticate, async (req, res) => {
  await transferMoney(req.user.id, req.body.to, req.body.amount);
  res.json({ success: true });
});

// ✅ Secure: Use CSRF tokens
const csrf = require('csurf');
const csrfProtection = csrf({ cookie: true });

app.get('/transfer', csrfProtection, (req, res) => {
  res.render('transfer', { csrfToken: req.csrfToken() });
});

app.post('/api/transfer', csrfProtection, authenticate, async (req, res) => {
  await transferMoney(req.user.id, req.body.to, req.body.amount);
  res.json({ success: true });
});

// ✅ Also use SameSite cookies
app.use(session({
  cookie: {
    httpOnly: true,
    secure: true,
    sameSite: 'strict'
  }
}));
```

### 5. Security Misconfiguration
```javascript
// ❌ Exposed sensitive information
app.use((err, req, res, next) => {
  res.status(500).json({
    error: err.message,
    stack: err.stack  // Exposes internal details
  });
});

// ✅ Secure: Generic error messages
app.use((err, req, res, next) => {
  console.error(err); // Log internally

  if (process.env.NODE_ENV === 'production') {
    res.status(500).json({ error: 'Internal server error' });
  } else {
    res.status(500).json({ error: err.message, stack: err.stack });
  }
});

// ✅ Security headers
const helmet = require('helmet');
app.use(helmet());

// ✅ Disable unnecessary features
app.disable('x-powered-by');

// ✅ Rate limiting
const rateLimit = require('express-rate-limit');
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100 // limit each IP to 100 requests per windowMs
});
app.use('/api/', limiter);
```

## Authentication & Authorization

### Password Security
```javascript
const bcrypt = require('bcrypt');
const SALT_ROUNDS = 12;

// Hash password
async function hashPassword(password) {
  // Validate password strength
  if (password.length < 12) {
    throw new Error('Password must be at least 12 characters');
  }

  if (!/[A-Z]/.test(password) || !/[a-z]/.test(password) ||
      !/[0-9]/.test(password) || !/[^A-Za-z0-9]/.test(password)) {
    throw new Error('Password must contain uppercase, lowercase, number, and special character');
  }

  return await bcrypt.hash(password, SALT_ROUNDS);
}

// Verify password
async function verifyPassword(password, hash) {
  return await bcrypt.compare(password, hash);
}

// Registration
app.post('/register', async (req, res) => {
  const { email, password } = req.body;

  // Check if user exists
  const existingUser = await User.findOne({ email });
  if (existingUser) {
    return res.status(400).json({ error: 'Email already registered' });
  }

  // Hash password
  const passwordHash = await hashPassword(password);

  // Create user
  const user = await User.create({
    email: email.toLowerCase(),
    passwordHash
  });

  res.status(201).json({ id: user.id });
});
```

### JWT Authentication
```javascript
const jwt = require('jsonwebtoken');
const JWT_SECRET = process.env.JWT_SECRET; // Use strong secret
const JWT_EXPIRY = '15m';
const REFRESH_TOKEN_EXPIRY = '7d';

// Generate tokens
function generateTokens(user) {
  const accessToken = jwt.sign(
    { userId: user.id, email: user.email },
    JWT_SECRET,
    { expiresIn: JWT_EXPIRY }
  );

  const refreshToken = jwt.sign(
    { userId: user.id, type: 'refresh' },
    JWT_SECRET,
    { expiresIn: REFRESH_TOKEN_EXPIRY }
  );

  return { accessToken, refreshToken };
}

// Verify token middleware
function authenticate(req, res, next) {
  const authHeader = req.headers.authorization;

  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return res.status(401).json({ error: 'No token provided' });
  }

  const token = authHeader.substring(7);

  try {
    const decoded = jwt.verify(token, JWT_SECRET);
    req.user = decoded;
    next();
  } catch (err) {
    if (err.name === 'TokenExpiredError') {
      return res.status(401).json({ error: 'Token expired' });
    }
    return res.status(401).json({ error: 'Invalid token' });
  }
}

// Login
app.post('/login', async (req, res) => {
  const { email, password } = req.body;

  const user = await User.findOne({ email: email.toLowerCase() });
  if (!user || !(await verifyPassword(password, user.passwordHash))) {
    // Generic error to prevent username enumeration
    return res.status(401).json({ error: 'Invalid credentials' });
  }

  // Update last login
  await user.update({ lastLoginAt: new Date() });

  const tokens = generateTokens(user);
  res.json(tokens);
});

// Refresh token
app.post('/refresh', async (req, res) => {
  const { refreshToken } = req.body;

  try {
    const decoded = jwt.verify(refreshToken, JWT_SECRET);

    if (decoded.type !== 'refresh') {
      return res.status(401).json({ error: 'Invalid token type' });
    }

    const user = await User.findById(decoded.userId);
    if (!user) {
      return res.status(401).json({ error: 'User not found' });
    }

    const tokens = generateTokens(user);
    res.json(tokens);
  } catch (err) {
    return res.status(401).json({ error: 'Invalid refresh token' });
  }
});
```

### Multi-Factor Authentication (MFA)
```javascript
const speakeasy = require('speakeasy');
const QRCode = require('qrcode');

// Generate MFA secret
app.post('/mfa/setup', authenticate, async (req, res) => {
  const secret = speakeasy.generateSecret({
    name: `MyApp (${req.user.email})`
  });

  // Store secret temporarily
  await redis.setex(`mfa:setup:${req.user.id}`, 300, secret.base32);

  // Generate QR code
  const qrCode = await QRCode.toDataURL(secret.otpauth_url);

  res.json({
    secret: secret.base32,
    qrCode
  });
});

// Verify and enable MFA
app.post('/mfa/verify', authenticate, async (req, res) => {
  const { token } = req.body;
  const secret = await redis.get(`mfa:setup:${req.user.id}`);

  if (!secret) {
    return res.status(400).json({ error: 'MFA setup expired' });
  }

  const verified = speakeasy.totp.verify({
    secret,
    encoding: 'base32',
    token,
    window: 2
  });

  if (!verified) {
    return res.status(400).json({ error: 'Invalid token' });
  }

  // Enable MFA for user
  await User.update(req.user.id, {
    mfaEnabled: true,
    mfaSecret: secret
  });

  await redis.del(`mfa:setup:${req.user.id}`);

  res.json({ success: true });
});

// Login with MFA
app.post('/login/mfa', async (req, res) => {
  const { email, password, mfaToken } = req.body;

  const user = await User.findOne({ email });
  if (!user || !(await verifyPassword(password, user.passwordHash))) {
    return res.status(401).json({ error: 'Invalid credentials' });
  }

  if (user.mfaEnabled) {
    if (!mfaToken) {
      return res.status(401).json({ error: 'MFA token required' });
    }

    const verified = speakeasy.totp.verify({
      secret: user.mfaSecret,
      encoding: 'base32',
      token: mfaToken,
      window: 2
    });

    if (!verified) {
      return res.status(401).json({ error: 'Invalid MFA token' });
    }
  }

  const tokens = generateTokens(user);
  res.json(tokens);
});
```

## Cryptography

### Encryption at Rest
```javascript
const crypto = require('crypto');

const ALGORITHM = 'aes-256-gcm';
const KEY = Buffer.from(process.env.ENCRYPTION_KEY, 'hex'); // 32 bytes

function encrypt(plaintext) {
  const iv = crypto.randomBytes(16);
  const cipher = crypto.createCipheriv(ALGORITHM, KEY, iv);

  let encrypted = cipher.update(plaintext, 'utf8', 'hex');
  encrypted += cipher.final('hex');

  const authTag = cipher.getAuthTag();

  return {
    iv: iv.toString('hex'),
    encrypted,
    authTag: authTag.toString('hex')
  };
}

function decrypt(iv, encrypted, authTag) {
  const decipher = crypto.createDecipheriv(
    ALGORITHM,
    KEY,
    Buffer.from(iv, 'hex')
  );

  decipher.setAuthTag(Buffer.from(authTag, 'hex'));

  let decrypted = decipher.update(encrypted, 'hex', 'utf8');
  decrypted += decipher.final('utf8');

  return decrypted;
}

// Store sensitive data
async function storeSensitiveData(userId, data) {
  const { iv, encrypted, authTag } = encrypt(JSON.stringify(data));

  await db.sensitiveData.create({
    userId,
    iv,
    encrypted,
    authTag
  });
}
```

### Secure Random Generation
```javascript
// ✅ Cryptographically secure random
const crypto = require('crypto');

function generateSecureToken(length = 32) {
  return crypto.randomBytes(length).toString('hex');
}

function generateSecureId() {
  return crypto.randomUUID();
}

// ❌ Don't use Math.random() for security
const insecureToken = Math.random().toString(36); // Predictable!
```

## Input Validation

```javascript
const { body, validationResult } = require('express-validator');

app.post('/api/users',
  // Validation rules
  body('email').isEmail().normalizeEmail(),
  body('name').trim().isLength({ min: 2, max: 100 }).escape(),
  body('age').optional().isInt({ min: 18, max: 120 }),
  body('website').optional().isURL(),

  async (req, res) => {
    // Check validation results
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }

    // Process validated data
    const user = await User.create(req.body);
    res.status(201).json(user);
  }
);

// File upload validation
const multer = require('multer');

const upload = multer({
  limits: {
    fileSize: 5 * 1024 * 1024, // 5MB max
  },
  fileFilter: (req, file, cb) => {
    // Check file type
    const allowedMimes = ['image/jpeg', 'image/png', 'image/gif'];
    if (!allowedMimes.includes(file.mimetype)) {
      return cb(new Error('Invalid file type'));
    }

    // Check file extension
    const ext = path.extname(file.originalname).toLowerCase();
    if (!['.jpg', '.jpeg', '.png', '.gif'].includes(ext)) {
      return cb(new Error('Invalid file extension'));
    }

    cb(null, true);
  }
});

app.post('/upload', upload.single('image'), (req, res) => {
  // Verify file content matches extension
  // Store with random filename to prevent path traversal
  const filename = `${crypto.randomUUID()}${path.extname(req.file.originalname)}`;
  // Save file...
});
```

## Security Headers

```javascript
const helmet = require('helmet');

app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      scriptSrc: ["'self'", "'unsafe-inline'"], // Avoid unsafe-inline in production
      styleSrc: ["'self'", "'unsafe-inline'"],
      imgSrc: ["'self'", 'data:', 'https:'],
      connectSrc: ["'self'"],
      fontSrc: ["'self'"],
      objectSrc: ["'none'"],
      mediaSrc: ["'self'"],
      frameSrc: ["'none'"],
    },
  },
  hsts: {
    maxAge: 31536000,
    includeSubDomains: true,
    preload: true
  },
  frameguard: {
    action: 'deny'
  },
  noSniff: true,
  xssFilter: true,
}));

// Additional headers
app.use((req, res, next) => {
  res.setHeader('X-Content-Type-Options', 'nosniff');
  res.setHeader('X-Frame-Options', 'DENY');
  res.setHeader('X-XSS-Protection', '1; mode=block');
  res.setHeader('Referrer-Policy', 'strict-origin-when-cross-origin');
  res.setHeader('Permissions-Policy', 'geolocation=(), microphone=(), camera=()');
  next();
});
```

## Secure Logging

```javascript
const winston = require('winston');

const logger = winston.createLogger({
  level: 'info',
  format: winston.format.json(),
  transports: [
    new winston.transports.File({ filename: 'error.log', level: 'error' }),
    new winston.transports.File({ filename: 'combined.log' })
  ]
});

// Log security events
function logSecurityEvent(event, details) {
  logger.warn('Security Event', {
    event,
    ...details,
    timestamp: new Date().toISOString()
  });
}

// Failed login attempts
app.post('/login', async (req, res) => {
  const { email, password } = req.body;
  const user = await User.findOne({ email });

  if (!user || !(await verifyPassword(password, user.passwordHash))) {
    logSecurityEvent('failed_login', {
      email,
      ip: req.ip,
      userAgent: req.headers['user-agent']
    });

    return res.status(401).json({ error: 'Invalid credentials' });
  }

  // Success
  logSecurityEvent('successful_login', {
    userId: user.id,
    ip: req.ip
  });

  // Generate tokens...
});

// ❌ Don't log sensitive data
logger.info('User data', user); // May contain passwordHash, tokens

// ✅ Sanitize before logging
logger.info('User data', {
  id: user.id,
  email: user.email,
  // Omit sensitive fields
});
```

## Best Practices

### Secure Development Lifecycle
1. Threat modeling
2. Security requirements
3. Secure coding standards
4. Code review
5. Security testing (SAST/DAST)
6. Vulnerability scanning
7. Penetration testing
8. Security monitoring

### Defense in Depth
- Multiple layers of security
- Assume breach mentality
- Principle of least privilege
- Input validation at every layer
- Output encoding
- Secure configuration

### Security Testing
- Static Application Security Testing (SAST)
- Dynamic Application Security Testing (DAST)
- Interactive Application Security Testing (IAST)
- Software Composition Analysis (SCA)
- Penetration testing
- Bug bounty programs

## Anti-Patterns to Avoid

❌ **Storing passwords in plaintext**: Always hash with bcrypt/argon2
❌ **Rolling your own crypto**: Use established libraries
❌ **Trusting user input**: Validate and sanitize everything
❌ **Exposing sensitive errors**: Use generic error messages
❌ **No rate limiting**: Implement rate limiting on all endpoints
❌ **Weak session management**: Use secure, httpOnly cookies
❌ **No logging**: Log security events for monitoring
❌ **Hardcoded secrets**: Use environment variables

## Resources

- OWASP: https://owasp.org/
- OWASP Top 10: https://owasp.org/Top10/
- CWE Top 25: https://cwe.mitre.org/top25/
- NIST Guidelines: https://www.nist.gov/cybersecurity
- Security Headers: https://securityheaders.com/
- SSL Labs: https://www.ssllabs.com/
