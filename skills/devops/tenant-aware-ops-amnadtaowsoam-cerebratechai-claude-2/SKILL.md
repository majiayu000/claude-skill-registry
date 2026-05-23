---
name: Tenant-Aware Ops
description: Operational patterns for multi-tenant systems: tenant-safe debugging and monitoring, per-tenant maintenance and migrations, fairness controls, and compliance-aware access
---

# Tenant-Aware Ops

## Overview

วิธีการทำ operations (debugging, monitoring, maintenance) ใน multi-tenant environment โดยไม่กระทบ tenants อื่น และมี visibility per tenant

## Why This Matters

- **Isolation**: แก้ปัญหา tenant หนึ่งไม่กระทบอื่น
- **Visibility**: Debug per tenant ได้
- **Fairness**: ป้องกัน noisy neighbor
- **Compliance**: Data access per tenant

---

## Core Concepts

### 1. Tenant Context Propagation

- ทุก request/job/event ต้องมี `tenantId` ใน context (ไม่ใช่แค่ใน UI)
- propagate ไป logs/traces และใช้สำหรับ authz + data scoping
- อ้างอิง: `62-scale-operations/multi-tenancy-saas/SKILL.md`

### 2. Observability per Tenant (อย่างระมัดระวัง)

- logs/traces filter by tenantId ได้ (debug ได้เร็ว)
- metrics labels ต้องคุม cardinality: ใช้ `tenantTier`/`plan` แทน `tenantId` ถ้าจำนวน tenants สูง

### 3. Tenant-Scoped Operations

- maintenance/backfill/migrations ต้องสามารถ “ทำเฉพาะ tenant” และ pause/resume ได้
- support tooling ต้อง enforce authorization ก่อนอนุญาตดูข้อมูล tenant

### 4. Noisy Neighbor Controls

- rate limiting, concurrency caps, queue fairness
- quotas (storage/requests/jobs) และ alert เมื่อใกล้เพดาน

## Tenant-Aware Logging

```typescript
// All logs include tenant context
logger.info('User created', {
  tenantId: ctx.tenantId,
  userId: user.id,
  action: 'user.created',
});

// Query logs by tenant
// Loki: {tenantId="tenant-123"}
// CloudWatch: @tenantId="tenant-123"
```

## Tenant-Aware Metrics

```typescript
// Metrics with tenant label
counter.inc({
  tenant: ctx.tenantId,
  endpoint: '/api/users',
  status: 200,
});

// Dashboard filter by tenant
// Grafana: sum(http_requests_total{tenant="tenant-123"})
```

## Quick Start

1. บังคับ `tenantId` ใน request/job context และผ่าน authz ตรวจสิทธิ์ก่อนเสมอ
2. ทำ logging/tracing ให้ค้นหาได้ด้วย `tenantId` แต่ทำ redaction ของ PII/secret
3. ออกแบบ tenant-scoped backfills/maintenance ที่หยุด/จำกัดความเร็วได้
4. ใส่ guardrails กัน noisy neighbor (rate limits, quotas, fair scheduling)

## Tenant-Aware Operations

| Operation | Tenant-Aware Approach |
|-----------|----------------------|
| Debug | Filter logs/traces by tenantId |
| Maintenance | Scope to specific tenant |
| Migration | Run per-tenant, monitor impact |
| Scaling | Per-tenant resource limits |
| Alerts | Include tenant in alert context |

## Noisy Neighbor Prevention

```typescript
// Rate limiting per tenant
const limiter = new RateLimiter({
  keyGenerator: (req) => req.tenantId,
  points: 1000,
  duration: 60, // per minute
});

// Resource quotas per tenant
const quotas = {
  'tenant-123': { maxRequests: 10000, maxStorage: '10GB' },
  'tenant-456': { maxRequests: 50000, maxStorage: '50GB' },
};
```

## Production Checklist

- [ ] Tenant isolation verified (data, cache, queues, background jobs)
- [ ] Support tooling มี audit + authz (ไม่ให้ดูข้อมูล tenant แบบ “ใครก็ได้”)
- [ ] Logs/traces tenant-filterable และ scrub PII/secret
- [ ] Metrics ไม่ใช้ tenantId เป็น label ถ้า tenant count สูง
- [ ] Per-tenant maintenance/migration playbook + ability to pause/resume
- [ ] Rate limits/quotas/fairness controls พร้อม alerts

## Anti-patterns

1. **Tenant labels everywhere**: metric cardinality ระเบิด
2. **Tenant-blind jobs**: background jobs ลืม scope ทำให้ข้อมูลปน
3. **Support shortcuts**: bypass authz เพื่อ “แก้เร็ว” แล้วกลายเป็น data breach
4. **Global maintenance**: ทำ migration/backfill ทั้งหมดพร้อมกันจนกระทบทุก tenant

## Integration Points

- Authentication/authorization (tenant mapping, support access workflows)
- Observability stack (tenant filtering, dashboards, alert enrichment)
- Job queues (per-tenant concurrency, priorities, fairness)
- Billing/entitlements (quota enforcement, plan tiers)

## Further Reading

- [Multi-Tenant Observability](https://www.datadoghq.com/blog/multi-tenant-monitoring/)
- [Tenant Isolation Patterns](https://docs.microsoft.com/azure/architecture/guide/multitenant/)
