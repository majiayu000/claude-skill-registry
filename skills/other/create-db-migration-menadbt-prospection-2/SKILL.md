---
name: create-db-migration
description: Creates Alembic database migrations safely. Use when schema changes are needed, adding tables, columns, indexes, or modifying database structure.
allowed-tools: Read, Bash(docker compose exec back:*), Glob, Grep
---

# Create Database Migration

Creates Alembic database migrations for schema changes.

## Prerequisites

Ensure Docker containers are running:
```bash
docker compose ps
```

If not running, start them:
```bash
docker compose up -d
```

## Workflow

### 1. Create Migration

```bash
docker compose exec back uv run alembic revision --autogenerate -m "Description of change"
```

**Good migration descriptions**:
- "Add notifications table"
- "Add index on users.email"
- "Add description column to items"
- "Remove deprecated legacy_id column"

### 2. Review Migration

After creation, review the generated migration file in `back/alembic/versions/`.

**Check for**:
- Correct `upgrade()` and `downgrade()` operations
- No data loss in `downgrade()`
- Proper index creation
- Foreign key constraints

### 3. Apply Migration Locally

Migrations run automatically on container restart, or manually:

```bash
docker compose exec back uv run alembic upgrade head
```

### 4. Verify

```bash
docker compose exec back uv run alembic current
```

## Common Migration Patterns

### Add Column
```python
def upgrade():
    op.add_column('table_name', sa.Column('column_name', sa.String(), nullable=True))

def downgrade():
    op.drop_column('table_name', 'column_name')
```

### Add Index
```python
def upgrade():
    op.create_index('ix_table_column', 'table_name', ['column_name'])

def downgrade():
    op.drop_index('ix_table_column', table_name='table_name')
```

### Add Table
```python
def upgrade():
    op.create_table(
        'table_name',
        sa.Column('id', sa.UUID(), primary_key=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

def downgrade():
    op.drop_table('table_name')
```

## Warnings

- **Destructive operations**: Be careful with `DROP TABLE`, `DROP COLUMN`
- **Data migrations**: Consider data preservation in downgrade
- **Production**: Migrations run via Lambda, triggered by CI/CD after deployment

## Production Migration

In deployed environments:
- Migrations run via dedicated Migration Lambda
- Triggered automatically by CI/CD after deployment
- Manual trigger: `aws lambda invoke --function-name template-saas-api-migrate-lambda-{stage} /dev/null`
