---
name: alembic-migrations
description: Alembic migration patterns for SQLAlchemy 2.0 async. Use when creating database migrations, managing schema versions, handling zero-downtime deployments, or implementing reversible database changes.
context: fork
agent: database-engineer
version: 2.0.0
tags: [alembic, migrations, sqlalchemy, database, schema, python, async, 2026]
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob]
author: SkillForge
user-invocable: false
---

# Alembic Migration Patterns (2026)

Database migration management with Alembic for SQLAlchemy 2.0 async applications.

## When to Use

- Creating or modifying database tables and columns
- Auto-generating migrations from SQLAlchemy models
- Implementing zero-downtime schema changes
- Rolling back or managing migration history
- Adding indexes on large production tables
- Setting up Alembic with async PostgreSQL (asyncpg)

## Quick Reference

### Initialize Alembic (Async Template)

```bash
# Initialize with async template for asyncpg
alembic init -t async migrations

# Creates:
# - alembic.ini
# - migrations/env.py (async-ready)
# - migrations/script.py.mako
# - migrations/versions/
```

### Async env.py Configuration

```python
# migrations/env.py
import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

# Import your models' Base for autogenerate
from app.models.base import Base

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode - generates SQL."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()

async def run_async_migrations() -> None:
    """Run migrations in 'online' mode with async engine."""
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()

def run_migrations_online() -> None:
    """Entry point for online migrations."""
    asyncio.run(run_async_migrations())

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

### Migration Template

```python
"""Add users table.

Revision ID: abc123
Revises: None
Create Date: 2026-01-17 10:00:00.000000
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

revision = 'abc123'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index('idx_users_email', 'users', ['email'], unique=True)

def downgrade() -> None:
    op.drop_index('idx_users_email', table_name='users')
    op.drop_table('users')
```

### Autogenerate Migration

```bash
# Generate from model changes
alembic revision --autogenerate -m "add user preferences"

# Apply migrations
alembic upgrade head

# Rollback one step
alembic downgrade -1

# Generate SQL for review (production)
alembic upgrade head --sql > migration.sql

# Check current revision
alembic current

# Show migration history
alembic history --verbose
```

### Running Async Code in Migrations

```python
"""Migration with async operation.

NOTE: Alembic upgrade/downgrade cannot be async, but you can
run async code using sqlalchemy.util.await_only workaround.
"""
from alembic import op
from sqlalchemy import text
from sqlalchemy.util import await_only

def upgrade() -> None:
    # Get connection (works with async dialect)
    connection = op.get_bind()

    # For async-only operations, use await_only
    # This works because Alembic runs in greenlet context
    result = await_only(
        connection.execute(text("SELECT count(*) FROM users"))
    )

    # Standard operations work normally with async engine
    op.execute("""
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_users_org
        ON users (organization_id, created_at DESC)
    """)
```

### Concurrent Index (Zero-Downtime)

```python
def upgrade() -> None:
    # CONCURRENTLY avoids table locks on large tables
    # IMPORTANT: Cannot run inside transaction block
    op.execute("""
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_users_org
        ON users (organization_id, created_at DESC)
    """)

def downgrade() -> None:
    op.execute("DROP INDEX CONCURRENTLY IF EXISTS idx_users_org")

# In alembic.ini or env.py, disable transaction for this migration:
# Set transaction_per_migration = false for CONCURRENTLY operations
```

### Two-Phase NOT NULL Migration

```python
"""Add org_id column (phase 1 - nullable).

