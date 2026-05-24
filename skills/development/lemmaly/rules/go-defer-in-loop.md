---
id: go-defer-in-loop
title: defer inside loop — defers accumulate until function returns
severity: warning
impact: HIGH
impactDescription: Hot-path or correctness risk at realistic n
language: go
tags: go, warning
---

# defer inside loop — defers accumulate until function returns

`defer` fires when the enclosing *function* returns, not when the loop body ends. Deferring inside a loop over N files holds N open handles until the function exits — easy way to exhaust file descriptors.

## Fix

Wrap the body in a function so each iteration's defer fires at iteration end, or close resources explicitly.

## Incorrect

```go
for _, f := range files {
  fp, _ := os.Open(f)
  defer fp.Close() // accumulates; nothing closes until the outer function returns
  process(fp)
}
```

## Correct

```go
for _, f := range files {
  func() {
    fp, _ := os.Open(f)
    defer fp.Close() // closes at end of this iteration
    process(fp)
  }()
}
```
