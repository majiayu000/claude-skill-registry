---
name: devops-database
description: Manages PostgreSQL database operations including Alembic migrations (creation, application, rollback), database backups and restoration for both development and production environments, shell access, and pgvector extension management. This skill should be used when creating schema changes, running migrations, backing up data, or troubleshooting database issues.
---

# Devops Database

## Overview

Manage PostgreSQL database operations for the Bestays platform, including Alembic migrations, backups, restoration, and database administration for both development and production environments.

## When to Use This Skill

Use this skill when:
- Creating new database migrations (`alembic revision`)
- Applying migrations (`make migrate`, `alembic upgrade head`)
- Rolling back migrations (`alembic downgrade`)
- Backing up database (development or production)
- Restoring database from backup
- Accessing database shell for queries or inspection
- Troubleshooting database connection or schema issues
- Managing pgvector extension for vector embeddings

## Database Configuration

### Development Environment

**Container:** bestays-db-dev
**Image:** postgres:16-alpine
**Port:** localhost:5433 → container:5432
**Database:** bestays_dev
**User:** bestays_user
**Password:** bestays_password (from `.env`)

**Connection String (from host):**
```
postgresql://bestays_user:bestays_password@localhost:5433/bestays_dev
```

**Connection String (from containers):**
```
postgresql+asyncpg://bestays_user:bestays_password@postgres:5432/bestays_dev
```

**Data Persistence:** `postgres_data` Docker volume (survives `make down`)

**Extensions:**
- pgvector - Vector similarity search for embeddings

### Production Environment

**Container:** bestays-db-prod
**Image:** postgres:16-alpine
**Port:** Not exposed (internal network only)
**Database:** From `$POSTGRES_DB` environment variable
**User:** From `$POSTGRES_USER` environment variable
**Password:** From `$POSTGRES_PASSWORD` environment variable

**Connection String (from containers):**
```
postgresql+asyncpg://${POSTGRES_USER}:${POSTGRES_PASSWORD}@postgres:5432/${POSTGRES_DB}
```

**Data Persistence:** `postgres_data` Docker volume + backup directory mounted at `/backups`

## Alembic Migrations

Alembic is used for database schema versioning and migrations.

### Configuration

**Location:** `apps/server/alembic/`
**Config File:** `apps/server/alembic.ini`
**Migrations Directory:** `apps/server/alembic/versions/`
**Environment Script:** `apps/server/alembic/env.py`

**File Naming Template:** `YYYYMMDD_HHMM-{rev}_{slug}.py`
Example: `20251030_1045-abc123def456_add_users_table.py`

### Creating Migrations

#### Auto-Generate Migration (Recommended)

**From host machine:**
```bash
# 1. Start services if not running
make dev

# 2. Enter backend container
make shell-server

# 3. Auto-generate migration from model changes
alembic revision --autogenerate -m "Add users table"

# 4. Exit container
exit
```

**What it does:**
- Compares current models (SQLAlchemy) with database schema
- Generates migration script with detected changes
- Creates file in `apps/server/alembic/versions/`

**Review the generated migration:**
```bash
# Check the latest migration file
ls -lt apps/server/alembic/versions/ | head -2
cat apps/server/alembic/versions/YYYYMMDD_HHMM-*_add_users_table.py
```

**⚠️ Important:** Always review auto-generated migrations! They may:
- Miss some changes (indexes, constraints)
- Include unintended changes
- Need manual data migrations

#### Manual Migration

