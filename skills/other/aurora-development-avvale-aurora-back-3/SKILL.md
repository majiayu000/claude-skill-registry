---
name: aurora-development
description: >
  Expert NestJS development with CQRS architecture for Aurora projects. Covers
  commands, queries, handlers, business logic placement, guards, interceptors,
  and custom decorators, Value Objects. Trigger: When implementing NestJS
  components, CQRS handlers, business logic, guards, interceptors, or custom
  decorators in Aurora projects.
license: MIT
metadata:
  author: aurora
  version: '1.2'
  auto_invoke:
    'Implementing NestJS/Aurora components, handlers, services, guards,
    interceptors'
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, WebFetch, WebSearch, Task
---

## When to Use

**This is the PRIMARY skill for IMPLEMENTING code in Aurora/NestJS projects.**

Use this skill when:

- **Writing business logic in command/query handlers** (validations, rules,
  checks)
- **Implementing any custom code** in Aurora-generated handlers
- Creating guards, interceptors, pipes, or custom decorators
- Implementing NestJS-specific features (middleware, exception filters)
- Working with dependency injection (DI) and inversion of control (IoC)
- Integrating with Sequelize ORM
- Testing with Jest (unit and e2e)

**Note:** For understanding CQRS architecture (what are Commands, Handlers,
etc.), see `aurora-cqrs` skill.

**Always combine with:**

- `prettier` skill for code formatting (MANDATORY after every edit)
- `typescript` skill for strict type patterns
- `aurora-cqrs` skill for CQRS architecture reference (structure, editable
  zones)
- `aurora-project-structure` skill for file locations
- `aurora-criteria` skill for QueryStatement filters

---

## Critical Patterns

### ⚠️ FIRST DECISION: Where Does the Logic Go? (MANDATORY GATE)

**Before writing ANY code, classify the operation:**

```
Is it a DOMAIN OPERATION? (provision, cancel, approve, reject, activate, close, etc.)
│
├─ YES → Create Command + Handler + Service in @app/application/<operation>/
│        The @api handler ONLY does: commandBus.dispatch(new CustomCommand(...))
│        Business validations go in the @app CommandHandler.execute()
│        Persistence + events go in the @app Service.main()
│        SEE: patterns.md → Pattern 4 for full example
│
└─ NO → It's standard CRUD or simple orchestration
         Use existing generated commands/queries
```

**⚠️ NEVER put business logic (validations, status checks, repository queries,
if/throw) in @api handlers. Even if you see existing @api handlers in the
codebase that do this (e.g., IAM account handlers), those are LEGACY EXCEPTIONS
for cross-module orchestration, NOT a pattern to follow for domain operations.**

**⚠️ Domain operations with additionalApis ALWAYS need their own @app layer
(Command + Handler + Service). The @api handler is ONLY a thin dispatcher.**

---

### ⚠️ Code Formatting (CRITICAL!)

**MANDATORY: Use `prettier` skill after EVERY file modification**

```bash
# Quick reference (see prettier skill for full details)
npm run format -- <file-path>
```

**❌ NEVER skip formatting or leave unformatted code**

---

### ⚠️ Business Logic Placement (CRITICAL!)

#### ✅ Command Handler (execute() method)

**PUT HERE:** Business validations, complex rules, pre-validation queries,
duplicate checks, external service calls, transformations before persisting.

#### ❌ Service (main() method)

**DO NOT PUT HERE:** Business validations, business rules, pre-validation
queries.

**Services are ONLY for:** Creating aggregate with factory pattern, persisting
via repository, publishing domain events.

#### 🔑 Decision Tree

```
What am I implementing?
│
├─ Validation, business rule, pre-check query
│  └─ ✅ Command Handler (execute method)
│      - Inject repository if you need queries
│      - Add logic BEFORE calling service
│
└─ Persistence, aggregate creation, events
   └─ ✅ Service (main method)
       - NO validations here
       - Only create, persist, publish events
```

For detailed handler and service examples, see [Handler Examples](handlers.md).

---

### ⚠️ @api Handlers Rule (CRITICAL!)

**@api handlers MUST ONLY dispatch commands/queries.** No business logic, no
repository queries, no if/throw logic. See `aurora-cqrs` skill for full details.

---

### ⚠️ Querying with Relations (CRITICAL!)

**BEFORE writing queries that need related data:**

1. ✅ **Read `.aurora.yaml` schema using `aurora-schema` skill**
2. ✅ **Identify relationships in `aggregateProperties`**
3. ✅ **Use `include` in QueryStatement (see `aurora-criteria` skill)**

```typescript
/* #region AI-generated code */
const queryStatement: QueryStatement = {
  where: { id: unitId },
  include: [{ association: 'model' }], // Field name from YAML relationship
};
/* #endregion AI-generated code */
```

**Benefits:** Single query (avoid N+1 problem), better performance.

---

### Marking Custom Code

**Always mark custom code with AI-generated comments:**

