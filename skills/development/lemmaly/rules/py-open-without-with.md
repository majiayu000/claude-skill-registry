---
id: py-open-without-with
title: open() without `with` — risk of leaked file descriptors
severity: info
impact: MEDIUM
impactDescription: Suboptimal; flag when n is large or on a hot path
language: python
tags: python, info
---

# open() without `with` — risk of leaked file descriptors

`open()` returns a file object. Without `with`, an exception between open and close leaks the file descriptor. Long-running processes (servers, workers) eventually exhaust the OS limit.

## Fix

Use `with open(path) as f:` to ensure the handle is released.

## Incorrect

```python
f = open(path)
data = f.read()
f.close()  # skipped if read() raises
```

## Correct

```python
with open(path) as f:
    data = f.read()
# f is closed even if read() raises
```
