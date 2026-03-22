---
name: effect-ts
description: This skill should be used when the user asks about Effect-TS patterns, services, layers, error handling, service composition, or writing/refactoring code that imports from 'effect'. Also covers Effect + Next.js integration with @prb/effect-next.
---

# Effect-TS Expert

Expert guidance for functional programming with the Effect library, covering error handling, dependency injection,
composability, and testing patterns.

## Prerequisites Check

Before starting any Effect-related work, verify the Effect-TS source code exists at `~/.effect`.

**If missing, stop immediately and inform the user.** Clone it before proceeding:

```bash
git clone https://github.com/Effect-TS/effect.git ~/.effect
```

## Research Strategy

Effect-TS has many ways to accomplish the same task. Proactively research best practices using the Task tool to spawn
research agents when working with Effect patterns, especially for moderate to high complexity tasks.

### Research Sources (Priority Order)

1. **Codebase Patterns First** — Examine similar patterns in the current project before implementing. If Effect patterns
   exist in the codebase, follow them for consistency. If no patterns exist, skip this step.

2. **Effect Source Code** — For complex type errors, unclear behavior, or implementation details, examine the Effect
   source at `~/.effect/packages/effect/src/`. This contains the core Effect logic and modules.

### When to Research

**HIGH Priority (Always Research):**

- Implementing Services, Layers, or complex dependency injection
- Error handling with multiple error types or complex error hierarchies
- Stream-based operations and reactive patterns
- Resource management with scoped effects and cleanup
- Concurrent/parallel operations and performance-critical code
- Testing patterns, especially unfamiliar test scenarios

**MEDIUM Priority (Research if Complex):**

- Refactoring imperative code (try-catch, promises) to Effect patterns
- Adding new service dependencies or restructuring service layers
- Custom error types or extending existing error hierarchies
- Integrations with external systems (databases, APIs, third-party services)

### Research Approach

- Spawn multiple concurrent Task agents when investigating multiple related patterns
- Focus on finding canonical, readable, and maintainable solutions rather than clever optimizations
- Verify suggested approaches against existing codebase patterns for consistency (if patterns exist)
- When multiple approaches are possible, research to find the most idiomatic Effect-TS solution

## Codebase Pattern Discovery

When working in a project that uses Effect, check for existing patterns before implementing new code:

1. **Search for Effect imports** — Look for files importing from `'effect'` to understand existing usage
2. **Identify service patterns** — Find how Services and Layers are structured in the project
3. **Note error handling conventions** — Check how errors are defined and propagated
4. **Examine test patterns** — Look at how Effect code is tested in the project

**If no Effect patterns exist in the codebase**, proceed using canonical patterns from the Effect source and examples.
Do not block on missing codebase patterns.

## Effect Principles

Apply these core principles when writing Effect code:

### Error Handling

- Use Effect's typed error system instead of throwing exceptions
- Define descriptive error types with proper error propagation
- Use `Effect.fail`, `Effect.catchTag`, `Effect.catchAll` for error control flow
- See `./references/critical-rules.md` for forbidden patterns

### Dependency Injection

- Implement dependency injection using Services and Layers
- Define services with `Context.Tag`
- Compose layers with `Layer.merge`, `Layer.provide`
- Use `Effect.provide` to inject dependencies

### Composability

- Leverage Effect's composability for complex operations
- Use appropriate constructors: `Effect.succeed`, `Effect.fail`, `Effect.tryPromise`, `Effect.try`
- Apply proper resource management with scoped effects
- Chain operations with `Effect.flatMap`, `Effect.map`, `Effect.tap`

### Code Quality

- Write type-safe code that leverages Effect's type system
- Use `Effect.gen` for readable sequential code
- Implement proper testing patterns using Effect's testing utilities
- Prefer `Effect.fn()` for automatic telemetry and better stack traces

## Critical Rules

Read and internalize `./references/critical-rules.md` before writing any Effect code. Key guidelines:

