---
id: rs-clone-in-loop
title: .clone() inside iterator — avoid if a borrow works
severity: info
impact: MEDIUM
impactDescription: Suboptimal; flag when n is large or on a hot path
language: rust
tags: rust, info, complexity-cuts
---

# .clone() inside iterator — avoid if a borrow works

A `.clone()` inside an iterator allocates a fresh copy per element. If a borrow (`&x`) or `Rc::clone` (cheap atomic increment for shared ownership) would do, the deep clone is wasted work.

## Fix

Borrow with &, use Rc/Arc for shared ownership, or move once outside the loop.

## Incorrect

```rust
// Deep clones every element
let names: Vec<String> = users.iter().map(|u| u.name.clone()).collect();
```

## Correct

```rust
// Borrow when possible
let names: Vec<&str> = users.iter().map(|u| u.name.as_str()).collect();

// Cheap reference-counted clone when shared ownership is needed
let shared: Vec<Rc<String>> = users.iter().map(|u| Rc::clone(&u.name)).collect();
```

## Escalate to

If this pattern is widespread in the codebase, load **complexity-cuts** for the corrective workflow.
