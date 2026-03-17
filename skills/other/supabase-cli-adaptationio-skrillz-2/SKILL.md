---
name: supabase-cli
description: Supabase CLI commands for local development, migrations, project management, and deployment. Use when working with Supabase CLI, starting local dev, managing migrations, or deploying changes.
---

# Supabase CLI Skill

Complete CLI command reference for Supabase development.

## Quick Reference

| Task | Command |
|------|---------|
| Install CLI | `npm install supabase --save-dev` |
| Login | `supabase login` |
| Init project | `supabase init` |
| Link to remote | `supabase link --project-ref <ref>` |
| Start local stack | `supabase start` |
| Stop local stack | `supabase stop` |
| Check status | `supabase status` |
| Create migration | `supabase migration new <name>` |
| Push to remote | `supabase db push` |
| Pull from remote | `supabase db pull` |
| Reset local DB | `supabase db reset` |
| Generate types | `supabase gen types typescript --local > types.ts` |

## Installation

```bash
# NPM (recommended for projects)
npm install supabase --save-dev
npx supabase [command]

# Homebrew (macOS/Linux)
brew install supabase/tap/supabase

# Scoop (Windows)
scoop bucket add supabase https://github.com/supabase/scoop-bucket.git
scoop install supabase
```

**Prerequisites**: Docker (required for local development)

## Project Setup

### Initialize Project

```bash
supabase init
```

Creates:
- `supabase/config.toml` - Configuration file
- `supabase/migrations/` - Migration files
- `supabase/seed.sql` - Seed data

### Link to Remote Project

```bash
supabase link --project-ref <project-ref>
```

Get project ref from: Dashboard → Project Settings → General

## Local Development

### Start Local Stack

```bash
supabase start
```

Starts:
- PostgreSQL database
- PostgREST API
- GoTrue Auth
- Realtime server
- Storage service
- Studio dashboard
- Inbucket (email testing)

**Output URLs**:
```
API URL: http://localhost:54321
DB URL: postgresql://postgres:postgres@localhost:54322/postgres
Studio URL: http://localhost:54323
Inbucket URL: http://localhost:54324
```

### Stop Local Stack

```bash
# Stop and save data
supabase stop

# Stop and delete all data
supabase stop --no-backup
```

### Check Status

```bash
supabase status
```

Shows URLs, API keys, and service status.

## Database Commands

### Create Migration

```bash
supabase migration new create_users_table
```

Creates: `supabase/migrations/<timestamp>_create_users_table.sql`

### Generate Migration from Changes

```bash
# Make changes locally, then generate migration
supabase db diff -f my_schema_changes

# Diff against specific schemas
supabase db diff -f changes --schema public,extensions
```

### Apply Migrations

```bash
# Apply pending migrations locally
supabase migration up

# Push to remote
supabase db push

# Preview what would be pushed
supabase db push --dry-run
```

### Pull Remote Changes

```bash
supabase db pull
```

Creates migration from Dashboard changes.

### Reset Local Database

```bash
supabase db reset
```

Recreates database and applies all migrations.

### List Migrations

```bash
supabase migration list
```

Shows local vs remote migration status.

### Rollback Migrations

```bash
# Rollback last n migrations
supabase migration down --count 1

# Rollback specific number
supabase migration down --count 3
```

### Squash Migrations

```bash
# Combine multiple migrations into one
supabase migration squash --version 20240101000000

# Squash all migrations up to version
supabase migration squash --version <target_version>
```

Useful for cleaning up migration history before release.

## Type Generation

### Generate TypeScript Types

```bash
# From local database
supabase gen types typescript --local > database.types.ts

# From linked remote
supabase gen types typescript --linked > database.types.ts

# From specific project
supabase gen types typescript --project-id "your-id" > database.types.ts
```

## Edge Functions

### Create Function

```bash
supabase functions new hello-world
```

Creates: `supabase/functions/hello-world/index.ts`

### Serve Locally

```bash
# Serve all functions
supabase functions serve

# Serve specific function
supabase functions serve hello-world

# With env file and no JWT
supabase functions serve --env-file .env --no-verify-jwt
```

### Deploy

```bash
# Deploy all functions
supabase functions deploy

# Deploy specific function
supabase functions deploy hello-world

# Deploy without JWT verification (for webhooks)
supabase functions deploy webhook-handler --no-verify-jwt
```

### Test Function

```bash
curl -i --request POST \
  'http://localhost:54321/functions/v1/hello-world' \
  --header 'Authorization: Bearer <ANON_KEY>' \
  --header 'Content-Type: application/json' \
  --data '{"name":"Functions"}'
```

## Secrets Management

```bash
# Set secret
supabase secrets set API_KEY=abc123

# Set multiple secrets
supabase secrets set API_KEY=abc123 DB_PASSWORD=secret

# Set from .env file
supabase secrets set --env-file .env

# List secrets
supabase secrets list

# Remove secret
supabase secrets unset API_KEY
```

## Project Management

```bash
# List organizations
supabase orgs list

# List projects
supabase projects list

# Create project
supabase projects create <name> --org-id <id> --region <region>

# Delete project
supabase projects delete --project-ref <ref>

# Update remote config from local
supabase projects update-config
```

## Database Inspection

```bash
# Cache hit ratio
supabase inspect db cache-hit --linked

# Unused indexes
supabase inspect db unused-indexes --local

# Table bloat
supabase inspect db bloat --linked

# Long running queries
supabase inspect db long-running-queries --linked

# Active connections
supabase inspect db role-connections --linked
```

## Backup & Restore

### Backup

```bash
# Dump roles
supabase db dump --linked -f roles.sql --role-only

# Dump schema
supabase db dump --linked -f schema.sql

# Dump data
supabase db dump --linked -f data.sql --use-copy --data-only
```

### Restore

```bash
psql --single-transaction \
  --file roles.sql \
  --file schema.sql \
  --command 'SET session_replication_role = replica' \
  --file data.sql \
  --dbname [CONNECTION_STRING]
```

## Common Flags

| Flag | Description |
|------|-------------|
| `--debug` | Verbose output |
| `--local` | Use local database |
| `--linked` | Use linked remote |
| `--project-ref <ref>` | Specific project |
| `--db-url <url>` | Connection string |
| `--dry-run` | Preview without executing |
| `-f <file>` | Output to file |

## References

- [local-development.md](references/local-development.md) - Local stack setup
- [migrations.md](references/migrations.md) - Migration workflow
- [config-toml.md](references/config-toml.md) - Configuration options
