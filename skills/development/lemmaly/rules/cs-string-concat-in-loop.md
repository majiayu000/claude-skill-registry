---
id: cs-string-concat-in-loop
title: string += inside loop — O(n^2) on immutable string
severity: warning
impact: HIGH
impactDescription: Hot-path or correctness risk at realistic n
language: csharp
tags: csharp, warning, complexity-cuts
---

# string += inside loop — O(n^2) on immutable string

C# `string` is immutable. `s += x` allocates a new string each iteration — O(n²). `StringBuilder` reuses one buffer; or use `string.Concat` / `string.Join` for known parts.

## Fix

Use StringBuilder: `var sb = new StringBuilder(); foreach (...) sb.Append(x); sb.ToString();`

## Incorrect

```csharp
// O(n²)
string s = "";
foreach (var line in lines) {
  s += line + "\n";
}
```

## Correct

```csharp
// O(n)
var sb = new StringBuilder(lines.Count * 80);
foreach (var line in lines) {
  sb.Append(line).Append('\n');
}
var s = sb.ToString();
```

## Escalate to

If this pattern is widespread in the codebase, load **complexity-cuts** for the corrective workflow.
