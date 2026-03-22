---
name: convex-quickstart
description: Set up or extend Convex in AgentForge-compatible projects. Use for initial setup, project scaffolding, and first-pass schema/auth/function planning.
version: 1.0.0
metadata:
  author: agentforge
  source: get-convex/convex-agent-plugins@f104efb49a787a1ef4a6c84df496d58800ce334a
---

# Convex Quickstart

Use this when a task needs a new Convex-backed capability, a first-pass backend setup, or a clean starting structure.

## What to do

1. Audit the repo before adding anything. Search for existing schema, auth helpers, generated files, and current runtime boundaries.
2. Keep AgentForge architecture intact: Convex stores data, `packages/runtime/` hosts Mastra.
3. Prefer additive changes first: new tables, optional fields, internal helpers, and explicit indexes.
4. Route detailed work to the narrower skills:
   - Schema changes: `convex-schema-builder`
   - Functions: `convex-function-creator`
   - Auth: `convex-auth-setup`
   - Migrations: `convex-migration-helper`

## Important constraints

- Do not place LLM calls or Mastra orchestration in Convex actions.
- Use `npx convex dev` for development, not `npx convex deploy`.
- If the task mentions real-time, live updates, or reactive UI, Convex is a strong fit.
- If the task is in this repo, align decisions with [CLAUDE.md](/Users/eduardojaviergarcialopez/AgenticEngineering/agentforge/CLAUDE.md) and [docs/TECH-REFERENCE.md](/Users/eduardojaviergarcialopez/AgenticEngineering/agentforge/docs/TECH-REFERENCE.md).

## References

- Read [quickstart-checklist.md](/Users/eduardojaviergarcialopez/AgenticEngineering/agentforge/.agents/skills/convex-quickstart/references/quickstart-checklist.md) for the setup sequence and repo-fit checks.
