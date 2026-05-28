---
name: research-better-auth
description: Research Better Auth patterns, authentication flows, and session management using Exa code search and Ref documentation
---

# Research Better Auth Patterns

Use this skill when you need to:
- Learn Better Auth setup and configuration
- Understand authentication flows (email/password, OAuth, magic links)
- Research session management and cookies
- Find middleware protection patterns
- Learn role-based access control (RBAC)

## Process

1. **Identify Auth Need**
   - Authentication methods?
   - Session management?
   - Protected routes?
   - User management?
   - RBAC/permissions?

2. **Search Documentation (Ref)**
   ```
   Query patterns:
   - "Better Auth [feature]"
   - "Better Auth Next.js setup"
   - "Better Auth session management"
   - "Better Auth middleware"
   ```

3. **Find Implementation Examples (Exa)**
   ```
   Query patterns:
   - "Better Auth Next.js server actions authentication"
   - "Better Auth middleware protected routes example"
   - "Better Auth OAuth provider setup example"
   - "Better Auth role-based access control implementation"
   ```

## Common Research Topics

### Setup and Configuration
```typescript
// Documentation
Query: "Better Auth Next.js setup configuration"

// Code examples
Query: "Better Auth Next.js app router configuration example"
```

### Email/Password Auth
```typescript
// Documentation
Query: "Better Auth email password authentication"

// Code examples
Query: "Better Auth signup login bcrypt password hash example"
```

### OAuth Providers
```typescript
// Documentation
Query: "Better Auth OAuth providers Google GitHub"

// Code examples
Query: "Better Auth OAuth Google authentication Next.js example"
```

### Session Management
```typescript
// Documentation
Query: "Better Auth session management cookies"

// Code examples
Query: "Better Auth session validation server component example"
```

### Middleware Protection
```typescript
// Documentation
Query: "Better Auth Next.js middleware protected routes"

// Code examples
Query: "Better Auth middleware authentication check redirect example"
```

### User Management
```typescript
// Documentation
Query: "Better Auth user CRUD operations"

// Code examples
Query: "Better Auth user profile update password change example"
```

## Authentication Flows

### Sign Up
```
Query: "Better Auth signup flow validation email verification"
```

### Sign In
```
Query: "Better Auth login flow remember me session duration"
```

### Password Reset
```
Query: "Better Auth password reset forgot password email token"
```

### Email Verification
```
Query: "Better Auth email verification token expiration"
```

### Two-Factor Auth
```
Query: "Better Auth 2FA TOTP authenticator setup"
```

## Integration Patterns

### Server Components
```typescript
// Research pattern
Query: "Better Auth Next.js server component auth check example"
```

### Server Actions
```typescript
// Research pattern
Query: "Better Auth Next.js server action authentication mutation"
```

### API Routes
```typescript
// Research pattern
Query: "Better Auth Next.js API route authentication validation"
```

### Client Components
```typescript
// Research pattern
Query: "Better Auth React client component useSession hook"
```

## Authorization Patterns

### Role-Based Access Control
```
Query: "Better Auth RBAC role permissions check example"
```

### Protected Routes
```
Query: "Better Auth protected routes middleware redirect example"
```

### Resource Ownership
```
Query: "Better Auth check resource ownership authorization"
```

### API Authorization
```
Query: "Better Auth API route authorization role check"
```

## Session Patterns

### Cookie Configuration
```
Query: "Better Auth session cookie httpOnly secure sameSite"
```

### Session Expiration
```
Query: "Better Auth session expiration refresh token example"
```

### Multiple Sessions
```
Query: "Better Auth multiple device sessions management"
```

### Session Storage
```
Query: "Better Auth session storage database Redis"
```

## Security Patterns

### Password Security
```
Query: "Better Auth password hashing bcrypt security best practices"
```

### CSRF Protection
```
Query: "Better Auth CSRF protection token validation"
```

### Rate Limiting
```
Query: "Better Auth rate limiting brute force protection"
```

### Account Lockout
```
Query: "Better Auth account lockout failed login attempts"
```

## Database Integration

### With Drizzle ORM
```
Query: "Better Auth Drizzle ORM schema integration example"
```

### User Schema
```
Query: "Better Auth user table schema Drizzle PostgreSQL"
```

### Session Schema
```
Query: "Better Auth session table schema database"
```

## Advanced Features

### Social Auth
```
Query: "Better Auth social authentication multiple providers"
```

### Magic Links
```
Query: "Better Auth magic link passwordless authentication"
```

### Webhooks
```
Query: "Better Auth webhooks user events notifications"
```

### Account Linking
```
Query: "Better Auth link multiple auth methods single account"
```

## Output Format

Provide:
1. **Setup guide** - Configuration and initialization
2. **Auth flows** - Complete authentication flows
3. **Code examples** - Real implementations from Exa
4. **Security practices** - Password hashing, CSRF, rate limiting
5. **Integration patterns** - Next.js, Drizzle, API routes
6. **Common pitfalls** - What to avoid based on examples

## Project Context

Your project uses:
- Better Auth 1.1.3
- bcryptjs 3.0.3 (password hashing)
- Next.js 15 Server Components/Actions
- Drizzle ORM with PostgreSQL
- TypeScript strict mode

Security requirements:
- httpOnly secure cookies
- CSRF protection
- Rate limiting (Upstash Redis)
- Password requirements enforcement

## Common Use Cases

### User Registration
```
Research: "Better Auth user registration email password validation"
```

### Login System
```
Research: "Better Auth login system remember me session"
```

### Protected Dashboard
```
Research: "Better Auth protected dashboard routes middleware"
```

### Profile Management
```
Research: "Better Auth user profile update password change"
```

### OAuth Integration
```
Research: "Better Auth OAuth Google GitHub integration Next.js"
```

## When to Use

- Setting up authentication
- Adding new auth providers
- Implementing protected routes
- Managing user sessions
- Adding RBAC/permissions
- Debugging auth issues
- Learning Better Auth patterns
- Migrating from other auth systems

## Comparison with Other Solutions

Research when to use Better Auth vs:
- NextAuth.js
- Clerk
- Auth0
- Supabase Auth

```
Query: "Better Auth vs NextAuth comparison features"
```

## Related Skills

- research-nextjs (for middleware and routes)
- research-drizzle (for database integration)
- research-security (for security best practices)
- research-zod-validation (for input validation)
