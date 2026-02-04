---
name: database-migration
description: Database schema migration patterns for Aurora MySQL including reconciliation migrations, idempotent operations, and MySQL-specific gotchas.
---

# Database Migration Skill

**Tech Stack**: Aurora MySQL 8.0, PyMySQL, migrations via Python scripts

**Source**: Extracted from CLAUDE.md database migration principles and real migration failures.

---

## When to Use This Skill

Use the database-migration skill when:
- ✓ Creating new database migrations
- ✓ Fixing broken migrations in unknown state
- ✓ Debugging schema mismatch issues
- ✓ Reviewing migration PRs
- ✓ Reconciling production schema drift

**DO NOT use this skill for:**
- ✗ Query optimization (use code-review PERFORMANCE.md)
- ✗ Data migrations (this skill is schema-only)
- ✗ NoSQL databases (DynamoDB has different patterns)

---

## Quick Decision Tree

```
What's the migration scenario?

├─ New feature schema?
│  ├─ Dev database clean? → Sequential migration (001_add_feature.sql)
│  └─ Dev database dirty? → Reconciliation migration (RECONCILE_*.sql)
│
├─ Production schema drift?
│  └─ Always → Reconciliation migration (idempotent operations)
│
├─ Migration failed mid-execution?
│  ├─ Can rollback? → Rollback, fix migration, re-run
│  └─ Cannot rollback? → Reconciliation migration to fix state
│
└─ Schema review before merge?
   └─ Check: RECONCILIATION-MIGRATIONS.md + MYSQL-GOTCHAS.md
```

---

## Core Migration Principles

### Principle 1: Immutability of Committed Migrations

**From CLAUDE.md:**
> "Migration files are immutable once committed to version control—never edit them, always create new migrations for schema changes."

**Why This Matters:**
- Reproducibility: Same migration file produces same schema across all environments
- History: Preserves evolution of schema over time
- Multi-developer: Prevents conflicts when multiple people migrate simultaneously

```python
# ❌ DON'T: Edit existing migration
# migrations/001_create_users.sql (committed 2 weeks ago)
CREATE TABLE users (
    id INT PRIMARY KEY,
    name VARCHAR(100)  # Changed from VARCHAR(50) → Breaks reproducibility!
);

# ✅ DO: Create new migration
# migrations/002_widen_user_name.sql
ALTER TABLE users MODIFY COLUMN name VARCHAR(100);
```

**Exceptions:**
- Migration not yet committed to version control → Can edit freely
- Migration failed in dev environment → Can delete and recreate
- Migration never ran in production → Can edit if also updating all dev environments

---

### Principle 2: Reconciliation Over Sequential Migrations

**Pattern:** When database state is unknown or partially migrated, use reconciliation migrations.

**Sequential Migration Assumption:**
```sql
-- migrations/003_add_status_column.sql
-- Assumes: users table exists AND status column doesn't exist
ALTER TABLE users ADD COLUMN status ENUM('active', 'inactive');
```

**Problem:** If migration ran before on some servers but not others, you get:
- Already has column → Error: "Duplicate column name 'status'"
- Doesn't have column → Success
- Unknown state → 50/50 chance of failure

**Reconciliation Migration Solution:**
```sql
-- migrations/RECONCILE_user_status.sql
-- Works regardless of current state
CREATE TABLE IF NOT EXISTS users (
    id INT PRIMARY KEY,
    name VARCHAR(100)
);

-- Add column only if missing
SET @col_exists = (
    SELECT COUNT(*)
    FROM information_schema.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE()
      AND TABLE_NAME = 'users'
      AND COLUMN_NAME = 'status'
);

SET @sql = IF(@col_exists = 0,
    'ALTER TABLE users ADD COLUMN status ENUM("active", "inactive")',
    'SELECT "Column status already exists" AS message'
);

PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;
```

**When to Use:**
- Production schema drift (someone manually altered schema)
- Migration failed mid-execution (half the changes applied)
- Multiple environments out of sync
- After fixing a broken migration

See [RECONCILIATION-MIGRATIONS.md](RECONCILIATION-MIGRATIONS.md) for detailed patterns.

---

### Principle 3: Verify Schema After Migration

**Pattern:** Always verify migrations changed what you expected.

