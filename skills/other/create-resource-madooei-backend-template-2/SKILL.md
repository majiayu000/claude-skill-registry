---
name: create-resource
description: Orchestrator skill for creating a complete CRUD resource with all layers. Use when creating a new domain entity like notes, users, or courses from scratch. Triggers on "create resource", "new entity", "add crud for".
---

# Create Resource (Orchestrator)

Complete workflow for creating a new CRUD resource with all layers, tests, and real-time events.

## Overview

This skill orchestrates the creation of a complete resource by guiding you through all the required skills in the correct order.

## Prerequisites

Before starting, you should know:

- **Entity name** (e.g., "Course", "Project", "Task")
- **Entity fields** (what data does it hold?)
- **Business rules** (who can do what?)

## Creation Workflow

### Phase 1: Schema Layer

| Step | Skill           | Output                                  |
| ---- | --------------- | --------------------------------------- |
| 1    | `create-schema` | `src/schemas/{entity}.schema.ts`        |
| 2    | `test-schema`   | `tests/schemas/{entity}.schema.test.ts` |

**Creates**: Zod schemas for entity, create DTO, update DTO, query params, and TypeScript types.

### Phase 2: Repository Layer

| Step | Skill                       | Output                                                    |
| ---- | --------------------------- | --------------------------------------------------------- |
| 3    | `create-repository`         | `src/repositories/{entity}.repository.ts`                 |
| 4    | `create-mockdb-repository`  | `src/repositories/mockdb/{entity}.mockdb.repository.ts`   |
| 5    | `test-mockdb-repository`    | `tests/repositories/{entity}.mockdb.repository.test.ts`   |
| 6    | `create-mongodb-repository` | `src/repositories/mongodb/{entity}.mongodb.repository.ts` |
| 7    | `test-mongodb-repository`   | `tests/repositories/{entity}.mongodb.repository.test.ts`  |

**Creates**: Repository interface and implementations for MockDB and MongoDB.

### Phase 3: Service Layer

| Step | Skill                       | Output                                         |
| ---- | --------------------------- | ---------------------------------------------- |
| 8    | `create-resource-service`   | `src/services/{entity}.service.ts`             |
| 9    | `add-authorization-methods` | Update `src/services/authorization.service.ts` |
| 10   | `test-resource-service`     | `tests/services/{entity}.service.test.ts`      |

**Creates**: Business logic service with authorization and event emission.

### Phase 4: Controller Layer

| Step | Skill               | Output                                          |
| ---- | ------------------- | ----------------------------------------------- |
| 11   | `create-controller` | `src/controllers/{entity}.controller.ts`        |
| 12   | `test-controller`   | `tests/controllers/{entity}.controller.test.ts` |

**Creates**: HTTP request handlers.

### Phase 5: Routes Layer

| Step | Skill              | Output                                 |
| ---- | ------------------ | -------------------------------------- |
| 13   | `create-routes`    | `src/routes/{entity}.router.ts`        |
| 14   | `integrate-routes` | Update `src/app.ts` to mount routes    |
| 15   | `test-routes`      | `tests/routes/{entity}.router.test.ts` |

**Creates**: Route definitions with middleware, integrated into app.

### Phase 6: Events (Optional)

| Step | Skill                 | Output               |
| ---- | --------------------- | -------------------- |
| 16   | `add-resource-events` | Update events router |

**Creates**: Real-time SSE event streaming for the resource.

## Files Created Summary