**When to use manual migrations:**
- Complex data transformations
- Renaming columns (Alembic can't detect renames)
- Adding data (seed data, lookup tables)
- Custom SQL operations

**Create empty migration:**
```bash
make shell-server
alembic revision -m "Migrate user data"
exit
```

**Edit the migration file:**
```python
# apps/server/alembic/versions/YYYYMMDD_HHMM-xxx_migrate_user_data.py
def upgrade() -> None:
    # Add your migration logic here
    op.execute("""
        UPDATE users
        SET email_verified = true
        WHERE created_at < '2025-01-01'
    """)

def downgrade() -> None:
    # Add rollback logic here
    op.execute("""
        UPDATE users
        SET email_verified = false
        WHERE created_at < '2025-01-01'
    """)
```

### Applying Migrations

#### Development

**Apply all pending migrations:**
```bash
make migrate
```

Equivalent to:
```bash
make shell-server
alembic upgrade head
exit
```

**Apply specific number of migrations:**
```bash
make shell-server
alembic upgrade +1    # Apply next migration
alembic upgrade +2    # Apply next 2 migrations
exit
```

**Apply to specific revision:**
```bash
make shell-server
alembic upgrade abc123def456
exit
```

#### Production

**Apply migrations in production:**
```bash
# SSH into production server
ssh user@production-server

# Navigate to project
cd /path/to/bestays-monorepo

# Apply migrations (with production compose file)
docker-compose -f docker-compose.prod.yml exec backend alembic upgrade head
```

**Best Practice:** Test migrations in staging environment first!

### Rolling Back Migrations

**Downgrade one migration:**
```bash
make shell-server
alembic downgrade -1
exit
```

**Downgrade to specific revision:**
```bash
make shell-server
alembic downgrade abc123def456
exit
```

**Downgrade all (back to empty database):**
```bash
make shell-server
alembic downgrade base
exit
```

**⚠️ Warning:** Downgrading can cause data loss! Always backup first.

### Migration History

**View current revision:**
```bash
make shell-server
alembic current
exit
```

**View migration history:**
```bash
make shell-server
alembic history
exit
```

**View pending migrations:**
```bash
make shell-server
alembic history --verbose
exit
```

## Database Backups

### Creating Backups

**Development backup:**
```bash
docker-compose -f docker-compose.dev.yml exec postgres \
  pg_dump -U bestays_user bestays_dev > backups/dev-backup-$(date +%Y%m%d-%H%M%S).sql
```

**Production backup:**
```bash
docker-compose -f docker-compose.prod.yml exec postgres \
  pg_dump -U $POSTGRES_USER $POSTGRES_DB > backups/prod-backup-$(date +%Y%m%d-%H%M%S).sql
```

**Compressed backup:**
```bash
# Add | gzip > file.sql.gz to compress
docker-compose -f docker-compose.dev.yml exec postgres \
  pg_dump -U bestays_user bestays_dev | gzip > backups/backup.sql.gz
```

## Database Restoration

### Restore Development Database

**From SQL dump:**
```bash
# 1. Stop services
make down

# 2. Start only PostgreSQL
docker-compose -f docker-compose.dev.yml up -d postgres

# 3. Wait for PostgreSQL to be ready
sleep 5

# 4. Drop and recreate database
docker-compose -f docker-compose.dev.yml exec postgres psql -U bestays_user -d postgres -c "DROP DATABASE IF EXISTS bestays_dev;"
docker-compose -f docker-compose.dev.yml exec postgres psql -U bestays_user -d postgres -c "CREATE DATABASE bestays_dev OWNER bestays_user;"

# 5. Restore from backup
cat backups/dev-backup-20251030-104530.sql | docker-compose -f docker-compose.dev.yml exec -T postgres psql -U bestays_user -d bestays_dev

# 6. Start all services
make up
```

**From compressed backup:**
```bash
gunzip -c backups/dev-backup-20251030-104530.sql.gz | \
  docker-compose -f docker-compose.dev.yml exec -T postgres psql -U bestays_user -d bestays_dev
```

### Restore Production Database

**⚠️ CRITICAL:** Always test restoration procedure in staging first!

**Production restoration:**
```bash
# 1. SSH into production server
ssh user@production-server

# 2. Put site in maintenance mode (if possible)
# ... maintenance mode steps ...

# 3. Stop backend to prevent writes
docker-compose -f docker-compose.prod.yml stop backend

# 4. Create backup of current state (safety!)
docker-compose -f docker-compose.prod.yml exec postgres \
  pg_dump -U $POSTGRES_USER $POSTGRES_DB > backups/pre-restore-backup-$(date +%Y%m%d-%H%M%S).sql

# 5. Drop and recreate database
docker-compose -f docker-compose.prod.yml exec postgres psql -U $POSTGRES_USER -d postgres -c "DROP DATABASE IF EXISTS $POSTGRES_DB;"
docker-compose -f docker-compose.prod.yml exec postgres psql -U $POSTGRES_USER -d postgres -c "CREATE DATABASE $POSTGRES_DB OWNER $POSTGRES_USER;"

# 6. Restore from backup
cat backups/prod-backup-20251030-020000.sql | \
  docker-compose -f docker-compose.prod.yml exec -T postgres psql -U $POSTGRES_USER -d $POSTGRES_DB

# 7. Verify restoration
docker-compose -f docker-compose.prod.yml exec postgres psql -U $POSTGRES_USER -d $POSTGRES_DB -c "\dt"

# 8. Start backend
docker-compose -f docker-compose.prod.yml start backend

# 9. Remove maintenance mode
# ... remove maintenance mode ...
```

## Database Shell Access

### psql (PostgreSQL Shell)

**Development:**
```bash
make shell-db
```

**Production:**
```bash
docker-compose -f docker-compose.prod.yml exec postgres psql -U $POSTGRES_USER -d $POSTGRES_DB
```

**Common psql commands:**
```sql
-- List tables
\dt

-- Describe table structure
\d users
\d+ users  -- With detailed info

-- List indexes
\di

-- List views
\dv

-- Show table sizes
\dt+

-- List functions
\df

-- List schemas
\dn

-- Execute SQL from file
\i /path/to/file.sql

-- Output to file
\o /tmp/output.txt
SELECT * FROM users;
\o

-- Quit
\q
```

### Running SQL Queries

**Quick query from host:**
```bash
# Development
docker-compose -f docker-compose.dev.yml exec postgres \
  psql -U bestays_user -d bestays_dev -c "SELECT COUNT(*) FROM users;"

# Production
docker-compose -f docker-compose.prod.yml exec postgres \
  psql -U $POSTGRES_USER -d $POSTGRES_DB -c "SELECT COUNT(*) FROM users;"
```

**Query from SQL file:**
```bash
cat query.sql | docker-compose -f docker-compose.dev.yml exec -T postgres \
  psql -U bestays_user -d bestays_dev
```

## pgvector Extension

The database includes pgvector extension for vector similarity search (LLM embeddings).

### Verify pgvector Installation

```sql
-- In psql
\dx
-- Should show: pgvector extension
```

### Using pgvector

**Create table with vector column:**
```sql
CREATE TABLE embeddings (
    id SERIAL PRIMARY KEY,
    content TEXT,
    embedding vector(1536)  -- OpenAI embedding dimension
);

-- Create index for similarity search
CREATE INDEX ON embeddings USING ivfflat (embedding vector_cosine_ops);
```

**Insert vectors:**
```sql
INSERT INTO embeddings (content, embedding)
VALUES ('Sample text', '[0.1, 0.2, 0.3, ...]');
```

**Similarity search:**
```sql
-- Find similar vectors
SELECT content, embedding <=> '[0.1, 0.2, 0.3, ...]' AS distance
FROM embeddings
ORDER BY embedding <=> '[0.1, 0.2, 0.3, ...]'
LIMIT 10;
```

## Troubleshooting

### Migration Fails

**Error:** "Target database is not up to date"
```bash
# Check current revision
make shell-server
alembic current

# Check history
alembic history

# Stamp database to specific revision if needed
alembic stamp head

exit
```

**Error:** "Can't locate revision"
```bash
# Verify migration files exist
ls apps/server/alembic/versions/

# Regenerate migration if needed
make shell-server
alembic revision --autogenerate -m "Regenerate migration"
exit
```

### Connection Refused

**Check if database is running:**
```bash
make status
```

**Check database health:**
```bash
make check
```

**Check connection from backend:**
```bash
make shell-server
echo $DATABASE_URL
python -c "import asyncpg; print('Connection OK')"
exit
```

### Database Locked

**Error:** "Database is locked" or "Could not access database"

**Solution:** Stop all connections:
```bash
# Restart database
make restart-db

# Or restart all services
make restart
```

### Backup/Restore Fails

**Error:** "Permission denied"

**Solution:** Check file permissions:
```bash
ls -l backups/
chmod 644 backups/*.sql
```

**Error:** "Database does not exist"

**Solution:** Create database first:
```bash
docker-compose -f docker-compose.dev.yml exec postgres \
  psql -U bestays_user -d postgres -c "CREATE DATABASE bestays_dev OWNER bestays_user;"
```

## Related Skills

- **devops-local-dev** - Docker Compose orchestration and service management

## Key Files

- `apps/server/alembic.ini` - Alembic configuration
- `apps/server/alembic/versions/` - Migration files
- `apps/server/alembic/env.py` - Migration environment
- `docker-compose.dev.yml` - Development database config
- `docker-compose.prod.yml` - Production database config

## Quick Reference

### Common Tasks

**Create migration:**
```bash
make shell-server
alembic revision --autogenerate -m "Description"
exit
```

**Apply migrations:**
```bash
make migrate
```

**Backup development database:**
```bash
docker-compose -f docker-compose.dev.yml exec postgres \
  pg_dump -U bestays_user bestays_dev | gzip > backups/backup-$(date +%Y%m%d-%H%M%S).sql.gz
```

**Access database shell:**
```bash
make shell-db
```

**Check migration status:**
```bash
make shell-server
alembic current
alembic history
exit
```

**Rollback one migration:**
```bash
make shell-server
alembic downgrade -1
exit
```
