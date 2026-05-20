---
name: convex-helpers-guide
description: Discover and apply convex-helpers patterns such as relationship helpers and custom function wrappers.
version: 1.0.0
metadata:
  author: agentforge
  source: get-convex/convex-agent-plugins@f104efb49a787a1ef4a6c84df496d58800ce334a
---

# Convex Helpers Guide

Use this when a task needs common Convex patterns without introducing full components.

## Best uses

- relationship traversal helpers,
- custom function wrappers for data protection,
- common server-side utilities that remove boilerplate.

## Decision rule

- Reach for helpers when the problem is repeated but still local to the app.
- Reach for components when the capability should be encapsulated and reusable across projects.

## References

- Read [helpers-catalog.md](/Users/eduardojaviergarcialopez/AgenticEngineering/agentforge/.agents/skills/convex-helpers-guide/references/helpers-catalog.md) for the high-value helpers to consider first.