```
src/
├── schemas/
│   └── {entity}.schema.ts          # Zod schemas + types
├── repositories/
│   ├── {entity}.repository.ts      # Interface
│   ├── mockdb/
│   │   └── {entity}.mockdb.repository.ts
│   └── mongodb/
│       └── {entity}.mongodb.repository.ts
├── services/
│   ├── {entity}.service.ts         # Business logic
│   └── authorization.service.ts    # Updated with permissions
├── controllers/
│   └── {entity}.controller.ts      # HTTP handlers
├── routes/
│   ├── {entity}.router.ts          # Route definitions
│   └── events.router.ts            # Updated for SSE
└── app.ts                          # Updated to mount routes

tests/
├── schemas/
│   └── {entity}.schema.test.ts
├── repositories/
│   ├── {entity}.mockdb.repository.test.ts
│   └── {entity}.mongodb.repository.test.ts
├── services/
│   └── {entity}.service.test.ts
├── controllers/
│   └── {entity}.controller.test.ts
└── routes/
    └── {entity}.router.test.ts
```

## Quick Start Checklist

```markdown
## Creating {Entity} Resource

### Phase 1: Schema

- [ ] Create schema with `create-schema`
- [ ] Add tests with `test-schema`
- [ ] Run tests: `pnpm test tests/schemas/{entity}.schema.test.ts`

### Phase 2: Repository

- [ ] Create interface with `create-repository`
- [ ] Create MockDB implementation with `create-mockdb-repository`
- [ ] Add MockDB tests with `test-mockdb-repository`
- [ ] Run tests: `pnpm test tests/repositories/{entity}.mockdb.repository.test.ts`
- [ ] Create MongoDB implementation with `create-mongodb-repository`
- [ ] Add MongoDB tests with `test-mongodb-repository`
- [ ] Run tests: `pnpm test tests/repositories/{entity}.mongodb.repository.test.ts`

### Phase 3: Service

- [ ] Create service with `create-resource-service`
- [ ] Add authorization methods with `add-authorization-methods`
- [ ] Add tests with `test-resource-service`
- [ ] Run tests: `pnpm test tests/services/{entity}.service.test.ts`

### Phase 4: Controller

- [ ] Create controller with `create-controller`
- [ ] Add tests with `test-controller`
- [ ] Run tests: `pnpm test tests/controllers/{entity}.controller.test.ts`

### Phase 5: Routes

- [ ] Create routes with `create-routes`
- [ ] Mount routes in app.ts with `integrate-routes`
- [ ] Add tests with `test-routes`
- [ ] Run tests: `pnpm test tests/routes/{entity}.router.test.ts`

### Phase 6: Events (Optional)

- [ ] Add event emission with `add-resource-events`
- [ ] Update events router

### Final Verification

- [ ] Run all tests: `pnpm test`
- [ ] Run type check: `pnpm type-check`
- [ ] Run linting: `pnpm lint`
- [ ] Test manually with API client
```

## Example: Creating a "Project" Resource

```bash
# Follow skills in order:
1. create-schema             → src/schemas/project.schema.ts
2. test-schema               → tests/schemas/project.schema.test.ts
3. create-repository         → src/repositories/project.repository.ts
4. create-mockdb-repository  → src/repositories/mockdb/project.mockdb.repository.ts
5. test-mockdb-repository    → tests/repositories/project.mockdb.repository.test.ts
6. create-mongodb-repository → src/repositories/mongodb/project.mongodb.repository.ts
7. test-mongodb-repository   → tests/repositories/project.mongodb.repository.test.ts
8. create-resource-service   → src/services/project.service.ts
9. add-authorization-methods → Update authorization.service.ts with canViewProject, etc.
10. test-resource-service    → tests/services/project.service.test.ts
11. create-controller        → src/controllers/project.controller.ts
12. test-controller          → tests/controllers/project.controller.test.ts
13. create-routes            → src/routes/project.router.ts
14. integrate-routes         → Update app.ts to mount /projects routes
15. test-routes              → tests/routes/project.router.test.ts
16. add-resource-events      → Update events.router.ts (optional)
```

## See Also

- Individual skill files for detailed instructions
- `review-resource` - Validate a completed resource follows all patterns
- `integrate-routes` - Mounting routes in app.ts
- `add-authorization-methods` - Adding entity permissions
- `add-query-filter` - Adding custom query filters
- `bootstrap-project` - Starting a new project from scratch
