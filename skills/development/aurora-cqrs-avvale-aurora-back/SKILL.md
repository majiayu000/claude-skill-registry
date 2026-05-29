---
name: aurora-cqrs
description: >
  Aurora CQRS Architecture Reference - Understanding the CQRS structure,
  component relationships, editable zones, and data flow in Aurora/NestJS
  projects. Trigger: When needing to understand CQRS architecture, component
  structure, or editable zones.
license: MIT
metadata:
  author: aurora
  version: '1.2'
  auto_invoke:
    'Understanding CQRS architecture, component structure, editable zones'
---

## When to Use

Use this skill as a **REFERENCE** when:

- Understanding CQRS architecture and component relationships
- Learning what Commands, Queries, Handlers, Events, Sagas are
- Identifying which zones in generated files are editable
- Understanding the data flow between layers
- Learning the structure of Services, Repositories, Aggregates, Mappers

**⚠️ For IMPLEMENTING business logic in handlers, use `aurora-development` skill
instead.**

This skill is for UNDERSTANDING the architecture. The `aurora-development` skill
is for WRITING code.

## What is CQRS in Aurora?

**CQRS** (Command Query Responsibility Segregation) separates read operations
(Queries) from write operations (Commands).

Aurora implements CQRS using NestJS CQRS module with:

- **Commands** → Change state (Create, Update, Delete)
- **Queries** → Read state (Find, Get, Paginate, Count, etc.)
- **Handlers** → Execute commands/queries
- **Events** → Domain events triggered by aggregates
- **Sagas** → Coordinate complex workflows

## Architecture Layers

```
┌─────────────────────────────────────────────────────────────┐
│                    @api Layer (REST/GraphQL)                 │
│  Controllers/Resolvers → Handlers → dispatch Commands/Queries│
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                   @app/application Layer                     │
│  Commands → CommandHandlers → Services                       │
│  Queries  → QueryHandlers   → Services                       │
│  Events   → EventHandlers                                    │
│  Sagas    → React to events                                  │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    @app/domain Layer                         │
│  Aggregates (Entities with events)                           │
│  Value Objects (Immutable types)                             │
│  Repository Interfaces                                       │
│  Mappers (Domain ↔ Response)                                 │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                @app/infrastructure Layer                     │
│  Repository Implementations (Sequelize/TypeORM)              │
│  Seeders, Models                                             │
└─────────────────────────────────────────────────────────────┘
```

### ⚠️ @api Handler Responsibility (CRITICAL!)

**@api handlers (REST controllers, GraphQL resolvers, handler classes in @api/)
have ONE job:**

- ✅ Dispatch commands/queries via `commandBus.dispatch()` or `queryBus.ask()`
- ✅ Map HTTP/GraphQL input to command/query objects
- ✅ Return response to client

**@api handlers MUST NOT contain:**

- ❌ Business validations (status checks, permission rules)
- ❌ Repository queries (findById, find, get)
- ❌ State transitions or business rules
- ❌ Multiple sequential command/query dispatches with logic between them

**If you find yourself writing `if/throw` logic in an @api handler, STOP. That
logic belongs in a CommandHandler in `@app/`.**

**⚠️ WARNING about codebase examples:** Some IAM `@api` handlers (e.g.,
`iam-update-me-account.handler.ts`, `iam-check-password-me-account.handler.ts`)
contain business logic directly in `@api`. These are LEGACY cross-module
orchestration handlers, NOT a pattern to replicate. For domain operations
(provision, cancel, approve, etc.), ALWAYS create Command + Handler + Service in
`@app/application/<operation>/`.

## Critical Patterns

### ⚠️ EDITABLE ZONES (CRITICAL!)

**In Aurora-generated files, you can ONLY edit the `execute()` method body in
handlers.**

**DO NOT modify:**

