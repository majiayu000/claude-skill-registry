---
name: cli-services
description: Effect.Service patterns for CLI infrastructure. Covers service definition, Layer composition, and dependency injection for CLI applications.
model_invoked: true
triggers:
  - "Effect.Service"
  - "CLI service"
  - "Layer composition"
  - "dependency injection CLI"
  - "Context.Tag"
---

# CLI Services Patterns

Effect.Service patterns for building modular, testable CLI infrastructure.

## Quick Start

```typescript
import { Context, Effect, Layer } from "effect"

// 1. Define service interface
interface Logger {
  readonly info: (msg: string) => Effect.Effect<void>
  readonly error: (msg: string) => Effect.Effect<void>
}

// 2. Create service tag
class Logger extends Context.Tag("Logger")<Logger, Logger>() {}

// 3. Implement live layer
const LoggerLive = Layer.succeed(
  Logger,
  Logger.of({
    info: (msg) => Effect.sync(() => console.log(`[INFO] ${msg}`)),
    error: (msg) => Effect.sync(() => console.error(`[ERROR] ${msg}`)),
  })
)

// 4. Use in commands
const myCommand = Command.make("cmd", {}, () =>
  Effect.gen(function* () {
    const logger = yield* Logger
    yield* logger.info("Command started")
  })
)
```

---

## Service Architecture

### Pattern: Full Service Class

```typescript
import { Context, Effect, Layer } from "effect"
import { SqlClient } from "@effect/sql"

// =============================================================================
// SERVICE INTERFACE
// =============================================================================

interface SessionService {
  readonly create: (topic: string) => Effect.Effect<string, CreateError>
  readonly get: (id: string) => Effect.Effect<Session, NotFoundError>
  readonly list: (opts?: ListOptions) => Effect.Effect<Session[]>
  readonly update: (id: string, data: Partial<Session>) => Effect.Effect<Session, NotFoundError>
  readonly delete: (id: string) => Effect.Effect<void, NotFoundError>
}

// =============================================================================
// SERVICE TAG
// =============================================================================

class SessionService extends Context.Tag("SessionService")<
  SessionService,
  SessionService
>() {}

// =============================================================================
// IMPLEMENTATION
// =============================================================================

const SessionServiceLive = Layer.effect(
  SessionService,
  Effect.gen(function* () {
    // Acquire dependencies
    const sql = yield* SqlClient.SqlClient

    // Return implementation
    return SessionService.of({
      create: (topic) =>
        Effect.gen(function* () {
          const id = crypto.randomUUID()
          yield* sql`INSERT INTO sessions (id, topic) VALUES (${id}, ${topic})`
          return id
        }),

      get: (id) =>
        Effect.gen(function* () {
          const rows = yield* sql`SELECT * FROM sessions WHERE id = ${id}`
          if (rows.length === 0) {
            return yield* Effect.fail(new NotFoundError({ id }))
          }
          return rows[0] as Session
        }),

      list: (opts = {}) =>
        Effect.gen(function* () {
          const limit = opts.limit ?? 20
          return yield* sql`SELECT * FROM sessions ORDER BY updated_at DESC LIMIT ${limit}`
        }),

      update: (id, data) =>
        Effect.gen(function* () {
          yield* sql`UPDATE sessions SET topic = COALESCE(${data.topic}, topic) WHERE id = ${id}`
          return yield* SessionService.get(id)
        }),

      delete: (id) =>
        Effect.gen(function* () {
          yield* SessionService.get(id) // Verify exists
          yield* sql`DELETE FROM sessions WHERE id = ${id}`
        }),
    })
  })
)
```

---

## Layer Composition

### Pattern: Service Dependencies

```typescript
// Logger (no dependencies)
const LoggerLive = Layer.succeed(Logger, { /* ... */ })

// Config (no dependencies)
const ConfigLive = Layer.succeed(Config, { /* ... */ })

// Database (depends on Config)
const DatabaseLive = Layer.effect(
  Database,
  Effect.gen(function* () {
    const config = yield* Config
    return yield* createDatabase(config.dbPath)
  })
)

// SessionService (depends on Database + Logger)
const SessionServiceLive = Layer.effect(
  SessionService,
  Effect.gen(function* () {
    const db = yield* Database
    const logger = yield* Logger
    return { /* implementation using db and logger */ }
  })
)
```

