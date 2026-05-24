---
id: js-includes-in-iterator
title: Array.includes inside .map/.filter/.forEach — O(n*m); use a Set
severity: info
impact: MEDIUM
impactDescription: Suboptimal; flag when n is large or on a hot path
language: javascript
tags: javascript, info, complexity-cuts
---

# Array.includes inside .map/.filter/.forEach — O(n*m); use a Set

`.includes` on an array is O(n). Calling it inside `.map`/`.filter`/`.forEach` over m items is O(n × m). A `Set` lookup is O(1).

## Fix

Build a Set once outside the iterator, then `set.has(x)` inside.

## Incorrect

```ts
// O(n × m)
const allowed = ['admin', 'editor', 'owner'];
const result = users.filter((u) => allowed.includes(u.role));
```

## Correct

```ts
// O(n + m)
const allowed = new Set(['admin', 'editor', 'owner']);
const result = users.filter((u) => allowed.has(u.role));
```

## Escalate to

If this pattern is widespread in the codebase, load **complexity-cuts** for the corrective workflow.
