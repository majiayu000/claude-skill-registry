---
id: cpp-map-double-lookup
title: map.count(k) then map[k] — two lookups; use find()
severity: info
impact: MEDIUM
impactDescription: Suboptimal; flag when n is large or on a hot path
language: cpp
tags: cpp, info, complexity-cuts
---

# map.count(k) then map[k] — two lookups; use find()

`m.count(k)` then `m[k]` does two hash lookups (and for `std::map`, two binary searches). `find` returns an iterator that gives both presence and value in one lookup.

## Fix

Use `auto it = m.find(k); if (it != m.end()) use(it->second);` — one lookup.

## Incorrect

```cpp
if (m.count(k)) {
  use(m[k]); // second lookup
}
```

## Correct

```cpp
auto it = m.find(k);
if (it != m.end()) {
  use(it->second);
}
```

## Escalate to

If this pattern is widespread in the codebase, load **complexity-cuts** for the corrective workflow.
