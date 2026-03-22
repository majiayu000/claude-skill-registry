---
name: convex-component-authoring
description: Author reusable Convex components with isolated schema, functions, and exports. Use when packaging shareable backend capabilities.
version: 1.0.0
metadata:
  author: agentforge
  source: waynesutton/convexskills
---

# Convex Component Authoring

Use this when the task is to create a reusable Convex component, not just consume one.

## Focus areas

- isolated schema and function boundaries,
- narrow public surface,
- packageable structure,
- explicit dependency and configuration wiring.

## Decision rule

- If the capability is meant to be shared across projects, component authoring is appropriate.
- If the capability is local to AgentForge, prefer normal app code unless reuse pressure is real.
