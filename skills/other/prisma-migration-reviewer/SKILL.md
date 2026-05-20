---
name: prisma-migration-reviewer
description: Review Prisma SQL migration files for risks before production deployment. Use when asked to review a migration, check migration safety, analyze schema changes, or audit Prisma migrations before deploying.
---

# Prisma Migration Reviewer

Before generating any output, read `config/defaults.md` and adapt all patterns, imports, and code examples to the user's configured stack.

## Process

1. Read the `migration.sql` file (typically at `prisma/migrations/<timestamp>_<name>/migration.sql`).
2. Parse each SQL statement and classify it by risk level.
3. Identify data loss risks, breaking changes, performance concerns, and missing safeguards.
4. Suggest safer alternatives for dangerous operations.
5. Produce a risk report with actionable recommendations.

## Risk Classification

### CRITICAL — Data Loss Risk

These operations destroy data. Block deployment until reviewed.

**Column drop:**
```sql
-- CRITICAL: Drops column and all its data
ALTER TABLE "User" DROP COLUMN "legacyId";
```
Safe alternative: Rename to `_deprecated_legacyId`, drop in a later migration after confirming no code references it.

**Table drop:**
```sql
-- CRITICAL: Drops table and all rows
DROP TABLE "OldAuditLog";
```
Safe alternative: Rename table to `_archived_OldAuditLog`. Drop after data is verified migrated or backed up.

**Type change with data loss:**
```sql
-- CRITICAL: Changing TEXT to VARCHAR(50) truncates values longer than 50 chars
ALTER TABLE "Post" ALTER COLUMN "title" TYPE VARCHAR(50);
```
Safe alternative: First query `SELECT MAX(LENGTH(title)) FROM "Post"` to verify no data exceeds the new limit.

**Enum value removal:**
```sql
-- CRITICAL: Rows with removed value become invalid
-- Prisma recreates enum without the old value
CREATE TYPE "Role_new" AS ENUM ('USER', 'ADMIN');
ALTER TABLE "User" ALTER COLUMN "role" TYPE "Role_new" USING ("role"::text::"Role_new");
DROP TYPE "Role";
ALTER TYPE "Role_new" RENAME TO "Role";
```
Safe alternative: First update all rows with the old value, then remove it.

### WARNING — Potential Downtime or Breakage

**NOT NULL on existing column without default:**
```sql
-- WARNING: Fails if any existing rows have NULL in this column
ALTER TABLE "User" ALTER COLUMN "name" SET NOT NULL;
```
Safe alternative:
1. `UPDATE "User" SET "name" = 'Unknown' WHERE "name" IS NULL;`
2. Then `ALTER TABLE "User" ALTER COLUMN "name" SET NOT NULL;`

**Adding unique constraint on column with potential duplicates:**
```sql
-- WARNING: Fails if duplicate values exist
ALTER TABLE "User" ADD CONSTRAINT "User_email_key" UNIQUE ("email");
```
Safe alternative: First query `SELECT email, COUNT(*) FROM "User" GROUP BY email HAVING COUNT(*) > 1` and resolve duplicates.

**Renaming column (Prisma drops and recreates):**
```sql
-- WARNING: Prisma may generate DROP + ADD instead of RENAME, losing data
ALTER TABLE "User" DROP COLUMN "name";
ALTER TABLE "User" ADD COLUMN "fullName" TEXT;
```
Safe alternative: Use raw SQL migration with `ALTER TABLE "User" RENAME COLUMN "name" TO "fullName"`.

**Large table ALTER:**
```sql
-- WARNING: On tables with millions of rows, this acquires an exclusive lock
ALTER TABLE "Event" ADD COLUMN "metadata" JSONB;
```
For PostgreSQL, adding a nullable column with no default is fast (no table rewrite). But adding a column with a `DEFAULT` requires a table rewrite on PostgreSQL < 11.

### INFO — Optimization Opportunities

**Missing index on foreign key:**
```sql
ALTER TABLE "Post" ADD COLUMN "authorId" TEXT NOT NULL;
ALTER TABLE "Post" ADD CONSTRAINT "Post_authorId_fkey"
  FOREIGN KEY ("authorId") REFERENCES "User"("id");
-- INFO: No index on "Post"."authorId" — queries filtering/joining on this FK will be slow
```
Recommend: `CREATE INDEX "Post_authorId_idx" ON "Post"("authorId");`

**Missing composite index for common query patterns:**
```sql
-- INFO: If queries often filter by both status and createdAt, add a composite index
CREATE INDEX "Order_status_createdAt_idx" ON "Order"("status", "createdAt");
```

## Prisma-Specific Gotchas

- **Prisma renames = drop + create**: When you rename a field in `schema.prisma`, Prisma generates a column drop and add, not a rename. Always use `npx prisma migrate --create-only` and edit the SQL to use `RENAME COLUMN`.
- **Enum changes recreate the type**: Any change to a Prisma enum generates a full drop-and-recreate cycle. Inspect the migration to ensure existing data is preserved.
- **Optional → required**: Changing a field from `String?` to `String` generates `SET NOT NULL` without a backfill. Always add a backfill step.
- **Relation changes**: Changing relation cardinality or required-ness can drop and recreate foreign key constraints, potentially orphaning data.

## Checklist

Before approving any migration:

- [ ] No `DROP COLUMN` or `DROP TABLE` without confirmed backup or rename strategy
- [ ] No `SET NOT NULL` without backfill for existing NULL rows
- [ ] No `UNIQUE` constraint on columns with unverified uniqueness
- [ ] All foreign key columns have indexes
- [ ] Column renames use `RENAME COLUMN`, not drop + add
- [ ] Enum changes preserve existing data values
- [ ] Large table operations assessed for lock duration
- [ ] Down migration strategy documented for irreversible operations

## Output Format

```
## Migration Review: `<migration_name>`

### Summary
| Risk Level | Count |
|-----------|-------|
| 🔴 CRITICAL | N |
| 🟡 WARNING  | N |
| 🔵 INFO     | N |

### Findings

#### 🔴 CRITICAL: [Title]
**Statement**: `[SQL statement]`
**Risk**: [What can go wrong]
**Recommendation**: [Safer alternative with SQL]

#### 🟡 WARNING: [Title]
...

#### 🔵 INFO: [Title]
...

### Pre-Deploy Checklist
- [ ] [Actionable step based on findings]
```

## Reference

See [references/migration-risks.md](references/migration-risks.md) for the complete catalog of dangerous operations and zero-downtime patterns.
