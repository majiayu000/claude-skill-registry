---
name: effect-testing
description: Use when testing Effect code including Effect.gen in tests, test layers, mocking services, and testing error scenarios. Use for writing tests for Effect applications.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
---

# Effect Testing

Master testing Effect applications with test utilities, mock layers, and
patterns for testing effectful code. This skill covers unit testing, integration
testing, and testing concurrent and resource-managed code.

## Basic Effect Testing

### Testing with Effect.gen

```typescript
import { Effect } from "effect"
import { describe, it, expect } from "vitest"

describe("User Service", () => {
  it("should fetch user by ID", async () => {
    const program = Effect.gen(function* () {
      const user = yield* fetchUser("123")
      return user
    })

    const result = await Effect.runPromise(program.pipe(
      Effect.provide(TestLayer)
    ))

    expect(result.id).toBe("123")
    expect(result.name).toBe("Alice")
  })
})
```

### Testing Success and Failure

```typescript
import { Effect, Exit } from "effect"
import { describe, it, expect } from "vitest"

describe("Validation", () => {
  it("should succeed with valid email", async () => {
    const program = validateEmail("alice@example.com")

    const result = await Effect.runPromise(program)

    expect(result).toBe("alice@example.com")
  })

  it("should fail with invalid email", async () => {
    const program = validateEmail("invalid")

    const exit = await Effect.runPromiseExit(program)

    expect(Exit.isFailure(exit)).toBe(true)

    if (Exit.isFailure(exit)) {
      const error = Cause.failureOption(exit.cause)
      expect(error._tag).toBe("ValidationError")
    }
  })
})
```

## Mock Layers for Testing

### Creating Test Layers

```typescript
import { Context, Effect, Layer } from "effect"

interface UserRepository {
  findById: (id: string) => Effect.Effect<Option<User>, DbError, never>
  save: (user: User) => Effect.Effect<User, DbError, never>
}

const UserRepository = Context.GenericTag<UserRepository>("UserRepository")

// In-memory test implementation
const UserRepositoryTest = Layer.succeed(
  UserRepository,
  {
    findById: (id: string) =>
      Effect.succeed(
        id === "1"
          ? Option.some({ id: "1", name: "Alice", email: "alice@example.com" })
          : Option.none()
      ),

    save: (user: User) =>
      Effect.succeed(user)
  }
)

// Use in tests
const testProgram = Effect.gen(function* () {
  const repo = yield* UserRepository
  const user = yield* repo.findById("1")
  return user
}).pipe(
  Effect.provide(UserRepositoryTest)
)
```

### Stateful Mock Layers

```typescript
import { Context, Effect, Layer, Ref } from "effect"

// Mock with state
const UserRepositoryStateful = Layer.effect(
  UserRepository,
  Effect.gen(function* () {
    const storage = yield* Ref.make<Map<string, User>>(new Map([
      ["1", { id: "1", name: "Alice", email: "alice@example.com" }]
    ]))

    return {
      findById: (id: string) =>
        storage.get.pipe(
          Effect.map((map) => {
            const user = map.get(id)
            return user ? Option.some(user) : Option.none()
          })
        ),

      save: (user: User) =>
        storage.update((map) => map.set(user.id, user)).pipe(
          Effect.map(() => user)
        )
    }
  })
)

// Test with state
describe("User Repository", () => {
  it("should save and retrieve user", async () => {
    const program = Effect.gen(function* () {
      const repo = yield* UserRepository

      const newUser = { id: "2", name: "Bob", email: "bob@example.com" }
      yield* repo.save(newUser)

      const retrieved = yield* repo.findById("2")
      return retrieved
    }).pipe(
      Effect.provide(UserRepositoryStateful)
    )

    const result = await Effect.runPromise(program)

    expect(Option.isSome(result)).toBe(true)
    if (Option.isSome(result)) {
      expect(result.value.name).toBe("Bob")
    }
  })
})
```

## Spy Layers

### Recording Calls

```typescript
import { Context, Effect, Layer, Ref } from "effect"

interface LoggerCalls {
  info: string[]
  error: string[]
}

const LoggerSpy = Layer.effect(
  Logger,
  Effect.gen(function* () {
    const calls = yield* Ref.make<LoggerCalls>({
      info: [],
      error: []
    })

    return {
      logger: {
        info: (message: string) =>
          calls.update((c) => ({
            ...c,
            info: [...c.info, message]
          })),

        error: (message: string) =>
          calls.update((c) => ({
            ...c,
            error: [...c.error, message]
          }))
      },

      getCalls: () => calls.get
    }
  })
)

// Test with spy
describe("User Service", () => {
  it("should log user creation", async () => {
    const program = Effect.gen(function* () {
      const spy = yield* LoggerSpy
      const service = yield* UserService

      yield* service.createUser({ name: "Alice" })

      const calls = yield* spy.getCalls()
      return calls
    }).pipe(
      Effect.provide(Layer.merge(LoggerSpy, UserServiceLive))
    )

    const calls = await Effect.runPromise(program)

    expect(calls.info).toContain("Creating user: Alice")
  })
})
```

