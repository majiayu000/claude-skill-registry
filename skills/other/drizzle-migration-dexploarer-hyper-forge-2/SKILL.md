---
name: drizzle-migration
description: Execute the proper Drizzle Kit workflow for database schema migrations in asset-forge. Use this when the user asks to create a database migration, update the database schema, or when schema changes need to be applied to the database.
allowed-tools: [Bash, Read, Grep, Edit]
---

# Drizzle Kit Migration Workflow

This skill guides you through the proper database migration workflow using Drizzle Kit for the asset-forge project.

## When to Use This Skill

Use this skill when:
- User asks to "create a migration" or "generate a migration"
- Database schema files in `server/db/schema/` have been modified
- User asks to "update the database" or "apply migrations"
- User asks about the migration workflow

## Workflow Steps

### 1. Generate Migration from Schema

After making changes to TypeScript schema files in `packages/asset-forge/server/db/schema/`, generate a migration:

```bash
cd ${WORKSPACE_DIR}/packages/asset-forge
bun run db:generate
```

**What this does:**
- Reads all schema files from `server/db/schema/`
- Compares with previous migration state
- Generates SQL migration file in `server/db/migrations/`
- Auto-generates migration name like `0001_clever_name.sql`

**Common errors:**
- TypeScript syntax errors in schema files → Fix with `/check-types`
- Circular dependencies → Check foreign key references
- Invalid column types → Verify Drizzle types

### 2. Review Generated SQL

**ALWAYS review the SQL before applying!** Use the Read tool to check:

```bash
# Find latest migration
cd ${WORKSPACE_DIR}/packages/asset-forge
ls -t server/db/migrations/*.sql | head -1
```

**Review checklist:**
- [ ] SQL statements match intended schema changes
- [ ] No unintended DROP TABLE or DROP COLUMN statements
- [ ] Foreign keys reference existing tables
- [ ] Indexes are properly named
- [ ] Data migrations (if any) are correct

### 3. Apply Migration to Database

After reviewing, apply the migration:

```bash
cd ${WORKSPACE_DIR}/packages/asset-forge
bun run db:migrate
```

**What this does:**
- Connects to database using DATABASE_URL
- Runs pending migrations in order
- Updates migration journal table
- Applies schema changes

**Troubleshooting:**
- Migration fails → Check database connection in .env
- "Relation already exists" → Schema already in DB, might need to reset or create fix migration
- Permission errors → Check database file permissions (SQLite) or user permissions (PostgreSQL)

### 4. Verify Changes

After successful migration, verify with Drizzle Studio:

```bash
cd ${WORKSPACE_DIR}/packages/asset-forge
bun run db:studio
```

Opens web UI at http://test-db-studio:4983 to inspect:
- Tables created/modified correctly
- Data integrity maintained
- Indexes created
- Foreign keys working

## Important Notes

### Auto-Generated vs Manual SQL
- ✅ **ALWAYS use Drizzle Kit** to generate migrations
- ❌ **NEVER write SQL files manually** in migrations folder
- Why: Drizzle tracks schema state and ensures consistency

### Migration Files Must Be Committed
After generating and applying migrations:
1. Add both schema files AND migration SQL to git
2. Commit together to keep schema + migrations in sync
3. Never .gitignore the migrations folder

### Development vs Production
- **Development**: Can use `bun run db:push` to sync schema directly (skips migrations)
- **Production**: ALWAYS use migrations (db:generate + db:migrate)

### Rollback Strategy
Drizzle Kit doesn't have automatic rollback. To rollback:
1. Create a new "down" migration that reverses changes
2. Or restore database from backup
3. Or manually write DROP/ALTER statements

## Environment Requirements

Required in `.env`:
```bash
DATABASE_URL="postgresql://user:pass@host:port/dbname"
# or for SQLite:
DATABASE_URL="file:./local.db"
```

## Related Commands

- `/migrate` - Full migration workflow (generate → review → apply)
- `/migrate generate` - Generate only
- `/migrate apply` - Apply only
- `/db/studio` - Launch Drizzle Studio
- `/check-types` - Verify schema TypeScript

## Example Workflow

```typescript
// 1. User modifies schema
// packages/asset-forge/server/db/schema/teams.schema.ts
export const teams = pgTable('teams', {
  id: uuid('id').primaryKey().defaultRandom(),
  name: varchar('name', { length: 255 }).notNull(),
  // NEW: added description field
  description: text('description'),
  createdAt: timestamp('created_at').defaultNow().notNull(),
});

// 2. Generate migration
// bun run db:generate
// → Creates: 0004_amazing_hulk.sql

// 3. Review SQL
// ALTER TABLE "teams" ADD COLUMN "description" text;

// 4. Apply migration
// bun run db:migrate
// → Migration applied successfully

// 5. Commit changes
// git add server/db/schema/teams.schema.ts
// git add server/db/migrations/0004_amazing_hulk.sql
// git commit -m "feat: add description field to teams table"
```

## Key Takeaways

1. **TypeScript → SQL**: Schema changes in .ts files generate .sql migrations
2. **Review First**: Always read the SQL before applying
3. **Commit Together**: Schema files + migration files in same commit
4. **Production-Safe**: Migrations are the safe way to evolve schema
5. **Drizzle Studio**: Visual verification after applying migrations

## Files to Know

- `packages/asset-forge/drizzle.config.ts` - Drizzle Kit configuration
- `packages/asset-forge/server/db/schema/` - All schema definitions
- `packages/asset-forge/server/db/migrations/` - Generated SQL migrations
- `packages/asset-forge/server/db/migrations/meta/_journal.json` - Migration tracking

---

**Remember**: Never skip the review step! Always inspect the generated SQL before running db:migrate.
