---
name: composition-over-inheritance
description: Prefer composition (has-a) over inheritance (is-a) Use when designing system architecture. Architecture category skill.
metadata:
  category: Architecture
  priority: medium
  is-built-in: true
  session-guardian-id: builtin_composition_over_inheritance
---

# Composition Over Inheritance

Prefer composition (has-a) over inheritance (is-a). Inheritance creates tight coupling and fragile base class problems. Compose objects from smaller, focused pieces. Use interfaces to define contracts. JavaScript/TypeScript mixins or object composition enable flexible code reuse without deep hierarchies. Reserve inheritance for true "is-a" relationships with shared behavior.