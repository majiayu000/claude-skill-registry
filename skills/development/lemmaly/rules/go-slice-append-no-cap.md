---
id: go-slice-append-no-cap
title: append in loop without preallocated capacity — repeated reallocation
severity: info
impact: MEDIUM
impactDescription: Suboptimal; flag when n is large or on a hot path
language: go
tags: go, info, complexity-cuts
---

# append in loop without preallocated capacity — repeated reallocation

A slice grown by repeated `append` reallocates and copies its backing array each time it crosses a capacity boundary. Preallocating with `make([]T, 0, n)` does one allocation total.

## Fix

Preallocate: `out := make([]T, 0, len(in))` then `append`.

## Incorrect

```go
var out []int
for _, x := range in {
  out = append(out, x*2) // grows; reallocates log(n) times
}
```

## Correct

```go
out := make([]int, 0, len(in))
for _, x := range in {
  out = append(out, x*2)
}
```

## Escalate to

If this pattern is widespread in the codebase, load **complexity-cuts** for the corrective workflow.
