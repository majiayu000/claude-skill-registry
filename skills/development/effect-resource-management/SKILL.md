---
name: effect-resource-management
description: Use when Effect resource management patterns including Scope, addFinalizer, scoped effects, and automatic cleanup. Use for managing resources in Effect applications.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
---

# Effect Resource Management

Master automatic resource management in Effect using Scopes and finalizers.
This skill covers resource acquisition, cleanup, scoped effects, and patterns
for building leak-free Effect applications.

## Scope Fundamentals

A Scope represents the lifetime of resources. When a scope closes, all
registered finalizers execute automatically.

### Basic Scope Usage

```typescript
import { Effect, Scope } from "effect"

const program = Effect.scoped(
  Effect.gen(function* () {
    // Resources acquired here are tied to this scope
    const resource = yield* acquireResource()

    // Use resource
    const result = yield* useResource(resource)

    return result
    // Scope closes here, resources cleaned up automatically
  })
)
```

### Adding Finalizers

```typescript
import { Effect } from "effect"

const acquireFile = (path: string) =>
  Effect.gen(function* () {
    // Acquire resource
    const file = yield* Effect.sync(() => openFile(path))

    // Register cleanup
    yield* Effect.addFinalizer(() =>
      Effect.sync(() => {
        console.log(`Closing file: ${path}`)
        file.close()
      })
    )

    return file
  })

// Usage
const program = Effect.scoped(
  Effect.gen(function* () {
    const file = yield* acquireFile("data.txt")
    const content = yield* readFile(file)
    return content
    // File automatically closed on scope exit
  })
)
```

## Finalizer Behavior

### Execution Order

Finalizers execute in reverse order of registration (LIFO):

```typescript
import { Effect } from "effect"

const program = Effect.scoped(
  Effect.gen(function* () {
    yield* Effect.addFinalizer(() =>
      Effect.log("Finalizer 1")
    )

    yield* Effect.addFinalizer(() =>
      Effect.log("Finalizer 2")
    )

    yield* Effect.addFinalizer(() =>
      Effect.log("Finalizer 3")
    )

    return "done"
  })
)
// Output:
// Finalizer 3
// Finalizer 2
// Finalizer 1
```

### Exit Information

Finalizers receive exit information:

```typescript
import { Effect, Exit } from "effect"

const acquireWithContext = Effect.gen(function* () {
  yield* Effect.addFinalizer((exit) =>
    Effect.sync(() => {
      if (Exit.isSuccess(exit)) {
        console.log("Scope exited successfully:", exit.value)
      } else if (Exit.isFailure(exit)) {
        console.log("Scope failed:", exit.cause)
      } else {
        console.log("Scope interrupted")
      }
    })
  )

  // Acquire resource
  const resource = yield* Effect.sync(() => createResource())
  return resource
})
```

## Resource Patterns

### Database Connection

```typescript
import { Effect } from "effect"

interface DbConnection {
  query: <T>(sql: string) => Promise<T>
  close: () => Promise<void>
}

const acquireConnection = (config: DbConfig) =>
  Effect.gen(function* () {
    // Acquire connection
    const conn = yield* Effect.tryPromise({
      try: () => createConnection(config),
      catch: (error) => ({
        _tag: "ConnectionError",
        message: String(error)
      })
    })

    // Register cleanup
    yield* Effect.addFinalizer(() =>
      Effect.tryPromise({
        try: () => conn.close(),
        catch: (error) => ({
          _tag: "CloseError",
          message: String(error)
        })
      }).pipe(
        Effect.catchAll((error) =>
          Effect.log(`Failed to close connection: ${error.message}`)
        )
      )
    )

    return conn
  })

// Usage
const queryDatabase = Effect.scoped(
  Effect.gen(function* () {
    const conn = yield* acquireConnection(dbConfig)
    const users = yield* Effect.tryPromise(() =>
      conn.query<User[]>("SELECT * FROM users")
    )
    return users
    // Connection automatically closed
  })
)
```

### File Operations

