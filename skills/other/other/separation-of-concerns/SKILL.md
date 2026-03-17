---
name: separation-of-concerns
description: Separate business logic from infrastructure (databases, APIs, UI) Use when designing system architecture. Architecture category skill.
metadata:
  category: Architecture
  priority: high
  is-built-in: true
  session-guardian-id: builtin_separation_of_concerns
---

# Separation of Concerns

Separate business logic from infrastructure (databases, APIs, UI). Keep presentation logic separate from data access. Layer your application: controllers handle HTTP, services contain business logic, repositories handle persistence. Don't mix concerns—a function that validates, transforms, persists, and notifies is doing too much. Changes to one concern shouldn't ripple through unrelated code.