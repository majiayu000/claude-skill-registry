---
name: add-domain-entity
description: |
  Create domain layer components: models, repository interfaces, marshallers, and implementations.
  Use when: (1) adding domain model in internal/domain/model/, (2) creating repository interface in internal/domain/repository/, (3) implementing repository with marshaller in internal/infrastructure/{db}/.
  This is Step 2 of CRUD workflow (after add-database-table, before add-api-endpoint).
---

# Add Domain Entity

Create domain layer components for a new entity following DDD patterns.

## Prerequisites

- Database table created (use **add-database-table** skill first)
- SQLBoiler model generated via `make migrate.up`

## Quick Workflow

```
1. Domain Model     → internal/domain/model/{entity}.go
2. Domain Error     → internal/domain/errors/errors.go
3. Repository Interface → internal/domain/repository/{entity}.go
4. Marshaller       → internal/infrastructure/{db}/internal/marshaller/{entity}.go
5. Repository Impl  → internal/infrastructure/{db}/repository/{entity}.go
6. Generate Mocks   → make generate.mock
```

## Step 1: Create Domain Model

Location: `internal/domain/model/{entity}.go`

Create the entity struct, constructor, update methods, and type aliases.

Key requirements:
- Use `id.New()` for ID generation in constructor
- Set both `CreatedAt` and `UpdatedAt` to the same time parameter
- Define `ReadonlyReference` for relations (always nil in constructor)
- Create slice type alias: `type Examples []*Example`

See: [references/domain-model-patterns.md](references/domain-model-patterns.md)

## Step 2: Add Domain Error

Location: `internal/domain/errors/errors.go`

Add a not-found error for the entity:

```go
ExampleNotFoundErr = NewNotFoundError("E2xxxxx", "Example not found")
```

Follow error code conventions from `.claude/rules/domain-errors.md`.

## Step 3: Create Repository Interface

Location: `internal/domain/repository/{entity}.go`

Define the repository interface with standard CRUD operations and query structs.

Key requirements:
- Add `//go:generate` directive for mock generation
- Use `nullable.Type[T]` for optional enum/custom type filter fields
- Embed `BaseGetOptions` / `BaseListOptions` in query structs

See: [references/repository-patterns.md](references/repository-patterns.md)

## Step 4: Create Marshaller

Location: `internal/infrastructure/{mysql|postgresql|spanner}/internal/marshaller/{entity}.go`

Convert between DB models and domain models.

Key requirements:
- Related entity's `ReadonlyReference` must remain nil (no recursive loading)
- Use var declaration pattern for nullable timestamp fields
- Include both `ToModel` and `ToDBModel` functions

See: [references/marshaller-patterns.md](references/marshaller-patterns.md)

## Step 5: Create Repository Implementation

Location: `internal/infrastructure/{mysql|postgresql|spanner}/repository/{entity}.go`

Implement the repository interface using SQLBoiler.

Key requirements:
- Use `transactable.GetContextExecutor(ctx)` for all DB operations
- Implement `buildListQuery` helper for reusable filter logic
- Implement `buildPreload` helper for relation loading
- Use base helper functions: `addForUpdateFromBaseGetOptions`, `addForUpdateFromBaseListOptions`

See: [references/repository-patterns.md](references/repository-patterns.md)

## Step 6: Generate Mocks

```bash
make generate.mock
```

This generates mock implementations in `internal/domain/repository/mock/`.

## Checklist

### Domain Model
- [ ] Entity struct with all fields
- [ ] `ReadonlyReference` for relations (if any)
- [ ] Constructor with `id.New()` and `ReadonlyReference: nil`
- [ ] Update method using `null.*` types for optional fields
- [ ] Slice type alias (`Examples []*Example`)
- [ ] Helper methods on slice (`IDs()`, `MapByID()`)

### Status/Enum Types (if needed)
- [ ] Type definition with `Unknown` as first constant
- [ ] `String()` and `Valid()` methods
- [ ] `New{Type}(str string)` constructor

### Repository
- [ ] Interface with `//go:generate` directive
- [ ] Query structs with `nullable.Type[T]` for optional enums
- [ ] Domain error added for not-found case

### Implementation
- [ ] Marshaller with `ToModel`, `ToDBModel`, `ToModels`, `ToDBModels`
- [ ] Marshaller handles `ReadonlyReference` correctly
- [ ] Repository implementation with all CRUD methods
- [ ] `buildListQuery` and `buildPreload` helpers
- [ ] Mocks generated

## Next Steps

After creating domain entity, use **add-api-endpoint** skill to create:
- Usecase input/output structs
- Interactor interface and implementation
- Protocol Buffers definition
- gRPC handler
