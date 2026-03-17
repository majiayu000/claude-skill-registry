---
name: Security Baseline Controls
description: Minimum security controls every service must implement: authentication/authorization, input validation, secrets management, security headers, dependency security, audit logging, and operational guardrails
---

# Security Baseline Controls

## Overview

Minimum security controls every service must implement: authentication, authorization, input validation, secrets handling, and security headers that make the system secure from day one.

## Why This Matters

- **Compliance**: Meet SOC2, ISO27001, GDPR requirements
- **Defense in depth**: Multiple security layers
- **Consistency**: Same security posture across services
- **Audit**: Clear evidence of controls

---

## Core Concepts

### 1. Authentication Requirements

- ทุก endpoint (ยกเว้น health) ต้องมี authentication
- validate tokens อย่างถูกต้อง: signature, issuer, audience, expiry, clock skew
- สำหรับ sessions ต้องมี: secure cookie, CSRF protection, session rotation

### 2. Authorization Patterns

- resource-level authorization (owner/tenant) เป็น default
- RBAC สำหรับ roles ทั่วไป, ABAC/policies สำหรับเงื่อนไขซับซ้อน (tenant tier, attributes)
- deny-by-default: ถ้าไม่มี policy/permission ให้ reject

### 3. Input Validation

- validate ที่ boundary: request body/query/path headers (schema-based)
- enforce limits: max size, max length, enums, number ranges
- normalize/sanitize ตามชนิดข้อมูล (เช่น trim, canonicalize emails)

### 4. Output Encoding

- ตั้ง `Content-Type` ถูกต้องเสมอ และใช้ JSON serialization มาตรฐาน
- UI ที่ render HTML ต้อง escape/encode ตาม context (server ไม่ควรส่ง HTML ที่มี user input โดยตรง)
- หลีกเลี่ยงการสะท้อน input กลับไปใน error message โดยไม่ sanitize

### 5. Secrets Management

- secrets ต้องไม่อยู่ใน repo, container image, หรือ logs
- ใช้ secret manager + least privilege access (scoped identities)
- รองรับ rotation: short TTL tokens, reload without redeploy ถ้าเป็นไปได้

### 6. Security Headers

- เปิดใช้ HSTS บน production domains ที่รองรับ HTTPS
- ใส่ CSP ที่เหมาะสม (สำหรับ web apps) และปิด clickjacking (`X-Frame-Options`/`frame-ancestors`)
- ตั้ง `Referrer-Policy`, `X-Content-Type-Options` เป็น baseline

### 7. Dependency Security

- เปิดใช้ dependency scanning ใน CI (SCA) และกำหนด SLA ในการ patch
- pin versions และหลีกเลี่ยง `latest` ใน production
- สำหรับ containers: scan base image + SBOM ถ้า platform รองรับ

### 8. Audit Logging

- log security-relevant events: login, token refresh, permission changes, admin actions, data export
- audit logs ต้อง immutable/append-only และเข้าถึงจำกัด
- ใส่ `requestId`/`actorId`/`tenantId` (ถ้ามี) และ redact PII ตาม policy

## Quick Start

```typescript
import helmet from "helmet";
import type { Request, Response, NextFunction } from "express";

export function securityHeaders() {
  return helmet({
    contentSecurityPolicy: false, // enable + tune per app (web) when ready
  });
}

export function requireAuth(req: Request, res: Response, next: NextFunction) {
  const auth = req.header("authorization");
  if (!auth?.startsWith("Bearer ")) return res.status(401).json({ error: "Unauthorized" });
  // verify token (issuer/audience/signature/expiry) here
  next();
}
```

## Production Checklist

- [ ] Authentication on all endpoints (except health)
- [ ] Authorization checks for protected resources
- [ ] Input validation on all user inputs
- [ ] Security headers configured
- [ ] Secrets from secret manager (not env/code)
- [ ] Dependencies scanned for vulnerabilities
- [ ] Security audit logging enabled

## Security Headers

```typescript
// Required headers
{
  "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
  "X-Content-Type-Options": "nosniff",
  "X-Frame-Options": "DENY",
  "X-XSS-Protection": "1; mode=block",
  "Content-Security-Policy": "default-src 'self'",
  "Referrer-Policy": "strict-origin-when-cross-origin"
}
```

## Input Validation Checklist

```typescript
// Every user input must be:
// 1. Type-checked (string, number, etc.)
// 2. Length-limited (max characters)
// 3. Format-validated (regex, enum)
// 4. Sanitized (HTML escape, SQL escape)

const schema = z.object({
  email: z.string().email().max(255),
  name: z.string().min(1).max(100),
  age: z.number().int().min(0).max(150)
});
```

## Authentication Requirements

| Endpoint Type | Auth Required | Notes |
|---------------|---------------|-------|
| Health check | No | `/health`, `/ready` |
| Metrics | Optional | Depends on exposure |
| Public API | Yes | Bearer token |
| Internal API | Yes | Service-to-service auth |
| Admin API | Yes | Additional MFA |

## Anti-patterns

1. **Security as afterthought**: Add security later
2. **Trust internal traffic**: No service-to-service auth
3. **Log everything**: Including secrets
4. **Ignore dependencies**: Old vulnerable packages
5. **Over-logging**: log PII/credentials แล้วค่อย “ลบทีหลัง” (ทำไม่ได้จริง)

## Integration Points

- Identity providers
- Secret managers
- Security scanning tools
- SIEM systems

## Further Reading

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/)
- [Security Headers](https://securityheaders.com/)
