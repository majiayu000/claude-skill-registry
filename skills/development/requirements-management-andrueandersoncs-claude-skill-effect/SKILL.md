---
name: Requirements Management
description: This skill should be used when the user asks about "Effect services", "dependency injection", "Effect.Tag", "Context.Tag", "Layer", "Effect.provide", "Effect.provideService", "service implementation", "managing dependencies", "Layer.succeed", "Layer.effect", "Layer.scoped", "composing layers", "Layer.merge", "Layer.provide", "default services", "layer memoization", "testability", "test layers", "mock services", or needs to understand how Effect handles the Requirements (R) type parameter.
version: 1.1.0
---

# Requirements Management in Effect

## Overview

The third type parameter in `Effect<A, E, R>` represents **requirements** - services and dependencies the effect needs to run:

```typescript
Effect<Success, Error, Requirements>
//                     ^^^^^^^^^^^^ Services needed
```

Effect uses a powerful dependency injection system based on `Context` and `Layer`.

**The primary reason to define services is testability.** Every external dependency (API calls, databases, file systems, third-party SDKs) MUST be wrapped in a `Context.Tag` service so that tests can provide a test implementation instead of hitting real systems. This is how Effect achieves 100% test coverage — business logic depends only on service interfaces, and tests swap in test layers that control all I/O.

## Defining Services

### Using Effect.Tag (Recommended)

```typescript
import { Effect, Context } from "effect"

// Define service interface and tag together
class UserRepository extends Context.Tag("UserRepository")<
  UserRepository,
  {
    readonly findById: (id: string) => Effect.Effect<User, UserNotFound>
    readonly save: (user: User) => Effect.Effect<void>
  }
>() {}

// Using the service
const program = Effect.gen(function* () {
  const repo = yield* UserRepository
  const user = yield* repo.findById("123")
  return user
})
// Type: Effect<User, UserNotFound, UserRepository>
```

### Alternative: Context.Tag Directly

```typescript
interface UserRepository {
  readonly findById: (id: string) => Effect.Effect<User, UserNotFound>
}

const UserRepository = Context.Tag<UserRepository>("UserRepository")
```

## Using Services

```typescript
const program = Effect.gen(function* () {
  const userRepo = yield* UserRepository
  const emailService = yield* EmailService

  const user = yield* userRepo.findById(userId)
  yield* emailService.send(user.email, "Welcome!")
})
```

## Creating Layers

Layers are recipes for building services:

### Layer.succeed - Simple Value

```typescript
const LoggerLive = Layer.succeed(
  Logger,
  {
    log: (msg) => Effect.sync(() => console.log(msg))
  }
)
```

### Layer.effect - Effect-Based Construction

```typescript
const ConfigLive = Layer.effect(
  Config,
  Effect.gen(function* () {
    const env = yield* Effect.sync(() => process.env)
    return {
      apiUrl: env.API_URL ?? "http://localhost:3000",
      debug: env.DEBUG === "true"
    }
  })
)
```

### Layer.scoped - Resource with Lifecycle

```typescript
const DatabaseLive = Layer.scoped(
  Database,
  Effect.gen(function* () {
    const pool = yield* Effect.acquireRelease(
      createPool(),
      (pool) => Effect.promise(() => pool.end())
    )
    return {
      query: (sql) => Effect.promise(() => pool.query(sql))
    }
  })
)
```

### Layer.function - From Function

```typescript
const HttpClientLive = Layer.function(
  HttpClient,
  (baseUrl: string) => ({
    get: (path) => Effect.tryPromise(() => fetch(baseUrl + path))
  })
)
```

## Providing Dependencies

### Effect.provide - Provide Layer

```typescript
const program = getUserById("123")

const runnable = program.pipe(
  Effect.provide(AppLive)
)

await Effect.runPromise(runnable)
```

### Effect.provideService - Provide Single Service

```typescript
const runnable = program.pipe(
  Effect.provideService(UserRepository, {
    findById: (id) => Effect.succeed(mockUser),
    save: (user) => Effect.void
  })
)
```

## Composing Layers

### Layer.merge - Combine Independent Layers

```typescript
const InfraLive = Layer.merge(
  DatabaseLive,
  LoggerLive
)
```

### Layer.provide - Layer Dependencies

```typescript
const UserRepositoryLive = Layer.effect(
  UserRepository,
  Effect.gen(function* () {
    const db = yield* Database
    return {
      findById: (id) => db.query(`SELECT * FROM users WHERE id = ${id}`)
    }
  })
)

const FullUserRepo = UserRepositoryLive.pipe(
  Layer.provide(DatabaseLive)
)
```

### Layer.provideMerge - Provide and Keep

```typescript
const Combined = UserRepositoryLive.pipe(
  Layer.provideMerge(DatabaseLive)
)
```

## Building Application Layers

### Typical Pattern

