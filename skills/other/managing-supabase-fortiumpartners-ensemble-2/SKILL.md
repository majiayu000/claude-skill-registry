---
name: managing-supabase
description: Supabase CLI for database management, Edge Functions, migrations, and local development. Use for managing Postgres databases, deploying serverless functions, and debugging Supabase projects.
---

# Supabase CLI Skill

## Table of Contents

1. [Quick Reference](#quick-reference)
2. [Critical: Avoiding Interactive Mode](#critical-avoiding-interactive-mode)
3. [Prerequisites](#prerequisites)
4. [Authentication](#authentication)
5. [CLI Decision Tree](#cli-decision-tree)
6. [Essential Commands](#essential-commands)
7. [Local Development Ports](#local-development-ports)
8. [Common Workflows](#common-workflows)
9. [Error Handling](#error-handling)
10. [Auto-Detection Triggers](#auto-detection-triggers)
11. [Agent Integration](#agent-integration)
12. [Quick Reference Card](#quick-reference-card)
13. [Further Reading](#further-reading)

---

## Quick Reference

Supabase CLI enables local development, database migrations, Edge Functions deployment, and project management for Supabase projects.

---

## Critical: Avoiding Interactive Mode

**Supabase CLI can enter interactive mode which will hang Claude Code.** Always use flags to bypass prompts:

| Command | WRONG (Interactive) | CORRECT (Non-Interactive) |
|---------|---------------------|---------------------------|
| Login | `supabase login` | Use `SUPABASE_ACCESS_TOKEN` env var |
| Link project | `supabase link` | `supabase link --project-ref <ref>` |
| Create project | `supabase projects create` | `supabase projects create <name> --org-id <id> --region <region>` |
| Start local | `supabase start` | `supabase start` (non-interactive by default) |
| Deploy functions | `supabase functions deploy` | `supabase functions deploy <name> --project-ref <ref>` |

**Never use in Claude Code**:
- `supabase login` without token (opens browser)
- Any command without `--project-ref` when not linked
- Interactive prompts for organization/region selection

**Always include**:
- `SUPABASE_ACCESS_TOKEN` environment variable for authentication
- `--project-ref` flag or pre-linked project
- Explicit flags for all configuration options

---

## Prerequisites

### Installation Verification

```bash
supabase --version
# Expected: 2.x.x or higher
```

### Installation Methods

```bash
# npm (requires Node.js 20+)
npm install -g supabase

# Homebrew (macOS/Linux)
brew install supabase/tap/supabase

# Scoop (Windows)
scoop bucket add supabase https://github.com/supabase/scoop-bucket.git
scoop install supabase
```

---

## Authentication

### Environment Variables (CI/CD Required)

| Variable | Purpose | Required For |
|----------|---------|--------------|
| `SUPABASE_ACCESS_TOKEN` | Personal access token | All remote operations |
| `SUPABASE_DB_PASSWORD` | Database password | `db push`, `db pull`, `link` |
| `SUPABASE_PROJECT_ID` | Project reference string | Linking without interactive prompt |

### Token Generation

Generate tokens at: `https://supabase.com/dashboard/account/tokens`

### Authentication Pattern for Claude Code

```bash
# Set from project .env file
export SUPABASE_ACCESS_TOKEN="$(grep SUPABASE_ACCESS_TOKEN .env | cut -d= -f2)"
export SUPABASE_DB_PASSWORD="$(grep SUPABASE_DB_PASSWORD .env | cut -d= -f2)"

# All commands will use these automatically
supabase projects list
supabase link --project-ref <ref>
```

---

## CLI Decision Tree

### What do you need to do?

```
Project Setup
├── Initialize local project ──────────► supabase init
├── Link to remote project ────────────► supabase link --project-ref <ref>
├── Start local stack ─────────────────► supabase start
├── Stop local stack ──────────────────► supabase stop
└── Check status ──────────────────────► supabase status

Database Operations
├── Create migration ──────────────────► supabase migration new <name>
├── Apply migrations locally ──────────► supabase db reset
├── Push migrations to remote ─────────► supabase db push
├── Pull remote schema ────────────────► supabase db pull
├── Diff local vs remote ──────────────► supabase db diff --linked
└── Lint database schema ──────────────► supabase db lint

Edge Functions
├── Create new function ───────────────► supabase functions new <name>
├── Serve locally ─────────────────────► supabase functions serve
├── Deploy function ───────────────────► supabase functions deploy <name>
├── List deployed functions ───────────► supabase functions list
└── Delete function ───────────────────► supabase functions delete <name>

Secrets Management
├── Set secret ────────────────────────► supabase secrets set NAME=value
├── Set from file ─────────────────────► supabase secrets set --env-file .env
├── List secrets ──────────────────────► supabase secrets list
└── Remove secret ─────────────────────► supabase secrets unset NAME

Type Generation
├── Generate TypeScript types ─────────► supabase gen types typescript --linked
└── Generate from local ───────────────► supabase gen types typescript --local

Debugging
├── View container logs ───────────────► supabase logs (local)
├── Check slow queries ────────────────► supabase inspect db outliers
└── View blocking queries ─────────────► supabase inspect db blocking
```

> For complete command reference including storage, project management, and all inspection commands, see [REFERENCE.md](REFERENCE.md).

---

## Essential Commands

### Project Setup

| Command | Description | Key Flags |
|---------|-------------|-----------|
| `supabase init` | Initialize local project | `--workdir` |
| `supabase start` | Start local development stack | `-x` (exclude services) |
| `supabase stop` | Stop local stack | `--no-backup` |
| `supabase status` | Show local container status | - |
| `supabase link` | Link to remote project | `--project-ref <ref>` (required) |

### Database Commands

| Command | Description | Key Flags |
|---------|-------------|-----------|
| `supabase db reset` | Reset local database | - |
| `supabase db push` | Push migrations to remote | `--dry-run`, `--include-seed` |
| `supabase db pull` | Pull schema from remote | `--schema <name>` |
| `supabase db diff` | Diff schema changes | `--linked`, `--local`, `-f <name>` |
| `supabase db lint` | Lint for schema errors | `--linked`, `--level <warning\|error>` |

### Migration Commands

| Command | Description | Key Flags |
|---------|-------------|-----------|
| `supabase migration new` | Create new migration | `<name>` (required) |
| `supabase migration list` | List migration history | `--db-url <url>` |
| `supabase migration up` | Apply pending migrations | `--local`, `--linked` |

### Edge Functions Commands

| Command | Description | Key Flags |
|---------|-------------|-----------|
| `supabase functions new` | Create new function | `<name>` (required) |
| `supabase functions serve` | Serve locally | `--env-file <path>` |
| `supabase functions deploy` | Deploy function(s) | `--no-verify-jwt`, `--project-ref` |
| `supabase functions delete` | Delete function | `<name>` (required) |

### Secrets Commands

| Command | Description | Key Flags |
|---------|-------------|-----------|
| `supabase secrets set` | Set secret(s) | `NAME=value`, `--env-file <path>` |
| `supabase secrets list` | List secrets | `--project-ref` |
| `supabase secrets unset` | Remove secret(s) | `<NAME>` |

> For type generation, database inspection, storage, and project management commands, see [REFERENCE.md](REFERENCE.md#complete-command-reference).

---

## Local Development Ports

| Service | Port | URL |
|---------|------|-----|
| API Gateway | 54321 | `http://localhost:54321` |
| Database | 54322 | `postgresql://postgres:postgres@localhost:54322/postgres` |
| Studio | 54323 | `http://localhost:54323` |
| Inbucket (Email) | 54324 | `http://localhost:54324` |

---

## Common Workflows

### 1. Initialize New Project

```bash
# Create local project structure
supabase init

# Link to existing remote project
export SUPABASE_ACCESS_TOKEN="your-token"
supabase link --project-ref <project-ref>

# Start local development
supabase start
```

### 2. Create and Apply Migrations

```bash
# Create new migration
supabase migration new add_users_table

# Edit migration file at supabase/migrations/<timestamp>_add_users_table.sql

# Apply locally
supabase db reset

# Push to remote
supabase db push
```

### 3. Pull Remote Schema Changes

```bash
# Link project first
supabase link --project-ref <ref>

# Pull all schema changes
supabase db pull

# Or create migration from remote changes
supabase db pull --schema public
```

### 4. Deploy Edge Functions

```bash
# Create new function
supabase functions new hello-world

# Edit supabase/functions/hello-world/index.ts

# Test locally
supabase functions serve

# Deploy to production
supabase functions deploy hello-world

# Deploy without JWT verification (for webhooks)
supabase functions deploy hello-world --no-verify-jwt
```

### 5. Manage Secrets

```bash
# Set individual secret
supabase secrets set STRIPE_KEY=sk_test_xxx

# Set from .env file
supabase secrets set --env-file .env.production

# List current secrets
supabase secrets list

# Remove secret
supabase secrets unset STRIPE_KEY
```

### 6. Generate TypeScript Types

```bash
# From remote database
supabase gen types typescript --linked > src/types/database.ts

# From local database
supabase gen types typescript --local > src/types/database.ts
```

### 7. Debug Database Performance

```bash
# Find slow queries
supabase inspect db outliers

# Check for blocking queries
supabase inspect db blocking

# Check cache hit ratios
supabase inspect db cache-hit
```

> For advanced workflows including CI/CD integration and migration strategies, see [REFERENCE.md](REFERENCE.md#advanced-patterns).

---

## Error Handling

### Common Errors and Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| `Error: You need to be logged in` | Missing access token | Set `SUPABASE_ACCESS_TOKEN` env var |
| `Error: Project ref is required` | No project linked | Use `--project-ref` or run `supabase link` |
| `Error: Cannot connect to Docker` | Docker not running | Start Docker Desktop |
| `Error: Port 54321 already in use` | Previous instance running | Run `supabase stop` first |
| `Error: Migration failed` | SQL syntax error | Check migration file syntax |

### Docker Issues

```bash
# Check if Docker is running
docker info

# Clean up Supabase containers
supabase stop --no-backup
docker system prune -f

# Restart with fresh state
supabase start
```

### Migration Conflicts

```bash
# View migration status
supabase migration list

# Repair migration history
supabase migration repair --status reverted <version>

# Squash migrations if needed
supabase migration squash --version <timestamp>
```

> For complete troubleshooting guide including permission issues and advanced debugging, see [REFERENCE.md](REFERENCE.md#troubleshooting).

---

## Auto-Detection Triggers

This skill auto-loads when Supabase context is detected:

**File-based triggers**:
- `supabase/config.toml` in project
- `supabase/` directory present
- `SUPABASE_ACCESS_TOKEN` in `.env` file

**Context-based triggers**:
- User mentions "Supabase"
- User runs supabase CLI commands
- Database migration discussions
- Edge Functions deployment

---

## Agent Integration

### Compatible Agents

| Agent | Use Case |
|-------|----------|
| `deployment-orchestrator` | Automated deployments, CI/CD |
| `infrastructure-developer` | Database provisioning |
| `deep-debugger` | Query analysis, performance debugging |
| `backend-developer` | Database schema, Edge Functions |
| `postgresql-specialist` | Advanced database operations |

### Handoff Patterns

**To Deep-Debugger**: Slow query investigation, migration failures, Edge Function runtime errors

**From Deep-Debugger**: Schema problems requiring migrations, environment variable changes

---

## Quick Reference Card

```bash
# Authentication (NEVER use supabase login in Claude Code)
export SUPABASE_ACCESS_TOKEN="xxx"

# Project setup
supabase init
supabase link --project-ref <ref>
supabase start
supabase stop

# Database
supabase migration new <name>
supabase db reset
supabase db push
supabase db pull
supabase db diff --linked

# Edge Functions
supabase functions new <name>
supabase functions serve
supabase functions deploy <name>

# Secrets
supabase secrets set KEY=value
supabase secrets list
supabase secrets unset KEY

# Types
supabase gen types typescript --linked > types.ts

# Debugging
supabase inspect db outliers
supabase inspect db blocking
```

---

## Further Reading

- [REFERENCE.md](REFERENCE.md) - Complete command reference, regions, CI/CD integration, advanced patterns
- [Supabase CLI Docs](https://supabase.com/docs/reference/cli/introduction)
- [Local Development Guide](https://supabase.com/docs/guides/local-development/cli/getting-started)
