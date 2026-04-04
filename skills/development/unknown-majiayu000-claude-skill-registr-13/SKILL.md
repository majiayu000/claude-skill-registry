---
name: convex-migration
description: guidance on how to properly do data migrations in Convex
---

**[Full docs](https://www.convex.dev/components/migrations)**

Use `@convex-dev/migrations` in `convex/migrations.ts` (reference `convex_migrations.md` for full guidance). The standard flow is:

- loosen schema/app to tolerate old+new values
- add `migrations.define({ table, migrateOne })` in `convex/migrations.ts` (idempotent; skip no‑ops; no external APIs).
- dry run: `npx convex run migrations:runYourFn '{"dryRun":true,"cursor":null}'`
- full run: `npx convex run migrations:runYourFn '{"cursor":null}'`*
- monitor: `npx convex run --component migrations lib:getStatus --watch`
- cancel: `npx convex run --component migrations lib:cancel '{"name":"migrations:yourFnName"}'`.

*`"cursor":null` makes it to real work from the start (as opposed to the dry-run default); omit only when resuming from a specific cursor.