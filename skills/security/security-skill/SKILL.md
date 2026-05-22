---
name: "security-skill"
description: "Application security patterns - authentication, secrets management, input validation, OWASP Top 10. Use when: auth, JWT, secrets, API keys, SQL injection, XSS, CSRF, RLS, security audit, pen testing basics."
---

<objective>
Comprehensive security skill covering authentication patterns, secrets management, input validation, and common vulnerability prevention. Focuses on practical patterns for web applications with Supabase, Next.js, and Python backends.

Security is not optional - it's a fundamental requirement. This skill helps you build secure applications from the start, not bolt on security as an afterthought.
</objective>

<security_mindset>
## The Security Mindset

### Core Principles

1. **Defense in depth** - Multiple layers of security, not one wall
2. **Least privilege** - Grant minimum access required
3. **Never trust input** - Validate everything from users and external systems
4. **Fail secure** - Errors should deny access, not grant it
5. **Keep secrets secret** - API keys never in code or logs

### Security Questions to Ask

Before shipping any feature:
- [ ] What data does this expose?
- [ ] Who can access this endpoint/page?
- [ ] What happens if the user sends malicious input?
- [ ] Are secrets properly protected?
- [ ] Is sensitive data logged?
</security_mindset>

<authentication>
## Authentication Patterns

### JWT vs Session

| Aspect | JWT | Session |
|--------|-----|---------|
| Storage | Client (localStorage/cookie) | Server (DB/Redis) |
| Scalability | Stateless, easy to scale | Requires shared session store |
| Revocation | Hard (need blacklist) | Easy (delete from store) |
| Size | Larger (contains claims) | Small (just session ID) |
| Best for | APIs, microservices | Traditional web apps |

### JWT Best Practices

```typescript
// DO: Short-lived access tokens + refresh tokens
const accessToken = jwt.sign(
  { userId: user.id, role: user.role },
  process.env.JWT_SECRET,
  { expiresIn: '15m' } // Short-lived!
);

const refreshToken = jwt.sign(
  { userId: user.id },
  process.env.JWT_REFRESH_SECRET,
  { expiresIn: '7d' }
);

// DON'T: Long-lived tokens with sensitive data
// Bad example - never do this:
// { expiresIn: '365d' } // Too long!
// Including PII like SSN in token payload
```

### Token Storage

| Method | XSS Safe | CSRF Safe | Recommendation |
|--------|----------|-----------|----------------|
| localStorage | No | Yes | Avoid for auth |
| httpOnly cookie | Yes | No (needs CSRF token) | Recommended |
| Memory (variable) | Yes | Yes | Best for SPAs |

### Refresh Token Flow

```
┌─────────┐                    ┌─────────┐                    ┌─────────┐
│ Client  │                    │  Server │                    │   DB    │
└────┬────┘                    └────┬────┘                    └────┬────┘
     │                              │                              │
     │  Login (email, password)     │                              │
     │─────────────────────────────>│                              │
     │                              │  Verify credentials          │
     │                              │─────────────────────────────>│
     │                              │<─────────────────────────────│
     │  Access token (15m)          │                              │
     │  Refresh token (7d)          │  Store refresh token hash    │
     │<─────────────────────────────│─────────────────────────────>│
     │                              │                              │
     │  API call + access token     │                              │
     │─────────────────────────────>│                              │
     │  Response                    │                              │
     │<─────────────────────────────│                              │
     │                              │                              │
     │  [Access token expired]      │                              │
     │  Refresh token               │                              │
     │─────────────────────────────>│  Verify refresh token        │
     │                              │─────────────────────────────>│
     │  New access token            │                              │
     │<─────────────────────────────│                              │
```

### Password Handling

```typescript
import bcrypt from 'bcrypt';

// DO: Hash with sufficient rounds
const SALT_ROUNDS = 12; // ~300ms on modern hardware
const hash = await bcrypt.hash(password, SALT_ROUNDS);

// DO: Constant-time comparison
const isValid = await bcrypt.compare(inputPassword, storedHash);

// DON'T: Use weak hashing algorithms like MD5 or SHA1 for passwords
```

### Password Requirements

