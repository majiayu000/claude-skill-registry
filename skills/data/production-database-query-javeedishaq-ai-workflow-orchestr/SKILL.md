---
name: "production-database-query"
description: "Query Ballee production and staging databases safely using .env.local credentials (with 1Password fallback); use when debugging production/staging data, verifying data exists, investigating bugs, checking RLS behavior, applying hotfix migrations, or triggering Meteor sync"
version: "1.2.0"
last_updated: "2025-12-08"
---

# Production & Staging Database Query Skill

Query the Ballee production and staging databases safely using credentials from `.env.local` (with automatic 1Password fallback and caching).

## When to Use This Skill

Use this skill when:
- Debugging production/staging data issues
- Verifying data exists on production or staging
- Investigating user-reported bugs that require database inspection
- Checking RLS policy behavior in production/staging
- Analyzing production data for support requests
- Applying hotfix migrations to production or staging

## Supabase Project Reference

Ballee uses **two separate Supabase databases** for production and staging environments.

| Environment | Project Name | Project Reference ID | URL | Region |
|-------------|--------------|---------------------|-----|--------|
| **Production** | `ballee` | `csjruhqyqzzqxnfeyiaf` | `https://csjruhqyqzzqxnfeyiaf.supabase.co` | Central EU (Frankfurt) |
| **Staging** | `ballee-staging` | `hxpcknyqswetsqmqmeep` | `https://hxpcknyqswetsqmqmeep.supabase.co` | Central EU (Frankfurt) |

### Connection Pooler Hostnames

**Important**: Use `aws-1-eu-central-1` (not `aws-0`) for reliable connections.

**Production:**
- Session mode: `aws-1-eu-central-1.pooler.supabase.com:5432`
- Database user: `postgres.csjruhqyqzzqxnfeyiaf`

**Staging:**
- Session mode: `aws-1-eu-central-1.pooler.supabase.com:5432`
- Database user: `postgres.hxpcknyqswetsqmqmeep`

## Credential Management

### Environment Variables (Primary - Preferred)

Credentials are stored in `apps/web/.env.local`:

| Variable | Environment | Description |
|----------|-------------|-------------|
| `SUPABASE_DB_PASSWORD_PROD` | Production | Production database password |
| `SUPABASE_DB_PASSWORD_STAGING` | Staging | Staging database password |

### 1Password (Fallback - Auto-cache)

If environment variables are not set, credentials will be fetched from 1Password and cached to `.env.local`:

| Credential | 1Password Item ID | 1Password Field | Environment |
|------------|------------------|-----------------|-------------|
| Production DB Password | `kuyspxxlyi2mxg7nfeb6dm3pje` | `notesPlain` | Production |
| Staging DB Password | `rkzjnr5ffy5u6iojnsq3clnmia` | `notesPlain` | Staging |
| Supabase Access Token | `uipc6jse6q32hu3nyfh6qmssoq` | `password` | Both |

## Prerequisites

- PostgreSQL client tools installed (`psql`)
- Credentials in `.env.local` OR 1Password CLI installed and authenticated (`op whoami`)

## Quick Reference Commands

### Production Database

```bash
# Load password from .env.local (or fetch from 1Password and cache)
source apps/web/.env.local 2>/dev/null
if [ -z "$SUPABASE_DB_PASSWORD_PROD" ]; then
  SUPABASE_DB_PASSWORD_PROD="$(op item get kuyspxxlyi2mxg7nfeb6dm3pje --fields notesPlain --reveal)"
  echo "SUPABASE_DB_PASSWORD_PROD=$SUPABASE_DB_PASSWORD_PROD" >> apps/web/.env.local
fi

# Connect to production
PGPASSWORD="$SUPABASE_DB_PASSWORD_PROD" psql \
  "postgresql://postgres.csjruhqyqzzqxnfeyiaf@aws-1-eu-central-1.pooler.supabase.com:5432/postgres"

# Execute single query on production
PGPASSWORD="$SUPABASE_DB_PASSWORD_PROD" psql \
  "postgresql://postgres.csjruhqyqzzqxnfeyiaf@aws-1-eu-central-1.pooler.supabase.com:5432/postgres" \
  -c "SELECT * FROM events LIMIT 5;"

# Apply migration to production
PGPASSWORD="$SUPABASE_DB_PASSWORD_PROD" psql \
  "postgresql://postgres.csjruhqyqzzqxnfeyiaf@aws-1-eu-central-1.pooler.supabase.com:5432/postgres" \
  -f apps/web/supabase/migrations/YYYYMMDDHHMMSS_description.sql
```

