---
name: lazy-evaluation
description: Use lazy evaluation for expensive operations that may not be needed Use when optimizing code performance. Performance category skill.
metadata:
  category: Performance
  priority: medium
  is-built-in: true
  session-guardian-id: builtin_lazy_evaluation
---

# Lazy Evaluation

Use lazy evaluation for expensive operations that may not be needed. Implement lazy loading for resources (images, data, modules). Use generators or iterators for large data processing to avoid loading everything into memory. Consider computed properties that calculate on demand vs. eagerly. Short-circuit evaluation in boolean expressions can skip expensive checks.