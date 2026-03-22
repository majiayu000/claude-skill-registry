---
name: database-migrations
description: Create and manage database migrations safely. Covers SQL migrations, ORM migrations (Prisma, TypeORM, Flyway, Alembic), rollback strategies, and zero-downtime migration patterns.
allowed-tools: Read, Write, Bash, Glob, Grep
---

# Database Migrations

Create safe, reversible database migrations.

## Detect Migration Tool

```bash
ls prisma/schema.prisma migrations/ db/migrate/ alembic.ini flyway.conf src/main/resources/db/migration/ 2>/dev/null
```

## Universal Migration Rules

1. **Always reversible** — every migration must have an `up()` and `down()`
2. **Never delete data** in a migration (archive first, delete later)
3. **One change per migration** — don't bundle multiple schema changes
4. **Test on a copy first** — never run untested migration on production
5. **Backup before running** on production

## SQL Migration Pattern

```sql
-- V001__create_users_table.sql (Flyway naming)
-- or 001_create_users.up.sql

-- UP
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);

-- DOWN (in separate file or section)
DROP TABLE IF EXISTS users;
```

## Zero-Downtime Column Add

```sql
-- ✅ Safe: adding nullable column
ALTER TABLE users ADD COLUMN display_name VARCHAR(100);

-- ✅ Safe: adding column with default (new rows get default)
ALTER TABLE users ADD COLUMN is_active BOOLEAN NOT NULL DEFAULT true;

-- ❌ Dangerous: adding NOT NULL column without default (locks table)
ALTER TABLE users ADD COLUMN required_field VARCHAR(100) NOT NULL;
-- Instead: add nullable → backfill → add NOT NULL constraint
```

## Zero-Downtime Column Rename (3 migrations)

```sql
-- Migration 1: Add new column
ALTER TABLE users ADD COLUMN user_name VARCHAR(100);

-- Migration 2 (after deploy): Copy data + update app to write both
UPDATE users SET user_name = username;

-- Migration 3 (after next deploy): Drop old column
ALTER TABLE users DROP COLUMN username;
```

## Prisma (TypeScript)

```bash
# Create migration
npx prisma migrate dev --name add_user_avatar

# Apply to production
npx prisma migrate deploy

# Rollback (manual — Prisma doesn't auto-rollback)
# Keep manual rollback SQL in migrations/rollbacks/
```

```prisma
// schema.prisma
model User {
  id        String   @id @default(cuid())
  email     String   @unique
  avatar    String?  // ← new nullable field (safe)
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
}
```

## Alembic (Python)

```python
# alembic/versions/001_add_avatar.py
def upgrade():
    op.add_column("users", sa.Column("avatar", sa.String(255), nullable=True))

def downgrade():
    op.drop_column("users", "avatar")
```

## Flyway (Java/Spring Boot)

```sql
-- src/main/resources/db/migration/V002__add_user_avatar.sql
ALTER TABLE users ADD COLUMN avatar VARCHAR(255);

-- src/main/resources/db/migration/V002__add_user_avatar__undo.sql (for Flyway Teams)
ALTER TABLE users DROP COLUMN avatar;
```

## Migration Checklist

Before running any migration:
- [ ] Migration has both up and down operations
- [ ] Tested on development database first
- [ ] Large table migrations tested for lock duration
- [ ] Database backup taken (production)
- [ ] Rollback plan documented
- [ ] Zero-downtime pattern used for live tables

## Usage

```
/database-migrations add-column users avatar
/database-migrations create-table orders
/database-migrations rename-column users username user_name
/database-migrations zero-downtime    # for high-traffic tables
```
