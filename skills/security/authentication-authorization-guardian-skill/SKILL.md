---
name: authentication-authorization-guardian
description: Offensive authentication and authorization security enforcement. Triggered when implementing login/signup, reviewing JWT token handling, debugging session issues, implementing RBAC, or preparing auth for production. Scans for token exposure, weak password policies, session hijacking vulnerabilities, CSRF risks, and privilege escalation paths. Produces auto-scan reports with security hardening recommendations.
---

# Authentication & Authorization Guardian

**Mission:** Prevent authentication and authorization vulnerabilities through proactive security scanning and best practice enforcement. This skill operates in **offensive mode** - finding potential exploits and privilege escalation paths before attackers do.

## Activation Triggers

- Implementing login/signup endpoints
- "Users can't stay logged in"
- JWT token configuration review
- "How do I protect admin routes?"
- Session persistence issues
- Password reset functionality
- Role-based access control (RBAC) implementation
- "Token expired" errors
- Production auth deployment prep
- OAuth/SSO integration

## Tech Stack Awareness

This skill is specialized for **PDFLab's auth stack**:

- **JWT tokens** (access + refresh)
- **Bcrypt** password hashing
- **Express middleware** for route protection
- **localStorage** for token persistence (frontend)
- **AuthContext** (React Context API)
- **Role-based access:** User, Admin
- **Plan-based limits:** Free, Starter, Pro, Enterprise

## Scan Methodology

### 1. Initial Context Gathering

**Ask if not provided:**
- "Show me your JWT middleware"
- "How are passwords hashed?"
- "Where are tokens stored?" (localStorage, cookies, memory)
- "What roles/permissions exist?"
- "Is there a refresh token mechanism?"
- "How is session restored on page reload?"

### 2. Critical Security Scan

Execute ALL checks in this section. Each is based on real security breaches.

#### 🔴 CRITICAL: JWT Token Security

**Historical Vulnerability:** JWT secret leaked via .env in git, attackers forged admin tokens

**Scan for:**
- [ ] Strong JWT secret (32+ random characters)
- [ ] HS256 or RS256 algorithm (not 'none')
- [ ] Token expiration set (7d max for access tokens)
- [ ] Refresh token rotation
- [ ] Secret not in git (.env in .gitignore)
- [ ] Signature verification on every request
- [ ] Token payload doesn't contain sensitive data (passwords, credit cards)

**Red flags:**
```typescript
// ❌ Weak secret
const JWT_SECRET = 'secret123'  // Error! Easily guessed

// ❌ No expiration
jwt.sign({ userId }, JWT_SECRET)  // Token valid forever!

// ❌ Algorithm 'none' (no signature)
jwt.sign({ userId }, '', { algorithm: 'none' })  // Anyone can forge

// ❌ Sensitive data in payload
jwt.sign({ userId, password: 'hunter2' }, JWT_SECRET)  // Error! Payload is visible

// ❌ No signature verification
const decoded = jwt.decode(token)  // Error! Doesn't verify signature
```

