---
name: effect-logging-discipline
description: Enforce Effect.log over console.log in TMNL. Effect-native logging provides structured output, dynamic log levels, annotations, spans, and observability integration.
model_invoked: true
triggers:
  - "console.log"
  - "console.error"
  - "console.warn"
  - "logging"
  - "debug"
  - "tracing"
  - "observability"
---

# Effect Logging Discipline

## CRITICAL RULE: No console.log

**BANNED:** `console.log`, `console.error`, `console.warn`, `console.debug`

**REQUIRED:** `Effect.log`, `Effect.logError`, `Effect.logWarning`, `Effect.logDebug`

### Why Effect.log?

| Feature | console.log | Effect.log |
|---------|-------------|------------|
| Dynamic log levels | ❌ | ✅ Per-effect control |
| Structured output | ❌ | ✅ timestamp, level, fiber |
| Custom destinations | ❌ | ✅ File, service, etc. |
| Environment-based | ❌ | ✅ Different levels per env |
| Annotations | ❌ | ✅ Custom metadata |
| Spans | ❌ | ✅ Duration tracking |
| Disable in tests | ❌ Pollutes output | ✅ `LogLevel.None` |

---

## Pattern 1: Basic Logging

### Effect Context

```typescript
import { Effect } from "effect"

// INFO level (default, always shown)
yield* Effect.log("Application started")
yield* Effect.log("Processing", "user", userId)

// Multiple messages
yield* Effect.log("message1", "message2", "message3")
```

### Log Levels

```typescript
// DEBUG - Hidden by default, enable with Logger.withMinimumLogLevel(LogLevel.Debug)
yield* Effect.logDebug("Verbose debug info")

// INFO - Default, always shown
yield* Effect.logInfo("Operation completed")
yield* Effect.log("Same as logInfo")

// WARN - For potential issues
yield* Effect.logWarning("Deprecated API called")

// ERROR - For failures
yield* Effect.logError("Request failed", cause)

// FATAL - Unrecoverable
yield* Effect.logFatal("System shutdown required")
```

### Output Format

```
timestamp=2024-01-15T10:30:00.000Z level=INFO fiber=#0 message="Application started"
```

---

## Pattern 2: Annotations (Structured Context)

Add metadata to all logs within a scope:

```typescript
const program = Effect.gen(function* () {
  yield* Effect.log("Processing request")
  yield* Effect.log("Request complete")
}).pipe(
  Effect.annotateLogs("requestId", "req-123"),
  Effect.annotateLogs({ userId: "user-456", service: "auth" })
)

// Output:
// level=INFO message="Processing request" requestId=req-123 userId=user-456 service=auth
// level=INFO message="Request complete" requestId=req-123 userId=user-456 service=auth
```

---

## Pattern 3: Spans (Duration Tracking)

Measure operation duration:

```typescript
const operation = Effect.gen(function* () {
  yield* Effect.sleep("1 second")
  yield* Effect.log("The job is finished!")
}).pipe(
  Effect.withLogSpan("myOperation")
)

// Output:
// level=INFO message="The job is finished!" myOperation=1011ms
```

---

## Pattern 4: Scoped Logging in Services

```typescript
class SearchService extends Effect.Service<SearchService>()("app/SearchService", {
  effect: Effect.gen(function* () {
    const search = (query: string) =>
      Effect.gen(function* () {
        yield* Effect.logDebug(`Starting search for: ${query}`)
        const results = yield* performSearch(query)
        yield* Effect.log(`Found ${results.length} results`)
        return results
      }).pipe(
        Effect.annotateLogs("query", query),
        Effect.withLogSpan("SearchService.search")
      )

    return { search } as const
  }),
}) {}
```

---

## Pattern 5: React Components (Non-Effect Context)

For React components that can't use Effect.gen, create helper functions:

### Option A: Fire-and-forget logging (PREFERRED)

```typescript
import { Effect } from "effect"

// Module-level helper
const logInfo = (message: string, ...args: unknown[]) =>
  Effect.runFork(Effect.log(message, ...args.map(String)))

const logDebug = (message: string, ...args: unknown[]) =>
  Effect.runFork(Effect.logDebug(message, ...args.map(String)))

const logError = (message: string, error?: unknown) =>
  Effect.runFork(Effect.logError(message, error ? String(error) : undefined))

// Usage in React
function MyComponent() {
  useEffect(() => {
    logInfo("[MyComponent] Mounted")
    return () => logInfo("[MyComponent] Unmounted")
  }, [])
}
```

