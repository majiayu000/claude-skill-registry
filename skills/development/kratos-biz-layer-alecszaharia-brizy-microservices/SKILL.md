---
name: kratos-biz-layer
description: Generates business logic layer components (use cases, repository interfaces, business models, validators) for go-kratos microservices following Clean Architecture. Use when implementing domain logic, creating entity CRUD operations, adding validation rules, or orchestrating data access in kratos services.
---

<essential_principles>
## How Kratos Business Layer Works

### Clean Architecture Dependency Rule
The business layer (biz) is the core of Clean Architecture in Kratos microservices:

**Dependency Flow**: Service → Biz → Data
- **Biz defines interfaces** that data layer implements
- **Biz contains business logic** independent of frameworks
- **Biz uses domain models** not ORM entities

### Domain-Driven Structure (Current Pattern)

The biz layer follows domain-driven design with these subdirectories:

**1. Domain Layer** (`internal/biz/domain/`)
- `models.go` - Domain entities with validation tags
- `interfaces.go` - Repository, use case, and event publisher interfaces
- `errors.go` - Domain errors (ErrSymbolNotFound) and data layer errors (ErrDataNotFound)

**2. Use Case Layer** (`internal/biz/{entity}/`)
- `usecase.go` - Use case implementation
- `usecase_test.go` - Use case tests with event assertions
- `validator.go` - Validation logic factory

**3. Event Layer** (`internal/biz/event/`) - Optional
- `mapper.go` - Event payload transformations
- `topics.go` - Event topic constants

**4. Provider** (`internal/biz/provider.go`)
- Wire ProviderSet for dependency injection

### Error Separation Pattern

**Data Layer Errors** (returned by repositories):
- `domain.ErrDataNotFound` - Record not found
- `domain.ErrDataDuplicateEntry` - Unique constraint violation
- `domain.ErrDataDatabase` - Generic database error

**Domain Errors** (returned by use cases):
- `domain.ErrSymbolNotFound` - Symbol not found (business error)
- `domain.ErrDuplicateSymbol` - Duplicate symbol (business error)
- `domain.ErrDatabaseOperation` - Database operation failed

**Pattern**: Repositories return data errors, use cases map to domain errors via `toDomainError()` helper.

### Event Publishing Pattern

Use cases integrate event publishing for domain events:
- Accept `domain.{Entity}EventPublisher` interface
- Publish events within transactions
- Transaction rolls back if publishing fails

**Example**:
```go
err := uc.tm.InTx(ctx, func(ctx context.Context) error {
    symbol, err = uc.repo.Create(ctx, s)
    if err != nil {
        return err
    }
    return uc.pub.PublishSymbolCreated(ctx, symbol)
})
```

### Wire Dependency Injection
All constructors must be added to `ProviderSet` in `internal/biz/provider.go`:
```go
var ProviderSet = wire.NewSet(symbol.NewValidator, symbol.NewUseCase)
```
After changes, run `make generate` to regenerate Wire code.
</essential_principles>

<intake>
What would you like to do?

1. Create a new entity (use case + interface + model + validator)
2. Add methods to existing use case
3. Create standalone validator
4. View examples and patterns

**Wait for response before proceeding.**
</intake>

<routing>
| Response | Workflow |
|----------|----------|
| 1, "create", "new entity", "new" | `workflows/create-entity.md` |
| 2, "add method", "add", "extend" | `workflows/add-methods.md` |
| 3, "validator", "validation" | `workflows/create-validator.md` |
| 4, "examples", "patterns", "help" | `workflows/view-examples.md` |

**After reading the workflow, follow it exactly.**
</routing>

<reference_index>
All domain knowledge in `references/`:

**Core Patterns**: use-case-pattern.md, interface-pattern.md, model-pattern.md
**Code Style**: naming-conventions.md

Additional patterns (error handling, logging, transactions, testing) are covered within use-case-pattern.md.
</reference_index>

<workflows_index>
| Workflow | Purpose |
|----------|---------|
| create-entity.md | Generate complete biz layer for new entity |
| add-methods.md | Add CRUD methods to existing use case |
| create-validator.md | Create standalone validator |
| view-examples.md | Show patterns and examples |
</workflows_index>

<success_criteria>
Business layer code is correct when:

**Structure**:
- Domain models in `internal/biz/domain/models.go`
- Interfaces in `internal/biz/domain/interfaces.go`
- Errors in `internal/biz/domain/errors.go`
- Use case in `internal/biz/{entity}/usecase.go`
- Validator in `internal/biz/{entity}/validator.go`
- Tests in `internal/biz/{entity}/usecase_test.go`

**Use Case Implementation**:
- Struct has repo, pub, log, validator, tm fields
- Constructor returns interface type (domain.{Entity}UseCase)
- Methods accept context.Context as first parameter
- Validation happens before repository calls
- Data errors mapped to domain errors via `toDomainError()`
- Events published within transactions
- All errors logged with context

**Domain Layer**:
- Repository interface in `domain/interfaces.go`
- Event publisher interface in `domain/interfaces.go` (if events)
- Business model in `domain/models.go` with validation tags
- Domain errors (ErrSymbolNotFound) separated from data errors (ErrDataNotFound)

**Wire Integration**:
- Constructor added to ProviderSet in `internal/biz/provider.go`
- User reminded to run `make generate`
</success_criteria>
