---
name: effect-error-handling
description: Use when Effect error handling patterns including catchAll, catchTag, either, option, and typed errors. Use for handling expected errors in Effect applications.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
---

# Effect Error Handling

Master type-safe error handling in Effect applications. This skill covers
expected errors, error recovery, selective error handling, and error
transformations using Effect's error management operators.

## Expected Errors vs Defects

Effect distinguishes between two types of failures:

- **Expected Errors (E channel)**: Recoverable errors tracked in the type system
- **Defects**: Unexpected failures (bugs, programming errors)

```typescript
import { Effect } from "effect"

// Expected error - tracked in type
interface ValidationError {
  _tag: "ValidationError"
  field: string
  message: string
}

const validateEmail = (email: string): Effect.Effect<string, ValidationError, never> => {
  if (!email.includes("@")) {
    return Effect.fail({
      _tag: "ValidationError",
      field: "email",
      message: "Invalid email format"
    })
  }
  return Effect.succeed(email)
}

// Defect - throws, becomes unexpected failure
const riskyOperation = Effect.sync(() => {
  throw new Error("Unexpected error") // This is a defect
})

// Proper way - expected error
const safeOperation = Effect.try({
  try: () => {
    // Code that might throw
    return riskyParse(data)
  },
  catch: (error) => ({
    _tag: "ParseError",
    message: String(error)
  })
})
```

## Tagged Error Types

Use tagged unions for error types to enable pattern matching:

```typescript
import { Effect } from "effect"

// Define tagged error types
interface NotFoundError {
  _tag: "NotFoundError"
  id: string
}

interface UnauthorizedError {
  _tag: "UnauthorizedError"
  userId: string
}

interface NetworkError {
  _tag: "NetworkError"
  message: string
}

type AppError = NotFoundError | UnauthorizedError | NetworkError

// Functions returning typed errors
const fetchUser = (id: string): Effect.Effect<User, NotFoundError | NetworkError, never> => {
  // Implementation
}

const authenticate = (token: string): Effect.Effect<User, UnauthorizedError | NetworkError, never> => {
  // Implementation
}
```

## Catching All Errors

### Effect.catchAll - Recover from Any Error

Catches all expected errors and provides fallback:

```typescript
import { Effect } from "effect"

const program = Effect.gen(function* () {
  const user = yield* fetchUser("123")
  return user
}).pipe(
  Effect.catchAll((error) =>
    Effect.succeed({ id: "default", name: "Guest" })
  )
)
// Effect<User, never, never> - Error channel is now never

// With error inspection
const programWithLogging = Effect.gen(function* () {
  const user = yield* fetchUser("123")
  return user
}).pipe(
  Effect.catchAll((error) => {
    console.error("Error occurred:", error)
    return Effect.succeed(defaultUser)
  })
)

// Fallback to another effect
const programWithFallback = pipe(
  fetchUser("123"),
  Effect.catchAll(() => fetchUserFromCache("123"))
)
```

## Selective Error Handling

### Effect.catchTag - Handle Specific Error Types

Catches errors by their `_tag` field:

```typescript
import { Effect, pipe } from "effect"

const program = pipe(
  fetchUser("123"),
  Effect.catchTag("NotFoundError", (error) =>
    Effect.succeed({ id: error.id, name: "Not Found" })
  )
)
// Still can fail with NetworkError

// Handling multiple tags
const program2 = pipe(
  authenticatedRequest(),
  Effect.catchTag("UnauthorizedError", (error) =>
    Effect.fail({ _tag: "LoginRequired" })
  ),
  Effect.catchTag("NetworkError", (error) =>
    retryRequest()
  )
)

// Using Effect.gen with early return
const program3 = Effect.gen(function* () {
  const result = yield* riskyOperation().pipe(
    Effect.catchTag("TemporaryError", () =>
      Effect.succeed(null)
    )
  )
  return result
})
```

### Effect.catchTags - Handle Multiple Error Types

```typescript
import { Effect, pipe } from "effect"

const program = pipe(
  complexOperation(),
  Effect.catchTags({
    NotFoundError: (error) =>
      Effect.succeed(defaultValue),
    UnauthorizedError: (error) =>
      Effect.fail({ _tag: "LoginRequired" }),
    NetworkError: (error) =>
      retryOperation()
  })
)

// With different recovery strategies
const programWithStrategies = pipe(
  processPayment(amount),
  Effect.catchTags({
    InsufficientFunds: (error) =>
      Effect.fail({ _tag: "PaymentDeclined", reason: "insufficient-funds" }),
    NetworkError: () =>
      retryPayment(amount),
    ValidationError: (error) =>
      Effect.fail({ _tag: "InvalidPayment", field: error.field })
  })
)
```

### Effect.catchIf - Conditional Error Handling

Catches errors that match a predicate:

