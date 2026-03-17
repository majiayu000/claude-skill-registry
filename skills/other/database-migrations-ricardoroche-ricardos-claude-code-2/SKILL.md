---
name: database-migrations
description: Automatically applies when working with database migrations. Ensures proper Alembic patterns, upgrade/downgrade scripts, data migrations, rollback safety, and migration testing.
category: python
---

# Database Migration Patterns

When managing database migrations, follow these patterns for safe, reversible schema changes.

**Trigger Keywords**: migration, alembic, database schema, upgrade, downgrade, migrate, schema change, DDL, database version, revision

**Agent Integration**: Used by `backend-architect`, `database-engineer`, `data-engineer`

## ✅ Correct Pattern: Alembic Setup

```python
# alembic/env.py
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from app.models import Base  # Import your models
from app.config import settings

# Alembic Config object
config = context.config

# Configure logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set target metadata
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine.
    """
    url = settings.database_url
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,  # Detect column type changes
        compare_server_default=True  # Detect default changes
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """
    Run migrations in 'online' mode.

    Creates an Engine and associates a connection with the context.
    """
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = settings.database_url

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

## Create Migration

```python
"""
Create migration with proper naming and structure.

Command:
    alembic revision --autogenerate -m "add_user_email_index"

Revision ID: abc123
Revises: xyz456
Create Date: 2025-01-15 10:30:00
"""
from alembic import op
import sqlalchemy as sa
from typing import Sequence, Union

# revision identifiers
revision: str = 'abc123'
down_revision: Union[str, None] = 'xyz456'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    Apply migration.

    Add index on users.email for faster lookups.
    """
    op.create_index(
        'ix_users_email',
        'users',
        ['email'],
        unique=False
    )


def downgrade() -> None:
    """
    Revert migration.

    Remove index on users.email.
    """
    op.drop_index('ix_users_email', table_name='users')
```

## Safe Column Additions

```python
"""Add user phone number column"""
from alembic import op
import sqlalchemy as sa


def upgrade() -> None:
    """Add phone column with nullable default."""
    # Add column as nullable first
    op.add_column(
        'users',
        sa.Column(
            'phone',
            sa.String(20),
            nullable=True  # Start nullable!
        )
    )

    # Optionally set default value for existing rows
    op.execute(
        """
        UPDATE users
        SET phone = ''
        WHERE phone IS NULL
        """
    )

    # Then make NOT NULL if needed (separate migration recommended)
    # op.alter_column('users', 'phone', nullable=False)


def downgrade() -> None:
    """Remove phone column."""
    op.drop_column('users', 'phone')
```

## Safe Column Modifications

```python
"""Increase email column length"""
from alembic import op
import sqlalchemy as sa


def upgrade() -> None:
    """
    Increase email length from 255 to 500.

    Safe for PostgreSQL (no table rewrite).
    """
    # Check constraints first
    with op.batch_alter_table('users') as batch_op:
        batch_op.alter_column(
            'email',
            type_=sa.String(500),
            existing_type=sa.String(255),
            existing_nullable=False
        )


def downgrade() -> None:
    """
    Decrease email length back to 255.

    WARNING: May fail if existing data exceeds 255 chars.
    """
    # Check for data that would be truncated
    op.execute(
        """
        SELECT COUNT(*)
        FROM users
        WHERE LENGTH(email) > 255
        """
    )

    with op.batch_alter_table('users') as batch_op:
        batch_op.alter_column(
            'email',
            type_=sa.String(255),
            existing_type=sa.String(500),
            existing_nullable=False
        )
```

## Data Migration

```python
"""Migrate user status enum values"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import text


def upgrade() -> None:
    """
    Migrate status from 'active'/'inactive' to 'enabled'/'disabled'.

    Two-phase approach:
    1. Add new column
    2. Migrate data
    3. Drop old column (in next migration)
    """
    # Phase 1: Add new column
    op.add_column(
        'users',
        sa.Column(
            'account_status',
            sa.Enum('enabled', 'disabled', 'suspended', name='account_status'),
            nullable=True
        )
    )

    # Phase 2: Migrate data
    connection = op.get_bind()

    # Map old values to new values
    connection.execute(
        text("""
            UPDATE users
            SET account_status = CASE
                WHEN status = 'active' THEN 'enabled'
                WHEN status = 'inactive' THEN 'disabled'
                ELSE 'disabled'
            END
        """)
    )

    # Phase 3: Make NOT NULL (after verifying data)
    op.alter_column('users', 'account_status', nullable=False)

    # Note: Drop old 'status' column in next migration
    # to allow rollback window


