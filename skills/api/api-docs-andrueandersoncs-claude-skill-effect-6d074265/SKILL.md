---
name: API Documentation Lookup
description: This skill should be used when the user asks to "look up Effect API", "check the Effect docs", "find Effect function signature", "what does Effect.X do", "how to use Effect.X", "Effect API reference", "fetch Effect documentation", or needs to look up specific function signatures, parameters, or usage examples from the official Effect-TS API documentation.
version: 1.0.0
---

# Effect-TS API Documentation Lookup

## Overview

Use WebFetch to retrieve API documentation directly from the official Effect-TS documentation site at `https://effect-ts.github.io/effect/`.

## URL Patterns

### Core Effect Modules

For modules in the main `effect` package:

```
https://effect-ts.github.io/effect/effect/{Module}.ts.html
```

**Common modules:**
| Module | URL |
|--------|-----|
| Effect | `https://effect-ts.github.io/effect/effect/Effect.ts.html` |
| Schema | `https://effect-ts.github.io/effect/effect/Schema.ts.html` |
| Stream | `https://effect-ts.github.io/effect/effect/Stream.ts.html` |
| Layer | `https://effect-ts.github.io/effect/effect/Layer.ts.html` |
| Context | `https://effect-ts.github.io/effect/effect/Context.ts.html` |
| Schedule | `https://effect-ts.github.io/effect/effect/Schedule.ts.html` |
| Fiber | `https://effect-ts.github.io/effect/effect/Fiber.ts.html` |
| Queue | `https://effect-ts.github.io/effect/effect/Queue.ts.html` |
| Ref | `https://effect-ts.github.io/effect/effect/Ref.ts.html` |
| Scope | `https://effect-ts.github.io/effect/effect/Scope.ts.html` |
| Option | `https://effect-ts.github.io/effect/effect/Option.ts.html` |
| Either | `https://effect-ts.github.io/effect/effect/Either.ts.html` |
| Chunk | `https://effect-ts.github.io/effect/effect/Chunk.ts.html` |
| HashMap | `https://effect-ts.github.io/effect/effect/HashMap.ts.html` |
| HashSet | `https://effect-ts.github.io/effect/effect/HashSet.ts.html` |
| Duration | `https://effect-ts.github.io/effect/effect/Duration.ts.html` |
| Config | `https://effect-ts.github.io/effect/effect/Config.ts.html` |
| ConfigProvider | `https://effect-ts.github.io/effect/effect/ConfigProvider.ts.html` |
| Match | `https://effect-ts.github.io/effect/effect/Match.ts.html` |
| Data | `https://effect-ts.github.io/effect/effect/Data.ts.html` |
| Cause | `https://effect-ts.github.io/effect/effect/Cause.ts.html` |
| Exit | `https://effect-ts.github.io/effect/effect/Exit.ts.html` |
| Random | `https://effect-ts.github.io/effect/effect/Random.ts.html` |
| Clock | `https://effect-ts.github.io/effect/effect/Clock.ts.html` |
| Tracer | `https://effect-ts.github.io/effect/effect/Tracer.ts.html` |
| Metric | `https://effect-ts.github.io/effect/effect/Metric.ts.html` |
| Logger | `https://effect-ts.github.io/effect/effect/Logger.ts.html` |
| Sink | `https://effect-ts.github.io/effect/effect/Sink.ts.html` |
| PubSub | `https://effect-ts.github.io/effect/effect/PubSub.ts.html` |
| Deferred | `https://effect-ts.github.io/effect/effect/Deferred.ts.html` |
| Semaphore | `https://effect-ts.github.io/effect/effect/Semaphore.ts.html` |
| Request | `https://effect-ts.github.io/effect/effect/Request.ts.html` |
| RequestResolver | `https://effect-ts.github.io/effect/effect/RequestResolver.ts.html` |
| Cache | `https://effect-ts.github.io/effect/effect/Cache.ts.html` |
| TestClock | `https://effect-ts.github.io/effect/effect/TestClock.ts.html` |
| Runtime | `https://effect-ts.github.io/effect/effect/Runtime.ts.html` |
| ManagedRuntime | `https://effect-ts.github.io/effect/effect/ManagedRuntime.ts.html` |

### Scoped Packages

For `@effect/*` packages:

```
https://effect-ts.github.io/effect/{package-name}/{Module}.ts.html
```

