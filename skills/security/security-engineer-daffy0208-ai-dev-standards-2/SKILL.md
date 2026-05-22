---
name: Security Engineer
description: Implement security best practices across the application stack. Use when securing APIs, implementing authentication, preventing vulnerabilities, or conducting security reviews. Covers OWASP Top 10, auth patterns, input validation, encryption, and security monitoring.
version: 1.0.0
---

# Security Engineer

Security is not optional - build it in from day one.

## Core Principle

**Security is built-in, not bolted-on.**

Every feature, every endpoint, every data flow must consider security implications. Security vulnerabilities cost 10x more to fix in production than during development.

## 5 Security Pillars

### Pillar 1: Authentication & Authorization 🔐

**Authentication:** Who are you?
**Authorization:** What can you do?

#### Authentication Strategies

**JWT (JSON Web Tokens):**

- **When:** Stateless APIs, mobile apps, microservices
- **How:** Sign tokens with secret, store in httpOnly cookies or Authorization header
- **Security:** Use RS256 (not HS256), short expiry (15min access, 7d refresh)

```typescript
// Example: Next.js API with JWT
import { SignJWT, jwtVerify } from 'jose'

const secret = new TextEncoder().encode(process.env.JWT_SECRET!)

export async function createToken(userId: string) {
  return await new SignJWT({ userId })
    .setProtectedHeader({ alg: 'HS256' })
    .setExpirationTime('15m')
    .sign(secret)
}

export async function verifyToken(token: string) {
  const { payload } = await jwtVerify(token, secret)
  return payload
}
```

**Session-Based:**

- **When:** Traditional web apps, server-side rendering
- **How:** Server stores session ID in encrypted cookie
- **Security:** HttpOnly, Secure, SameSite=Strict cookies

**OAuth 2.0 / OIDC:**

- **When:** Social login, third-party integrations
- **How:** Use NextAuth.js, Passport.js, or Auth0
- **Security:** Validate state parameter, use PKCE for mobile

#### Authorization Patterns

**RBAC (Role-Based Access Control):**

```typescript
// Define roles
enum Role {
  ADMIN = 'admin',
  USER = 'user',
  GUEST = 'guest'
}

// Check permissions
function requireRole(allowedRoles: Role[]) {
  return (req, res, next) => {
    if (!allowedRoles.includes(req.user.role)) {
      return res.status(403).json({ error: 'Forbidden' })
    }
    next()
  }
}

// Usage
app.delete('/api/users/:id', requireRole([Role.ADMIN]), deleteUser)
```

**ABAC (Attribute-Based):**

- More granular: user can edit resource if they created it
- Example: User can delete post only if post.authorId === user.id

**Key Principles:**

- ✅ Always verify authentication before authorization
- ✅ Default deny (whitelist, not blacklist)
- ✅ Check permissions on server, never trust client
- ✅ Re-verify permissions before critical actions

---

### Pillar 2: Input Validation & Sanitization 🛡️

**Never trust user input** - validate, sanitize, escape everything.

#### Prevent SQL Injection

**❌ Bad (Vulnerable):**

```javascript
// DON'T DO THIS!
const query = `SELECT * FROM users WHERE email = '${userInput}'`
db.query(query) // SQL injection vulnerability!
```

**✅ Good (Parameterized Queries):**

```javascript
// Always use parameterized queries
const query = 'SELECT * FROM users WHERE email = ?'
db.query(query, [userInput]) // Safe - parameterized

// With Prisma
const user = await prisma.user.findUnique({
  where: { email: userInput } // Safe - ORM handles it
})
```

#### Prevent XSS (Cross-Site Scripting)

**❌ Bad (Vulnerable):**

```jsx
// DON'T DO THIS!
<div dangerouslySetInnerHTML={{ __html: userInput }} />
```

**✅ Good (Escaped):**

```jsx
// React automatically escapes
;<div>{userInput}</div> // Safe

// If you must render HTML, sanitize first
import DOMPurify from 'isomorphic-dompurify'
;<div dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(userInput) }} />
```

#### Input Validation with Zod

```typescript
import { z } from 'zod'

const UserSchema = z.object({
  email: z.string().email().max(255),
  password: z.string().min(8).max(100),
  age: z.number().int().min(13).max(120),
  website: z.string().url().optional()
})

// Validate
const result = UserSchema.safeParse(req.body)
if (!result.success) {
  return res.status(400).json({ errors: result.error.issues })
}

const validData = result.data // Type-safe!
```

#### File Upload Security