**Hardening:**
```typescript
// ✅ Strong random secret (generate once, store in .env)
// Generate: openssl rand -base64 32
// .env
JWT_SECRET=Kx7jN9mP2qR4sT6vW8yZ0aB3cD5eF7gH9iJ1kL3mN5oP7qR9sT1uV3wX5yZ7aB9

// ✅ Proper token generation with expiration
import jwt from 'jsonwebtoken'

interface TokenPayload {
  userId: string
  email: string
  plan: string
  role: 'user' | 'admin'
}

export function generateAccessToken(user: User): string {
  const payload: TokenPayload = {
    userId: user.id,
    email: user.email,
    plan: user.plan,
    role: user.role
  }

  return jwt.sign(payload, process.env.JWT_SECRET!, {
    expiresIn: '7d',  // Access token valid for 7 days
    algorithm: 'HS256'
  })
}

export function generateRefreshToken(user: User): string {
  return jwt.sign(
    { userId: user.id },
    process.env.JWT_REFRESH_SECRET!,  // Different secret
    { expiresIn: '30d' }  // Refresh token valid for 30 days
  )
}

// ✅ Signature verification middleware
export const authMiddleware = async (
  req: Request,
  res: Response,
  next: NextFunction
) => {
  try {
    // 1. Extract token
    const authHeader = req.headers.authorization
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      return res.status(401).json({ error: 'No token provided' })
    }

    const token = authHeader.substring(7)

    // 2. Verify signature and expiration
    const decoded = jwt.verify(token, process.env.JWT_SECRET!) as TokenPayload

    // 3. Load user from database (verify not deleted/banned)
    const user = await User.findByPk(decoded.userId)
    if (!user) {
      return res.status(401).json({ error: 'User not found' })
    }

    // 4. Attach to request
    req.user = user
    next()
  } catch (error) {
    if (error.name === 'TokenExpiredError') {
      return res.status(401).json({ error: 'Token expired' })
    }
    if (error.name === 'JsonWebTokenError') {
      return res.status(401).json({ error: 'Invalid token' })
    }
    return res.status(500).json({ error: 'Authentication failed' })
  }
}

// ✅ Refresh token endpoint
app.post('/api/auth/refresh', async (req, res) => {
  try {
    const { refreshToken } = req.body

    // Verify refresh token
    const decoded = jwt.verify(refreshToken, process.env.JWT_REFRESH_SECRET!) as { userId: string }

    const user = await User.findByPk(decoded.userId)
    if (!user) {
      return res.status(401).json({ error: 'User not found' })
    }

    // Generate new access token
    const newAccessToken = generateAccessToken(user)

    // Optionally rotate refresh token
    const newRefreshToken = generateRefreshToken(user)

    res.json({
      accessToken: newAccessToken,
      refreshToken: newRefreshToken
    })
  } catch (error) {
    res.status(401).json({ error: 'Invalid refresh token' })
  }
})
```

**Token expiration best practices:**
- Access token: 15min - 7 days (PDFLab uses 7d for UX)
- Refresh token: 30-90 days
- Sensitive operations: Require fresh login (<5 min old token)

#### 🔴 CRITICAL: Password Security

**Historical Vulnerability:** Plain text passwords in database, breach exposes all accounts

**Scan for:**
- [ ] Bcrypt hashing (not MD5, SHA1, or plain text)
- [ ] Salt rounds ≥ 10 (12 recommended)
- [ ] Password complexity requirements (8+ chars, mix of types)
- [ ] Password reuse prevention (check against history)
- [ ] Timing-safe password comparison
- [ ] Rate limiting on login endpoint (brute force prevention)
- [ ] Account lockout after N failed attempts

**Red flags:**
```typescript
// ❌ Plain text password storage
await User.create({ email, password })  // Error! Plain text in DB

// ❌ Weak hashing
const hash = crypto.createHash('md5').update(password).digest('hex')  // Error! MD5 is broken

// ❌ No salt (rainbow table attacks)
const hash = bcrypt.hashSync(password, 1)  // Error! Salt rounds = 1 (too low)

// ❌ Timing attack vulnerability
if (user.password === password) {  // Error! Leaks info via timing
  // login
}

// ❌ No rate limiting
app.post('/login', loginHandler)  // Can brute force 1000s of attempts
```

