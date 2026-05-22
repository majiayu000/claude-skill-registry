---
name: add-api-endpoint
description: Create API layer components for a new entity. Includes usecase interactors (internal/usecase/), proto definitions (schema/proto/), gRPC handlers (internal/infrastructure/grpc/), and DI registration. Use when adding CRUD endpoints or Step 3 of CRUD workflow (after add-domain-entity).
---

# Add API Endpoint

Create complete API layer: usecase interactors, proto definitions, gRPC handlers, and DI registration.

## Prerequisites

- Domain entity created (use **add-domain-entity** skill first)
- Repository interface and implementation ready
- SQLBoiler models generated (`make migrate.up`)

## Workflow Overview

```
1. Usecase Input/Output  -->  internal/usecase/input/, output/
2. Interactor Interface  -->  internal/usecase/{actor}_{entity}.go
3. Interactor Impl       -->  internal/usecase/{actor}_{entity}_impl.go
4. Proto Definition      -->  schema/proto/rapid/{actor}_api/v1/
5. Generate Proto        -->  make generate.buf
6. Handler Marshaller    -->  handler/{actor}/marshaller/{entity}.go
7. Handler Methods       -->  handler/{actor}/{entity}.go
8. Update Handler Struct -->  handler/{actor}/handler.go
9. Register in DI        -->  dependency/dependency.go
10. Generate & Test      -->  make generate.mock && make test
```

## Step 1: Create Usecase Input/Output

Location: `internal/usecase/input/{actor}_{entity}.go`

Create input structs for each operation (Create, Get, List, Update, Delete).
Each struct needs a `Validate()` method.

See: [references/usecase-patterns.md](references/usecase-patterns.md#input-structs)

Location: `internal/usecase/output/{actor}_{entity}.go`

Create output struct only for List operations (returns slice + count).

See: [references/usecase-patterns.md](references/usecase-patterns.md#output-structs)

## Step 2: Create Interactor Interface

Location: `internal/usecase/{actor}_{entity}.go`

Define interface with `//go:generate` directive for mock generation.

See: [references/usecase-patterns.md](references/usecase-patterns.md#interactor-interface)

## Step 3: Implement Interactor

Location: `internal/usecase/{actor}_{entity}_impl.go`

Implement CRUD methods following transaction patterns:
- **Create**: Validate -> Create entity -> RWTx -> Get with Preload
- **Get**: Validate -> Get with Preload
- **List**: Validate -> List + Count with Preload
- **Update**: Validate -> RWTx(Get ForUpdate -> Update) -> Get with Preload
- **Delete**: Validate -> RWTx(Get ForUpdate -> Delete)

See: [references/usecase-patterns.md](references/usecase-patterns.md#interactor-implementation)

## Step 4: Define Protocol Buffers

Create two files:
- Model/Enum: `schema/proto/rapid/{actor}_api/v1/model_{entity}.proto`
- Request/Response: `schema/proto/rapid/{actor}_api/v1/api_{entity}.proto`

Then add RPCs to: `schema/proto/rapid/{actor}_api/v1/api.proto`

See: [references/proto-patterns.md](references/proto-patterns.md)

## Step 5: Generate Proto Code

```bash
make generate.buf
```

## Step 6: Create Handler Marshaller

Location: `internal/infrastructure/grpc/internal/handler/{actor}/marshaller/{entity}.go`

Convert between domain models and proto messages.

See: [references/handler-patterns.md](references/handler-patterns.md#marshaller)

## Step 7: Create Handler Methods

Location: `internal/infrastructure/grpc/internal/handler/{actor}/{entity}.go`

Implement gRPC handler methods that delegate to interactors.

See: [references/handler-patterns.md](references/handler-patterns.md#handler-methods)

## Step 8: Update Handler Struct

Location: `internal/infrastructure/grpc/internal/handler/{actor}/handler.go`

Add new interactor field and constructor parameter.

See: [references/handler-patterns.md](references/handler-patterns.md#handler-struct)

## Step 9: Register in DI

Location: `internal/infrastructure/dependency/dependency.go`

1. Add interactor field to `Dependency` struct
2. Initialize repository and interactor in `Inject()` method
3. Update `grpc/run.go` to pass interactor to handler constructor

See: [references/handler-patterns.md](references/handler-patterns.md#di-registration)

## Step 10: Generate Mocks & Test

```bash
make generate.mock
make test
```

## Checklist

- [ ] Input structs with `Validate()` method
- [ ] Output struct for List operation
- [ ] Interactor interface with `//go:generate`
- [ ] Interactor implementation with proper transaction handling
- [ ] Proto model/enum definitions
- [ ] Proto request/response messages with `openapiv2_schema`
- [ ] Proto service RPCs with HTTP annotations
- [ ] Proto code generated (`make generate.buf`)
- [ ] Handler marshaller (both directions + enums)
- [ ] Handler methods
- [ ] Handler struct updated
- [ ] DI configuration updated
- [ ] Mocks generated (`make generate.mock`)
- [ ] Tests passing (`make test`)

## Common Errors

| Error | Solution |
|-------|----------|
| `undefined: pb.Example` | Run `make generate.buf` |
| `undefined: mock_usecase.MockAdminExampleInteractor` | Run `make generate.mock` |
| Handler method not found | Check handler struct field name and interface registration |
