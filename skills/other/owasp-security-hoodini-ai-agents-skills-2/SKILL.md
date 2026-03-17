---
name: owasp-security
description: Implement secure coding practices following OWASP Top 10. Use when preventing security vulnerabilities, implementing authentication, securing APIs, or conducting security reviews. Triggers on OWASP, security, XSS, SQL injection, CSRF, authentication security, secure coding, vulnerability.
---

# OWASP Top 10 Security

Prevent common security vulnerabilities in web applications.

## OWASP Top 10 (2021)

| # | Vulnerability | Prevention |
|---|---------------|------------|
| A01 | Broken Access Control | Proper authorization checks |
| A02 | Cryptographic Failures | Strong encryption, secure storage |
| A03 | Injection | Input validation, parameterized queries |
| A04 | Insecure Design | Threat modeling, secure patterns |
| A05 | Security Misconfiguration | Hardened configs, no defaults |
| A06 | Vulnerable Components | Dependency scanning, updates |
| A07 | Auth Failures | MFA, secure session management |
| A08 | Data Integrity Failures | Input validation, signed updates |
| A09 | Logging Failures | Comprehensive audit logs |
| A10 | SSRF | URL validation, allowlists |

## A01: Broken Access Control

### Prevention Patterns
```typescript
// ❌ BAD: No authorization check
app.get('/api/users/:id', async (req, res) => {
  const user = await db.users.findById(req.params.id);
  res.json(user);
});

// ✅ GOOD: Verify ownership
app.get('/api/users/:id', authenticate, async (req, res) => {
  const userId = req.params.id;
  
  // Users can only access their own data
  if (req.user.id !== userId && req.user.role !== 'admin') {
    return res.status(403).json({ error: 'Forbidden' });
  }
  
  const user = await db.users.findById(userId);
  res.json(user);
});

// ✅ GOOD: Role-based access control (RBAC)
const requireRole = (...roles: string[]) => {
  return (req: Request, res: Response, next: NextFunction) => {
    if (!roles.includes(req.user?.role)) {
      return res.status(403).json({ error: 'Insufficient permissions' });
    }
    next();
  };
};

app.delete('/api/posts/:id', authenticate, requireRole('admin', 'moderator'), deletePost);
```

### Insecure Direct Object Reference (IDOR)
```typescript
// ❌ BAD: Predictable IDs exposed
GET /api/invoices/1001
GET /api/invoices/1002  // Can enumerate others' invoices

// ✅ GOOD: Use UUIDs + ownership check
app.get('/api/invoices/:id', authenticate, async (req, res) => {
  const invoice = await db.invoices.findOne({
    id: req.params.id,
    userId: req.user.id,  // Enforce ownership
  });
  
  if (!invoice) {
    return res.status(404).json({ error: 'Not found' });
  }
  
  res.json(invoice);
});
```

## A02: Cryptographic Failures

### Password Hashing
```typescript
import bcrypt from 'bcrypt';
import crypto from 'crypto';

// ✅ Hash passwords with bcrypt
const SALT_ROUNDS = 12;

async function hashPassword(password: string): Promise<string> {
  return bcrypt.hash(password, SALT_ROUNDS);
}

async function verifyPassword(password: string, hash: string): Promise<boolean> {
  return bcrypt.compare(password, hash);
}

// ✅ Secure token generation
function generateSecureToken(length = 32): string {
  return crypto.randomBytes(length).toString('hex');
}

// ✅ Encrypt sensitive data
const ALGORITHM = 'aes-256-gcm';
const KEY = crypto.scryptSync(process.env.ENCRYPTION_KEY!, 'salt', 32);

function encrypt(text: string): { encrypted: string; iv: string; tag: string } {
  const iv = crypto.randomBytes(16);
  const cipher = crypto.createCipheriv(ALGORITHM, KEY, iv);
  
  let encrypted = cipher.update(text, 'utf8', 'hex');
  encrypted += cipher.final('hex');
  
  return {
    encrypted,
    iv: iv.toString('hex'),
    tag: cipher.getAuthTag().toString('hex'),
  };
}

function decrypt(encrypted: string, iv: string, tag: string): string {
  const decipher = crypto.createDecipheriv(ALGORITHM, KEY, Buffer.from(iv, 'hex'));
  decipher.setAuthTag(Buffer.from(tag, 'hex'));
  
  let decrypted = decipher.update(encrypted, 'hex', 'utf8');
  decrypted += decipher.final('utf8');
  
  return decrypted;
}
```

### Secure Headers
```typescript
import helmet from 'helmet';

app.use(helmet());
app.use(helmet.hsts({ maxAge: 31536000, includeSubDomains: true }));
app.use(helmet.contentSecurityPolicy({
  directives: {
    defaultSrc: ["'self'"],
    scriptSrc: ["'self'", "'strict-dynamic'"],
    styleSrc: ["'self'", "'unsafe-inline'"],
    imgSrc: ["'self'", 'data:', 'https:'],
    connectSrc: ["'self'"],
    fontSrc: ["'self'"],
    objectSrc: ["'none'"],
    frameAncestors: ["'none'"],
  },
}));
```