### Pattern: Composing Layers

```typescript
// Option 1: mergeAll (parallel composition)
const AppLayer = Layer.mergeAll(
  LoggerLive,
  ConfigLive,
  DatabaseLive,
  SessionServiceLive
)

// Option 2: provideMerge (explicit dependencies)
const AppLayer = SessionServiceLive.pipe(
  Layer.provideMerge(DatabaseLive),
  Layer.provideMerge(LoggerLive),
  Layer.provideMerge(ConfigLive)
)

// Option 3: provide (sequential)
const AppLayer = Layer.provide(
  Layer.provide(SessionServiceLive, DatabaseLive),
  Layer.mergeAll(LoggerLive, ConfigLive)
)
```

### Pattern: Platform Integration

```typescript
import { NodeContext } from "@effect/platform-node"
import { SqliteClient } from "@effect/sql-sqlite-bun"

// CLI needs NodeContext for filesystem, process, etc.
const PlatformLayer = NodeContext.layer

// Database layer
const SqliteLive = SqliteClient.layer({ filename: DB_PATH })

// Full app layer
const AppLayer = Layer.mergeAll(
  PlatformLayer,
  SqliteLive,
  SessionServiceLive,
  LoggerLive
)

// Run program
pipe(
  program,
  Effect.provide(AppLayer),
  NodeRuntime.runMain
)
```

---

## Common CLI Services

### Logger Service

```typescript
interface Logger {
  readonly debug: (msg: string) => Effect.Effect<void>
  readonly info: (msg: string) => Effect.Effect<void>
  readonly warn: (msg: string) => Effect.Effect<void>
  readonly error: (msg: string) => Effect.Effect<void>
}

class Logger extends Context.Tag("Logger")<Logger, Logger>() {}

const LoggerLive = Layer.effect(
  Logger,
  Effect.gen(function* () {
    const config = yield* Config

    const shouldLog = (level: string) => {
      const levels = ["debug", "info", "warn", "error"]
      return levels.indexOf(level) >= levels.indexOf(config.logLevel)
    }

    return Logger.of({
      debug: (msg) =>
        shouldLog("debug")
          ? Effect.sync(() => console.log(`[DEBUG] ${msg}`))
          : Effect.void,
      info: (msg) =>
        shouldLog("info")
          ? Effect.sync(() => console.log(`[INFO] ${msg}`))
          : Effect.void,
      warn: (msg) =>
        shouldLog("warn")
          ? Effect.sync(() => console.warn(`[WARN] ${msg}`))
          : Effect.void,
      error: (msg) =>
        shouldLog("error")
          ? Effect.sync(() => console.error(`[ERROR] ${msg}`))
          : Effect.void,
    })
  })
)
```

### Output Service

```typescript
interface OutputService {
  readonly print: (text: string) => Effect.Effect<void>
  readonly json: <T>(data: T) => Effect.Effect<void>
  readonly table: <T extends Record<string, unknown>>(
    data: T[],
    columns: ColumnDef[]
  ) => Effect.Effect<void>
}

class OutputService extends Context.Tag("OutputService")<
  OutputService,
  OutputService
>() {}

const OutputServiceLive = Layer.effect(
  OutputService,
  Effect.gen(function* () {
    const config = yield* Config

    return OutputService.of({
      print: (text) => Console.log(text),

      json: (data) =>
        Console.log(
          config.prettyPrint
            ? JSON.stringify(data, null, 2)
            : JSON.stringify(data)
        ),

      table: (data, columns) =>
        Console.log(formatTable(data, columns)),
    })
  })
)
```

### FileManager Service

