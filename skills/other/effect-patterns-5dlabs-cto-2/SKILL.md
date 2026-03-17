---
name: effect-patterns
description: Effect TypeScript patterns including services, layers, schema validation, and Elysia integration.
agents: [nova]
triggers: [effect, elysia, bun, typescript backend]
llm_docs:
  - effect
  - drizzle
  - elysia
  - bun
  - zod
---

# Effect TypeScript Patterns

Type-safe error handling and composable services using Effect as the core type system for Node.js/Bun backends.

## Core Stack

| Component | Library | Purpose |
|-----------|---------|---------|
| Runtime | Bun 1.1+ | Fastest Node.js-compatible runtime |
| Framework | Elysia 1.x | End-to-end type safety |
| Type System | Effect 3.x | TypeScript's missing standard library |
| Validation | Effect Schema | Type-safe validation (replaces Zod) |
| HTTP Client | @effect/platform | HTTP operations |
| Database | Drizzle ORM | TypeScript ORM |
| Testing | Vitest, bun:test | Test framework |

## Context7 Library IDs

Query these libraries for current best practices:

- **Effect**: `/effect-ts/effect`
- **Elysia**: `elysiajs`
- **Drizzle**: `/drizzle-team/drizzle-orm`

## Effect Documentation

Before implementing Effect code, consult:
- **AI Documentation**: `https://effect.website/llms.txt`
- **Main Docs**: `https://effect.website/docs`

## Typed Errors

Define errors as classes extending `Schema.TaggedError`:

```typescript
import { Schema } from "effect"

class UserNotFoundError extends Schema.TaggedError<UserNotFoundError>("UserNotFoundError")({
  userId: Schema.String,
}) {}

class ValidationError extends Schema.TaggedError<ValidationError>("ValidationError")({
  message: Schema.String,
  field: Schema.String,
}) {}

class DatabaseError extends Schema.TaggedError<DatabaseError>("DatabaseError")({
  message: Schema.String,
}) {}
```

## Services with Context.Tag

Define services with typed interfaces:

```typescript
import { Effect, Context, Layer } from "effect"

class UserRepository extends Context.Tag("UserRepository")<
  UserRepository,
  {
    findById: (id: string) => Effect.Effect<User, UserNotFoundError>
    create: (data: CreateUser) => Effect.Effect<User, ValidationError>
  }
>() {}

class DatabaseService extends Context.Tag("DatabaseService")<
  DatabaseService,
  { query: <T>(sql: string) => Effect.Effect<T[], DatabaseError> }
>() {}
```

## Layer Implementation

Implement services with Layer:

```typescript
const UserRepositoryLive = Layer.succeed(
  UserRepository,
  UserRepository.of({
    findById: (id) => Effect.tryPromise({
      try: () => db.findUser(id),
      catch: () => new UserNotFoundError({ userId: id })
    }),
    create: (data) => Effect.tryPromise({
      try: () => db.createUser(data),
      catch: (e) => new ValidationError({ message: String(e), field: "unknown" })
    })
  })
)

const DatabaseServiceLive = Layer.succeed(
  DatabaseService,
  DatabaseService.of({
    query: (sql) => Effect.tryPromise({
      try: () => db.query(sql),
      catch: (e) => new DatabaseError({ message: String(e) })
    })
  })
)
```

## Effect.gen for Composition

Use generator syntax for composable logic:

```typescript
const getUser = (id: string) =>
  Effect.gen(function* () {
    const repo = yield* UserRepository
    const user = yield* repo.findById(id)
    return user
  })

const createUserWithAudit = (data: CreateUser) =>
  Effect.gen(function* () {
    const repo = yield* UserRepository
    const user = yield* repo.create(data)
    yield* Effect.log(`Created user: ${user.id}`)
    return user
  })
```

## Schema Validation

Use Effect Schema for validation:

```typescript
import { Schema } from "effect"

const CreateUserSchema = Schema.Struct({
  name: Schema.String.pipe(Schema.minLength(1), Schema.maxLength(100)),
  email: Schema.String.pipe(Schema.pattern(/^[^@]+@[^@]+\.[^@]+$/)),
  age: Schema.optional(Schema.Number.pipe(Schema.int(), Schema.positive())),
})
type CreateUser = Schema.Schema.Type<typeof CreateUserSchema>

// Validate unknown data
const validateUser = Schema.decodeUnknown(CreateUserSchema)
```

## Error Handling with catchTags

Pattern match on typed errors:

```typescript
const result = await Effect.runPromise(
  program.pipe(
    Effect.catchTags({
      UserNotFoundError: (e) => Effect.succeed({ error: `User ${e.userId} not found` }),
      ValidationError: (e) => Effect.succeed({ error: `Invalid ${e.field}: ${e.message}` }),
      DatabaseError: (e) => Effect.succeed({ error: `Database error: ${e.message}` }),
    })
  )
)
```

## Retry with Schedule

```typescript
import { Effect, Schedule } from "effect"

const fetchWithRetry = Effect.retry(
  fetchExternalApi,
  Schedule.exponential("1 second").pipe(Schedule.compose(Schedule.recurs(3)))
)
```

## Elysia + Effect Integration

```typescript
import { Elysia, t } from "elysia"
import { Effect } from "effect"

const app = new Elysia()
  .post("/api/users", async ({ body }) => {
    const program = Effect.gen(function* () {
      const validated = yield* Schema.decodeUnknown(CreateUserSchema)(body)
      const repo = yield* UserRepository
      return yield* repo.create(validated)
    })
    
    return Effect.runPromise(
      program.pipe(
        Effect.provide(UserRepositoryLive),
        Effect.catchAll((e) => Effect.succeed({ error: e.message }))
      )
    )
  }, {
    body: t.Object({
      name: t.String(),
      email: t.String({ format: "email" }),
    })
  })
```

## Testing with Effect

```typescript
import { Effect, Layer } from "effect"

const TestUserRepository = Layer.succeed(
  UserRepository,
  UserRepository.of({
    findById: (id) => 
      id === "123" 
        ? Effect.succeed({ id: "123", name: "Test User" })
        : Effect.fail(new UserNotFoundError({ userId: id })),
    create: (data) => Effect.succeed({ id: "new", ...data })
  })
)

// In tests
const result = await Effect.runPromise(
  getUser("123").pipe(Effect.provide(TestUserRepository))
)
```

## Validation Commands

```bash
bun tsc --noEmit
bun eslint src/
bun test
bun build src/index.ts --outdir=dist
```

## Guidelines

- Always define typed errors with Schema.TaggedError
- Use Context.Tag for all services
- Implement services with Layer.succeed
- Compose logic with Effect.gen
- Use Schema for all validation
- Pattern match errors with catchTags
- Provide layers at the edge of the application
