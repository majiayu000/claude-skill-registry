---
name: aurora-project-structure
description: >
  Provides structured information about the Aurora/NestJS project folder hierarchy, explaining the purpose and responsibility of each directory and key files.
  Trigger: When user asks about project structure, folder organization, "where is X", or navigating the codebase.
license: MIT
metadata:
  author: aurora
  version: "1.0"
  auto_invoke: "Navigating project structure, locating files, understanding folder organization"
---

## When to Use

- User asks "where is..." or "where should I put..."
- User needs to understand the project organization
- User asks about naming conventions
- User needs to navigate between layers (API, Application, Domain, Infrastructure)
- User is new to Aurora/NestJS CQRS architecture

---

## Critical Patterns

### Layer Responsibilities

| Layer | Path | Responsibility | Can Modify? |
|-------|------|----------------|-------------|
| **API** | `@api/[package]/[module]/` | Entry points (REST/GraphQL), DTOs, Resolvers, Handlers | Normally handler (generated) |
| **Application** | `@app/[package]/[module]/application/` | Use cases, Commands, Queries, Events, Sagas | Exceptionally (generated) |
| **Domain** | `@app/[package]/[module]/domain/` | Aggregates, Value Objects, Repository interfaces | Exceptionally (generated) |
| **Infrastructure** | `@app/[package]/[module]/infrastructure/` | Repository implementations, ORM models | Exceptionally (generated) |

### File Generation Marker

All generated files include this header - **NEVER modify these files directly**:
```typescript
/**
 * @aurora-generated
 * @source cliter/[package]/[module].aurora.yaml
 */
```

---

## Project Structure

```
cliter/                                 # Aurora YAML Definitions
├── [package]/
│   ├── [module].aurora.yaml            # Module definition (source of truth)
│   └── [module]-lock.json              # Generation lock file
postman/                                # Postman files
├── [package]/
│   └── [package].[module].postman.json # Postman file collection v2.1
│
src/
├── @api/[package]/                    # API Layer - Entry points
│   ├── [module]/
│   │   ├── controllers/               # REST Controllers (generated)
│   │   ├── dto/                       # Data Transfer Objects (generated)
│   │   ├── graphql/                   # GraphQL schema definitions (generated)
│   │   ├── handlers/                  # API handlers - bridge to application layer (generated)
│   │   ├── resolvers/                 # GraphQL Resolvers (generated)
│   │   ├── seeder/                    # Data seeders for e2e tests
│   │   └── index.ts                   # Barrel exports
│   ├── [package].module.ts            # NestJS module declaration
│   └── [package].seeder.ts            # Package-level seeder
│
├── @app/[package]/                    # Application + Domain Layer
│   ├── [module]/
│   │   ├── application/               # CQRS Use Cases
│   │   │   ├── count/                 # Count query handlers
│   │   │   ├── create/                # Create command handlers
│   │   │   ├── delete/                # Delete command handlers
│   │   │   ├── events/                # Domain events and handlers
│   │   │   ├── find/                  # Find query handlers
│   │   │   ├── get/                   # Get (list) query handlers
│   │   │   ├── max/                   # Max aggregation handlers
│   │   │   ├── min/                   # Min aggregation handlers
│   │   │   ├── paginate/              # Pagination query handlers
│   │   │   ├── raw-sql/               # Raw SQL query handlers
│   │   │   ├── sagas/                 # CQRS Sagas for side effects
│   │   │   ├── sum/                   # Sum aggregation handlers
│   │   │   ├── update/                # Update command handlers
│   │   │   └── upsert/                # Upsert command handlers
│   │   ├── domain/                    # Domain Layer
│   │   │   ├── [module].aggregate.ts  # Aggregate Root (generated)
│   │   │   ├── [module].mapper.ts     # Entity <-> DTO mapper (generated)
│   │   │   ├── [module].repository.ts # Repository interface (generated)
│   │   │   ├── [module].response.ts   # Response type (generated)
│   │   │   ├── types/                 # Enums and types from module (generated)
│   │   │   └── value-objects/         # Value Objects (generated)
│   │   └── infrastructure/            # Infrastructure Layer
│   │       ├── mock/                  # Mock repository for testing
│   │       │   ├── mock-[module].data.ts
│   │       │   ├── mock-[module].repository.ts
│   │       │   └── mock-[module].seeder.ts
│   │       └── sequelize/             # Sequelize ORM implementation
│   │           ├── sequelize-[module].model.ts
│   │           └── sequelize-[module].repository.ts
│   ├── [package].seed.ts              # Package seed configuration
│   ├── [package].types.ts             # Package type definitions
│   ├── index.ts                       # Barrel exports
│   └── public-api.ts                  # Public API exports
│
├── @aurora/                           # Framework Core (DO NOT MODIFY)
│   ├── decorators/                    # Custom decorators
│   ├── modules/                       # Core modules (CQRS, GraphQL, etc.)
│   ├── services/                      # Core services (Bootstrap, Logger)
│   ├── core.module.ts                 # Core module configuration
│   └── shared.module.ts               # Shared module exports
│
├── @config/                           # Configuration modules
│   └── mailer/                        # Email configuration
│
├── assets/                            # Static assets
├── i18n/                              # Internationalization files
│
├── app.module.ts                      # Root application module
├── app.controller.ts                  # Root controller
├── app.service.ts                     # Root service
├── main.ts                            # Application entry point
├── repl.ts                            # REPL mode entry point
│
test/
├── acceptance/                        # E2E acceptance tests
│   └── [package]/
│       └── [module].e2e-spec.ts       # Module e2e tests
└── jest-e2e.json                      # E2E Jest configuration
```

