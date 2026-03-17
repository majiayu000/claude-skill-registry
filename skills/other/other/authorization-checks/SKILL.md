---
name: authorization-checks
description: Check authorization at every access point, not just the UI layer Use when implementing security best practices. Security category skill.
metadata:
  category: Security
  priority: high
  is-built-in: true
  session-guardian-id: builtin_authorization_checks
---

# Authorization Checks

Check authorization at every access point, not just the UI layer. Verify the user has permission for the specific resource being accessed (not just the resource type). Implement authorization consistently—use middleware, decorators, or centralized checks. Apply principle of least privilege. Log authorization failures. Test authorization boundaries explicitly in your test suite.