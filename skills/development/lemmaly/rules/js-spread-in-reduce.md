---
id: js-spread-in-reduce
title: Object spread inside reduce — O(n^2)
severity: warning
impact: HIGH
impactDescription: Hot-path or correctness risk at realistic n
language: javascript
tags: javascript, warning, complexity-cuts
---

# Object spread inside reduce — O(n^2)

Object-spread in a reducer copies the accumulator on every iteration — O(n²) work and O(n²) allocation. The result is the same as mutating once.

## Fix

Mutate the accumulator (`acc[k] = v; return acc`) or use Object.fromEntries(arr.map(...)).

## Incorrect

```ts
// O(n²)
const byId = items.reduce((acc, x) => ({ ...acc, [x.id]: x }), {});
```

## Correct

```ts
// O(n)
const byId = Object.fromEntries(items.map((x) => [x.id, x]));

// Or mutate the accumulator
const byId = items.reduce((acc, x) => { acc[x.id] = x; return acc; }, {});
```

## Escalate to

If this pattern is widespread in the codebase, load **complexity-cuts** for the corrective workflow.
