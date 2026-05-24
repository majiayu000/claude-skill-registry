---
id: js-async-in-foreach
title: async passed to .forEach — returned promises are dropped
severity: error
impact: CRITICAL
impactDescription: Will break or scale-fail in production
language: javascript
tags: javascript, error, complexity-cuts
---

# async passed to .forEach — returned promises are dropped

`Array.prototype.forEach` ignores return values. Passing an `async` function returns promises that are dropped — errors are swallowed and the caller continues before the work finishes.

## Fix

Use `for (const x of arr) await fn(x)` or `await Promise.all(arr.map(fn))`.

## Incorrect

```ts
// Promises dropped; errors silently swallowed
items.forEach(async (item) => {
  await save(item);
});
console.log('done'); // logs before any save completes
```

## Correct

```ts
// Sequential, with errors propagated
for (const item of items) {
  await save(item);
}

// Parallel
await Promise.all(items.map((item) => save(item)));
```

## Escalate to

If this pattern is widespread in the codebase, load **complexity-cuts** for the corrective workflow.
