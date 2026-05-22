---
name: security-practices
description: Secure coding with Claude Code - vulnerability prevention, secrets, security review
version: 1.0.0
author: Claude Code SDK
tags: [security, vulnerabilities, secrets, owasp]
---

# Security Practices for Claude Code

A practical guide for writing secure code with Claude Code assistance.

## Quick Reference

### Security Prompts

When asking Claude Code for help, include security context:

```
"Implement user login with proper password hashing, rate limiting, and protection against timing attacks"

"Create an API endpoint that validates all inputs and prevents SQL injection"

"Review this code for security vulnerabilities, focusing on OWASP top 10"
```

### Security Checklist

Before committing any code, verify:

- [ ] No secrets in code (API keys, passwords, tokens)
- [ ] All user inputs validated and sanitized
- [ ] SQL queries use parameterized statements
- [ ] HTML output properly encoded
- [ ] Authentication uses secure patterns
- [ ] Dependencies checked for vulnerabilities
- [ ] Error messages do not leak sensitive info
- [ ] Logging excludes sensitive data

## Core Security Principles

### 1. Never Trust User Input

```typescript
// BAD - Direct use of user input
const query = `SELECT * FROM users WHERE id = ${req.params.id}`;

// GOOD - Parameterized query
const query = db.query('SELECT * FROM users WHERE id = ?', [req.params.id]);
```

### 2. Defense in Depth

Apply multiple security layers:

```typescript
// Layer 1: Input validation
const userId = validateUUID(req.params.id);

// Layer 2: Parameterized query
const user = await db.query('SELECT * FROM users WHERE id = ?', [userId]);

// Layer 3: Authorization check
if (user.organizationId !== req.user.organizationId) {
  throw new ForbiddenError('Access denied');
}

// Layer 4: Output sanitization
return sanitizeUserResponse(user);
```

### 3. Fail Securely

```typescript
// BAD - Reveals internal state
catch (error) {
  res.status(500).json({ error: error.message, stack: error.stack });
}

// GOOD - Generic error to client, detailed logging
catch (error) {
  logger.error('Database error', { error, userId: req.user?.id });
  res.status(500).json({ error: 'An unexpected error occurred' });
}
```

### 4. Principle of Least Privilege

```typescript
// BAD - Broad permissions
const dbConnection = connect({ user: 'root', permissions: 'ALL' });

// GOOD - Minimal required permissions
const dbConnection = connect({
  user: 'app_readonly',
  permissions: ['SELECT'],
  tables: ['public_users', 'public_posts']
});
```

## Injection Prevention

### SQL Injection

```typescript
// Always use parameterized queries
// Drizzle ORM (recommended)
const users = await db.select().from(usersTable).where(eq(usersTable.id, userId));

// Raw SQL with parameters
const result = await db.execute(sql`SELECT * FROM users WHERE id = ${userId}`);

// Prisma
const user = await prisma.user.findUnique({ where: { id: userId } });
```

### Command Injection

```typescript
// BAD - Shell command with user input
exec(`convert ${userFilename} output.png`);

// GOOD - Use arrays to prevent injection
execFile('convert', [userFilename, 'output.png']);

// BETTER - Validate filename first
const safeFilename = path.basename(userFilename).replace(/[^a-zA-Z0-9._-]/g, '');
execFile('convert', [safeFilename, 'output.png']);
```

### XSS Prevention

```typescript
// React auto-escapes by default
return <div>{userContent}</div>;  // Safe

// Dangerous - avoid unless absolutely necessary
return <div dangerouslySetInnerHTML={{ __html: sanitizedHtml }} />;

// If you must render HTML, use DOMPurify
import DOMPurify from 'dompurify';
const clean = DOMPurify.sanitize(userHtml);
```

## Authentication Patterns

### Password Hashing

```typescript
import { hash, verify } from '@node-rs/argon2';

// Hash password on registration
const hashedPassword = await hash(password, {
  memoryCost: 65536,
  timeCost: 3,
  parallelism: 4,
});

// Verify on login
const isValid = await verify(storedHash, providedPassword);
```

### Session Management

```typescript
// Generate secure session tokens
import { randomBytes } from 'crypto';
const sessionToken = randomBytes(32).toString('base64url');

// Store with secure cookie settings
res.cookie('session', sessionToken, {
  httpOnly: true,      // Prevents XSS access
  secure: true,        // HTTPS only
  sameSite: 'strict',  // CSRF protection
  maxAge: 3600000,     // 1 hour
  path: '/',
});
```

### JWT Best Practices

```typescript
import jwt from 'jsonwebtoken';

// Sign with appropriate algorithm
const token = jwt.sign(
  { userId: user.id, role: user.role },
  process.env.JWT_SECRET,
  {
    algorithm: 'HS256',
    expiresIn: '1h',
    issuer: 'your-app',
    audience: 'your-api',
  }
);

// Verify with all options
const decoded = jwt.verify(token, process.env.JWT_SECRET, {
  algorithms: ['HS256'],  // Prevent algorithm confusion
  issuer: 'your-app',
  audience: 'your-api',
});
```