**Hardening:**
```typescript
// ✅ Bcrypt with proper salt rounds
import bcrypt from 'bcrypt'

const SALT_ROUNDS = 12  // Good balance of security and performance

export async function hashPassword(password: string): Promise<string> {
  return bcrypt.hash(password, SALT_ROUNDS)
}

export async function verifyPassword(password: string, hash: string): Promise<boolean> {
  return bcrypt.compare(password, hash)  // Timing-safe comparison
}

// ✅ Password complexity validation
export function validatePassword(password: string): { valid: boolean; errors: string[] } {
  const errors: string[] = []

  if (password.length < 8) {
    errors.push('Password must be at least 8 characters')
  }
  if (!/[a-z]/.test(password)) {
    errors.push('Password must contain lowercase letter')
  }
  if (!/[A-Z]/.test(password)) {
    errors.push('Password must contain uppercase letter')
  }
  if (!/[0-9]/.test(password)) {
    errors.push('Password must contain number')
  }
  if (!/[!@#$%^&*]/.test(password)) {
    errors.push('Password must contain special character (!@#$%^&*)')
  }

  return { valid: errors.length === 0, errors }
}

// ✅ Signup with password validation
app.post('/api/auth/register', async (req, res) => {
  const { email, password, name } = req.body

  // Validate password
  const validation = validatePassword(password)
  if (!validation.valid) {
    return res.status(400).json({ errors: validation.errors })
  }

  // Check if user exists
  const existingUser = await User.findOne({ where: { email } })
  if (existingUser) {
    return res.status(400).json({ error: 'Email already registered' })
  }

  // Hash password
  const passwordHash = await hashPassword(password)

  // Create user
  const user = await User.create({
    email,
    password_hash: passwordHash,
    name
  })

  res.status(201).json({ message: 'User created successfully' })
})

// ✅ Login with timing-safe comparison
app.post('/api/auth/login', async (req, res) => {
  const { email, password } = req.body

  // Find user
  const user = await User.findOne({ where: { email } })
  if (!user) {
    // Use bcrypt.compare even if user not found (prevent timing attack)
    await bcrypt.compare(password, '$2b$12$dummyhashtopreventtimingattack')
    return res.status(401).json({ error: 'Invalid credentials' })
  }

  // Verify password (timing-safe)
  const isValid = await verifyPassword(password, user.password_hash)
  if (!isValid) {
    return res.status(401).json({ error: 'Invalid credentials' })
  }

  // Generate tokens
  const accessToken = generateAccessToken(user)
  const refreshToken = generateRefreshToken(user)

  res.json({ accessToken, refreshToken, user: user.toJSON() })
})

// ✅ Rate limiting on login
import rateLimit from 'express-rate-limit'

const loginLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,  // 15 minutes
  max: 5,  // 5 login attempts per 15 min
  message: 'Too many login attempts, please try again later',
  skipSuccessfulRequests: true  // Only count failed attempts
})

app.post('/api/auth/login', loginLimiter, loginHandler)

// ✅ Account lockout after failed attempts
// Add to User model
interface User {
  failed_login_attempts: number
  locked_until: Date | null
}

async function incrementFailedAttempts(user: User): Promise<void> {
  user.failed_login_attempts += 1

  // Lock account after 5 failed attempts (30 min lockout)
  if (user.failed_login_attempts >= 5) {
    user.locked_until = new Date(Date.now() + 30 * 60 * 1000)
  }

  await user.save()
}

async function resetFailedAttempts(user: User): Promise<void> {
  user.failed_login_attempts = 0
  user.locked_until = null
  await user.save()
}

// In login handler:
if (user.locked_until && user.locked_until > new Date()) {
  const minutesLeft = Math.ceil((user.locked_until.getTime() - Date.now()) / 60000)
  return res.status(429).json({
    error: `Account locked. Try again in ${minutesLeft} minutes.`
  })
}
```

#### 🔴 CRITICAL: Authorization & RBAC

**Historical Vulnerability:** Regular users accessing admin panel via URL guessing