```typescript
import { Effect, pipe } from "effect"

const isRetryable = (error: AppError): boolean => {
  return error._tag === "NetworkError" || error._tag === "TimeoutError"
}

const program = pipe(
  fetchData(),
  Effect.catchIf(isRetryable, (error) =>
    retryFetchData()
  )
)

// With type narrowing
const program2 = pipe(
  operation(),
  Effect.catchIf(
    (error): error is NetworkError => error._tag === "NetworkError",
    (error) => {
      // TypeScript knows error is NetworkError here
      console.log("Network error:", error.message)
      return retry()
    }
  )
)
```

### Effect.catchSome - Partial Error Handling

Catches errors and optionally handles them:

```typescript
import { Effect, Option, pipe } from "effect"

const program = pipe(
  fetchUser("123"),
  Effect.catchSome((error) => {
    if (error._tag === "NotFoundError") {
      return Option.some(Effect.succeed(guestUser))
    }
    return Option.none() // Don't handle, propagate error
  })
)

// Complex decision logic
const programWithDecision = pipe(
  processRequest(request),
  Effect.catchSome((error) => {
    if (error._tag === "RateLimitError" && error.retryAfter < 1000) {
      return Option.some(
        Effect.sleep(error.retryAfter).pipe(
          Effect.andThen(processRequest(request))
        )
      )
    }
    return Option.none()
  })
)
```

## Converting Errors

### Effect.either - Convert to Either<Success, Error>

Transforms an effect into one that cannot fail, wrapping result in Either:

```typescript
import { Effect, Either } from "effect"

const program = Effect.gen(function* () {
  const result = yield* fetchUser("123").pipe(Effect.either)

  if (Either.isLeft(result)) {
    // Handle error
    console.error("Error:", result.left)
    return null
  } else {
    // Handle success
    return result.right
  }
})
// Effect<User | null, never, never>

// Pattern matching on Either
const program2 = pipe(
  fetchUser("123"),
  Effect.either,
  Effect.map(
    Either.match({
      onLeft: (error) => ({ success: false, error }),
      onRight: (user) => ({ success: true, data: user })
    })
  )
)
```

### Effect.option - Convert to Option<Success>

Converts failures to None, success to Some:

```typescript
import { Effect, Option } from "effect"

const program = Effect.gen(function* () {
  const maybeUser = yield* fetchUser("123").pipe(Effect.option)

  if (Option.isNone(maybeUser)) {
    return guestUser
  } else {
    return maybeUser.value
  }
})
// Effect<User, never, never>

// Using Option.match
const program2 = pipe(
  fetchUser("123"),
  Effect.option,
  Effect.map(
    Option.match({
      onNone: () => "No user found",
      onSome: (user) => `Found: ${user.name}`
    })
  )
)
```

## Error Transformation

### Effect.mapError - Transform Error Types

```typescript
import { Effect, pipe } from "effect"

interface DbError {
  _tag: "DbError"
  code: string
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
    context: `Database operation failed: ${dbError.code}`
  }))
)

// Enriching errors with context
const enrichError = <E extends { message: string }>(
  context: string
) => (error: E) => ({
  ...error,
  message: `${context}: ${error.message}`
})

const programWithContext = pipe(
  fetchData(),
  Effect.mapError(enrichError("Failed to fetch user data"))
)
```

### Effect.tapError - Side Effects on Error

Perform side effects when an error occurs without changing it:

```typescript
import { Effect, pipe } from "effect"

const program = pipe(
  processPayment(amount),
  Effect.tapError((error) =>
    Effect.sync(() => {
      console.error("Payment failed:", error)
      logToMonitoring(error)
    })
  ),
  Effect.tapError((error) =>
    sendErrorNotification(error)
  )
)
// Error still propagates after taps
```

## Retry and Fallback Patterns

### Effect.orElse - Fallback Effect

Provide alternative effect on failure:

```typescript
import { Effect, pipe } from "effect"

const program = pipe(
  fetchFromPrimarySource(),
  Effect.orElse(() => fetchFromSecondarySource())
)

// With error-specific fallbacks
const programWithCheck = pipe(
  fetchData(),
  Effect.orElse((error) => {
    if (error._tag === "NetworkError") {
      return fetchFromCache()
    }
    return Effect.fail(error)
  })
)

// Multiple fallbacks
const programWithMultipleFallbacks = pipe(
  fetchFromPrimary(),
  Effect.orElse(() => fetchFromSecondary()),
  Effect.orElse(() => fetchFromTertiary()),
  Effect.orElse(() => Effect.succeed(defaultData))
)
```

### Effect.retry - Retry on Failure

```typescript
import { Effect, Schedule, pipe } from "effect"

// Retry with schedule
const program = pipe(
  fetchData(),
  Effect.retry(Schedule.recurs(3)) // Retry up to 3 times
)

// Exponential backoff
const programWithBackoff = pipe(
  fetchData(),
  Effect.retry(
    Schedule.exponential("100 millis", 2.0) // 100ms, 200ms, 400ms, ...
  )
)

// Conditional retry
const programConditionalRetry = pipe(
  fetchData(),
  Effect.retry({
    while: (error) => error._tag === "NetworkError",
    schedule: Schedule.recurs(5)
  })
)
```