Phase 1: Add nullable column
Phase 2: Backfill data
Phase 3: Add NOT NULL (separate migration after verification)
"""

def upgrade() -> None:
    # Phase 1: Add as nullable first
    op.add_column('users', sa.Column('org_id', UUID(as_uuid=True), nullable=True))

    # Phase 2: Backfill with default org
    op.execute("""
        UPDATE users
        SET org_id = 'default-org-uuid'
        WHERE org_id IS NULL
    """)

    # Phase 3 in SEPARATE migration after app updated:
    # op.alter_column('users', 'org_id', nullable=False)

def downgrade() -> None:
    op.drop_column('users', 'org_id')
```

## Key Decisions

| Decision | Recommendation | Rationale |
|----------|----------------|-----------|
| Async dialect | Use `postgresql+asyncpg` | Native async support |
| NOT NULL column | Two-phase: nullable first, then alter | Avoids locking, backward compatible |
| Large table index | `CREATE INDEX CONCURRENTLY` | Zero-downtime, no table locks |
| Column rename | 4-phase expand/contract | Safe migration without downtime |
| Autogenerate review | Always review generated SQL | May miss custom constraints |
| Migration granularity | One logical change per file | Easier rollback and debugging |
| Production deployment | Generate SQL, review, then apply | Never auto-run in production |
| Downgrade function | Always implement properly | Ensures reversibility |
| Transaction mode | Default on, disable for CONCURRENTLY | CONCURRENTLY requires no transaction |

## Anti-Patterns (FORBIDDEN)

```python
# NEVER: Add NOT NULL without default or two-phase approach
op.add_column('users', sa.Column('org_id', UUID, nullable=False))  # LOCKS TABLE, FAILS!

# NEVER: Use blocking index creation on large tables
op.create_index('idx_large', 'big_table', ['col'])  # LOCKS TABLE - use CONCURRENTLY

# NEVER: Skip downgrade implementation
def downgrade():
    pass  # WRONG - implement proper rollback

# NEVER: Modify migration after deployment
# Create a new migration instead!

# NEVER: Run migrations automatically in production
# Use: alembic upgrade head --sql > review.sql

# NEVER: Use asyncio.run() in env.py if loop exists
# Already handled by async template, but check for FastAPI lifespan conflicts

# NEVER: Run CONCURRENTLY inside transaction
op.execute("BEGIN; CREATE INDEX CONCURRENTLY ...; COMMIT;")  # FAILS
```

## Alembic with FastAPI Lifespan

```python
# When running migrations during FastAPI startup (advanced)
# Issue: Event loop already running

# Solution 1: Run migrations before app starts (recommended)
# In entrypoint.sh:
# alembic upgrade head && uvicorn app.main:app

# Solution 2: Use run_sync for programmatic migrations
from sqlalchemy import Connection
from alembic import command
from alembic.config import Config

async def run_migrations(connection: Connection) -> None:
    """Run migrations programmatically within existing async context."""
    def do_upgrade(connection: Connection):
        config = Config("alembic.ini")
        config.attributes["connection"] = connection
        command.upgrade(config, "head")

    await connection.run_sync(do_upgrade)
```

## Related Skills

- `database-schema-designer` - Schema design and normalization patterns
- `database-versioning` - Version control and change management
- `zero-downtime-migration` - Expand/contract patterns for safe migrations
- `sqlalchemy-2-async` - Async SQLAlchemy session patterns
- `integration-testing` - Testing migrations with test databases

## Capability Details

### autogenerate-migrations
**Keywords:** autogenerate, auto-generate, revision, model sync, compare
**Solves:**
- Auto-generate migrations from SQLAlchemy models
- Sync database with model changes
- Detect schema drift

### revision-management
**Keywords:** upgrade, downgrade, rollback, history, current, revision
**Solves:**
- Apply or rollback migrations
- View migration history
- Check current database version

### zero-downtime-changes
**Keywords:** concurrent, expand contract, online migration, no downtime
**Solves:**
- Add indexes without locking
- Rename columns safely
- Large table migrations

### data-migration
**Keywords:** backfill, data migration, transform, batch update
**Solves:**
- Backfill new columns with data
- Transform existing data
- Migrate between column formats

### async-configuration
**Keywords:** asyncpg, async engine, env.py async, run_async_migrations
**Solves:**
- Configure Alembic for async SQLAlchemy
- Run migrations with asyncpg
- Handle existing event loop conflicts
