---
name: "cloudflare-d1-migrations-and-production-seeding"
description: "Use this skill whenever the user wants to design, run, or refine Cloudflare D1 schema management, migrations, and data seeding for dev/staging/production environments, especially in conjunction with Hono/Workers apps."
---

# Cloudflare D1 Migrations & Production Seeding Skill

## Purpose

You are a specialized assistant for **schema and data lifecycle** of **Cloudflare D1** databases,
used typically with Hono + TypeScript apps running on Cloudflare Workers/Pages.

Use this skill to:

- Design and evolve **D1 schemas** using SQL (not ad-hoc changes in the UI)
- Set up and manage **D1 migrations** via Wrangler
- Implement safe **migration workflows** for dev, staging, and production
- Create **seed scripts/data** for development & test
- Help with **data migrations** (changing schema without losing data)
- Keep D1 usage **predictable and reproducible** across environments

Do **not** use this skill for:

- Hono routing or business logic → `hono-app-scaffold`, feature skills
- D1 query code in TypeScript → `hono-d1-integration` (that skill handles data access layer)
- Non-D1 databases (Postgres/MySQL/etc.) → use other DB skills

If `CLAUDE.md` or existing docs describe DB conventions (naming, migrations folder, tenant strategy), follow them.

---

## When To Apply This Skill

Trigger this skill when the user says things like:

- “Set up migrations for D1.”
- “Create/modify tables in D1 in a structured way.”
- “Apply schema changes across dev/staging/prod.”
- “Seed test data into my D1 database.”
- “Help me evolve this D1 schema safely.”
- “My D1 schema in prod is out of sync, fix the process.”

Avoid when:

- Only a single dev-only prototype DB is used with no need for consistency.
- Schema is fully managed externally and NOT via SQL/migrations in this repo.

---

## Core Concepts for This Skill

- **Schema is code**: D1 schema should be defined via SQL files in the repo.
- **Migrations are ordered**: Each change is a migration with a timestamp/sequence.
- **Environments differ**: dev/staging/prod may have different DBs, but **same migrations**.
- **Seeds are environment-aware**: dev/test seeds can differ from prod initial data.

This skill assumes that:

- D1 is bound in `wrangler.toml` as `DB` (or some project-defined name).
- The project has or will have a `db/` or `migrations/` directory for SQL.

---

## Recommended Project Structure

```text
project-root/
  src/
    db/
      schema.sql               # initial base schema
  db/
    migrations/
      0001_init.sql
      0002_add_posts_table.sql
      0003_add_indexes.sql
    seeds/
      dev.seed.sql
      test.seed.sql
  wrangler.toml
```

> Note: location is flexible as long as Wrangler commands reference the correct path.

This skill will adapt structure to the existing repo but keep these concepts.

---

## Defining Initial Schema (`schema.sql`)

For a new project, start with a base schema file:

```sql
-- src/db/schema.sql or db/schema.sql

CREATE TABLE IF NOT EXISTS users (
  id TEXT PRIMARY KEY,
  email TEXT NOT NULL UNIQUE,
  password_hash TEXT NOT NULL,
  created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
  updated_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now'))
);

CREATE TABLE IF NOT EXISTS posts (
  id TEXT PRIMARY KEY,
  user_id TEXT NOT NULL,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
  FOREIGN KEY (user_id) REFERENCES users(id)
);
```

Use this as the **canonical source of truth** for the initial DB state.

To apply `schema.sql` to a local dev DB:

```bash
wrangler d1 execute <db_name> --local --file=src/db/schema.sql
```

This skill will:

- Encourage a clean, normalized initial schema.
- Align SQL with Types (`User`, `Post`, etc.) defined in `hono-d1-integration` skill.

---

## Migrations: Creating & Applying

**Do not re-run `schema.sql` as a way to “update” prod.** Instead, use **migrations**.

### Creating a Migration

Use Wrangler to create a migration file (name is a description):

```bash
wrangler d1 migrations create <db_name> add_comments_table
```

This creates a new SQL file under the migrations folder, e.g.:

```text
db/migrations/
  0001_init.sql
  0002_add_comments_table.sql   # created by wrangler
```

Edit the new migration file:

```sql
-- db/migrations/0002_add_comments_table.sql

CREATE TABLE comments (
  id TEXT PRIMARY KEY,
  post_id TEXT NOT NULL,
  user_id TEXT NOT NULL,
  body TEXT NOT NULL,
  created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
  FOREIGN KEY (post_id) REFERENCES posts(id),
  FOREIGN KEY (user_id) REFERENCES users(id)
);
```

This skill should:

- Ensure migrations are **append-only** (don’t edit old migrations after applying to any environment).
- Encourage small, focused migrations with clear names.

### Applying Migrations (Local / Dev)

To apply all pending migrations to local dev DB:

```bash
wrangler d1 migrations apply <db_name> --local
```

This will run all migrations that haven’t been applied yet.

For **Cloud/prod DB**:

```bash
wrangler d1 migrations apply <db_name>
```

This skill should recommend:

- Apply migrations to **staging** before production.
- Run migrations as part of a deploy or a separate pre-deploy step (via CI/CD).

---

## Migration Strategy Across Environments

Assume `wrangler.toml` contains environment-specific D1 bindings:

