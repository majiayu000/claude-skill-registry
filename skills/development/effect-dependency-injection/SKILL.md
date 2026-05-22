---
name: effect-dependency-injection
description: Use when Effect dependency injection patterns including Context, Layer, service definitions, and dependency composition. Use for managing dependencies in Effect applications.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
---

# Effect Dependency Injection

Master dependency injection and management in Effect applications using Context
and Layers. This skill covers service definitions, layer construction, and
composing complex dependency graphs.

## Context and Services

### Defining Services with Context.Tag

Services are defined using Context.Tag to create type-safe identifiers:

```typescript
import { Context, Effect } from "effect"

// Define service interface
interface UserService {
  getUser: (id: string) => Effect.Effect<User, UserNotFound, never>
  createUser: (data: UserData) => Effect.Effect<User, ValidationError, never>
}

// Create service tag
const UserService = Context.GenericTag<UserService>("UserService")

// Using the service
const program = Effect.gen(function* () {
  const userService = yield* UserService
  const user = yield* userService.getUser("123")
  return user
})
// Effect<User, UserNotFound, UserService>
```

### Multiple Services

```typescript
import { Context, Effect } from "effect"

interface Logger {
  info: (message: string) => Effect.Effect<void, never, never>
  error: (message: string) => Effect.Effect<void, never, never>
}

interface Database {
  query: <T>(sql: string) => Effect.Effect<T, DbError, never>
}

const Logger = Context.GenericTag<Logger>("Logger")
const Database = Context.GenericTag<Database>("Database")

// Using multiple services
const program = Effect.gen(function* () {
  const logger = yield* Logger
  const db = yield* Database

  yield* logger.info("Querying database...")
  const users = yield* db.query<User[]>("SELECT * FROM users")
  yield* logger.info(`Found ${users.length} users`)

  return users
})
// Effect<User[], DbError, Logger | Database>
```

## Creating Layers

Layers are blueprints for constructing services.

### Layer.succeed - Simple Service Implementation

```typescript
import { Context, Effect, Layer } from "effect"

interface Config {
  apiUrl: string
  timeout: number
}

const Config = Context.GenericTag<Config>("Config")

// Create a layer with a fixed value
const ConfigLive = Layer.succeed(
  Config,
  {
    apiUrl: "https://api.example.com",
    timeout: 5000
  }
)
```

### Layer.effect - Service with Dependencies

Create a service that depends on other services:

```typescript
import { Context, Effect, Layer } from "effect"

interface HttpClient {
  get: (url: string) => Effect.Effect<Response, NetworkError, never>
  post: (url: string, body: unknown) => Effect.Effect<Response, NetworkError, never>
}

const HttpClient = Context.GenericTag<HttpClient>("HttpClient")

// HttpClient depends on Config and Logger
const HttpClientLive = Layer.effect(
  HttpClient,
  Effect.gen(function* () {
    const config = yield* Config
    const logger = yield* Logger

    return {
      get: (url: string) =>
        Effect.gen(function* () {
          yield* logger.info(`GET ${url}`)
          const response = yield* Effect.tryPromise({
            try: () => fetch(`${config.apiUrl}${url}`, {
              timeout: config.timeout
            }),
            catch: (error) => ({
              _tag: "NetworkError",
              message: String(error)
            })
          })
          return response
        }),
      post: (url: string, body: unknown) =>
        Effect.gen(function* () {
          yield* logger.info(`POST ${url}`)
          const response = yield* Effect.tryPromise({
            try: () => fetch(`${config.apiUrl}${url}`, {
              method: "POST",
              body: JSON.stringify(body),
              timeout: config.timeout
            }),
            catch: (error) => ({
              _tag: "NetworkError",
              message: String(error)
            })
          })
          return response
        })
    }
  })
)
// Layer<HttpClient, never, Config | Logger>
```

### Layer.scoped - Resources with Cleanup

For services that need cleanup:

```typescript
import { Context, Effect, Layer } from "effect"

interface DatabaseConnection {
  query: <T>(sql: string) => Effect.Effect<T, DbError, never>
}

const DatabaseConnection = Context.GenericTag<DatabaseConnection>("DatabaseConnection")

const DatabaseConnectionLive = Layer.scoped(
  DatabaseConnection,
  Effect.gen(function* () {
    const config = yield* Config

    // Acquire connection
    const connection = yield* Effect.tryPromise({
      try: () => createConnection(config.dbUrl),
      catch: (error) => ({
        _tag: "ConnectionError",
        message: String(error)
      })
    })

    // Register cleanup
    yield* Effect.addFinalizer(() =>
      Effect.sync(() => {
        console.log("Closing database connection")
        connection.close()
      })
    )

    return {
      query: <T>(sql: string) =>
        Effect.tryPromise({
          try: () => connection.query<T>(sql),
          catch: (error) => ({
            _tag: "DbError",
            message: String(error)
          })
        })
    }
  })
)
```

## Providing Layers

### Effect.provide - Provide Single Layer

```typescript
import { Effect, Layer } from "effect"

const program = Effect.gen(function* () {
  const config = yield* Config
  return config.apiUrl
})
// Effect<string, never, Config>

// Provide the Config layer
const runnable = program.pipe(
  Effect.provide(ConfigLive)
)
// Effect<string, never, never>

// Now can run without dependencies
const result = await Effect.runPromise(runnable)
```

### Effect.provideService - Provide Service Directly

For testing or simple cases:

```typescript
import { Effect } from "effect"

const testConfig: Config = {
  apiUrl: "http://localhost:3000",
  timeout: 1000
}

const program = Effect.gen(function* () {
  const config = yield* Config
  return config.apiUrl
})

const runnable = program.pipe(
  Effect.provideService(Config, testConfig)
)
```

## Composing Layers

### Layer.provide - Layer Dependencies

Provide dependencies to a layer:

```typescript
import { Layer } from "effect"

// UserServiceLive needs HttpClient
// HttpClient needs Config and Logger

const UserServiceLive = Layer.effect(
  UserService,
  Effect.gen(function* () {
    const http = yield* HttpClient

    return {
      getUser: (id: string) =>
        Effect.gen(function* () {
          const response = yield* http.get(`/users/${id}`)
          const user = yield* Effect.tryPromise({
            try: () => response.json(),
            catch: () => ({ _tag: "ParseError" })
          })
          return user
        })
    }
  })
)

// Provide HttpClient to UserService
const UserServiceWithDeps = UserServiceLive.pipe(
  Layer.provide(HttpClientLive)
)
// Layer<UserService, never, Config | Logger>
```

### Layer.merge - Combine Layers

Merge multiple independent layers:

```typescript
import { Layer } from "effect"

// Combine Config and Logger
const AppConfigLayer = Layer.merge(
  ConfigLive,
  LoggerLive
)
// Layer<Config | Logger, never, never>

// Use merged layer
const program = Effect.gen(function* () {
  const config = yield* Config
  const logger = yield* Logger
  yield* logger.info(`API URL: ${config.apiUrl}`)
})

const runnable = program.pipe(
  Effect.provide(AppConfigLayer)
)
```

### Layer Pipelines

Build complex dependency graphs:

```typescript
import { Layer, Effect } from "effect"

// Build dependency graph
const AppLayer = Layer.merge(
  ConfigLive,
  LoggerLive
).pipe(
  Layer.provideMerge(HttpClientLive),
  Layer.provideMerge(DatabaseConnectionLive),
  Layer.provideMerge(UserServiceLive)
)

// All services now available
const program = Effect.gen(function* () {
  const userService = yield* UserService
  const logger = yield* Logger

  yield* logger.info("Fetching user...")
  const user = yield* userService.getUser("123")
  yield* logger.info(`User: ${user.name}`)

  return user
})

const runnable = program.pipe(
  Effect.provide(AppLayer)
)
```

## Service Patterns

### Repository Pattern

```typescript
import { Context, Effect, Layer } from "effect"

interface UserRepository {
  findById: (id: string) => Effect.Effect<Option<User>, DbError, never>
  save: (user: User) => Effect.Effect<User, DbError, never>
  delete: (id: string) => Effect.Effect<void, DbError, never>
}

const UserRepository = Context.GenericTag<UserRepository>("UserRepository")

const UserRepositoryLive = Layer.effect(
  UserRepository,
  Effect.gen(function* () {
    const db = yield* Database

    return {
      findById: (id: string) =>
        Effect.gen(function* () {
          const rows = yield* db.query<User[]>(
            `SELECT * FROM users WHERE id = ?`,
            [id]
          )
          return rows.length > 0 ? Option.some(rows[0]) : Option.none()
        }),

      save: (user: User) =>
        db.query(
          `INSERT INTO users (id, name, email) VALUES (?, ?, ?)`,
          [user.id, user.name, user.email]
        ).pipe(
          Effect.map(() => user)
        ),

      delete: (id: string) =>
        db.query(`DELETE FROM users WHERE id = ?`, [id]).pipe(
          Effect.asVoid
        )
    }
  })
)
```