**Scan for:**
- [ ] Role-based middleware (admin vs user)
- [ ] Resource ownership verification (users can only access their own data)
- [ ] Plan-based feature gates (Free vs Pro features)
- [ ] Privilege escalation prevention (users can't promote themselves)
- [ ] Horizontal privilege escalation (user A can't access user B's data)

**Red flags:**
```typescript
// ❌ No role check (anyone can delete users)
app.delete('/api/admin/users/:id', authMiddleware, deleteUser)

// ❌ No ownership check (can delete other users' jobs)
app.delete('/api/jobs/:id', authMiddleware, async (req, res) => {
  await ConversionJob.destroy({ where: { id: req.params.id } })
  // Didn't check if job belongs to req.user!
})

// ❌ Client-side role check only
// Frontend: if (user.role === 'admin') { showAdminPanel() }
// Backend has no check → can call admin API directly

// ❌ Users can change their own role
app.patch('/api/profile', authMiddleware, async (req, res) => {
  const { role } = req.body  // Error! User sets role = 'admin'
  await req.user.update({ role })
})
```

**Hardening:**
```typescript
// ✅ Role-based middleware
export const requireAdmin = (req: Request, res: Response, next: NextFunction) => {
  if (!req.user || req.user.role !== 'admin') {
    return res.status(403).json({ error: 'Admin access required' })
  }
  next()
}

// ✅ Plan-based middleware
export const requirePlan = (...allowedPlans: UserPlan[]) => {
  return (req: Request, res: Response, next: NextFunction) => {
    if (!req.user || !allowedPlans.includes(req.user.plan)) {
      return res.status(403).json({
        error: 'Upgrade required',
        currentPlan: req.user?.plan,
        requiredPlans: allowedPlans
      })
    }
    next()
  }
}

// Usage
app.delete('/api/admin/users/:id', authMiddleware, requireAdmin, deleteUser)

app.post('/api/batch/upload',
  authMiddleware,
  requirePlan(UserPlan.PRO, UserPlan.ENTERPRISE),
  uploadBatchFiles
)

// ✅ Ownership verification
app.delete('/api/jobs/:id', authMiddleware, async (req, res) => {
  const job = await ConversionJob.findByPk(req.params.id)

  if (!job) {
    return res.status(404).json({ error: 'Job not found' })
  }

  // Verify ownership (or admin override)
  if (job.user_id !== req.user.id && req.user.role !== 'admin') {
    return res.status(403).json({ error: 'Not your job' })
  }

  await job.destroy()
  res.json({ message: 'Job deleted' })
})

// ✅ Protected fields (users can't change role/plan)
const PROTECTED_FIELDS = ['role', 'plan', 'conversions_limit', 'subscription_status']

app.patch('/api/profile', authMiddleware, async (req, res) => {
  const updates = req.body

  // Check for protected fields
  for (const field of PROTECTED_FIELDS) {
    if (field in updates) {
      return res.status(403).json({ error: `Cannot modify ${field}` })
    }
  }

  // Allow name, email updates only
  await req.user.update(updates)
  res.json({ user: req.user.toJSON() })
})

// ✅ Reusable ownership check helper
export async function verifyOwnership<T extends { user_id: string }>(
  model: any,
  id: string,
  userId: string,
  userRole: string
): Promise<T | null> {
  const resource = await model.findByPk(id)

  if (!resource) {
    return null
  }

  // Admin bypass
  if (userRole === 'admin') {
    return resource
  }

  // Ownership check
  if (resource.user_id !== userId) {
    throw new Error('Forbidden: Not your resource')
  }

  return resource
}

// Usage
const job = await verifyOwnership<ConversionJob>(
  ConversionJob,
  req.params.id,
  req.user.id,
  req.user.role
)
```

#### 🟡 HIGH: Frontend Token Storage

**Historical Vulnerability:** XSS attack steals JWT from localStorage

**Scan for:**
- [ ] Token storage location (localStorage vs httpOnly cookie)
- [ ] XSS prevention (Content Security Policy)
- [ ] Token exposed in URL (query params or hash)
- [ ] Token logged to console/analytics
- [ ] Session restoration on page reload

**Red flags:**
```typescript
// ❌ Token in URL (shows in browser history, server logs)
window.location.href = `/dashboard?token=${token}`

// ❌ Token logged
console.log('Login successful:', { user, token })  // Error! Visible in console

// ❌ No CSP headers (XSS can steal from localStorage)
// No Content-Security-Policy header

// ❌ Token in localStorage without httpOnly protection
localStorage.setItem('token', token)  // Accessible to XSS
```

**Hardening:**
```typescript
// ✅ httpOnly cookie (best security, not accessible to JavaScript)
// Backend sets cookie
app.post('/api/auth/login', async (req, res) => {
  const { accessToken, refreshToken } = await login(req.body)

  // Set httpOnly cookie (XSS can't access)
  res.cookie('accessToken', accessToken, {
    httpOnly: true,  // Not accessible to JavaScript
    secure: true,    // HTTPS only
    sameSite: 'strict',  // CSRF protection
    maxAge: 7 * 24 * 60 * 60 * 1000  // 7 days
  })

  res.json({ message: 'Logged in successfully' })
})

// Middleware reads from cookie
export const authMiddleware = (req, res, next) => {
  const token = req.cookies.accessToken  // From cookie, not header
  // ... verify token
}

// ✅ Content Security Policy headers
import helmet from 'helmet'

app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      scriptSrc: ["'self'", "'unsafe-inline'"],  // Minimize unsafe-inline
      styleSrc: ["'self'", "'unsafe-inline'"],
      imgSrc: ["'self'", 'data:', 'https:'],
      connectSrc: ["'self'", 'https://api.cloudconvert.com']
    }
  }
}))

// ✅ If using localStorage, sanitize all user input (XSS prevention)
// Frontend
import DOMPurify from 'dompurify'

function displayUserName(name: string) {
  const clean = DOMPurify.sanitize(name)
  return <div>{clean}</div>
}

// ✅ Session restoration without exposing token
// Frontend: AuthContext.tsx
export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Restore session on mount (backend reads httpOnly cookie)
    fetch('/api/auth/profile', { credentials: 'include' })
      .then(res => res.json())
      .then(data => setUser(data.user))
      .catch(() => setUser(null))
      .finally(() => setLoading(false))
  }, [])

  return (
    <AuthContext.Provider value={{ user, loading }}>
      {children}
    </AuthContext.Provider>
  )
}
```

**Storage comparison:**
| Method | XSS Risk | CSRF Risk | Best For |
|--------|----------|-----------|----------|
| localStorage | High (accessible to JS) | Low | SPAs with good XSS protection |
| httpOnly cookie | Low (not accessible to JS) | Medium (need sameSite) | Traditional web apps |
| Memory only | Low (lost on refresh) | Low | High security, poor UX |

**PDFLab uses localStorage** - ensure XSS protection via:
- Input sanitization (DOMPurify)
- CSP headers
- Avoid `dangerouslySetInnerHTML`

#### 🟠 MEDIUM: Password Reset Security

**Historical Vulnerability:** Password reset tokens valid forever, guessable tokens

**Scan for:**
- [ ] Reset token is random (UUID or crypto.randomBytes)
- [ ] Token expiration (15-60 minutes)
- [ ] Token single-use (invalidated after reset)
- [ ] Rate limiting on reset requests
- [ ] Email verification before sending reset link

**Red flags:**
```typescript
// ❌ Guessable token
const resetToken = user.id  // Error! Predictable

// ❌ Token never expires
await PasswordReset.create({ user_id, token })  // Valid forever

// ❌ Token reusable
// Can use same reset link multiple times

// ❌ No rate limiting
app.post('/forgot-password', sendResetEmail)  // Can spam emails
```

**Hardening:**
```typescript
// ✅ Secure password reset flow
import crypto from 'crypto'

// 1. Request reset
app.post('/api/auth/forgot-password', async (req, res) => {
  const { email } = req.body

  const user = await User.findOne({ where: { email } })
  if (!user) {
    // Don't reveal if email exists
    return res.json({ message: 'If email exists, reset link sent' })
  }

  // Generate secure random token
  const resetToken = crypto.randomBytes(32).toString('hex')

  // Hash token before storing (in case DB leaks)
  const hashedToken = crypto
    .createHash('sha256')
    .update(resetToken)
    .digest('hex')

  // Store with 15-minute expiration
  await PasswordReset.create({
    user_id: user.id,
    token: hashedToken,
    expires_at: new Date(Date.now() + 15 * 60 * 1000)
  })

  // Send email with reset link
  const resetUrl = `https://pdflab.pro/reset-password?token=${resetToken}`
  await sendEmail(user.email, 'Password Reset', `Reset your password: ${resetUrl}`)

  res.json({ message: 'If email exists, reset link sent' })
})