## Secret Management

### Environment Variables

```bash
# .env.example (commit this)
DATABASE_URL=postgresql://user:password@localhost:5432/db
JWT_SECRET=your-secret-here

# .env (NEVER commit)
DATABASE_URL=postgresql://prod_user:actual_password@prod-host:5432/prod_db
JWT_SECRET=actual-secret-value
```

### Git Protection

```gitignore
# .gitignore - Always include
.env
.env.local
.env.*.local
*.pem
*.key
credentials.json
secrets/
```

### Pre-commit Hook

```bash
#!/bin/bash
# .husky/pre-commit

# Check for potential secrets
if git diff --cached --name-only | xargs grep -l -E "(password|secret|api_key|private_key)\s*[:=]" 2>/dev/null; then
  echo "ERROR: Potential secret detected in staged files"
  exit 1
fi
```

See [SECRET-MANAGEMENT.md](./SECRET-MANAGEMENT.md) for comprehensive secret handling.

## Input Validation

### Schema Validation with Zod

```typescript
import { z } from 'zod';

const UserInputSchema = z.object({
  email: z.string().email().max(255),
  username: z.string()
    .min(3)
    .max(30)
    .regex(/^[a-zA-Z0-9_]+$/, 'Alphanumeric and underscore only'),
  age: z.number().int().min(13).max(120),
});

// Validate before processing
const result = UserInputSchema.safeParse(req.body);
if (!result.success) {
  return res.status(400).json({ errors: result.error.flatten() });
}
const validatedData = result.data;
```

### File Upload Validation

```typescript
const ALLOWED_TYPES = ['image/jpeg', 'image/png', 'image/webp'];
const MAX_SIZE = 5 * 1024 * 1024; // 5MB

function validateUpload(file: File): void {
  // Check MIME type (also verify magic bytes for production)
  if (!ALLOWED_TYPES.includes(file.type)) {
    throw new ValidationError('Invalid file type');
  }

  // Check size
  if (file.size > MAX_SIZE) {
    throw new ValidationError('File too large');
  }

  // Sanitize filename
  const safeName = file.name
    .replace(/[^a-zA-Z0-9._-]/g, '')
    .substring(0, 100);
}
```

## Dependency Security

### Check for Vulnerabilities

```bash
# Bun
bun audit

# npm
npm audit

# Check specific package
npx is-my-node-vulnerable

# Snyk (more comprehensive)
npx snyk test
```

### Keep Dependencies Updated

```bash
# Check for updates
bun outdated

# Update to latest (review changes first)
bun update

# Update specific security-critical packages
bun update package-name@latest
```

## Security Review Prompts

Ask Claude Code to review with specific focus:

```
"Review this authentication code for:
1. Password storage security
2. Timing attack vulnerabilities
3. Session management issues
4. Rate limiting gaps"

"Check this API endpoint for OWASP Top 10 vulnerabilities"

"Audit this code for sensitive data exposure in logs or errors"
```

See [REVIEW-SECURITY.md](./REVIEW-SECURITY.md) for detailed review patterns.

## Quick Fixes for Common Issues

### Exposed Secrets in Git History

```bash
# Remove file from history (use with caution)
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch path/to/secret-file" \
  --prune-empty --tag-name-filter cat -- --all

# Rotate all exposed credentials immediately
# Force push to all remotes
git push origin --force --all
```

### Add Security Headers

```typescript
// Express middleware
app.use((req, res, next) => {
  res.setHeader('X-Content-Type-Options', 'nosniff');
  res.setHeader('X-Frame-Options', 'DENY');
  res.setHeader('X-XSS-Protection', '1; mode=block');
  res.setHeader('Strict-Transport-Security', 'max-age=31536000; includeSubDomains');
  res.setHeader('Content-Security-Policy', "default-src 'self'");
  next();
});
```

### Rate Limiting

```typescript
import rateLimit from 'express-rate-limit';

const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 5, // 5 attempts
  message: 'Too many login attempts, please try again later',
  standardHeaders: true,
  legacyHeaders: false,
});

app.post('/login', authLimiter, loginHandler);
```

## Related Files

- [VULNERABILITY-PREVENTION.md](./VULNERABILITY-PREVENTION.md) - OWASP Top 10 and common vulnerabilities
- [SECRET-MANAGEMENT.md](./SECRET-MANAGEMENT.md) - Comprehensive secret handling
- [REVIEW-SECURITY.md](./REVIEW-SECURITY.md) - Security code review patterns

## Resources

- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/)
- [CWE Top 25](https://cwe.mitre.org/top25/)
- [Node.js Security Best Practices](https://nodejs.org/en/docs/guides/security/)