### Service Facade Pattern

```typescript
import { Context, Effect, Layer } from "effect"

// High-level service that coordinates multiple services
interface UserFacade {
  registerUser: (data: UserData) => Effect.Effect<User, ValidationError | DbError | NetworkError, never>
  getUserProfile: (id: string) => Effect.Effect<UserProfile, NotFoundError | DbError, never>
}

const UserFacade = Context.GenericTag<UserFacade>("UserFacade")

const UserFacadeLive = Layer.effect(
  UserFacade,
  Effect.gen(function* () {
    const userRepo = yield* UserRepository
    const emailService = yield* EmailService
    const logger = yield* Logger

    return {
      registerUser: (data: UserData) =>
        Effect.gen(function* () {
          yield* logger.info(`Registering user: ${data.email}`)

          const user = yield* userRepo.save({
            id: generateId(),
            ...data
          })

          yield* emailService.sendWelcomeEmail(user.email)
          yield* logger.info(`User registered: ${user.id}`)

          return user
        }),

      getUserProfile: (id: string) =>
        Effect.gen(function* () {
          const userOption = yield* userRepo.findById(id)

          if (Option.isNone(userOption)) {
            return yield* Effect.fail({
              _tag: "NotFoundError",
              id
            })
          }

          const user = userOption.value
          const posts = yield* postRepo.findByUserId(user.id)

          return {
            user,
            posts,
            postCount: posts.length
          }
        })
    }
  })
)
```

## Testing with Layers

### Creating Test Layers

```typescript
import { Context, Effect, Layer, Ref } from "effect"

// In-memory test implementation
const UserRepositoryTest = Layer.effect(
  UserRepository,
  Effect.gen(function* () {
    const storage = yield* Ref.make<Map<string, User>>(new Map())

    return {
      findById: (id: string) =>
        storage.get.pipe(
          Effect.map(map => {
            const user = map.get(id)
            return user ? Option.some(user) : Option.none()
          })
        ),

      save: (user: User) =>
        storage.update(map => map.set(user.id, user)).pipe(
          Effect.map(() => user)
        ),

      delete: (id: string) =>
        storage.update(map => {
          map.delete(id)
          return map
        }).pipe(Effect.asVoid)
    }
  })
)

// Mock logger for tests
const LoggerTest = Layer.succeed(
  Logger,
  {
    info: (message) => Effect.sync(() => { /* no-op */ }),
    error: (message) => Effect.sync(() => { /* no-op */ })
  }
)

// Test layer composition
const TestLayer = Layer.merge(
  UserRepositoryTest,
  LoggerTest
)

// Use in tests
const testProgram = Effect.gen(function* () {
  const repo = yield* UserRepository
  const user = yield* repo.save({ id: "1", name: "Test", email: "test@example.com" })
  const found = yield* repo.findById("1")
  return found
}).pipe(
  Effect.provide(TestLayer)
)

const result = await Effect.runPromise(testProgram)
```

### Spy Layers for Testing

```typescript
import { Context, Effect, Layer, Ref } from "effect"

interface LoggerSpy {
  readonly logger: Logger
  readonly infoMessages: Ref.Ref<string[]>
  readonly errorMessages: Ref.Ref<string[]>
}

const LoggerSpy = Context.GenericTag<LoggerSpy>("LoggerSpy")

const LoggerSpyLive = Layer.effect(
  LoggerSpy,
  Effect.gen(function* () {
    const infoMessages = yield* Ref.make<string[]>([])
    const errorMessages = yield* Ref.make<string[]>([])

    const logger: Logger = {
      info: (message) =>
        infoMessages.update(msgs => [...msgs, message]),
      error: (message) =>
        errorMessages.update(msgs => [...msgs, message])
    }

    return {
      logger,
      infoMessages,
      errorMessages
    }
  })
)

// Use in test
const testWithSpy = Effect.gen(function* () {
  const spy = yield* LoggerSpy
  const logger = spy.logger

  yield* logger.info("Test message")

  const messages = yield* spy.infoMessages.get
  expect(messages).toEqual(["Test message"])
}).pipe(
  Effect.provide(LoggerSpyLive)
)
```

