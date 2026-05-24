---
id: java-arraylist-remove-in-for-i
title: list.remove(i) inside for-i — index shifts; ConcurrentModification risk
severity: error
impact: CRITICAL
impactDescription: Will break or scale-fail in production
language: java
tags: java, error, invariant-guard
---

# list.remove(i) inside for-i — index shifts; ConcurrentModification risk

Removing from an `ArrayList` inside a `for (int i = 0; i < list.size(); i++)` shifts indices and skips elements — and on a `Collections.synchronizedList` or in concurrent code, it throws `ConcurrentModificationException`.

## Fix

Iterate backwards, use Iterator.remove(), or collect indexes and remove in one removeIf().

## Incorrect

```java
for (int i = 0; i < list.size(); i++) {
  if (shouldRemove(list.get(i))) {
    list.remove(i); // shifts everything; next element is skipped
  }
}
```

## Correct

```java
// Idiomatic and correct
list.removeIf(this::shouldRemove);

// Or, with an explicit iterator:
var it = list.iterator();
while (it.hasNext()) {
  if (shouldRemove(it.next())) it.remove();
}
```

## Escalate to

If this pattern is widespread in the codebase, load **invariant-guard** for the corrective workflow.
