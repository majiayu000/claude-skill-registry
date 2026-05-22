---
name: event-driven-design
description: Use events to decouple producers from consumers Use when designing system architecture. Architecture category skill.
metadata:
  category: Architecture
  priority: medium
  is-built-in: true
  session-guardian-id: builtin_event_driven_design
---

# Event-Driven Design

Use events to decouple producers from consumers. Publishers emit events without knowing who handles them. This enables: adding new behaviors without modifying publishers, asynchronous processing, audit logging, and cross-service communication. Define clear event schemas. Consider eventual consistency implications. Use established patterns like pub/sub, event sourcing when appropriate.