---
id: go-loop-var-capture
title: Loop variable captured by goroutine — pre-1.22 races on the last value
severity: error
impact: CRITICAL
impactDescription: Will break or scale-fail in production
language: go
tags: go, error, invariant-guard
---

# Loop variable captured by goroutine — pre-1.22 races on the last value

Before Go 1.22, the loop variable in `for ... := range` was reused across iterations. Goroutines that closed over it all read the *same* (final) value. Go 1.22+ fixes this at the language level, but the pattern still appears in libraries that target older versions.

## Fix

Pin the variable inside the loop: `i := i` before `go func() { use(i) }()`, or pass as argument: `go func(i int) { ... }(i)`. (Fixed automatically in Go 1.22+.)

## Incorrect

```go
// Pre-1.22: all goroutines print the last item
for _, v := range items {
  go func() {
    fmt.Println(v)
  }()
}
```

## Correct

```go
// Pin the variable explicitly
for _, v := range items {
  v := v
  go func() { fmt.Println(v) }()
}

// Or pass as a parameter
for _, v := range items {
  go func(v string) { fmt.Println(v) }(v)
}
```

## Escalate to

If this pattern is widespread in the codebase, load **invariant-guard** for the corrective workflow.
