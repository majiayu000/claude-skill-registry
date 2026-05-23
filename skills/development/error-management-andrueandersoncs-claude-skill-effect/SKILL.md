---
name: Error Management
description: This skill should be used when the user asks about "Effect errors", "typed errors", "error handling", "Effect.catchAll", "Effect.catchTag", "Effect.mapError", "Effect.orElse", "error accumulation", "defects vs errors", "expected errors", "unexpected errors", "sandboxing", "retrying", "timeout", "Effect.cause", "TaggedError", "Schema.TaggedError", or needs to understand how Effect handles failures in the error channel.
version: 1.0.0
---

# Error Management in Effect

## Overview

Effect distinguishes between two types of failures:

1. **Expected Errors (Recoverable)** - Represented in the `Error` type parameter, tracked at compile time
2. **Defects (Unexpected/Unrecoverable)** - Runtime exceptions, bugs, not in type signature

```typescript
Effect<Success, Error, Requirements>
//              ^^^^^ Expected errors live here
```

## Creating Typed Errors

### Using Schema.TaggedError (Recommended)

```typescript
import { Schema, Effect } from "effect"

class UserNotFound extends Schema.TaggedError<UserNotFound>()(
  "UserNotFound",
  { userId: Schema.String }
) {}

// Note: Schema.Unknown is semantically correct here because `cause` captures
// arbitrary caught exceptions whose type is genuinely unknown at the domain level.
// This is NOT type weakening - JavaScript exceptions can be any value.
class NetworkError extends Schema.TaggedError<NetworkError>()(
  "NetworkError",
  { cause: Schema.Unknown }
) {}

const getUser = (id: string): Effect.Effect<User, UserNotFound | NetworkError> =>
  Effect.gen(function* () {
    // ...implementation
    return yield* Effect.fail(new UserNotFound({ userId: id }))
  })
```

### Using Effect.fail

```typescript
const divide = (a: number, b: number) =>
  b === 0
    ? Effect.fail(new DivisionByZero())
    : Effect.succeed(a / b)
```

## Catching and Recovering from Errors

### catchAll - Catch All Errors

```typescript
program.pipe(
  Effect.catchAll((error) =>
    Effect.succeed("fallback value")
  )
)
```

### catchTag - Catch Specific Error by Tag

```typescript
const program = getUser(id).pipe(
  Effect.catchTag("UserNotFound", (error) =>
    Effect.succeed(defaultUser)
  ),
  Effect.catchTag("NetworkError", (error) =>
    Effect.retry(Schedule.exponential("1 second"))
  )
)
```

### catchTags - Handle Multiple Error Types

```typescript
const program = getUser(id).pipe(
  Effect.catchTags({
    UserNotFound: (error) => Effect.succeed(defaultUser),
    NetworkError: (error) => Effect.fail(new ServiceUnavailable())
  })
)
```

### orElse - Provide Fallback Effect

```typescript
const primary = fetchFromPrimary()
const fallback = fetchFromBackup()

const resilient = primary.pipe(
  Effect.orElse(() => fallback)
)
```

### orElseSucceed - Provide Fallback Value

```typescript
const program = fetchConfig().pipe(
  Effect.orElseSucceed(() => defaultConfig)
)
```

## Transforming Errors

### mapError - Transform Error Type

```typescript
const program = rawApiCall().pipe(
  Effect.mapError((error) => new ApiError({ cause: error }))
)
```

### mapBoth - Transform Both Success and Error

```typescript
const program = effect.pipe(
  Effect.mapBoth({
    onError: (e) => new WrappedError({ cause: e }),
    onSuccess: (a) => a.toUpperCase()
  })
)
```

## Error Accumulation

When running multiple effects, collect all errors instead of failing fast:

### Using Effect.all with mode: "either"

```typescript
const results = yield* Effect.all(
  [effect1, effect2, effect3],
  { mode: "either" }
)
```

### Using Effect.partition

```typescript
const [failures, successes] = yield* Effect.partition(
  items,
  (item) => processItem(item)
)
```

### Using Effect.validate

```typescript
const result = yield* Effect.validate(
  [check1, check2, check3],
  { concurrency: "unbounded" }
)
```

## Defects (Unexpected Errors)

Defects are bugs/unexpected failures not tracked in types:

```typescript
const defect = Effect.die(new Error("Unexpected!"))

const program = effect.pipe(Effect.orDie)

const sandboxed = Effect.sandbox(program)
```

### Cause - Full Error Information

The `Cause` type contains complete failure information:

```typescript
import { Cause, Match } from "effect"

// In sandbox, you get full Cause - use Match for handling
const handled = Effect.sandbox(program).pipe(
  Effect.catchAll((cause) =>
    Match.value(cause).pipe(
      Match.when(Cause.isFailure, () => {
        // Expected error
        return Effect.succeed(fallback)
      }),
      Match.when(Cause.isDie, () => {
        // Defect - log and recover
        return Effect.succeed(fallback)
      }),
      Match.when(Cause.isInterrupt, () => {
        // Interruption
        return Effect.succeed(fallback)
      }),
      Match.orElse(() => Effect.succeed(fallback))
    )
  )
)
```

## Retrying

```typescript
import { Schedule } from "effect"

const resilient = effect.pipe(
  Effect.retry(
    Schedule.exponential("100 millis").pipe(
      Schedule.jittered,
      Schedule.compose(Schedule.recurs(5))
    )
  )
)

// Retry with condition - use Match.tag for error type checking
const conditional = effect.pipe(
  Effect.retry({
    schedule: Schedule.recurs(3),
    while: (error) =>
      Match.value(error).pipe(
        Match.tag("NetworkError", () => true),
        Match.orElse(() => false)
      )
  })
)
```

## Timeouts

```typescript
const withTimeout = effect.pipe(
  Effect.timeout("5 seconds")
)

const failOnTimeout = effect.pipe(
  Effect.timeoutFail({
    duration: "5 seconds",
    onTimeout: () => new TimeoutError()
  })
)
```

## Error Matching Patterns

### Using Effect.match

```typescript
const result = yield* effect.pipe(
  Effect.match({
    onFailure: (error) => `Failed: ${error.message}`,
    onSuccess: (value) => `Success: ${value}`
  })
)
```

### Using Effect.matchEffect

```typescript
const result = yield* effect.pipe(
  Effect.matchEffect({
    onFailure: (error) => logError(error).pipe(Effect.as("failed")),
    onSuccess: (value) => logSuccess(value).pipe(Effect.as("success"))
  })
)
```

## Best Practices

1. **Use TaggedError for all domain errors** - Enables `catchTag` pattern matching
2. **Keep error channel for recoverable errors** - Use defects for bugs
3. **Transform errors at boundaries** - Map low-level errors to domain errors
4. **Use typed errors generously** - The compiler tracks them for free
5. **Accumulate validation errors** - Don't fail fast when validating
6. **Only use Schema.Unknown for genuinely untyped values** - The `cause` field on error types is the canonical example (caught JS exceptions can be any value). Never use Schema.Unknown or Schema.Any for fields whose shape you can describe - define proper schemas instead.

## Additional Resources

For comprehensive error management documentation, consult `${CLAUDE_PLUGIN_ROOT}/references/llms-full.txt`.

Search for these sections:
- "Expected Errors" for creating typed errors
- "Error Accumulation" for collecting multiple errors
- "Sandboxing" for handling defects
- "Retrying" for retry policies
- "Timing Out" for timeout patterns
- "Two Types of Errors" for error philosophy
