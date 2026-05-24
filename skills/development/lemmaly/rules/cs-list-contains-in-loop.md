---
id: cs-list-contains-in-loop
title: List.Contains inside LINQ/loop — O(n*m); use HashSet<T>
severity: warning
impact: HIGH
impactDescription: Hot-path or correctness risk at realistic n
language: csharp
tags: csharp, warning, complexity-cuts
---

# List.Contains inside LINQ/loop — O(n*m); use HashSet<T>

`List<T>.Contains` is O(n). Inside LINQ over m items it is O(n·m). `HashSet<T>` is O(1).

## Fix

Convert to HashSet once: `var s = new HashSet<T>(list); s.Contains(x);`

## Incorrect

```csharp
// O(n·m)
var active = users.Where(u => !banned.Contains(u.Id)).ToList();
```

## Correct

```csharp
// O(n+m)
var bannedSet = new HashSet<int>(banned);
var active = users.Where(u => !bannedSet.Contains(u.Id)).ToList();
```

## Escalate to

If this pattern is widespread in the codebase, load **complexity-cuts** for the corrective workflow.
