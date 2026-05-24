---
name: functional-programming
# IMPORTANT: Keep description on ONE line for Claude Code compatibility
# prettier-ignore
description: Use when writing functional code - covers FP best practices (Lea differs from traditional FP languages)
---

# Functional Programming Best Practices

## Quick Start

```
-- Prefer pure functions and immutable data
let double = (x) -> x * 2
[1, 2, 3] /> map(double) /> filter((x) -> x > 2)
```

## Core Principles

- **Immutability**: Use `let` by default, `maybe` only when mutation is necessary
- **Pure functions**: No side effects, same input always produces same output
- **Composition**: Build complex behavior from simple, composable functions
- **Higher-order functions**: Pass functions as arguments, return functions

## Lea-Specific Warnings

**Lea differs from traditional FP languages:**

- **No currying** - Use placeholders: `5 /> add(3, input)`
- **Pipes prepend** - `x /> fn(a)` becomes `fn(x, a)`
- **Mutable bindings** - `maybe` allows mutation; avoid unless necessary
- **No monads** - Async uses `#async` decorator instead
- **Opt-in types** - Add `:: Type :> ReturnType`, use `#strict` for enforcement

## Notes

- Prefer `let` over `maybe`
- Use pipelines (`/>`) for left-to-right data flow
- Callbacks receive `(element, index)`