```typescript
import { Effect } from "effect"
import * as fs from "fs/promises"

const withFile = <A, E, R>(
  path: string,
  use: (handle: fs.FileHandle) => Effect.Effect<A, E, R>
) =>
  Effect.scoped(
    Effect.gen(function* () {
      // Acquire file handle
      const handle = yield* Effect.tryPromise({
        try: () => fs.open(path, "r"),
        catch: (error) => ({
          _tag: "FileError",
          message: String(error)
        })
      })

      // Register cleanup
      yield* Effect.addFinalizer(() =>
        Effect.tryPromise(() => handle.close()).pipe(
          Effect.catchAll(() => Effect.void)
        )
      )

      // Use file
      return yield* use(handle)
    })
  )

// Usage
const readFileContent = withFile("data.txt", (handle) =>
  Effect.tryPromise(() => handle.readFile({ encoding: "utf8" }))
)
```

### Network Resources

```typescript
import { Effect } from "effect"

interface WebSocket {
  send: (data: string) => void
  close: () => void
  onMessage: (handler: (data: string) => void) => void
}

const acquireWebSocket = (url: string) =>
  Effect.gen(function* () {
    const ws = yield* Effect.async<WebSocket, never>((resume) => {
      const socket = new WebSocket(url)

      socket.onopen = () => {
        resume(Effect.succeed(socket))
      }

      socket.onerror = () => {
        resume(Effect.fail({ _tag: "ConnectionError" }))
      }
    })

    yield* Effect.addFinalizer(() =>
      Effect.sync(() => {
        console.log("Closing WebSocket")
        ws.close()
      })
    )

    return ws
  })
```

## Scoped Effects

### Effect.acquireRelease

Simplified resource acquisition:

```typescript
import { Effect } from "effect"

const resource = Effect.acquireRelease(
  // Acquire
  Effect.sync(() => {
    console.log("Acquiring resource")
    return createResource()
  }),
  // Release
  (resource) =>
    Effect.sync(() => {
      console.log("Releasing resource")
      resource.cleanup()
    })
)

// Usage
const program = Effect.scoped(
  Effect.gen(function* () {
    const r = yield* resource
    return yield* useResource(r)
  })
)
```

### Effect.acquireUseRelease

One-shot resource usage:

```typescript
import { Effect } from "effect"

const readConfig = Effect.acquireUseRelease(
  // Acquire
  Effect.tryPromise(() => fs.open("config.json", "r")),

  // Use
  (handle) =>
    Effect.tryPromise(() =>
      handle.readFile({ encoding: "utf8" })
    ).pipe(
      Effect.map((content) => JSON.parse(content))
    ),

  // Release
  (handle) =>
    Effect.tryPromise(() => handle.close()).pipe(
      Effect.orDie
    )
)
```

## Nested Scopes

### Scope Nesting

Scopes can be nested for hierarchical cleanup:

```typescript
import { Effect } from "effect"

const program = Effect.scoped(
  Effect.gen(function* () {
    const db = yield* acquireConnection()

    yield* Effect.scoped(
      Effect.gen(function* () {
        const transaction = yield* beginTransaction(db)
        yield* updateUsers(transaction)
        yield* commitTransaction(transaction)
        // Transaction scope ends, resources cleaned up
      })
    )

    // DB connection still alive
    yield* runQuery(db)
    // DB scope ends, connection closed
  })
)
```

### Parallel Scopes

```typescript
import { Effect } from "effect"

const parallelResources = Effect.gen(function* () {
  const results = yield* Effect.all([
    Effect.scoped(
      Effect.gen(function* () {
        const conn1 = yield* acquireConnection(db1Config)
        return yield* queryDb(conn1)
      })
    ),
    Effect.scoped(
      Effect.gen(function* () {
        const conn2 = yield* acquireConnection(db2Config)
        return yield* queryDb(conn2)
      })
    )
  ])

  return results
  // Both connections closed automatically
})
```

## Advanced Patterns

### Resource Pool