## Advanced Patterns

### Optional Dependencies

```typescript
import { Context, Effect, Option } from "effect"

interface CacheService {
  get: (key: string) => Effect.Effect<Option<string>, never, never>
  set: (key: string, value: string) => Effect.Effect<void, never, never>
}

const CacheService = Context.GenericTag<CacheService>("CacheService")

// Service that can work with or without cache
const getUserWithOptionalCache = (id: string) =>
  Effect.gen(function* () {
    const cache = yield* Effect.serviceOption(CacheService)

    if (Option.isSome(cache)) {
      const cached = yield* cache.value.get(`user:${id}`)
      if (Option.isSome(cached)) {
        return JSON.parse(cached.value)
      }
    }

    const user = yield* fetchUserFromDb(id)

    if (Option.isSome(cache)) {
      yield* cache.value.set(`user:${id}`, JSON.stringify(user))
    }

    return user
  })
```

### Environment-Based Layers

```typescript
import { Layer } from "effect"

const getConfigLayer = (env: "development" | "production") => {
  if (env === "production") {
    return Layer.succeed(Config, {
      apiUrl: "https://api.production.com",
      timeout: 10000
    })
  } else {
    return Layer.succeed(Config, {
      apiUrl: "http://localhost:3000",
      timeout: 5000
    })
  }
}

const AppLayer = getConfigLayer(process.env.NODE_ENV as any).pipe(
  Layer.provideMerge(LoggerLive),
  Layer.provideMerge(HttpClientLive)
)
```

## Best Practices

1. **Define Service Interfaces**: Always define clear interfaces for services.

2. **Use Context.GenericTag**: Create service tags for type-safe access.

3. **Layer Composition**: Build complex dependency graphs through layer
   composition.

4. **Separate Concerns**: Keep service interfaces focused and single-purpose.

5. **Test with Mock Layers**: Create test implementations for easy testing.

6. **Document Dependencies**: Make service dependencies explicit in types.

7. **Resource Management**: Use Layer.scoped for services needing cleanup.

8. **Avoid Circular Dependencies**: Design layers to avoid circular references.

9. **Environment Configuration**: Use layers to switch implementations by
   environment.

10. **Type Safety**: Leverage Effect's type system to catch dependency issues at
    compile time.

## Common Pitfalls

1. **Circular Dependencies**: Creating layers that depend on each other.

2. **Missing Layers**: Forgetting to provide required layers.

3. **Over-Abstraction**: Creating too many tiny services unnecessarily.

4. **Not Using scoped**: Forgetting cleanup for resources like database
   connections.

5. **Mixing Live and Test Layers**: Accidentally using production services in
   tests.

6. **Global State in Services**: Storing mutable state incorrectly in service
   implementations.

7. **Ignoring Type Errors**: Not paying attention to the R (Requirements) type
   parameter.

8. **Heavy Layers**: Creating layers that do too much during construction.

9. **Not Reusing Layers**: Recreating the same layer in multiple places.

10. **Wrong Layer Scope**: Not understanding when layers are constructed and
    torn down.

## When to Use This Skill

Use effect-dependency-injection when you need to:

- Manage complex dependency graphs
- Build testable applications with Effect
- Implement repository patterns
- Create service facades
- Handle resource lifecycle (acquire/release)
- Switch implementations by environment
- Mock dependencies for testing
- Build modular, composable applications
- Ensure type-safe dependency injection
- Manage application configuration

## Resources

### Official Documentation

- [Context Management](https://effect.website/docs/guides/context-management/)
- [Layers](https://effect.website/docs/guides/context-management/layers)
- [Services](https://effect.website/docs/guides/context-management/services)
- [Managing Services](https://effect.website/docs/guides/context-management/managing-services)

### Related Skills

- effect-core-patterns - Basic Effect operations
- effect-testing - Testing with Effect
- effect-resource-management - Resource cleanup patterns
