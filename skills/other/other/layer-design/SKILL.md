---
name: layer-design
description: Design and compose Effect layers for clean dependency management
---

# Layer Design Skill

Create layers that construct services while managing their dependencies cleanly.

## Layer Structure

```typescript
Layer<RequirementsOut, Error, RequirementsIn>
         ▲                ▲           ▲
         │                │           └─ What this layer needs
         │                └─ Errors during construction
         └─ What this layer produces
```

## Pattern: Simple Layer (No Dependencies)

```typescript
export class Config extends Context.Tag("Config")<
  Config,
  {
    readonly getConfig: Effect.Effect<ConfigData>
  }
>() {}

// Layer<Config, never, never>
//         ▲      ▲      ▲
//         │      │      └─ No dependencies
//         │      └─ Cannot fail
//         └─ Produces Config
export const ConfigLive = Layer.succeed(
  Config,
  Config.of({
    getConfig: Effect.succeed({
      logLevel: "INFO",
      connection: "mysql://localhost/db"
    })
  })
)
```

## Pattern: Layer with Dependencies

```typescript
export class Logger extends Context.Tag("Logger")<
  Logger,
  { readonly log: (message: string) => Effect.Effect<void> }
>() {}

// Layer<Logger, never, Config>
//         ▲      ▲      ▲
//         │      │      └─ Needs Config
//         │      └─ Cannot fail
//         └─ Produces Logger
export const LoggerLive = Layer.effect(
  Logger,
  Effect.gen(function* () {
    const config = yield* Config  // Access dependency
    return Logger.of({
      log: (message) =>
        Effect.gen(function* () {
          const { logLevel } = yield* config.getConfig
          console.log(`[${logLevel}] ${message}`)
        })
    })
  })
)
```

## Pattern: Layer with Resource Management

Use `Layer.scoped` for resources that need cleanup:

```typescript
// Layer<Database, DatabaseError, Config>
export const DatabaseLive = Layer.scoped(
  Database,
  Effect.gen(function* () {
    const config = yield* Config

    // Acquire resource with automatic release
    const connection = yield* Effect.acquireRelease(
      connectToDatabase(config),
      (conn) => Effect.sync(() => conn.close())  // Cleanup
    )

    return Database.of({
      query: (sql) => executeQuery(connection, sql)
    })
  })
)
```

## Composing Layers: Merge vs Provide

### Merge (Parallel Composition)

Combine independent layers:

```typescript
// Layer<Config | Logger, never, Config>
//         ▲               ▲      ▲
//         │               │      └─ LoggerLive needs Config
//         │               └─ No errors
//         └─ Produces both Config and Logger
const AppConfigLive = Layer.merge(ConfigLive, LoggerLive)
```

Result combines:
- **Requirements**: Union (`never | Config = Config`)
- **Outputs**: Union (`Config | Logger`)

### Provide (Sequential Composition)

Chain dependent layers:

```typescript
// Layer<Logger, never, never>
//         ▲      ▲      ▲
//         │      │      └─ ConfigLive satisfies LoggerLive's requirement
//         │      └─ No errors
//         └─ Only Logger in output
const FullLoggerLive = Layer.provide(LoggerLive, ConfigLive)
```

Result:
- **Requirements**: Outer layer's requirements (`never`)
- **Output**: Inner layer's output (`Logger`)

## Pattern: Layered Architecture

Build applications in layers:

```typescript
// Infrastructure: No dependencies
const InfrastructureLive = Layer.mergeAll(
  ConfigLive,          // Layer<Config, never, never>
  DatabaseLive,        // Layer<Database, never, Config>
  CacheLive            // Layer<Cache, never, Config>
).pipe(
  Layer.provide(ConfigLive)  // Satisfy Config requirement
)

// Domain: Depends on infrastructure
const DomainLive = Layer.mergeAll(
  PaymentDomainLive,   // Layer<PaymentDomain, never, Database>
  OrderDomainLive,     // Layer<OrderDomain, never, Database>
).pipe(
  Layer.provide(InfrastructureLive)
)

// Application: Depends on domain
const ApplicationLive = Layer.mergeAll(
  PaymentGatewayLive,
  NotificationServiceLive
).pipe(
  Layer.provide(DomainLive)
)
```

## Pattern: Multiple Implementations

Switch implementations for different environments:

```typescript
// Production
export const DatabaseLive = Layer.scoped(
  Database,
  Effect.gen(function* () {
    const connection = yield* connectToProduction()
    return createDatabaseService(connection)
  })
)

// Test
export const DatabaseTest = Layer.succeed(
  Database,
  Database.of({
    query: () => Effect.succeed({ rows: [] })
  })
)

// Use in application
const program = myProgram.pipe(
  Effect.provide(process.env.NODE_ENV === "test" ? DatabaseTest : DatabaseLive)
)
```

## Pattern: Layer Sharing

Layers are memoized - same instance shared across program:

```typescript
// Config is constructed once and shared
const program = Effect.all([
  Effect.gen(function* () {
    const config = yield* Config
    // Uses shared instance
  }),
  Effect.gen(function* () {
    const config = yield* Config
    // Same instance
  })
]).pipe(Effect.provide(ConfigLive))
```

## Error Handling in Layers

Handle construction errors:

```typescript
export const DatabaseLive = Layer.effect(
  Database,
  Effect.gen(function* () {
    const connection = yield* connectToDatabase().pipe(
      Effect.catchTag("ConnectionError", (error) =>
        Effect.fail(new DatabaseConstructionError({ cause: error }))
      )
    )
    return createDatabaseService(connection)
  })
)
```

## Naming Convention

- `*Live` - Production implementation
- `*Test` - Test implementation
- `*Mock` - Mock for testing
- Descriptive names for specialized implementations

## Quality Checklist

- [ ] Layer type accurately reflects dependencies
- [ ] Resource cleanup using `acquireRelease` if needed
- [ ] Layer can be tested with mock dependencies
- [ ] No dependency leakage into service interface
- [ ] Appropriate use of merge vs provide
- [ ] Error handling for construction failures
- [ ] JSDoc with example usage

Layers should make dependency management explicit while keeping service interfaces clean and focused.
