---
name: Repo Map SSOT
description: Single source of truth for repository structure and entry points, including key directories, domain boundaries, shared code, integrations, and build/deploy references
---

# Repo Map SSOT

## Overview

Single Source of Truth (SSOT) สำหรับ repository structure ที่ให้ AI และคนเข้าใจ codebase ได้ทันที รวม folder structure, key files, และ architectural decisions ในที่เดียว

## Why This Matters

- **Quick orientation**: รู้ว่าอะไรอยู่ตรงไหนทันที
- **AI efficiency**: AI ไม่ต้อง explore ซ้ำทุกครั้ง
- **Onboarding**: คนใหม่เข้าใจ repo structure เร็ว
- **Consistency**: ทุกคนมี mental model เดียวกัน

---

## Core Concepts

### 1. Structure Overview

- สรุป “โครงบนสุด” ของ repo ให้เห็นภาพใน 30 วินาที (src/tests/docs/scripts/config)
- ระบุว่าเป็น monorepo หรือ single service และ boundaries อยู่ตรงไหน

### 2. Key Directories

- เขียน “purpose” ของแต่ละโฟลเดอร์ใหญ่เป็น 1–2 บรรทัด (อะไรอยู่ในนั้น / อะไรไม่ควรอยู่)
- ใส่ ownership ถ้ามี (ทีม/owner) เพื่อช่วย routing PR/review

### 3. Entry Points

- ระบุไฟล์เริ่มต้น: server bootstrap, routes, DI/container, job runners, consumers
- ระบุ “happy path”: ถ้าจะตาม flow request เข้า service ต้องเริ่มอ่านที่ไหน

### 4. Configuration Files

- บอกที่อยู่ของ env/config และลำดับความสำคัญ (สอดคล้องกับ config conventions)
- list config files ที่ทำให้ deploy แตกต่าง (docker, k8s, terraform, workflows)

### 5. Domain Boundaries

- ระบุ domain modules และ dependency direction (domain ไม่ควรรู้ infra)
- ระบุ shared contracts/types และวิธี versioning/backward-compat

### 6. Shared Code

- รวม “จุดรวม” ของ shared libs และข้อห้าม (เช่น ห้าม import จาก app layer)
- อธิบาย pattern ของ barrel exports (ใช้/ไม่ใช้) เพื่อลด confusion

### 7. External Integrations

- list integrations สำคัญ (payment, auth, email, analytics) + config location + docs link
- ระบุ webhook/queues/topics ที่เกี่ยวข้อง (ถ้ามี)

### 8. Build & Deploy

- ระบุ scripts ที่ต้องรู้: build/test/lint/migrate/seed
- ระบุ pipeline/deploy target (GitHub Actions, k8s, ECS, serverless) และไฟล์ config ที่เกี่ยวข้อง

## Quick Start

```markdown
# Create/maintain `REPO.md` at repo root:
# - 30s overview (tree + key entry points)
# - Where configs live (env, secrets, deploy)
# - Domain boundaries + owners
# - Links to deeper docs (architecture, API, runbooks)
```

## Production Checklist

- [ ] REPO.md exists at root
- [ ] All major directories documented
- [ ] Entry points clearly marked
- [ ] Domain boundaries defined
- [ ] Kept up-to-date (review quarterly)
- [ ] Links to detailed docs

## Repo Map Template

````markdown
# REPO.md - Repository Map

> Last updated: 2024-01-15 | Auto-generated: Yes

## Quick Overview
[Project name] - [One sentence description]

## Structure

```
├── src/                    # Application source code
│   ├── api/               # HTTP/REST endpoints
│   ├── domain/            # Business logic, entities
│   ├── infrastructure/    # Database, external services
│   └── shared/            # Cross-cutting utilities
├── tests/                  # Test files (mirrors src/)
├── docs/                   # Documentation
├── scripts/                # Build, deploy, utility scripts
├── config/                 # Environment configs
└── [key files at root]
```

## Entry Points
| File | Purpose |
|------|---------|
| `src/index.ts` | Application bootstrap |
| `src/api/routes.ts` | API route definitions |
| `package.json` | Dependencies, scripts |

## Key Directories

### `src/api/`
HTTP layer: routes, controllers, middleware
- Owner: @backend-team
- Related: OpenAPI spec at `docs/api.yaml`

### `src/domain/`
Business logic, domain models, services
- Owner: @domain-team
- Pattern: Domain-Driven Design

### `src/infrastructure/`
External integrations: DB, cache, queues, APIs
- Owner: @infra-team

## Configuration
| File | Purpose |
|------|---------|
| `.env.example` | Required environment variables |
| `config/default.ts` | Default configuration |
| `tsconfig.json` | TypeScript settings |

## External Dependencies
| System | Purpose | Config Location |
|--------|---------|-----------------|
| PostgreSQL | Primary database | `src/infrastructure/db/` |
| Redis | Caching, queues | `src/infrastructure/cache/` |
| Stripe | Payments | `src/infrastructure/stripe/` |

## Build & Deploy
- Build: `npm run build`
- Test: `npm test`
- Deploy: GitHub Actions → AWS ECS

## Quick Commands
```bash
npm run dev       # Start dev server
npm run test      # Run tests
npm run lint      # Lint code
npm run build     # Build for production
```

## Related Docs
- [Architecture](./docs/architecture.md)
- [API Reference](./docs/api.md)
- [Development Guide](./docs/development.md)
````

## Anti-patterns

1. **No map**: ต้อง explore ทุกครั้ง
2. **Outdated map**: ไม่ตรงกับ reality
3. **Too detailed**: เป็น full docs แทน overview
4. **Missing entry points**: ไม่รู้จะเริ่มจากไหน

## Auto-Generation

```bash
# Generate repo map from folder structure
find . -type d -name "node_modules" -prune -o -type f -print | \
  grep -E '\.(ts|js|py|go)$' | \
  tree --fromfile > REPO_STRUCTURE.txt
```

## Integration Points

- IDE plugins (file tree)
- Documentation generators
- AI context loaders
- CI checks (verify map is current)

## Further Reading

- [Monorepo Tools](https://monorepo.tools/)
- [Architecture Documentation](https://arc42.org/)
