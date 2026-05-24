---
id: rs-vec-push-no-capacity
title: Vec::new() + push in loop — repeated reallocation
severity: info
impact: MEDIUM
impactDescription: Suboptimal; flag when n is large or on a hot path
language: rust
tags: rust, info, complexity-cuts
---

# Vec::new() + push in loop — repeated reallocation

`Vec::new()` starts with capacity 0; each `push` past the current capacity reallocates and copies. Preallocating with `Vec::with_capacity(n)` does one allocation.

## Fix

Preallocate: `Vec::with_capacity(n)`, or use `.collect::<Vec<_>>()` over an iterator that has a size hint.

## Incorrect

```rust
let mut out = Vec::new();
for x in input.iter() {
  out.push(transform(x)); // grows; reallocates log(n) times
}
```

## Correct

```rust
let mut out = Vec::with_capacity(input.len());
for x in input.iter() {
  out.push(transform(x));
}

// Or, when transform is pure:
let out: Vec<_> = input.iter().map(transform).collect();
```

## Escalate to

If this pattern is widespread in the codebase, load **complexity-cuts** for the corrective workflow.
