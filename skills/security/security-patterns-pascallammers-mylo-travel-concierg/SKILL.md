---
name: security-patterns
description: Implement comprehensive security patterns to protect applications against OWASP Top 10 vulnerabilities including XSS, CSRF, SQL injection, authentication bypass, and data exposure. Use when handling user data, implementing authentication and authorization, validating input, encrypting sensitive data, preventing injection attacks, securing API endpoints, managing sessions and tokens, implementing rate limiting, configuring security headers, or building security-critical features that require defense-in-depth protection.
---

# Security Patterns - Building Secure Applications

## When to use this skill

- Implementing authentication and authorization systems
- Handling sensitive user data and personal information
- Validating and sanitizing all user inputs
- Preventing SQL injection with parameterized queries
- Protecting against XSS attacks with output escaping
- Implementing CSRF protection with tokens
- Encrypting data at rest and in transit
- Securing API endpoints with authentication
- Configuring security headers (CSP, HSTS, etc.)
- Implementing rate limiting and DDoS protection
- Managing sessions, JWTs, and authentication tokens
- Conducting security audits and vulnerability assessments

## When to use this skill

- Handling user data, authentication, authorization, or any security-sensitive operations.
- When working on related tasks or features
- During development that requires this expertise

**Use when**: Handling user data, authentication, authorization, or any security-sensitive operations.

## Core Principles

1. **Defense in Depth** - Multiple layers of security
2. **Principle of Least Privilege** - Minimum necessary permissions
3. **Fail Securely** - Errors shouldn't expose sensitive data
4. **Never Trust User Input** - Validate everything
5. **Security by Design** - Not an afterthought

## OWASP Top 10 Protection

### 1. **Injection Prevention** (SQL, NoSQL, Command)

```typescript
// ❌ VULNERABLE - SQL Injection
app.get('/user', (req, res) => {
  const query = `SELECT * FROM users WHERE id = '${req.query.id}'`;
  db.query(query); // Can inject: ?id=' OR '1'='1
});

// ✅ SAFE - Parameterized Query
app.get('/user', (req, res) => {
  const query = 'SELECT * FROM users WHERE id = ?';
  db.query(query, [req.query.id]);
});

// ✅ SAFE - ORM with validation
app.get('/user', async (req, res) => {
  const userId = parseInt(req.query.id, 10);
  if (!userId || isNaN(userId)) {
    return res.status(400).json({ error: 'Invalid ID' });
  }
  const user = await db.users.findById(userId);
  res.json(user);
});
```

### 2. **Authentication & Session Management**

```typescript
// ✅ Password Hashing (NEVER store plaintext)
import bcrypt from 'bcrypt';

async function createUser(email, password) {
  const SALT_ROUNDS = 10;
  const passwordHash = await bcrypt.hash(password, SALT_ROUNDS);
  
  return await db.users.create({
    email,
    passwordHash // Never store password directly!
  });
}

async function verifyPassword(email, password) {
  const user = await db.users.findOne({ email });
  if (!user) return false;
  
  return await bcrypt.compare(password, user.passwordHash);
}

// ✅ JWT Token Authentication
import jwt from 'jsonwebtoken';

function generateToken(userId) {
  return jwt.sign(
    { userId },
    process.env.JWT_SECRET, // Store in environment variable!
    { expiresIn: '1h' }
  );
}

function verifyToken(token) {
  try {
    return jwt.verify(token, process.env.JWT_SECRET);
  } catch (error) {
    return null;
  }
}

// ✅ Session Management
import session from 'express-session';
import RedisStore from 'connect-redis';

app.use(session({
  store: new RedisStore({ client: redisClient }),
  secret: process.env.SESSION_SECRET,
  resave: false,
  saveUninitialized: false,
  cookie: {
    secure: true, // HTTPS only
    httpOnly: true, // No JavaScript access
    maxAge: 1000 * 60 * 60 * 24, // 24 hours
    sameSite: 'strict' // CSRF protection
  }
}));
```

### 3. **XSS (Cross-Site Scripting) Prevention**

```typescript
// ❌ VULNERABLE - Direct HTML insertion
app.get('/profile', (req, res) => {
  const html = `<h1>Welcome ${req.query.name}</h1>`;
  res.send(html); // Can inject: ?name=<script>alert('xss')</script>
});

// ✅ SAFE - Template escaping (React auto-escapes)
function Profile({ name }) {
  return <h1>Welcome {name}</h1>; // React escapes by default
}

// ✅ SAFE - Explicit sanitization for rich content
import DOMPurify from 'isomorphic-dompurify';

function RichContent({ html }) {
  const sanitized = DOMPurify.sanitize(html, {
    ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'p'],
    ALLOWED_ATTR: []
  });
  
  return <div dangerouslySetInnerHTML={{ __html: sanitized }} />;
}

// ✅ Content Security Policy Headers
app.use((req, res, next) => {
  res.setHeader(
    'Content-Security-Policy',
    "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'"
  );
  next();
});
```

### 4. **CSRF (Cross-Site Request Forgery) Protection**

