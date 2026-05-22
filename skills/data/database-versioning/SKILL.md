---
name: database-versioning
description: Database version control and change management patterns. Use when managing schema history, coordinating database changes across environments, implementing audit trails, or versioning database objects.
context: fork
agent: database-engineer
version: 1.0.0
tags: [database, versioning, schema, change-management, audit, 2026]
author: SkillForge
user-invocable: false
---

# Database Versioning Patterns

Version control strategies for database schemas and data across environments.

## Overview

- Tracking schema changes over time
- Coordinating database changes across dev/staging/prod
- Implementing database audit trails
- Managing stored procedures and functions
- Versioning reference data
- Blue-green database deployments

## Version Control Strategies

### Schema Versioning Table

```sql
-- Track schema version in the database itself
CREATE TABLE schema_version (
    version_id SERIAL PRIMARY KEY,
    version_number VARCHAR(20) NOT NULL,
    description TEXT NOT NULL,
    applied_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    applied_by VARCHAR(100),
    execution_time_ms INTEGER,
    checksum VARCHAR(64),

    CONSTRAINT uq_version_number UNIQUE (version_number)
);

-- Example entries
INSERT INTO schema_version (version_number, description, applied_by) VALUES
('1.0.0', 'Initial schema', 'deploy-bot'),
('1.1.0', 'Add user preferences table', 'deploy-bot'),
('1.2.0', 'Add audit columns to all tables', 'deploy-bot');
```

### Semantic Versioning for Databases

```
MAJOR.MINOR.PATCH

MAJOR: Breaking changes (drop tables, rename columns)
MINOR: Backward-compatible additions (new tables, nullable columns)
PATCH: Bug fixes, index changes, data migrations
```

### Migration Numbering Schemes

```
Option 1: Sequential
001_initial_schema.sql
002_add_users.sql
003_add_orders.sql

Option 2: Timestamp
20260115120000_initial_schema.sql
20260116143000_add_users.sql
20260117091500_add_orders.sql

Option 3: Hybrid (Date + Sequence)
2026_01_15_001_initial_schema.sql
2026_01_15_002_add_users.sql
2026_01_16_001_add_orders.sql
```

## Environment Coordination

### Multi-Environment Migration Flow

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Local     │───>│     CI      │───>│   Staging   │───>│ Production  │
│   (dev)     │    │   (test)    │    │   (preview) │    │   (live)    │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
       │                  │                  │                  │
       v                  v                  v                  v
   alembic            alembic           alembic            alembic
   upgrade            upgrade           upgrade            upgrade
    head               head              head               head
```

### Environment-Specific Migrations

```python
# alembic/env.py
import os

def run_migrations_online():
    env = os.getenv("ENVIRONMENT", "development")

    # Apply environment-specific settings
    if env == "production":
        # Use statement timeout for safety
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            transaction_per_migration=True,
            # Lock timeout for production
            postgresql_set_session_options={
                "statement_timeout": "30s",
                "lock_timeout": "10s"
            }
        )
    else:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )
```

### Migration Locks (Prevent Concurrent Migrations)

```python
"""Migration with advisory lock.

Prevents multiple instances from running migrations simultaneously.
"""
from alembic import op
from sqlalchemy import text

def upgrade():
    # Acquire advisory lock (blocks until available)
    op.execute(text("SELECT pg_advisory_lock(12345)"))

    try:
        # Run migration
        op.create_table('new_table', ...)
    finally:
        # Release lock
        op.execute(text("SELECT pg_advisory_unlock(12345)"))
```

## Audit Trail Patterns

### Row-Level Versioning

```sql
-- Versioned table with history
CREATE TABLE products (
    id UUID PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,

    -- Versioning columns
    version INTEGER NOT NULL DEFAULT 1,
    valid_from TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    valid_to TIMESTAMP WITH TIME ZONE,
    is_current BOOLEAN NOT NULL DEFAULT TRUE,

    -- Audit columns
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    created_by VARCHAR(100) NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE,
    updated_by VARCHAR(100)
);

