---
name: security-hardening
description: "Security best practices for web applications. Covers OWASP Top 10, authentication, authorization, input validation, CSP, and secure headers."
version: 1.0.0
triggers:
  - security
  - owasp
  - authentication
  - authorization
  - xss
  - csrf
  - injection
---

# Security Hardening Skill

Implement comprehensive security practices to protect web applications from common vulnerabilities.

## OWASP Top 10 (2024)

| Risk | Prevention |
|------|------------|
| **Injection** | Parameterized queries, input validation |
| **Broken Auth** | MFA, secure sessions, rate limiting |
| **Sensitive Data** | Encryption at rest/transit, minimal exposure |
| **XXE** | Disable external entities, use JSON |
| **Broken Access** | RBAC, verify ownership |
| **Misconfig** | Security headers, disable debug |
| **XSS** | Output encoding, CSP |
| **Insecure Deserialization** | Validate input, use safe formats |
| **Vulnerable Components** | Audit deps, update regularly |
| **Logging Gaps** | Log security events, monitor |

## Security Headers

### Next.js Configuration

```typescript
// next.config.js
const securityHeaders = [
  {
    key: 'X-DNS-Prefetch-Control',
    value: 'on'
  },
  {
    key: 'Strict-Transport-Security',
    value: 'max-age=63072000; includeSubDomains; preload'
  },
  {
    key: 'X-Frame-Options',
    value: 'SAMEORIGIN'
  },
  {
    key: 'X-Content-Type-Options',
    value: 'nosniff'
  },
  {
    key: 'X-XSS-Protection',
    value: '1; mode=block'
  },
  {
    key: 'Referrer-Policy',
    value: 'strict-origin-when-cross-origin'
  },
  {
    key: 'Permissions-Policy',
    value: 'camera=(), microphone=(), geolocation=()'
  },
  {
    key: 'Content-Security-Policy',
    value: `
      default-src 'self';
      script-src 'self' 'unsafe-inline';
      style-src 'self' 'unsafe-inline';
      img-src 'self' blob: data: https:;
      font-src 'self';
      connect-src 'self' https://api.frankx.ai;
      frame-ancestors 'none';
    `.replace(/\n/g, '')
  }
];

module.exports = {
  async headers() {
    return [
      {
        source: '/:path*',
        headers: securityHeaders,
      },
    ];
  },
};
```

## Input Validation

### Zod Schema Validation

```typescript
import { z } from 'zod';

const UserInputSchema = z.object({
  email: z.string().email().max(255),
  name: z.string().min(1).max(100).regex(/^[a-zA-Z\s]+$/),
  age: z.number().int().min(0).max(150),
  url: z.string().url().optional(),
});

// Sanitize HTML content
import DOMPurify from 'isomorphic-dompurify';

const sanitizedHtml = DOMPurify.sanitize(userInput, {
  ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'a'],
  ALLOWED_ATTR: ['href'],
});
```

### SQL Injection Prevention

```typescript
// GOOD: Parameterized queries
const user = await prisma.user.findUnique({
  where: { email: userEmail }
});

// BAD: String interpolation - NEVER do this
// const user = db.query(`SELECT * FROM users WHERE email = '${email}'`);
```

## Authentication Best Practices

### Password Hashing

```typescript
import { hash, verify } from 'argon2';

// Hash password
const hashedPassword = await hash(password, {
  type: 2, // Argon2id
  memoryCost: 65536,
  timeCost: 3,
  parallelism: 4,
});

// Verify password
const isValid = await verify(hashedPassword, password);
```

### Session Security

