---
name: least-privilege
description: "Database accounts should have only required permissions (read-only where writes aren't needed) Use when implementing security best practices. Security category skill."
metadata:
  category: Security
  priority: high
  is-built-in: true
  session-guardian-id: builtin_least_privilege
---

# Least Privilege

Database accounts should have only required permissions (read-only where writes aren't needed). API tokens should be scoped to specific operations. Service accounts should have minimal roles. User permissions should default to restricted and be elevated as needed. File system access should be limited to required directories. Network access should be restricted to necessary endpoints.