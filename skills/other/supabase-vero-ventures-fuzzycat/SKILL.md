---
name: supabase
description: >
  Manage Supabase projects via CLI and Management API. List projects, check auth config,
  manage users, update settings, query databases, and inspect project health.
  Use for any Supabase administration task.
allowed-tools: Bash, Read, Grep, Glob
---

# Supabase CLI & Management API

Manage FuzzyCat's Supabase projects via the CLI (`npx supabase`) and the Management API.

## Projects

| Name | Ref | Purpose |
|------|-----|---------|
| FuzzyCatApp | `wrqwmpptetipbccxzeai` | Production |
| fuzzycat-dev | `nkndduzbzshjaaeicmad` | Development |

## Authentication

```bash
# Source credentials from .env.local
source <(grep -E '^(SUPABASE_ACCESS_TOKEN|SUPABASE_SERVICE_ROLE_KEY|NEXT_PUBLIC_SUPABASE_URL|DATABASE_URL)=' .env.local | sed 's/^/export /')

# For Management API (cross-project admin)
export SUPABASE_ACCESS_TOKEN  # from .env.local

# For project-specific operations
export SUPABASE_SERVICE_ROLE_KEY  # from .env.local (dev) or vercel env pull (prod)
```

## CLI Commands (`npx supabase`)

```bash
# Project management
npx supabase projects list
npx supabase db dump --project-ref wrqwmpptetipbccxzeai  # dump production schema
npx supabase db diff --project-ref wrqwmpptetipbccxzeai   # compare local vs remote schema

# Database operations (use DATABASE_URL from .env.local for dev)
npx supabase db push --project-ref nkndduzbzshjaaeicmad   # push schema to dev
```

## Management API (REST)

All Management API calls use `https://api.supabase.com/v1/` with the access token.

```bash
TOKEN=$(grep SUPABASE_ACCESS_TOKEN .env.local | cut -d'"' -f2)
PROJECT="wrqwmpptetipbccxzeai"  # or nkndduzbzshjaaeicmad for dev

# List projects
curl -s "https://api.supabase.com/v1/projects" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool

# Get auth config
curl -s "https://api.supabase.com/v1/projects/$PROJECT/config/auth" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool

# Update auth config (PATCH)
curl -s -X PATCH "https://api.supabase.com/v1/projects/$PROJECT/config/auth" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"site_url": "https://www.fuzzycatapp.com"}'

# Get project health
curl -s "https://api.supabase.com/v1/projects/$PROJECT/health" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
```

## Auth Admin API (per-project)

Uses the project's service role key directly against the Supabase instance.

```bash
SUPABASE_URL=$(grep NEXT_PUBLIC_SUPABASE_URL .env.local | cut -d'"' -f2)
SERVICE_KEY=$(grep SUPABASE_SERVICE_ROLE_KEY .env.local | cut -d'"' -f2)

# List users
curl -s "$SUPABASE_URL/auth/v1/admin/users" \
  -H "apikey: $SERVICE_KEY" \
  -H "Authorization: Bearer $SERVICE_KEY" | python3 -m json.tool

# Get specific user
curl -s "$SUPABASE_URL/auth/v1/admin/users/<user-id>" \
  -H "apikey: $SERVICE_KEY" \
  -H "Authorization: Bearer $SERVICE_KEY"

# Create user
curl -s -X POST "$SUPABASE_URL/auth/v1/admin/users" \
  -H "apikey: $SERVICE_KEY" \
  -H "Authorization: Bearer $SERVICE_KEY" \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"...","email_confirm":true,"user_metadata":{"role":"owner"}}'

# Update user (e.g., reset password)
curl -s -X PUT "$SUPABASE_URL/auth/v1/admin/users/<user-id>" \
  -H "apikey: $SERVICE_KEY" \
  -H "Authorization: Bearer $SERVICE_KEY" \
  -H "Content-Type: application/json" \
  -d '{"password":"new-password"}'

# Delete user
curl -s -X DELETE "$SUPABASE_URL/auth/v1/admin/users/<user-id>" \
  -H "apikey: $SERVICE_KEY" \
  -H "Authorization: Bearer $SERVICE_KEY"
```

## Production Access

To get production credentials:
```bash
vercel env pull /tmp/prod-env.txt --environment production 2>&1
grep SUPABASE /tmp/prod-env.txt
```

## Common Tasks

- **Check site URL / redirect config**: GET auth config, check `site_url` and `uri_allow_list`
- **Manage users**: Use Auth Admin API with service role key
- **Schema changes**: `bunx drizzle-kit push` (dev) or `bunx drizzle-kit migrate` (prod)
- **Debug auth issues**: Check `rate_limit_email_sent`, `mailer_autoconfirm`, SMTP settings