```typescript
// ✅ CSRF Tokens
import csrf from 'csurf';

const csrfProtection = csrf({ cookie: true });

app.get('/form', csrfProtection, (req, res) => {
  res.render('form', { csrfToken: req.csrfToken() });
});

app.post('/submit', csrfProtection, (req, res) => {
  // Token validated automatically
  res.json({ success: true });
});

// ✅ SameSite Cookies
res.cookie('session', sessionId, {
  sameSite: 'strict', // Prevents CSRF
  secure: true,
  httpOnly: true
});

// ✅ Check Origin/Referer Headers
app.use((req, res, next) => {
  const origin = req.get('origin') || req.get('referer');
  if (origin && !origin.startsWith('https://yourdomain.com')) {
    return res.status(403).json({ error: 'Invalid origin' });
  }
  next();
});
```

### 5. **Access Control & Authorization**

```typescript
// ✅ Role-Based Access Control (RBAC)
const ROLES = {
  ADMIN: 'admin',
  USER: 'user',
  GUEST: 'guest'
};

function requireRole(role) {
  return (req, res, next) => {
    if (!req.user) {
      return res.status(401).json({ error: 'Not authenticated' });
    }
    
    if (req.user.role !== role) {
      return res.status(403).json({ error: 'Insufficient permissions' });
    }
    
    next();
  };
}

app.delete('/users/:id', requireRole(ROLES.ADMIN), async (req, res) => {
  await db.users.delete(req.params.id);
  res.json({ success: true });
});

// ✅ Resource-Based Access Control
async function canEditPost(userId, postId) {
  const post = await db.posts.findById(postId);
  if (!post) return false;
  
  // User can edit their own posts or if admin
  const user = await db.users.findById(userId);
  return post.authorId === userId || user.role === 'admin';
}

app.put('/posts/:id', async (req, res) => {
  if (!await canEditPost(req.user.id, req.params.id)) {
    return res.status(403).json({ error: 'Cannot edit this post' });
  }
  
  const updated = await db.posts.update(req.params.id, req.body);
  res.json(updated);
});
```

### 6. **Rate Limiting & DDoS Protection**

```typescript
// ✅ Rate Limiting
import rateLimit from 'express-rate-limit';

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // Limit each IP to 100 requests per window
  message: 'Too many requests, please try again later'
});

app.use('/api/', limiter);

// ✅ Stricter limits for auth endpoints
const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 5, // Only 5 login attempts per 15 minutes
  skipSuccessfulRequests: true
});

app.post('/login', authLimiter, async (req, res) => {
  // Login logic
});

// ✅ Redis-based rate limiting (distributed)
import RedisStore from 'rate-limit-redis';

const limiter = rateLimit({
  store: new RedisStore({
    client: redisClient
  }),
  windowMs: 15 * 60 * 1000,
  max: 100
});
```

### 7. **Sensitive Data Exposure Prevention**

```typescript
// ❌ VULNERABLE - Exposing sensitive data
app.get('/user/:id', async (req, res) => {
  const user = await db.users.findById(req.params.id);
  res.json(user); // Includes password hash, internal IDs, etc!
});

// ✅ SAFE - Explicit field selection
app.get('/user/:id', async (req, res) => {
  const user = await db.users.findById(req.params.id);
  
  res.json({
    id: user.id,
    name: user.name,
    email: user.email
    // passwordHash NOT included
  });
});

// ✅ SAFE - Using DTOs/Serializers
class UserDTO {
  static fromUser(user) {
    return {
      id: user.id,
      name: user.name,
      email: user.email,
      createdAt: user.createdAt
    };
  }
}

app.get('/user/:id', async (req, res) => {
  const user = await db.users.findById(req.params.id);
  res.json(UserDTO.fromUser(user));
});

// ✅ Encrypt sensitive data at rest
import crypto from 'crypto';

function encrypt(text) {
  const key = Buffer.from(process.env.ENCRYPTION_KEY, 'hex');
  const iv = crypto.randomBytes(16);
  const cipher = crypto.createCipheriv('aes-256-cbc', key, iv);
  
  let encrypted = cipher.update(text, 'utf8', 'hex');
  encrypted += cipher.final('hex');
  
  return iv.toString('hex') + ':' + encrypted;
}

function decrypt(encrypted) {
  const key = Buffer.from(process.env.ENCRYPTION_KEY, 'hex');
  const parts = encrypted.split(':');
  const iv = Buffer.from(parts[0], 'hex');
  const encryptedText = parts[1];
  const decipher = crypto.createDecipheriv('aes-256-cbc', key, iv);
  
  let decrypted = decipher.update(encryptedText, 'hex', 'utf8');
  decrypted += decipher.final('utf8');
  
  return decrypted;
}
```

### 8. **Input Validation**

