---
name: solid-interface-segregation
description: Keep interfaces small and focused Use when designing system architecture. Architecture category skill.
metadata:
  category: Architecture
  priority: medium
  is-built-in: true
  session-guardian-id: builtin_solid_isp
---

# SOLID - Interface Segregation

Keep interfaces small and focused. If classes implementing an interface leave methods empty or throw "not supported," the interface is too large. Split large interfaces into smaller, cohesive ones. Clients should only need to know about methods relevant to them. Prefer multiple small interfaces over one large one—composition is flexible.