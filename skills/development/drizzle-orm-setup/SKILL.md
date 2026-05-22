---
name: drizzle-orm-setup
description: "Scaffold a Drizzle ORM project with TypeScript schema, relations, database client, and migrations. Use for: setting up Drizzle from scratch, designing table schemas, configuring drizzle-kit, writing type-safe queries, multi-database support (PostgreSQL, MySQL, SQLite). Triggers: drizzle, drizzle orm, drizzle setup, drizzle schema, drizzle migration, drizzle-kit, typescript orm, sql-like orm, drizzle config, drizzle relations, drizzle project."
---

# Drizzle ORM Setup

Set up a Drizzle ORM project with typed schema definitions, relations, database client configuration, and migration tooling. Covers PostgreSQL, MySQL, and SQLite (including Neon, Turso, PlanetScale, Cloudflare D1).

## When to Use

- Starting a new project that needs a TypeScript ORM
- Adding Drizzle ORM to an existing TypeScript/Node.js project
- Designing database schema with type-safe table definitions
- Setting up relations between tables for the relational query API
- Configuring `drizzle-kit` for migration generation and execution
- Migrating from another ORM (Prisma, TypeORM, Knex) to Drizzle
- Setting up Drizzle with a specific database provider (Neon, Turso, PlanetScale, Supabase, Cloudflare D1)

## Tools Used

- **Read** — inspect existing project files (package.json, tsconfig.json, existing schemas)
- **Write** — create schema, config, and client files
- **Edit** — modify existing files (add tables, update relations)
- **Bash** — install dependencies, run drizzle-kit commands
- **Glob** — find existing schema files, detect project structure
- **Grep** — search for existing ORM usage, import patterns

## Bundled Files

```
drizzle-orm-setup/
├── references/
│   ├── schema-patterns.md    # Table definitions, columns, enums, indexes, relations
│   ├── query-patterns.md     # Core SQL-like API + relational query API
│   └── troubleshooting.md    # Common errors and fixes
└── templates/
    ├── schema.ts             # Multi-table starter schema with relations
    ├── drizzle.config.ts     # drizzle-kit config (all 3 dialects)
    └── db.ts                 # Database client setup
```

## Workflow

Follow these four phases in order. **Stop after each phase** to confirm with the user before continuing.

---

### Phase 1: Discover

**Goal:** Understand the project and choose the right database dialect.

1. Check for an existing project:
   ```
   Read package.json        → existing deps, scripts, type:"module"
   Read tsconfig.json       → moduleResolution, target, paths
   Glob **/*.ts             → project structure
   ```

2. Detect any existing ORM or database usage:
   ```
   Grep "prisma|typeorm|knex|sequelize|drizzle" in package.json
   Grep "pg|mysql2|better-sqlite3|@libsql|@neondatabase" in package.json
   ```

3. Determine the database dialect. Ask the user if not obvious:
   - **PostgreSQL** → `drizzle-orm` + `pg` (or `postgres`, `@neondatabase/serverless`, `@vercel/postgres`)
   - **MySQL** → `drizzle-orm` + `mysql2` (or `@planetscale/database`)
   - **SQLite** → `drizzle-orm` + `better-sqlite3` (or `@libsql/client` for Turso, `@cloudflare/workers-types` for D1)

4. Determine the schema organization:
   - Single `schema.ts` file (small projects)
   - `schema/` directory with one file per table (recommended for >3 tables)

> **STOP.** Confirm dialect, driver, and schema organization with the user.

---

### Phase 2: Schema

**Goal:** Create typed table definitions and relations.

1. Read `references/schema-patterns.md` for the full pattern reference.

2. Create the schema file(s). Use the appropriate table constructor:
   - PostgreSQL: `pgTable()`, `pgEnum()`
   - MySQL: `mysqlTable()`, `mysqlEnum()`
   - SQLite: `sqliteTable()`

3. For each table, define:
   - **Columns** with types and constraints (`.notNull()`, `.default()`, `.unique()`, `.references()`)
   - **Primary key** (`.primaryKey()` or `.generatedAlwaysAsIdentity()`)
   - **Indexes** via the third argument: `(table) => [index('name').on(table.col)]`
   - **Timestamps** using the shared pattern from `references/schema-patterns.md`

4. Define relations in the same file (or a separate `relations.ts`):
   ```typescript
   import { relations } from 'drizzle-orm';

   export const usersRelations = relations(users, ({ many }) => ({
     posts: many(posts),
   }));
   ```

5. Use `templates/schema.ts` as a starter if building from scratch.

**Key rules:**
- Relations are for the relational query API only. They do NOT create foreign keys.
- Foreign keys are defined via `.references(() => otherTable.id)` on the column.
- Always define BOTH sides of a relation (e.g., `users → many(posts)` AND `posts → one(users)`).
- Use `$onUpdateFn(() => new Date())` for `updatedAt` columns, NOT database-level triggers.

> **STOP.** Review the schema with the user. Confirm table structure, column types, and relations.

---

### Phase 3: Client + Config

**Goal:** Set up the database connection and drizzle-kit configuration.

1. Read `templates/db.ts` and `templates/drizzle.config.ts` for the starter patterns.