```typescript
const InfraLive = Layer.mergeAll(
  DatabaseLive,
  LoggerLive,
  HttpClientLive
)

const RepositoryLive = Layer.mergeAll(
  UserRepositoryLive,
  OrderRepositoryLive
).pipe(Layer.provide(InfraLive))

const ServiceLive = Layer.mergeAll(
  UserServiceLive,
  OrderServiceLive
).pipe(Layer.provide(RepositoryLive))

const AppLive = ServiceLive.pipe(
  Layer.provide(InfraLive)
)
```

## Layer Memoization

Layers are memoized by default - each service is created once:

```typescript
const AppLive = Layer.mergeAll(
  UserServiceLive,
  OrderServiceLive
).pipe(Layer.provide(DatabaseLive))
```

### Fresh Layers (No Memoization)

```typescript
const FreshDatabase = Layer.fresh(DatabaseLive)
```

## Default Services

Effect provides default implementations for common services:

```typescript
const program = Effect.gen(function* () {
  const now = yield* Clock.currentTimeMillis
  const random = yield* Random.next
})
```

### Overriding Defaults

```typescript
import { TestClock } from "effect"

const testProgram = program.pipe(
  Effect.provide(TestClock.layer)
)
```

## Testing with Services (CRITICAL for 100% Coverage)

**Every service MUST have a test layer.** This is how you achieve complete test coverage without hitting real external systems.

### Simple Test Layer (Stateless)

Use `Layer.succeed` for services that don't need to track state:

```typescript
const EmailServiceTest = Layer.succeed(EmailService, {
  send: (to, subject, body) => Effect.void, // No-op in tests
  sendBulk: (recipients, subject, body) => Effect.void
})
```

### Stateful Test Layer (Repositories)

Use `Layer.effect` with `Ref` for services that need to maintain state:

```typescript
const UserRepositoryTest = Layer.effect(
  UserRepository,
  Effect.gen(function* () {
    const store = yield* Ref.make<Map<string, User>>(new Map())

    return {
      findById: (id: string) =>
        Effect.gen(function* () {
          const users = yield* Ref.get(store)
          return yield* Option.match(Option.fromNullable(users.get(id)), {
            onNone: () => Effect.fail(new UserNotFound({ userId: id })),
            onSome: Effect.succeed
          }).pipe(Effect.flatten)
        }),
      save: (user: User) =>
        Ref.update(store, (m) => new Map(m).set(user.id, user))
    }
  })
)
```

### Composing Test Layers

```typescript
const TestEnv = Layer.mergeAll(
  UserRepositoryTest,
  EmailServiceTest,
  PaymentGatewayTest
)
```

### Using Test Layers with @effect/vitest

```typescript
import { it, expect, layer } from "@effect/vitest"
import { Effect } from "effect"

layer(TestEnv)("UserService", (it) => {
  it.effect("should create user and send welcome email", () =>
    Effect.gen(function* () {
      const repo = yield* UserRepository
      const email = yield* EmailService

      const user = new User({ id: "1", name: "Alice", email: "alice@test.com" })
      yield* repo.save(user)
      yield* email.send(user.email, "Welcome!", "Hello Alice")

      const found = yield* repo.findById("1")
      expect(found.name).toBe("Alice")
    })
  )
})
```

### Combining Test Layers with Property Testing

The ultimate testing pattern — service test layers control all I/O, Arbitrary generates all data:

```typescript
layer(TestEnv)("UserService Properties", (it) => {
  it.effect.prop(
    "should save and retrieve any valid user",
    [Arbitrary.make(User)],
    ([user]) =>
      Effect.gen(function* () {
        const repo = yield* UserRepository
        yield* repo.save(user)
        const found = yield* repo.findById(user.id)
        expect(found).toEqual(user)
      })
  )
})
```

## Best Practices

1. **Define service interface with Tag** - Keeps interface and tag together
2. **ALWAYS create a test layer for every service** - This is required, not optional. Without test layers, your code is untestable.
3. **Wrap ALL external dependencies in services** - API calls, database queries, file I/O, third-party SDKs, email, caches, queues — everything external MUST go through a service
4. **Use Layer.scoped for resources** - Ensures proper cleanup
5. **Compose layers bottom-up** - Infrastructure → Repositories → Services
6. **Keep layers focused** - One service per layer typically
7. **Name convention** - `*Live` for production layers, `*Test` for test layers (e.g., `UserRepositoryLive`, `UserRepositoryTest`)
8. **Use `Layer.effect` with `Ref` for stateful test layers** - Repositories and caches need state tracking
9. **Combine test layers with Arbitrary** - Services control I/O, Arbitrary generates data — together they enable 100% coverage

## Additional Resources

For comprehensive requirements management documentation, consult `${CLAUDE_PLUGIN_ROOT}/references/llms-full.txt`.

Search for these sections:
- "Managing Services" for service patterns
- "Managing Layers" for layer composition
- "Layer Memoization" for sharing services
- "Default Services" for built-in services
