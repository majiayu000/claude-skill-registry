---
name: deploy
description: Safe deployment workflow for Fly.io and infrastructure changes. Use before ANY deployment, config modification, or infrastructure change. Prevents panic-driven debugging and production incidents.
---

# Deployment Discipline

## The Golden Rules

1. **LOCAL FIRST, ALWAYS** - Never deploy until local tests pass
2. **ONE CHANGE AT A TIME** - Make one fix, test it, verify it works, then proceed
3. **UNDERSTAND BEFORE FIXING** - Don't conflate unrelated errors
4. **NOTIFICATIONS ARE PRODUCTION** - Failed deployments spam Slack

## Pre-Deployment Checklist

Before ANY deployment:

```bash
# 1. Test locally first
source .venv/bin/activate
python scripts/run_pipeline.py everflow

# 2. Check what changed
git diff

# 3. Verify no broken imports
python -c "from signalroom.workers.main import main; print('OK')"
```

## Fly.io Deployment

```bash
# Deploy (builds and pushes)
fly deploy

# Check status
fly status

# View logs
fly logs

# Check secrets are set
fly secrets list
```

## Known Working Configuration

**Supabase Pooler (REQUIRED for Fly.io):**
- Host: `aws-0-us-east-1.pooler.supabase.com`
- Port: `6543`
- User: `postgres.{project_ref}` (NOT just `postgres`)

**Temporal Cloud:**
- Address: `ap-northeast-1.aws.api.temporal.io:7233`
- Namespace: `signalroom-713.nzg5u`

## If Something Breaks

**STOP. Do not deploy again.**

1. Check what you changed: `git diff`
2. Revert if needed: `git checkout -- <file>`
3. Test locally before any retry
4. Ask: "What was working before, and what did I change?"

## Secrets with Special Characters

Passwords with backticks, quotes, or special chars:
- **Do NOT use CLI** - shell escaping will break them
- **Use Fly.io dashboard** - Settings > Secrets > Set manually

## Rollback

```bash
# List recent deployments
fly releases

# Rollback to previous
fly deploy --image <previous-image>
```
