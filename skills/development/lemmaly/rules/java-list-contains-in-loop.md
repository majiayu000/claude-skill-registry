---
id: java-list-contains-in-loop
title: List.contains inside iterator — O(n*m); use HashSet
severity: warning
impact: HIGH
impactDescription: Hot-path or correctness risk at realistic n
language: java
tags: java, warning, complexity-cuts
---

# List.contains inside iterator — O(n*m); use HashSet

`List.contains` is O(n). Used inside a stream/iterator over m items it is O(n·m). A `HashSet` lookup is O(1).

## Fix

Build a HashSet outside: `Set<T> s = new HashSet<>(list); s.contains(x);`

## Incorrect

```java
// O(n·m)
var active = users.stream()
    .filter(u -> !banned.contains(u.id))
    .toList();
```

## Correct

```java
// O(n+m)
var bannedSet = new HashSet<>(banned);
var active = users.stream()
    .filter(u -> !bannedSet.contains(u.id))
    .toList();
```

## Escalate to

If this pattern is widespread in the codebase, load **complexity-cuts** for the corrective workflow.