-- Index for current records
CREATE INDEX idx_products_current ON products (id) WHERE is_current = TRUE;

-- Index for temporal queries
CREATE INDEX idx_products_temporal ON products (id, valid_from, valid_to);
```

### Temporal Tables (PostgreSQL 15+)

```sql
-- Enable temporal tables extension
CREATE EXTENSION IF NOT EXISTS temporal_tables;

-- Create temporal table
CREATE TABLE products (
    id UUID PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    sys_period TSTZRANGE NOT NULL DEFAULT tstzrange(NOW(), NULL)
);

-- History table
CREATE TABLE products_history (LIKE products);

-- Trigger for automatic versioning
CREATE TRIGGER versioning_trigger
BEFORE INSERT OR UPDATE OR DELETE ON products
FOR EACH ROW EXECUTE FUNCTION versioning(
    'sys_period', 'products_history', true
);

-- Query at a point in time
SELECT * FROM products
WHERE sys_period @> '2026-01-15 10:00:00+00'::timestamptz;
```

### Change Data Capture (CDC)

```sql
-- CDC table for tracking all changes
CREATE TABLE change_log (
    id BIGSERIAL PRIMARY KEY,
    table_name VARCHAR(100) NOT NULL,
    operation VARCHAR(10) NOT NULL, -- INSERT, UPDATE, DELETE
    record_id UUID NOT NULL,
    old_data JSONB,
    new_data JSONB,
    changed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    changed_by VARCHAR(100),
    transaction_id BIGINT DEFAULT txid_current()
);

-- Generic trigger function
CREATE OR REPLACE FUNCTION log_changes()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO change_log (table_name, operation, record_id, new_data, changed_by)
        VALUES (TG_TABLE_NAME, 'INSERT', NEW.id, to_jsonb(NEW), current_user);
        RETURN NEW;
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO change_log (table_name, operation, record_id, old_data, new_data, changed_by)
        VALUES (TG_TABLE_NAME, 'UPDATE', NEW.id, to_jsonb(OLD), to_jsonb(NEW), current_user);
        RETURN NEW;
    ELSIF TG_OP = 'DELETE' THEN
        INSERT INTO change_log (table_name, operation, record_id, old_data, changed_by)
        VALUES (TG_TABLE_NAME, 'DELETE', OLD.id, to_jsonb(OLD), current_user);
        RETURN OLD;
    END IF;
END;
$$ LANGUAGE plpgsql;

-- Apply to tables
CREATE TRIGGER products_audit
AFTER INSERT OR UPDATE OR DELETE ON products
FOR EACH ROW EXECUTE FUNCTION log_changes();
```

## Database Object Versioning

### Stored Procedure Versioning

```sql
-- Version tracking for stored procedures
CREATE TABLE procedure_versions (
    id SERIAL PRIMARY KEY,
    procedure_name VARCHAR(200) NOT NULL,
    version VARCHAR(20) NOT NULL,
    definition TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by VARCHAR(100),
    is_current BOOLEAN DEFAULT TRUE,

    CONSTRAINT uq_procedure_version UNIQUE (procedure_name, version)
);

-- Before updating a procedure, archive it
INSERT INTO procedure_versions (procedure_name, version, definition, created_by)
SELECT
    'calculate_order_total',
    '1.0.0',
    pg_get_functiondef(oid),
    current_user
FROM pg_proc
WHERE proname = 'calculate_order_total';
```

### View Versioning

```sql
-- Versioned views with _v1, _v2 naming
CREATE VIEW orders_summary_v1 AS
SELECT order_id, customer_id, total
FROM orders;

CREATE VIEW orders_summary_v2 AS
SELECT order_id, customer_id, total, shipping_cost, tax
FROM orders;

-- Current version alias
CREATE VIEW orders_summary AS
SELECT * FROM orders_summary_v2;
```

## Reference Data Versioning

```python
"""Reference data migration with versioning."""
from alembic import op
from sqlalchemy.sql import table, column
import sqlalchemy as sa

