---
id: js-helper-call-in-iterator
title: get*/find*/fetch* helper called inside iterator — likely N round-trips
severity: warning
impact: HIGH
impactDescription: Hot-path or correctness risk at realistic n
language: javascript
tags: javascript, warning, complexity-cuts
---

# get*/find*/fetch* helper called inside iterator — likely N round-trips

A `get*`/`find*`/`fetch*` helper inside an iterator usually means N independent lookups. If the helper hits a DB or network, this is N+1. If it scans an array, it is O(n × m).

## Fix

Hoist the helper out of the loop and pass a precomputed lookup (Map/Set) into the iterator, or batch with a single bulk query.

## Incorrect

```ts
// N round trips
const enriched = orders.map((o) => ({
  ...o,
  user: getUserById(o.userId),
}));
```

## Correct

```ts
// 1 round trip
const userIds = [...new Set(orders.map((o) => o.userId))];
const users = await db.users.findMany({ where: { id: { in: userIds } } });
const userById = new Map(users.map((u) => [u.id, u]));
const enriched = orders.map((o) => ({ ...o, user: userById.get(o.userId) }));
```

## Escalate to

If this pattern is widespread in the codebase, load **complexity-cuts** for the corrective workflow.