## Combining Error Handlers

### Chaining Multiple Handlers

```typescript
import { Effect, pipe } from "effect"

const program = pipe(
  complexOperation(),
  Effect.catchTag("NotFoundError", () =>
    Effect.succeed(defaultValue)
  ),
  Effect.catchTag("NetworkError", () =>
    retryOperation()
  ),
  Effect.catchTag("UnauthorizedError", () =>
    Effect.fail({ _tag: "LoginRequired" })
  ),
  Effect.catchAll((unknownError) =>
    Effect.sync(() => {
      console.error("Unhandled error:", unknownError)
      return fallbackValue
    })
  )
)
```

### Error Accumulation

```typescript
import { Effect, Array } from "effect"

interface ValidationError {
  _tag: "ValidationError"
  errors: string[]
}

const validateAll = (fields: string[]) =>
  Effect.gen(function* () {
    const results = yield* Effect.all(
      fields.map(validateField),
      { mode: "either" } // Don't short-circuit on first error
    )

    const errors = results.filter(Either.isLeft)
    if (errors.length > 0) {
      return yield* Effect.fail({
        _tag: "ValidationError",
        errors: errors.map(e => e.left.message)
      })
    }

    return results.map(r => r.right)
  })
```

## Handling Defects

### Effect.catchAllCause - Handle Both Errors and Defects

```typescript
import { Effect, Cause, Exit, pipe } from "effect"

const program = pipe(
  riskyOperation(),
  Effect.catchAllCause((cause) => {
    if (Cause.isFailure(cause)) {
      // Expected error
      const error = Cause.failureOption(cause)
      return handleExpectedError(error)
    } else if (Cause.isDie(cause)) {
      // Defect (unexpected error)
      const defect = Cause.dieOption(cause)
      return handleDefect(defect)
    } else {
      // Interruption
      return Effect.succeed(defaultValue)
    }
  })
)
```

### Effect.sandbox - Expose Defects as Errors

Converts defects into the error channel for handling:

```typescript
import { Effect, Cause, pipe } from "effect"

const program = pipe(
  riskyOperation(),
  Effect.sandbox,
  Effect.catchAll((cause) => {
    console.error("Failure cause:", cause)
    return Effect.succeed(fallbackValue)
  })
)
```

## Best Practices

1. **Use Tagged Error Types**: Always tag errors with `_tag` for catchTag.

2. **Keep Error Types Specific**: Don't use generic Error. Define specific
   error types for each failure mode.

3. **Handle Errors Close to Source**: Catch errors where you have enough
   context to handle them properly.

4. **Use catchTag Over catchAll**: Prefer specific error handling to blanket
   catching.

5. **Convert at Boundaries**: Use either/option when interfacing with code that
   doesn't expect errors.

6. **Log Before Catching**: Use tapError to log before handling errors.

7. **Don't Swallow Errors**: Always handle errors meaningfully or propagate
   them.

8. **Use Retry Strategically**: Only retry transient failures, not all errors.

9. **Enrich Errors with Context**: Add context to errors as they propagate up.

10. **Document Error Types**: Clearly document what errors each function can
    produce.

## Common Pitfalls

1. **Using catchAll Everywhere**: Over-using catchAll hides error types. Use
   catchTag.

2. **Not Tagging Errors**: Without tags, you can't use catchTag effectively.

3. **Swallowing Errors**: Catching errors and returning success without proper
   handling.

4. **Infinite Retry**: Not limiting retries or checking error types before
   retrying.

5. **Losing Error Information**: Transforming errors without preserving
   important details.

6. **Not Handling Defects**: Forgetting that some operations can throw
   unexpectedly.

7. **Wrong Error Boundaries**: Catching errors too early or too late in the
   pipeline.

8. **Type Widening**: Losing specific error types by combining with catchAll
   too early.

9. **Ignoring Error Channel**: Not checking the E type parameter when composing
   effects.

10. **Not Testing Error Paths**: Only testing happy paths, not failure
    scenarios.

## When to Use This Skill

Use effect-error-handling when you need to:

- Handle expected errors in a type-safe manner
- Recover from failures with fallback logic
- Implement retry strategies for transient failures
- Transform errors between different layers
- Log errors without stopping execution
- Implement error boundaries in applications
- Handle specific error types differently
- Convert errors to Option or Either
- Accumulate validation errors
- Build resilient error recovery systems

## Resources

### Official Documentation

- [Error Management](https://effect.website/docs/error-management/expected-errors)
- [Expected Errors](https://effect.website/docs/error-management/expected-errors)
- [Unexpected Errors](https://effect.website/docs/error-management/unexpected-errors)
- [Error Channel Operations](https://effect.website/docs/error-management/error-channel-operations)
- [Fallback](https://effect.website/docs/error-management/fallback)
- [Retrying](https://effect.website/docs/error-management/retrying)
- [Sandboxing](https://effect.website/docs/error-management/sandboxing)

### Related Skills

- effect-core-patterns - Basic Effect operations
- effect-testing - Testing error scenarios