```typescript
/* #region AI-generated code */
// Custom logic here
/* #endregion AI-generated code */
```

---

## Detailed References

For detailed code examples, see:

- [Handler Examples](handlers.md) — Command/Query handler examples with business
  logic
- [NestJS Components](nestjs-components.md) — Guards, Interceptors, Pipes,
  Decorators, Exception Filters
- [Common Patterns](patterns.md) — Validation, caching, exception filters,
  custom domain operations
- [Value Objects](value-objects.md) — Value Object construction rules for
  partial updates (provision, status changes)
- [Testing Patterns](testing.md) — Unit test examples

---

## Code Style & Conventions

### Import Order

```typescript
// 1. Node.js
import { readFile } from 'fs/promises';

// 2. NestJS
import { Injectable, Controller } from '@nestjs/common';
import { CommandHandler } from '@nestjs/cqrs';

// 3. External libraries
import { v4 as uuid } from 'uuid';

// 4. Internal (@app, @domain, @infrastructure)
import { UserRepository } from '@infrastructure/iam/user/repositories/user.repository';

// 5. Relative
import { CreateUserCommand } from './create-user.command';
```

### Naming Conventions

| Type        | Pattern                   | Example              |
| ----------- | ------------------------- | -------------------- |
| Command     | `[Action][Entity]Command` | `CreateUserCommand`  |
| Query       | `[Action][Entity]Query`   | `FindUserByIdQuery`  |
| Handler     | `[Action][Entity]Handler` | `CreateUserHandler`  |
| Event       | `[Entity][Action]Event`   | `UserCreatedEvent`   |
| Service     | `[Entity]Service`         | `UserService`        |
| Guard       | `[Purpose]Guard`          | `JwtAuthGuard`       |
| Interceptor | `[Purpose]Interceptor`    | `LoggingInterceptor` |
| Pipe        | `[Purpose]Pipe`           | `ValidationPipe`     |
| Decorator   | `[Purpose]`               | `CurrentUser`        |

### Formatting

- **Indentation**: 4 spaces
- **Braces**: New line for classes/methods
- **Semicolons**: Required
- **Quotes**: Single quotes

---

## Dependency Injection

### Constructor Injection (Preferred)

```typescript
@Injectable()
export class UserService {
  constructor(
    private readonly repository: UserRepository,
    private readonly logger: Logger,
    private readonly eventBus: EventBus,
  ) {}
}
```

### Module Registration

```typescript
@Module({
  imports: [CqrsModule],
  controllers: [UserController],
  providers: [UserService, CreateUserHandler, GetUsersHandler, UserRepository],
  exports: [UserService],
})
export class UserModule {}
```

---

## Decision Trees

### When to use Guard vs Interceptor vs Pipe?

```
Need authentication/authorization?
└─ Use Guard (before route handler)

Need to transform input data?
└─ Use Pipe (before route handler, per parameter)

Need to transform response or add cross-cutting logic?
└─ Use Interceptor (before and after route handler)

Need request/response logging?
└─ Use Middleware or Interceptor

Need to catch and format exceptions?
└─ Use Exception Filter
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
```

---

## Best Practices

### ✅ DO

- Always mark custom code with `/* #region AI-generated code */`
- Put business logic in **handlers**, not services
- Inject repository in handlers if you need pre-validation queries
- Use dependency injection for all dependencies
- Create custom services for reusable logic
- Use guards for authentication/authorization
- Use interceptors for logging/caching
- Use pipes for validation
- Write unit tests for handlers
- Follow NestJS naming conventions
- Use TypeScript strict mode (see `typescript` skill)
- Use enum types from `domain/types/` instead of hardcoded strings for enum
  fields

### ❌ DON'T

- Don't put business logic in services (put in handlers)
- Don't modify generated files (marked with `@aurora-generated`)
- Don't bypass repository (always use repository interface)
- Don't use `any` type (use `unknown` or generics, see `typescript` skill)
- Don't forget to commit events (call `aggregate.commit()`)
- Don't create commands/queries manually (use Aurora CLI)
- Don't mix concerns (keep separation of concerns)

---

## Resources

- **NestJS Docs**: https://docs.nestjs.com
- **CQRS Module**: https://docs.nestjs.com/recipes/cqrs
- **Testing**: https://docs.nestjs.com/fundamentals/testing
- **Aurora CQRS**: `.claude/skills/aurora-cqrs/SKILL.md`
- **TypeScript**: `.claude/skills/typescript/SKILL.md`
- **Aurora CLI**: `.claude/skills/aurora-cli/SKILL.md`
- **Project Structure**: `.claude/skills/aurora-project-structure/SKILL.md`

---

## Related Skills

- `aurora-cqrs` - CQRS architecture reference (structure, editable zones, data
  flow)
- `typescript` - Strict type patterns
- `aurora-project-structure` - File locations
- `aurora-criteria` - QueryStatement for filters
- `jest-nestjs` - Testing patterns
- `supertest-nestjs` - E2E API testing