## A03: Injection

### SQL Injection Prevention
```typescript
// ❌ BAD: String concatenation
const query = `SELECT * FROM users WHERE email = '${email}'`;

// ✅ GOOD: Parameterized queries
// With Prisma
const user = await prisma.user.findUnique({ where: { email } });

// With raw SQL (parameterized)
const user = await db.query('SELECT * FROM users WHERE email = $1', [email]);

// With Knex
const user = await knex('users').where({ email }).first();
```

### NoSQL Injection Prevention
```typescript
// ❌ BAD: Direct user input in query
const user = await User.findOne({ username: req.body.username });
// Attack: { "username": { "$gt": "" } } returns first user

// ✅ GOOD: Validate input type
import { z } from 'zod';

const loginSchema = z.object({
  username: z.string().min(3).max(50),
  password: z.string().min(8),
});

app.post('/login', async (req, res) => {
  const { username, password } = loginSchema.parse(req.body);
  const user = await User.findOne({ username: String(username) });
  // ...
});
```

### Command Injection Prevention
```typescript
import { execFile } from 'child_process';

// ❌ BAD: Shell injection
exec(`convert ${userInput} output.png`);  // userInput: "; rm -rf /"

// ✅ GOOD: Use execFile with array args
execFile('convert', [userInput, 'output.png'], (error, stdout) => {
  // Safe - arguments are not shell-interpreted
});

// ✅ GOOD: Validate and sanitize
const allowedFormats = ['png', 'jpg', 'gif'];
if (!allowedFormats.includes(format)) {
  throw new Error('Invalid format');
}
```

## A04: Insecure Design

### Rate Limiting
```typescript
import rateLimit from 'express-rate-limit';

// General rate limit
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // 100 requests per window
  standardHeaders: true,
  legacyHeaders: false,
});

// Strict limit for auth endpoints
const authLimiter = rateLimit({
  windowMs: 60 * 60 * 1000, // 1 hour
  max: 5, // 5 failed attempts
  skipSuccessfulRequests: true,
});

app.use('/api/', limiter);
app.use('/api/auth/', authLimiter);
```

### Input Validation
```typescript
import { z } from 'zod';

const userSchema = z.object({
  email: z.string().email(),
  password: z.string()
    .min(8)
    .regex(/[A-Z]/, 'Must contain uppercase')
    .regex(/[a-z]/, 'Must contain lowercase')
    .regex(/[0-9]/, 'Must contain number')
    .regex(/[^A-Za-z0-9]/, 'Must contain special character'),
  age: z.number().int().min(13).max(120),
  role: z.enum(['user', 'admin']).default('user'),
});

app.post('/api/users', async (req, res) => {
  try {
    const data = userSchema.parse(req.body);
    // Validated data is safe to use
  } catch (error) {
    if (error instanceof z.ZodError) {
      return res.status(400).json({ errors: error.errors });
    }
    throw error;
  }
});
```

## A05: Security Misconfiguration

### Environment Configuration
```typescript
// ✅ Never expose stack traces in production
app.use((err: Error, req: Request, res: Response, next: NextFunction) => {
  console.error(err.stack); // Log for debugging
  
  res.status(500).json({
    error: process.env.NODE_ENV === 'production' 
      ? 'Internal server error' 
      : err.message,
  });
});

// ✅ Disable sensitive headers
app.disable('x-powered-by');

// ✅ Secure cookie configuration
app.use(session({
  secret: process.env.SESSION_SECRET!,
  cookie: {
    secure: process.env.NODE_ENV === 'production',
    httpOnly: true,
    sameSite: 'strict',
    maxAge: 24 * 60 * 60 * 1000, // 24 hours
  },
  resave: false,
  saveUninitialized: false,
}));
```

## A06: Vulnerable Components

### Dependency Scanning
```bash
# Check for vulnerabilities
npm audit
npm audit fix

# Use Snyk for deeper scanning
npx snyk test
npx snyk monitor

# Keep dependencies updated
npx npm-check-updates -u
```

```json
// package.json - Use exact versions or ranges
{
  "dependencies": {
    "express": "^4.18.0",  // Minor updates OK
    "lodash": "4.17.21"    // Exact version
  },
  "overrides": {
    "vulnerable-package": "^2.0.0"  // Force safe version
  }
}
```

## A07: Authentication Failures

### Secure Session Management
```typescript
import jwt from 'jsonwebtoken';

// ✅ JWT with short expiry + refresh tokens
function generateTokens(userId: string) {
  const accessToken = jwt.sign(
    { userId },
    process.env.JWT_SECRET!,
    { expiresIn: '15m' }  // Short-lived
  );
  
  const refreshToken = jwt.sign(
    { userId, type: 'refresh' },
    process.env.JWT_REFRESH_SECRET!,
    { expiresIn: '7d' }
  );
  
  return { accessToken, refreshToken };
}

// ✅ Secure password reset
async function initiatePasswordReset(email: string) {
  const user = await db.users.findByEmail(email);
  if (!user) return; // Don't reveal if email exists
  
  const token = crypto.randomBytes(32).toString('hex');
  const hashedToken = crypto.createHash('sha256').update(token).digest('hex');
  
  await db.passwordResets.create({
    userId: user.id,
    token: hashedToken,
    expiresAt: new Date(Date.now() + 60 * 60 * 1000), // 1 hour
  });
  
  await sendEmail(email, `Reset link: /reset?token=${token}`);
}
```

