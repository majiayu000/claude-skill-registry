---
name: solid-dependency-inversion
description: Depend on abstractions (interfaces, abstract classes), not concrete implementations Use when designing system architecture. Architecture category skill.
metadata:
  category: Architecture
  priority: high
  is-built-in: true
  session-guardian-id: builtin_solid_dip
---

# SOLID - Dependency Inversion

Depend on abstractions (interfaces, abstract classes), not concrete implementations. High-level business logic should not directly instantiate databases, APIs, or frameworks. Use dependency injection to provide concrete implementations. This enables testing (inject mocks), flexibility (swap implementations), and clear boundaries between layers.