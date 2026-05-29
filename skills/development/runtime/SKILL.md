---
name: Runtime
description: This skill should be used when the user asks about "Effect Runtime", "ManagedRuntime", "Effect.Tag", "custom runtime", "runtime layers", "running effects", "runtime configuration", "runtime context", "Effect.runPromise", "Effect.runSync", "runtime scope", or needs to understand how Effect's runtime system executes effects.
version: 1.0.0
---

# Runtime in Effect

## Overview

The Runtime is Effect's execution engine:

- **Default Runtime** - Built-in, zero configuration
- **Custom Runtime** - Configure services, context, execution
- **ManagedRuntime** - Lifecycle-managed custom runtimes

## Default Runtime

Effects run via the default runtime:

```typescript
import { Effect } from "effect"

const program = Effect.succeed(42)

const result = await Effect.runPromise(program)

const syncResult = Effect.runSync(program)

const exit = await Effect.runPromiseExit(program)
```

### Run Methods

| Method | Returns | Throws on Error |
|--------|---------|-----------------|
| `Effect.runPromise(e)` | `Promise<A>` | Yes |
| `Effect.runPromiseExit(e)` | `Promise<Exit<A, E>>` | No |
| `Effect.runSync(e)` | `A` | Yes |
| `Effect.runSyncExit(e)` | `Exit<A, E>` | No |

## Locally Scoped Configuration

Modify runtime behavior for specific effects:

```typescript
import { Logger, LogLevel } from "effect"

const program = Effect.gen(function* () {
  yield* Effect.log("This appears")
  yield* Effect.logDebug("This may not appear")
})

const withDebug = program.pipe(
  Logger.withMinimumLogLevel(LogLevel.Debug)
)
```

## Effect.Tag for Services

Create typed service tags for dependency injection:

```typescript
import { Effect, Context } from "effect"

class Database extends Context.Tag("Database")<
  Database,
  {
    readonly query: (sql: string) => Effect.Effect<unknown[]>
    readonly execute: (sql: string) => Effect.Effect<void>
  }
>() {}

const program = Effect.gen(function* () {
  const db = yield* Database
  const users = yield* db.query("SELECT * FROM users")
  return users
})
```

## ManagedRuntime

For applications needing custom runtime configuration:

```typescript
import { ManagedRuntime, Layer } from "effect"

const AppLive = Layer.mergeAll(
  DatabaseLive,
  LoggerLive,
  ConfigLive
)

const runtime = ManagedRuntime.make(AppLive)

const main = async () => {
  const result = await runtime.runPromise(program)
  console.log(result)

  await runtime.dispose()
}
```

### ManagedRuntime Benefits

- Pre-builds layer once
- Reuses services across effect runs
- Proper cleanup with dispose()
- Integration with frameworks

## Framework Integration

### Express Integration

```typescript
import express from "express"
import { ManagedRuntime, Layer } from "effect"

const AppLive = Layer.mergeAll(DatabaseLive, AuthLive)
const runtime = ManagedRuntime.make(AppLive)

const app = express()

app.get("/users", async (req, res) => {
  const result = await runtime.runPromise(
    getUsers().pipe(
      Effect.catchAll((error) =>
        Effect.succeed({ error: error.message })
      )
    )
  )
  res.json(result)
})

// Cleanup on shutdown
process.on("SIGTERM", () => {
  runtime.dispose().then(() => process.exit(0))
})
```

### React Integration

```typescript
import { ManagedRuntime } from "effect"
import { createContext, useContext } from "react"

// Create runtime context
const RuntimeContext = createContext<ManagedRuntime<AppServices> | null>(null)

// Provider component
export function AppProvider({ children }: { children: React.ReactNode }) {
  const [runtime] = useState(() => ManagedRuntime.make(AppLive))

  useEffect(() => {
    return () => { runtime.dispose() }
  }, [])

  return (
    <RuntimeContext.Provider value={runtime}>
      {children}
    </RuntimeContext.Provider>
  )
}

// Hook to use runtime
export function useRuntime() {
  const runtime = useContext(RuntimeContext)
  if (!runtime) throw new Error("Runtime not provided")
  return runtime
}

// Usage in components
function UserList() {
  const runtime = useRuntime()
  const [users, setUsers] = useState<User[]>([])

  useEffect(() => {
    runtime.runPromise(fetchUsers()).then(setUsers)
  }, [])

  return <ul>{users.map(u => <li key={u.id}>{u.name}</li>)}</ul>
}
```

## Runtime Configuration

### Custom Execution Context

```typescript
import { Runtime, FiberRef } from "effect"

const customRuntime = Runtime.defaultRuntime.pipe(
  Runtime.withFiberRef(FiberRef.currentLogLevel, LogLevel.Debug)
)

Runtime.runPromise(customRuntime)(program)
```

### Providing Services to Runtime

```typescript
const runtimeWithServices = Runtime.defaultRuntime.pipe(
  Runtime.provideService(Database, databaseImpl),
  Runtime.provideService(Logger, loggerImpl)
)
```

## Default Services

Effect provides these services automatically:

```typescript
import { Clock, Random, Tracer, Console } from "effect"

const program = Effect.gen(function* () {
  const now = yield* Clock.currentTimeMillis

  const rand = yield* Random.next

  yield* Console.log("Hello")
})
```

### Overriding Default Services

```typescript
import { TestClock } from "effect"

const testProgram = program.pipe(
  Effect.provide(TestClock.layer)
)

const testWithTime = Effect.gen(function* () {
  const fiber = yield* Effect.fork(Effect.sleep("1 hour"))
  yield* TestClock.adjust("1 hour")
  yield* Fiber.join(fiber)
})
```

## Interruption Handling

```typescript
const program = Effect.gen(function* () {
  const fiber = yield* Effect.fork(longRunningTask)

  yield* Fiber.interrupt(fiber)
})

const critical = Effect.uninterruptible(
  Effect.gen(function* () {
    yield* startTransaction()
    yield* doWork()
    yield* commitTransaction()
  })
)
```

## Best Practices

1. **Use ManagedRuntime for apps** - Proper lifecycle management
2. **Provide services via layers** - Not runtime modification
3. **Use Effect.Tag for services** - Type-safe dependency injection
4. **Handle cleanup properly** - Always dispose() ManagedRuntime
5. **Test with TestClock** - Deterministic time in tests

## Additional Resources

For comprehensive runtime documentation, consult `${CLAUDE_PLUGIN_ROOT}/references/llms-full.txt`.

Search for these sections:
- "Introduction to Runtime" for core concepts
- "ManagedRuntime" for managed runtime
- "Effect.Tag" for service tags
- "Integrations" for framework integration
