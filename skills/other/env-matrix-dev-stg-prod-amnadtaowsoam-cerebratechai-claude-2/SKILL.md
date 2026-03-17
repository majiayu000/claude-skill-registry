---
name: Environment Matrix: Dev/Stg/Prod
description: Environment standards for development, staging, and production: parity principles, data and access policies, configuration boundaries, and deployment controls
---

# Environment Matrix: Dev/Stg/Prod

## Overview

มาตรฐานการจัดการ environments (development, staging, production) รวมถึง configs, data policies, access controls ที่แตกต่างกันแต่ละ environment

## Why This Matters

- **Parity**: Environments ใกล้เคียงกัน ลด "works on my machine"
- **Safety**: Production protected, staging for testing
- **Clarity**: รู้ว่า environment ไหนทำอะไรได้
- **Compliance**: Proper access controls

---

## Core Concepts

### 1. Parity (เหมือนกันเท่าที่จำเป็น)

- staging ควร “production-like” ในเรื่อง topology, config shape, observability, and deployment flow
- ต่างเฉพาะสิ่งที่จำเป็นต่อความปลอดภัย/ต้นทุน (scale, data, access)

### 2. Data Policy

- dev: seed/mock ได้ แต่ต้องป้องกันการใช้ข้อมูลจริงโดยไม่ตั้งใจ
- staging: sanitized copy หรือ synthetic data (ห้าม PII ถ้าไม่จำเป็น)
- prod: real data + audit + retention policy

### 3. Access & Change Control

- prod ต้องมี least privilege, approvals, และ audit trail
- staging ใช้สำหรับ validation และ rehearsal ของ deployments/rollbacks

## Environment Matrix

| Aspect | Development | Staging | Production |
|--------|-------------|---------|------------|
| Purpose | Local dev, experiments | Pre-prod testing | Live users |
| Data | Seed/mock | Sanitized copy | Real |
| Scale | Minimal | Production-like | Full |
| Access | All devs | Restricted | Very restricted |
| Logging | Verbose | Standard | Standard + audit |
| Feature flags | All enabled | Selective | Controlled rollout |
| Secrets | Local vault | Staging vault | Prod vault |
| Domain | localhost | staging.example.com | example.com |

## Quick Start

1. ตั้ง `APP_ENV=development|staging|production|test` เป็น source-of-truth
2. สร้าง “config matrix” ที่ keys เหมือนกันทุก env (ต่างเฉพาะค่า)
3. แยก secrets ออกจาก config และใช้ secret manager ต่อ env
4. ทำ access control matrix และกำหนดว่า “ใครทำอะไรได้” ต่อ env

## Config Per Environment

```typescript
// config/environments.ts
export const environments = {
  development: {
    apiUrl: 'http://localhost:3000',
    database: 'dev_db',
    logLevel: 'debug',
    features: { all: true },
  },
  staging: {
    apiUrl: 'https://staging-api.example.com',
    database: 'staging_db',
    logLevel: 'info',
    features: { experimental: true },
  },
  production: {
    apiUrl: 'https://api.example.com',
    database: 'prod_db',
    logLevel: 'warn',
    features: { stable: true },
  },
};
```

## Access Control Matrix

| Role | Dev | Staging | Production |
|------|-----|---------|------------|
| Developer | Full | Read + Deploy | Read logs only |
| Tech Lead | Full | Full | Read + Deploy |
| SRE/DevOps | Full | Full | Full |
| QA | Read | Full | Read only |

## Production Checklist

- [ ] staging deploy flow เหมือน production (ต่างเฉพาะ scale/data/access)
- [ ] data policy ชัดเจน (sanitized, retention, PII handling)
- [ ] secrets แยกตาม env (ไม่มี reuse ข้าม env)
- [ ] prod มี approvals + audit logs สำหรับ deploy/config changes
- [ ] feature flags rollout rules ต่างกันชัดเจนระหว่าง envs

## Anti-patterns

1. **Staging != Prod**: staging ใช้งานจริงไม่ได้ ทำให้ bug หลุด prod
2. **Sharing secrets**: ใช้ secret เดียวกันทุก env (risk สูงมาก)
3. **Real data in dev/staging**: PII leak และ compliance risk
4. **No ownership**: ไม่มีคนรับผิดชอบ access/policies ของแต่ละ env

## Integration Points

- CI/CD environments (GitHub Environments, approvals, secrets)
- Secret managers and IAM
- Observability (separate tenants/projects per env)
- Data pipelines (masking/sanitization jobs)

## Further Reading

- [12-Factor App: Dev/Prod Parity](https://12factor.net/dev-prod-parity)
- [Environment Management](https://docs.github.com/en/actions/deployment/targeting-different-environments)