```typescript
const passwordSchema = z.string()
  .min(8, 'Minimum 8 characters')
  .max(128, 'Maximum 128 characters')
  .regex(/[a-z]/, 'Must contain lowercase')
  .regex(/[A-Z]/, 'Must contain uppercase')
  .regex(/[0-9]/, 'Must contain number')
  .regex(/[^a-zA-Z0-9]/, 'Must contain special character');

// Check against common passwords (haveibeenpwned API)
async function isPasswordPwned(password: string): Promise<boolean> {
  const sha1 = crypto.createHash('sha1').update(password).digest('hex').toUpperCase();
  const prefix = sha1.slice(0, 5);
  const suffix = sha1.slice(5);

  const response = await fetch(`https://api.pwnedpasswords.com/range/${prefix}`);
  const text = await response.text();

  return text.includes(suffix);
}
```
</authentication>

<secrets_management>
## Secrets Management

### The Golden Rule

**NEVER commit secrets to version control**

```bash
# .gitignore - Always include
.env
.env.local
.env.*.local
*.pem
*.key
credentials.json
secrets.yaml
```

### Environment Variables

```bash
# .env (local development)
DATABASE_URL=postgresql://localhost:5432/myapp
JWT_SECRET=dev-secret-change-in-production
STRIPE_SECRET_KEY=sk_test_...

# .env.example (commit this!)
DATABASE_URL=postgresql://localhost:5432/myapp
JWT_SECRET=generate-secure-secret
STRIPE_SECRET_KEY=sk_test_your_key_here
```

### Loading Secrets

```typescript
// DO: Validate at startup
import { z } from 'zod';

const envSchema = z.object({
  DATABASE_URL: z.string().url(),
  JWT_SECRET: z.string().min(32),
  STRIPE_SECRET_KEY: z.string().startsWith('sk_'),
});

const env = envSchema.parse(process.env);

// DON'T: Use undefined secrets
// Always validate that required env vars exist
```

### Secret Rotation

```typescript
// Support multiple secrets during rotation
const JWT_SECRETS = [
  process.env.JWT_SECRET_NEW,    // Current
  process.env.JWT_SECRET_OLD,    // Previous (for validation)
].filter(Boolean);

function verifyToken(token: string): JWTPayload {
  for (const secret of JWT_SECRETS) {
    try {
      return jwt.verify(token, secret);
    } catch {
      continue;
    }
  }
  throw new Error('Invalid token');
}
```

### Never Log Secrets

```typescript
// DO: Mask sensitive data in logs
logger.info('User login', {
  userId: user.id,
  email: maskEmail(user.email), // t***@example.com
});

// DON'T: Log tokens or credentials
// Never log: authorization headers, request bodies with passwords, API keys
```
</secrets_management>

<input_validation>
## Input Validation

### Validate at System Boundaries

```
┌─────────────────────────────────────────────────────────┐
│                    Your Application                      │
│                                                          │
│   ┌──────────┐     VALIDATE      ┌──────────────────┐  │
│   │  User    │ ───────────────>  │  Business Logic   │  │
│   │  Input   │                   │  (trusted data)   │  │
│   └──────────┘                   └──────────────────┘  │
│                                                          │
│   ┌──────────┐     VALIDATE      ┌──────────────────┐  │
│   │ External │ ───────────────>  │  Services         │  │
│   │   API    │                   │                   │  │
│   └──────────┘                   └──────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

### Schema Validation (Zod)

```typescript
import { z } from 'zod';

// Define schemas
const createUserSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8).max(128),
  name: z.string().min(1).max(100),
  age: z.number().int().min(13).max(120).optional(),
});

// Validate input
export async function createUser(input: unknown) {
  const data = createUserSchema.parse(input); // Throws if invalid
  // data is now typed and validated
  return db.users.create(data);
}

// API handler
export async function POST(req: Request) {
  try {
    const body = await req.json();
    const user = await createUser(body);
    return Response.json(user, { status: 201 });
  } catch (error) {
    if (error instanceof z.ZodError) {
      return Response.json({ errors: error.errors }, { status: 400 });
    }
    throw error;
  }
}
```

### Sanitization

```typescript
import DOMPurify from 'dompurify';
import { JSDOM } from 'jsdom';

const window = new JSDOM('').window;
const purify = DOMPurify(window);

// Sanitize HTML (for rich text fields)
const cleanHtml = purify.sanitize(userInput, {
  ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'a', 'p'],
  ALLOWED_ATTR: ['href']
});

// For plain text - escape or strip HTML
const plainText = purify.sanitize(userInput, { ALLOWED_TAGS: [] });
```
</input_validation>

<sql_injection>
## SQL Injection Prevention

### The Problem

Attackers can manipulate SQL queries through unsanitized input.
Example attack payload: `'; DROP TABLE users; --`

