---
name: Change Impact Map
description: A practical framework to map change dependencies and blast radius, including who/what is affected, what to test, rollout/rollback strategies, and stakeholder ownership
---

# Change Impact Map

## Overview

Documentation ที่แสดงว่า "แก้ A กระทบ B/C อะไรบ้าง" - dependency relationships ระหว่าง components ที่ช่วยให้ประเมิน impact ของ changes ได้ก่อน implement

## Why This Matters

- **Risk assessment**: รู้ว่าแก้แล้วพังอะไรบ้าง
- **Test coverage**: รู้ว่าต้อง test อะไรเพิ่ม
- **Review scope**: รู้ว่าต้องให้ใคร review
- **Rollback planning**: รู้ว่าต้อง rollback อะไรบ้าง

---

## Core Concepts

### 1. Dependency Types

- **Code deps**: imports, shared modules, shared contracts, shared libraries
- **Runtime deps**: services called, queues/topics, caches, feature flags, config
- **Data deps**: tables/collections, schemas, indexes, migrations, analytics pipelines
- **Integration deps**: third-party APIs, webhooks, auth providers, payment processors

### 2. Impact Categories

- **Direct**: component ที่แก้โดยตรง (ไฟล์/โมดูล/service)
- **Indirect**: สิ่งที่เรียกใช้/ถูกเรียกใช้ (upstream/downstream)
- **Operational**: deploy, migrations, observability, on-call/runbooks
- **User-facing**: UX, SLAs/SLOs, billing, security/compliance

### 3. Critical Paths

- ระบุ P0/P1 เส้นทางที่ถ้าพังจะกระทบทั้งระบบ (auth, payments, DB connection, routing)
- เชื่อมกับ SLOs และ alerts ที่มีอยู่ เพื่อกำหนด “must watch” metrics
- ห้ามเปลี่ยน behavior ใน critical path โดยไม่มี staged rollout หรือ kill switch

### 4. Change Scopes

- **Small**: single module, isolated behavior → unit tests + targeted smoke
- **Medium**: multiple files, one service → integration tests + staging validation
- **Large**: multi-service หรือ schema/contract change → migration plan + canary + rollback playbook

### 5. Blast Radius

- ถามว่า “ถ้าส่วนนี้ล้ม จะล้มเป็นโดมิโนไปถึงอะไรบ้าง” (availability / correctness / latency)
- ระบุ failure modes: timeout, retries storm, stale cache, partial writes, auth failures
- ระบุ data risk: corruption, duplication, backfill issues, missing events

### 6. Ripple Effects

- ผลกระทบลำดับสอง/สาม: background jobs, reporting, search indexing, notifications
- เปลี่ยน field/type อาจกระทบ: SDKs, mobile app, dashboards, data warehouse
- พิจารณา “migration window” ที่มี versions ผสมกัน (old/new running together)

### 7. Affected Stakeholders

- owners/reviewers ตาม component (ทีม + on-call)
- consumers ของ API/events (ทีมอื่น/partner)
- stakeholders: support, sales, finance, security/compliance (ตามประเภท change)

### 8. Mitigation Strategies

- **Feature flags** สำหรับ cutover/kill switch
- **Canary/gradual rollout** เพื่อลดความเสี่ยงและตรวจจับเร็ว
- **Compatibility**: backward-compatible contracts + deprecation plan
- **Verification**: dashboards, synthetic checks, sampling, shadow reads (ถ้าเหมาะ)

## Quick Start

- ระบุ “change surface”: ไฟล์/โมดูล/service/table/event ที่แตะ
- ทำ dependency sweep: code imports + runtime calls + data + integrations
- เติม impact matrix (direct/indirect + must test)
- ใส่ mitigation: feature flag/canary/rollback + metrics to watch
- ระบุ owners/reviewers และสื่อสารกับ stakeholders ก่อน merge/deploy

## Production Checklist

- [ ] Critical paths documented
- [ ] Dependencies mapped
- [ ] Impact matrix created
- [ ] Stakeholders identified
- [ ] Updated on architecture changes
- [ ] Used in change management

## Change Impact Map Template

````markdown
# IMPACT_MAP.md

> Last updated: 2024-01-15

## High-Level Dependencies

```
┌─────────────────────────────────────────────────────┐
│                    Frontend                          │
│  (React App, Mobile App)                            │
└─────────────────────┬───────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────┐
│                   API Gateway                        │
│  (Auth, Rate Limiting, Routing)                     │
└──────┬─────────────┬─────────────┬──────────────────┘
       │             │             │
       ▼             ▼             ▼
┌──────────┐   ┌──────────┐   ┌──────────┐
│  User    │   │  Order   │   │  Payment │
│  Service │   │  Service │   │  Service │
└────┬─────┘   └────┬─────┘   └────┬─────┘
     │              │              │
     └──────────────┼──────────────┘
                    ▼
          ┌──────────────────┐
          │    PostgreSQL    │
          │    Redis Cache   │
          └──────────────────┘
```

