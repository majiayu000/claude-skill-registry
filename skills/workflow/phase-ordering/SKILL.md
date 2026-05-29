---
name: phase-ordering
description: Canonical phase ordering and dependency rules. ALWAYS reference this skill when creating phases to ensure correct sequencing.
---

// Project Autopilot - Phase Ordering Rules
// Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

# Phase Ordering Skill

**CRITICAL:** Always reference this skill when creating phases. Incorrect ordering causes failures.

---

## Canonical Phase Order

```
┌─────────────────────────────────────────────────────────────┐
│  001: PROJECT SETUP                                         │
│  - Repo init, configs, dependencies                         │
│  - CLAUDE.md, .editorconfig, eslint, prettier               │
│  Prerequisites: None                                        │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  002: DATABASE FOUNDATION                                   │
│  - Schema design, migrations, seed data                     │
│  - Database connection, ORM setup                           │
│  Prerequisites: 001                                         │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  003: CORE INFRASTRUCTURE                                   │
│  - Configuration management                                 │
│  - Logging, error handling                                  │
│  - Base middleware, utilities                               │
│  Prerequisites: 001, 002                                    │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  004: AUTHENTICATION & AUTHORIZATION                        │
│  - User model, auth endpoints                               │
│  - JWT/session management                                   │
│  - Role-based access control                                │
│  Prerequisites: 002, 003                                    │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  005: API LAYER                                             │
│  - API contracts (OpenAPI)                                  │
│  - Route handlers                                           │
│  - Request validation, serialization                        │
│  Prerequisites: 003, 004                                    │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  006: BUSINESS LOGIC                                        │
│  - Domain services                                          │
│  - Use cases                                                │
│  - Business rules                                           │
│  Prerequisites: 002, 005                                    │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  007: FRONTEND FOUNDATION                                   │
│  - Project setup, routing                                   │
│  - Component library                                        │
│  - State management setup                                   │
│  Prerequisites: 001, 005 (API contracts)                    │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  008: FEATURE IMPLEMENTATION                                │
│  - Feature-specific backend                                 │
│  - Feature-specific frontend                                │
│  - Feature tests                                            │
│  Prerequisites: 006, 007                                    │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  009: INTEGRATION & TESTING                                 │
│  - Integration tests                                        │
│  - E2E tests                                                │
│  - Performance tests                                        │
│  Prerequisites: 008                                         │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  010: SECURITY HARDENING                                    │
│  - Security audit                                           │
│  - Vulnerability fixes                                      │
│  - Security tests                                           │
│  Prerequisites: 008, 009                                    │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  011: DOCUMENTATION                                         │
│  - API documentation                                        │
│  - User guides                                              │
│  - Developer docs                                           │
│  Prerequisites: 008 (features stable)                       │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  012: DEVOPS & DEPLOYMENT                                   │
│  - CI/CD pipelines                                          │
│  - Docker/K8s configs                                       │
│  - Monitoring, alerting                                     │
│  Prerequisites: 009, 010                                    │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  013: POLISH & OPTIMIZATION                                 │
│  - Performance tuning                                       │
│  - UX improvements                                          │
│  - Final bug fixes                                          │
│  Prerequisites: All above                                   │
└─────────────────────────────────────────────────────────────┘
```

---

## Dependency Rules

### Hard Dependencies (MUST follow)

| Phase | MUST Come After |
|-------|-----------------|
| Database | Setup |
| Auth | Database |
| API | Infrastructure, Auth |
| Business Logic | Database, API contracts |
| Frontend | API contracts exist |
| Features | Business logic, Frontend foundation |
| Integration Tests | Feature implementation |
| Security | Implementation complete |
| Documentation | Features stable |
| Deployment | Tests pass, Security done |

### Soft Dependencies (Recommended)

| Phase | Should Come After |
|-------|-------------------|
| Performance tests | Integration tests |
| Security hardening | Basic tests exist |
| Documentation | Most features done |

---

## What Can Run in Parallel

### Safe Parallel Work

```
After Phase 005 (API Layer):
├── Backend features (Phase 006+)
└── Frontend development (Phase 007+)

After Phase 008 (Features):
├── Integration tests
├── Security audit
└── Documentation
```

### Never Parallel

```
❌ Database schema + API (needs schema)
❌ Auth + features (needs auth)
❌ Frontend + backend for SAME feature
❌ Tests + implementation of same feature
```

---

## Task Ordering Within Phase

### Standard Task Order

```
1. Schema/Config changes
2. Types/Interfaces  
3. Core implementation
4. Integration (routes, wiring)
5. Tests
6. Exports/Index files
```

### Example: API Endpoint Phase

```
Task 1: Add database migration
Task 2: Create entity/model
Task 3: Create repository
Task 4: Create service/use case
Task 5: Create route handler
Task 6: Add validation schemas
Task 7: Register routes
Task 8: Write unit tests
Task 9: Write integration tests
```

---

## Phase Dependencies Lookup Table

```
Phase 001 (Setup)         → []
Phase 002 (Database)      → [001]
Phase 003 (Infrastructure)→ [001, 002]
Phase 004 (Auth)          → [002, 003]
Phase 005 (API)           → [003, 004]
Phase 006 (Business)      → [002, 005]
Phase 007 (Frontend)      → [001, 005]
Phase 008 (Features)      → [006, 007]
Phase 009 (Testing)       → [008]
Phase 010 (Security)      → [008, 009]
Phase 011 (Docs)          → [008]
Phase 012 (DevOps)        → [009, 010]
Phase 013 (Polish)        → [all]
```

---

## Quick Validation

Before creating phases, verify:

- [ ] No phase depends on a later phase
- [ ] Database phases come before API phases
- [ ] Auth exists before protected features
- [ ] API contracts exist before frontend
- [ ] Implementation before testing
- [ ] All dependencies can be satisfied

---

## Anti-Patterns

### ❌ WRONG

```
Phase 1: Build login UI
Phase 2: Create user table
Phase 3: Add auth endpoints
```

### ✅ CORRECT

```
Phase 1: Create user table + migrations
Phase 2: Add auth endpoints
Phase 3: Build login UI
```
