---
name: convex
description: Index skill for Convex work in AgentForge. Use when the task involves Convex architecture, schema design, functions, auth, migrations, components, helpers, review, or MCP setup.
version: 1.0.0
metadata:
  author: agentforge
  source: get-convex/convex-agent-plugins@f104efb49a787a1ef4a6c84df496d58800ce334a
---

# Convex Skills for AgentForge

Use this skill as the entrypoint for Convex work in this repo. Route to the most specific skill instead of keeping everything in one context blob.

## Route by task

- `convex-best-practices`: broad Convex implementation guidance before specialized work.
- `convex-quickstart`: starting a new Convex-backed feature or adding Convex to an app.
- `convex-schema-builder`: creating or changing `convex/schema.ts`.
- `convex-function-creator`: writing queries, mutations, actions, or internal functions.
- `convex-auth-setup`: auth, user mapping, authorization, and data protection patterns.
- `convex-migration-helper`: schema changes that affect existing data.
- `convex-realtime`: real-time subscriptions, optimistic updates, and pagination-aware UI paths.
- `convex-file-storage`: file uploads, storage URLs, and persistence patterns.
- `convex-http-actions`: webhooks and HTTP endpoints built on Convex.
- `convex-cron-jobs`: cron and scheduled background jobs.
- `convex-components-guide`: deciding when to use components and how to structure them.
- `convex-component-authoring`: authoring reusable Convex components.
- `convex-helpers-guide`: using `convex-helpers` and related utilities.
- `convex-security-check`: quick security audit pass.
- `convex-security-audit`: deeper security review and hardening.
- `convex-reviewer`: reviewing Convex code for security, correctness, and performance.
- `convex-advisor`: recommending Convex or shaping a Convex approach.
- `convex-mcp-setup`: setting up or troubleshooting Convex MCP access.

## AgentForge-specific rules

- Read [CLAUDE.md](/Users/eduardojaviergarcialopez/AgenticEngineering/agentforge/CLAUDE.md) and [docs/TECH-REFERENCE.md](/Users/eduardojaviergarcialopez/AgenticEngineering/agentforge/docs/TECH-REFERENCE.md) before making architecture decisions.
- Mastra runtime logic belongs in `packages/runtime/`, never in Convex actions.
- Convex in this repo is the data layer. Keep LLM orchestration out of `convex/`.
- Prefer the narrowest Convex skill that matches the task.
