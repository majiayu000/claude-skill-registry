---
id: py-string-concat-in-loop
title: String += inside loop — O(n^2)
severity: warning
impact: HIGH
impactDescription: Hot-path or correctness risk at realistic n
language: python
tags: python, warning, complexity-cuts
---

# String += inside loop — O(n^2)

Python strings are immutable. `s += x` in a loop allocates and copies the whole `s` each iteration — O(n²) total work. A list join is O(n).

## Fix

Append to a list, then ''.join(list). Or use io.StringIO.

## Incorrect

```python
# O(n²)
s = ""
for line in lines:
    s += line + "\n"
```

## Correct

```python
# O(n)
s = "\n".join(lines) + "\n"

# Or, for incremental building:
parts = []
for line in lines:
    parts.append(line)
s = "\n".join(parts)
```

## Escalate to

If this pattern is widespread in the codebase, load **complexity-cuts** for the corrective workflow.