```typescript
// ✅ Schema Validation with Zod
import { z } from 'zod';

const CreateUserSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8).max(100),
  age: z.number().int().min(0).max(150),
  website: z.string().url().optional()
});

app.post('/users', async (req, res) => {
  try {
    const validated = CreateUserSchema.parse(req.body);
    const user = await createUser(validated);
    res.json(user);
  } catch (error) {
    res.status(400).json({ error: error.errors });
  }
});

// ✅ Sanitize file uploads
import multer from 'multer';
import path from 'path';

const upload = multer({
  dest: 'uploads/',
  limits: {
    fileSize: 5 * 1024 * 1024 // 5MB max
  },
  fileFilter: (req, file, cb) => {
    const allowedTypes = ['image/jpeg', 'image/png', 'image/gif'];
    
    if (!allowedTypes.includes(file.mimetype)) {
      return cb(new Error('Invalid file type'));
    }
    
    cb(null, true);
  }
});

app.post('/upload', upload.single('avatar'), (req, res) => {
  res.json({ filename: req.file.filename });
});
```

### 9. **Logging & Monitoring**

```typescript
// ✅ Security event logging
import winston from 'winston';

const securityLogger = winston.createLogger({
  level: 'info',
  format: winston.format.json(),
  transports: [
    new winston.transports.File({ filename: 'security.log' })
  ]
});

// Log failed authentication attempts
app.post('/login', async (req, res) => {
  const user = await verifyCredentials(req.body.email, req.body.password);
  
  if (!user) {
    securityLogger.warn('Failed login attempt', {
      email: req.body.email,
      ip: req.ip,
      userAgent: req.get('user-agent'),
      timestamp: new Date().toISOString()
    });
    
    return res.status(401).json({ error: 'Invalid credentials' });
  }
  
  res.json({ token: generateToken(user.id) });
});

// Log privilege escalation attempts
app.put('/users/:id/role', requireAdmin, async (req, res) => {
  securityLogger.info('Role change', {
    adminId: req.user.id,
    targetUserId: req.params.id,
    newRole: req.body.role,
    timestamp: new Date().toISOString()
  });
  
  await db.users.updateRole(req.params.id, req.body.role);
  res.json({ success: true });
});
```

### 10. **Security Headers**

```typescript
// ✅ Essential security headers
import helmet from 'helmet';

app.use(helmet()); // Sets multiple headers automatically

// Or manually:
app.use((req, res, next) => {
  // Prevent clickjacking
  res.setHeader('X-Frame-Options', 'DENY');
  
  // Prevent MIME sniffing
  res.setHeader('X-Content-Type-Options', 'nosniff');
  
  // Enable XSS filter
  res.setHeader('X-XSS-Protection', '1; mode=block');
  
  // Strict Transport Security (HTTPS only)
  res.setHeader('Strict-Transport-Security', 'max-age=31536000; includeSubDomains');
  
  // Referrer Policy
  res.setHeader('Referrer-Policy', 'strict-origin-when-cross-origin');
  
  // Permissions Policy
  res.setHeader('Permissions-Policy', 'geolocation=(), microphone=(), camera=()');
  
  next();
});
```

## Environment & Secrets Management

```typescript
// ❌ NEVER do this
const apiKey = 'sk_live_abc123'; // Hardcoded secret
const dbPassword = 'password123';

// ✅ Use environment variables
import dotenv from 'dotenv';
dotenv.config();

const apiKey = process.env.API_KEY;
const dbPassword = process.env.DB_PASSWORD;

// ✅ Validate required secrets on startup
const requiredEnvVars = [
  'DATABASE_URL',
  'JWT_SECRET',
  'API_KEY'
];

for (const envVar of requiredEnvVars) {
  if (!process.env[envVar]) {
    console.error(`Missing required environment variable: ${envVar}`);
    process.exit(1);
  }
}

// ✅ Use secret management services (production)
import { SecretsManager } from '@aws-sdk/client-secrets-manager';

async function getSecret(secretName) {
  const client = new SecretsManager({ region: 'us-east-1' });
  const response = await client.getSecretValue({ SecretId: secretName });
  return JSON.parse(response.SecretString);
}
```

## Security Checklist

```
Authentication & Sessions:
□ Passwords hashed with bcrypt/argon2
□ JWT secrets stored securely
□ Token expiration implemented
□ Session cookies: httpOnly, secure, sameSite
□ MFA available for sensitive operations

Input Validation:
□ All inputs validated with schema
□ SQL injection prevented (parameterized queries)
□ XSS prevented (output escaping)
□ File uploads restricted and validated
□ URLs validated before redirects

Authorization:
□ Authentication required for protected routes
□ Role-based access control implemented
□ Resource ownership verified
□ Principle of least privilege enforced

Data Protection:
□ HTTPS enforced everywhere
□ Sensitive data encrypted at rest
□ Secrets in environment variables (not code)
□ No sensitive data in logs/errors
□ PII handling compliant with regulations

Infrastructure:
□ Rate limiting on public endpoints
□ Security headers configured
□ CORS properly configured
□ Dependency vulnerabilities scanned
□ Security monitoring and alerting

Audit & Compliance:
□ Security events logged
□ Access logs retained
□ Regular security audits scheduled
□ Incident response plan documented
```

## Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OWASP Cheat Sheets](https://cheatsheetseries.owasp.org/)
- [CWE Top 25](https://cwe.mitre.org/top25/)
- [Security Headers](https://securityheaders.com/)

---

**Remember**: Security is not optional. It must be built into every layer from day one.
