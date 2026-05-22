---
name: effect-core-patterns
description: Use when Effect core patterns including Effect<A, E, R> type, succeed, fail, sync, promise, and Effect.gen for composing effects. Use for basic Effect operations.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
---

# Effect Core Patterns

Master the core Effect patterns for building type-safe, composable applications
with Effect. This skill covers the Effect type, constructors, and composition
patterns using Effect.gen.

## The Effect Type

The Effect type has three type parameters:

```typescript
Effect<Success, Error, Requirements>
```

- **Success (A)**: The type of value that an effect can succeed with
- **Error (E)**: The expected errors that can occur (use `never` for no errors)
- **Requirements (R)**: The contextual dependencies required (use `never` for no dependencies)

```typescript
import { Effect } from "effect"

// Effect that succeeds with number, never fails, no requirements
const simpleEffect: Effect.Effect<number, never, never> = Effect.succeed(42)

// Effect that can fail with string error
const failableEffect: Effect.Effect<number, string, never> =
  Effect.fail("Something went wrong")

// Effect that requires a UserService
interface UserService {
  getUser: (id: string) => Effect.Effect<User, DbError, never>
}

const effectWithDeps: Effect.Effect<User, DbError, UserService> =
  Effect.gen(function* () {
    const userService = yield* Effect.service(UserService)
    const user = yield* userService.getUser("123")
    return user
  })
```

## Creating Effects

### Effect.succeed - Always Succeeds

Use when you have a pure value and need an Effect:

```typescript
import { Effect } from "effect"

const result = Effect.succeed(42)
// Effect<number, never, never>

const user = Effect.succeed({ id: "1", name: "Alice" })
// Effect<User, never, never>

// Void effect (produces no useful value)
const voidEffect = Effect.succeed(undefined)
// Effect<void, never, never>
```

### Effect.fail - Expected Failure

Use for recoverable, expected errors:

```typescript
import { Effect } from "effect"

interface ValidationError {
  _tag: "ValidationError"
  message: string
}

const validateAge = (age: number): Effect.Effect<number, ValidationError, never> => {
  if (age < 0) {
    return Effect.fail({
      _tag: "ValidationError",
      message: "Age must be positive"
    })
  }
  return Effect.succeed(age)
}

// Usage with Effect.gen
const program = Effect.gen(function* () {
  const age = yield* validateAge(-5) // This will fail
  return age
})
```

### Effect.sync - Synchronous Side Effects

Use for synchronous operations with side effects:

```typescript
import { Effect } from "effect"

// Reading from a mutable variable
let counter = 0

const incrementCounter = Effect.sync(() => {
  counter++
  return counter
})

// Logging
const log = (message: string) =>
  Effect.sync(() => {
    console.log(message)
  })

// Current timestamp
const now = Effect.sync(() => Date.now())

// IMPORTANT: The function should not throw
// Thrown errors become "defects" (unexpected failures)
```

### Effect.try - Synchronous Operations That May Fail

Use for sync operations that might throw:

```typescript
import { Effect } from "effect"

// Parse JSON safely
const parseJSON = (text: string): Effect.Effect<unknown, Error, never> =>
  Effect.try(() => JSON.parse(text))

// With custom error mapping
interface ParseError {
  _tag: "ParseError"
  message: string
}

const parseJSONCustom = (text: string): Effect.Effect<unknown, ParseError, never> =>
  Effect.try({
    try: () => JSON.parse(text),
    catch: (error) => ({
      _tag: "ParseError",
      message: error instanceof Error ? error.message : String(error)
    })
  })

// Usage
const program = Effect.gen(function* () {
  const data = yield* parseJSON('{"name": "Alice"}')
  return data
})
```

### Effect.promise - Async Operations (No Errors)

Use for promises that should never reject:

```typescript
import { Effect } from "effect"

// Delayed execution
const delay = (ms: number): Effect.Effect<void, never, never> =>
  Effect.promise(() =>
    new Promise<void>((resolve) => setTimeout(resolve, ms))
  )

// Fetch with assumption it won't fail
const fetchData = (url: string): Effect.Effect<Response, never, never> =>
  Effect.promise(() => fetch(url))

// IMPORTANT: If promise rejects, it becomes a "defect"
// Use Effect.tryPromise for operations that can fail
```

### Effect.tryPromise - Async Operations That May Fail

Use for promises that might reject:

```typescript
import { Effect } from "effect"

interface NetworkError {
  _tag: "NetworkError"
  message: string
  statusCode?: number
}

const fetchUser = (id: string): Effect.Effect<User, NetworkError, never> =>
  Effect.tryPromise({
    try: async () => {
      const response = await fetch(`/api/users/${id}`)
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`)
      }
      return response.json()
    },
    catch: (error) => ({
      _tag: "NetworkError",
      message: error instanceof Error ? error.message : String(error),
      statusCode: error instanceof Error && 'status' in error
        ? (error as any).status
        : undefined
    })
  })

// Simplified version (errors become UnknownException)
const fetchUserSimple = (id: string): Effect.Effect<User, UnknownException, never> =>
  Effect.tryPromise(() => fetch(`/api/users/${id}`).then(r => r.json()))
