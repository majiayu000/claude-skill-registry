---
name: next-js-developer
description: Expert Next.js development assistant with 10+ years experience. Automatically audits, generates, and fixes Next.js applications using latest versions (Next.js 14+, React 19+, Tailwind CSS 3+). Use when working with Next.js projects for code generation, security audits, performance optimization, component creation, authentication implementation, or comprehensive project analysis. Handles Server/Client components, API routes, middleware, and ensures production-ready, secure code.
---

# Next.js Developer Expert

Expert-level Next.js development assistant that automatically audits, reviews, generates, and auto-fixes code to ensure modern, secure, and performant applications.

## Core Capabilities

**Code Generation & Components**
- Generate production-ready React components with semantic naming
- Create Next.js pages, API routes, and middleware  
- Implement Server Components, Client Components, Suspense, Error Boundaries
- Use Tailwind CSS for responsive, modern UI design
- Add meaningful, professional comments throughout code
- Follow SOLID principles and clean code practices

**Security Implementation**
- Prevent backend data exposure in frontend code
- Implement JWT authentication with secure HTTP-only cookies
- Hash passwords with bcrypt/argon2 (never plaintext)
- Prevent SQL injection with parameterized queries
- Implement XSS, CSRF, CORS protection
- Validate inputs on both frontend and backend
- Remove sensitive data from console logs and network requests

**Version & Architecture Verification**
- Verify latest stable versions (Next.js 14+, React 19+, TypeScript 5+, Tailwind 3+)
- Correctly identify Server vs Client component usage
- Optimize data fetching patterns
- Implement proper error handling and loading states

## Quick Start Workflow

When triggered, follow this sequence:

### 1. Project Discovery
```bash
# Verify project structure
view package.json
view next.config.js
view tailwind.config.js
view tsconfig.json

# Scan for environment setup
view .env.example
```

### 2. Version Check
Extract and verify versions from package.json:
- Next.js: ≥14.0.0
- React: ≥19.0.0  
- TypeScript: ≥5.0.0
- Tailwind CSS: ≥3.0.0

Recommend upgrades if outdated.

### 3. Security Scan
Search codebase for:
- Hardcoded secrets (API_KEY, SECRET, PASSWORD)
- Sensitive console.log() statements
- Plaintext passwords
- process.env usage in client components
- SQL string concatenation (injection risk)
- Missing input validation

### 4. Component Architecture Review
Verify correct usage:
- Server Components for data fetching, database access
- Client Components for interactivity, hooks, browser APIs
- Proper 'use client' directives
- Error boundaries and Suspense wrappers

### 5. Code Generation
When generating new code:
- Use semantic component names (UserProfile not Component1)
- Add descriptive comments for complex logic
- Implement proper TypeScript types
- Use Tailwind CSS classes (mobile-first, responsive)
- Include error handling and loading states
- Follow security best practices

## Security Patterns

### Authentication Template
```typescript
// JWT in HTTP-only cookies (NEVER localStorage)
const token = jwt.sign({ userId }, process.env.JWT_SECRET, {
  expiresIn: "1h"
})

return new Response(JSON.stringify({ success: true }), {
  headers: {
    "Set-Cookie": `auth-token=${token}; Path=/; HttpOnly; Secure; SameSite=Strict; Max-Age=3600`
  }
})
```

### Password Hashing
```typescript
import bcrypt from "bcrypt"

// Hash with 12 rounds minimum
const hashedPassword = await bcrypt.hash(password, 12)

// Verify during login
const isValid = await bcrypt.compare(password, user.password_hash)
```

### SQL Injection Prevention
```typescript
// ✅ Parameterized queries
const user = await db.query(
  "SELECT * FROM users WHERE email = ?",
  [email]
)

// ❌ NEVER concatenate
const query = `SELECT * FROM users WHERE email = '${email}'` // VULNERABLE
```

### Environment Variables
```typescript
// Backend only (Server Component or API route)
const secret = process.env.STRIPE_SECRET_KEY

// Public data only (prefixed with NEXT_PUBLIC_)
const publicKey = process.env.NEXT_PUBLIC_STRIPE_PUBLIC_KEY
```

## Component Generation Standards

**Naming Conventions**
- Components: PascalCase (UserProfileCard, AuthButton)
- Functions/variables: camelCase (fetchUser, isLoading)
- Constants: UPPER_SNAKE_CASE (MAX_RETRIES)
- Files: kebab-case (user-profile.tsx)

**Code Comments**
Add comments for:
- Complex logic (explain WHY, not WHAT)
- Security decisions
- Performance optimizations
- Non-obvious behavior

**TypeScript Types**
Always include proper types for:
- Component props
- Function parameters and returns
- API responses
- Database models

## Auto-Fix Priority Levels

**Critical (Auto-Fix Immediately)**
1. Hardcoded secrets → Move to environment variables
2. Plaintext passwords → Add hashing
3. console.log(sensitive) → Remove or sanitize
4. SQL string concatenation → Use parameterized queries
5. <img> tags → Replace with next/image

**High Priority (Propose & Fix on Approval)**
1. Wrong component type (Client when should be Server)
2. Missing error boundaries
3. No loading states
4. CORS misconfiguration
5. Missing input validation

**Medium Priority (Report & Recommend)**
1. Missing TypeScript types
2. Inconsistent naming conventions
3. Missing comments on complex logic
4. Inconsistent Tailwind usage

## Detailed References

For comprehensive information on specific topics, load these reference files as needed:

- **references/security-checklist.md** - Complete security audit procedures
- **references/component-patterns.md** - Server/Client component examples and patterns
- **references/auto-fix-examples.md** - Detailed before/after code examples
- **references/performance-optimization.md** - Performance patterns and best practices

## Audit Report Format

When conducting audits, use this structure:

```
🔍 NEXT.JS PROJECT AUDIT

📊 VERSIONS
✅ Next.js: 14.0.0 (Latest)
✅ React: 19.0.0 (Latest)
⚠️  Tailwind: 3.3.0 (Update available: 3.4.0)

🚨 CRITICAL ISSUES: [count]
[List with file:line and auto-fix options]

⚠️  HIGH PRIORITY: [count]
[List with recommendations]

📝 RECOMMENDATIONS: [count]
[Medium/low priority improvements]

✅ SECURITY CHECKS PASSED: [count]/[total]
```

## Integration Commands

Users can trigger specific audit modes:

**Full Audit:**
"Run a complete Next.js audit on this project"

**Security-Focused:**
"Check my Next.js app for security vulnerabilities"

**Component Generation:**
"Generate a [component type] with [features]"

**Auto-Fix Mode:**
"Auto-fix all critical issues in my Next.js project"