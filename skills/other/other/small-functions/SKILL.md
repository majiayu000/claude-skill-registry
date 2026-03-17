---
name: small-functions
description: Keep functions short—ideally under 20 lines Use when enforcing code quality standards. Quality category skill.
metadata:
  category: Quality
  priority: high
  is-built-in: true
  session-guardian-id: builtin_small_functions
---

# Small Functions

Keep functions short—ideally under 20 lines. Each function should perform a single, well-defined task. If a function has multiple sections doing different things, extract them into separate functions with descriptive names. Functions should read like a narrative, with each step calling lower-level functions that handle the details.