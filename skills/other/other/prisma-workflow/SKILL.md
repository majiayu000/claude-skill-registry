---
name: prisma-workflow
description: Prisma workflow for schema changes, migrations, and common pitfalls in this repo.
compatibility: opencode
---

Use this when changing the database schema or repository layer.

## Key files

- Schema: `prisma/schema.prisma`
- Migrations: `prisma/migrations/`
- Seed: `prisma/seed.ts`

## Common commands

- Generate client: `npm run prisma:generate`
- Create/apply migration (dev): `npm run prisma:migrate:dev`
- Introspect DB -> schema: `npm run prisma:db:pull`
- Explore data: `npm run prisma:studio`

## Nullability gotcha

- Prisma maps SQL `NULL` to JavaScript `null`.
- Prefer `value !== null` (or truthiness checks) over `value !== undefined` for DB-nullable fields.
