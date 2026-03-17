---
name: mern-stack
description: Stack decisions for MERN apps (Next.js, pnpm monorepo). Reference before scaffolding or architecture work.
---

## Locked decisions

| Layer        | Decision                                        |
| ------------ | ----------------------------------------------- |
| Monorepo     | pnpm workspaces                                 |
| Frontend     | Next.js (app router), TypeScript required       |
| API          | Next.js route handlers (`app/api/`) by default  |
| Database     | MongoDB + Mongoose                              |
| Validation   | Zod (shared schemas in `packages/shared`)       |
| Environments | local → non-prod → prod                         |
| Secrets      | `.env.local` for dev; AWS for production        |
| Containers   | Not required unless deployment target forces it |

## Project layout

```
apps/web/                 # Next.js app
  app/api/                # API route handlers
  src/server/             # Server-only code
packages/shared/          # Zod schemas, types, utilities
.github/workflows/        # CI/CD
(root configs)            # eslint, prettier, tsconfig
```

## When to add a separate API service

Only justified if:

- Long-running jobs exceed serverless timeouts
- WebSocket/persistent connections required
- Shared API serves multiple non-Next.js clients
- Compliance requires API isolation

Default: keep API in Next.js route handlers.

## Reference

For versions, env setup, and deployment patterns, see `reference/mern-stack-reference.md`
