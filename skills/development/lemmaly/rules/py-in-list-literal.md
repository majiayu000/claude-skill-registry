---
id: py-in-list-literal
title: Membership against a list literal — O(n) per check; use a set
severity: info
impact: MEDIUM
impactDescription: Suboptimal; flag when n is large or on a hot path
language: python
tags: python, info, complexity-cuts
---

# Membership against a list literal — O(n) per check; use a set

`x in [a, b, c, ...]` is an O(n) linear scan. Inside a loop over m items, this is O(n × m). A `set` (or a literal `{a, b, c}` for membership) is O(1).

## Fix

Hoist to a module-level frozenset({...}).

## Incorrect

```python
# O(n × m)
roles = ["admin", "editor", "owner"]
result = [u for u in users if u.role in roles]
```

## Correct

```python
# O(n + m)
roles = {"admin", "editor", "owner"}
result = [u for u in users if u.role in roles]
```

## Escalate to

If this pattern is widespread in the codebase, load **complexity-cuts** for the corrective workflow.
