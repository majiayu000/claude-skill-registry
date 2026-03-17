---
name: Deployment Patterns
description: Practical deployment strategies (rolling, blue-green, canary) for safe releases with rollback, health checks, and database compatibility guidance—without requiring full Kubernetes complexity
---

# Deployment Patterns

## Overview

รูปแบบการ deploy ที่เหมาะกับ scale และความต้องการต่างๆ: rolling update, blue-green, canary โดยไม่ต้องพึ่ง full Kubernetes complexity

## Why This Matters

- **Zero downtime**: Users ไม่รู้สึกว่ามี deployment
- **Safe rollouts**: ค่อยๆ release, ถอยได้เร็ว
- **Right-sized**: เลือก pattern ตาม needs
- **Simplicity**: ไม่ต้อง over-engineer

---

## Core Concepts

### 1. Health Gates (ต้องมี)

- liveness/readiness checks เป็น gating ก่อนรับ traffic
- deploy ต้องหยุด/rollback ได้เมื่อ error rate/latency เกิน threshold
- ควรมี smoke tests หลัง switch traffic

### 2. Compatibility Window

- รองรับช่วงที่ version เก่า/ใหม่รันพร้อมกัน (mixed versions)
- schema changes ต้องเป็น backward-compatible หรือทำแบบ expand/contract

### 3. Rollback Strategy

- rollback คือ “กลับไป stable state” ทั้ง app + config + routing
- มี kill switch/feature flags สำหรับ cutover ที่เสี่ยง

## Deployment Patterns

### Rolling Update
```
Best for: Most applications
Risk: Medium (gradual)

Old: [A] [A] [A] [A]
     ↓
     [B] [A] [A] [A]
     ↓
     [B] [B] [A] [A]
     ↓
     [B] [B] [B] [B]
```

### Blue-Green
```
Best for: Database migrations, big changes
Risk: Low (instant rollback)

Blue (current): [A] [A] ← traffic
Green (new):    [B] [B]

Switch traffic:
Blue:  [A] [A]
Green: [B] [B] ← traffic
```

### Canary
```
Best for: Risky changes, A/B testing
Risk: Very low (1% first)

1%:  [B] ←1%
     [A] [A] [A] ←99%

10%: [B] [B] ←10%
     [A] [A] ←90%

100%: [B] [B] [B] [B] ←100%
```

## When to Use

| Pattern | Use When |
|---------|----------|
| Rolling | Standard deploys, stateless apps |
| Blue-Green | DB changes, need instant rollback |
| Canary | New features, high-risk changes |

## Quick Start

1. เลือก pattern ตาม blast radius (rolling สำหรับทั่วไป, canary สำหรับ risky, blue-green สำหรับ cutover ใหญ่)
2. เตรียม health gates + dashboards (errors/latency/saturation)
3. วาง rollback plan (ทำได้จริงภายในนาที)
4. ถ้ามี DB/schema change ให้ใช้ expand/contract + phased rollout

## Simple Implementation (Docker Compose)

```yaml
# Blue-green with nginx
services:
  nginx:
    image: nginx
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    ports:
      - "80:80"

  app-blue:
    image: myapp:1.0.0

  app-green:
    image: myapp:1.1.0

# Switch by updating nginx.conf upstream
```

## Production Checklist

- [ ] Readiness/liveness configured และใช้เป็น deploy gates
- [ ] Rollback plan ชัดเจน (routing + app version + config)
- [ ] Observability พร้อม: error rate/latency dashboards + alerts
- [ ] Canary/blue-green มีวิธี “ลด traffic/สลับ traffic” ที่ทำซ้ำได้
- [ ] DB migrations ถูกออกแบบให้ compatible กับ mixed versions

## Anti-patterns

1. **Deploy without gates**: ปล่อย traffic ก่อน readiness ผ่าน
2. **Big bang cutover**: เปลี่ยนพร้อมกันหมดโดยไม่มี staged rollout
3. **Rollback only in theory**: ไม่มีคนลอง rollback จริง/ไม่มี playbook
4. **Ignoring DB compatibility**: schema breaking ในขณะที่มี app หลาย version

## Integration Points

- CI/CD pipelines (progressive delivery, approvals, rollbacks)
- Load balancers / reverse proxies (Nginx, HAProxy, ALB)
- Feature flags (kill switch, gradual rollout)
- Runbooks/incident response

## Further Reading

- [Deployment Strategies](https://www.redhat.com/en/topics/devops/what-is-blue-green-deployment)
- [Canary Deployments](https://martinfowler.com/bliki/CanaryRelease.html)
