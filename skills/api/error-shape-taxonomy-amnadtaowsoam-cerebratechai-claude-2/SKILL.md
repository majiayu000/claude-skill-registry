---
name: Error Shape Taxonomy
description: Standard error response taxonomy and envelope for services, including error codes, categories, retryability, correlation IDs, safe messaging, and validation error details
---

# Error Shape Taxonomy

## Overview

มาตรฐาน error response format ที่ใช้ทั้งองค์กร ครอบคลุม error codes, categories, และ structure ที่ทำให้ client และ monitoring tools เข้าใจ error ได้ทันที

## Why This Matters

- **Debuggability**: รู้ทันทีว่า error มาจากไหน ทำไม
- **Client handling**: Frontend/mobile handle errors ได้ถูกต้อง
- **Monitoring**: Alert และ dashboard แยก error types ได้
- **Documentation**: Error catalog ที่ reference ได้

---

## Core Concepts

### 1. Error Envelope Structure

- แนะนำให้ยึดแนวคิด RFC 7807 (problem details) แต่ให้คงโครงเดียวกันทั้งองค์กร
- ต้องมี: `code`, `message`, `requestId`, `timestamp`, `status`
- ถ้าเป็น retryable ให้มี `retryable` และ `retryAfterSeconds` (ถ้ามี)

### 2. Error Code System

- `PREFIX_###` หรือ `PREFIX_SUB_###` (อ่านง่าย, stable)
- code ต้อง **คงที่** (ห้ามเปลี่ยนความหมาย) และต้อง document ใน catalog
- หลีกเลี่ยงใช้ HTTP status เป็น code (เช่น `ERR_500`) เพราะไม่สื่อสาเหตุ

### 3. Error Categories

กำหนดหมวดให้ชัดเพื่อ routing/alert:

- `AUTH_` / `AUTHZ_`: authn/authz
- `VAL_`: validation / malformed requests
- `BIZ_`: business/domain rules
- `RATE_`: rate limiting / quotas
- `SYS_`: infra/system dependencies (DB, queue, upstream)

### 4. Error Messages

- `message` ต้องเป็น **user-safe** (ไม่เปิดเผย stacktrace/SQL/secret)
- รายละเอียดเชิงเทคนิคให้ใส่ใน `details` (และต้อง scrub PII/secret)
- ถ้าต้องการข้อความที่ UI แสดง ให้มี `userMessage` แยก (optional) และรองรับ i18n

### 5. Error Context

- ทุก error ต้องมี `requestId` (correlation) และควรมี `traceId` ถ้ามี tracing
- `path` และ `method` ช่วย debug ได้เร็ว (optional)
- stacktrace ห้ามส่งกลับ client; ให้เก็บใน logs เท่านั้น

### 6. Localization

- ถ้ารองรับหลายภาษา: client ใช้ `Accept-Language` และ server map เป็น `userMessage`
- ไม่ควร encode ภาษาไว้ใน `code` (code ควรเป็นภาษากลาง)

### 7. Error Mapping

- map internal errors → external errors แบบ deterministic และทดสอบได้
- errors จาก upstream ต้อง normalize เข้าสู่ shape มาตรฐานของเรา
- `status` ต้องสะท้อน semantics (เช่น `VAL_` ส่วนใหญ่เป็น `400/422`)

### 8. Error Documentation

- มี “error catalog” ต่อ service หรือองค์กร: `code`, `status`, `meaning`, `client action`, `retryable`
- ใช้เป็นแหล่งข้อมูลสำหรับ client SDK, docs, และ alert routing

## Quick Start

```typescript
export type ErrorCategory = "AUTH" | "AUTHZ" | "VAL" | "BIZ" | "RATE" | "SYS";

export interface ErrorResponse {
  error: {
    code: string;
    category: ErrorCategory;
    message: string;
    status: number;
    requestId: string;
    timestamp: string;
    path?: string;
    method?: string;
    retryable?: boolean;
    retryAfterSeconds?: number;
    details?: Record<string, unknown>;
    validationErrors?: Array<{ field: string; reason: string }>;
  };
}
```

## Production Checklist

- [ ] All errors follow standard shape
- [ ] Error codes documented in catalog
- [ ] User-safe messages (no sensitive data)
- [ ] Request ID included in all errors
- [ ] Error logging consistent

## Standard Error Shape

```typescript
// Example payload (VAL_)
// {
//   "error": {
//     "code": "VAL_001",
//     "category": "VAL",
//     "message": "Invalid request",
//     "status": 422,
//     "requestId": "req-789",
//     "timestamp": "2024-01-15T10:00:00Z",
//     "validationErrors": [
//       { "field": "email", "reason": "Invalid email format" }
//     ]
//   }
// }
```

## Error Code Taxonomy

| Prefix | Category | Example |
|--------|----------|---------|
| AUTH_  | Authentication | AUTH_001 Token expired |
| AUTHZ_ | Authorization | AUTHZ_001 Permission denied |
| VAL_   | Validation | VAL_001 Invalid email format |
| BIZ_   | Business logic | BIZ_001 Insufficient balance |
| SYS_   | System | SYS_001 Database unavailable |
| RATE_  | Rate limiting | RATE_001 Too many requests |

## Status + Retryability Guidelines

- `401/403`: ไม่ควร retry แบบอัตโนมัติ (ต้องแก้ credential/permission)
- `400/422`: ไม่ควร retry (ต้องแก้ request)
- `409`: retry ได้ในบางกรณี (ใช้ backoff) ถ้าเป็น conflict ชั่วคราว
- `429`: retry ได้ โดยใช้ `Retry-After`
- `503/504`: retry ได้ (bounded retries + jitter)

## Anti-patterns

1. **Generic errors**: "Something went wrong"
2. **Leaking internals**: Stack traces to client
3. **Inconsistent shape**: Different format per service
4. **Missing correlation**: No request ID
5. **Changing meaning**: เปลี่ยน semantics ของ code เดิม ทำให้ client/alert พัง

## Integration Points

- API gateways (error transformation)
- Frontend error boundaries
- Monitoring/alerting
- Documentation generators

## Further Reading

- [RFC 7807 Problem Details](https://datatracker.ietf.org/doc/html/rfc7807)
- [API Error Handling Best Practices](https://apisyouwonthate.com/blog/creating-good-api-errors-in-rest-graphql-and-grpc)
