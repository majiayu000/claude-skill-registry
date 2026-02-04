---
name: supastarter-nextjs-skill
description: "Guides development with supastarter for Next.js only (not Vue/Nuxt): tech stack, setup, configuration, database (Prisma), API (Hono/oRPC), auth (Better Auth), organizations, payments (Stripe), AI, customization, storage, mailing, i18n, SEO, deployment, background tasks, analytics, monitoring, E2E. Use when building or modifying supastarter Next.js apps, adding features, or when the user mentions supastarter Next.js, Prisma, oRPC, Better Auth, or related Next.js stack topics."
license: See LICENSE
metadata:
  author: supastarter
  version: "1.0"
  compatibility: "Designed for Cursor (or similar agents). Run scripts from supastarter monorepo root."
---

# supastarter for Next.js – Skill

Expert guidance for building production-ready SaaS applications with the supastarter Next.js starter kit. **Next.js only**; no Vue/Nuxt content.

## When to Use This Skill

Use this skill when:

- Building or modifying a supastarter Next.js app
- Adding features (new entities, API endpoints, UI, i18n)
- Working with Prisma, oRPC, Better Auth, Stripe, or the monorepo structure
- Debugging setup, configuration, deployment, or troubleshooting
- The user mentions supastarter Next.js, Prisma, oRPC, Better Auth, or related stack topics

## High-Level Workflow: New Feature

Follow this order when adding a feature:

1. **Schema** – Add or update Prisma models in `packages/database/prisma/schema.prisma`; run migrations.
2. **Queries** – Add query functions in `packages/database/prisma/queries/` and export from `queries/index.ts`.
3. **API** – Add oRPC procedures in `packages/api/modules/<name>/` (types, procedures, router); mount router in `packages/api/orpc/router.ts`.
4. **UI** – Add React components in `apps/web/` (e.g. `modules/shared/components/`); use shadcn, TanStack Query, session hooks.
5. **i18n** – Add translation keys in `packages/i18n/translations/{en,de}.json`.

Full walkthrough: [assets/recipes/feedback-widget.md](assets/recipes/feedback-widget.md).

## Project Structure (Next.js Monorepo)

```
apps/web/                 # Next.js app (App Router, app/, components/, config/, lib/)
packages/
  api/                    # Hono + oRPC (modules/, orpc/router.ts)
  auth/                   # Better Auth config
  database/               # Prisma schema, migrations, queries
  i18n/                   # Translations
  mail/                   # React Email templates, providers
  storage/                # S3-compatible storage
  ui/                     # Shared UI (shadcn)
  config/                 # Shared config
```

Use package exports (e.g. `@repo/api`, `@repo/database`) instead of deep relative imports.

## References (Progressive Disclosure)

Load only the reference files you need. All paths are from the skill root, one level deep.

**Before writing code**, read [references/coding-conventions.md](references/coding-conventions.md). For copy-paste patterns and commands, use [references/code-patterns.md](references/code-patterns.md) and [references/quick-reference.md](references/quick-reference.md).

| Topic | File |
|-------|------|
| **Coding conventions** (read first) | [references/coding-conventions.md](references/coding-conventions.md) |
| **Code patterns** (examples) | [references/code-patterns.md](references/code-patterns.md) |
| **Quick reference** (commands, paths) | [references/quick-reference.md](references/quick-reference.md) |
| Tech stack | [references/tech-stack.md](references/tech-stack.md) |
| Setup, install, deps | [references/setup.md](references/setup.md) |
| Env, config, feature flags | [references/configuration.md](references/configuration.md) |
| Debugging, common issues | [references/troubleshooting.md](references/troubleshooting.md) |
| Prisma schema, migrations, queries | [references/database-patterns.md](references/database-patterns.md) |
| Hono/oRPC, procedures, router | [references/api-patterns.md](references/api-patterns.md) |
| Better Auth, session, protected endpoints | [references/auth-patterns.md](references/auth-patterns.md) |
| Orgs, roles, multi-tenancy | [references/organization-patterns.md](references/organization-patterns.md) |
| Stripe, webhooks, subscriptions | [references/payments-patterns.md](references/payments-patterns.md) |
| AI features, models | [references/ai-patterns.md](references/ai-patterns.md) |
| UI, theming, extensions | [references/customization.md](references/customization.md) |
| S3-compatible, uploads | [references/storage-patterns.md](references/storage-patterns.md) |
| Emails, templates, providers | [references/mailing-patterns.md](references/mailing-patterns.md) |
| i18n, locales, translations | [references/internationalization.md](references/internationalization.md) |
| Meta, sitemap, structured data | [references/seo.md](references/seo.md) |
| Deploy, production | [references/deployment.md](references/deployment.md) |
| Cron, background jobs | [references/background-tasks.md](references/background-tasks.md) |
| Analytics integration | [references/analytics.md](references/analytics.md) |
| Monitoring, errors | [references/monitoring.md](references/monitoring.md) |
| E2E tests | [references/e2e-testing.md](references/e2e-testing.md) |

## Assets

- **Env template**: [assets/env.example](assets/env.example) – environment variable keys and short comments (no secrets).
- **Full recipe**: [assets/recipes/feedback-widget.md](assets/recipes/feedback-widget.md) – build a feature from DB → API → UI → i18n (feedback widget example).

## Scripts

- **generate_module.py** – Scaffolds a new API module (types, procedures, router). See [scripts/README.md](scripts/README.md) or the Scripts section below.

**How to run** (from supastarter monorepo root):

```bash
python scripts/generate_module.py <module-name>
```

Example: `python scripts/generate_module.py feedback` creates `packages/api/modules/feedback/` with `types.ts`, `procedures/create.ts`, and `router.ts`. Mount the router in `packages/api/orpc/router.ts` manually.

## Conventions (Summary)

- TypeScript everywhere; interfaces for object shapes.
- Named function exports for React components; prefer Server Components; use `"use client"` only when needed.
- Forms: react-hook-form + zod; API: oRPC procedures in `packages/api/modules/`.
- Use `@repo/*` package imports; do not instantiate Prisma/Drizzle in app code.
- pnpm, Biome (format/lint), Turbo; Node.js ≥ 20.

**Before writing code**, read [references/coding-conventions.md](references/coding-conventions.md). For examples and commands: [references/code-patterns.md](references/code-patterns.md), [references/quick-reference.md](references/quick-reference.md), [references/customization.md](references/customization.md), [references/api-patterns.md](references/api-patterns.md).

## Official Docs

- Next.js docs (only): <https://supastarter.dev/docs/nextjs>
- Download docs as .md: <https://supastarter.dev/nextjs-docs.zip>