revision = 'ref001'

status_codes = table(
    'status_codes',
    column('code', sa.String),
    column('name', sa.String),
    column('description', sa.String),
    column('version', sa.Integer),
    column('is_active', sa.Boolean)
)


def upgrade():
    # Deactivate old version
    op.execute(
        status_codes.update()
        .where(status_codes.c.version == 1)
        .values(is_active=False)
    )

    # Insert new version
    op.bulk_insert(status_codes, [
        {'code': 'PENDING', 'name': 'Pending', 'description': 'Awaiting processing', 'version': 2, 'is_active': True},
        {'code': 'PROCESSING', 'name': 'Processing', 'description': 'Currently being processed', 'version': 2, 'is_active': True},
        {'code': 'COMPLETED', 'name': 'Completed', 'description': 'Successfully completed', 'version': 2, 'is_active': True},
        {'code': 'FAILED', 'name': 'Failed', 'description': 'Processing failed', 'version': 2, 'is_active': True},
    ])


def downgrade():
    op.execute(
        status_codes.delete()
        .where(status_codes.c.version == 2)
    )
    op.execute(
        status_codes.update()
        .where(status_codes.c.version == 1)
        .values(is_active=True)
    )
```

## Migration Testing

```python
# tests/test_migrations.py
import pytest
from alembic.config import Config
from alembic import command
from alembic.script import ScriptDirectory

@pytest.fixture
def alembic_config():
    return Config("alembic.ini")


def test_migrations_upgrade_downgrade(alembic_config, test_db):
    """Test all migrations can be applied and rolled back."""
    # Get all revisions
    script = ScriptDirectory.from_config(alembic_config)
    revisions = list(script.walk_revisions())

    # Apply all migrations
    command.upgrade(alembic_config, "head")

    # Downgrade all migrations
    command.downgrade(alembic_config, "base")

    # Verify clean state
    assert get_table_count(test_db) == 0


def test_migration_checksums(alembic_config):
    """Verify migrations haven't been modified after deployment."""
    script = ScriptDirectory.from_config(alembic_config)

    for revision in script.walk_revisions():
        if revision.revision in DEPLOYED_MIGRATIONS:
            current_checksum = calculate_checksum(revision.path)
            expected_checksum = DEPLOYED_MIGRATIONS[revision.revision]
            assert current_checksum == expected_checksum, \
                f"Migration {revision.revision} was modified after deployment!"
```

## Best Practices

| Practice | Reason |
|----------|--------|
| Version everything | Full traceability |
| Immutable history | Audit compliance |
| Test rollbacks | Ensure recoverability |
| Environment parity | Consistent deployments |
| Checksum verification | Detect unauthorized changes |

## Anti-Patterns

```python
# NEVER modify deployed migrations
# Instead: create new migration

# NEVER delete migration history
command.stamp(alembic_config, "head")  # Loses history

# NEVER skip environments
# Always: local -> CI -> staging -> production

# NEVER version sensitive data in migrations
op.bulk_insert(users, [{"password": "secret"}])  # Security risk!
```

## Related Skills

- `alembic-migrations` - Migration implementation
- `database-schema-designer` - Schema design
- `audit-trail-patterns` - Compliance logging

## Capability Details

### schema-versioning
**Keywords:** schema version, database version, migration history
**Solves:**
- Track schema changes
- Version history
- Schema metadata

### temporal-queries
**Keywords:** temporal, point-in-time, history query, as-of
**Solves:**
- Query historical data
- Temporal tables
- Time-travel queries

### change-tracking
**Keywords:** cdc, change data capture, audit log, change tracking
**Solves:**
- Track all changes
- Audit compliance
- Change history

### environment-sync
**Keywords:** environment sync, migration coordination, multi-env
**Solves:**
- Sync across environments
- Coordinate deployments
- Environment consistency