```typescript
import { FileSystem, Path } from "@effect/platform"

interface FileManager {
  readonly read: (path: string) => Effect.Effect<string, FileError>
  readonly write: (path: string, content: string) => Effect.Effect<void, FileError>
  readonly exists: (path: string) => Effect.Effect<boolean>
  readonly ensureDir: (path: string) => Effect.Effect<void>
}

class FileManager extends Context.Tag("FileManager")<
  FileManager,
  FileManager
>() {}

const FileManagerLive = Layer.effect(
  FileManager,
  Effect.gen(function* () {
    const fs = yield* FileSystem.FileSystem
    const path = yield* Path.Path

    return FileManager.of({
      read: (filePath) =>
        fs.readFileString(filePath).pipe(
          Effect.mapError((e) => new FileError({ path: filePath, cause: e }))
        ),

      write: (filePath, content) =>
        Effect.gen(function* () {
          yield* fs.makeDirectory(path.dirname(filePath), { recursive: true })
          yield* fs.writeFileString(filePath, content)
        }).pipe(
          Effect.mapError((e) => new FileError({ path: filePath, cause: e }))
        ),

      exists: (filePath) =>
        fs.exists(filePath),

      ensureDir: (dirPath) =>
        fs.makeDirectory(dirPath, { recursive: true }),
    })
  })
)
```

---

## Testing with Services

### Pattern: Mock Layers

```typescript
import { it, describe, expect } from "@effect/vitest"

// Mock implementation
const LoggerTest = Layer.succeed(
  Logger,
  Logger.of({
    info: () => Effect.void,
    error: () => Effect.void,
  })
)

// In-memory database for tests
const TestDbLayer = SqliteClient.layer({ filename: ":memory:" })

// Test layer composition
const TestLayer = Layer.mergeAll(
  TestDbLayer,
  LoggerTest,
  SessionServiceLive
)

describe("SessionService", () => {
  it.effect("creates a session", () =>
    Effect.gen(function* () {
      const service = yield* SessionService
      const id = yield* service.create("test topic")

      expect(id).toBeDefined()

      const session = yield* service.get(id)
      expect(session.topic).toBe("test topic")
    }).pipe(Effect.provide(TestLayer))
  )
})
```

### Pattern: Test Fixtures

```typescript
const withTestSession = <A, E>(
  effect: (session: Session) => Effect.Effect<A, E>
) =>
  Effect.gen(function* () {
    const service = yield* SessionService

    // Setup
    const id = yield* service.create("test session")
    const session = yield* service.get(id)

    // Run test
    const result = yield* effect(session)

    // Cleanup
    yield* service.delete(id)

    return result
  })

it.effect("updates session", () =>
  withTestSession((session) =>
    Effect.gen(function* () {
      const service = yield* SessionService
      const updated = yield* service.update(session.id, { topic: "new topic" })
      expect(updated.topic).toBe("new topic")
    })
  ).pipe(Effect.provide(TestLayer))
)
```

---

## Service Patterns

### Pattern: Service with State (Ref)

```typescript
import { Ref } from "effect"

interface Counter {
  readonly increment: Effect.Effect<number>
  readonly get: Effect.Effect<number>
  readonly reset: Effect.Effect<void>
}

class Counter extends Context.Tag("Counter")<Counter, Counter>() {}

const CounterLive = Layer.effect(
  Counter,
  Effect.gen(function* () {
    const ref = yield* Ref.make(0)

    return Counter.of({
      increment: Ref.updateAndGet(ref, (n) => n + 1),
      get: Ref.get(ref),
      reset: Ref.set(ref, 0),
    })
  })
)
```

### Pattern: Service with Caching

```typescript
import { Cache } from "effect"

interface CachedSessionService {
  readonly get: (id: string) => Effect.Effect<Session, NotFoundError>
  readonly invalidate: (id: string) => Effect.Effect<void>
}

class CachedSessionService extends Context.Tag("CachedSessionService")<
  CachedSessionService,
  CachedSessionService
>() {}

const CachedSessionServiceLive = Layer.effect(
  CachedSessionService,
  Effect.gen(function* () {
    const sessionService = yield* SessionService

    const cache = yield* Cache.make({
      capacity: 100,
      timeToLive: "5 minutes",
      lookup: (id: string) => sessionService.get(id),
    })

    return CachedSessionService.of({
      get: (id) => cache.get(id),
      invalidate: (id) => cache.invalidate(id),
    })
  })
)
```

