---
name: database-migration
description: Create, execute, and roll back versioned database schema migrations using tools like Alembic, Prisma Migrate, Flyway, and Knex. Use when the user requests database migration or provides relevant inputs for this workflow.
license: MIT
metadata:
  author: AI Agent Skills Community
  version: 1.0.0
---

# Database Migration

This skill enables an AI agent to manage versioned database schema changes through migration frameworks. The agent creates forward and rollback migration scripts, handles data backfills during schema changes, ensures zero-downtime deployments with safe migration patterns, and integrates migration workflows into CI/CD pipelines. It supports major tools including Alembic (Python/SQLAlchemy), Prisma Migrate (TypeScript/Node), Flyway (Java/SQL), and Knex (JavaScript).

## Workflow

1. **Assess the schema change:** Analyze the requested change — adding columns, creating tables, modifying constraints, renaming fields, or transforming data. Classify the change as backward-compatible (additive) or breaking (destructive) to determine the deployment strategy. Breaking changes require a multi-phase migration approach.

2. **Select the migration tool:** Choose the appropriate migration framework based on the project's tech stack. Use Alembic for Python/SQLAlchemy projects, Prisma Migrate for TypeScript/Prisma projects, Flyway for Java or SQL-first workflows, and Knex for Node.js/Express projects. Ensure the tool is initialized and connected to the target database.

3. **Generate the migration script:** Auto-generate a migration from schema diffs where supported (Alembic autogenerate, Prisma migrate dev), then review and edit the generated script. Add explicit rollback (downgrade) logic. For data backfills, include the data transformation within the migration to keep schema and data changes atomic.

4. **Test in a staging environment:** Apply the migration against a staging database that mirrors production. Verify that the migration applies cleanly, that existing queries still work, and that the rollback restores the previous state. Run the application's test suite against the migrated schema.

5. **Deploy with zero-downtime strategy:** For production, use expand-and-contract migrations. Phase 1: add new columns/tables (expand) without removing old ones. Phase 2: deploy application code that writes to both old and new structures. Phase 3: backfill data. Phase 4: deploy code using only new structures. Phase 5: remove old columns/tables (contract). This ensures no downtime and safe rollback at each phase.

6. **Verify and monitor:** After deployment, verify migration status with the framework's status command. Monitor application logs and database performance for regressions. Confirm all migration metadata is recorded in the framework's version table.

## Supported Technologies

- **Alembic:** Python, SQLAlchemy, PostgreSQL/MySQL/SQLite
- **Prisma Migrate:** TypeScript/JavaScript, Prisma ORM, PostgreSQL/MySQL/SQLite/SQL Server
- **Flyway:** Java, SQL-based migrations, all major RDBMS
- **Knex:** JavaScript/TypeScript, Node.js, PostgreSQL/MySQL/SQLite
- **Django Migrations:** Python, Django ORM
- **Sequelize:** JavaScript, Node.js ORM

## Usage

Describe the schema change you need (e.g., "add a `phone_number` column to the `users` table") and specify which migration framework your project uses. The agent will generate the migration file with both upgrade and downgrade logic, provide instructions to apply it, and advise on safe deployment strategies for production.

## Examples

### Example 1: Alembic Migration — Adding a Column with Data Backfill

**Request:** Add a `display_name` column to the `users` table and backfill it by concatenating `first_name` and `last_name`.

**Generate the migration:**

```bash
alembic revision --autogenerate -m "add_display_name_to_users"
```

**Migration file (`versions/20250115_add_display_name_to_users.py`):**

```python
"""add display_name to users

Revision ID: a1b2c3d4e5f6
Revises: 9z8y7x6w5v4u
Create Date: 2025-01-15 10:30:00.000000
"""
from alembic import op
import sqlalchemy as sa

revision = "a1b2c3d4e5f6"
down_revision = "9z8y7x6w5v4u"
branch_labels = None
depends_on = None


def upgrade():
    # Phase 1: Add the column as nullable (safe, no locks on reads)
    op.add_column("users", sa.Column("display_name", sa.String(300), nullable=True))

    # Phase 2: Backfill existing rows
    users = sa.table(
        "users",
        sa.column("id", sa.Integer),
        sa.column("first_name", sa.String),
        sa.column("last_name", sa.String),
        sa.column("display_name", sa.String),
    )
    op.execute(
        users.update().values(
            display_name=sa.func.concat(
                users.c.first_name, " ", users.c.last_name
            )
        )
    )

    # Phase 3: Set NOT NULL after backfill is complete
    op.alter_column("users", "display_name", nullable=False)


def downgrade():
    op.drop_column("users", "display_name")
```

