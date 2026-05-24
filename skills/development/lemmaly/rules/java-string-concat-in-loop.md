---
id: java-string-concat-in-loop
title: String += inside loop — O(n^2) on immutable String
severity: warning
impact: HIGH
impactDescription: Hot-path or correctness risk at realistic n
language: java
tags: java, warning, complexity-cuts
---

# String += inside loop — O(n^2) on immutable String

Java `String` is immutable. `s += x` allocates a fresh `String` (and an underlying `char[]`) each iteration — O(n²) total work. `StringBuilder` reuses one buffer.

## Fix

Use StringBuilder: `var sb = new StringBuilder(); for (...) sb.append(x); sb.toString();`

## Incorrect

```java
// O(n²)
String s = "";
for (var line : lines) {
  s += line + "\n";
}
```

## Correct

```java
// O(n)
var sb = new StringBuilder(lines.size() * 80);
for (var line : lines) {
  sb.append(line).append('\n');
}
String s = sb.toString();
```

## Escalate to

If this pattern is widespread in the codebase, load **complexity-cuts** for the corrective workflow.