## Testing Error Scenarios

### Testing Expected Errors

```typescript
import { Effect } from "effect"
import { describe, it, expect } from "vitest"

describe("Error Handling", () => {
  it("should handle NotFoundError", async () => {
    const program = Effect.gen(function* () {
      const result = yield* fetchUser("999").pipe(
        Effect.catchTag("NotFoundError", (error) =>
          Effect.succeed({ id: "default", name: "Guest" })
        )
      )
      return result
    })

    const result = await Effect.runPromise(program.pipe(
      Effect.provide(TestLayer)
    ))

    expect(result.name).toBe("Guest")
  })

  it("should propagate unhandled errors", async () => {
    const program = Effect.gen(function* () {
      const result = yield* fetchUser("999")
      return result
    })

    await expect(
      Effect.runPromise(program.pipe(
        Effect.provide(TestLayer)
      ))
    ).rejects.toThrow()
  })
})
```

### Testing Error Recovery

```typescript
import { Effect } from "effect"
import { describe, it, expect } from "vitest"

describe("Retry Logic", () => {
  it("should retry on network error", async () => {
    let attempts = 0

    const unstableOperation = Effect.gen(function* () {
      attempts++
      if (attempts < 3) {
        return yield* Effect.fail({ _tag: "NetworkError" })
      }
      return yield* Effect.succeed("Success")
    })

    const program = unstableOperation.pipe(
      Effect.retry(Schedule.recurs(5))
    )

    const result = await Effect.runPromise(program)

    expect(result).toBe("Success")
    expect(attempts).toBe(3)
  })
})
```

## Testing Concurrent Code

### Testing Parallel Execution

```typescript
import { Effect, Ref } from "effect"
import { describe, it, expect } from "vitest"

describe("Concurrent Operations", () => {
  it("should process items in parallel", async () => {
    const program = Effect.gen(function* () {
      const processed = yield* Ref.make<string[]>([])

      const items = ["a", "b", "c", "d", "e"]

      yield* Effect.all(
        items.map((item) =>
          Effect.gen(function* () {
            yield* Effect.sleep("10 millis")
            yield* processed.update((p) => [...p, item])
          })
        ),
        { concurrency: "unbounded" }
      )

      return yield* processed.get
    })

    const result = await Effect.runPromise(program)

    expect(result).toHaveLength(5)
    expect(result).toContain("a")
    expect(result).toContain("b")
  })
})
```

### Testing Fiber Interruption

```typescript
import { Effect, Fiber, Ref } from "effect"
import { describe, it, expect } from "vitest"

describe("Interruption", () => {
  it("should interrupt long-running task", async () => {
    const program = Effect.gen(function* () {
      const completed = yield* Ref.make(false)

      const fiber = yield* Effect.fork(
        Effect.gen(function* () {
          yield* Effect.sleep("1 second")
          yield* completed.set(true)
        })
      )

      yield* Effect.sleep("100 millis")
      yield* Fiber.interrupt(fiber)

      return yield* completed.get
    })

    const result = await Effect.runPromise(program)

    expect(result).toBe(false)
  })
})
```

## Testing Resource Management

### Testing Cleanup

```typescript
import { Effect, Ref } from "effect"
import { describe, it, expect } from "vitest"

describe("Resource Management", () => {
  it("should clean up resources on success", async () => {
    const program = Effect.gen(function* () {
      const cleaned = yield* Ref.make(false)

      yield* Effect.scoped(
        Effect.gen(function* () {
          yield* Effect.addFinalizer(() =>
            cleaned.set(true)
          )

          yield* Effect.succeed("done")
        })
      )

      return yield* cleaned.get
    })

    const result = await Effect.runPromise(program)

    expect(result).toBe(true)
  })

  it("should clean up resources on failure", async () => {
    const program = Effect.gen(function* () {
      const cleaned = yield* Ref.make(false)

      const result = yield* Effect.scoped(
        Effect.gen(function* () {
          yield* Effect.addFinalizer(() =>
            cleaned.set(true)
          )

          yield* Effect.fail({ _tag: "TestError" })
        })
      ).pipe(
        Effect.catchAll(() => Effect.succeed("handled"))
      )

      const wasCleanedUp = yield* cleaned.get

      return { result, wasCleanedUp }
    })

    const { result, wasCleanedUp } = await Effect.runPromise(program)

    expect(result).toBe("handled")
    expect(wasCleanedUp).toBe(true)
  })
})
```

