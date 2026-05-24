---
id: py-bare-except
title: Bare except — hides timeouts, OOM, KeyboardInterrupt
severity: info
impact: MEDIUM
impactDescription: Suboptimal; flag when n is large or on a hot path
language: python
tags: python, info, invariant-guard
---

# Bare except — hides timeouts, OOM, KeyboardInterrupt

Bare `except:` catches `SystemExit`, `KeyboardInterrupt`, `MemoryError`, and `GeneratorExit` — things you almost never want to swallow. It hides timeouts, OOM, and Ctrl-C.

## Fix

Catch specific exceptions: `except (TimeoutError, ConnectionError):`.

## Incorrect

```python
try:
    do_work()
except:
    log("failed")  # also swallows Ctrl-C, OOM, timeouts
```

## Correct

```python
try:
    do_work()
except Exception as e:  # excludes SystemExit, KeyboardInterrupt
    log(f"failed: {e}")
```

## Escalate to

If this pattern is widespread in the codebase, load **invariant-guard** for the corrective workflow.
