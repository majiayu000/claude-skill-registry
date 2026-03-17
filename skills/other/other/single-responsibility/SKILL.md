---
name: single-responsibility
description: Each function should do exactly one thing and do it well Use when enforcing code quality standards. Quality category skill.
metadata:
  category: Quality
  priority: high
  is-built-in: true
  session-guardian-id: builtin_single_responsibility
---

# Single Responsibility

Each function should do exactly one thing and do it well. Classes should have a single, focused purpose. If a function name requires "and" or "or" to describe what it does, split it. When a class handles multiple concerns (e.g., data access AND business logic AND formatting), separate these into distinct classes.