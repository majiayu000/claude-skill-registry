---
name: effect-lookup
version: 1.0.0
description: Quick lookup for Effect TypeScript library APIs, patterns, and source code. Use when you need to find Effect functions, understand Effect patterns, or look up implementation details.
---

# Effect Library Lookup

Quick reference for finding and understanding Effect TypeScript library APIs from local source code.

## Source Code Access

Source code is available locally and on GitHub. Check local first, fall back to GitHub if not available.

| Repo           | Local path                                            | GitHub                                       |
| -------------- | ----------------------------------------------------- | -------------------------------------------- |
| Effect         | `opensrc/repos/github.com/effect-ts/effect/`          | https://github.com/effect-ts/effect          |
| EffectPatterns | `opensrc/repos/github.com/PaulJPhilp/EffectPatterns/` | https://github.com/PaulJPhilp/EffectPatterns |

## When to Use This Skill

Use this skill when:

- Looking up Effect function signatures or implementations
- Finding examples of Effect patterns (Effect.gen, Layer, Context, etc.)
- Understanding how Effect modules work internally
- Checking API availability or deprecation status
- Learning Effect idioms from source code

## How to Look Up Effect APIs

### 1. Use the Effect Docs MCP Server (Fastest)

The `effect-docs` MCP server provides indexed documentation:

```
mcp__effect-docs__effect_docs_search: Search for Effect concepts
mcp__effect-docs__get_effect_doc: Get specific documentation by ID
```

### 2. Search the Local Source

For implementation details, search the local source at `opensrc/repos/github.com/effect-ts/effect/`:

```bash
# Find a specific function
grep -r "export const myFunction" opensrc/repos/github.com/effect-ts/effect/packages/effect/src/

# Find usage patterns
grep -rn "Effect.gen" opensrc/repos/github.com/effect-ts/effect/packages/effect/src/

# Find type definitions
grep -rn "interface MyType" opensrc/repos/github.com/effect-ts/effect/packages/effect/src/
```

### 3. Read Source Files Directly

Core modules are at: `opensrc/repos/github.com/effect-ts/effect/packages/effect/src/<Module>.ts`

Example: To understand `Effect.map`, read `opensrc/repos/github.com/effect-ts/effect/packages/effect/src/Effect.ts`

## Quick Reference

| Task              | Reference                |
| ----------------- | ------------------------ |
| Module categories | `references/modules.md`  |
| Common patterns   | `references/patterns.md` |

## Package Structure

```text
opensrc/repos/github.com/effect-ts/effect/
├── packages/
│   ├── effect/               # Core Effect library
│   │   └── src/              # Source files (Effect.ts, Layer.ts, etc.)
│   ├── platform/             # Cross-platform utilities (HTTP, FileSystem)
│   ├── platform-node/        # Node.js platform implementation
│   ├── platform-browser/     # Browser platform implementation
│   ├── cli/                  # CLI building utilities
│   ├── sql/                  # SQL database utilities
│   ├── sql-pg/               # PostgreSQL implementation
│   ├── sql-kysely/           # Kysely integration
│   ├── rpc/                  # Remote procedure calls
│   ├── cluster/              # Distributed computing
│   ├── opentelemetry/        # OpenTelemetry integration
│   ├── experimental/         # Experimental features
│   └── ai/                   # AI integrations (OpenAI, Anthropic, etc.)
```

## Core Modules Quick Lookup

### Effect System

| Module  | File         | Purpose                          |
| ------- | ------------ | -------------------------------- |
| Effect  | `Effect.ts`  | Core effect type and combinators |
| Layer   | `Layer.ts`   | Dependency injection layers      |
| Context | `Context.ts` | Type-safe service context        |
| Scope   | `Scope.ts`   | Resource management              |
| Runtime | `Runtime.ts` | Effect execution                 |

### Data Types

| Module  | File         | Purpose                |
| ------- | ------------ | ---------------------- |
| Option  | `Option.ts`  | Optional values        |
| Either  | `Either.ts`  | Success/failure values |
| Chunk   | `Chunk.ts`   | Immutable arrays       |
| HashMap | `HashMap.ts` | Immutable hash maps    |
| HashSet | `HashSet.ts` | Immutable hash sets    |
| List    | `List.ts`    | Immutable linked lists |

