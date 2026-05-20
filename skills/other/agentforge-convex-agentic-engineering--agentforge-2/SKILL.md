---
name: agentforge-convex
description: >
  Comprehensive Convex development skill for building production-ready apps.
  Covers functions (queries, mutations, actions, HTTP endpoints), schemas,
  real-time subscriptions, cron jobs, migrations, and security.
  USE THIS SKILL whenever the user is working with Convex — whether they
  mention Convex directly, reference files in a convex/ directory, ask about
  reactive databases, real-time subscriptions, Convex functions, Convex
  schemas, cron jobs in Convex, HTTP actions, webhook handling, data
  migrations, or security audits for a Convex app. Also trigger for
  questions about ConvexError, v.* validators, defineSchema, defineTable,
  useQuery, useMutation, usePaginatedQuery, optimistic updates, or
  ctx.db / ctx.scheduler / ctx.storage calls.
---

# AgentForge — Convex

Build production-ready Convex applications using established patterns for
functions, schemas, real-time data, scheduling, HTTP endpoints, migrations,
and security.

> **Source:** Adapted from [waynesutton/convexskills](https://github.com/waynesutton/convexskills) (Apache-2.0).
> Always cross-check with the live docs at <https://docs.convex.dev/> and
> <https://docs.convex.dev/llms.txt> before implementing.

---

## Quick-Reference Card

| Need to…                           | Read reference file              |
| ---------------------------------- | -------------------------------- |
| Organize functions & general rules | `references/best-practices.md`   |
| Write queries / mutations / actions | `references/functions.md`       |
| Add real-time subs & optimistic UI | `references/realtime.md`         |
| Define schemas, validators, indexes | `references/schema-validator.md` |
| Schedule recurring background work | `references/cron-jobs.md`        |
| Create HTTP endpoints / webhooks   | `references/http-actions.md`     |
| Evolve schema & backfill data      | `references/migrations.md`       |
| Deep security review (RBAC, rate limiting) | `references/security-audit.md` |
| Quick security checklist           | `references/security-check.md`   |

**How to use this table:** Read only the reference file(s) relevant to the
current task. Each file is self-contained with documentation links, code
examples, best practices, and common pitfalls.

---

## Core Principles (The Zen of Convex)

1. **Convex manages the hard parts** — caching, real-time sync, consistency.
2. **Functions are the API** — design them as your application's interface.
3. **Schema is truth** — define your data model explicitly in `schema.ts`.
4. **TypeScript everywhere** — leverage end-to-end type safety.
5. **Queries are reactive** — think subscriptions, not requests.

---

## Universal Rules

These apply to *every* Convex task regardless of which reference you read:

- **Never** run `npx convex deploy` unless explicitly instructed.
- **Never** run any git commands unless explicitly instructed.
- Always define both `args` and `returns` validators on every function.
- Use indexes (`withIndex`) instead of `.filter()` for efficient queries.
- Use `internalMutation` / `internalQuery` / `internalAction` for anything
  that should not be callable from the client.
- Use `ConvexError` for user-facing errors; sanitize internal errors.
- Store all secrets in environment variables; access only inside actions.
- Install and configure `@convex-dev/eslint-plugin` for build-time enforcement.

---

## Function Types at a Glance

| Type        | DB Access            | External APIs | Cached / Reactive | Typical Use           |
| ----------- | -------------------- | ------------- | ----------------- | --------------------- |
| Query       | Read-only            | No            | Yes               | Fetching data         |
| Mutation    | Read / Write         | No            | No                | Modifying data        |
| Action      | Via `runQuery`/`runMutation` | Yes   | No                | External integrations |
| HTTP Action | Via `runQuery`/`runMutation` | Yes   | No                | Webhooks, REST APIs   |

---

## Linting Setup

```bash
npm i @convex-dev/eslint-plugin --save-dev
```

```js
// eslint.config.js
import { defineConfig } from "eslint/config";
import convexPlugin from "@convex-dev/eslint-plugin";

export default defineConfig([
  ...convexPlugin.configs.recommended,
]);
```

Enforced rules: object syntax with `handler`, argument validators on all
functions, explicit table names in DB operations, no Node imports in the
Convex runtime.

---

## Canonical Documentation Links

- Best Practices: <https://docs.convex.dev/understanding/best-practices/>
- Functions: <https://docs.convex.dev/functions>
- Schemas & Indexes: <https://docs.convex.dev/database/schemas>
- Realtime / React Client: <https://docs.convex.dev/client/react>
- Cron Jobs: <https://docs.convex.dev/scheduling/cron-jobs>
- HTTP Actions: <https://docs.convex.dev/functions/http-actions>
- Auth: <https://docs.convex.dev/auth>
- Production: <https://docs.convex.dev/production>
- Full LLM context: <https://docs.convex.dev/llms.txt>
