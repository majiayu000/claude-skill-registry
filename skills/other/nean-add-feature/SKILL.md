---
name: nean-add-feature
description: Scaffold a new feature with NestJS module, TypeORM entity, DTOs, and Angular components.
argument-hint: "<feature-name> [--no-ui] [--no-api] [--no-entity]"
allowed-tools: Bash, Write, Read, Glob, Grep
---

## Purpose
Add a complete feature slice to an existing NEAN project with all layers wired up and tests included.

## Arguments
- `feature-name` — Feature name in kebab-case (e.g., `user-profile`, `invoice`)
- `--no-ui` — Skip Angular components (API-only feature)
- `--no-api` — Skip NestJS module (frontend-only feature)
- `--no-entity` — Skip TypeORM entity (use existing entity)

## What gets created

### Default (all layers)
```
libs/shared/types/src/<feature>.dto.ts           # DTOs + interfaces
libs/api/database/src/entities/<feature>.entity.ts   # TypeORM entity
apps/api/src/modules/<feature>/
  <feature>.module.ts
  <feature>.controller.ts
  <feature>.service.ts
  __tests__/
    <feature>.controller.spec.ts
    <feature>.service.spec.ts
apps/web/src/app/<feature>/
  <feature>.routes.ts
  <feature>-list/
    <feature>-list.component.ts
  <feature>-form/
    <feature>-form.component.ts
  <feature>-detail/
    <feature>-detail.component.ts
libs/web/data-access/src/<feature>/
  <feature>.service.ts
  <feature>.store.ts  (NgRx feature state)
```

### With flags
- `--no-ui`: Only DTOs + entity + NestJS module
- `--no-api`: Only DTOs + Angular components + data-access
- `--no-entity`: Only DTOs + NestJS module + Angular (uses existing entity)

## Conventions

### Naming
- Feature name: `kebab-case` (input)
- Classes: `PascalCase` (e.g., `UserProfile`, `CreateUserProfileDto`)
- Files: `kebab-case.ts` for everything
- API routes: `/api/<feature>` for collection, `/api/<feature>/:id` for item

### DTO location
All DTOs go in `libs/shared/types/src/<feature>.dto.ts`:
- `Create<Feature>Dto` — creation input with validation decorators
- `Update<Feature>Dto` — partial update input (PartialType)
- `<Feature>ResponseDto` — API response shape
- Interfaces exported alongside classes

### API endpoint structure
- `GET /api/<feature>` — list (paginated)
- `POST /api/<feature>` — create
- `GET /api/<feature>/:id` — get one
- `PATCH /api/<feature>/:id` — update
- `DELETE /api/<feature>/:id` — delete

### Entity conventions
- Timestamps enabled (@CreateDateColumn, @UpdateDateColumn)
- Indexes defined with comments explaining why
- UUID primary keys by default
- Soft delete pattern if deletion is reversible

## Workflow
1. Create DTOs in libs/shared/types
2. Create TypeORM entity (if not --no-entity)
3. Create NestJS module with controller + service (if not --no-api)
4. Create Angular components and routing (if not --no-ui)
5. Create NgRx feature state
6. Create tests for each layer
7. Run `npm run lint` and `npm run test` to verify

## Output
Summarize: files created, API endpoints available, components ready to use.

## Reference
For templates and patterns, see `reference/nean-add-feature-reference.md`
