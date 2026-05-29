---
name: service-boundaries
description: Each microservice should own a specific business capability end-to-end (including its data) Use when designing system architecture. Architecture category skill.
metadata:
  category: Architecture
  priority: medium
  is-built-in: true
  session-guardian-id: builtin_service_boundaries
---

# Service Boundaries

Each microservice should own a specific business capability end-to-end (including its data). Services should be independently deployable and loosely coupled. Avoid distributed monoliths where services are tightly dependent. Services communicate via well-defined APIs. Consider bounded contexts from Domain-Driven Design to identify boundaries. Start with a modular monolith; extract services when needed.