```bash
# After running migration
mysql> DESCRIBE users;
+--------+--------------------------+------+-----+---------+-------+
| Field  | Type                     | Null | Key | Default | Extra |
+--------+--------------------------+------+-----+---------+-------+
| id     | int                      | NO   | PRI | NULL    |       |
| name   | varchar(100)             | YES  |     | NULL    |       |
| status | enum('active','inactive')| YES  |     | NULL    |       |
+--------+--------------------------+------+-----+---------+-------+

# Verify:
# ✓ status column exists
# ✓ ENUM values correct
# ✓ Nullable (or NOT NULL if intended)
```

**Why This Matters:** MySQL's idempotent operations can silently skip changes:

- `CREATE TABLE IF NOT EXISTS` → Skips if table exists with **different** schema
- `ALTER TABLE MODIFY COLUMN` → Changes type but **not existing data**

See [MYSQL-GOTCHAS.md](MYSQL-GOTCHAS.md) for detailed MySQL-specific issues.

---

### Principle 4: Add Column Comments to Prevent Semantic Confusion

**Pattern:** Use MySQL's native `COMMENT` syntax to document column semantics directly in the database schema.

**Problem:** Column names alone can be semantically ambiguous:
```sql
-- What does "date" mean?
CREATE TABLE ticker_data (
    date DATE NOT NULL  -- Is this fetch date? Trading date? Calendar date?
);
```

**Real Bug Example (2025-12-29):**
- User queried `WHERE date = '2025-12-29'` expecting "today's data"
- Got 0 results because `date` represents **trading date** (market close), NOT fetch date
- Data for Dec 29 won't exist until Dec 30 5:00 AM Bangkok (19-hour gap)
- Root cause: Semantic confusion about what "date" field represents

**Solution:** Add `COLUMN COMMENT` to clarify semantics:
```sql
ALTER TABLE ticker_data
MODIFY COLUMN date DATE NOT NULL
COMMENT 'Trading date for stock market data (NOT fetch date). Represents the date when market closed, not when data was retrieved. Data for date D is fetched at 5:00 AM Bangkok on date D+1.';

ALTER TABLE ticker_data
MODIFY COLUMN fetched_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
COMMENT 'UTC timestamp when this data was fetched from Yahoo Finance API. Compare with date field to understand data age.';
```

**When to Add Comments:**
1. **Date/timestamp columns** (highest confusion risk):
   - Clarify what the date represents (trading date vs fetch date vs calendar date)
   - Document timezone semantics (UTC vs local time)
   - Explain time windows when data won't exist yet

2. **JSON columns** (structure documentation):
   - Document expected schema: `{date, open, high, low, close, volume}`
   - List required vs optional fields

3. **Enum-like VARCHAR columns** (valid values):
   - Document valid values: `'pending', 'in_progress', 'completed', 'failed'`

4. **Foreign key columns** (relationship clarity):
   - Document what they reference: `'References ticker_master.id'`

**Querying Column Comments:**
```sql
-- Get all comments for a table
SELECT COLUMN_NAME, DATA_TYPE, COLUMN_COMMENT
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = DATABASE()
  AND TABLE_NAME = 'ticker_data'
ORDER BY ORDINAL_POSITION;

-- Find uncommented date/timestamp columns (needs attention)
SELECT TABLE_NAME, COLUMN_NAME
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = DATABASE()
  AND DATA_TYPE IN ('date', 'timestamp')
  AND (COLUMN_COMMENT IS NULL OR COLUMN_COMMENT = '');
```

**Migration Pattern:**
```sql
-- Migration 016: Add semantic comments to prevent date field confusion
ALTER TABLE ticker_data
MODIFY COLUMN date DATE NOT NULL
COMMENT 'Trading date for stock market data (NOT fetch date). Represents the date when market closed, not when data was retrieved. Data for date D is fetched at 5:00 AM Bangkok on date D+1.';

-- Always preserve existing column definition (type, constraints, defaults)
-- when adding comments - use MODIFY COLUMN with full definition
```

**Benefits:**
- Self-documenting database (no separate docs needed)
- Queryable via `INFORMATION_SCHEMA.COLUMNS`
- Zero performance impact (comments are metadata only)
- Version-controlled via migration files
- Prevents semantic misinterpretation bugs