def downgrade() -> None:
    """Rollback account_status column."""
    op.drop_column('users', 'account_status')
```

## Foreign Key Changes

```python
"""Add foreign key to orders table"""
from alembic import op
import sqlalchemy as sa


def upgrade() -> None:
    """
    Add foreign key constraint.

    Ensure referential integrity.
    """
    # Create index first for performance
    op.create_index(
        'ix_orders_user_id',
        'orders',
        ['user_id']
    )

    # Add foreign key constraint
    op.create_foreign_key(
        'fk_orders_user_id',  # Constraint name
        'orders',              # Source table
        'users',               # Target table
        ['user_id'],           # Source columns
        ['id'],                # Target columns
        ondelete='CASCADE'     # Delete orders when user deleted
    )


def downgrade() -> None:
    """Remove foreign key constraint."""
    op.drop_constraint(
        'fk_orders_user_id',
        'orders',
        type_='foreignkey'
    )

    op.drop_index('ix_orders_user_id', table_name='orders')
```

## Complex Table Changes

```python
"""Split user table into users and profiles"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import text


def upgrade() -> None:
    """
    Split users table into users (auth) and profiles (data).

    Multi-step migration:
    1. Create new profiles table
    2. Copy data
    3. Add foreign key
    4. Drop columns from users
    """
    # Step 1: Create profiles table
    op.create_table(
        'profiles',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('first_name', sa.String(100), nullable=True),
        sa.Column('last_name', sa.String(100), nullable=True),
        sa.Column('bio', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # Step 2: Copy data from users to profiles
    connection = op.get_bind()
    connection.execute(
        text("""
            INSERT INTO profiles (user_id, first_name, last_name, bio, created_at)
            SELECT id, first_name, last_name, bio, created_at
            FROM users
        """)
    )

    # Step 3: Add foreign key
    op.create_foreign_key(
        'fk_profiles_user_id',
        'profiles',
        'users',
        ['user_id'],
        ['id'],
        ondelete='CASCADE'
    )

    # Step 4: Drop old columns (in separate migration recommended)
    # op.drop_column('users', 'first_name')
    # op.drop_column('users', 'last_name')
    # op.drop_column('users', 'bio')


def downgrade() -> None:
    """
    Reverse table split.

    WARNING: Complex rollback.
    """
    # Add columns back to users
    op.add_column('users', sa.Column('first_name', sa.String(100)))
    op.add_column('users', sa.Column('last_name', sa.String(100)))
    op.add_column('users', sa.Column('bio', sa.Text()))

    # Copy data back
    connection = op.get_bind()
    connection.execute(
        text("""
            UPDATE users
            SET first_name = p.first_name,
                last_name = p.last_name,
                bio = p.bio
            FROM profiles p
            WHERE users.id = p.user_id
        """)
    )

    # Drop profiles table
    op.drop_table('profiles')
```

## Migration Testing

```python
# tests/test_migrations.py
import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, inspect, text
from app.config import settings


@pytest.fixture
def alembic_config():
    """Create Alembic configuration."""
    config = Config("alembic.ini")
    config.set_main_option("sqlalchemy.url", settings.test_database_url)
    return config


@pytest.fixture
def empty_database():
    """Create empty test database."""
    engine = create_engine(settings.test_database_url)

    # Drop all tables
    with engine.begin() as conn:
        conn.execute(text("DROP SCHEMA public CASCADE"))
        conn.execute(text("CREATE SCHEMA public"))

    yield engine
    engine.dispose()


def test_migrations_upgrade_downgrade(alembic_config, empty_database):
    """
    Test migrations can upgrade and downgrade.

    Ensures all migrations are reversible.
    """
    # Upgrade to head
    command.upgrade(alembic_config, "head")

    # Verify tables exist
    inspector = inspect(empty_database)
    tables = inspector.get_table_names()
    assert "users" in tables
    assert "alembic_version" in tables

    # Downgrade to base
    command.downgrade(alembic_config, "base")

    # Verify tables removed
    inspector = inspect(empty_database)
    tables = inspector.get_table_names()
    assert "users" not in tables


def test_migration_data_integrity(alembic_config, empty_database):
    """
    Test data migration preserves data integrity.

    Insert test data, run migration, verify data.
    """
    # Upgrade to revision before data migration
    command.upgrade(alembic_config, "abc123")

    # Insert test data
    with empty_database.begin() as conn:
        conn.execute(
            text("INSERT INTO users (email, status) VALUES (:email, :status)"),
            {"email": "test@example.com", "status": "active"}
        )

    # Run data migration
    command.upgrade(alembic_config, "abc124")

    # Verify data migrated correctly
    with empty_database.begin() as conn:
        result = conn.execute(
            text("SELECT account_status FROM users WHERE email = :email"),
            {"email": "test@example.com"}
        )
        row = result.fetchone()
        assert row[0] == "enabled"


def test_migration_rollback_safety(alembic_config, empty_database):
    """
    Test rollback doesn't lose data.

    Verify downgrade preserves critical data.
    """
    # Upgrade and insert data
    command.upgrade(alembic_config, "head")

    with empty_database.begin() as conn:
        conn.execute(
            text("INSERT INTO users (email) VALUES (:email)"),
            {"email": "test@example.com"}
        )

    # Downgrade one revision
    command.downgrade(alembic_config, "-1")

    # Verify data still exists
    with empty_database.begin() as conn:
        result = conn.execute(
            text("SELECT COUNT(*) FROM users WHERE email = :email"),
            {"email": "test@example.com"}
        )
        count = result.scalar()
        assert count == 1
```

## ❌ Anti-Patterns

```python
# ❌ Making column NOT NULL immediately
def upgrade():
    op.add_column('users', sa.Column('phone', sa.String(), nullable=False))
    # Fails for existing rows!

# ✅ Better: Add as nullable, populate, then make NOT NULL
def upgrade():
    op.add_column('users', sa.Column('phone', sa.String(), nullable=True))
    op.execute("UPDATE users SET phone = '' WHERE phone IS NULL")
    # Make NOT NULL in separate migration


# ❌ No downgrade implementation
def downgrade():
    pass  # Not reversible!

# ✅ Better: Implement proper downgrade
def downgrade():
    op.drop_column('users', 'phone')


# ❌ Data migration in schema migration
def upgrade():
    op.add_column('users', sa.Column('full_name', sa.String()))
    op.execute("UPDATE users SET full_name = first_name || ' ' || last_name")
    op.drop_column('users', 'first_name')
    op.drop_column('users', 'last_name')
    # Too many changes in one migration!

# ✅ Better: Split into multiple migrations
# Migration 1: Add column
# Migration 2: Migrate data
# Migration 3: Drop old columns


# ❌ No constraint naming
def upgrade():
    op.create_foreign_key(None, 'orders', 'users', ['user_id'], ['id'])
    # Auto-generated name!

# ✅ Better: Explicit constraint names
def upgrade():
    op.create_foreign_key('fk_orders_user_id', 'orders', 'users', ['user_id'], ['id'])
```

## Best Practices Checklist

- ✅ Use descriptive migration names
- ✅ Always implement downgrade()
- ✅ Add columns as nullable first
- ✅ Use batch operations for SQLite
- ✅ Name all constraints explicitly
- ✅ Test migrations up and down
- ✅ Split complex changes into multiple migrations
- ✅ Create indexes before foreign keys
- ✅ Use transactions for data migrations
- ✅ Document breaking changes
- ✅ Test with production-like data volumes
- ✅ Keep migrations idempotent when possible

## Auto-Apply

When creating migrations:
1. Use `alembic revision --autogenerate -m "descriptive_name"`
2. Review generated migration carefully
3. Implement proper downgrade()
4. Add columns as nullable initially
5. Split data migrations from schema migrations
6. Name all constraints explicitly
7. Write tests for complex migrations
8. Document breaking changes in docstring

## Related Skills

- `query-optimization` - For index creation
- `type-safety` - For type hints in migrations
- `pytest-patterns` - For migration testing
- `structured-errors` - For error handling
- `docstring-format` - For migration documentation
