---
id: go-string-concat-in-loop
title: string += inside loop — O(n^2); use strings.Builder
severity: warning
impact: HIGH
impactDescription: Hot-path or correctness risk at realistic n
language: go
tags: go, warning, complexity-cuts
---

# string += inside loop — O(n^2); use strings.Builder

Go strings are immutable. `s += x` allocates each iteration — O(n²). `strings.Builder` reuses one backing array.

## Fix

Use strings.Builder: `var sb strings.Builder; for ... { sb.WriteString(x) }; sb.String()`.

## Incorrect

```go
// O(n²)
var s string
for _, line := range lines {
  s += line + "\n"
}
```

## Correct

```go
// O(n)
var sb strings.Builder
sb.Grow(len(lines) * 80)
for _, line := range lines {
  sb.WriteString(line)
  sb.WriteByte('\n')
}
s := sb.String()
```

## Escalate to

If this pattern is widespread in the codebase, load **complexity-cuts** for the corrective workflow.