**Apply and verify:**

```bash
alembic upgrade head
alembic current   # Confirms: a1b2c3d4e5f6 (head)
```

### Example 2: Prisma Migrate — Adding a Reviews Model

**Request:** Add a `Review` model linked to `User` and `Product` in a Prisma project.

**Update `prisma/schema.prisma`:**

```prisma
model Review {
  id        Int      @id @default(autoincrement())
  rating    Int      @db.SmallInt
  comment   String?  @db.Text
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
  userId    Int
  productId Int
  user      User     @relation(fields: [userId], references: [id], onDelete: Cascade)
  product   Product  @relation(fields: [productId], references: [id], onDelete: Cascade)

  @@unique([userId, productId])
  @@index([productId])
  @@index([rating])
}
```

**Generate and apply the migration:**

```bash
npx prisma migrate dev --name add_reviews_table
```

**Generated SQL (`prisma/migrations/20250115_add_reviews_table/migration.sql`):**

```sql
CREATE TABLE "Review" (
    "id" SERIAL NOT NULL,
    "rating" SMALLINT NOT NULL,
    "comment" TEXT,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,
    "userId" INTEGER NOT NULL,
    "productId" INTEGER NOT NULL,
    CONSTRAINT "Review_pkey" PRIMARY KEY ("id")
);

CREATE INDEX "Review_productId_idx" ON "Review"("productId");
CREATE INDEX "Review_rating_idx" ON "Review"("rating");
CREATE UNIQUE INDEX "Review_userId_productId_key" ON "Review"("userId", "productId");
ALTER TABLE "Review" ADD CONSTRAINT "Review_userId_fkey"
    FOREIGN KEY ("userId") REFERENCES "User"("id") ON DELETE CASCADE;
ALTER TABLE "Review" ADD CONSTRAINT "Review_productId_fkey"
    FOREIGN KEY ("productId") REFERENCES "Product"("id") ON DELETE CASCADE;
```

## Best Practices

- **Always write explicit downgrade/rollback logic** for every migration so you can revert safely if the deployment causes issues. Never assume you can manually undo a migration under pressure.
- **Make migrations backward-compatible** by using expand-and-contract: add new structures first, then migrate data, then remove old structures in a separate migration after the new code is fully deployed.
- **Never run autogenerated migrations without review** — auto-detect tools may produce destructive operations (dropping columns) when they encounter renamed fields. Always inspect the generated SQL.
- **Use transactions for DDL** where supported (PostgreSQL wraps DDL in transactions; MySQL does not). For non-transactional DDL databases, plan for partial-failure recovery.
- **Keep migrations small and focused** — one logical change per migration file. This makes rollbacks granular and makes it easier to identify which migration caused a problem.
- **Run migrations in CI** against a disposable database to catch errors before they reach production. Include both upgrade and downgrade paths in the test.

## Edge Cases

- **Large table migrations:** Adding a NOT NULL column with a default to a table with millions of rows can lock the table for minutes in older PostgreSQL versions. Use `ADD COLUMN ... DEFAULT ... NOT NULL` (lock-free in PostgreSQL 11+) or add as nullable, backfill in batches, then set NOT NULL.
- **Renaming columns:** Most migration tools treat renames as a drop + add, which causes data loss. Use `op.alter_column()` in Alembic or raw `ALTER TABLE ... RENAME COLUMN` to perform a true rename. Verify the generated migration before applying.
- **Concurrent migrations:** In multi-instance deployments, ensure only one instance runs migrations. Use advisory locks (Flyway and Alembic support this) or a deployment pipeline that runs migrations as a dedicated step before rolling out application instances.
- **Enum type changes:** Adding values to a PostgreSQL enum is non-transactional. Create a new enum type, migrate the column, then drop the old type. Alternatively, use a VARCHAR with a CHECK constraint for easier modification.
- **Data-only migrations:** When you need to transform data without changing the schema (e.g., encrypting a column's values), still use a migration file to keep it versioned and reproducible across environments.