### Concurrency

| Module    | File           | Purpose              |
| --------- | -------------- | -------------------- |
| Fiber     | `Fiber.ts`     | Lightweight threads  |
| Queue     | `Queue.ts`     | Concurrent queues    |
| Ref       | `Ref.ts`       | Mutable references   |
| Semaphore | `Semaphore.ts` | Concurrency limiting |
| PubSub    | `PubSub.ts`    | Publish/subscribe    |

### Schema & Validation

| Module      | File             | Purpose                    |
| ----------- | ---------------- | -------------------------- |
| Schema      | `Schema.ts`      | Data validation & encoding |
| ParseResult | `ParseResult.ts` | Parsing results            |
| Arbitrary   | `Arbitrary.ts`   | Property-based testing     |

### Streaming

| Module  | File         | Purpose                 |
| ------- | ------------ | ----------------------- |
| Stream  | `Stream.ts`  | Effectful streams       |
| Sink    | `Sink.ts`    | Stream consumers        |
| Channel | `Channel.ts` | Bidirectional streaming |

### Scheduling & Time

| Module   | File          | Purpose                |
| -------- | ------------- | ---------------------- |
| Schedule | `Schedule.ts` | Retry/repeat schedules |
| Duration | `Duration.ts` | Time durations         |
| DateTime | `DateTime.ts` | Date/time handling     |
| Clock    | `Clock.ts`    | Time service           |
| Cron     | `Cron.ts`     | Cron expressions       |

### Configuration

| Module         | File                | Purpose                 |
| -------------- | ------------------- | ----------------------- |
| Config         | `Config.ts`         | Type-safe configuration |
| ConfigProvider | `ConfigProvider.ts` | Configuration sources   |

## Common Lookup Patterns

### Find Function Signature

```bash
# In Effect.ts, functions are well-documented with JSDoc
grep -A 20 "export const map" opensrc/repos/github.com/effect-ts/effect/packages/effect/src/Effect.ts
```

### Find Type Definition

```bash
# Look for interface or type alias
grep -n "interface Effect<" opensrc/repos/github.com/effect-ts/effect/packages/effect/src/Effect.ts
```

### Find Examples in Tests

```bash
# Tests often have practical examples
grep -rn "Effect.gen" opensrc/repos/github.com/effect-ts/effect/packages/effect/test/
```

### Check Platform APIs

```bash
# HTTP client/server
ls opensrc/repos/github.com/effect-ts/effect/packages/platform/src/Http*.ts

# FileSystem
cat opensrc/repos/github.com/effect-ts/effect/packages/platform/src/FileSystem.ts
```

## EffectPatterns Knowledge Base

Community-driven patterns and architectural guides at `opensrc/repos/github.com/PaulJPhilp/EffectPatterns/`.

```bash
# Browse pattern categories
ls opensrc/repos/github.com/PaulJPhilp/EffectPatterns/content/

# Search for a specific pattern
grep -rn "Layer" opensrc/repos/github.com/PaulJPhilp/EffectPatterns/content/

# Read docs
ls opensrc/repos/github.com/PaulJPhilp/EffectPatterns/docs/
```

Covers: getting started, core concepts, error management, resource management, concurrency, streams, scheduling, domain modeling, schema, platform, HTTP APIs, data pipelines, testing, and observability.

## External References

- [Effect Website](https://effect.website/) - Official documentation
- [Effect API Reference](https://effect-ts.github.io/effect/) - Full API docs
- [Effect Discord](https://discord.gg/hdt7t7jpvn) - Community support

## Tips for Effective Lookups

1. **Start with MCP search** - Use `effect_docs_search` for conceptual questions
1. **Read JSDoc comments** - Effect source has excellent inline documentation
1. **Check tests for examples** - Test files show real usage patterns
1. **Use module tables above** - Quickly navigate to the right source file
1. **Platform packages** - HTTP, FileSystem, etc. are in `@effect/platform`
1. **EffectPatterns** - Use for architectural patterns and best practices
