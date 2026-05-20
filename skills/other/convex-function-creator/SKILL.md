---
name: convex-function-creator
description: Create Convex queries, mutations, actions, and internal functions with validators, auth checks, async safety, and correct runtime boundaries.
version: 1.0.0
metadata:
  author: agentforge
  source: get-convex/convex-agent-plugins@f104efb49a787a1ef4a6c84df496d58800ce334a
---

# Convex Function Creator

Use this when writing or reviewing Convex functions.

## Default requirements

- Public functions should define `args` and `returns`.
- Await all promises.
- Use auth and authorization checks for protected data.
- Use `internal.*` for scheduler and backend-only flows.
- Keep wrappers thin and move reusable logic into plain TypeScript helpers.

## Runtime boundaries

- Queries and mutations stay in the default Convex runtime.
- `"use node"` files may contain only actions and helper logic for actions.
- In AgentForge, actions are still not the place for Mastra runtime orchestration.

## Query design

- Prefer `.withIndex()` over `.filter()` for primary lookups.
- Avoid unbounded `.collect()` when pagination is the real requirement.
- Never use `Date.now()` in queries.

## References

- Read [function-patterns.md](/Users/eduardojaviergarcialopez/AgenticEngineering/agentforge/.agents/skills/convex-function-creator/references/function-patterns.md) for templates and anti-patterns.
