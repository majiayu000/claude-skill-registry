---
name: avoid-long-parameter-lists
description: "If a function requires more than 3-4 parameters, consider: grouping related parameters into an ob... Use when enforcing code quality standards. Quality category skill."
metadata:
  category: Quality
  priority: medium
  is-built-in: true
  session-guardian-id: builtin_avoid_long_params
---

# Avoid Long Parameter Lists

If a function requires more than 3-4 parameters, consider: grouping related parameters into an object or struct, using the Builder pattern for complex object construction, or questioning if the function is doing too much. Named parameters or options objects improve readability and allow for future extension without breaking changes.