```typescript
import { Effect, Queue, Ref } from "effect"

interface Pool<R> {
  acquire: Effect.Effect<R, never, Scope.Scope>
  release: (resource: R) => Effect.Effect<void, never, never>
}

const createPool = <R, E>(
  create: Effect.Effect<R, E, never>,
  destroy: (resource: R) => Effect.Effect<void, never, never>,
  size: number
): Effect.Effect<Pool<R>, E, Scope.Scope> =>
  Effect.gen(function* () {
    const available = yield* Queue.bounded<R>(size)
    const counter = yield* Ref.make(0)

    // Initialize pool
    yield* Effect.forEach(
      Array.from({ length: size }),
      () =>
        Effect.gen(function* () {
          const resource = yield* create
          yield* Queue.offer(available, resource)
        }),
      { concurrency: "unbounded" }
    )

    // Register pool cleanup
    yield* Effect.addFinalizer(() =>
      Effect.gen(function* () {
        const resources = yield* Queue.takeAll(available)
        yield* Effect.forEach(
          resources,
          (r) => destroy(r),
          { concurrency: "unbounded" }
        )
      })
    )

    return {
      acquire: Effect.gen(function* () {
        const resource = yield* Queue.take(available)
        yield* Effect.addFinalizer(() => Queue.offer(available, resource))
        return resource
      }),
      release: (resource) => Queue.offer(available, resource)
    }
  })
```

### Cached Resource

```typescript
import { Effect, Ref } from "effect"

const cached = <A, E, R>(
  acquire: Effect.Effect<A, E, R>
): Effect.Effect<Effect.Effect<A, E, never>, never, Scope.Scope | R> =>
  Effect.gen(function* () {
    const ref = yield* Ref.make<Option<A>>(Option.none())

    yield* Effect.addFinalizer(() =>
      ref.set(Option.none())
    )

    return ref.get.pipe(
      Effect.flatMap((option) =>
        Option.match(option, {
          onNone: () =>
            acquire.pipe(
              Effect.tap((value) => ref.set(Option.some(value)))
            ),
          onSome: (value) => Effect.succeed(value)
        })
      )
    )
  })
```

## Best Practices

1. **Always Use Scoped**: Acquire resources within Effect.scoped.

2. **Register Finalizers Immediately**: Add finalizers right after acquisition.

3. **Handle Cleanup Errors**: Catch and log errors in finalizers.

4. **Reverse Order**: Rely on LIFO finalizer execution for dependencies.

5. **Use acquireRelease**: Prefer acquireRelease for simple acquire/release
   patterns.

6. **Test Cleanup**: Verify finalizers execute correctly.

7. **Avoid Manual Cleanup**: Don't manually clean up scoped resources.

8. **Nest Appropriately**: Use nested scopes for hierarchical resources.

9. **Pool Expensive Resources**: Use resource pools for expensive acquisitions.

10. **Document Scope Requirements**: Make it clear which effects need scopes.

## Common Pitfalls

1. **Missing Scoped**: Acquiring resources without Effect.scoped.

2. **Not Adding Finalizers**: Forgetting to register cleanup.

3. **Finalizer Errors**: Throwing errors in finalizers without handling.

4. **Wrong Scope Nesting**: Closing scopes in wrong order.

5. **Resource Leaks**: Not cleaning up on all exit paths.

6. **Duplicate Cleanup**: Cleaning up resources multiple times.

7. **Blocking Finalizers**: Using long-running operations in finalizers.

8. **Ignoring Exit Info**: Not using exit information appropriately.

9. **Scope Scope Confusion**: Confusing when scopes close.

10. **Missing Error Handling**: Not handling errors during acquisition.

## When to Use This Skill

Use effect-resource-management when you need to:

- Manage database connections
- Handle file operations safely
- Work with network resources
- Implement connection pools
- Build transaction systems
- Ensure cleanup on all exit paths
- Manage WebSocket connections
- Handle distributed locks
- Implement caching with cleanup
- Build leak-free applications

## Resources

### Official Documentation

- [Resource Management](https://effect.website/docs/resource-management/)
- [Scope](https://effect.website/docs/resource-management/scope)
- [Adding Finalizers](https://effect.website/docs/resource-management/adding-finalizers)
- [acquireRelease](https://effect.website/docs/resource-management/acquire-release)

### Related Skills

- effect-core-patterns - Basic Effect operations
- effect-concurrency - Managing fiber lifecycles
- effect-dependency-injection - Layer cleanup with scoped
