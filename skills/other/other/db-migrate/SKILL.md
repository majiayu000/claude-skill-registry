---
name: db-migrate
description: Creates a database migration using Drizzle. Use this EVERY TIME you need to modify the database schema. Walks through the complete workflow including generating migration, writing SQL, running it locally, and committing ALL required files.
allowed-tools: Bash, Read, Write, Edit, Glob
---

# Database Migration Workflow

**ALWAYS use this skill when modifying the database schema.** Never create migration files manually.

## Step 1: Modify the Schema

Edit the relevant schema file in `apps/web/src/db/schema/`:

```bash
# Find existing schema files
ls apps/web/src/db/schema/
```

Make your changes to the TypeScript schema file (add columns, tables, etc.)

## Step 2: Generate the Migration

```bash
cd apps/web && npx drizzle-kit generate --custom --name describe_your_change
```

This creates THREE files:
- `drizzle/XXXX_name.sql` - Empty SQL file for you to write
- `drizzle/meta/_journal.json` - Updated with new entry (REQUIRED)
- `drizzle/meta/XXXX_snapshot.json` - Schema snapshot (REQUIRED)

## Step 3: Write the SQL

Edit the generated `.sql` file with your migration SQL:

```sql
-- For adding a column:
ALTER TABLE `table_name` ADD COLUMN `column_name` type;

-- For multiple statements, ADD BREAKPOINTS:
CREATE TABLE `foo` (...);
--> statement-breakpoint
INSERT INTO `foo` VALUES (...);
```

**CRITICAL:** If you have multiple SQL statements, you MUST add `--> statement-breakpoint` between them or the migration will crash.

## Step 4: Verify Timestamp Ordering

```bash
tail -10 apps/web/drizzle/meta/_journal.json | grep -E '"when"|"tag"'
```

Ensure your new migration's `when` timestamp is GREATER than all previous migrations. If not, edit `_journal.json` to fix it.

## Step 5: Run Migration Locally

```bash
cd apps/web && pnpm db:migrate
```

## Step 6: Verify the Change

```bash
# Use MCP tool to check the table
mcp__sqlite__describe_table table_name
```

Or manually verify:
```bash
cd apps/web && sqlite3 data/sqlite.db "PRAGMA table_info(table_name);"
```

## Step 7: Commit ALL Files

**CRITICAL: You must commit the entire `drizzle/` directory, not just the SQL file!**

```bash
git add apps/web/src/db/schema/ apps/web/drizzle/
git status  # Verify you see: .sql file, _journal.json, snapshot.json
git commit -m "feat(db): describe your change"
```

The `drizzle/` directory contains:
- `drizzle/XXXX_name.sql` - Your SQL migration
- `drizzle/meta/_journal.json` - Migration registry (REQUIRED for drizzle to run it!)
- `drizzle/meta/XXXX_snapshot.json` - Schema state (REQUIRED)

**If you only commit the .sql file, the migration will NOT run in production!**

## Common Mistakes

| Mistake | Result | Fix |
|---------|--------|-----|
| Only commit .sql file | Migration not recognized | `git add drizzle/` (whole directory) |
| Missing statement breakpoint | RangeError crash | Add `--> statement-breakpoint` between statements |
| Edit deployed migration | Change ignored | Create NEW migration instead |
| Wrong timestamp order | Migration skipped | Edit _journal.json, increase timestamp |

## Quick Reference

```bash
# Full workflow one-liner (after editing schema):
cd apps/web && \
  npx drizzle-kit generate --custom --name my_change && \
  echo "Now edit the .sql file, then run:" && \
  echo "pnpm db:migrate && git add src/db/schema/ drizzle/ && git commit"
```
