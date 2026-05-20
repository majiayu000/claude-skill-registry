---
name: alembic
description: |
  Generates and manages database migrations with Alembic for the Bookkeep backend.
  Use when: creating database migrations, modifying models, adding columns, creating tables, or running schema changes.
allowed-tools: Read, Edit, Write, Glob, Grep, Bash
---

# Alembic Skill

Alembic manages schema migrations for Bookkeep's SQLAlchemy models. Migrations live in `backend/alembic/versions/` with numeric prefixes (001, 002, etc.). The project supports both PostgreSQL (production) and SQLite (development) with idempotent migrations using existence checks.

## Quick Start

### Generate Migration

```bash
cd backend
alembic revision --autogenerate -m "add_column_to_table"
```

### Apply Migrations

```bash
cd backend
alembic upgrade head     # Apply all pending
alembic upgrade +1       # Apply next migration only
alembic downgrade -1     # Roll back one migration
```

### Check Status

```bash
cd backend
alembic current          # Show current revision
alembic history          # List all migrations
```

## Key Concepts

| Concept | Usage | Example |
|---------|-------|---------|
| Numeric prefix | Sequential ordering | `022_add_download_system.py` |
| Idempotent checks | Safe reruns | `if not table_exists('download_tasks'):` |
| batch_alter_table | SQLite compatibility | `with op.batch_alter_table('books'):` |
| Data migrations | Transform existing data | `op.execute("UPDATE books SET ...")` |

## Project Configuration

- **alembic.ini**: `backend/alembic.ini`
- **env.py**: `backend/alembic/env.py` (loads `DATABASE_URL` from `app.database`)
- **versions**: `backend/alembic/versions/` (30 migrations)
- **Models**: `backend/app/models.py`

## Common Patterns

### Add Column with Default

```python
if not column_exists('users', 'can_download'):
    op.add_column('users', sa.Column(
        'can_download', 
        sa.Boolean(), 
        nullable=True, 
        server_default='true'
    ))
```

### Create Table with Indexes

```python
if not table_exists('download_tasks'):
    op.create_table('download_tasks',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('book_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['book_id'], ['books.id']),
    )
if not index_exists('download_tasks', 'ix_download_tasks_book_id'):
    op.create_index('ix_download_tasks_book_id', 'download_tasks', ['book_id'])
```

## See Also

- [patterns](references/patterns.md) - Migration patterns and helper functions
- [workflows](references/workflows.md) - Common migration workflows

## Related Skills

- See the **sqlalchemy** skill for model definitions
- See the **python** skill for Python backend conventions
- See the **fastapi** skill for API integration after migrations