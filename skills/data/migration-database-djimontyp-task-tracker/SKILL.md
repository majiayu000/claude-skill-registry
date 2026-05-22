---
name: migration-database
description: This skill should be used when working with database migrations in SQLModel-based projects. Trigger when user asks to create migrations for new/modified models, generate database schema changes, or apply migrations. Enforces SQLModel as single source of truth and automatic migration generation only.
---

# Database Migration (SQLModel + Alembic)

## Overview

Automate database migration workflows for SQLModel-based projects using Alembic. This skill enforces strict rules: SQLModel models are the single source of truth, migrations are generated automatically only (never manual), and all migrations must include `import sqlmodel` for proper functioning.

## When to Use This Skill

Trigger this skill when the user requests:
- "Create a migration for the new User model"
- "Generate migration after I updated Task fields"
- "I added a column to Topic, make a migration"
- "Apply pending migrations to the database"
- Any task involving database schema changes in SQLModel projects

## Core Principles

### 1. SQLModel as Single Source of Truth
- **NEVER** modify database schema directly (via SQL, pgAdmin, psql, etc.)
- **ALWAYS** modify SQLModel model classes first, then generate migrations
- Database must reflect SQLModel models exactly

### 2. Automatic Generation Only
- **ALWAYS** use `just alembic-auto -m "description"` to generate migrations
- **NEVER** create empty manual migrations
- **NEVER** write custom SQL without explicit user approval

### 3. Required Import Fix
Alembic often omits `import sqlmodel`, causing errors with SQLModel types. **ALWAYS** add this import after generation.

## Workflow

### Step 1: Pre-Generation Safety Checks

Before generating any migration, verify prerequisites:

1. **Check PostgreSQL is running**:
   ```bash
   docker compose ps postgres
   ```
   If not running, start it: `docker compose up -d postgres`

2. **Verify model imports** in `backend/app/models/__init__.py`:
   - Read the file and confirm new/modified models are imported
   - Add missing imports if needed

3. **Type check for syntax errors**:
   ```bash
   just typecheck
   ```
   Fix any errors before proceeding

### Step 2: Generate Migration

Use the automatic migration generation command:

```bash
just alembic-auto -m "descriptive message"
```

**Message conventions**:
- ✅ `"add User table with authentication fields"`
- ✅ `"update Task: add priority and status fields"`
- ✅ `"add foreign key relationship Task.user_id → User.id"`
- ❌ `"migration"` (too vague)
- ❌ `"changes"` (not descriptive)

### Step 3: Post-Generation Fixes (MANDATORY)

**Critical step - never skip this:**

1. **Locate the migration file**:
   - Alembic prints the path in output: `backend/alembic/versions/{revision_id}_{slug}.py`
   - Example: `backend/alembic/versions/abc123def456_add_user_table.py`

2. **Read the migration file** completely

3. **Check for `import sqlmodel`**:
   - Look in the import section (after `import sqlalchemy as sa`)
   - If `import sqlmodel` is **missing**, add it:

   ```python
   """add User table

   Revision ID: abc123def456
   Revises: previous_revision
   Create Date: 2024-01-01 12:00:00.000000

   """
   from alembic import op
   import sqlalchemy as sa
   import sqlmodel  # ← ADD THIS IF MISSING

   # revision identifiers
   revision = 'abc123def456'
   down_revision = 'previous_revision'
   branch_labels = None
   depends_on = None
   ```

4. **Validate migration operations**:
   - Review `upgrade()` and `downgrade()` functions
   - Check operations match expected model changes
   - Warn user about destructive operations (DROP COLUMN, DROP TABLE)

### Step 4: Present Migration for Review

**Provide clickable file link for user review:**

1. Provide file path as clickable link (format: `backend/alembic/versions/{filename}.py:1`)
2. Summarize key changes from `upgrade()` and `downgrade()` functions
3. Call out any potentially destructive operations (DROP COLUMN, DROP TABLE)
4. Wait for explicit user confirmation before applying

**DO NOT** paste full migration contents in chat - provide file link only.

### Step 5: Apply Migration (After Confirmation Only)

Only proceed after user explicitly confirms:

```bash
just alembic-up
```

**NEVER apply migrations without user approval.**