2. Create the database client file (`src/db/index.ts` or `src/db.ts`):
   ```typescript
   import { drizzle } from 'drizzle-orm/node-postgres';
   import * as schema from './schema';

   export const db = drizzle(process.env.DATABASE_URL!, { schema });
   ```
   - The `{ schema }` option enables the relational query API (`db.query.*`).
   - Without it, only the core SQL-like API works (`db.select()`, `db.insert()`, etc.).

3. Create `drizzle.config.ts` at project root:
   ```typescript
   import { defineConfig } from 'drizzle-kit';

   export default defineConfig({
     dialect: 'postgresql',  // or 'mysql' or 'sqlite'
     schema: './src/db/schema.ts',
     out: './drizzle',
     dbCredentials: {
       url: process.env.DATABASE_URL!,
     },
   });
   ```

4. Install dependencies:
   ```bash
   # Core (always needed)
   npm install drizzle-orm

   # Dev tooling (always needed)
   npm install -D drizzle-kit

   # Database driver (pick one)
   npm install pg                          # PostgreSQL (node-postgres)
   npm install @neondatabase/serverless    # Neon serverless
   npm install mysql2                      # MySQL
   npm install better-sqlite3              # SQLite
   npm install @libsql/client              # Turso / libSQL
   ```

5. Add scripts to `package.json`:
   ```json
   {
     "scripts": {
       "db:generate": "drizzle-kit generate",
       "db:migrate": "drizzle-kit migrate",
       "db:push": "drizzle-kit push",
       "db:studio": "drizzle-kit studio"
     }
   }
   ```

> **STOP.** Confirm the client setup and config. Verify the DATABASE_URL is available (env var, .env file, etc.).

---

### Phase 4: Migrate

**Goal:** Generate and run the initial migration.

1. Choose the migration strategy:
   - **`drizzle-kit push`** — Direct schema push. Good for prototyping and local dev. No migration files.
   - **`drizzle-kit generate` + `drizzle-kit migrate`** — Generates SQL migration files in `./drizzle/`. Use for production.

2. For production migrations, run:
   ```bash
   npx drizzle-kit generate    # Creates SQL files in ./drizzle/
   npx drizzle-kit migrate     # Applies pending migrations
   ```

3. Verify the migration:
   ```bash
   # Check generated SQL
   ls ./drizzle/
   cat ./drizzle/0000_*.sql

   # Open Drizzle Studio to inspect
   npx drizzle-kit studio
   ```

4. For programmatic migrations (CI/CD, startup scripts):
   ```typescript
   import { migrate } from 'drizzle-orm/node-postgres/migrator';
   import { db } from './db';

   await migrate(db, { migrationsFolder: './drizzle' });
   ```

**Important notes:**
- Drizzle does NOT support migration rollbacks. To undo, create a new migration that reverses the changes.
- `push` is lossy — it may drop and recreate columns/tables. Never use on production data.
- Migration files are append-only. Don't edit generated SQL files.
- The `./drizzle/meta/` directory tracks migration state. Commit it to version control.

> **STOP.** Confirm migrations ran successfully. Check for any errors.

---

## Troubleshooting Quick Reference

Read `references/troubleshooting.md` for detailed solutions.

| Symptom | Likely Cause | Quick Fix |
|---------|-------------|-----------|
| `Type instantiation is excessively deep` | Too many tables/relations in one file | Split schema into multiple files, use `satisfies` |
| `Relation not found` | Missing relation definition | Define both sides of every relation |
| `Cannot find module 'drizzle-orm/...'` | Wrong dialect import | Match import path to your dialect (e.g., `drizzle-orm/pg-core`) |
| `push` drops a column unexpectedly | Column rename detected as drop+add | Use `generate` + edit the SQL migration manually |
| `Column does not exist` after migration | Schema and DB out of sync | Run `drizzle-kit introspect` to check actual DB state |
| Circular import errors | Relations importing from each other | Put all relations in one file or use barrel exports |

## Architecture Notes

- **Schema-as-code**: Drizzle schemas are plain TypeScript. No DSL, no code generation step. The schema IS the source of truth.
- **Two query APIs**: Core API (`db.select().from()`) for SQL-like control. Relational API (`db.query.users.findMany()`) for nested data loading. Both are fully typed.
- **Relations are virtual**: `relations()` definitions exist only in TypeScript. They tell the relational query API how to join tables but create no database constraints. Foreign keys are separate.
- **drizzle-kit is the CLI**: It reads your TypeScript schema, diffs it against the database (or prior migrations), and generates SQL. It is a dev dependency only — not needed at runtime.
- **Multi-database**: Same API patterns across PostgreSQL, MySQL, and SQLite. Column type imports differ (`pg-core`, `mysql-core`, `sqlite-core`) but the shape is identical.

## Output Summary

After completing all phases, the user should have:

- [ ] Schema file(s) with typed table definitions and relations
- [ ] Database client (`db.ts`) with schema-aware `drizzle()` instance
- [ ] `drizzle.config.ts` at project root
- [ ] Dependencies installed (`drizzle-orm` + `drizzle-kit` + driver)
- [ ] npm scripts for generate/migrate/push/studio
- [ ] Initial migration generated and applied (or schema pushed)