---

## CQRS File Naming Convention

### Commands (Write operations)
```
[package]-create-[module].command.ts           # Create single
[package]-create-[modules].command.ts          # Create multiple
[package]-update-[module]-by-id.command.ts     # Update by ID
[package]-update-[modules].command.ts          # Update multiple
[package]-delete-[module]-by-id.command.ts     # Delete by ID
[package]-delete-[modules].command.ts          # Delete multiple
[package]-upsert-[module].command.ts           # Upsert single
```

### Queries (Read operations)
```
[package]-find-[module].query.ts               # Find single by criteria
[package]-find-[module]-by-id.query.ts         # Find by ID
[package]-get-[modules].query.ts               # Get all/list
[package]-paginate-[modules].query.ts          # Paginated list
[package]-count-[module].query.ts              # Count
[package]-sum-[module].query.ts                # Sum aggregation
[package]-max-[module].query.ts                # Max aggregation
[package]-min-[module].query.ts                # Min aggregation
[package]-raw-sql-[modules].query.ts           # Raw SQL query
```

### Events
```
[package]-created-[module].event.ts            # Created event
[package]-updated-[module].event.ts            # Updated event
[package]-deleted-[module].event.ts            # Deleted event
```

---

## Decision Tree: Where to Put Code?

```
Need to add a new field/entity?
  → Modify cliter/[package]/[module].aurora.yaml
  → Run Aurora CLI to regenerate

Need custom business logic?
  → Add to command/query handler execute() method
  → Create custom service in services/ folder

Need new API endpoint?
  → Modify YAML and regenerate
  → Or create custom controller (rare)

Need to validate data?
  → Add validation in command handler
  → Or create custom validator service

Need to react to domain events?
  → Create event handler in events/ folder
  → Or use sagas for complex workflows

Need database-specific logic?
  → AVOID if possible
  → Use repository interface methods
```

---

## Quick Navigation Commands

```bash
# Find all files for a module
find src -name "*unit*" -type f

# Find all command handlers
find src -name "*command-handler.ts" -type f

# Find all query handlers
find src -name "*query-handler.ts" -type f

# Find YAML definitions
ls cliter/*/

# Find generated files by source
grep -r "@source cliter" src/
```

---

## Resources

- **YAML Definitions**: See `cliter/[package]/[module].aurora.yaml` for module source
- **Framework Core**: See `src/@aurora/` for reusable decorators and modules
- **Tests**: See `test/acceptance/[package]/` for e2e test examples