## Common Scenarios

### Creating New Model

User adds a new SQLModel in `backend/app/models/`:

1. Verify model is imported in `backend/app/models/__init__.py`
2. Run pre-generation checks (PostgreSQL, type check)
3. Generate: `just alembic-auto -m "add {ModelName} table"`
4. Read migration file
5. Add `import sqlmodel` if missing
6. Provide clickable file link and summarize changes
7. Apply after confirmation: `just alembic-up`

### Modifying Existing Model

User changes fields in an existing SQLModel:

1. Run pre-generation checks
2. Generate: `just alembic-auto -m "update {ModelName}: {change description}"`
3. Read migration file
4. Add `import sqlmodel` if missing
5. Provide clickable file link and summarize changes
6. Apply after confirmation: `just alembic-up`

### Multiple Model Changes

User modifies several models at once:

1. Group related changes into logical units
2. Generate one migration per logical change (preferred)
3. OR generate single migration for all changes if closely related
4. Follow standard workflow for each migration

## Error Handling

### "NameError: name 'sqlmodel' is not defined"
**Cause**: Missing `import sqlmodel` in migration
**Fix**: Edit migration file, add `import sqlmodel` to imports

### "Target database is not up to date"
**Cause**: Pending unapplied migrations exist
**Fix**: Run `just alembic-up` to apply pending migrations before generating new ones

### "Can't proceed with autogenerate"
**Cause**: Models not imported or database inaccessible
**Fix**:
1. Check `backend/app/models/__init__.py` for missing imports
2. Verify: `docker compose ps postgres`
3. Check database connection settings

## Extending SQLModel

**⚠️ Important**: Always prefer native SQLModel features first. Only use SQLAlchemy extensions when SQLModel doesn't support the feature.

When SQLModel lacks native support for a feature (e.g., PostgreSQL JSON/ARRAY, CHECK constraints, composite unique constraints), extend via SQLAlchemy:

```python
from sqlmodel import Field, Column
from sqlalchemy import JSON, CheckConstraint

class Model(SQLModel, table=True):
    # PostgreSQL JSON type
    data: dict = Field(sa_column=Column(JSON, nullable=False))

    # CHECK constraint
    rating: int = Field(
        sa_column=Column(Integer, CheckConstraint('rating >= 1 AND rating <= 5'))
    )
```

See `references/sqlmodel-migration-rules.md` → "Extending SQLModel with SQLAlchemy" for full examples.

## Safety Rules (STRICT)

### Forbidden Without User Approval
- Creating manual migrations (empty migrations)
- Modifying database schema directly (SQL commands, GUI tools)
- Editing already-applied migrations (in `alembic_version`)
- Running custom SQL in migrations
- Applying migrations without providing file link and summary first
- Removing `import sqlmodel` from migrations

### Always Required
- Generate migrations using `just alembic-auto`
- Add `import sqlmodel` to every migration if missing
- Provide clickable file link and summarize changes before applying
- Wait for explicit user confirmation before `alembic-up`
- Verify PostgreSQL is running before generation

## References

For detailed information about SQLModel types, migration patterns, and comprehensive rules, refer to:
- `references/sqlmodel-migration-rules.md` - Complete migration rules and type mappings

## Quick Reference

```bash
# Pre-generation checks
docker compose ps postgres          # Verify DB is running
just typecheck                      # Check for syntax errors

# Generate migration
just alembic-auto -m "description"  # Create migration

# Apply migration (after review)
just alembic-up                     # Apply to database

# Common debugging
docker compose logs postgres        # Check DB logs
docker compose restart postgres     # Restart if needed
```

## Workflow Summary

1. ✅ Pre-checks: PostgreSQL running, models imported, no syntax errors
2. ✅ Generate: `just alembic-auto -m "description"`
3. ✅ Read migration file completely
4. ✅ Add `import sqlmodel` if missing
5. ✅ Provide file link (format: `file.py:1`) and summarize changes
6. ⏸️ **WAIT for user confirmation**
7. ✅ Apply: `just alembic-up` (only after confirmation)

**Remember**: SQLModel is truth, autogenerate only, always add `import sqlmodel`, provide file links (not full contents), never apply without approval.