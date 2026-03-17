---
name: avoid-null-returns
description: "Instead of returning null, consider: throwing an exception for unexpected missing data, returning... Use when enforcing code quality standards. Quality category skill."
metadata:
  category: Quality
  priority: medium
  is-built-in: true
  session-guardian-id: builtin_avoid_null_returns
---

# Avoid Null Returns

Instead of returning null, consider: throwing an exception for unexpected missing data, returning an empty collection for list operations, using the Null Object pattern, or using Optional/Maybe types. When null is truly valid, document it clearly and consider making it explicit in the type system (e.g., User | null in TypeScript).