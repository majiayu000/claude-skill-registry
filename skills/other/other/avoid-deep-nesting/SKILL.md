---
name: avoid-deep-nesting
description: Keep nesting to a maximum of 2-3 levels Use when enforcing code quality standards. Quality category skill.
metadata:
  category: Quality
  priority: high
  is-built-in: true
  session-guardian-id: builtin_avoid_deep_nesting
---

# Avoid Deep Nesting

Keep nesting to a maximum of 2-3 levels. Use early returns (guard clauses) to handle edge cases and errors first, leaving the main logic un-nested. Extract nested blocks into well-named functions. Consider using techniques like map/filter/reduce instead of nested loops. If you can't flatten the nesting, the function is likely doing too much.