```typescript
import multer from 'multer'

const upload = multer({
  limits: {
    fileSize: 5 * 1024 * 1024 // 5MB max
  },
  fileFilter: (req, file, cb) => {
    // Whitelist file types
    const allowedTypes = ['image/jpeg', 'image/png', 'image/webp']
    if (!allowedTypes.includes(file.mimetype)) {
      return cb(new Error('Invalid file type'))
    }
    cb(null, true)
  }
})

// Generate random filenames (don't trust user input)
const filename = crypto.randomUUID() + path.extname(file.originalname)
```

**Key Principles:**

- ✅ Validate on server (never trust client validation)
- ✅ Use schema validation libraries (Zod, Yup, Joi)
- ✅ Whitelist allowed values, don't blacklist
- ✅ Escape output based on context (HTML, URL, JS)

---

### Pillar 3: Secure Configuration 🔧

#### Environment Variables

**Never commit secrets:**

```bash
# .env (add to .gitignore!)
DATABASE_URL="postgresql://user:pass@localhost:5432/db"
JWT_SECRET="generate-with-openssl-rand-base64-32"
OPENAI_API_KEY="sk-..."
```

**Access in code:**

```typescript
// Validate env vars on startup
if (!process.env.JWT_SECRET) {
  throw new Error('JWT_SECRET is required')
}

const config = {
  jwtSecret: process.env.JWT_SECRET,
  databaseUrl: process.env.DATABASE_URL
}
```

**Secret Management (Production):**

- AWS Secrets Manager
- Vercel Environment Variables
- HashiCorp Vault
- Doppler

#### Security Headers

```typescript
// Next.js middleware
export function middleware(request: NextRequest) {
  const response = NextResponse.next()

  // Prevent clickjacking
  response.headers.set('X-Frame-Options', 'DENY')

  // Prevent MIME sniffing
  response.headers.set('X-Content-Type-Options', 'nosniff')

  // XSS Protection
  response.headers.set('X-XSS-Protection', '1; mode=block')

  // Content Security Policy
  response.headers.set(
    'Content-Security-Policy',
    "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'"
  )

  // HTTPS only
  response.headers.set('Strict-Transport-Security', 'max-age=31536000; includeSubDomains')

  return response
}
```

#### CORS Configuration

```typescript
// Configure CORS properly
app.use(
  cors({
    origin:
      process.env.NODE_ENV === 'production' ? 'https://yourdomain.com' : 'http://localhost:3000',
    credentials: true, // Allow cookies
    methods: ['GET', 'POST', 'PUT', 'DELETE'],
    allowedHeaders: ['Content-Type', 'Authorization']
  })
)
```

**Key Principles:**

- ✅ Use environment variables for all secrets
- ✅ Different secrets per environment (dev, staging, prod)
- ✅ Rotate secrets regularly
- ✅ Set security headers on all responses
- ✅ Configure CORS restrictively

---

### Pillar 4: Data Protection 🔒

#### Password Hashing

**❌ Never store passwords in plain text or use MD5/SHA1!**

**✅ Use bcrypt or argon2:**

```typescript
import bcrypt from 'bcrypt'

// Hash password (on signup)
const saltRounds = 12
const hashedPassword = await bcrypt.hash(password, saltRounds)
await db.user.create({
  email,
  password: hashedPassword // Store hash, never plain text
})

// Verify password (on login)
const user = await db.user.findUnique({ where: { email } })
const isValid = await bcrypt.compare(password, user.password)
if (!isValid) {
  throw new Error('Invalid credentials')
}
```

#### Encryption at Rest

**Sensitive data should be encrypted:**

```typescript
import crypto from 'crypto'

const algorithm = 'aes-256-gcm'
const key = Buffer.from(process.env.ENCRYPTION_KEY!, 'hex')

function encrypt(text: string) {
  const iv = crypto.randomBytes(16)
  const cipher = crypto.createCipheriv(algorithm, key, iv)
  const encrypted = Buffer.concat([cipher.update(text, 'utf8'), cipher.final()])
  const authTag = cipher.getAuthTag()
  return {
    iv: iv.toString('hex'),
    encryptedData: encrypted.toString('hex'),
    authTag: authTag.toString('hex')
  }
}

function decrypt(encrypted: any) {
  const decipher = crypto.createDecipheriv(algorithm, key, Buffer.from(encrypted.iv, 'hex'))
  decipher.setAuthTag(Buffer.from(encrypted.authTag, 'hex'))
  return decipher.update(encrypted.encryptedData, 'hex', 'utf8') + decipher.final('utf8')
}

// Encrypt sensitive fields
const ssn = encrypt(user.ssn)
await db.user.update({ where: { id }, data: { ssnEncrypted: JSON.stringify(ssn) } })
```

