---
name: defensive-programming
description: Validate all external inputs at system boundaries (API endpoints, user input, file reads, environ... Use when enforcing code quality standards. Quality category skill.
metadata:
  category: Quality
  priority: high
  is-built-in: true
  session-guardian-id: builtin_defensive_programming
---

# Defensive Programming

Validate all external inputs at system boundaries (API endpoints, user input, file reads, environment variables). Use guard clauses to fail fast with clear error messages. Never trust data from external sources—always sanitize and validate. Consider what happens when dependencies are unavailable and handle those cases gracefully.