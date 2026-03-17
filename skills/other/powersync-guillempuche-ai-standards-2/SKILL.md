---
name: powersync
description: Build local-first, offline-capable TypeScript apps with PowerSync. Use when implementing real-time sync between SQLite and backend databases (Postgres, MongoDB, MySQL, SQL Server). Covers schema definition, database setup, CRUD operations, React/Vue hooks, watch queries, and Kysely/Drizzle ORM integration.
license: Apache-2.0
metadata:
  author: ai-standards
  version: '1.0'
  language: typescript
  frameworks: react, react-native, vue, node
compatibility: Node.js 18+, TypeScript 4.7+
allowed-tools: Read Write Edit Bash Grep Glob
---

# PowerSync TypeScript Skill

Sync engine for local-first apps with real-time sync between client SQLite and backend databases.

## When to Use

- Offline-first/local-first applications
- Real-time sync between client and server
- Instant UI responsiveness with background sync

## Installation

| Platform        | Package                                            |
| --------------- | -------------------------------------------------- |
| Web             | `@powersync/web` + `@journeyapps/wa-sqlite`        |
| React Native    | `@powersync/react-native` + `@powersync/op-sqlite` |
| React hooks     | `@powersync/react`                                 |
| Vue composables | `@powersync/vue`                                   |
| Node.js         | `@powersync/node`                                  |
| Kysely ORM      | `@powersync/kysely-driver`                         |
| Drizzle ORM     | `@powersync/drizzle-driver`                        |

## Core Setup

1. **Schema** → [docs](https://docs.powersync.com/installation/client-side-setup/define-your-schema.md) · [example](https://github.com/powersync-ja/powersync-js/blob/main/demos/react-supabase-todolist/src/library/powersync/AppSchema.ts)
1. **Database** → [docs](https://docs.powersync.com/installation/client-side-setup/instantiate-powersync-database.md) · [example](https://github.com/powersync-ja/powersync-js/blob/main/demos/react-supabase-todolist/src/library/powersync/system.ts)
1. **Connector** → [docs](https://docs.powersync.com/installation/client-side-setup/integrating-with-your-backend.md) · [example](https://github.com/powersync-ja/powersync-js/blob/main/demos/react-supabase-todolist/src/library/powersync/SupabaseConnector.ts)

## API Quick Reference

| Operation   | Method                                                |
| ----------- | ----------------------------------------------------- |
| Get one     | `db.get(sql, params)` / `db.getOptional(sql, params)` |
| Get all     | `db.getAll(sql, params)`                              |
| Execute     | `db.execute(sql, params)`                             |
| Transaction | `db.writeTransaction(async (tx) => { ... })`          |
| Watch       | `db.query({sql, parameters}).watch()`                 |
| Diff watch  | `db.query({sql, parameters}).differentialWatch()`     |

> Full CRUD: [docs](https://docs.powersync.com/client-sdk-references/javascript-web.md#using-powersync-crud-functions)

## React Hooks

| Hook               | Purpose                         |
| ------------------ | ------------------------------- |
| `useQuery`         | Query with loading/error states |
| `useSuspenseQuery` | Query with Suspense             |
| `useStatus`        | Connection status               |
| `usePowerSync`     | Database instance               |

> Docs: [React](https://docs.powersync.com/client-sdk-references/javascript-web/javascript-spa-frameworks.md#react-hooks) · [Vue](https://docs.powersync.com/client-sdk-references/javascript-web/javascript-spa-frameworks.md#vue-composables)

## ORM Integration

| ORM         | Docs                                                                                                  | Example                                                                                                 |
| ----------- | ----------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| Kysely      | [docs](https://docs.powersync.com/client-sdk-references/javascript-web/javascript-orm/kysely.md)      | [source](https://github.com/powersync-ja/powersync-js/tree/main/packages/kysely-driver)                 |
| Drizzle     | [docs](https://docs.powersync.com/client-sdk-references/javascript-web/javascript-orm/drizzle.md)     | [source](https://github.com/powersync-ja/powersync-js/tree/main/packages/drizzle-driver)                |
| TanStack DB | [docs](https://docs.powersync.com/client-sdk-references/javascript-web/javascript-orm/tanstack-db.md) | [demo](https://github.com/powersync-ja/powersync-js/tree/main/demos/react-supabase-todolist-tanstackdb) |

## Documentation

| Topic            | URL                                                                         |
| ---------------- | --------------------------------------------------------------------------- |
| Overview         | <https://docs.powersync.com/intro/powersync-overview.md>                    |
| Web SDK          | <https://docs.powersync.com/client-sdk-references/javascript-web.md>        |
| React Native SDK | <https://docs.powersync.com/client-sdk-references/react-native-and-expo.md> |
| Sync Rules       | <https://docs.powersync.com/usage/sync-rules.md>                            |
| Watch Queries    | <https://docs.powersync.com/usage/use-case-examples/watch-queries.md>       |
| API Reference    | <https://powersync-ja.github.io/powersync-js/web-sdk>                       |

## Local References

- `references/sync-rules.md` - Sync Rules configuration
- `references/examples.md` - All official example projects

## GitHub Source

[powersync-ja/powersync-js](https://github.com/powersync-ja/powersync-js)

| Package                                                                                                      | Description                       |
| ------------------------------------------------------------------------------------------------------------ | --------------------------------- |
| [common](https://github.com/powersync-ja/powersync-js/tree/main/packages/common)                             | Shared core (schema, sync, types) |
| [web](https://github.com/powersync-ja/powersync-js/tree/main/packages/web)                                   | Web SDK                           |
| [react-native](https://github.com/powersync-ja/powersync-js/tree/main/packages/react-native)                 | React Native SDK                  |
| [node](https://github.com/powersync-ja/powersync-js/tree/main/packages/node)                                 | Node.js SDK                       |
| [capacitor](https://github.com/powersync-ja/powersync-js/tree/main/packages/capacitor)                       | Capacitor SDK                     |
| [react](https://github.com/powersync-ja/powersync-js/tree/main/packages/react)                               | React hooks                       |
| [vue](https://github.com/powersync-ja/powersync-js/tree/main/packages/vue)                                   | Vue composables                   |
| [tanstack-react-query](https://github.com/powersync-ja/powersync-js/tree/main/packages/tanstack-react-query) | TanStack Query integration        |
| [kysely-driver](https://github.com/powersync-ja/powersync-js/tree/main/packages/kysely-driver)               | Kysely ORM driver                 |
| [drizzle-driver](https://github.com/powersync-ja/powersync-js/tree/main/packages/drizzle-driver)             | Drizzle ORM driver                |
| [attachments](https://github.com/powersync-ja/powersync-js/tree/main/packages/attachments)                   | File attachments helper           |
| [powersync-op-sqlite](https://github.com/powersync-ja/powersync-js/tree/main/packages/powersync-op-sqlite)   | OP-SQLite adapter                 |
| [adapter-sql-js](https://github.com/powersync-ja/powersync-js/tree/main/packages/adapter-sql-js)             | SQL.js adapter (Expo Go)          |