## Property-Based Testing

### Using fast-check with Effect

```typescript
import { Effect } from "effect"
import { describe, it } from "vitest"
import * as fc from "fast-check"

describe("Property Tests", () => {
  it("should always succeed for valid emails", () => {
    fc.assert(
      fc.asyncProperty(
        fc.emailAddress(),
        async (email) => {
          const program = validateEmail(email)

          const result = await Effect.runPromise(program)

          expect(result).toBe(email.toLowerCase())
        }
      )
    )
  })

  it("should handle any string input", () => {
    fc.assert(
      fc.asyncProperty(
        fc.string(),
        async (input) => {
          const program = parseJSON(input).pipe(
            Effect.catchAll(() => Effect.succeed(null))
          )

          const result = await Effect.runPromise(program)

          // Should never throw
          expect(result).toBeDefined()
        }
      )
    )
  })
})
```

## Testing Best Practices

### Test Organization

```typescript
import { Effect, Layer } from "effect"
import { describe, it, beforeEach, expect } from "vitest"

describe("User Service", () => {
  // Shared test layer
  const TestLayer = Layer.merge(
    UserRepositoryTest,
    LoggerTest,
    ConfigTest
  )

  describe("createUser", () => {
    it("should create user with valid data", async () => {
      const program = Effect.gen(function* () {
        const service = yield* UserService
        const user = yield* service.createUser({
          name: "Alice",
          email: "alice@example.com"
        })
        return user
      }).pipe(
        Effect.provide(TestLayer)
      )

      const result = await Effect.runPromise(program)

      expect(result.name).toBe("Alice")
    })

    it("should fail with invalid email", async () => {
      const program = Effect.gen(function* () {
        const service = yield* UserService
        const user = yield* service.createUser({
          name: "Bob",
          email: "invalid"
        })
        return user
      }).pipe(
        Effect.provide(TestLayer)
      )

      await expect(Effect.runPromise(program)).rejects.toThrow()
    })
  })
})
```

## Best Practices

1. **Use Test Layers**: Create dedicated test implementations for services.

2. **Test Error Paths**: Test both success and failure scenarios.

3. **Mock Dependencies**: Use layers to inject test dependencies.

4. **Test Concurrency**: Verify concurrent behavior with multiple fibers.

5. **Test Cleanup**: Ensure resources are cleaned up properly.

6. **Use Property Tests**: Test invariants with property-based testing.

7. **Isolate Tests**: Each test should be independent.

8. **Test Interruption**: Verify correct behavior on interruption.

9. **Use Spies**: Track calls to verify behavior.

10. **Test Edge Cases**: Cover boundary conditions and error cases.

## Common Pitfalls

1. **Not Providing Layers**: Forgetting to provide required services.

2. **Shared State**: Tests interfering with each other via shared state.

3. **Not Testing Errors**: Only testing happy paths.

4. **Missing Cleanup Tests**: Not verifying finalizers execute.

5. **Ignoring Concurrency**: Not testing concurrent behavior.

6. **Flaky Tests**: Race conditions in concurrent tests.

7. **Over-Mocking**: Mocking too much, losing integration value.

8. **Not Testing Interruption**: Missing interruption scenarios.

9. **Hardcoded Timing**: Tests that depend on specific timing.

10. **Missing Exit Checks**: Not verifying Exit values properly.

## When to Use This Skill

Use effect-testing when you need to:

- Write unit tests for Effect code
- Create integration tests with dependencies
- Test error handling and recovery
- Verify concurrent behavior
- Test resource cleanup
- Mock external services
- Verify retry logic
- Test interruption handling
- Use property-based testing
- Build reliable test suites

## Resources

### Official Documentation

- [Effect Testing](https://effect.website/docs/testing/)
- [Testing Guide](https://effect.website/docs/guides/testing/)

### Testing Libraries

- [Vitest](https://vitest.dev/)
- [Jest](https://jestjs.io/)
- [fast-check](https://github.com/dubzzz/fast-check)

### Related Skills

- effect-core-patterns - Basic Effect operations
- effect-dependency-injection - Creating test layers
- effect-error-handling - Testing error scenarios
- effect-concurrency - Testing concurrent code
- effect-resource-management - Testing cleanup
