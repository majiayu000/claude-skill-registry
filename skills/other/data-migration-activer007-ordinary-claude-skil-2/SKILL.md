---
name: data-migration
description: Plan and execute database migrations, data transformations, and system migrations safely with rollback strategies and data integrity validation. Use when migrating databases, transforming data schemas, moving between database systems, implementing versioned migrations, handling data transformations, ensuring data integrity, or planning zero-downtime migrations.
---

# Data Migration - Safe Schema Changes

## When to use this skill

- Migrating database schemas and structures
- Transforming data between formats
- Moving data between database systems
- Implementing versioned database migrations
- Handling data transformations during migrations
- Ensuring data integrity and validation
- Planning zero-downtime migrations
- Rolling back failed migrations safely
- Migrating from legacy systems
- Implementing data backfill strategies
- Testing migrations in staging environments
- Creating migration rollback procedures

## When to use this skill

- Migrating data between schemas, zero-downtime deployments.
- When working on related tasks or features
- During development that requires this expertise

**Use when**: Migrating data between schemas, zero-downtime deployments.

## Process
1. Add new column
2. Dual-write to old & new
3. Backfill historical data
4. Switch reads to new column
5. Remove old column

## Example
\`\`\`sql
-- Step 1: Add column
ALTER TABLE users ADD COLUMN email_new VARCHAR(255);

-- Step 2: Backfill
UPDATE users SET email_new = email WHERE email_new IS NULL;

-- Step 3: Swap
ALTER TABLE users DROP COLUMN email;
ALTER TABLE users RENAME COLUMN email_new TO email;
\`\`\`

## Resources
- [Database Migrations](https://www.prisma.io/docs/concepts/components/prisma-migrate)
