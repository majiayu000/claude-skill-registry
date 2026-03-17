---
name: explicit-returns
description: In TypeScript, explicitly type return values for public functions Use when maintaining consistent code style. Style category skill.
metadata:
  category: Style
  priority: medium
  is-built-in: true
  session-guardian-id: builtin_explicit_returns
---

# Explicit Returns

In TypeScript, explicitly type return values for public functions. Avoid returning undefined implicitly—return null explicitly or use void functions. In arrow functions, be intentional about implicit returns (=> value) vs. explicit (=> { return value; }). Explicit returns make intent clear and catch accidental returns.