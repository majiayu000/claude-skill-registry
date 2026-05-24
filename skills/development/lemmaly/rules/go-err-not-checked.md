---
id: go-err-not-checked
title: Error return value discarded — silent failures
severity: warning
impact: HIGH
impactDescription: Hot-path or correctness risk at realistic n
language: go
tags: go, warning, invariant-guard
---

# Error return value discarded — silent failures

Discarding the error return with `_` is silent failure. The function looks like it succeeded; downstream code sees zero values and behaves unpredictably.

## Fix

Handle the error or comment why it is safe to ignore (`_ = err // <reason>`).

## Incorrect

```go
data, _ := os.ReadFile(path)
return parse(data) // parse on empty buffer if file missing
```

## Correct

```go
data, err := os.ReadFile(path)
if err != nil {
  return nil, fmt.Errorf("read %s: %w", path, err)
}
return parse(data), nil
```

## Escalate to

If this pattern is widespread in the codebase, load **invariant-guard** for the corrective workflow.
