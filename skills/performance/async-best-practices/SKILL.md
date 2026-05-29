---
name: async-best-practices
description: Use Promise Use when optimizing code performance. Performance category skill.
metadata:
  category: Performance
  priority: high
  is-built-in: true
  session-guardian-id: builtin_async_best_practices
---

# Async Best Practices

Use Promise.all() for independent async operations that can run concurrently. Avoid await inside loops when iterations are independent—collect promises and await them together. Handle errors appropriately with try/catch or .catch(). Don't mix callbacks and promises unnecessarily. Consider Promise.allSettled() when you need results even if some promises fail.