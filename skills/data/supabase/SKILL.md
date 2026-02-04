---
name: supabase
description: Supabase CLI patterns - replaces MCP (more reliable)
allowed-tools: Bash
model: haiku
user-invocable: false
---

# Supabase CLI

Use CLI instead of MCP - more reliable, fewer permission issues.

## Common Commands

```bash
# Apply migrations (limit output)
supabase db push --project-ref PROJECT_ID 2>&1 | tail -10

# Run SQL directly
supabase db execute --sql "SELECT * FROM table LIMIT 5" --project-ref PROJECT_ID

# Deploy edge functions
supabase functions deploy FUNCTION_NAME --project-ref PROJECT_ID

# Deploy all functions
supabase functions deploy --project-ref PROJECT_ID

# List projects
supabase projects list

# Check status
supabase status --project-ref PROJECT_ID
```

## Context-Efficient Patterns

```bash
# Limit output to reduce context
supabase db push 2>&1 | tail -5

# Check if migration exists before applying
supabase db execute --sql "SELECT 1 FROM table LIMIT 1" 2>&1 | grep -q "1" && echo "exists"

# Run in background for long operations
Bash({ command: "supabase functions deploy --project-ref X", run_in_background: true })
```

## Project IDs

Get from CLAUDE.md or:
```bash
supabase projects list 2>&1 | grep -E "^\w"
```

## Multi-Org Auth

CLI only supports one token at a time. For multiple orgs, use per-command token:

```bash
# Option 1: Inline token (best for multi-org)
SUPABASE_ACCESS_TOKEN=$SUPABASE_TOKEN_REELR supabase db push --project-ref XXX

# Option 2: Source project's .env.local first
source .env.local && supabase db push --project-ref $SUPABASE_PROJECT_ID

# Option 3: Use --db-url with connection string (bypasses auth)
supabase db execute --db-url "postgresql://postgres:PASSWORD@db.XXX.supabase.co:5432/postgres" --sql "..."
```

**Project .env.local should have:**
```env
SUPABASE_ACCESS_TOKEN=sbp_xxx
SUPABASE_PROJECT_ID=xxx
SUPABASE_DB_PASSWORD=xxx
```

## Direct psql (Most Reliable)

**Use Pooler URL (IPv4 compatible), not direct connection:**
```bash
# ❌ Direct - IPv6 only, won't work on most networks
# psql "postgresql://postgres:PASS@db.REF.supabase.co:5432/postgres"

# ✅ Pooler - IPv4 compatible (use this)
psql "postgresql://postgres.REF:PASS@aws-0-REGION.pooler.supabase.com:6543/postgres" -c "SELECT 1"
```

Get pooler URL: Dashboard → Connect → Connection String → Session Pooler

## Skip MCP

MCP has permission issues. Always prefer CLI or psql:
- More reliable
- Better error messages
- Multi-org support via env vars
- Output can be limited
