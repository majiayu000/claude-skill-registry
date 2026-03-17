---
name: fail-fast
description: "Check preconditions at the start of functions and fail immediately if they aren't met Use when enforcing code quality standards. Quality category skill."
metadata:
  category: Quality
  priority: high
  is-built-in: true
  session-guardian-id: builtin_fail_fast
---

# Fail Fast

Check preconditions at the start of functions and fail immediately if they aren't met. Throw exceptions with descriptive messages that include relevant context (what failed, why, and what values caused it). Never silently swallow exceptions. Use specific exception types rather than generic ones. Log errors with enough context to diagnose issues in production.