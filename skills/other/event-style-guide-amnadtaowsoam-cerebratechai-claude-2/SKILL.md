---
name: Event Style Guide
description: Event-driven design conventions: event envelope, naming, versioning, schema evolution rules, idempotency, ordering/partitioning, retry and dead-letter handling
---

# Event Style Guide

## Overview

มาตรฐานการออกแบบ events สำหรับ event-driven architecture: envelope format, naming, versioning, และ schema evolution ที่ทำให้ระบบ decouple ได้อย่างปลอดภัย

## Why This Matters

- **Interoperability**: ทุก service เข้าใจ event format เดียวกัน
- **Evolution**: เปลี่ยน schema โดยไม่ break consumers
- **Debugging**: Trace events ข้าม services ได้
- **Contract**: Clear agreement between producers/consumers

---

## Core Concepts

### 1. Event Envelope Structure

- ทุก event ต้องเป็น envelope เดียวกัน เพื่อให้ tooling/observability ทำงานได้
- metadata ต้องมี `id`, `type`, `source`, `time`, `specVersion`
- correlation ต้องมี `correlationId` (ผูกกับ request/trace) และ `causationId` (optional)
- payload อยู่ใน `data` เท่านั้น (หลีกเลี่ยง “metadata ปน payload”)

### 2. Event Naming Convention

- รูปแบบ: `<domain>.<entity>.<action>.v<major>`
- ใช้ past-tense สำหรับ domain events (`created`, `updated`, `completed`)
- actions ต้องสื่อความหมายและไม่กว้างเกินไป (หลีกเลี่ยง `changed`, `processed` ถ้าไม่จำเป็น)

### 3. Event Versioning

- version ใน `type` เป็น **major** เพื่อบอก breaking changes: `user.created.v1`
- changes แบบ non-breaking (เพิ่ม field optional) ไม่ต้อง bump major แต่ควร track schema version ใน registry
- หากต้อง breaking: ออก `v2` และรองรับ consumers เก่าในช่วง deprecation

### 4. Schema Evolution

กฎหลัก: consumers ต้อง “ignore unknown fields” และ producers ต้องไม่ลบ/เปลี่ยนความหมาย field เดิมภายใน major เดียวกัน

- ✅ เพิ่ม field optional (หรือเพิ่ม enum values แบบ backward-compatible ถ้า consumers handle unknown)
- ❌ ลบ field, rename field, เปลี่ยน type, เพิ่ม required field
- ถ้าจำเป็นต้อง rename: ทำแบบ “add new + deprecate old” แล้วค่อยตัดใน major ถัดไป

### 5. Event Types

- **Domain events**: facts ที่เกิดขึ้นแล้ว (source-of-truth) เช่น `order.payment.completed.v1`
- **Integration events**: แปล domain event สำหรับระบบอื่น/ภายนอก (อาจ mask/redact fields)
- **Commands**: “ขอให้ทำ” (ควรเป็น request/response หรือ separate channel) ไม่ควรปนกับ domain events

### 6. Idempotency

- `id` ต้อง unique (UUID v4) และใช้สำหรับ dedupe ที่ consumer
- consumer ต้อง idempotent: บันทึก `eventId` ที่ process แล้ว หรือใช้ upsert/deterministic state transitions
- ถ้า broker อาจส่งซ้ำ (at-least-once) ให้คาดไว้ตั้งแต่แรก

### 7. Event Ordering

- ถ้าต้องการ ordering ให้ define partition key (เช่น `tenantId`, `orderId`) และส่งไป partition เดียวกัน
- ถ้าต้อง strict ordering ต่อ entity ให้มี `sequence` (optional) ใน `data` หรือ `details`
- หลีกเลี่ยงการพึ่ง ordering ข้าม partition (แทบไม่รับประกัน)

### 8. Dead Letter Handling

- define retry policy: exponential backoff + jitter + max attempts
- classify errors: retryable vs non-retryable (validation/domain errors ไม่ควร retry)
- เมื่อเกิน max retries ให้ส่ง DLQ พร้อม metadata ที่พอสำหรับ replay (แต่ไม่ใส่ secrets/PII เกินจำเป็น)
- ต้องมี playbook: “inspect → fix → replay”

## Quick Start

```typescript
export interface EventEnvelope<T> {
  id: string;
  type: string;
  source: string;
  specVersion: "1.0";
  time: string;

  correlationId: string;
  causationId?: string;

  dataContentType: "application/json";
  dataSchema?: string;
  data: T;
}

export type UserCreatedV1 = EventEnvelope<{
  userId: string;
  email: string;
  tenantId: string;
}>;
```

## Production Checklist

- [ ] All events follow envelope standard
- [ ] Event naming consistent
- [ ] Version in every event
- [ ] Schema registered in registry
- [ ] Idempotency keys present
- [ ] Dead letter queue configured

## Event Envelope Standard

```typescript
interface EventEnvelope<T> {
  // Metadata
  id: string;                    // UUID v4
  type: string;                  // "user.created.v1"
  source: string;                // "user-service"
  specVersion: string;           // "1.0"
  time: string;                  // ISO 8601

  // Correlation
  correlationId: string;         // Request correlation
  causationId?: string;          // Causing event ID

  // Payload
  data: T;                       // Event-specific data
  dataContentType: string;       // "application/json"
  dataSchema?: string;           // Schema URL
}
```

## Retry & DLQ Policy (ตัวอย่าง)

- retry: 1s, 5s, 15s, 1m, 5m (max 5 ครั้ง) + jitter
- non-retryable: `VAL_`, `BIZ_`, `AUTH_`, `AUTHZ_` (ส่ง DLQ ทันทีหรือ discard ตาม policy)
- DLQ message ต้องมี: original `event.id`, `event.type`, error summary, attempt count, first/last seen timestamp

## Event Naming Convention

```
# Format: <domain>.<entity>.<action>.v<version>

# Examples:
user.account.created.v1
order.payment.completed.v1
inventory.stock.reserved.v1
notification.email.sent.v1

# Actions (past tense for domain events):
- created, updated, deleted
- completed, failed, cancelled
- started, finished, expired
```

## Schema Evolution Rules

| Change Type | Compatibility | Example |
|-------------|---------------|---------|
| Add optional field | ✅ Safe | Add `middleName?: string` |
| Add required field | ❌ Breaking | Add `email: string` |
| Remove field | ❌ Breaking | Remove `age` |
| Rename field | ❌ Breaking | `name` → `fullName` |
| Change type | ❌ Breaking | `age: string` → `age: number` |

## Anti-patterns

1. **No versioning**: Can't evolve schemas
2. **Massive payloads**: Events too large
3. **Missing correlation**: Can't trace flows
4. **Shared events**: Tight coupling between services
5. **Hidden contracts**: schema อยู่ใน code แต่ไม่มี registry/docs

## Integration Points

- Message brokers (Kafka, RabbitMQ)
- Schema registries
- Event stores
- Monitoring systems

## Further Reading

- [CloudEvents Specification](https://cloudevents.io/)
- [Event-Driven Architecture Patterns](https://www.confluent.io/blog/)
- [Schema Evolution Best Practices](https://docs.confluent.io/platform/current/schema-registry/)
