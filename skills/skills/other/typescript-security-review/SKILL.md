---
name: typescript-security-review
description: Provides comprehensive security review capability for TypeScript and Node.js applications, validates code against XSS, injection, CSRF, JWT/OAuth2 flaws, dependency CVEs, and secrets exposure. Use when performing security audits, before deployment, reviewing authentication/authorization implementations, or ensuring OWASP compliance for Express, NestJS, and Next.js. Triggers on "security review", "check for security issues", "TypeScript security audit".
allowed-tools: Read, Edit, Grep, Glob, Bash
---

# TypeScript Security Review

## Overview

This skill provides structured, comprehensive security review for TypeScript and Node.js applications. It evaluates code against OWASP Top 10, framework-specific security best practices, and production-readiness security criteria. The review produces actionable findings classified by severity (Critical, High, Medium, Low) with concrete remediation examples.

This skill delegates to the `typescript-security-expert` agent for deep security analysis when invoked through the agent system.

## When to Use

- Performing security audits on TypeScript/Node.js codebases
- Reviewing authentication and authorization implementations (JWT, OAuth2, Passport.js)
- Checking for common vulnerabilities (XSS, injection, CSRF, path traversal)
- Validating input validation and sanitization logic
- Reviewing dependency security (npm audit, known CVEs)
- Checking secrets management and environment variable handling
- Assessing API security (rate limiting, CORS, security headers)
- Reviewing Express, NestJS, or Next.js security configurations
- Before deploying to production or after significant code changes
- Compliance checks (GDPR, HIPAA, SOC2 data handling requirements)

## Instructions

1. **Identify Scope**: Determine which files and modules are under security review. Prioritize authentication, authorization, data handling, API endpoints, and configuration files. Use `grep` to find security-sensitive patterns (`eval`, `exec`, `innerHTML`, password handling, JWT operations).

2. **Check Authentication & Authorization**: Review JWT implementation (signing algorithm, expiration, refresh tokens), OAuth2/OIDC integration, session management, password hashing (bcrypt/argon2), and multi-factor authentication. Verify that all protected routes enforce authentication.

3. **Scan for Injection Vulnerabilities**: Check for SQL/NoSQL injection in database queries, command injection in `exec`/`spawn`, template injection, and LDAP injection. Verify that all user input is validated and parameterized queries are used.

4. **Review Input Validation**: Check that all API inputs are validated with Zod, Joi, or class-validator. Verify schema completeness — no missing fields, proper type constraints, length limits, and format validation. Check for validation bypass paths.

5. **Assess XSS Prevention**: Review React component output for `dangerouslySetInnerHTML` usage, check Content Security Policy headers, verify HTML sanitization for user-generated content, and check template rendering in server-side code.

6. **Check Secrets Management**: Scan for hardcoded credentials, API keys, and secrets in source code. Verify `.env` files are gitignored, environment variables are validated at startup, and secrets are accessed through proper management services.

7. **Review Dependency Security**: Run `npm audit` or check `package-lock.json` for known vulnerabilities. Identify outdated dependencies with known CVEs. Check for unnecessary dependencies that increase attack surface.

8. **Evaluate Security Headers & Configuration**: Check for helmet.js or manual security header configuration. Review CORS policy, rate limiting, HTTPS enforcement, cookie security flags (HttpOnly, Secure, SameSite), and CSP configuration.

9. **Produce Security Report**: Generate a structured report with severity-classified findings (Critical, High, Medium, Low), remediation guidance with code examples, and a security posture summary.

## Examples

### Example 1: JWT Security Review

```typescript
// ❌ Critical: Weak JWT configuration
import jwt from 'jsonwebtoken';

const SECRET = 'mysecret123'; // Hardcoded weak secret

function generateToken(user: User) {
  return jwt.sign({ id: user.id, role: user.role }, SECRET);
  // Missing expiration, weak secret, no algorithm specification
}

function verifyToken(token: string) {
  return jwt.verify(token, SECRET); // No algorithm restriction
}

// ✅ Secure: Proper JWT configuration
import jwt from 'jsonwebtoken';
import { randomBytes } from 'crypto';

const JWT_SECRET = process.env.JWT_SECRET;
if (!JWT_SECRET || JWT_SECRET.length < 32) {
  throw new Error('JWT_SECRET must be set and at least 32 characters');
}

function generateToken(user: User): string {
  return jwt.sign(
    { sub: user.id }, // Minimal claims, no sensitive data
    JWT_SECRET,
    {
      algorithm: 'HS256',
      expiresIn: '15m',
      issuer: 'my-app',
      audience: 'my-app-client',
    }
  );
}

function verifyToken(token: string): JwtPayload {
  return jwt.verify(token, JWT_SECRET, {
    algorithms: ['HS256'], // Restrict accepted algorithms
    issuer: 'my-app',
    audience: 'my-app-client',
  }) as JwtPayload;
}
```

### Example 2: SQL Injection Prevention

```typescript
// ❌ Critical: SQL injection vulnerability
async function findUser(email: string) {
  const result = await db.query(
    `SELECT * FROM users WHERE email = '${email}'`
  );
  return result.rows[0];
}

// ✅ Secure: Parameterized query
async function findUser(email: string) {
  const result = await db.query(
    'SELECT id, name, email FROM users WHERE email = $1',
    [email]
  );
  return result.rows[0];
}

// ✅ Secure: ORM with type-safe queries (Drizzle example)
async function findUser(email: string) {
  return db.select({
    id: users.id,
    name: users.name,
    email: users.email,
  })
  .from(users)
  .where(eq(users.email, email))
  .limit(1);
}
```