#### Encryption in Transit

**Always use HTTPS:**

- Development: `mkcert` for local HTTPS
- Production: Let's Encrypt, Cloudflare, Vercel (auto HTTPS)

**Verify external API certificates:**

```typescript
// Don't disable SSL verification in production!
fetch(url, {
  // DON'T: agent: new https.Agent({ rejectUnauthorized: false })
})
```

**Key Principles:**

- ✅ Hash passwords with bcrypt (12+ rounds) or argon2
- ✅ Encrypt PII (SSN, credit cards, health data)
- ✅ Use HTTPS everywhere (enforce with HSTS header)
- ✅ Encrypt database backups

---

### Pillar 5: Monitoring & Response 📊

#### Rate Limiting

**Prevent brute force and DDoS:**

```typescript
import rateLimit from 'express-rate-limit'

// Global rate limit
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // 100 requests per window
  message: 'Too many requests from this IP'
})
app.use(limiter)

// Stricter limit for auth endpoints
const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 5, // Only 5 login attempts per 15min
  skipSuccessfulRequests: true
})
app.post('/api/auth/login', authLimiter, loginHandler)
```

#### Audit Logging

**Log all security-relevant events:**

```typescript
async function auditLog(event: {
  userId?: string
  action: string
  resource: string
  ip: string
  userAgent: string
  success: boolean
  metadata?: any
}) {
  await db.auditLog.create({
    data: {
      ...event,
      timestamp: new Date()
    }
  })
}

// Usage
await auditLog({
  userId: user.id,
  action: 'LOGIN',
  resource: 'auth',
  ip: req.ip,
  userAgent: req.headers['user-agent'],
  success: true
})
```

#### Error Handling

**Don't leak sensitive info in errors:**

**❌ Bad:**

```typescript
// Exposes database structure!
catch (error) {
  res.status(500).json({ error: error.message })
}
```

**✅ Good:**

```typescript
catch (error) {
  // Log full error server-side
  console.error('Error:', error)

  // Send generic message to client
  res.status(500).json({
    error: 'Internal server error',
    requestId: generateRequestId() // For support
  })
}
```

#### Security Monitoring

**Tools to integrate:**

- **Sentry:** Error tracking, security alerts
- **Datadog:** APM, anomaly detection
- **CloudWatch:** AWS infrastructure monitoring
- **OWASP ZAP:** Automated security scans

**Key Principles:**

- ✅ Rate limit all public endpoints
- ✅ Log authentication attempts, authorization failures
- ✅ Never expose sensitive data in errors
- ✅ Set up alerts for suspicious patterns
- ✅ Regular security audits

---

## OWASP Top 10 Quick Reference

| #   | Vulnerability                 | Prevention                                    |
| --- | ----------------------------- | --------------------------------------------- |
| 1   | Broken Access Control         | Verify permissions server-side, default deny  |
| 2   | Cryptographic Failures        | Use TLS, hash passwords (bcrypt), encrypt PII |
| 3   | Injection                     | Parameterized queries, input validation       |
| 4   | Insecure Design               | Threat modeling, security requirements        |
| 5   | Security Misconfiguration     | Secure defaults, remove unused features       |
| 6   | Vulnerable Components         | Keep dependencies updated, use Dependabot     |
| 7   | Auth & Session Issues         | Strong passwords, MFA, secure session mgmt    |
| 8   | Software & Data Integrity     | Verify dependencies, sign releases            |
| 9   | Logging & Monitoring Failures | Log security events, set up alerts            |
| 10  | SSRF                          | Validate URLs, whitelist allowed domains      |

---

## Security Checklist (Pre-Deployment)

### Authentication

- [ ] Passwords hashed with bcrypt (12+ rounds)
- [ ] JWT tokens use RS256, short expiry
- [ ] Session cookies are HttpOnly, Secure, SameSite
- [ ] Rate limiting on login endpoints (5 attempts/15min)
- [ ] Password reset uses secure tokens (expires 1 hour)

### Authorization

- [ ] All routes check authentication
- [ ] Permissions verified server-side
- [ ] Default deny (whitelist approach)
- [ ] No sensitive operations allowed without re-authentication

### Input Validation

- [ ] All user input validated with schema (Zod)
- [ ] SQL queries use parameterized queries/ORM
- [ ] File uploads whitelist types and size limits
- [ ] Output escaped based on context

### Configuration

- [ ] No secrets in code or version control
- [ ] Environment variables for all config
- [ ] Security headers set (CSP, HSTS, X-Frame-Options)
- [ ] CORS configured restrictively
- [ ] HTTPS enforced in production

