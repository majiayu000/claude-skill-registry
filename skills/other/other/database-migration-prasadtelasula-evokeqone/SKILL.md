---
name: database-migration
description: Create and manage Alembic database migrations for SQLAlchemy models. Use when adding/modifying database tables or columns.
allowed-tools: Read, Write, Bash, Glob
---

You help create and manage database migrations using Alembic for the QA Team Portal backend.

## When to Use This Skill

- Creating new database tables (new SQLAlchemy models)
- Adding/removing/modifying columns in existing tables
- Adding indexes or constraints
- Data migrations (transforming existing data)
- Reviewing migration files before applying

## Prerequisites

- SQLAlchemy models exist in `backend/app/models/`
- Models are imported in `backend/app/db/base.py`
- Alembic is initialized (`backend/alembic/` directory exists)
- Database connection configured in `.env`

## Workflow

### 1. Create Migration

```bash
cd backend

# Auto-generate migration from model changes
uv run alembic revision --autogenerate -m "descriptive message"

# Or create empty migration for data changes
uv run alembic revision -m "migrate existing data"
```

### 2. Review Generated Migration

- Open the new file in `backend/alembic/versions/`
- Check `upgrade()` function for forward migration
- Check `downgrade()` function for rollback
- Verify changes match your intent
- Add any custom logic if needed (e.g., data transformation)

### 3. Apply Migration

```bash
# Apply to database
uv run alembic upgrade head

# Or apply one version
uv run alembic upgrade +1
```

### 4. Verify Migration

```bash
# Check current version
uv run alembic current

# View migration history
uv run alembic history --verbose
```

## Common Migration Patterns

### Adding a New Table

```python
def upgrade():
    op.create_table(
        'research',
        sa.Column('id', postgresql.UUID(), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('status', sa.Enum('ongoing', 'completed', 'planned'), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_research_status', 'research', ['status'])

def downgrade():
    op.drop_index('ix_research_status', table_name='research')
    op.drop_table('research')
```

### Adding a Column

```python
def upgrade():
    op.add_column('team_members',
        sa.Column('linkedin_url', sa.String(length=255), nullable=True)
    )

def downgrade():
    op.drop_column('team_members', 'linkedin_url')
```

### Data Migration

```python
def upgrade():
    # Add column
    op.add_column('users', sa.Column('role', sa.String(50), nullable=True))

    # Migrate data
    connection = op.get_bind()
    connection.execute(
        "UPDATE users SET role = 'member' WHERE role IS NULL"
    )

    # Make not nullable
    op.alter_column('users', 'role', nullable=False)

def downgrade():
    op.drop_column('users', 'role')
```

## Rollback Migrations

```bash
# Rollback one version
uv run alembic downgrade -1

# Rollback to specific version
uv run alembic downgrade <revision_id>

# Rollback all migrations
uv run alembic downgrade base
```

## Troubleshooting

### "Target database is not up to date"

```bash
# Check current version
uv run alembic current

# Stamp database with current code version
uv run alembic stamp head
```

### Migration conflicts

```bash
# List all heads
uv run alembic heads

# Merge conflicting branches
uv run alembic merge -m "merge branches" <rev1> <rev2>
```

### Reset migrations (development only!)

```bash
# Drop all tables
uv run alembic downgrade base

# Or drop database and recreate
dropdb qa_portal
createdb qa_portal
uv run alembic upgrade head
```

## Best Practices

1. **Always review auto-generated migrations** - Alembic may miss some changes
2. **Test migrations on dev database first** - Don't apply directly to production
3. **Write reversible migrations** - Ensure `downgrade()` actually works
4. **One logical change per migration** - Keep migrations focused
5. **Include data migrations when needed** - Don't just change schema
6. **Backup production database** before applying migrations
7. **Use descriptive messages** - Clear commit-style messages

## Safety Checks

Before applying to production:

- [ ] Migration reviewed and tested on dev database
- [ ] Downgrade tested and works
- [ ] No data loss in migration
- [ ] Indexes added for new query patterns
- [ ] Foreign key constraints properly defined
- [ ] Backup of production database taken
- [ ] Deployment plan includes rollback procedure

## Output Format

After creating/applying migration, report:

1. Migration file created: `<filename>`
2. Changes summary: What tables/columns affected
3. Applied successfully: Yes/No
4. Current database version: `<revision_id>`
5. Any warnings or issues encountered
