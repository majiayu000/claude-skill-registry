---
name: supabase-deployment
description: Deploy Supabase schema changes, manage migrations, maintain production database integrity.
---

# Supabase Deployment

Deploy database migrations safely with idempotent SQL and multi-tenant isolation.

## When to Use
- Creating new database migrations
- Deploying schema changes to production
- Troubleshooting migration issues
- Setting up new environments

## Quick Start
```bash
# 1. Create migration
npx supabase migration new your_change_description

# 2. Write idempotent SQL (see refs/migration-patterns.md)

# 3. Test locally
npx supabase db reset

# 4. Generate types
npx supabase gen types typescript --local > src/lib/database/types/database-generated.ts

# 5. Deploy to production
npx supabase db push
```

## Project Details
- **Project ID:** `yvnuayzslukamizrlhwb`
- **Region:** `ap-southeast-2` (Sydney)
- **Pooler (6543):** Serverless, API routes
- **Direct (5432):** Migrations, admin ops

## Pre-Deployment Checklist
- [ ] Migration is idempotent (IF NOT EXISTS, OR REPLACE)
- [ ] Foreign keys have CASCADE/RESTRICT
- [ ] RLS policies created
- [ ] Indexes added for performance
- [ ] Types generated and committed
- [ ] Tested locally with `db reset`
- [ ] Cultural review (if storyteller-facing)

## Critical Tables (Review Required)
- `elder_review_queue` - Elder approval workflow
- `cultural_protocols` - Community protocols
- `consent_change_log` - GDPR audit trail

## Reference Files
| Topic | File |
|-------|------|
| Migration patterns | `refs/migration-patterns.md` |
| Deployment workflow | `refs/workflow.md` |
| Troubleshooting | `refs/troubleshooting.md` |

## Related Skills
- `supabase-connection` - Database clients
- `supabase-sql-manager` - SQL operations
- `cultural-review` - Cultural safety check
