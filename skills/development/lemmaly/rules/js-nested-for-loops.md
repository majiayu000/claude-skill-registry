---
id: js-nested-for-loops
title: Nested for-loops — O(n*m); consider hashing one side
severity: info
impact: MEDIUM
impactDescription: Suboptimal; flag when n is large or on a hot path
language: javascript
tags: javascript, info, complexity-cuts
---

# Nested for-loops — O(n*m); consider hashing one side

Two `for` loops that check membership between arrays are O(n × m). Hashing one side into a `Set` makes it O(n + m).

## Fix

If looking up between the two arrays, put one into a Set/Map first → O(n+m).

## Incorrect

```ts
// O(n × m)
const matches = [];
for (const a of left) {
  for (const b of right) {
    if (a.id === b.id) matches.push([a, b]);
  }
}
```

## Correct

```ts
// O(n + m)
const rightById = new Map(right.map((b) => [b.id, b]));
const matches = [];
for (const a of left) {
  const b = rightById.get(a.id);
  if (b) matches.push([a, b]);
}
```

## Escalate to

If this pattern is widespread in the codebase, load **complexity-cuts** for the corrective workflow.
