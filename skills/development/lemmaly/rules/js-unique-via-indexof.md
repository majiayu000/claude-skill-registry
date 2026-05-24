---
id: js-unique-via-indexof
title: Unique-by-indexOf — O(n^2) dedupe; use `Array.from(new Set(arr))`
severity: warning
impact: HIGH
impactDescription: Hot-path or correctness risk at realistic n
language: javascript
tags: javascript, warning, complexity-cuts
---

# Unique-by-indexOf — O(n^2) dedupe; use `Array.from(new Set(arr))`

`.filter((x, i, a) => a.indexOf(x) === i)` is the textbook O(n²) dedupe. A `Set` does it in O(n).

## Fix

Use `Array.from(new Set(arr))`, or build a Set inline. O(n) instead of O(n^2).

## Incorrect

```ts
// O(n²)
const unique = arr.filter((x, i, a) => a.indexOf(x) === i);
```

## Correct

```ts
// O(n)
const unique = Array.from(new Set(arr));
```

## Escalate to

If this pattern is widespread in the codebase, load **complexity-cuts** for the corrective workflow.