### Example 3: Input Validation

```typescript
// ❌ High: Missing input validation
app.post('/api/users', async (req, res) => {
  const user = await createUser(req.body);
  res.json(user);
});

// ✅ Secure: Comprehensive input validation with Zod
import { z } from 'zod';

const createUserSchema = z.object({
  name: z.string().min(1).max(100).trim(),
  email: z.string().email().max(254).toLowerCase(),
  password: z.string()
    .min(12, 'Password must be at least 12 characters')
    .regex(/[A-Z]/, 'Must contain uppercase letter')
    .regex(/[a-z]/, 'Must contain lowercase letter')
    .regex(/[0-9]/, 'Must contain a number'),
  role: z.enum(['user', 'editor']).default('user'),
});

app.post('/api/users', async (req, res) => {
  const result = createUserSchema.safeParse(req.body);
  if (!result.success) {
    return res.status(400).json({ errors: result.error.flatten() });
  }
  const user = await createUser(result.data);
  res.status(201).json(user);
});
```

### Example 4: XSS Prevention

```tsx
// ❌ High: XSS vulnerability through dangerouslySetInnerHTML
function Comment({ content }: { content: string }) {
  return <div dangerouslySetInnerHTML={{ __html: content }} />;
}

// ✅ Secure: Sanitize HTML before rendering
import DOMPurify from 'isomorphic-dompurify';

function Comment({ content }: { content: string }) {
  const sanitized = DOMPurify.sanitize(content, {
    ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'a', 'p', 'br'],
    ALLOWED_ATTR: ['href', 'target', 'rel'],
  });
  return <div dangerouslySetInnerHTML={{ __html: sanitized }} />;
}

// ✅ Better: Use a markdown renderer instead of raw HTML
import ReactMarkdown from 'react-markdown';

function Comment({ content }: { content: string }) {
  return <ReactMarkdown>{content}</ReactMarkdown>;
}
```

### Example 5: Security Headers and Configuration

```typescript
// ❌ Medium: Missing security headers and permissive CORS
const app = express();
app.use(cors()); // Allows all origins

// ✅ Secure: Comprehensive security configuration
import helmet from 'helmet';
import cors from 'cors';
import rateLimit from 'express-rate-limit';

const app = express();

app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      scriptSrc: ["'self'"],
      styleSrc: ["'self'", "'unsafe-inline'"],
      imgSrc: ["'self'", 'data:', 'https:'],
    },
  },
  hsts: { maxAge: 31536000, includeSubDomains: true, preload: true },
}));

app.use(cors({
  origin: process.env.ALLOWED_ORIGINS?.split(',') ?? [],
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
}));

app.use(rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 100,
  standardHeaders: true,
  legacyHeaders: false,
}));
```

## Review Output Format

Structure all security review findings as follows:

### 1. Security Posture Summary
Overall security assessment score (1-10) with key observations and risk level.

### 2. Critical Vulnerabilities (Immediate Action)
Issues that can be exploited to compromise the system, steal data, or cause unauthorized access.

### 3. High Priority (Address Within 30 Days)
Security misconfigurations, missing protections, or vulnerabilities requiring near-term remediation.

### 4. Medium Priority (Address Within 90 Days)
Issues that reduce security posture but have mitigating factors or limited exploitability.

### 5. Low Priority (Next Cycle)
Security improvements, hardening recommendations, and defense-in-depth enhancements.

### 6. Positive Security Observations
Well-implemented security patterns and practices to acknowledge.

### 7. Remediation Roadmap
Prioritized action items with code examples for the most critical fixes.

## Best Practices

- Validate all inputs at the API boundary — never trust client-side validation alone
- Use parameterized queries or ORMs — never concatenate user input into queries
- Store secrets in environment variables or secret managers — never in source code
- Apply the principle of least privilege for database accounts, API keys, and IAM roles
- Enable security headers (helmet.js) and restrict CORS to known origins
- Implement rate limiting on all public-facing endpoints
- Hash passwords with bcrypt or argon2 — never use MD5/SHA for passwords
- Set cookie flags: `HttpOnly`, `Secure`, `SameSite=Strict`
- Use `npm audit` in CI pipelines to catch dependency vulnerabilities
- Log security events (failed logins, permission denials) without logging sensitive data

## Constraints and Warnings

- Security review is not a substitute for professional penetration testing
- Focus on code-level vulnerabilities — infrastructure security is out of scope
- Respect the project's framework — provide framework-specific remediation guidance
- Do not log, print, or expose discovered secrets — report their location only
- Dependency vulnerabilities should be assessed for actual exploitability, not just presence
- Security recommendations must be practical — consider implementation effort vs risk reduction

## References

See the `references/` directory for detailed security documentation:
- `references/owasp-typescript.md` — OWASP Top 10 mapped to TypeScript/Node.js patterns
- `references/common-vulnerabilities.md` — Common vulnerability patterns and remediation
- `references/dependency-security.md` — Dependency scanning and supply chain security guide
