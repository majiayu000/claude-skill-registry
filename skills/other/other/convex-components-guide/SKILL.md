---
name: convex-components-guide
description: Use Convex components for encapsulation, reuse, and feature isolation. Use when deciding between local code, helpers, and components.
version: 1.0.0
metadata:
  author: agentforge
  source: get-convex/convex-agent-plugins@f104efb49a787a1ef4a6c84df496d58800ce334a
---

# Convex Components Guide

Use this when the task involves reusable backend capabilities or when a feature is growing too monolithic.

## Prefer components for

- feature encapsulation,
- reusable infrastructure-like backend capabilities,
- isolated integrations,
- sibling services such as storage, billing, analytics, notifications, or AI-support utilities.

## Do not overuse components for

- trivial one-off helpers,
- tightly coupled core domain logic that is simpler as local app code.

## Decision rule

- If the capability should be reusable or independently maintained, consider a component.
- If the capability is just a few local helpers, keep it in app code or use `convex-helpers`.

## References

- Read [components-catalog.md](/Users/eduardojaviergarcialopez/AgenticEngineering/agentforge/.agents/skills/convex-components-guide/references/components-catalog.md) for examples and selection guidance.
