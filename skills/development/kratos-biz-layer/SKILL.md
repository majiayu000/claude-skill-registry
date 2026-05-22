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

### Three Key Components

**1. Business Models** (`internal/biz/models.go`)
- Domain entities with validation tags
- Independent of database structure
- Use `validator` struct tags for validation

**2. Repository Interfaces** (`internal/biz/interfaces.go`)
- Define data access contracts
- Implemented by data layer
- Accept/return business models, not ORM entities

**3. Use Cases** (`internal/biz/{entity}.go`)
- Orchestrate business logic
- Depend on repository interfaces
- Handle validation, logging, error mapping

### Wire Dependency Injection
All constructors must be added to `ProviderSet` in `internal/biz/biz.go`:
```go
var ProviderSet = wire.NewSet(NewSymbolValidator, NewSymbolUseCase)
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
- Use case struct has repo, log, validator, tm fields
- Constructor function returns interface type (not struct)
- Methods accept context.Context as first parameter
- Validation happens before repository calls
- Errors are properly wrapped and logged
- Repository interface added to interfaces.go
- Business model added to models.go with validation tags
- Constructor added to ProviderSet in biz.go
- User reminded to run `make generate`
</success_criteria>