```toml
[[d1_databases]]
binding = "DB"
database_name = "my_db_dev"
database_id = "dev-xxxx"

[env.staging]
[[env.staging.d1_databases]]
binding = "DB"
database_name = "my_db_staging"
database_id = "staging-xxxx"

[env.production]
[[env.production.d1_databases]]
binding = "DB"
database_name = "my_db_prod"
database_id = "prod-xxxx"
```

Then, the typical workflow:

- **Dev DB (local)**:
  - `wrangler d1 migrations apply my_db_dev --local`
- **Staging DB**:
  - `wrangler d1 migrations apply my_db_staging --env staging`
- **Production DB**:
  - `wrangler d1 migrations apply my_db_prod --env production`

This skill can:

- Provide canonical commands tailored to the project’s actual names.
- Suggest adding scripts in `package.json` to make this repeatable, e.g.:

  ```jsonc
  {
    "scripts": {
      "db:migrate:local": "wrangler d1 migrations apply my_db_dev --local",
      "db:migrate:staging": "wrangler d1 migrations apply my_db_staging --env staging",
      "db:migrate:prod": "wrangler d1 migrations apply my_db_prod --env production"
    }
  }
  ```

---

## Data Seeding

### Seed Files

Use SQL seed files for dev/test:

```sql
-- db/seeds/dev.seed.sql
INSERT INTO users (id, email, password_hash)
VALUES
  ("u1", "dev1@example.com", "HASH1"),
  ("u2", "dev2@example.com", "HASH2");

INSERT INTO posts (id, user_id, title, body)
VALUES
  ("p1", "u1", "Hello dev", "First dev post");
```

### Applying Seeds

For local dev:

```bash
wrangler d1 execute <db_name> --local --file=db/seeds/dev.seed.sql
```

For test DBs you might:

- Use a smaller or more targeted seed file (`test.seed.sql`).
- Or use in-test setup scripts that insert data programmatically (using D1 and Hono test helpers).

This skill will:

- Emphasize that **prod environments rarely use “seed files”** beyond initial, intentional bootstrapping (like initial admin user). Those should be careful, one-off migrations or controlled operations.

---

## Schema Evolution / Data Migration

When changing schema in a non-trivial way (e.g., splitting a column, renaming), this skill should:

1. Plan for **multi-step migrations**:

   Example: rename `username` to `handle`

   ```sql
   -- Step 1: add new column
   ALTER TABLE users ADD COLUMN handle TEXT;

   -- Step 2: copy data
   UPDATE users SET handle = username;

   -- Step 3: (later) drop old column if safe
   ```

2. Avoid destructive actions that lose data without an explicit backup/migration plan.

3. For large data sets, warn about expensive operations and suggest phased rollouts if needed.

The skill will also:

- Ensure changes in TS types/entities (from `hono-d1-integration`) match the new schema.
- Suggest adding “backfill” scripts or migrations when needed.

---

## Coordination With Application Code

This skill must coordinate schema changes with code changes:

- **Additive changes** (new columns with defaults) are usually safe to deploy before code that uses them.
- **Destructive changes** (drop columns, change types) require:
  - Rolling deploys where old code can still run for a while.
  - Possibly a “compat layer” or phased roll-out.
- **Versioned APIs**: For major schema reworks, consider versioned routes (`/v1`, `/v2`) temporarily.

The skill should help sequence:

1. Add new columns / tables.
2. Deploy code that writes to both old & new where needed.
3. Backfill data.
4. Switch reads to new columns.
5. Drop old columns.

Even if simplified, it must emphasize not to break prod accidentally.

---

## Integration with CI/CD

Though CI specifics belong to a separate skill (e.g., `cloudflare-ci-cd-github-actions`), this skill should:

- Suggest running `wrangler d1 migrations apply` against staging/prod as part of the deploy pipeline.
- Emphasize **idempotence** and ordered migrations.
- Provide example steps like:

  1. Run tests.
  2. Build Worker.
  3. Apply migrations to staging DB.
  4. Deploy Worker to staging.
  5. After verification, apply migrations to prod DB.
  6. Deploy Worker to prod.

---

## Error Handling & Debugging

When migrations fail, this skill should:

- Suggest checking:
  - SQL syntax in failing migration.
  - Whether migration was partially applied.
  - D1 console & Wrangler logs.

- Recommend recovery approaches:
  - Fix the migration and re-run (if it never applied successfully anywhere).
  - If applied partially in dev but not staging/prod, you may create a new corrective migration instead of editing history.

---

## Interaction with Other Skills

- `cloudflare-worker-deployment`:
  - This skill plugs into that one’s environment config, aligning D1 names with wrangler.toml.
- `hono-d1-integration`:
  - That skill defines TypeScript types and query helpers; this one defines schema & migrations these queries rely on.
- `hono-authentication`:
  - For user/auth tables, this skill defines the underlying D1 schema.
- `nestjs-typeorm-integration` and other DB skills:
  - Conceptual parallels, but for D1 we stay SQL + D1 APIs, not TypeORM.

---

## Example Prompts That Should Use This Skill

- “Create initial D1 schema and migrations for users/posts.”
- “Add a new table in D1 and generate a migration.”
- “Set up dev/staging/prod migration commands for D1.”
- “Add seeding for local dev in D1.”
- “Safely migrate a column in a D1 table without losing data.”

For such tasks, rely on this skill to maintain a **clean, versioned, and environment-aware D1 schema**,
keeping prod safe while making development and testing smooth.
