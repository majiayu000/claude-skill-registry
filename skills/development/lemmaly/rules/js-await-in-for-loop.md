---
id: js-await-in-for-loop
title: await inside for-loop — likely N+1 / serialized I/O
severity: error
impact: CRITICAL
impactDescription: Will break or scale-fail in production
language: javascript
tags: javascript, error, complexity-cuts
---

# await inside for-loop — likely N+1 / serialized I/O

Awaiting inside a `for` over independent items serializes wall-clock work into O(n × latency). For network or DB calls this is the N+1 problem.

## Fix

Collect promises into an array and use Promise.all(...), or batch with a bulk query (WHERE id IN (...)).

## Incorrect

```ts
// Wall-clock: O(n × latency)
for (const id of ids) {
  const user = await db.users.findById(id);
  results.push(user);
}
```

## Correct

```ts
// Wall-clock: O(latency); one bulk query
const users = await db.users.findMany({ where: { id: { in: ids } } });

// Or, if calls are truly independent:
const results = await Promise.all(ids.map(id => db.users.findById(id)));
```

## Escalate to

If this pattern is widespread in the codebase, load **complexity-cuts** for the corrective workflow.
