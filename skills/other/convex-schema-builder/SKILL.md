---
name: convex-schema-builder
description: Design and evolve Convex schemas with proper indexes, relationships, and repo-specific constraints. Use when editing convex/schema.ts or adding tables.
version: 1.0.0
metadata:
  author: agentforge
  source: get-convex/convex-agent-plugins@f104efb49a787a1ef4a6c84df496d58800ce334a
---

# Convex Schema Builder

Use this skill for `convex/schema.ts` work.

## Core rules

- Prefer flat, relational documents over deep nesting.
- Index foreign keys and common filter paths early.
- Use arrays only for small, naturally bounded sets.
- Keep schema changes compatible with current data unless the task explicitly includes a migration.

## AgentForge-specific guidance

- Schema should support the data layer only. Do not model Mastra runtime execution inside Convex unless the repo already does so intentionally.
- If a schema change is for daemon memory or runtime coordination, cross-check [docs/TECH-REFERENCE.md](/Users/eduardojaviergarcialopez/AgenticEngineering/agentforge/docs/TECH-REFERENCE.md) before changing table shapes.

## References

- Read [schema-checklist.md](/Users/eduardojaviergarcialopez/AgenticEngineering/agentforge/.agents/skills/convex-schema-builder/references/schema-checklist.md) for indexing, pagination, and anti-patterns.