```typescript
// lib/session.ts
import { cookies } from 'next/headers';
import { SignJWT, jwtVerify } from 'jose';

const secret = new TextEncoder().encode(process.env.SESSION_SECRET);

export async function createSession(userId: string) {
  const token = await new SignJWT({ userId })
    .setProtectedHeader({ alg: 'HS256' })
    .setIssuedAt()
    .setExpirationTime('7d')
    .sign(secret);

  (await cookies()).set('session', token, {
    httpOnly: true,
    secure: process.env.NODE_ENV === 'production',
    sameSite: 'lax',
    maxAge: 60 * 60 * 24 * 7, // 7 days
    path: '/',
  });
}
```

### Rate Limiting

```typescript
import { Ratelimit } from '@upstash/ratelimit';
import { Redis } from '@upstash/redis';

const ratelimit = new Ratelimit({
  redis: Redis.fromEnv(),
  limiter: Ratelimit.slidingWindow(5, '1 m'), // 5 attempts per minute
  analytics: true,
});

export async function loginRateLimit(ip: string) {
  const { success, remaining } = await ratelimit.limit(`login:${ip}`);
  if (!success) {
    throw new Error('Too many login attempts. Try again later.');
  }
  return remaining;
}
```

## Authorization (RBAC)

```typescript
// lib/permissions.ts
type Role = 'admin' | 'editor' | 'viewer';
type Permission = 'read' | 'write' | 'delete' | 'admin';

const rolePermissions: Record<Role, Permission[]> = {
  admin: ['read', 'write', 'delete', 'admin'],
  editor: ['read', 'write'],
  viewer: ['read'],
};

export function hasPermission(role: Role, permission: Permission): boolean {
  return rolePermissions[role]?.includes(permission) ?? false;
}

// Middleware usage
export async function requirePermission(permission: Permission) {
  const session = await getSession();
  if (!session || !hasPermission(session.role, permission)) {
    throw new Error('Forbidden');
  }
}
```

## CSRF Protection

```typescript
// For forms in Next.js, use Server Actions which have built-in CSRF protection
// For API routes, use the double-submit cookie pattern:

import { cookies } from 'next/headers';
import { nanoid } from 'nanoid';

export async function generateCsrfToken() {
  const token = nanoid(32);
  (await cookies()).set('csrf', token, {
    httpOnly: true,
    secure: true,
    sameSite: 'strict',
  });
  return token;
}

export async function verifyCsrfToken(submittedToken: string) {
  const storedToken = (await cookies()).get('csrf')?.value;
  if (!storedToken || storedToken !== submittedToken) {
    throw new Error('Invalid CSRF token');
  }
}
```

## Secrets Management

```typescript
// NEVER commit secrets to git
// Use environment variables

// .env.local (gitignored)
DATABASE_URL=postgresql://...
JWT_SECRET=super-long-random-string
API_KEY=sk-...

// Access in code
const apiKey = process.env.API_KEY;

// Validate required secrets at startup
const requiredEnvVars = ['DATABASE_URL', 'JWT_SECRET'];
for (const envVar of requiredEnvVars) {
  if (!process.env[envVar]) {
    throw new Error(`Missing required environment variable: ${envVar}`);
  }
}
```

## Security Checklist

- [ ] HTTPS only (HSTS enabled)
- [ ] Secure headers configured
- [ ] Input validation on all user input
- [ ] Parameterized database queries
- [ ] Passwords hashed with Argon2id
- [ ] Sessions: httpOnly, secure, sameSite
- [ ] Rate limiting on auth endpoints
- [ ] RBAC implemented
- [ ] CSRF protection enabled
- [ ] Dependencies audited (`npm audit`)
- [ ] Secrets in environment variables
- [ ] Error messages don't leak info
- [ ] Logging security events

## Anti-Patterns

Avoid these dangerous practices:
- Storing passwords in plain text
- Trusting client-side validation only
- Exposing stack traces to users
- Using MD5/SHA1 for passwords
- Hardcoding secrets in code
- Executing arbitrary user input as code

Best practices:
- Hash with Argon2id/bcrypt
- Server-side validation always
- Generic error messages
- Modern hashing algorithms
- Environment variables for secrets
- Never execute untrusted input
