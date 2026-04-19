---
name: security
description: Security audit workflow - OWASP Top 10, input validation, auth, secret detection, vulnerability scan
---

# Security Patterns

## OWASP Top 10 (2021) Checklist

| # | Vulnerability | Prevention |
|---|--------------|------------|
| A01 | Broken Access Control | RBAC, resource-level auth, CORS |
| A02 | Cryptographic Failures | Encrypt at rest/transit, no PII in logs |
| A03 | Injection (SQL/NoSQL/XSS/OS) | Parameterized queries, output encoding, CSP |
| A04 | Insecure Design | Threat modeling, secure design patterns |
| A05 | Security Misconfiguration | Hardened defaults, no debug in prod |
| A06 | Vulnerable Components | npm audit, dependency scan, CVE tracking |
| A07 | Auth Failures | Rate limiting, MFA, secure session |
| A08 | Data Integrity Failures | Input validation, signed updates, CI/CD security |
| A09 | Logging & Monitoring Failures | Audit log, alert on anomaly |
| A10 | SSRF | URL allowlist, network segmentation |

## Input Validation

```typescript
import { z } from 'zod';

const UserInput = z.object({
  email: z.string().email().max(255),
  name: z.string().min(1).max(100).regex(/^[\w\s-]+$/),
  age: z.number().int().min(0).max(150),
});

// Parameterized query (SQL injection prevention)
const user = await db.query('SELECT * FROM users WHERE id = $1', [userId]);
```

## Auth Best Practices

```typescript
// Password hashing
import bcrypt from 'bcryptjs';
const hash = await bcrypt.hash(password, 12);
const valid = await bcrypt.compare(password, hash);

// JWT with expiry
const token = jwt.sign({ userId: user.id, role: user.role }, secret, { expiresIn: '24h' });

// Rate limiting on auth endpoints
const authLimiter = rateLimit({ windowMs: 15 * 60 * 1000, max: 5 });
app.use('/api/auth', authLimiter);
```

## Secret Detection

```bash
# Git hooks ile secret engelleme
grep -rn "sk-\|pk_\|ghp_\|xoxb-\|AKIA" --include="*.ts" --include="*.js" src/
grep -rn "password\s*=\s*['\"]" --include="*.ts" src/
```

## Security Headers

```typescript
import helmet from 'helmet';
app.use(helmet());
// Content-Security-Policy, X-Frame-Options, X-Content-Type-Options, etc.
```

## Anti-Patterns

| Anti-Pattern | Cozum |
|-------------|-------|
| Hardcoded secrets | Environment variables |
| SQL string concat | Parameterized queries |
| No CORS config | Whitelist origins |
| Debug mode in prod | NODE_ENV check |
| No rate limiting | express-rate-limit |

## Pentest Methodology (Overview)

Detayli rehber icin: `pentest-methodology` skill

5-faz pipeline: Recon > Vuln Analysis > Exploitation > Verification > Report

### Proof Levels

| Level | Tanim |
|-------|-------|
| L1 - Theoretical | Potansiyel risk, exploit edilmemis |
| L2 - Demonstrated | Bypass/leak gosterildi |
| L3 - Exploited | Tam exploit, veri erisimi |
| L4 - Chained | Birden fazla vuln zincirlendi |

### Source-to-Sink Taint Tracing

Kullanici input'unun (source) tehlikeli fonksiyona (sink) ulasip ulasamadigini kontrol et:

```
Source: req.body, req.query, req.params, req.headers, cookies
Sink: db.query(), eval(), exec(), res.redirect(), innerHTML

Kontrol: Source ile Sink arasinda sanitizasyon/validasyon var mi?
```

Bu yaklasimi her code review'da auth/data islerinde kullan.
