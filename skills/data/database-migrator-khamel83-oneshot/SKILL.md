---
name: database-migrator
description: "Handle schema changes and data migrations safely. Creates migration files with rollback plans. Use when user says 'migration', 'schema change', 'add column', 'database change', or 'alter table'."
allowed-tools: Bash, Read, Write, Edit
---

# Database Migrator

You are an expert at handling database schema changes safely.

## When To Use

- Adding/removing/modifying database columns
- Creating new tables
- Data transformations needed
- User says "Add this field", "Change the schema"

## Inputs

- Current schema
- Desired change
- Data preservation requirements

## Outputs

- Migration file(s)
- Rollback strategy
- Updated schema documentation

## Workflow

### 1. Analyze Change

- Is this additive (safe) or destructive (risky)?
- Any data to preserve or transform?
- Downtime required?

### 2. Generate Migration

```bash
# Alembic (Python)
alembic revision --autogenerate -m "add user preferences"

# Prisma
npx prisma migrate dev --name add_preferences

# Raw SQL
# Create timestamped file: migrations/20241206_add_preferences.sql
```

### 3. Review Migration

- Check generated SQL
- Verify rollback works
- Consider indexes

### 4. Test Locally

```bash
# Apply
alembic upgrade head

# Rollback
alembic downgrade -1
```

### 5. Document

- Update ERD if exists
- Note in LLM-OVERVIEW.md

## Safe Migration Patterns

| Change | Safe? | Notes |
|--------|-------|-------|
| Add nullable column | ✅ | No data change needed |
| Add column with default | ✅ | Backfills automatically |
| Remove unused column | ⚠️ | Verify no code references |
| Rename column | ❌ | Requires code coordination |
| Change column type | ❌ | May lose data |
| Add index | ✅ | May lock table briefly |
| Add foreign key | ⚠️ | Existing data must be valid |

## Migration Templates

### SQLite

```sql
-- migrations/001_add_preferences.sql

-- Up
ALTER TABLE users ADD COLUMN preferences TEXT;

-- Down
-- SQLite doesn't support DROP COLUMN easily
-- Create new table without column, copy data, rename
```

### PostgreSQL

```sql
-- migrations/001_add_preferences.sql

-- Up
ALTER TABLE users ADD COLUMN preferences JSONB DEFAULT '{}';

-- Down
ALTER TABLE users DROP COLUMN preferences;
```

### Alembic (Python)

```python
"""add preferences column

Revision ID: abc123
"""
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column('users',
        sa.Column('preferences', sa.JSON(), nullable=True)
    )

def downgrade():
    op.drop_column('users', 'preferences')
```

## Zero-Downtime Patterns

### Adding Column

1. Add column (nullable)
2. Deploy code that writes to new column
3. Backfill existing data
4. Add NOT NULL constraint (if needed)

### Renaming Column

1. Add new column
2. Deploy code that writes to both
3. Backfill old → new
4. Deploy code that reads from new
5. Drop old column

## Rollback Strategy

Always have a plan:

```yaml
migration: add_preferences
rollback:
  command: "alembic downgrade -1"
  data_loss: false
  downtime: "~30 seconds"
  tested: true
```

---

## NoSQL Migrations

### MongoDB Schema Evolution

Unlike SQL, MongoDB is schema-less but you still need to manage document structure changes.

#### Adding a Field

```javascript
// No migration needed for new fields - just start writing them
// Optional: backfill existing documents
db.users.updateMany(
  { preferences: { $exists: false } },
  { $set: { preferences: {} } }
);
```

#### Renaming a Field

```javascript
// 1. Add new field, copy data
db.users.updateMany(
  {},
  [{ $set: { newName: "$oldName" } }]
);

// 2. Update code to use newName

// 3. Remove old field
db.users.updateMany(
  {},
  { $unset: { oldName: "" } }
);
```

#### Changing Field Type

```javascript
// String to Number
db.users.updateMany(
  {},
  [{ $set: { age: { $toInt: "$age" } } }]
);

// Nested object to flat
db.users.updateMany(
  {},
  [{
    $set: {
      city: "$address.city",
      country: "$address.country"
    },
    $unset: "address"
  }]
);
```

### MongoDB Migration Script Template

```javascript
// migrations/001_add_preferences.js
module.exports = {
  async up(db) {
    await db.collection('users').updateMany(
      { preferences: { $exists: false } },
      { $set: { preferences: { theme: 'light', notifications: true } } }
    );
  },

  async down(db) {
    await db.collection('users').updateMany(
      {},
      { $unset: { preferences: "" } }
    );
  }
};
```

### Redis Data Evolution

Redis doesn't have migrations per se, but key naming and data structure changes need planning.

#### Key Naming Convention

```
# Good: namespace:entity:id:attribute
user:123:profile
user:123:sessions
cache:products:list

# Bad: no structure
user_profile_123
```

#### Changing Key Structure

```python
# Migrate from old to new key format
import redis
r = redis.Redis()

# 1. Copy data to new keys
for key in r.scan_iter("user_*"):
    user_id = key.decode().split("_")[1]
    new_key = f"user:{user_id}:profile"
    r.copy(key, new_key)

# 2. Update code to use new keys
# 3. Delete old keys (after verification)
for key in r.scan_iter("user_*"):
    r.delete(key)
```

### When SQL vs NoSQL

| Factor | Use SQL | Use NoSQL |
|--------|---------|-----------|
| Schema | Fixed, well-known | Flexible, evolving |
| Relationships | Many, complex | Few, embedded |
| Transactions | Critical | Nice to have |
| Scale | Vertical first | Horizontal first |
| Query patterns | Complex joins | Key-value, document |
| Data size | <100GB | Any size |

**Default to SQL (SQLite → PostgreSQL)** unless you have specific NoSQL needs.

---

## Anti-Patterns

- Migrations without rollback plan
- Destructive changes without backup
- Long-running migrations during peak hours
- Not testing migrations locally first
- Combining multiple changes in one migration
- MongoDB: Not validating document structure
- Redis: Not using key namespaces

## Keywords

migration, schema change, add column, database, alter table, alembic, prisma, mongodb, redis, nosql