- **INEFFECTIVE:** try-catch in Effect.gen (Effect failures aren't thrown)
- **AVOID:** Type assertions (as never/any/unknown)
- **RECOMMENDED:** `return yield*` pattern for errors (makes termination explicit)

## Common Failure Modes

Quick links to patterns that frequently cause issues:

- **SubscriptionRef version mismatch** — `unsafeMake is not a function` → [Quick Reference](#subscriptionref-reactive-references)
- **Cancellation vs Failure** — Interrupts aren't errors → [Error Taxonomy](#error-taxonomy)
- **Option vs null** — Use Option internally, null at boundaries → [option-null.md](./references/option-null.md)
- **Stream backpressure** — Infinite streams hang → [streams.md](./references/streams.md)

## Explaining Solutions

When providing solutions, explain the Effect-TS concepts being used and why they're appropriate for the specific use
case. If encountering patterns not covered in the documentation, suggest improvements while maintaining consistency with
existing codebase patterns (when they exist).

## Quick Reference

### Creating Effects

```typescript
Effect.succeed(value)           // Wrap success value
Effect.fail(error)              // Create failed effect
Effect.tryPromise(fn)           // Wrap promise-returning function
Effect.try(fn)                  // Wrap synchronous throwing function
Effect.sync(fn)                 // Wrap synchronous non-throwing function
```

### Composing Effects

```typescript
Effect.flatMap(effect, fn)      // Chain effects
Effect.map(effect, fn)          // Transform success value
Effect.tap(effect, fn)          // Side effect without changing value
Effect.all([...effects])        // Run effects (concurrency configurable)
Effect.forEach(items, fn)       // Map over items with effects

// Collect ALL errors (not just first)
Effect.all([e1, e2, e3], { mode: "validate" })  // Returns all failures

// Partial success handling
Effect.partition([e1, e2, e3])  // Returns [failures, successes]
```

### Error Handling

```typescript
// Define typed errors with Data.TaggedError (preferred)
class UserNotFoundError extends Data.TaggedError("UserNotFoundError")<{
  userId: string
}> {}

// Direct yield of errors (no Effect.fail wrapper needed)
Effect.gen(function* () {
  if (!user) {
    return yield* new UserNotFoundError({ userId })
  }
})

Effect.catchTag(effect, tag, fn) // Handle specific error tag
Effect.catchAll(effect, fn)      // Handle all errors
Effect.result(effect)            // Convert to Exit value
Effect.orElse(effect, alt)       // Fallback effect
```

### Error Taxonomy

Categorize errors for appropriate handling:

| Category                | Examples                   | Handling                  |
| ----------------------- | -------------------------- | ------------------------- |
| **Expected Rejections** | User cancel, deny          | Graceful exit, no retry   |
| **Domain Errors**       | Validation, business rules | Show to user, don't retry |
| **Defects**             | Bugs, assertions           | Log + alert, investigate  |
| **Interruptions**       | Fiber cancel, timeout      | Cleanup, may retry        |
| **Unknown/Foreign**     | Thrown exceptions          | Normalize at boundary     |

```typescript
// Pattern: Normalize unknown errors at boundary
const safeBoundary = Effect.catchAllDefect(effect, (defect) =>
  Effect.fail(new UnknownError({ cause: defect }))
)

// Pattern: Catch user-initiated cancellations separately
Effect.catchTag(effect, "UserCancelledError", () => Effect.succeed(null))

// Pattern: Handle interruptions differently from failures
Effect.onInterrupt(effect, () => Effect.log("Operation cancelled"))
```

### Pattern Matching (Match Module)

**Default branching tool for tagged unions and complex conditionals.**

```typescript
import { Match } from "effect"

// Type-safe exhaustive matching on tagged errors
const handleError = Match.type<AppError>().pipe(
  Match.tag("UserCancelledError", () => null),          // Expected rejection
  Match.tag("ValidationError", (e) => e.message),       // Domain error
  Match.tag("NetworkError", () => "Connection failed"), // Retryable
  Match.exhaustive  // Compile error if case missing
)

// Replace nested catchTag chains
// BEFORE: effect.pipe(catchTag("A", ...), catchTag("B", ...), catchTag("C", ...))
// AFTER:
Effect.catchAll(effect, (error) =>
  Match.value(error).pipe(
    Match.tag("A", handleA),
    Match.tag("B", handleB),
    Match.tag("C", handleC),
    Match.exhaustive
  )
)

// Match on values (cleaner than if/else)
const describe = Match.value(status).pipe(
  Match.when("pending", () => "Loading..."),
  Match.when("success", () => "Done!"),
  Match.orElse(() => "Unknown")
)
```

### Services and Layers

```typescript
// Pattern 1: Context.Tag (implementation provided separately via Layer)
class MyService extends Context.Tag("MyService")<MyService, { ... }>() {}
const MyServiceLive = Layer.succeed(MyService, { ... })
Effect.provide(effect, MyServiceLive)

// Pattern 2: Effect.Service (default implementation bundled)
class UserRepo extends Effect.Service<UserRepo>()("UserRepo", {
  effect: Effect.gen(function* () {
    const db = yield* Database
    return { findAll: db.query("SELECT * FROM users") }
  }),
  dependencies: [Database.Default],  // Optional service dependencies
  accessors: true                     // Auto-generate method accessors
}) {}
Effect.provide(effect, UserRepo.Default)  // .Default layer auto-generated
// Use UserRepo.DefaultWithoutDependencies when deps provided separately

// Effect.Service with parameters (3.16.0+)
class ConfiguredApi extends Effect.Service<ConfiguredApi>()("ConfiguredApi", {
  effect: (config: { baseUrl: string }) =>
    Effect.succeed({ fetch: (path: string) => `${config.baseUrl}/${path}` })
}) {}

// Pattern 3: Context.Reference (defaultable tags - 3.11.0+)
class SpecialNumber extends Context.Reference<SpecialNumber>()(
  "SpecialNumber",
  { defaultValue: () => 2048 }
) {}
// No Layer required if default value suffices

// Pattern 4: Context.ReadonlyTag (covariant - 3.18.0+)
// Use for functions that consume services without modifying the type
function effectHandler<I, A, E, R>(service: Context.ReadonlyTag<I, Effect.Effect<A, E, R>>) {
  // Handler can use service in a covariant position
}
```

### Generator Pattern

```typescript
Effect.gen(function* () {
  const a = yield* effectA;
  const b = yield* effectB;
  if (error) {
    return yield* Effect.fail(new MyError());
  }
  return result;
});

// Effect.fn - automatic tracing and telemetry (preferred for named functions)
const fetchUser = Effect.fn("fetchUser")(function* (id: string) {
  const db = yield* Database
  return yield* db.query(id)
})
// Creates spans, captures call sites, provides better stack traces
```

### Resource Management

```typescript
Effect.acquireUseRelease(acquire, use, release)  // Bracket pattern
Effect.scoped(effect)                            // Scope lifetime to effect
Effect.addFinalizer(cleanup)                     // Register cleanup action
```

### Duration

Effect accepts human-readable duration strings anywhere a `DurationInput` is expected:

```typescript
// String syntax (preferred) - singular or plural forms work
Duration.toMillis("5 minutes")    // 300000
Duration.toMillis("1 minute")     // 60000
Duration.toMillis("30 seconds")   // 30000
Duration.toMillis("100 millis")   // 100

// Verbose syntax (avoid)
Duration.toMillis(Duration.minutes(5))  // Same result, more verbose

// Common units: millis, seconds, minutes, hours, days, weeks
// Also: nanos, micros
```

### Scheduling

```typescript
Effect.retry(effect, Schedule.exponential("100 millis"))  // Retry with backoff
Effect.repeat(effect, Schedule.fixed("1 second"))         // Repeat on schedule
Schedule.compose(s1, s2)                                  // Combine schedules
```

### State Management

```typescript
Ref.make(initialValue)       // Mutable reference
Ref.get(ref)                 // Read value
Ref.set(ref, value)          // Write value
Deferred.make<E, A>()        // One-time async value
```

### SubscriptionRef (Reactive References)

```typescript
// WARNING: Never use unsafeMake - it may not exist in your Effect version.
// If you see "unsafeMake is not a function", use the safe API below.

SubscriptionRef.make(initial)      // Create reactive reference (safe)
SubscriptionRef.get(ref)           // Read current value
SubscriptionRef.set(ref, value)    // Update value (notifies subscribers)
SubscriptionRef.changes(ref)       // Stream of value changes

// React integration (effect-atom pattern)
const ref = yield* SubscriptionRef.make<User | null>(null)
// Hook reads: useSubscriptionRef(ref) — returns current value or null
// Handle null explicitly in components
```

### Concurrency

```typescript
Effect.fork(effect)              // Run in background fiber
Fiber.join(fiber)                // Wait for fiber result
Effect.race(effect1, effect2)    // First to complete wins
Effect.all([...effects], { concurrency: "unbounded" })
```

### Configuration & Environment Variables

```typescript
import { Config, ConfigProvider, Effect, Layer, Redacted } from "effect"

// Basic config values
const port = Config.number("PORT")                    // Required number
const host = Config.string("HOST").pipe(              // Optional with default
  Config.withDefault("localhost")
)

// Sensitive values (masked in logs)
const apiKey = Config.redacted("API_KEY")             // Returns Redacted<string>
const secret = Redacted.value(yield* apiKey)          // Unwrap when needed

// Nested configuration with prefix
const dbConfig = Config.all({
  host: Config.string("HOST"),
  port: Config.number("PORT"),
  name: Config.string("NAME"),
}).pipe(Config.nested("DATABASE"))                    // DATABASE_HOST, DATABASE_PORT, etc.

// Using config in effects
const program = Effect.gen(function* () {
  const p = yield* Config.number("PORT")
  const key = yield* Config.redacted("API_KEY")
  return { port: p, apiKey: Redacted.value(key) }
})

// Custom config provider (e.g., from object instead of env)
const customProvider = ConfigProvider.fromMap(
  new Map([["PORT", "3000"], ["API_KEY", "secret"]])
)
const withCustomConfig = Effect.provide(
  program,
  Layer.setConfigProvider(customProvider)
)

// Config validation and transformation
const validPort = Config.number("PORT").pipe(
  Config.validate({
    message: "Port must be between 1 and 65535",
    validation: (n) => n >= 1 && n <= 65535,
  })
)
```

### Array Operations

```typescript
import { Array as Arr, Order } from "effect"

// Sorting with built-in orderings (accepts any Iterable)
Arr.sort([3, 1, 2], Order.number)              // [1, 2, 3]
Arr.sort(["b", "a", "c"], Order.string)        // ["a", "b", "c"]
Arr.sort(new Set([3n, 1n, 2n]), Order.bigint)  // [1n, 2n, 3n]

// Sort by derived value
Arr.sortWith(users, (u) => u.age, Order.number)

// Sort by multiple criteria
Arr.sortBy(
  users,
  Order.mapInput(Order.number, (u: User) => u.age),
  Order.mapInput(Order.string, (u: User) => u.name)
)

// Built-in orderings: Order.string, Order.number, Order.bigint, Order.boolean, Order.Date
// Reverse ordering: Order.reverse(Order.number)
```

### Utility Functions

```typescript
import { constVoid as noop } from "effect/Function"

// constVoid returns undefined, useful as a no-operation callback
noop()  // undefined

// Common use cases:
Effect.tap(effect, noop)              // Ignore value, just run effect
Promise.catch(noop)                   // Swallow errors
eventEmitter.on("event", noop)        // Register empty handler
```

### Deprecations

- **`BigDecimal.fromNumber`** — Use `BigDecimal.unsafeFromNumber` instead (3.11.0+)
- **`Schema.annotations()`** — Now removes previously set identifier annotations; identifiers are tied to the schema's
  `ast` reference only (3.17.10)

## Additional Resources

### Local Effect Resources

- **`~/.effect/packages/effect/src/`** — Core Effect modules and implementation

### External Resources

- **Effect-Atom** — https://github.com/tim-smart/effect-atom (open in browser for reactive state management patterns)

### Reference Files

- **`./references/critical-rules.md`** — Forbidden patterns and mandatory conventions
- **`./references/effect-atom.md`** — Effect-Atom reactive state management for React
- **`./references/next-js.md`** — Effect + Next.js 15+ App Router integration patterns
- **`./references/option-null.md`** — Option vs null boundary patterns
- **`./references/streams.md`** — Stream patterns and backpressure gotchas
- **`./references/testing.md`** — Vitest deterministic testing patterns