```

### Effect.async - Callback-Based APIs

Use for wrapping callback-style APIs:

```typescript
import { Effect } from "effect"

// Wrap setTimeout
const sleep = (ms: number): Effect.Effect<void, never, never> =>
  Effect.async<void>((resume) => {
    const timeoutId = setTimeout(() => {
      resume(Effect.succeed(undefined))
    }, ms)

    // Optional cleanup on interruption
    return Effect.sync(() => {
      clearTimeout(timeoutId)
    })
  })

// Wrap Node.js callback API
interface FileError {
  _tag: "FileError"
  message: string
}

const readFile = (path: string): Effect.Effect<string, FileError, never> =>
  Effect.async<string, FileError>((resume) => {
    fs.readFile(path, 'utf8', (error, data) => {
      if (error) {
        resume(Effect.fail({
          _tag: "FileError",
          message: error.message
        }))
      } else {
        resume(Effect.succeed(data))
      }
    })
  })
```

## Composing Effects with Effect.gen

Effect.gen allows you to write effect code using generator syntax:

```typescript
import { Effect } from "effect"

// Basic composition
const program = Effect.gen(function* () {
  const a = yield* Effect.succeed(10)
  const b = yield* Effect.succeed(20)
  return a + b
})

// With error handling
const programWithErrors = Effect.gen(function* () {
  const age = yield* validateAge(25)
  const user = yield* createUser({ age })
  return user
})

// Sequential operations
const fetchUserProfile = (userId: string) =>
  Effect.gen(function* () {
    const user = yield* fetchUser(userId)
    const posts = yield* fetchPosts(user.id)
    const comments = yield* fetchComments(user.id)
    return { user, posts, comments }
  })

// Using control flow
const processData = (data: unknown) =>
  Effect.gen(function* () {
    const validated = yield* validateData(data)

    if (validated.type === "user") {
      const user = yield* createUser(validated)
      return { type: "user", user }
    } else {
      const post = yield* createPost(validated)
      return { type: "post", post }
    }
  })

// Error handling with short-circuiting
const safeDivide = (a: number, b: number) =>
  Effect.gen(function* () {
    if (b === 0) {
      yield* Effect.fail({ _tag: "DivideByZero" })
      return // Explicit return for type narrowing
    }
    return a / b
  })
```

## Running Effects

### Effect.runSync - Synchronous Execution

Use for effects with no async operations or requirements:

```typescript
import { Effect } from "effect"

const result = Effect.runSync(Effect.succeed(42))
// 42

// Throws if effect can fail
try {
  Effect.runSync(Effect.fail("error"))
} catch (error) {
  // Caught
}

// CANNOT use with async effects or requirements
// Effect.runSync(Effect.promise(() => fetch("..."))) // Runtime error!
```

### Effect.runPromise - Async Execution

Use for async effects without requirements:

```typescript
import { Effect } from "effect"

const program = Effect.gen(function* () {
  yield* delay(1000)
  return "Done"
})

const result = await Effect.runPromise(program)
// "Done" after 1 second

// Rejects on failure
try {
  await Effect.runPromise(Effect.fail("error"))
} catch (error) {
  // error === "error"
}
```

### Effect.runPromiseExit - Get Full Exit Information

Use when you need detailed success/failure information:

```typescript
import { Effect, Exit } from "effect"

const program = Effect.succeed(42)

const exit = await Effect.runPromiseExit(program)

if (Exit.isSuccess(exit)) {
  console.log("Success:", exit.value)
} else if (Exit.isFailure(exit)) {
  console.log("Failure:", exit.cause)
}
```

## Building Pipelines

### Effect.map - Transform Success Values

```typescript
import { Effect, pipe } from "effect"

const double = (n: number) => n * 2

// Using pipe
const result = pipe(
  Effect.succeed(21),
  Effect.map(double)
)
// Effect<42, never, never>

// Using method
const result2 = Effect.succeed(21).pipe(
  Effect.map(double)
)

// Chaining transformations
const program = pipe(
  Effect.succeed("hello"),
  Effect.map(s => s.toUpperCase()),
  Effect.map(s => s.length)
)
// Effect<5, never, never>
```

### Effect.flatMap - Chain Dependent Effects

```typescript
import { Effect, pipe } from "effect"

const getUser = (id: string): Effect.Effect<User, DbError, never> => {
  // ...
}

const getUserPosts = (userId: string): Effect.Effect<Post[], DbError, never> => {
  // ...
}

// Using pipe
const program = pipe(
  getUser("123"),
  Effect.flatMap(user => getUserPosts(user.id))
)

// Using Effect.gen (more readable)
const program2 = Effect.gen(function* () {
  const user = yield* getUser("123")
  const posts = yield* getUserPosts(user.id)
  return posts
})
```

### Effect.andThen - Sequential Composition

```typescript
import { Effect, pipe } from "effect"

// Chain effects, ignoring previous result
const program = pipe(
  log("Starting..."),
  Effect.andThen(processData()),
  Effect.andThen(log("Done!"))
)

