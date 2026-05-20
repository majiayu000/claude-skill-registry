---
name: no-magic-numbers
description: Replace magic numbers with named constants that explain their purpose Use when enforcing code quality standards. Quality category skill.
metadata:
  category: Quality
  priority: high
  is-built-in: true
  session-guardian-id: builtin_no_magic_numbers
---

# No Magic Numbers

Replace magic numbers with named constants that explain their purpose. Instead of "if (status === 3)", use "if (status === OrderStatus.SHIPPED)". This applies to strings too—use constants for repeated string literals. The constant name serves as documentation and makes updates easier since the value is defined in one place.