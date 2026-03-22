---
name: fp-types-ref
description: Quick reference for fp-ts types. Use when user asks which type to use,
  needs Option/Either/Task decision help, or wants fp-ts imports.
version: 1.0.0
tags:
- fp-ts
- typescript
- quick-reference
- option
- either
- task
risk: safe
source: community
license: MIT
---

# fp-ts Quick Reference

## Which Type Should I Use?

```
Is the operation async?
├─ NO: Does it involve errors?
│   ├─ YES → Either<Error, Value>
│   └─ NO: Might value be missing?
│       ├─ YES → Option<Value>
│       └─ NO → Just use the value
└─ YES: Does it involve errors?
    ├─ YES → TaskEither<Error, Value>
    └─ NO: Might value be missing?
        ├─ YES → TaskOption<Value>
        └─ NO → Task<Value>
```

## Common Imports

```typescript
// Core
import { pipe, flow } from 'fp-ts/function'

// Types
import * as O from 'fp-ts/Option'      // Maybe exists
import * as E from 'fp-ts/Either'      // Success or failure
import * as TE from 'fp-ts/TaskEither' // Async + failure
import * as T from 'fp-ts/Task'        // Async (no failure)
import * as A from 'fp-ts/Array'       // Array utilities
```

## One-Line Patterns

| Need | Code |
|------|------|
| Wrap nullable | `O.fromNullable(value)` |
| Default value | `O.getOrElse(() => default)` |
| Transform if exists | `O.map(fn)` |
| Chain optionals | `O.flatMap(fn)` |
| Wrap try/catch | `E.tryCatch(() => risky(), toError)` |
| Wrap async | `TE.tryCatch(() => fetch(url), toError)` |
| Run pipe | `pipe(value, fn1, fn2, fn3)` |

## Pattern Match

```typescript
// Option
pipe(maybe, O.match(
  () => 'nothing',
  (val) => `got ${val}`
))

// Either
pipe(result, E.match(
  (err) => `error: ${err}`,
  (val) => `success: ${val}`
))
```

## When to Use
- Use this skill when you need for functional programming or specific domain tasks.
