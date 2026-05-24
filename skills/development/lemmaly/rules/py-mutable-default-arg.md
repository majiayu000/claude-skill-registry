---
id: py-mutable-default-arg
title: Mutable default argument — shared across calls
severity: error
impact: CRITICAL
impactDescription: Will break or scale-fail in production
language: python
tags: python, error, invariant-guard
---

# Mutable default argument — shared across calls

Python evaluates default arguments once, at function definition. A mutable default (list, dict, set) is **shared across every call** — calls accumulate state from previous calls.

## Fix

Default to None; create inside: `def f(x=None): x = x or []`.

## Incorrect

```python
def collect(item, bucket=[]):  # shared across all calls!
    bucket.append(item)
    return bucket
```

## Correct

```python
def collect(item, bucket=None):
    if bucket is None:
        bucket = []
    bucket.append(item)
    return bucket
```

## Escalate to

If this pattern is widespread in the codebase, load **invariant-guard** for the corrective workflow.