- ❌ Command/Query class definitions
- ❌ Service main() methods (unless custom service)
- ❌ Repository interfaces
- ❌ Aggregates (entities)
- ❌ Value Objects
- ❌ Mappers

### Marking Custom Code

**Always mark custom code with AI-generated comments:**

```typescript
/* #region AI-generated code */
// Custom logic here
/* #endregion AI-generated code */
```

## Detailed References

For detailed structures, types, and handler examples, see:

- [Commands & Queries Reference](commands-queries.md) — Command/Query
  structures, types, and handler examples
- [Services Reference](services.md) — Command, Query, and Custom service
  structures
- [Events & Sagas Reference](events-sagas.md) — Events, EventHandlers, Sagas
- [Aggregates, Repositories & Mappers](aggregates.md) — Aggregates,
  Repositories, Mappers
- [Common Patterns](patterns.md) — Validation, cache, events, saga patterns

## Decision Trees

### When to use Command vs Query?

```
Operation changes state?
├─ YES → Use Command
│  ├─ Create → CreateXCommand + CreateXCommandHandler
│  ├─ Update → UpdateXCommand + UpdateXCommandHandler
│  ├─ Delete → DeleteXCommand + DeleteXCommandHandler
│  └─ Upsert → UpsertXCommand + UpsertXCommandHandler
│
└─ NO → Use Query
   ├─ Single record → FindXQuery + FindXQueryHandler
   ├─ Multiple records → GetXQuery + GetXQueryHandler
   ├─ Paginated → PaginateXQuery + PaginateXQueryHandler
   └─ Aggregate → CountXQuery / MaxXQuery / MinXQuery / SumXQuery
```

### Where to add custom logic?

```
Need validation before save?
└─ Add in CommandHandler.execute() before service call

Need to react to events?
└─ Create EventHandler

Need to coordinate multiple operations?
└─ Create Saga

Need to transform data?
└─ Use Mapper

Need custom query logic?
└─ Add in QueryHandler.execute() before/after service call

Need reusable business logic?
└─ Create custom Service and inject in Handler

Need a domain operation (provision, cancel, approve)?
└─ Create new Command + Handler + Service in @app/application/<operation>/
   - @api handler ONLY dispatches the command
   - Handler validates business rules
   - Service handles persistence + events
```

## Best Practices

### ✅ DO

- Mark all custom code with `/* #region AI-generated code */` comments
- Only edit `execute()` method body in handlers
- Create custom services for reusable logic
- Use dependency injection for custom services
- Validate data in command handlers before calling service
- Use QueryStatement for complex filters
- Map aggregates to responses in query handlers
- Apply events in services (created, updated, deleted)
- Use sagas for cross-aggregate coordination
- Inject EventPublisher in command services
- Use Value Objects for type safety

### ❌ DON'T

- Don't modify generated Command/Query classes
- Don't modify Service main() methods (create custom services instead)
- Don't modify Repository interfaces
- Don't modify Aggregates or Value Objects
- Don't modify Mappers
- Don't put business logic in services (put in handlers or custom services)
- Don't bypass repository (always use repository interface)
- Don't create commands/queries manually (use Aurora CLI to regenerate)
- Don't forget to commit events (call `aggregate.commit()`)
- Don't use direct database access (use repository)

## Resources

- **NestJS CQRS**: https://docs.nestjs.com/recipes/cqrs
- **Aurora Core**: `@aurorajs.dev/core` exports CQMetadata, IRepository, etc.
- **Project Structure**: `.claude/skills/aurora-project-structure/SKILL.md`
- **Aurora CLI**: `.claude/skills/aurora-cli/SKILL.md`

## Related Skills

- `aurora-development` - **USE THIS** for implementing business logic in
  handlers
- `aurora-project-structure` - Understand where CQRS components live
- `aurora-criteria` - Build complex QueryStatements for queries
- `typescript` - Type-safe implementation
- `aurora-cli` - Regenerate CQRS structure after YAML changes