// 2. Verify token and reset password
app.post('/api/auth/reset-password', async (req, res) => {
  const { token, newPassword } = req.body

  // Hash token to match DB
  const hashedToken = crypto
    .createHash('sha256')
    .update(token)
    .digest('hex')

  // Find reset record
  const reset = await PasswordReset.findOne({
    where: {
      token: hashedToken,
      expires_at: { [Op.gt]: new Date() }  // Not expired
    }
  })

  if (!reset) {
    return res.status(400).json({ error: 'Invalid or expired token' })
  }

  // Validate new password
  const validation = validatePassword(newPassword)
  if (!validation.valid) {
    return res.status(400).json({ errors: validation.errors })
  }

  // Update password
  const user = await User.findByPk(reset.user_id)
  user.password_hash = await hashPassword(newPassword)
  await user.save()

  // Invalidate token (single-use)
  await reset.destroy()

  res.json({ message: 'Password reset successful' })
})

// ✅ Rate limiting
const resetLimiter = rateLimit({
  windowMs: 60 * 60 * 1000,  // 1 hour
  max: 3,  // 3 reset requests per hour
  message: 'Too many reset requests, try again later'
})

app.post('/api/auth/forgot-password', resetLimiter, forgotPasswordHandler)
```

### 3. Production Readiness Checklist

Generate this checklist in the auto-scan report:

```
AUTHENTICATION SECURITY SCORE: X/10

