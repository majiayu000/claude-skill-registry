---
id: rs-string-push-no-capacity
title: String::new() + push_str in loop — repeated reallocation
severity: info
impact: MEDIUM
impactDescription: Suboptimal; flag when n is large or on a hot path
language: rust
tags: rust, info, complexity-cuts
---

# String::new() + push_str in loop — repeated reallocation

`String::new()` starts at capacity 0. Each `push_str` past capacity reallocates. `with_capacity` or `join` avoids it.

## Fix

Preallocate: `String::with_capacity(n)`, or `parts.join(sep)` for known parts.

## Incorrect

```rust
let mut s = String::new();
for part in parts.iter() {
  s.push_str(part); // reallocates as it grows
}
```

## Correct

```rust
let total: usize = parts.iter().map(|p| p.len()).sum();
let mut s = String::with_capacity(total);
for part in parts.iter() {
  s.push_str(part);
}

// Or, simplest:
let s = parts.join("");
```

## Escalate to

If this pattern is widespread in the codebase, load **complexity-cuts** for the corrective workflow.
