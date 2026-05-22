---
name: pure-functions
description: Separate pure computation from side effects (I/O, mutations, API calls) Use when enforcing code quality standards. Quality category skill.
metadata:
  category: Quality
  priority: medium
  is-built-in: true
  session-guardian-id: builtin_pure_functions
---

# Pure Functions

Separate pure computation from side effects (I/O, mutations, API calls). Pure functions should not access global state, modify arguments, or depend on external mutable state. Keep side effects at the edges of your system (entry points, I/O boundaries) and push pure logic to the core. This makes unit testing trivial—no mocking required.