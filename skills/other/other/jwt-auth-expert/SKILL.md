---
name: jwt-auth-expert
description: Comprehensive JWT authentication expert for senior developers (10+ years experience). Intelligently detects project language/framework and implements production-ready JWT auth systems with refresh tokens, secure HTTP-only cookies, token rotation, blacklisting, RBAC, MFA, and complete security. Covers Express, FastAPI, Next.js, React, Django, Flask, NestJS, and more. Automatically audits JWT implementations, generates complete auth systems (registration, login, logout, refresh, password reset), implements middleware, prevents XSS/CSRF attacks, uses bcrypt/argon2 hashing, and follows OWASP best practices. Use for implementing JWT authentication, token refresh flows, secure cookie storage, protected routes, role-based access control, security audits, and complete auth system generation.
---

# JWT Authentication Expert

Comprehensive senior-level JWT authentication assistant that intelligently detects your project stack and implements production-ready, secure authentication systems.

## Core Capabilities

**Complete Auth System**
- User registration with email verification
- Login with JWT token generation
- Logout with token invalidation
- Refresh token rotation
- Password reset flow
- Email verification tokens
- Remember me functionality

**Security Implementation**
- Secure HTTP-only cookies (NOT localStorage)
- Token signing (HS256, RS256)
- Refresh token rotation
- Token blacklisting/revocation
- Password hashing (bcrypt, argon2)
- Rate limiting on auth endpoints
- CSRF protection
- XSS prevention
- Brute force protection

**Advanced Features**
- Role-Based Access Control (RBAC)
- Permission-based authorization
- Multi-Factor Authentication (MFA)
- OAuth2/Social login integration
- Session management
- Device tracking
- Concurrent session limits

**Framework Support**
- **Node.js**: Express, Fastify, NestJS, Koa
- **Python**: FastAPI, Django, Flask
- **Next.js**: API routes, middleware, App Router
- **React**: Frontend token handling, protected routes
- **TypeScript**: Full type safety

## Auto-Scan Workflow

When triggered, automatically execute:

### 1. Project Detection
```bash
# Detect language and framework
view package.json          # Node.js project
view requirements.txt      # Python project
view pyproject.toml        # Python with modern tools
view next.config.js        # Next.js
view tsconfig.json         # TypeScript

# Scan existing auth
view src/
view app/
view routes/
view middleware/
view models/
```

### 2. Framework Intelligence
Based on detected files:
- **package.json + express** → Express.js implementation
- **package.json + next** → Next.js implementation
- **requirements.txt + fastapi** → FastAPI implementation
- **requirements.txt + django** → Django implementation
- **tsconfig.json** → TypeScript throughout

### 3. Security Audit
Check for:
- Tokens in localStorage (CRITICAL - vulnerable to XSS)
- Weak JWT secrets
- Missing token expiration
- No refresh token mechanism
- Plaintext passwords
- Missing CSRF protection
- No rate limiting
- Weak password requirements
- Missing HTTPS enforcement

### 4. Code Generation Standards
Generate based on stack:
- **TypeScript projects** → Full TypeScript with strict types
- **JavaScript projects** → Modern ES6+ with JSDoc
- **Python projects** → Type hints with mypy
- All code includes comprehensive error handling
- Production-ready logging
- Detailed comments explaining security decisions

## JWT Token Structure

### Access Token (Short-lived: 15min)
```typescript
{
  "sub": "user_id",           // Subject (user identifier)
  "email": "user@example.com",
  "role": "admin",            // For RBAC
  "permissions": ["read", "write"],
  "iat": 1234567890,          // Issued at
  "exp": 1234568790,          // Expires (15 min from iat)
  "jti": "unique_token_id"    // JWT ID for blacklisting
}
```

### Refresh Token (Long-lived: 7 days)
```typescript
{
  "sub": "user_id",
  "type": "refresh",
  "tokenFamily": "family_id", // For rotation detection
  "iat": 1234567890,
  "exp": 1235172690           // 7 days
}
```

## Security Patterns

### ✅ Secure Token Storage (HTTP-only Cookies)
```typescript
// ❌ NEVER DO THIS - Vulnerable to XSS
localStorage.setItem('token', token)

// ✅ CORRECT - HTTP-only cookie
res.cookie('accessToken', token, {
  httpOnly: true,        // Not accessible via JavaScript
  secure: true,          // HTTPS only
  sameSite: 'strict',    // CSRF protection
  maxAge: 15 * 60 * 1000 // 15 minutes
})

res.cookie('refreshToken', refreshToken, {
  httpOnly: true,
  secure: true,
  sameSite: 'strict',
  maxAge: 7 * 24 * 60 * 60 * 1000, // 7 days
  path: '/api/auth/refresh' // Only sent to refresh endpoint
})
```

### ✅ Password Hashing
```typescript
import bcrypt from 'bcrypt'

// Hash on registration
const hashedPassword = await bcrypt.hash(password, 12) // 12 rounds minimum

// Verify on login
const isValid = await bcrypt.compare(password, user.hashedPassword)
```

