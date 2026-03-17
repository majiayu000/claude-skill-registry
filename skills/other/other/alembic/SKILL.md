---
name: alembic
description: Database migration management for SQLAlchemy projects using Alembic
when_to_use: When you need to create, apply, or manage database schema changes in SQLAlchemy projects
---

# Alembic Database Migrations

Alembic is a database migration tool for SQLAlchemy projects that provides version control for your database schema.

## Quick Start

### Create Migration (Autogenerate)

```bash
# Generate migration from model changes
uv run alembic revision --autogenerate -m "Add user table"

# Check if there are pending changes
uv run alembic check
```

### Apply Migrations

```bash
# Upgrade to latest version
uv run alembic upgrade head

# Upgrade to specific revision
uv run alembic upgrade ae1027a6acf

# Downgrade one revision
uv run alembic downgrade -1

# Downgrade to base (empty schema)
uv run alembic downgrade base
```

### Check Status

```bash
# Show current database revision
uv run alembic current

# Show all revision history
uv run alembic history

# Show revision details
uv run alembic show ae1027a6acf
```

## Common Patterns

### Autogenerate Configuration

**env.py setup for async SQLAlchemy:**

```python
import asyncio
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context

# Import your models
from app.models import Base
from app.config import get_settings

config = context.config
settings = get_settings()

# Configure database URL for async
database_url = settings.database_url.replace("postgresql://", "postgresql+asyncpg://")
config.set_main_option("sqlalchemy.url", database_url)

target_metadata = Base.metadata

async def run_async_migrations():
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()

def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        compare_server_default=True,
        render_as_batch=False,  # Set to True for SQLite
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    asyncio.run(run_async_migrations())

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

### Manual Migration Operations

**Common schema changes:**

```python
from alembic import op
import sqlalchemy as sa

def upgrade():
    # Add column
    op.add_column('users', sa.Column('email', sa.String(255), nullable=True))

    # Rename table
    op.rename_table('old_table', 'new_table')

    # Create index
    op.create_index('ix_users_email', 'users', ['email'])

    # Add constraint
    op.create_check_constraint('ck_age_positive', 'users', 'age > 0')

def downgrade():
    # Reverse operations
    op.drop_constraint('ck_age_positive', 'users')
    op.drop_index('ix_users_email')
    op.rename_table('new_table', 'old_table')
    op.drop_column('users', 'email')
```

### Batch Mode (for SQLite)

**Configure batch mode in env.py:**

```python
context.configure(
    connection=connection,
    target_metadata=target_metadata,
    render_as_batch=True  # Required for SQLite migrations
)
```

**Generated batch migration:**

```python
def upgrade():
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('email', sa.String(length=255), nullable=True))
        batch_op.create_index('ix_users_email', ['email'], unique=False)
```

### Filtering Objects

**Skip certain objects in autogenerate:**

```python
def include_object(object, name, type_, reflected, compare_to):
    # Skip temporary tables
    if type_ == "table" and name.startswith("temp_"):
        return False

    # Skip columns with skip_autogenerate flag
    if type_ == "column" and not reflected:
        if object.info.get("skip_autogenerate", False):
            return False

    return True

context.configure(
    connection=connection,
    target_metadata=target_metadata,
    include_object=include_object
)
```

**Filter by schema:**

```python
def include_name(name, type_, parent_names):
    if type_ == "schema":
        return name in [None, "public", "auth"]  # Include default + specific schemas
    elif type_ == "table":
        return parent_names["schema_qualified_table_name"] in target_metadata.tables
    return True

context.configure(
    connection=connection,
    target_metadata=target_metadata,
    include_name=include_name,
    include_schemas=True
)
```

### Custom Migration Processing

**Modify generated migrations:**

```python
def process_revision_directives(context, revision, directives):
    script = directives[0]

    # Skip empty migrations
    if config.cmd_opts.autogenerate and script.upgrade_ops.is_empty():
        directives[:] = []
        return

    # Remove downgrade operations for one-way migrations
    script.downgrade_ops.ops[:] = []

context.configure(
    connection=connection,
    target_metadata=target_metadata,
    process_revision_directives=process_revision_directives
)
```

### Data Migrations

**Migrate data during schema change:**

```python
def upgrade():
    # Add new column
    op.add_column('users', sa.Column('full_name', sa.String(255), nullable=True))

    # Migrate data
    connection = op.get_bind()
    connection.execute(
        sa.text("UPDATE users SET full_name = first_name || ' ' || last_name")
    )

    # Make column required after data migration
    op.alter_column('users', 'full_name', nullable=False)

def downgrade():
    op.drop_column('users', 'full_name')
```

### Branch Migrations

**Work with multiple branches:**

```bash
# Create branch
uv run alembic revision -m "Create feature branch" --head=base --branch-label=feature_x

# Upgrade specific branch
uv run alembic upgrade feature_x@head

# Merge branches
uv run alembic merge -m "Merge feature_x into main" feature_x@head main@head
```

## Practical Code Snippets

### Check if Database is Up-to-Date

```python
from alembic import config, script
from alembic.runtime import migration
from sqlalchemy import create_engine

def is_database_up_to_date(alembic_cfg_path, database_url):
    """Check if database schema matches latest migrations"""
    cfg = config.Config(alembic_cfg_path)
    directory = script.ScriptDirectory.from_config(cfg)

    engine = create_engine(database_url)
    with engine.begin() as connection:
        context = migration.MigrationContext.configure(connection)
        current_heads = set(context.get_current_heads())
        latest_heads = set(directory.get_heads())
        return current_heads == latest_heads
```

### Programmatically Run Migrations

```python
from alembic import command
from alembic.config import Config

def run_migrations(alembic_ini_path):
    """Run all pending migrations"""
    alembic_cfg = Config(alembic_ini_path)
    command.upgrade(alembic_cfg, "head")

def create_migration(alembic_ini_path, message, autogenerate=True):
    """Create new migration"""
    alembic_cfg = Config(alembic_ini_path)
    command.revision(alembic_cfg, message=message, autogenerate=autogenerate)
```

### Custom Migration Operations

```python
from alembic.autogenerate import rewriter
from alembic.operations import ops

writer = rewriter.Rewriter()

@writer.rewrites(ops.AddColumnOp)
def add_column_non_nullable(context, revision, op):
    """Add non-nullable columns in two steps"""
    if not op.column.nullable:
        op.column.nullable = True
        return [
            op,
            ops.AlterColumnOp(
                op.table_name,
                op.column.name,
                nullable=False,
                existing_type=op.column.type,
                schema=op.schema
            )
        ]
    return op

# Use in env.py
context.configure(
    connection=connection,
    target_metadata=target_metadata,
    process_revision_directives=writer
)
```

## Requirements

- **Python 3.8+**: Required for async support
- **SQLAlchemy 2.0+**: For modern async patterns
- **PostgreSQL/MySQL/SQLite**: Supported databases
- **Alembic 1.8+**: Migration tooling

### Common Dependencies

```bash
# Core dependencies
uv add alembic sqlalchemy

# For PostgreSQL with async
uv add asyncpg

# For MySQL with async
uv add aiomysql

# For SQLite (built-in)
# No additional packages needed
```

### Development Setup

```bash
# Initialize Alembic in existing project
uv run alembic init alembic

# Configure env.py for your models
# Edit alembic.ini for database URL

# First migration
uv run alembic revision --autogenerate -m "Initial schema"
uv run alembic upgrade head
```