// Provide value to next effect
const program2 = pipe(
  Effect.succeed(5),
  Effect.andThen(n => Effect.succeed(n * 2))
)
```

### Effect.tap - Side Effects Without Changing Value

```typescript
import { Effect, pipe } from "effect"

const program = pipe(
  fetchUser("123"),
  Effect.tap(user => log(`Fetched user: ${user.name}`)),
  Effect.tap(user => saveToCache(user)),
  Effect.map(user => user.email)
)

// The taps run but don't change the flowing value
```

## Effect Transformations

### Effect.mapError - Transform Errors

```typescript
import { Effect, pipe } from "effect"

interface DbError {
  _tag: "DbError"
  message: string
}

interface AppError {
  _tag: "AppError"
  message: string
  context: string
}

const program = pipe(
  queryDatabase(),
  Effect.mapError((dbError: DbError): AppError => ({
    _tag: "AppError",
    message: dbError.message,
    context: "user-service"
  }))
)
```

### Effect.mapBoth - Transform Success and Error

```typescript
import { Effect, pipe } from "effect"

const program = pipe(
  Effect.succeed(10),
  Effect.mapBoth({
    onSuccess: (n) => n * 2,
    onFailure: (e) => ({ _tag: "MappedError", original: e })
  })
)
```

### Effect.orElse - Fallback on Failure

```typescript
import { Effect, pipe } from "effect"

const program = pipe(
  fetchFromPrimaryDb(),
  Effect.orElse(() => fetchFromSecondaryDb())
)

// Fallback to different effect based on error
const programWithCheck = pipe(
  riskyOperation(),
  Effect.orElse((error) =>
    error._tag === "Timeout"
      ? retryOperation()
      : Effect.fail(error)
  )
)
```

## Best Practices

1. **Use Effect.gen for Readability**: Prefer Effect.gen over pipe for complex
   compositions with multiple steps.

2. **Type Your Errors**: Always use tagged unions for error types to enable
   catchTag and better error handling.

3. **Distinguish Errors from Defects**: Use Effect.try/tryPromise for operations
   that can fail. Let unexpected errors become defects.

4. **Keep Effects Pure**: Don't perform side effects outside of Effect
   constructors. Use Effect.sync for side effects.

5. **Use Descriptive Names**: Name effects based on what they do, not how they
   do it (e.g., `fetchUser` not `makeHttpRequest`).

6. **Compose Small Effects**: Build complex operations from small, focused
   effects that do one thing well.

7. **Handle Requirements Explicitly**: Use Effect.service and layers to manage
   dependencies rather than importing directly.

8. **Document Effect Types**: Explicitly type effects to make requirements,
   errors, and success types clear.

9. **Use pipe for Transformations**: For simple transformations, pipe is more
   concise than Effect.gen.

10. **Test Effects Independently**: Design effects to be testable by injecting
    dependencies via requirements.

## Common Pitfalls

1. **Using runSync on Async Effects**: runSync throws on async effects. Use
   runPromise instead.

2. **Not Handling Errors**: Forgetting that effects can fail. Always consider
   the error channel.

3. **Mixing Promises and Effects**: Converting between promises and effects
   incorrectly. Use Effect.promise/tryPromise.

4. **Ignoring Requirements**: Not providing required services causes runtime
   errors. Use layers properly.

5. **Throwing in Effect.sync**: Thrown errors become defects. Use Effect.try
   for operations that can throw.

6. **Not Using Effect.gen**: Complex pipe chains are hard to read. Use
   Effect.gen for better readability.

7. **Incorrect Error Types**: Using `unknown` or `Error` instead of specific
   tagged error types.

8. **Sequential When Parallel Is Better**: Using Effect.gen sequentially when
   operations could run in parallel with Effect.all.

9. **Over-Using map/flatMap**: Effect.gen is clearer for multi-step operations
   than nested maps.

10. **Not Leveraging Type Safety**: Not using TypeScript's type system to catch
    errors at compile time.

## When to Use This Skill

Use effect-core-patterns when you need to:

- Build type-safe applications with Effect
- Create and compose effectful operations
- Handle errors in a type-safe manner
- Work with async operations and promises
- Manage side effects explicitly
- Create pipelines of transformations
- Convert callback-based APIs to Effect
- Build maintainable, composable code
- Leverage functional programming patterns
- Ensure compile-time safety for effects

## Resources

### Official Documentation

- [Effect Website](https://effect.website/)
- [Getting Started](https://effect.website/docs/quickstart)
- [The Effect Type](https://effect.website/docs/getting-started/the-effect-type)
- [Creating Effects](https://effect.website/docs/getting-started/creating-effects)
- [Using Generators](https://effect.website/docs/getting-started/using-generators)
- [Running Effects](https://effect.website/docs/getting-started/running-effects)

### Guides

- [Effect GitHub](https://github.com/Effect-TS/effect)
- [Effect Discord](https://discord.gg/effect-ts)
- [Effect Examples](https://github.com/Effect-TS/examples)
