---
name: consistent-async-patterns
description: Prefer async/await over Use when maintaining consistent code style. Style category skill.
metadata:
  category: Style
  priority: high
  is-built-in: true
  session-guardian-id: builtin_consistent_async_patterns
---

# Consistent Async Patterns

Prefer async/await over .then() chains for readability. Don't mix callbacks with promises unless interfacing with legacy APIs. Use promisify for callback-based APIs. Keep async functions async—don't return plain values then. Handle errors with try/catch in async functions. Mark functions as async only when they use await or return promises.