### Pattern: Service Accessor Helpers

```typescript
// Instead of yielding service then calling method:
const session = yield* SessionService.pipe(
  Effect.flatMap((s) => s.get(id))
)

// Create accessor
const SessionService = {
  // ... tag definition ...

  // Accessors
  get: (id: string) =>
    Effect.flatMap(SessionService, (s) => s.get(id)),

  create: (topic: string) =>
    Effect.flatMap(SessionService, (s) => s.create(topic)),

  list: (opts?: ListOptions) =>
    Effect.flatMap(SessionService, (s) => s.list(opts)),
}

// Usage is cleaner
const session = yield* SessionService.get(id)
const sessions = yield* SessionService.list()
```

---

## Scope and Resources

### Pattern: Scoped Resources

```typescript
const DatabaseLive = Layer.scoped(
  Database,
  Effect.gen(function* () {
    const config = yield* Config

    // Acquire resource
    const db = yield* Effect.acquireRelease(
      Effect.sync(() => createConnection(config.dbUrl)),
      (conn) => Effect.sync(() => conn.close())
    )

    return Database.of({
      query: (sql) => Effect.sync(() => db.query(sql)),
    })
  })
)
```

### Pattern: Graceful Shutdown

```typescript
const AppLive = Layer.scoped(
  App,
  Effect.gen(function* () {
    const logger = yield* Logger

    yield* logger.info("Application starting...")

    // Register cleanup
    yield* Effect.addFinalizer(() =>
      Effect.gen(function* () {
        yield* logger.info("Application shutting down...")
        yield* flushLogs()
        yield* closeConnections()
      })
    )

    return App.of({ /* ... */ })
  })
)
```

---

## Anti-Patterns

### DON'T: Global mutable state

```typescript
// WRONG
let db: Database | null = null
const getDb = () => db ?? (db = createDb())

// CORRECT - Use service + layer
class Database extends Context.Tag("Database")<...>() {}
const DatabaseLive = Layer.scoped(Database, /* ... */)
```

### DON'T: Service in component

```typescript
// WRONG - Creates new service each render
const MyComponent = () => {
  const service = new SessionService()
  // ...
}

// CORRECT - Use layer, provide at top level
const AppLayer = Layer.mergeAll(SessionServiceLive, /* ... */)
```

### DON'T: Circular dependencies

```typescript
// WRONG - A depends on B, B depends on A
const ALive = Layer.effect(A, Effect.gen(function* () {
  const b = yield* B  // B not available yet!
  return { /* ... */ }
}))

// CORRECT - Extract shared logic to third service
const SharedLive = Layer.succeed(Shared, { /* common logic */ })
const ALive = Layer.effect(A, Effect.flatMap(Shared, /* ... */))
const BLive = Layer.effect(B, Effect.flatMap(Shared, /* ... */))
```

---

## Related Skills

| Skill | Purpose |
|-------|---------|
| `cli/core` | Command definition |
| `cli/persistence` | Storage patterns |
| `cli/messaging` | Error formatting |
| `cli/config` | Configuration patterns |
| `effect-service-authoring` | Deep dive on services |

---

## Quick Reference

| Pattern | Code |
|---------|------|
| Define tag | `class Svc extends Context.Tag("Svc")<Svc, Svc>() {}` |
| Simple layer | `Layer.succeed(Svc, { ...impl })` |
| Layer with deps | `Layer.effect(Svc, Effect.gen(...))` |
| Scoped layer | `Layer.scoped(Svc, Effect.acquireRelease(...))` |
| Compose layers | `Layer.mergeAll(A, B, C)` |
| Provide to program | `Effect.provide(program, layer)` |
| Access service | `yield* MyService` |
| Test mock | `Layer.succeed(Svc, mockImpl)` |