### Staging Database

```bash
# Load password from .env.local (or fetch from 1Password and cache)
source apps/web/.env.local 2>/dev/null
if [ -z "$SUPABASE_DB_PASSWORD_STAGING" ]; then
  SUPABASE_DB_PASSWORD_STAGING="$(op item get rkzjnr5ffy5u6iojnsq3clnmia --fields notesPlain --reveal)"
  echo "SUPABASE_DB_PASSWORD_STAGING=$SUPABASE_DB_PASSWORD_STAGING" >> apps/web/.env.local
fi

# Connect to staging
PGPASSWORD="$SUPABASE_DB_PASSWORD_STAGING" psql \
  "postgresql://postgres.hxpcknyqswetsqmqmeep@aws-1-eu-central-1.pooler.supabase.com:5432/postgres"

# Execute single query on staging
PGPASSWORD="$SUPABASE_DB_PASSWORD_STAGING" psql \
  "postgresql://postgres.hxpcknyqswetsqmqmeep@aws-1-eu-central-1.pooler.supabase.com:5432/postgres" \
  -c "SELECT * FROM events LIMIT 5;"

# Apply migration to staging
PGPASSWORD="$SUPABASE_DB_PASSWORD_STAGING" psql \
  "postgresql://postgres.hxpcknyqswetsqmqmeep@aws-1-eu-central-1.pooler.supabase.com:5432/postgres" \
  -f apps/web/supabase/migrations/YYYYMMDDHHMMSS_description.sql
```

## Dashboard SQL Editor URLs

**Production:** `https://supabase.com/dashboard/project/csjruhqyqzzqxnfeyiaf/sql/new`
**Staging:** `https://supabase.com/dashboard/project/hxpcknyqswetsqmqmeep/sql/new`

## Common Queries

### Check Hire Order Status

```sql
SELECT
  ho.id,
  ho.order_number,
  ho.status,
  ho.dancer_approved_at,
  ho.estimated_total,
  ho.created_at,
  cr.role_name,
  e.title as event_title
FROM hire_orders ho
LEFT JOIN cast_roles cr ON ho.cast_role_id = cr.id
LEFT JOIN events e ON ho.event_id = e.id
WHERE ho.event_id = 'event-uuid'
ORDER BY ho.created_at DESC;
```

### Check Event Participation

```sql
SELECT
  ep.id,
  ep.status,
  ep.created_at,
  p.first_name,
  p.last_name,
  p.email
FROM event_participants ep
LEFT JOIN profiles p ON ep.user_id = p.id
WHERE ep.event_id = 'event-uuid'
ORDER BY ep.created_at DESC;
```

### Check Cast Assignments

```sql
SELECT
  ca.id,
  ca.assignment_status,
  ca.rate,
  cr.role_name,
  p.first_name,
  p.last_name
FROM cast_assignments ca
LEFT JOIN cast_roles cr ON ca.cast_role_id = cr.id
LEFT JOIN profiles p ON ca.user_id = p.id
WHERE ca.event_id = 'event-uuid';
```

### Check RLS Policies for a Table

```sql
SELECT schemaname, tablename, policyname, permissive, roles, cmd, qual
FROM pg_policies
WHERE tablename = 'hire_orders';
```

### Check Migration Status

