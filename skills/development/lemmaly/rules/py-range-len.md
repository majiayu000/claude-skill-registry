---
id: py-range-len
title: range(len(x)) — un-Pythonic; use enumerate(x)
severity: info
impact: MEDIUM
impactDescription: Suboptimal; flag when n is large or on a hot path
language: python
tags: python, info
---

# range(len(x)) — un-Pythonic; use enumerate(x)

`for i in range(len(xs))` then indexing `xs[i]` is un-Pythonic, slower, and forces you to think about indices when you usually want the items. `enumerate` is idiomatic and faster.

## Fix

Use `for i, item in enumerate(x):` when you need the index too.

## Incorrect

```python
for i in range(len(xs)):
    process(xs[i])
```

## Correct

```python
for x in xs:
    process(x)

# When you actually need the index
for i, x in enumerate(xs):
    process(i, x)
```
