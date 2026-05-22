---
name: effect-scope-resource
description: Instructions on how to properly utilize Effect scopes for resource management, lifecycle concerns, etc.
model_invoked: true
triggers:
  - "scope"
  - "constrain"
  - "resource"
  - "resource management"
  - "management"
  - "cleanup"
---


# Effect Scope & Resources

## Triggers
- `[EFFECT:SCOPE:ACQUIRE]` - Acquiring managed resources
- `[EFFECT:SCOPE:RELEASE]` - Cleanup, finalizers, ensuring

---

## Core Principle

> **"If you open files and never close them, you are summoning demons of leaks."**

Resources must be acquired and released in a structured way. Effect's `Scope` ensures cleanup happens even on errors or interruption.

---

## [EFFECT:SCOPE:ACQUIRE] — Resource Acquisition

### Effect.acquireRelease — The Fundamental Pattern

```typescript
import { Effect, Scope } from "effect"

const managedConnection = Effect.acquireRelease(
  // Acquire
  Effect.sync(() => {
    console.log("Opening connection...")
    return createConnection()
  }),
  // Release (always runs)
  (connection) => Effect.sync(() => {
    console.log("Closing connection...")
    connection.close()
  })
)
```

### Using Scoped Resources

```typescript
const program = Effect.scoped(
  Effect.gen(function* () {
    const conn = yield* managedConnection
    const result = yield* conn.query("SELECT * FROM users")
    return result
    // Connection automatically closed when scope exits
  })
)
```

### Multiple Resources

```typescript
const program = Effect.scoped(
  Effect.gen(function* () {
    const db = yield* managedDatabase
    const cache = yield* managedCache
    const queue = yield* managedQueue

    // Use all three resources
    yield* doWork(db, cache, queue)

    // All three released in reverse order when scope exits
  })
)
```

### Pattern: File Handling

```typescript
const managedFile = (path: string) =>
  Effect.acquireRelease(
    Effect.sync(() => fs.openSync(path, "r")),
    (fd) => Effect.sync(() => fs.closeSync(fd))
  )

const readFile = (path: string) =>
  Effect.scoped(
    Effect.gen(function* () {
      const fd = yield* managedFile(path)
      return yield* Effect.sync(() => fs.readFileSync(fd, "utf-8"))
    })
  )
```

### Pattern: Connection Pool

```typescript
const managedPool = Effect.acquireRelease(
  Effect.sync(() => createPool({ max: 10 })),
  (pool) => Effect.promise(() => pool.end())
)

const withPool = <A, E>(
  use: (pool: Pool) => Effect.Effect<A, E>
): Effect.Effect<A, E> =>
  Effect.scoped(
    Effect.gen(function* () {
      const pool = yield* managedPool
      return yield* use(pool)
    })
  )
```

---

## [EFFECT:SCOPE:RELEASE] — Cleanup & Finalizers

### Scope.addFinalizer — Add Cleanup Actions

```typescript
const program = Effect.gen(function* () {
  const scope = yield* Effect.scope

  // Add finalizer to current scope
  yield* Scope.addFinalizer(scope,
    Effect.sync(() => console.log("Cleanup 1"))
  )

  yield* Scope.addFinalizer(scope,
    Effect.sync(() => console.log("Cleanup 2"))
  )

  yield* doWork()
  // Finalizers run in reverse order: "Cleanup 2", then "Cleanup 1"
})
```

### Effect.addFinalizer — Simpler API

```typescript
const program = Effect.gen(function* () {
  yield* Effect.addFinalizer(() =>
    Effect.sync(() => console.log("Cleaning up..."))
  )

  yield* doWork()
})

// Must run in scoped context
Effect.scoped(program)
```

### Effect.ensuring — Always Run

```typescript
const withCleanup = task.pipe(
  Effect.ensuring(
    Effect.sync(() => console.log("Always runs, success or failure"))
  )
)
```

### Effect.onExit — Conditional Cleanup

```typescript
const withConditionalCleanup = task.pipe(
  Effect.onExit((exit) =>
    Exit.isSuccess(exit)
      ? Effect.log("Success cleanup")
      : Effect.log("Failure cleanup")
  )
)
```

### Effect.onError — Only on Error

```typescript
const withErrorCleanup = task.pipe(
  Effect.onError((cause) =>
    Effect.log(`Failed with: ${Cause.pretty(cause)}`)
  )
)
```

### Effect.onInterrupt — Only on Interruption

```typescript
const withInterruptHandler = task.pipe(
  Effect.onInterrupt((interruptors) =>
    Effect.log("Was interrupted!")
  )
)
```

---

## Advanced Patterns

### Acquire-Use-Release with acquireUseRelease

```typescript
const result = yield* Effect.acquireUseRelease(
  // Acquire
  Effect.sync(() => openResource()),
  // Use
  (resource) => doWork(resource),
  // Release
  (resource) => Effect.sync(() => resource.close())
)
```

### Layered Resource Management

```typescript
const DatabaseLayer = Layer.scoped(
  Database,
  Effect.gen(function* () {
    const pool = yield* Effect.acquireRelease(
      createPool(),
      (pool) => Effect.promise(() => pool.end())
    )
    return { query: (sql: string) => pool.query(sql) }
  })
)
```

### Pattern: Transaction with Rollback

```typescript
const transaction = <A, E>(
  operation: (tx: Transaction) => Effect.Effect<A, E>
): Effect.Effect<A, E | TransactionError> =>
  Effect.acquireUseRelease(
    beginTransaction(),
    (tx) => operation(tx),
    (tx, exit) =>
      Exit.isSuccess(exit)
        ? tx.commit()
        : tx.rollback()
  )
```

### Pattern: Lock Acquisition

```typescript
const withLock = <A, E>(
  lock: Lock,
  operation: Effect.Effect<A, E>
): Effect.Effect<A, E> =>
  Effect.acquireUseRelease(
    lock.acquire(),
    () => operation,
    () => lock.release()
  )
```

---

## Scope Hierarchy

```
Global Scope
└── Layer Scope (services)
    └── Effect.scoped
        └── Effect.fork (fiber scope)
            └── Effect.forkScoped
```

- Resources in child scopes are released before parent scope closes
- `Effect.forkScoped` ties fiber lifetime to current scope
- Layer resources live for the lifetime of the layer

---

## Anti-Patterns

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Manual try/finally | Misses interruption | `Effect.acquireRelease` |
| Forgetting to close | Resource leaks | `Effect.scoped` wrapper |
| Cleanup in wrong order | Dependency issues | Reverse-order finalizers |
| Async cleanup without Effect | Untracked | `Effect.promise` in release |
| Nested scopes without reason | Complexity | Single `scoped` when possible |

---

## Quick Reference

```typescript
// Managed resource
const managed = Effect.acquireRelease(
  acquire,
  (resource) => release(resource)
)

// Use in scope
Effect.scoped(
  Effect.gen(function* () {
    const resource = yield* managed
    return yield* use(resource)
  })
)

// Add finalizer
yield* Effect.addFinalizer(() => cleanup)

// Always run
task.pipe(Effect.ensuring(cleanup))

// On error only
task.pipe(Effect.onError((cause) => logError(cause)))

// One-shot acquire-use-release
yield* Effect.acquireUseRelease(acquire, use, release)
```
