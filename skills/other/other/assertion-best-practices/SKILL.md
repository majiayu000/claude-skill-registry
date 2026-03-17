---
name: assertion-best-practices
description: Use specific assertions (toBeNull, toContain, toHaveLength) over generic ones (toBe, toBeTruthy) Use when writing and organizing tests. Testing category skill.
metadata:
  category: Testing
  priority: medium
  is-built-in: true
  session-guardian-id: builtin_assertion_best_practices
---

# Assertion Best Practices

Use specific assertions (toBeNull, toContain, toHaveLength) over generic ones (toBe, toBeTruthy). Test one concept per assertion group. Include custom failure messages when the default isn't clear. Avoid asserting implementation details—test observable behavior. Prefer deep equality for objects. Assert negative cases too (doesn't contain, not called).