```sql
SELECT version, name, statements
FROM supabase_migrations.schema_migrations
ORDER BY version DESC
LIMIT 20;
```

## Recording Migrations After Manual Application

After applying a migration manually, record it in the tracking table:

```sql
INSERT INTO supabase_migrations.schema_migrations (version, name, statements)
VALUES ('YYYYMMDDHHMMSS', 'migration_name', ARRAY['SQL_STATEMENT'])
ON CONFLICT (version) DO NOTHING;
```

## Safety Features

- **Read-only by default**: Prevents accidental data modification
- **Credential management**: Uses 1Password for secure credential storage
- **Connection pooling**: Uses Supabase pooler for reliable connections
- **Query logging**: All queries are logged for audit trail

## Error Handling

**1Password not authenticated:**
```bash
op signin
# Follow authentication flow
```

**psql not installed:**
```bash
brew install postgresql@16
```

**Connection timeout / "Tenant or user not found":**
- Use `aws-1-eu-central-1.pooler.supabase.com` (not `aws-0`)
- Verify credentials in 1Password
- Check network connection

## Best Practices

1. **Test on staging first**: Always test queries on staging before production
2. **Read-only by default**: Only use write operations when absolutely necessary
3. **Limit results**: Use `LIMIT` clause to avoid large result sets
4. **Use transactions**: For multiple queries, use transactions to ensure consistency
5. **Log queries**: Keep a record of production queries for audit purposes
6. **Record migrations**: After manual migration, always record in `schema_migrations`

## MongoDB (Meteor Legacy) Database Access

The Ballee legacy Meteor app uses a MongoDB database hosted on Zerion (zcloud.ws). This is used for syncing data from the old community app.

### MongoDB Credentials

| Credential | 1Password Item | Description |
|------------|----------------|-------------|
| MongoDB URL | `Ballee Meteor MongoDB URL` | Full connection string with credentials |
| DB Username | `root` | MongoDB admin user |
| DB Name | `meteor` | Database name |

### Connection String Format

```
mongodb://root:<password>@mdb-p-0.ballee.db-eu2.zcloud.ws:60601,mdb-p-1.ballee.db-eu2.zcloud.ws:60602,mdb-p-2.ballee.db-eu2.zcloud.ws:60603/meteor?authSource=admin&ssl=true&tlsInsecure=true&replicaSet=mdb-p
```

### Getting MongoDB URL

```bash
# From 1Password
op read "op://Private/Ballee Meteor MongoDB URL/password"
```

### Meteor Sync CLI

For syncing data from MongoDB to Supabase staging, use the CLI tool:

```bash
# Set environment variables
export METEOR_SYNC_API_KEY="$(op read 'op://Private/Ballee Meteor Sync API Key/password')"
export STAGING_URL="https://ballee-git-feat-community-app-antoineschallers.vercel.app"

# Available commands
pnpm meteor:staging status    # Check MongoDB connection
pnpm meteor:staging history   # View sync history
pnpm meteor:staging trigger   # Trigger full sync
pnpm meteor:staging trigger --type incremental
pnpm meteor:staging trigger --entity organization
pnpm meteor:staging logs <runId>
pnpm meteor:staging stats
```

### Vercel Environment Variables for Meteor Sync

| Variable | Environment | Description |
|----------|-------------|-------------|
| `METEOR_MONGO_URL` | Preview/Production | Full MongoDB connection URL |
| `METEOR_SYNC_API_KEY` | Preview/Production | API key for sync endpoint auth |

## Related Documentation

- Production Database Access: `apps/web/supabase/CLAUDE.md`
- SQL Debugging Tool: `.claude/skills/production-database-query/scripts/sql-exec.sh`
- Database Migration Manager: `.claude/skills/database-migration-manager/SKILL.md`
- Meteor Sync CLI: `scripts/meteor-sync/README.md`
- 1Password CLI: https://developer.1password.com/docs/cli
