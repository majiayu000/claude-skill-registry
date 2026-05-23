---
name: effect-time-tracing-logging
description: Time with Clock/Duration, tracing spans, and structured logging. Use for time-based logic, deadlines, and observability.
allowed-tools: Read, Grep, Glob, Edit, Write
---

# Time, Tracing & Logging

## When to use
- You need timeouts, deadlines, or sleeps
- You want spans for latency analysis or logs for debugging

## Time
```ts
import { Clock, Duration } from "effect"
const now = yield* Clock.currentTimeMillis
yield* Effect.sleep(Duration.seconds(1))
```

## Timeout
```ts
const guarded = yield* Effect.timeout(task, Duration.seconds(2))
```

## Tracing (span wrapper pattern)
```ts
const op = Effect.withSpan("operation")(Effect.succeed(1))
```

## Logging
```ts
yield* Effect.logInfo("message")
yield* Effect.logDebug("debug")
yield* Effect.logError("error")
```

## Real-world snippet: set minimum log level via Layer
```ts
import { Effect, Option, Logger, LogLevel, Layer } from "effect"

export const setMinimumLogLevel = (cliLevel: Option.Option<LogLevel.LogLevel>) =>
  APP_CONFIG["LOG_LEVEL"].pipe(
    Effect.map((envLevel) => Option.zipLeft(cliLevel, envLevel)),
    Effect.map(Option.getOrElse(() => LogLevel.Info)),
    Effect.map((level) => Logger.minimumLogLevel(level)),
    Layer.unwrapEffect
  )
```

## Guidance
- Prefer `Duration` helpers for clarity of units
- Wrap critical sections with spans; attach attributes for context
- Use structured logs and avoid ad-hoc console prints

## Pitfalls
- Mixing ms numbers → use `Duration` consistently
- No timeouts on external calls → risk of hanging operations

## Cross-links
- Errors & Retries for timeouts+races
- Concurrency for coordinated time-based operations

## Local Source Reference

**CRITICAL: Search local Effect source before implementing**

The full Effect source code is available at `docs/effect-source/`. Always search the actual implementation before writing Effect code.

### Key Source Files
- Clock: `docs/effect-source/effect/src/Clock.ts`
- Duration: `docs/effect-source/effect/src/Duration.ts`
- Effect (withSpan, log): `docs/effect-source/effect/src/Effect.ts`
- Logger: `docs/effect-source/effect/src/Logger.ts`
- LogLevel: `docs/effect-source/effect/src/LogLevel.ts`

### Example Searches
```bash
# Find Clock operations
grep -F "currentTimeMillis" docs/effect-source/effect/src/Clock.ts
grep -F "sleep" docs/effect-source/effect/src/Clock.ts

# Study Duration helpers
grep -F "seconds" docs/effect-source/effect/src/Duration.ts
grep -F "millis" docs/effect-source/effect/src/Duration.ts
grep -F "minutes" docs/effect-source/effect/src/Duration.ts

# Find span and logging patterns
grep -F "withSpan" docs/effect-source/effect/src/Effect.ts
grep -F "logInfo" docs/effect-source/effect/src/Effect.ts
grep -F "logError" docs/effect-source/effect/src/Effect.ts

# Look at Logger implementation
grep -F "minimumLogLevel" docs/effect-source/effect/src/Logger.ts
```

### Workflow
1. Identify the time/logging API you need (e.g., Clock, Duration, withSpan)
2. Search `docs/effect-source/effect/src/` for the implementation
3. Study the types and time-based patterns
4. Look at test files for usage examples
5. Write your code based on real implementations

**Real source code > documentation > assumptions**

## References
- Agent Skills overview: https://www.anthropic.com/news/skills
- Skills guide: https://docs.claude.com/en/docs/claude-code/skills