### Option B: Atom operation logging

```typescript
import { runtimeAtom } from "./atoms"

// Log within atom operations where you have Effect context
export const ops = {
  doSomething: runtimeAtom.fn<string>()((input, ctx) =>
    Effect.gen(function* () {
      yield* Effect.logDebug(`Processing: ${input}`)
      // ... work
      yield* Effect.log("Complete")
    })
  ),
}
```

---

## Pattern 6: Disable Logging in Tests

```typescript
import { Logger, LogLevel } from "effect"

// Method 1: Per-effect
Effect.runFork(
  program.pipe(Logger.withMinimumLogLevel(LogLevel.None))
)

// Method 2: Via layer
const silentLayer = Logger.minimumLogLevel(LogLevel.None)
Effect.runFork(program.pipe(Effect.provide(silentLayer)))

// Method 3: In vitest setup
// vitest.setup.ts
import { Logger, LogLevel, Effect } from "effect"
beforeAll(() => {
  // Global silent logger for tests
})
```

---

## Pattern 7: Enable Debug Logs

Debug logs are hidden by default:

```typescript
import { Logger, LogLevel } from "effect"

// Enable for specific effect
const debuggedEffect = myEffect.pipe(
  Logger.withMinimumLogLevel(LogLevel.Debug)
)

// Enable via layer
const debugLayer = Logger.minimumLogLevel(LogLevel.Debug)
```

---

## Migration Guide: console.log → Effect.log

### Before (BANNED)

```typescript
console.log(`[GenerativeContainer] MOUNT depth=${depth}`)
console.log(`[GenerativeContainer] prompt="${prompt?.substring(0, 60)}..."`)
console.error(`[GenerativeContainer] ERROR:`, err)
```

### After (REQUIRED)

```typescript
// If in Effect.gen context:
yield* Effect.log(`[GenerativeContainer] MOUNT depth=${depth}`)
yield* Effect.log(`[GenerativeContainer] prompt="${prompt?.substring(0, 60)}..."`)
yield* Effect.logError(`[GenerativeContainer] ERROR: ${err}`)

// If in React callback (fire-and-forget):
Effect.runFork(Effect.log(`[GenerativeContainer] MOUNT depth=${depth}`))
Effect.runFork(Effect.logError(`[GenerativeContainer] ERROR: ${err}`))

// Better: with annotations
Effect.runFork(
  Effect.log("MOUNT").pipe(
    Effect.annotateLogs({ component: "GenerativeContainer", depth })
  )
)
```

---

## Anti-Patterns (BANNED)

### 1. Raw console calls

```typescript
// BANNED
console.log("Debug:", value)
console.error("Error:", err)
console.warn("Warning")
console.debug("Trace")
```

### 2. Logging outside Effect without runFork

```typescript
// WRONG - Effect.log returns Effect, doesn't execute
Effect.log("This does nothing")

// CORRECT - Fire and forget
Effect.runFork(Effect.log("This executes"))
```

### 3. Mixing console and Effect.log

```typescript
// BANNED - Inconsistent
yield* Effect.log("Step 1")
console.log("Step 2")  // NO!
yield* Effect.log("Step 3")
```

---

## Canonical Examples

| Pattern | File |
|---------|------|
| Service logging | `src/lib/data-manager/v1/DataManager.ts` |
| Span usage | `src/lib/slider/v1/services/SliderService.ts` |
| Annotation usage | `src/lib/geoint/services/SearchService.ts` |

---

## Checklist: Logging Review

- [ ] No `console.log` calls
- [ ] No `console.error` calls
- [ ] No `console.warn` calls
- [ ] No `console.debug` calls
- [ ] Effect.log for INFO level
- [ ] Effect.logDebug for verbose debugging
- [ ] Effect.logError for errors with context
- [ ] Annotations for structured metadata
- [ ] Spans for operation timing
- [ ] Fire-and-forget wrapper for React callbacks

---

## Related Skills

- **effect-patterns** — General Effect-TS patterns
- **effect-service-authoring** — Service logging patterns
- **tmnl-debug-instrumentation** — Debug tooling
