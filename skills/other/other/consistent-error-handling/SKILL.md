---
name: consistent-error-handling
description: "Choose a consistent error handling approach: exceptions, Result types, or error callbacks Use when maintaining consistent code style. Style category skill."
metadata:
  category: Style
  priority: medium
  is-built-in: true
  session-guardian-id: builtin_consistent_error_handling
---

# Consistent Error Handling

Choose a consistent error handling approach: exceptions, Result types, or error callbacks. Don't mix styles arbitrarily. Use custom error classes with meaningful names (UserNotFoundError, ValidationError). Include relevant context in errors. Handle errors at appropriate levels—don't catch and ignore. Log errors with consistent structure. Document error handling patterns in the project.