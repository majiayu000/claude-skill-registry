---
name: secure-error-messages
description: Log detailed errors server-side but return generic messages to clients Use when implementing security best practices. Security category skill.
metadata:
  category: Security
  priority: high
  is-built-in: true
  session-guardian-id: builtin_secure_error_messages
---

# Secure Error Messages

Log detailed errors server-side but return generic messages to clients. Never expose stack traces, database errors, or internal paths in API responses. Use consistent error messages for authentication failures (don't reveal whether username or password was wrong). Implement custom error pages that don't expose framework information. Include correlation IDs for support without exposing internals.