**Cost:** Zero (comments are metadata, don't affect queries or storage)

See migration `db/migrations/016_add_semantic_comments.sql` for real example.

---

## Migration Workflow

### 1. Development Migration

```bash
# Step 1: Create migration file
cat > migrations/004_add_email_to_users.sql <<'EOF'
-- Add email column to users table
ALTER TABLE users ADD COLUMN email VARCHAR(255);
ALTER TABLE users ADD INDEX idx_email (email);
EOF

# Step 2: Test locally (requires Aurora tunnel)
# Verify tunnel active
ss -ltn | grep 3307

# Run migration
mysql -h localhost -P 3307 -u admin -p < migrations/004_add_email_to_users.sql

# Step 3: Verify schema
mysql -h localhost -P 3307 -u admin -p -e "DESCRIBE users;"
mysql -h localhost -P 3307 -u admin -p -e "SHOW INDEX FROM users;"

# Step 4: Commit migration
git add migrations/004_add_email_to_users.sql
git commit -m "db: Add email column to users table"
```

---

### 2. Production Migration (Reconciliation Pattern)

```bash
# Step 1: Check current production schema
# (via Aurora tunnel to production)
mysql -h localhost -P 3307 -u admin -p -e "DESCRIBE users;"

# Step 2: Create reconciliation migration
cat > migrations/RECONCILE_user_email.sql <<'EOF'
-- Reconciliation: Add email to users (idempotent)

-- Check if email column exists
SET @col_exists = (
    SELECT COUNT(*)
    FROM information_schema.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE()
      AND TABLE_NAME = 'users'
      AND COLUMN_NAME = 'email'
);

-- Add column if missing
SET @add_column = IF(@col_exists = 0,
    'ALTER TABLE users ADD COLUMN email VARCHAR(255)',
    'SELECT "Column email already exists"'
);

PREPARE stmt FROM @add_column;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Check if index exists
SET @idx_exists = (
    SELECT COUNT(*)
    FROM information_schema.STATISTICS
    WHERE TABLE_SCHEMA = DATABASE()
      AND TABLE_NAME = 'users'
      AND INDEX_NAME = 'idx_email'
);

-- Add index if missing
SET @add_index = IF(@idx_exists = 0,
    'ALTER TABLE users ADD INDEX idx_email (email)',
    'SELECT "Index idx_email already exists"'
);

PREPARE stmt FROM @add_index;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;
EOF

# Step 3: Run reconciliation migration
mysql -h localhost -P 3307 -u admin -p < migrations/RECONCILE_user_email.sql

# Step 4: Verify final state
scripts/verify_schema.py --table users --expected-columns id,name,status,email
```

---

### 3. Fixing Broken Migrations

**Scenario:** Migration failed mid-execution, database in unknown state.

```bash
# Step 1: Check what exists
mysql -h localhost -P 3307 -u admin -p <<'EOF'
SHOW TABLES;
DESCRIBE users;  -- Check which columns exist
SHOW INDEX FROM users;  -- Check which indexes exist
EOF

# Step 2: Create reconciliation migration to finish job
# (See RECONCILIATION-MIGRATIONS.md for patterns)

# Step 3: Mark old migration as obsolete (if needed)
mv migrations/004_add_email_to_users.sql migrations/OBSOLETE_004_add_email_to_users.sql

# Step 4: Commit reconciliation migration
git add migrations/RECONCILE_user_email.sql
git commit -m "db: Reconcile user email migration (fixes broken 004)"
```

---

## Migration File Naming Convention

```
migrations/
├── 001_create_users.sql              # Sequential: New feature
├── 002_add_status_to_users.sql       # Sequential: Follow-up
├── RECONCILE_user_status.sql         # Reconciliation: Fix drift
├── OBSOLETE_003_broken_migration.sql # Mark broken migrations
└── README.md                         # Migration history
```

**Rules:**
- **Sequential (001, 002, ...)**: For clean dev environments, new features
- **RECONCILE_**: For unknown state, production drift, fixing failures
- **OBSOLETE_**: Mark failed migrations (don't delete - preserve history)

---

## Common Migration Patterns

### Pattern 1: Add Column

```sql
-- Sequential (clean state)
ALTER TABLE users ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

-- Reconciliation (unknown state)
SET @col_exists = (
    SELECT COUNT(*)
    FROM information_schema.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE()
      AND TABLE_NAME = 'users'
      AND COLUMN_NAME = 'created_at'
);

SET @sql = IF(@col_exists = 0,
    'ALTER TABLE users ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP',
    'SELECT "Column created_at already exists"'
);

PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;
```

---

### Pattern 2: Add Index

```sql
-- Sequential
CREATE INDEX idx_email ON users(email);

-- Reconciliation
SET @idx_exists = (
    SELECT COUNT(*)
    FROM information_schema.STATISTICS
    WHERE TABLE_SCHEMA = DATABASE()
      AND TABLE_NAME = 'users'
      AND INDEX_NAME = 'idx_email'
);

SET @sql = IF(@idx_exists = 0,
    'CREATE INDEX idx_email ON users(email)',
    'SELECT "Index idx_email already exists"'
);

PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;
```

---

### Pattern 3: Modify Column Type

```sql
-- Sequential
ALTER TABLE users MODIFY COLUMN name VARCHAR(200);

-- Reconciliation
-- Note: MODIFY COLUMN changes type but not existing data!
SET @current_type = (
    SELECT COLUMN_TYPE
    FROM information_schema.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE()
      AND TABLE_NAME = 'users'
      AND COLUMN_NAME = 'name'
);

-- Only modify if type is different
SET @sql = IF(@current_type != 'varchar(200)',
    'ALTER TABLE users MODIFY COLUMN name VARCHAR(200)',
    'SELECT "Column name already VARCHAR(200)"'
);

PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- CRITICAL: Verify existing data fits new type
SELECT name FROM users WHERE LENGTH(name) > 200;
```

See [RECONCILIATION-MIGRATIONS.md](RECONCILIATION-MIGRATIONS.md) for more patterns.

---

## Migration Review Checklist

Before merging migration PR, verify:

### Correctness
- [ ] Migration tested locally (via Aurora tunnel)
- [ ] Schema verified with `DESCRIBE table_name`
- [ ] Indexes verified with `SHOW INDEX FROM table_name`
- [ ] Migration is idempotent (can run multiple times safely)

### Safety
- [ ] No `DROP TABLE` without backup strategy
- [ ] No `ALTER TABLE MODIFY COLUMN` that truncates data
- [ ] No `DELETE` without `WHERE` clause
- [ ] Large tables: Migration uses `ALGORITHM=INPLACE` (no table lock)

### Documentation
- [ ] Migration file has descriptive comment
- [ ] Breaking changes documented in PR description
- [ ] Migration history updated (if complex change)

### MySQL-Specific
- [ ] ENUM values validated (see MYSQL-GOTCHAS.md)
- [ ] Foreign key constraints checked
- [ ] Character set/collation compatible
- [ ] Nullable vs NOT NULL explicit

---

## Testing Migrations

### Unit Test Pattern

```python
import pytest
import pymysql

class TestUserEmailMigration:
    """Test 004_add_email_to_users.sql migration"""

    def setup_method(self):
        """Create clean test database"""
        self.conn = pymysql.connect(
            host='localhost',
            port=3307,
            user='admin',
            password='...',
            database='test_db'
        )
        # Run prerequisite migrations
        self._run_migration('001_create_users.sql')

    def test_migration_adds_email_column(self):
        """Verify migration adds email column"""
        # Run migration
        self._run_migration('004_add_email_to_users.sql')

        # Verify column exists
        with self.conn.cursor() as cursor:
            cursor.execute("DESCRIBE users")
            columns = {row[0]: row for row in cursor.fetchall()}

        assert 'email' in columns
        assert columns['email'][1] == 'varchar(255)'  # Type

    def test_migration_is_idempotent(self):
        """Verify migration can run multiple times"""
        # Run twice
        self._run_migration('004_add_email_to_users.sql')
        self._run_migration('004_add_email_to_users.sql')  # Should not error

        # Verify column exists (not duplicated)
        with self.conn.cursor() as cursor:
            cursor.execute("DESCRIBE users")
            columns = [row[0] for row in cursor.fetchall()]

        assert columns.count('email') == 1

    def _run_migration(self, filename):
        """Helper: Run migration file"""
        with open(f'migrations/{filename}') as f:
            sql = f.read()
        with self.conn.cursor() as cursor:
            for statement in sql.split(';'):
                if statement.strip():
                    cursor.execute(statement)
        self.conn.commit()
```

---

### Integration Test (Production-like)

```python
@pytest.mark.integration
def test_reconcile_user_email_migration_on_dirty_db():
    """Test reconciliation migration handles partial state"""

    # Setup: Create users table WITHOUT email (partial migration)
    conn.cursor().execute("CREATE TABLE users (id INT PRIMARY KEY, name VARCHAR(100))")

    # Run reconciliation migration
    run_migration('RECONCILE_user_email.sql')

    # Verify: email column added
    cursor.execute("DESCRIBE users")
    columns = {row[0] for row in cursor.fetchall()}
    assert 'email' in columns

    # Run again (should not error)
    run_migration('RECONCILE_user_email.sql')

    # Verify: still works
    cursor.execute("DESCRIBE users")
    columns = {row[0] for row in cursor.fetchall()}
    assert 'email' in columns
```

---

## Quick Reference

### When to Use Sequential vs Reconciliation

| Scenario | Migration Type | Example |
|----------|----------------|---------|
| **New feature (clean dev)** | Sequential | `001_add_feature.sql` |
| **Production deployment** | Reconciliation | `RECONCILE_feature.sql` |
| **Schema drift** | Reconciliation | `RECONCILE_fix_drift.sql` |
| **Failed migration** | Reconciliation | `RECONCILE_fix_migration.sql` |
| **Multi-environment sync** | Reconciliation | `RECONCILE_sync_envs.sql` |

### Migration Safety Levels

| Operation | Risk | Mitigation |
|-----------|------|------------|
| **ADD COLUMN** | Low | Use DEFAULT for NOT NULL columns |
| **DROP COLUMN** | High | Verify column unused first |
| **MODIFY COLUMN** | Medium | Check existing data compatibility |
| **ADD INDEX** | Low | Use `ALGORITHM=INPLACE` for large tables |
| **DROP INDEX** | Medium | Verify queries don't need it |
| **ADD FK** | Medium | Verify referential integrity first |

---

## Troubleshooting

### Error: "Duplicate column name 'email'"

**Cause:** Column already exists (migration ran before or schema drift).

**Solution:** Use reconciliation migration with conditional logic.

---

### Error: "Data truncated for column 'status'"

**Cause:** Existing data doesn't fit new ENUM values or column type.

**Solution:**
```sql
-- Check existing data first
SELECT DISTINCT status FROM users;

-- If incompatible, migrate data before changing type
UPDATE users SET status = 'active' WHERE status IS NULL;

-- Then change type
ALTER TABLE users MODIFY COLUMN status ENUM('active', 'inactive') NOT NULL;
```

---

### Migration Ran But Schema Unchanged

**Cause:** `CREATE TABLE IF NOT EXISTS` skipped because table exists with different schema.

**Solution:** Use `ALTER TABLE` for existing tables, not `CREATE TABLE IF NOT EXISTS`.

See [MYSQL-GOTCHAS.md](MYSQL-GOTCHAS.md) for comprehensive troubleshooting.

---

## File Organization

```
.claude/skills/database-migration/
├── SKILL.md                      # This file (entry point)
├── RECONCILIATION-MIGRATIONS.md  # Idempotent migration patterns
├── MYSQL-GOTCHAS.md              # MySQL-specific issues
└── scripts/
    └── verify_schema.py          # Schema verification tool
```

---

## Next Steps

- **For reconciliation patterns**: See [RECONCILIATION-MIGRATIONS.md](RECONCILIATION-MIGRATIONS.md)
- **For MySQL gotchas**: See [MYSQL-GOTCHAS.md](MYSQL-GOTCHAS.md)
- **For schema verification**: Run `scripts/verify_schema.py`

---

## References

- [MySQL ALTER TABLE Documentation](https://dev.mysql.com/doc/refman/8.0/en/alter-table.html)
- [Database Migrations Done Right](https://www.brunton-spall.co.uk/post/2014/05/06/database-migrations-done-right/)
- [Zero-Downtime Migrations](https://github.com/github/gh-ost)
