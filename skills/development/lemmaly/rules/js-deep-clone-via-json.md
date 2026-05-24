---
id: js-deep-clone-via-json
title: JSON.parse(JSON.stringify(x)) — slow clone; loses Dates/Maps/undefined
severity: warning
impact: HIGH
impactDescription: Hot-path or correctness risk at realistic n
language: javascript
tags: javascript, warning
---

# JSON.parse(JSON.stringify(x)) — slow clone; loses Dates/Maps/undefined

`JSON.parse(JSON.stringify(x))` is slow, allocates twice, and silently loses `Date`, `Map`, `Set`, `undefined`, `BigInt`, `RegExp`, and any non-enumerable property. It is also unsafe on cyclic structures.

## Fix

Use structuredClone(x), or copy only the fields you actually need.

## Incorrect

```ts
const copy = JSON.parse(JSON.stringify(state));
// state.createdAt was a Date — now a string
```

## Correct

```ts
const copy = structuredClone(state); // preserves Date, Map, Set, cycles

// Or, when you only need a few fields:
const copy = { id: state.id, name: state.name };
```
