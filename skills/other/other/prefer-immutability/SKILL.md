---
name: prefer-immutability
description: Prefer const over let and readonly properties where possible Use when enforcing code quality standards. Quality category skill.
metadata:
  category: Quality
  priority: medium
  is-built-in: true
  session-guardian-id: builtin_prefer_immutability
---

# Prefer Immutability

Prefer const over let and readonly properties where possible. Use immutable update patterns: spread operators for objects/arrays, map/filter/reduce instead of mutating loops. When working with shared state, consider immutable data structures. Mutations should be intentional and localized, not scattered throughout the codebase.