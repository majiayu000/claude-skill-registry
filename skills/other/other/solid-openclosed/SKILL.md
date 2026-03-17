---
name: solid-openclosed
description: Design components that can be extended without modifying existing code Use when designing system architecture. Architecture category skill.
metadata:
  category: Architecture
  priority: medium
  is-built-in: true
  session-guardian-id: builtin_solid_ocp
---

# SOLID - Open/Closed

Design components that can be extended without modifying existing code. Use abstractions (interfaces, abstract classes) and depend on them. Implement new behavior by adding new code (new implementations) rather than changing existing code. Strategy pattern, plugin architectures, and middleware are common OCP implementations. This reduces risk when adding features.