**Examples:**
| Package | Module | URL |
|---------|--------|-----|
| @effect/platform | HttpClient | `https://effect-ts.github.io/effect/platform/HttpClient.ts.html` |
| @effect/platform | FileSystem | `https://effect-ts.github.io/effect/platform/FileSystem.ts.html` |
| @effect/platform | KeyValueStore | `https://effect-ts.github.io/effect/platform/KeyValueStore.ts.html` |
| @effect/cli | Command | `https://effect-ts.github.io/effect/cli/Command.ts.html` |
| @effect/sql | SqlClient | `https://effect-ts.github.io/effect/sql/SqlClient.ts.html` |

## How to Look Up Documentation

### Step 1: Identify the Module

Determine which module contains the API:
- `Effect.map` → Effect module
- `Schema.Struct` → Schema module
- `Stream.fromIterable` → Stream module
- `Layer.provide` → Layer module

### Step 2: Construct the URL

Use the URL pattern for the identified module:

```typescript
// For Effect.retry
const url = "https://effect-ts.github.io/effect/effect/Effect.ts.html"

// For Schema.transform
const url = "https://effect-ts.github.io/effect/effect/Schema.ts.html"
```

### Step 3: Fetch with Targeted Prompt

Use WebFetch with a specific prompt to extract the relevant information:

```
WebFetch(
  url: "https://effect-ts.github.io/effect/effect/Effect.ts.html",
  prompt: "Find the documentation for Effect.retry. Include the function signature, description, parameters, and any usage examples."
)
```

## Example Queries

### Looking up a specific function

**User asks:** "What are the parameters for Effect.retry?"

**Action:**
```
WebFetch(
  url: "https://effect-ts.github.io/effect/effect/Effect.ts.html",
  prompt: "Find documentation for the retry function. Include its complete type signature, all parameters and options, and usage examples."
)
```

### Looking up a type/interface

**User asks:** "What fields does Schedule have?"

**Action:**
```
WebFetch(
  url: "https://effect-ts.github.io/effect/effect/Schedule.ts.html",
  prompt: "Describe the Schedule type and its main combinators. List common schedule functions like exponential, spaced, recurs, etc."
)
```

### Looking up a module overview

**User asks:** "What functions are available in the Stream module?"

**Action:**
```
WebFetch(
  url: "https://effect-ts.github.io/effect/effect/Stream.ts.html",
  prompt: "List the main categories of functions in this module with brief descriptions of each category."
)
```

### Looking up related functions

**User asks:** "What are all the catch* functions in Effect?"

**Action:**
```
WebFetch(
  url: "https://effect-ts.github.io/effect/effect/Effect.ts.html",
  prompt: "Find all error handling functions that start with 'catch'. Include catchAll, catchTag, catchTags, catchSome, etc. with their signatures and purposes."
)
```

## Prompt Patterns

Use these prompt patterns for effective documentation extraction:

### For function signatures:
```
"Find the complete type signature for {functionName}. Include all overloads if they exist."
```

### For usage examples:
```
"Find documentation and code examples for {functionName}. Focus on practical usage patterns."
```

### For understanding parameters:
```
"Explain the parameters and options for {functionName}. What does each parameter do?"
```

### For finding related functions:
```
"List all functions related to {topic} in this module. Include brief descriptions."
```

### For module overview:
```
"Provide an overview of this module. What are the main categories of functions and types?"
```

## Tips

1. **Be specific in prompts** - Ask for exactly what you need (signature, examples, parameters)
2. **Use the right module** - Effect functions are in Effect.ts, Schema functions in Schema.ts, etc.
3. **Check related functions** - The docs include "See also" links to related functions
4. **Look for examples** - Most functions include practical code examples with expected output
5. **Note version info** - Functions show "Since v2.0.0" or similar version information

## Documentation Site Index

The main documentation index is at:
```
https://effect-ts.github.io/effect/
```

Use this to discover available packages and modules if unsure which module contains a specific API.

## Best Practices

1. **Start with the right module** - Identify which module contains the API before fetching
2. **Use targeted prompts** - Ask for specific information (signature, examples, parameters)
3. **Check for overloads** - Many Effect functions have multiple signatures
4. **Look for "Since" annotations** - Verify the API is available in your Effect version

## Additional Resources

For comprehensive Effect documentation beyond API signatures, consult `${CLAUDE_PLUGIN_ROOT}/references/llms-full.txt` which contains tutorials, guides, and in-depth explanations.
