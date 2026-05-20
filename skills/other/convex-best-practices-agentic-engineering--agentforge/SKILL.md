---
name: convex-best-practices
description: General Convex implementation guidance for this repo. Use before or during schema, function, realtime, auth, or migration work.
version: 1.0.0
metadata:
  author: agentforge
  source: waynesutton/convexskills and get-convex/convex-agent-plugins
---

# Convex Best Practices

Use this skill as the default baseline for Convex work before switching to a narrower Convex skill.

## Default guidance

- Treat functions as the API surface.
- Keep schema explicit and indexes intentional.
- Validate public inputs and outputs.
- Prefer typed helpers over repeated inline logic.
- Use `npx convex dev` during development.

## AgentForge-specific constraints

- Convex is the data layer for this repo.
- Mastra runtime logic belongs in `packages/runtime/`, not in Convex actions.
- Avoid patterns that assume a standalone all-in-one Convex agent app.

## References

- Read [best-practices-checklist.md](/Users/eduardojaviergarcialopez/AgenticEngineering/agentforge/.agents/skills/convex-best-practices/references/best-practices-checklist.md).