## Component Impact Matrix

| If you change... | Direct Impact | Indirect Impact | Must Test |
|------------------|---------------|-----------------|-----------|
| User Service | Auth flow | All services (auth tokens) | Login, Registration, All API calls |
| Order Service | Order creation | Payment processing, Notifications | Create order, Payment flow |
| Payment Service | Checkout | Order completion, Receipts | Full checkout flow |
| Database Schema | All services | N/A | All integration tests |
| API Gateway Config | All routes | Frontend apps | Smoke tests |

## Critical Path Analysis

### 🔴 Critical (P0 Impact)
Changes here can cause total outage:
- `src/infrastructure/db/connection.ts` - Database connection
- `src/middleware/auth.ts` - Authentication
- `src/api/gateway/routes.ts` - API routing
- `config/production.ts` - Production config

**Required**: Full test suite, staged rollout, immediate rollback plan

### 🟠 High Impact (P1)
Changes here affect major features:
- `src/domain/users/` - User management
- `src/domain/orders/` - Order processing
- `src/domain/payments/` - Payment handling

**Required**: Integration tests, canary deployment

### 🟡 Medium Impact (P2)
Changes here affect specific features:
- `src/domain/notifications/` - Email/SMS
- `src/domain/reports/` - Reporting
- `src/api/admin/` - Admin functions

**Required**: Unit tests, feature flag

### 🟢 Low Impact (P3)
Changes here are isolated:
- `src/shared/utils/` - Utility functions
- `src/shared/constants/` - Constants
- Documentation files

**Required**: Unit tests

## Dependency Chains

### User Authentication
```
Change: src/domain/users/auth/
Impact chain:
1. User Service (login/logout)
   ↓
2. API Gateway (token validation)
   ↓
3. All Services (auth middleware)
   ↓
4. Frontend (auth state)
   ↓
5. Mobile App (auth state)
```

### Database Schema
```
Change: prisma/schema.prisma
Impact chain:
1. Database migration required
   ↓
2. All repositories using changed tables
   ↓
3. All services using those repositories
   ↓
4. API responses may change
   ↓
5. Frontend/Mobile display
```

### Shared Types
```
Change: src/shared/types/user.ts
Impact chain:
1. All files importing User type
   ↓
2. API request/response shapes
   ↓
3. Frontend type definitions
   ↓
4. Test mocks and fixtures
```

## Team Ownership

| Component | Owner | Reviewer |
|-----------|-------|----------|
| User Service | @auth-team | @security-team |
| Order Service | @commerce-team | @backend-lead |
| Payment Service | @payments-team | @security-team, @finance |
| Infrastructure | @platform-team | @sre |
| Database | @data-team | @backend-lead |
| Frontend | @frontend-team | @ux-team |

## Change Checklist by Scope

### Small Change (Single file, isolated)
- [ ] Unit tests pass
- [ ] Code review by 1 person
- [ ] Deploy to staging
- [ ] Quick smoke test

### Medium Change (Multiple files, one service)
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Code review by 2 people
- [ ] Deploy to staging
- [ ] Full feature test
- [ ] Monitor for 30 min

### Large Change (Multiple services, schema change)
- [ ] All tests pass
- [ ] Security review (if auth/data)
- [ ] Code review by team lead
- [ ] Database migration reviewed
- [ ] Feature flag ready
- [ ] Rollback plan documented
- [ ] Canary deployment
- [ ] Monitor for 24 hours
```

## Impact Assessment Questions

```markdown
Before making a change, answer:

1. **What depends on this?**
   - Which files import this?
   - Which services call this?
   - Which tests cover this?

2. **What does this depend on?**
   - External APIs?
   - Database tables?
   - Configuration?

3. **Who needs to know?**
   - Which teams?
   - Which stakeholders?
   - Which customers?

4. **What could go wrong?**
   - Failure modes?
   - Edge cases?
   - Data corruption?

5. **How do we verify success?**
   - Tests to run?
   - Metrics to watch?
   - Manual checks?
```
````

## Anti-patterns

1. **No impact assessment**: "It's just a small change"
2. **Missing dependencies**: Hidden coupling
3. **Outdated map**: Doesn't reflect current architecture
4. **No ownership**: No one responsible for areas

## Integration Points

- Change management process
- Code review templates
- CI/CD pipelines
- Incident post-mortems

## Further Reading

- [Dependency Mapping](https://martinfowler.com/bliki/Strangler.html)
- [Change Management](https://www.atlassian.com/itsm/change-management)