### Multi-Factor Authentication
```typescript
import { authenticator } from 'otplib';
import QRCode from 'qrcode';

// Setup TOTP
async function setupMFA(userId: string) {
  const secret = authenticator.generateSecret();
  const otpauth = authenticator.keyuri(userId, 'MyApp', secret);
  const qrCode = await QRCode.toDataURL(otpauth);
  
  await db.users.update(userId, { mfaSecret: encrypt(secret) });
  
  return { qrCode, secret };
}

// Verify TOTP
function verifyMFA(token: string, secret: string): boolean {
  return authenticator.verify({ token, secret });
}
```

## A08: XSS Prevention

```typescript
// ✅ React auto-escapes by default
const UserProfile = ({ user }) => (
  <div>{user.name}</div>  // Safe - auto-escaped
);

// ⚠️ Dangerous - avoid if possible
<div dangerouslySetInnerHTML={{ __html: sanitizedHtml }} />

// ✅ Sanitize HTML if needed
import DOMPurify from 'dompurify';

const sanitizedHtml = DOMPurify.sanitize(userHtml, {
  ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'a'],
  ALLOWED_ATTR: ['href'],
});

// ✅ Content Security Policy
app.use(helmet.contentSecurityPolicy({
  directives: {
    scriptSrc: ["'self'"],  // No inline scripts
    styleSrc: ["'self'", "'unsafe-inline'"],
  },
}));
```

## A09: Logging & Monitoring

```typescript
import winston from 'winston';

const logger = winston.createLogger({
  level: 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.json()
  ),
  transports: [
    new winston.transports.File({ filename: 'error.log', level: 'error' }),
    new winston.transports.File({ filename: 'combined.log' }),
  ],
});

// ✅ Log security events
function logSecurityEvent(event: string, details: object) {
  logger.warn({
    type: 'security',
    event,
    ...details,
    timestamp: new Date().toISOString(),
  });
}

// Usage
logSecurityEvent('failed_login', { email, ip: req.ip, userAgent: req.headers['user-agent'] });
logSecurityEvent('access_denied', { userId, resource, action });
logSecurityEvent('suspicious_activity', { userId, pattern: 'rapid_requests' });
```

## A10: SSRF Prevention

```typescript
import { URL } from 'url';

// ✅ Validate URLs against allowlist
const ALLOWED_HOSTS = ['api.example.com', 'cdn.example.com'];

function isAllowedUrl(urlString: string): boolean {
  try {
    const url = new URL(urlString);
    
    // Block private IPs
    const privatePatterns = [
      /^localhost$/i,
      /^127\./,
      /^10\./,
      /^172\.(1[6-9]|2[0-9]|3[01])\./,
      /^192\.168\./,
      /^0\./,
      /^169\.254\./,  // Link-local
    ];
    
    if (privatePatterns.some(p => p.test(url.hostname))) {
      return false;
    }
    
    // Check allowlist
    return ALLOWED_HOSTS.includes(url.hostname);
  } catch {
    return false;
  }
}

app.post('/api/fetch-url', async (req, res) => {
  const { url } = req.body;
  
  if (!isAllowedUrl(url)) {
    return res.status(400).json({ error: 'URL not allowed' });
  }
  
  const response = await fetch(url);
  // ...
});
```

## Security Checklist

```markdown
## Pre-Deployment Checklist

### Authentication
- [ ] Passwords hashed with bcrypt (cost ≥ 12)
- [ ] JWT tokens have short expiry
- [ ] Session cookies are httpOnly, secure, sameSite
- [ ] Rate limiting on auth endpoints

### Authorization
- [ ] All endpoints have auth checks
- [ ] RBAC implemented correctly
- [ ] No IDOR vulnerabilities

### Input/Output
- [ ] All input validated with Zod/Joi
- [ ] SQL queries parameterized
- [ ] XSS prevented (CSP, escaping)
- [ ] File uploads validated and sandboxed

### Infrastructure
- [ ] HTTPS enforced
- [ ] Security headers configured
- [ ] Dependencies audited
- [ ] Secrets in environment variables

### Monitoring
- [ ] Security events logged
- [ ] Error monitoring enabled
- [ ] Alerts configured
```

## Resources

- **OWASP Top 10**: https://owasp.org/Top10/
- **OWASP Cheat Sheets**: https://cheatsheetseries.owasp.org/
- **Node.js Security**: https://nodejs.org/en/docs/guides/security/
- **Snyk**: https://snyk.io/