### Data Protection

- [ ] PII encrypted at rest
- [ ] TLS/HTTPS for all connections
- [ ] Database backups encrypted
- [ ] Secure secret management (Vault, AWS Secrets)

### Monitoring

- [ ] Audit logging for security events
- [ ] Error tracking configured (Sentry)
- [ ] Rate limiting on all public endpoints
- [ ] Alerts for failed login attempts, 5xx errors

### Dependencies

- [ ] All dependencies up to date
- [ ] Dependabot enabled
- [ ] No known vulnerabilities (run `npm audit`)
- [ ] Minimal dependencies (remove unused)

---

## Common Security Mistakes

### Mistake 1: Client-Side Authorization

**❌ Wrong:**

```jsx
// Hiding UI doesn't prevent access!
{
  user.role === 'admin' && <DeleteButton />
}
```

**✅ Right:**

```jsx
// Always verify on server
app.delete('/api/users/:id', requireAdmin, deleteUser)
```

---

### Mistake 2: Trusting Client Data

**❌ Wrong:**

```typescript
// User can manipulate userId in request!
const userId = req.body.userId
await db.order.create({ data: { userId } })
```

**✅ Right:**

```typescript
// Get userId from authenticated session
const userId = req.user.id // From JWT/session
await db.order.create({ data: { userId } })
```

---

### Mistake 3: Weak Password Requirements

**❌ Wrong:**

```typescript
if (password.length < 6) throw new Error('Too short')
```

**✅ Right:**

```typescript
const passwordSchema = z
  .string()
  .min(8, 'At least 8 characters')
  .regex(/[A-Z]/, 'Needs uppercase')
  .regex(/[a-z]/, 'Needs lowercase')
  .regex(/[0-9]/, 'Needs number')
```

---

### Mistake 4: Insecure Direct Object References

**❌ Wrong:**

```typescript
// User can access any document by changing ID!
const doc = await db.document.findUnique({ where: { id: req.params.id } })
return res.json(doc)
```

**✅ Right:**

```typescript
// Verify ownership
const doc = await db.document.findFirst({
  where: {
    id: req.params.id,
    userId: req.user.id // Ensure user owns this document
  }
})
if (!doc) return res.status(404).json({ error: 'Not found' })
return res.json(doc)
```

---

## Framework-Specific Guidance

### Next.js Security

```typescript
// middleware.ts - Protect routes
export function middleware(request: NextRequest) {
  const token = request.cookies.get('token')

  // Redirect to login if no token
  if (!token && request.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', request.url))
  }

  return NextResponse.next()
}

export const config = {
  matcher: ['/dashboard/:path*', '/api/private/:path*']
}
```

### Express Security

```typescript
import helmet from 'helmet'
import mongoSanitize from 'express-mongo-sanitize'

app.use(helmet()) // Security headers
app.use(express.json({ limit: '10mb' })) // Prevent large payloads
app.use(mongoSanitize()) // Prevent NoSQL injection
```

### FastAPI Security

```python
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer

security = HTTPBearer()

async def get_current_user(token: str = Depends(security)):
    try:
        payload = verify_token(token.credentials)
        return payload['user_id']
    except:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/protected")
async def protected_route(user_id: str = Depends(get_current_user)):
    return {"user_id": user_id}
```

---

## Security Testing

### Automated Tools

- **OWASP ZAP:** Web vulnerability scanner
- **Snyk:** Dependency vulnerability scanning
- **npm audit:** Check for known vulnerabilities
- **Lighthouse:** Security audit in Chrome DevTools

### Manual Testing

1. **Try SQL injection:** `' OR '1'='1`
2. **Try XSS:** `<script>alert('XSS')</script>`
3. **Try CSRF:** Submit form from different origin
4. **Try path traversal:** `../../etc/passwd`
5. **Try auth bypass:** Access admin routes without token

---

## When to Use This Skill

Use security-engineer skill when:

- ✅ Implementing authentication/authorization
- ✅ Building API endpoints
- ✅ Handling sensitive data (PII, payments, health)
- ✅ Reviewing code for vulnerabilities
- ✅ Deploying to production
- ✅ Conducting security audits

---

## Related Resources

**Skills:**

- `api-designer` - API design patterns (pairs with security)
- `testing-strategist` - Security testing strategies
- `deployment-advisor` - Production security configuration

**Patterns:**

- `/STANDARDS/architecture-patterns/authentication-patterns.md`
- `/STANDARDS/best-practices/security-best-practices.md`

**External:**

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/)
- [Security Headers](https://securityheaders.com/)

---

**Security is everyone's responsibility. Build it in from day one.** 🔒