### The Solution: Parameterized Queries

```typescript
// SAFE: Parameterized query (Prisma)
const user = await prisma.user.findUnique({
  where: { email: email }
});

// SAFE: Parameterized query (raw SQL)
const user = await db.query(
  'SELECT * FROM users WHERE email = $1',
  [email]
);

// SAFE: Supabase
const { data } = await supabase
  .from('users')
  .select()
  .eq('email', email);
```

### Supabase RLS (Row Level Security)

```sql
-- Enable RLS
ALTER TABLE posts ENABLE ROW LEVEL SECURITY;

-- Users can only see their own posts
CREATE POLICY "Users see own posts"
  ON posts FOR SELECT
  USING (auth.uid() = user_id);

-- Users can only create posts as themselves
CREATE POLICY "Users create own posts"
  ON posts FOR INSERT
  WITH CHECK (auth.uid() = user_id);

-- Users can only update their own posts
CREATE POLICY "Users update own posts"
  ON posts FOR UPDATE
  USING (auth.uid() = user_id);

-- Users can only delete their own posts
CREATE POLICY "Users delete own posts"
  ON posts FOR DELETE
  USING (auth.uid() = user_id);
```
</sql_injection>

<xss_prevention>
## XSS Prevention

### The Problem

Attackers inject malicious scripts that execute in victim's browser, stealing cookies/data.

### The Solution: Auto-escaping + CSP

```typescript
// React auto-escapes by default - this is safe
return <div>Welcome, {userName}</div>;

// AVOID rendering raw HTML from user input
// If you absolutely must render user HTML, ALWAYS sanitize with DOMPurify first
import DOMPurify from 'dompurify';
const sanitizedContent = DOMPurify.sanitize(userContent);
```

### Content Security Policy

```typescript
// next.config.js
const securityHeaders = [
  {
    key: 'Content-Security-Policy',
    value: [
      "default-src 'self'",
      "script-src 'self'", // Avoid 'unsafe-inline' if possible
      "style-src 'self' 'unsafe-inline'",
      "img-src 'self' data: https:",
      "font-src 'self'",
      "connect-src 'self' https://api.supabase.co",
    ].join('; ')
  }
];
```
</xss_prevention>

<csrf_protection>
## CSRF Protection

### The Problem

Attackers trick authenticated users into submitting malicious requests to your site.

### The Solution: CSRF Tokens + SameSite Cookies

```typescript
// Server: Generate token
import { randomBytes } from 'crypto';

function generateCsrfToken(): string {
  return randomBytes(32).toString('hex');
}

// Store in session
session.csrfToken = generateCsrfToken();

// Client: Include in forms as hidden field
// Server: Validate token matches session

// Modern approach: SameSite cookies (most effective)
res.cookie('session', sessionId, {
  httpOnly: true,
  secure: true,
  sameSite: 'strict', // or 'lax'
});
```
</csrf_protection>

<references>
For detailed patterns, load the appropriate reference:

| Topic | Reference File | When to Load |
|-------|----------------|--------------|
| Auth patterns | `reference/auth-patterns.md` | JWT, OAuth, sessions |
| Secrets | `reference/secrets-management.md` | API keys, env vars |
| Input validation | `reference/input-validation.md` | Sanitization, schemas |
| Supabase RLS | `reference/rls-policies.md` | Row level security |
| OWASP Top 10 | `reference/owasp-top-10.md` | Vulnerability checklist |

**To load:** Ask for the specific topic or check if context suggests it.
</references>

<checklist>
## Security Checklist

Before deploying:

### Authentication
- [ ] Passwords hashed with bcrypt (12+ rounds)
- [ ] JWT tokens short-lived (15 min max)
- [ ] Refresh tokens stored securely
- [ ] Session cookies httpOnly + secure + sameSite

### Secrets
- [ ] No secrets in code or version control
- [ ] Environment variables validated at startup
- [ ] Secrets not logged

### Input
- [ ] All user input validated with schemas
- [ ] SQL uses parameterized queries
- [ ] HTML sanitized before rendering
- [ ] File uploads validated (type, size, name)

### Headers
- [ ] HTTPS enforced
- [ ] CSP header configured
- [ ] CORS restricted to allowed origins
- [ ] Security headers set (HSTS, X-Frame-Options)

### Authorization
- [ ] RLS enabled on all tables
- [ ] API endpoints check permissions
- [ ] Admin routes protected
- [ ] Rate limiting on auth endpoints
</checklist>
