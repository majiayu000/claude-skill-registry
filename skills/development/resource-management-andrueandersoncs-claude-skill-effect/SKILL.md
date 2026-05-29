---
name: Resource Management
description: This skill should be used when the user asks about "Effect resources", "acquireRelease", "Scope", "finalizers", "resource cleanup", "Effect.addFinalizer", "Effect.ensuring", "scoped effects", "resource lifecycle", "bracket pattern", "safe resource handling", "database connections", "file handles", or needs to understand how Effect guarantees resource cleanup.
version: 1.0.0
---

# Resource Management in Effect

## Overview

Effect provides structured resource management that **guarantees cleanup** even when errors occur or the effect is interrupted. This is essential for:

- Database connections
- File handles
- Network sockets
- Locks and semaphores
- Any resource requiring cleanup

## Core Concept: Scope

A `Scope` is a context that tracks resources and ensures their cleanup:

```typescript
Effect<A, E, R | Scope>
//              ^^^^^ Indicates resource needs cleanup
```

## Basic Resource Acquisition

### Effect.acquireRelease

The fundamental pattern for safe resource management:

```typescript
import { Effect } from "effect"

const managedFile = Effect.acquireRelease(
  Effect.sync(() => fs.openSync("file.txt", "r")),
  (fd) => Effect.sync(() => fs.closeSync(fd))
)
```

### Using the Resource

```typescript
const program = Effect.gen(function* () {
  const fd = yield* managedFile
  const content = yield* Effect.sync(() => fs.readFileSync(fd, "utf-8"))
  return content
})

// Run with automatic scope management
const result = yield* Effect.scoped(program)
```

## Effect.scoped

Converts a scoped effect into a regular effect by managing the scope:

```typescript
const runnable = Effect.scoped(program)
```

The scope closes when the scoped block completes, triggering all finalizers.

## acquireUseRelease Pattern

For simpler cases, combine acquire/use/release in one call:

```typescript
const readFile = (path: string) =>
  Effect.acquireUseRelease(
    Effect.sync(() => fs.openSync(path, "r")),
    (fd) => Effect.sync(() => fs.readFileSync(fd, "utf-8")),
    (fd) => Effect.sync(() => fs.closeSync(fd))
  )
```

## Finalizers

### Effect.addFinalizer

Add cleanup logic to the current scope:

```typescript
const program = Effect.gen(function* () {
  yield* Effect.addFinalizer(() =>
    Effect.log("Cleanup running!")
  )

  // ... do work ...

  return result
})
```

### Effect.ensuring

Run cleanup after effect completes (success or failure):

```typescript
const withCleanup = someEffect.pipe(
  Effect.ensuring(
    Effect.log("Always runs after effect")
  )
)
```

### Effect.onExit

Run different cleanup based on exit status:

```typescript
const withExitHandler = someEffect.pipe(
  Effect.onExit((exit) =>
    Exit.isSuccess(exit)
      ? Effect.log("Succeeded!")
      : Effect.log("Failed or interrupted")
  )
)
```

## Multiple Resources

### Sequential Acquisition

```typescript
const program = Effect.gen(function* () {
  const db = yield* acquireDbConnection
  const cache = yield* acquireRedisConnection
})

const result = yield* Effect.scoped(program)
```

### Parallel Acquisition

```typescript
const program = Effect.gen(function* () {
  const [db, cache] = yield* Effect.all([
    acquireDbConnection,
    acquireRedisConnection
  ])
})
```

## Resource Patterns

### Database Connection Pool

```typescript
const DbPool = Effect.acquireRelease(
  Effect.promise(() => createPool({
    host: "localhost",
    database: "mydb",
    max: 10
  })),
  (pool) => Effect.promise(() => pool.end())
)

const query = (sql: string) =>
  Effect.gen(function* () {
    const pool = yield* DbPool
    return yield* Effect.tryPromise(() => pool.query(sql))
  })
```

### File Handle

```typescript
const withFile = <A>(
  path: string,
  use: (handle: FileHandle) => Effect.Effect<A>
) =>
  Effect.acquireUseRelease(
    Effect.promise(() => fs.promises.open(path)),
    use,
    (handle) => Effect.promise(() => handle.close())
  )
```

### Lock/Mutex

```typescript
const withLock = <A>(
  lock: Lock,
  effect: Effect.Effect<A>
) =>
  Effect.acquireUseRelease(
    lock.acquire,
    () => effect,
    () => lock.release
  )
```

## Layered Resources

Use `Layer.scoped` for service-level resources:

```typescript
const DatabaseLive = Layer.scoped(
  Database,
  Effect.gen(function* () {
    const pool = yield* Effect.acquireRelease(
      createPool(),
      (pool) => Effect.promise(() => pool.end())
    )

    return {
      query: (sql) => Effect.tryPromise(() => pool.query(sql))
    }
  })
)
```

## Error Handling in Cleanup

Finalizers should not fail, but if they do:

```typescript
const safeRelease = (resource: Resource) =>
  Effect.sync(() => resource.close()).pipe(
    Effect.catchAll((error) =>
      Effect.logError("Cleanup failed", error)
    )
  )

const managed = Effect.acquireRelease(
  acquire,
  safeRelease
)
```

## Interruption Safety

Resources are cleaned up even on interruption:

```typescript
const program = Effect.gen(function* () {
  const resource = yield* acquireResource

  yield* Effect.sleep("1 hour")
})

const result = yield* program.pipe(
  Effect.scoped,
  Effect.timeout("1 second")
)
```

## Best Practices

1. **Use acquireRelease for paired operations** - Guarantees cleanup
2. **Keep finalizers simple and infallible** - Log errors instead of throwing
3. **Use Effect.scoped at appropriate boundaries** - Not too wide, not too narrow
4. **Clean up in reverse acquisition order** - Effect handles this automatically
5. **Use Layer.scoped for service-level resources** - Lifecycle tied to layer

## Additional Resources

For comprehensive resource management documentation, consult `${CLAUDE_PLUGIN_ROOT}/references/llms-full.txt`.

Search for these sections:
- "Introduction" (Resource Management) for core concepts
- "Scope" for detailed scope mechanics
- "Managing Layers" for Layer.scoped patterns
