---
name: owasp-top-10-prevention
description: >
  Prevent OWASP Top 10 vulnerabilities in web applications. Activate whenever the user
  writes API endpoints, form handlers, database queries, authentication logic, file uploads,
  HTML rendering, or any code that handles user input or external data. Also activate when
  the user asks about security, hardening, or vulnerability prevention.
---

# OWASP Top 10 Prevention

Prevent the most critical web application security risks by applying proven defensive
patterns. This skill covers injection, XSS, CSRF, SSRF, broken authentication, security
headers, insecure deserialization, and IDOR vulnerabilities.

## When to Use
- Writing or reviewing API endpoints that accept user input
- Building authentication or authorization logic
- Rendering user-generated content in HTML
- Making server-side HTTP requests based on user input
- Writing database queries with dynamic parameters
- Handling file uploads or downloads
- Setting up HTTP response headers

## Core Patterns

### SQL Injection Prevention

Never concatenate user input into SQL queries. Always use parameterized queries or an ORM.

```typescript
// WRONG: SQL injection vulnerability
const query = `SELECT * FROM users WHERE email = '${email}'`;
await db.query(query);

// CORRECT: Parameterized query
const query = 'SELECT * FROM users WHERE email = $1';
await db.query(query, [email]);

// CORRECT: Using an ORM (Prisma)
const user = await prisma.user.findUnique({
  where: { email },
});
```

### XSS Prevention

Sanitize all user-generated content before rendering. Use framework-provided escaping.

```typescript
// WRONG: Direct HTML insertion
element.innerHTML = userComment;

// CORRECT: Use textContent for plain text
element.textContent = userComment;

// CORRECT: Sanitize HTML when rich text is needed
import DOMPurify from 'dompurify';
element.innerHTML = DOMPurify.sanitize(userComment);

// CORRECT: React auto-escapes by default, but avoid dangerouslySetInnerHTML
function Comment({ text }: { text: string }) {
  return <p>{text}</p>; // Auto-escaped
}
```

### CSRF Protection

Validate origin and use anti-CSRF tokens for state-changing requests.

```typescript
// Express middleware for CSRF protection
import csrf from 'csurf';

const csrfProtection = csrf({ cookie: true });
app.use(csrfProtection);

app.post('/api/transfer', csrfProtection, (req, res) => {
  // Token automatically validated by middleware
  processTransfer(req.body);
});

// Also validate Origin header
function validateOrigin(req: Request): boolean {
  const origin = req.headers.origin;
  const allowedOrigins = [process.env.FRONTEND_URL];
  return allowedOrigins.includes(origin);
}
```

### SSRF Prevention

Never allow user input to control server-side HTTP request destinations without validation.

```typescript
// WRONG: User controls the URL
app.get('/proxy', async (req, res) => {
  const response = await fetch(req.query.url as string);
  res.send(await response.text());
});

// CORRECT: Allowlist of permitted domains
const ALLOWED_HOSTS = new Set(['api.example.com', 'cdn.example.com']);

app.get('/proxy', async (req, res) => {
  const url = new URL(req.query.url as string);
  if (!ALLOWED_HOSTS.has(url.hostname)) {
    return res.status(403).json({ error: 'Domain not allowed' });
  }
  if (url.protocol !== 'https:') {
    return res.status(403).json({ error: 'HTTPS required' });
  }
  const response = await fetch(url.toString());
  res.send(await response.text());
});
```

### Broken Authentication Prevention

Use secure session management, strong password hashing, and rate limiting.

```typescript
import bcrypt from 'bcrypt';
import rateLimit from 'express-rate-limit';

// Hash passwords with sufficient rounds
const SALT_ROUNDS = 12;
const hashedPassword = await bcrypt.hash(password, SALT_ROUNDS);

// Rate limit login attempts
const loginLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 5,
  message: 'Too many login attempts, try again later',
});
app.post('/api/login', loginLimiter, loginHandler);

// Secure session configuration
app.use(session({
  secret: process.env.SESSION_SECRET,
  resave: false,
  saveUninitialized: false,
  cookie: {
    secure: true,
    httpOnly: true,
    sameSite: 'strict',
    maxAge: 3600000,
  },
}));
```

### Security Headers

Set proper HTTP headers to prevent common attacks.

```typescript
import helmet from 'helmet';

app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      scriptSrc: ["'self'"],
      styleSrc: ["'self'", "'unsafe-inline'"],
      imgSrc: ["'self'", "data:", "https:"],
    },
  },
  hsts: { maxAge: 31536000, includeSubDomains: true },
  referrerPolicy: { policy: 'strict-origin-when-cross-origin' },
}));
```

### IDOR Prevention

Always verify the requesting user has access to the requested resource.

```typescript
// WRONG: No authorization check
app.get('/api/orders/:id', async (req, res) => {
  const order = await db.orders.findById(req.params.id);
  res.json(order);
});

// CORRECT: Verify ownership
app.get('/api/orders/:id', authenticate, async (req, res) => {
  const order = await db.orders.findById(req.params.id);
  if (!order) {
    return res.status(404).json({ error: 'Not found' });
  }
  if (order.userId !== req.user.id) {
    return res.status(403).json({ error: 'Forbidden' });
  }
  res.json(order);
});
```

## Anti-Patterns
- Using `eval()`, `new Function()`, or template literals for SQL/HTML construction
- Storing passwords in plaintext or with weak hashing (MD5, SHA1)
- Trusting client-side validation as the sole defense
- Returning different error messages for "user not found" vs "wrong password" (enables enumeration)
- Disabling CORS entirely with `Access-Control-Allow-Origin: *` on authenticated endpoints
- Logging sensitive data (passwords, tokens, PII) in application logs

## Quick Reference

| Vulnerability | Defense |
|--------------|---------|
| SQL Injection | Parameterized queries, ORM |
| XSS | Output encoding, CSP, DOMPurify |
| CSRF | Anti-CSRF tokens, SameSite cookies |
| SSRF | URL allowlisting, block internal IPs |
| Broken Auth | bcrypt, rate limiting, secure sessions |
| Security Headers | helmet middleware, strict CSP |
| IDOR | Authorization checks on every resource access |
| Deserialization | Validate/schema-check before deserializing, avoid native deserialization of untrusted data |