### ✅ Token Refresh Flow
```typescript
1. Client request with expired access token
2. Server detects expiration → Check refresh token
3. Validate refresh token
4. Generate NEW access token + NEW refresh token (rotation)
5. Invalidate old refresh token (prevent reuse)
6. Set new tokens in HTTP-only cookies
7. Return success to client
```

### ✅ Token Blacklisting (Logout)
```typescript
// Store invalidated tokens in Redis/database
await redis.set(`blacklist:${tokenId}`, 'true', 'EX', tokenExpiry)

// Check on every request
const isBlacklisted = await redis.get(`blacklist:${tokenId}`)
if (isBlacklisted) {
  throw new UnauthorizedError('Token has been revoked')
}
```

## Complete Auth System Template

### Registration → Login → Protected Route Flow

**1. Registration**
```typescript
POST /api/auth/register
{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "name": "John Doe"
}

→ Hash password (bcrypt)
→ Create user in database
→ Generate email verification token
→ Send verification email
→ Return success (NO tokens yet)
```

**2. Email Verification**
```typescript
GET /api/auth/verify-email?token=verification_token

→ Verify token validity
→ Mark email as verified
→ Allow user to login
```

**3. Login**
```typescript
POST /api/auth/login
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}

→ Validate credentials
→ Check email verified
→ Generate access token (15min)
→ Generate refresh token (7 days)
→ Store refresh token in database
→ Set HTTP-only cookies
→ Return user info (NO tokens in body)
```

**4. Access Protected Route**
```typescript
GET /api/users/profile
Cookie: accessToken=xxx; refreshToken=yyy

→ Extract token from cookie
→ Verify token signature
→ Check expiration
→ Check blacklist
→ Attach user to request
→ Continue to route handler
```

**5. Token Refresh (When Access Token Expires)**
```typescript
POST /api/auth/refresh
Cookie: refreshToken=xxx

→ Extract refresh token from cookie
→ Verify refresh token
→ Check if revoked/blacklisted
→ Generate NEW access token
→ Generate NEW refresh token (rotation)
→ Invalidate old refresh token
→ Set new cookies
→ Return success
```

**6. Logout**
```typescript
POST /api/auth/logout
Cookie: accessToken=xxx; refreshToken=yyy

→ Extract tokens
→ Blacklist access token
→ Delete refresh token from database
→ Clear cookies
→ Return success
```

## Reference Documentation

For framework-specific implementations, load:

### Backend Frameworks
- **references/express-jwt.md** - Complete Express.js implementation
- **references/fastapi-jwt.md** - FastAPI with dependency injection
- **references/nextjs-jwt.md** - Next.js API routes + middleware
- **references/django-jwt.md** - Django REST framework
- **references/nestjs-jwt.md** - NestJS with decorators

### Frontend
- **references/react-jwt.md** - React hooks, protected routes, context
- **references/nextjs-frontend.md** - Next.js client-side auth

### Advanced Topics
- **references/jwt-security.md** - Complete security checklist
- **references/rbac-implementation.md** - Role-based access control
- **references/token-rotation.md** - Refresh token strategies
- **references/mfa-implementation.md** - Multi-factor authentication

### Infrastructure
- **references/redis-session.md** - Redis for token blacklisting
- **references/rate-limiting.md** - Brute force protection

## Auto-Fix Priority

**Critical (Auto-Fix Immediately)**
1. Tokens in localStorage → HTTP-only cookies
2. Plaintext passwords → bcrypt/argon2 hashing
3. No token expiration → Add exp claim
4. Weak JWT secret → Generate strong secret
5. No HTTPS in production → Enforce HTTPS

**High Priority (Propose & Fix)**
1. Missing refresh token mechanism
2. No token rotation
3. No rate limiting on auth endpoints
4. Missing CSRF protection
5. No password strength validation

**Medium Priority (Recommend)**
1. No email verification
2. Missing password reset flow
3. No device tracking
4. Single session only (no concurrent sessions)
5. No MFA support

## Common Patterns by Framework

### Express.js Pattern
```typescript
// Middleware-based with cookie-parser
app.use(cookieParser())
app.use('/api/protected', authenticateToken)

// Token in HTTP-only cookie
res.cookie('accessToken', token, cookieOptions)
```

### Next.js Pattern
```typescript
// Middleware for route protection
export function middleware(request: NextRequest) {
  const token = request.cookies.get('accessToken')
  // Verify and protect routes
}

// API routes with cookies
import { cookies } from 'next/headers'
cookies().set('accessToken', token, cookieOptions)
```

### FastAPI Pattern
```typescript
# Dependency injection
async def get_current_user(token: str = Cookie(...)):
    # Verify token from cookie
    return user

@app.get("/protected")
async def protected_route(user = Depends(get_current_user)):
    return {"user": user}
```

## Integration Commands

**Complete Auth System:**
"Create a complete JWT auth system for Express with refresh tokens in cookies"

**Add to Existing:**
"Add JWT authentication to my Next.js app"

**Security Audit:**
"Audit my JWT implementation for security vulnerabilities"

**Protected Routes:**
"Implement JWT middleware for protected routes"

**RBAC:**
"Add role-based access control to my auth system"

**Frontend:**
"Implement JWT auth in React with protected routes"