---
name: solid-single-responsibility
description: Each class should encapsulate a single concept or responsibility Use when designing system architecture. Architecture category skill.
metadata:
  category: Architecture
  priority: high
  is-built-in: true
  session-guardian-id: builtin_solid_srp
---

# SOLID - Single Responsibility

Each class should encapsulate a single concept or responsibility. If a class has methods that change for different reasons (UI changes vs. business logic vs. persistence), split it. Signs of SRP violation: large classes, many dependencies, god objects, difficulty naming the class. Apply this at module level too—each module should have a cohesive purpose.