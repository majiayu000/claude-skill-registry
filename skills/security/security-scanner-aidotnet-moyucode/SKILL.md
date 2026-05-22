---
name: security-scanner
description: 全面的安全分析，识别OWASP Top 10漏洞、检测硬编码密钥和审查安全配置。
metadata:
  short-description: 扫描代码安全漏洞
---

# Security Scanner Skill

## Description
Perform security-focused code analysis to identify vulnerabilities and security issues.

## Trigger
- `/security` command
- User requests security review
- User asks about vulnerabilities

## Prompt

You are a security expert that identifies vulnerabilities and recommends fixes.

### SQL Injection Prevention

```typescript
// ❌ VULNERABLE: SQL Injection
const query = `SELECT * FROM users WHERE email = '${email}'`;

// ✅ SAFE: Parameterized query
const query = 'SELECT * FROM users WHERE email = $1';
const result = await db.query(query, [email]);

// ✅ SAFE: Using ORM
const user = await prisma.user.findUnique({ where: { email } });
```

### XSS Prevention

```typescript
// ❌ VULNERABLE: XSS in React (rare but possible)
<div dangerouslySetInnerHTML={{ __html: userInput }} />

// ✅ SAFE: Sanitize HTML
import DOMPurify from 'dompurify';
<div dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(userInput) }} />

// ✅ SAFE: Use text content (React auto-escapes)
<div>{userInput}</div>
```

### Authentication Security

```typescript
// ❌ BAD: Weak password hashing
const hash = crypto.createHash('md5').update(password).digest('hex');

// ✅ GOOD: Strong password hashing
import bcrypt from 'bcrypt';
const hash = await bcrypt.hash(password, 12);
const isValid = await bcrypt.compare(password, hash);

// ✅ GOOD: JWT with proper configuration
import jwt from 'jsonwebtoken';
const token = jwt.sign(
  { userId: user.id },
  process.env.JWT_SECRET!,
  { expiresIn: '1h', algorithm: 'HS256' }
);
```

### Secret Detection Patterns

```typescript
// ❌ DETECTED: Hardcoded secrets
const API_KEY = 'sk-1234567890abcdef';
const password = 'admin123';
const awsSecret = 'AKIAIOSFODNN7EXAMPLE';

// ✅ SAFE: Environment variables
const API_KEY = process.env.API_KEY;
const password = process.env.DB_PASSWORD;
```

### Security Headers (Express)

```typescript
import helmet from 'helmet';

app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      scriptSrc: ["'self'", "'unsafe-inline'"],
      styleSrc: ["'self'", "'unsafe-inline'"],
      imgSrc: ["'self'", "data:", "https:"],
    },
  },
  hsts: { maxAge: 31536000, includeSubDomains: true },
  noSniff: true,
  referrerPolicy: { policy: 'strict-origin-when-cross-origin' },
}));

// CORS configuration
app.use(cors({
  origin: ['https://myapp.com'],
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
}));
```

### Input Validation

```typescript
import { z } from 'zod';

const CreateUserSchema = z.object({
  email: z.string().email().max(255),
  password: z.string().min(8).max(100),
  name: z.string().min(1).max(100).regex(/^[a-zA-Z\s]+$/),
});

// Validate input
const validated = CreateUserSchema.parse(req.body);
```

## Tags
`security`, `vulnerability`, `owasp`, `scanning`, `compliance`

## Compatibility
- Codex: ✅
- Claude Code: ✅
