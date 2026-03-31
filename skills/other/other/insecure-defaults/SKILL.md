---
name: insecure-defaults
description: Detect fail-open configurations, hardcoded secrets, weak authentication defaults, permissive CORS, disabled security features, and other insecure-by-default patterns. Adapted from Trail of Bits. Use during security review or when auditing configuration and initialization code.
---

# Insecure Defaults Detection

Systematic detection of security misconfigurations where the default behavior is insecure. These are the bugs that ship because "it worked in development."

## Detection Categories

### 1. Fail-Open Configurations

Code that defaults to allowing access when a security check fails.

```typescript
// BAD: Fail-open -- if auth service is down, everyone gets in
async function checkAuth(token: string): Promise<boolean> {
  try {
    return await authService.verify(token)
  } catch {
    return true  // INSECURE: fails open
  }
}

// GOOD: Fail-closed -- if auth service is down, deny access
async function checkAuth(token: string): Promise<boolean> {
  try {
    return await authService.verify(token)
  } catch {
    return false  // SECURE: fails closed
  }
}
```

**Detection pattern**: Look for `catch` blocks that return truthy/permissive values in auth/authz code.

### 2. Hardcoded Secrets

```typescript
// BAD patterns -- detect ALL of these
const API_KEY = "sk-proj-abc123"
const DB_PASSWORD = "admin123"
const JWT_SECRET = "super-secret-key"
const ENCRYPTION_KEY = Buffer.from("0123456789abcdef")

// GOOD
const API_KEY = process.env.API_KEY
if (!API_KEY) throw new Error('API_KEY environment variable required')
```

**Detection patterns**:
- String literals assigned to variables named `*key*`, `*secret*`, `*password*`, `*token*`, `*credential*`
- Base64-encoded strings in source (potential embedded keys)
- `Bearer ` followed by a string literal
- AWS access keys (`AKIA...`), GitHub tokens (`ghp_...`), Stripe keys (`sk_live_...`)

### 3. Weak Authentication Defaults

```typescript
// BAD: Session without secure flags
app.use(session({
  secret: 'keyboard cat',      // Hardcoded secret
  cookie: {}                    // Missing secure, httpOnly, sameSite
}))

// GOOD
app.use(session({
  secret: process.env.SESSION_SECRET,
  cookie: {
    secure: true,               // HTTPS only
    httpOnly: true,             // No JS access
    sameSite: 'strict',         // CSRF protection
    maxAge: 3600000             // 1 hour expiry
  },
  resave: false,
  saveUninitialized: false
}))
```

### 4. Permissive CORS

```typescript
// BAD: Allow everything
app.use(cors())                          // Defaults to origin: '*'
app.use(cors({ origin: '*' }))          // Explicit wildcard
app.use(cors({ origin: true }))         // Reflect any origin

// GOOD: Explicit allowlist
app.use(cors({
  origin: ['https://app.example.com', 'https://admin.example.com'],
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
  allowedHeaders: ['Content-Type', 'Authorization']
}))
```

### 5. Disabled Security Features

```typescript
// BAD: Disabling security in code (not just config)
app.disable('x-powered-by')  // This one is actually GOOD
// But these are BAD:
process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0'  // Disable TLS verification
helmet({ contentSecurityPolicy: false })          // Disable CSP
app.use(csrf({ ignoreMethods: ['POST'] }))       // Disable CSRF for POST
```

**Detection pattern**: Look for `false`, `'0'`, `disable`, `skip`, `ignore` near security-related configs.

### 6. Debug Mode in Production

```typescript
// BAD: Debug flags that leak info
app.use(errorHandler({ dumpExceptions: true, showStack: true }))
mongoose.set('debug', true)
app.set('env', 'development')  // Hardcoded to dev

// GOOD: Environment-aware
if (process.env.NODE_ENV !== 'production') {
  mongoose.set('debug', true)
}
```

### 7. Overly Permissive File/Directory Permissions

```bash
# BAD
chmod 777 /app/config
chmod 666 /app/.env

# GOOD
chmod 600 /app/.env
chmod 700 /app/config
```

### 8. Missing Rate Limiting

```typescript
// BAD: No rate limit on auth endpoints
app.post('/api/login', loginHandler)
app.post('/api/register', registerHandler)
app.post('/api/forgot-password', forgotPasswordHandler)

// GOOD: Rate limited
const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,  // 15 minutes
  max: 5,                     // 5 attempts
  message: 'Too many attempts, try again later'
})
app.post('/api/login', authLimiter, loginHandler)
```

### 9. Insecure Deserialization

```typescript
// BAD: Deserializing untrusted input
const data = JSON.parse(userInput)        // JSON is generally safe
const obj = yaml.load(userInput)           // YAML can execute code!
const result = eval(userInput)             // Never ever

// GOOD
const obj = yaml.load(userInput, { schema: yaml.FAILSAFE_SCHEMA })
```

### 10. Missing Security Headers

Required headers for web applications:

```typescript
// Minimum security headers
app.use(helmet())  // Sets many headers, but verify:

// Or manually:
app.use((req, res, next) => {
  res.setHeader('X-Content-Type-Options', 'nosniff')
  res.setHeader('X-Frame-Options', 'DENY')
  res.setHeader('X-XSS-Protection', '0')  // Disabled intentionally, CSP replaces it
  res.setHeader('Strict-Transport-Security', 'max-age=31536000; includeSubDomains')
  res.setHeader('Content-Security-Policy', "default-src 'self'")
  res.setHeader('Referrer-Policy', 'strict-origin-when-cross-origin')
  res.setHeader('Permissions-Policy', 'camera=(), microphone=(), geolocation=()')
  next()
})
```

## Audit Checklist

```
Authentication:
[ ] No hardcoded secrets in source code
[ ] Session cookies have secure, httpOnly, sameSite flags
[ ] JWT secrets are env vars, not constants
[ ] Password hashing uses bcrypt/argon2 (not MD5/SHA1)
[ ] Default admin passwords don't exist

Authorization:
[ ] Fail-closed on error (deny by default)
[ ] No wildcard permissions in defaults
[ ] Role checks can't be bypassed by omitting headers

Network:
[ ] CORS is not wildcard in production
[ ] TLS verification is not disabled
[ ] Rate limiting on auth and sensitive endpoints
[ ] Security headers are set

Configuration:
[ ] Debug mode is off in production
[ ] Stack traces are not exposed to users
[ ] Error messages don't leak internals
[ ] File permissions are restrictive (600/700)

Data:
[ ] No sensitive data in logs
[ ] No PII in URLs/query strings
[ ] Encryption keys are not hardcoded
[ ] Database connections use TLS
```

## Rationalizations to Reject

| Rationalization | Why It's Wrong | Required Action |
|----------------|---------------|-----------------|
| "It's just for development" | Dev configs ship to prod constantly | Use env-based config switching |
| "We'll secure it before launch" | Deadline pressure skips security | Secure by default NOW |
| "The firewall protects us" | Firewalls have holes, cloud is complex | Defense in depth required |
| "It's an internal API" | Internal = one hop from external | Treat as semi-trusted |
| "Nobody knows this endpoint exists" | Security through obscurity fails | Authenticate everything |

## Integration with vibecosystem

- **security-reviewer agent**: Primary consumer -- runs this checklist on every review
- **code-reviewer agent**: Flags obvious insecure defaults during general review
- **config-validator agent**: Applies these patterns to configuration files
- **verifier agent**: Includes insecure default check in final quality gate

Inspired by [Trail of Bits](https://github.com/trailofbits/skills) insecure-defaults plugin.