✅ JWT secret: 32+ random characters (not in git)
✅ Password hashing: Bcrypt with 12 salt rounds
✅ Token expiration: 7 days (access), 30 days (refresh)
✅ Role-based access control (admin vs user)
✅ Ownership verification on protected resources
✅ Rate limiting: Login (5/15min), Password reset (3/hour)
⚠️  Token storage: localStorage (XSS risk, add CSP headers)
⚠️  Missing: Account lockout after failed attempts
❌ Critical: Admin routes not protected with requireAdmin
❌ Security: Users can modify their own plan field

RISK LEVEL: [LOW/MEDIUM/HIGH/CRITICAL]
BLOCKERS: X critical issues must be resolved
OPTIMIZATIONS: Y security wins available
```

## Output Format: Auto-Scan Report

```
═══════════════════════════════════════════════
🛡️ AUTHENTICATION & AUTHORIZATION GUARDIAN - SCAN RESULTS
═══════════════════════════════════════════════

📊 SCAN SCOPE
• Auth method: JWT (access + refresh)
• Password hashing: Bcrypt (12 rounds)
• Token storage: localStorage (frontend)
• Roles: User, Admin
• Plans: Free, Starter, Pro, Enterprise

🚨 CRITICAL FINDINGS: [count]

⚠️  HIGH PRIORITY: [count]

💡 OPTIMIZATIONS: [count]

🔐 AUTHENTICATION AUDIT:
✅ JWT signature verification: HS256 algorithm
✅ Password complexity: 8+ chars, mixed case, numbers, special
✅ Timing-safe comparison: bcrypt.compare()
❌ Token expiration: No expiration set (valid forever)
⚠️  Rate limiting: Login endpoint limited (5/15min)

🔒 AUTHORIZATION AUDIT:
✅ Role-based middleware: requireAdmin implemented
✅ Ownership checks: Jobs, subscriptions verified
❌ Plan gating: Batch feature not protected
⚠️  Protected fields: Users can modify plan field

═══════════════════════════════════════════════
FINAL VERDICT
═══════════════════════════════════════════════
Production Ready: [YES/NO/BLOCKED]
Risk Level: [LOW/MEDIUM/HIGH/CRITICAL]
Estimated Fix Time: [X hours]

NEXT ACTIONS:
1. [Most critical fix]
2. [Second priority]
3. [Optional optimization]

═══════════════════════════════════════════════
```

## Key Principles

1. **Defense in depth:** JWT + password hash + rate limiting + RBAC
2. **Zero trust:** Verify every request, never trust client
3. **Principle of least privilege:** Users get minimum necessary permissions
4. **Secure defaults:** Deny access unless explicitly allowed
5. **Audit trails:** Log all auth events (login, failed attempts, role changes)
6. **Password security:** Bcrypt ≥ 10 rounds, complexity requirements

## Quick Reference: Common Fixes

```bash
# Generate strong JWT secret
openssl rand -base64 32

# Test JWT token
# Install: npm install -g jwt-cli
jwt decode YOUR_TOKEN_HERE

# Check bcrypt rounds (from hash)
# Hash format: $2b$12$... (12 = salt rounds)

# Test login rate limiting
# Attempt 6 logins in < 15 min, should block 6th
```

## PDFLab-Specific Patterns

**backend/src/middleware/auth.middleware.ts:**
- Export `authMiddleware`, `requireAdmin`, `requirePlan`
- Verify JWT signature with jwt.verify()
- Load user from database on each request
- Handle TokenExpiredError gracefully

**contexts/AuthContext.tsx:**
- Store token in localStorage (add CSP headers)
- Restore session on mount via GET /api/auth/profile
- Provide login(), logout(), checkAuth() methods
- Handle token expiration (redirect to login)

**backend/src/models/User.ts:**
- Store password_hash (never plain text)
- Add failed_login_attempts, locked_until fields
- Implement getMaxFileSize(), getMaxBatchSize() for plan gating
- Add role enum: 'user' | 'admin'

**Admin Routes Protection:**
```typescript
app.get('/api/admin/users', authMiddleware, requireAdmin, listUsers)
app.delete('/api/admin/users/:id', authMiddleware, requireAdmin, deleteUser)
app.get('/api/admin/stats', authMiddleware, requireAdmin, getStats)
```

**Plan-Based Feature Gating:**
```typescript
app.post('/api/batch/upload',
  authMiddleware,
  requirePlan(UserPlan.PRO, UserPlan.ENTERPRISE),
  uploadBatchFiles
)
```
