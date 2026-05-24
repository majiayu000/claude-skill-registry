---
id: rs-unwrap-in-prod
title: .unwrap() / .expect() panics on None/Err — surface the error
severity: warning
impact: HIGH
impactDescription: Hot-path or correctness risk at realistic n
language: rust
tags: rust, warning, invariant-guard
---

# .unwrap() / .expect() panics on None/Err — surface the error

`.unwrap()` and `.expect()` panic on `None`/`Err`. In production code they crash the process and lose the structured error. Rust gives you `?`, `match`, and `ok_or` to surface the error to the caller.

## Fix

Use `?`, `match`, `unwrap_or`, `unwrap_or_else`, or `ok_or(...)?`. Reserve unwrap for tests and provably infallible paths.

## Incorrect

```rust
let value = map.get(&key).unwrap(); // panics if key missing
```

## Correct

```rust
let value = map.get(&key).ok_or(Error::MissingKey)?;

// Or, when None has a meaningful default:
let value = map.get(&key).copied().unwrap_or_default();
```

## Escalate to

If this pattern is widespread in the codebase, load **invariant-guard** for the corrective workflow.
