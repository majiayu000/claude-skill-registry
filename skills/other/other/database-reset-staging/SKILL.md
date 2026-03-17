---
name: database-reset-staging
description: Resets staging database with full schema drop. Use for schema changes or migrations. SINGLE SOURCE OF TRUTH for staging database reset automation.
---

# Database Reset Staging Skill

**Purpose**: Full database reset for staging environment - drops all tables and lets migrations rebuild.

**When to Use**:
- Schema changes requiring clean slate
- Migration conflicts with existing tables
- Database corruption or inconsistencies
- After major refactoring

**When NOT to Use**:
- Just need fresh seed data (use selective delete instead, see database guide)
- Production database (NEVER - this is staging only)

**Background Documentation**: See `/docs/guides-setup/database-setup.md` (Staging Database Management section) for context and manual procedures.

## 🚨 CRITICAL WARNINGS

**This skill performs DESTRUCTIVE operations:**
- ❌ ALL data in staging database will be DELETED
- ❌ All tables will be DROPPED (not schemas - managed DB limitation)
- ❌ Cannot be undone
- ✅ ONLY affects staging database (`pgbouncer-staging`)
- ✅ Migrations will rebuild tables automatically

**Note**: DigitalOcean managed databases don't allow dropping the `public` schema (owned by `doadmin`). This skill drops all tables owned by `witchcity_staging` user instead.

**Prerequisites:**
- Staging code already deployed (use `staging-deploy` skill first)
- Database backup if needed (though staging data is expendable)

---

## How to Use This Skill

**Executable Script**: `execute.sh`

```bash
# From project root - with confirmation prompt
bash .claude/skills/database-reset-staging/execute.sh

# Skip confirmation prompt (for automation)
SKIP_CONFIRMATION=true bash .claude/skills/database-reset-staging/execute.sh
```

**What the script does**:
1. Shows pre-flight information (purpose, when/when NOT to use, destructive operation warnings)
2. Requires confirmation before proceeding (skippable with env var)
3. Validates prerequisites:
   - SSH key accessible
   - PostgreSQL client installed (psql)
   - Server connectivity
4. Retrieves database credentials from staging server (from `.env.staging`)
5. Stops API container
6. Drops all tables owned by `witchcity_staging` user (CASCADE)
7. Starts containers (migrations run automatically)
8. Waits for database initialization
9. Verifies tables rebuilt
10. Runs health check
11. Reports summary

**Script includes CRITICAL safety warnings** - this is a DESTRUCTIVE operation that cannot be undone.

---

## Manual Override (Emergency Only)

If skill fails, manual steps:

**Prerequisites**: Get DB credentials from server first
```bash
ssh witchcity@104.131.165.14 'cat /opt/witchcityrope/staging/.env.staging | grep STAGING_DB_CONNECTION_STRING'
```

**Manual table drop:**
Connect to database and execute:
```sql
-- Generate DROP statements for all tables owned by witchcity_staging
SELECT 'DROP TABLE IF EXISTS "' || tablename || '" CASCADE;'
FROM pg_tables
WHERE schemaname = 'public' AND tableowner = 'witchcity_staging';

-- Then execute the generated statements
```

**Then**: Restart staging containers via SSH:
```bash
ssh witchcity@104.131.165.14 'cd /opt/witchcityrope/staging && docker compose -f docker-compose.staging.yml up -d --force-recreate api'
```

---

## Common Issues & Solutions

### Issue: psql command not found

**Cause**: PostgreSQL client not installed locally

**Solution**:
```bash
# Ubuntu/Debian
sudo apt install postgresql-client

# macOS
brew install postgresql
```

### Issue: Connection timeout

**Cause**: Firewall or network issue

**Solution**:
1. Verify server is accessible: `ssh witchcity@104.131.165.14`
2. Check staging containers: Use `restart-dev-containers` skill
3. Verify database port is open (25060)

### Issue: Migrations fail after reset

**Cause**: Old migration state or code/DB mismatch

**Solution**:
1. Check API logs: `restart-dev-containers` skill
2. Ensure latest code deployed: `staging-deploy` skill
3. Verify no lingering tables: Run query to list all tables

### Issue: Seed data not populating

**Cause**: Seed condition not met

**Solution**:
- API only seeds if `appsettings.Staging.json` has `SeedData: true`
- Check environment configuration on server
- Manual trigger: Restart API container with `restart-dev-containers` skill

---

## Integration with Process

**Typical workflow:**
1. Make schema changes locally
2. Test migrations locally
3. Deploy code: Use `staging-deploy` skill
4. Reset database: Use THIS skill
5. Verify: Use `restart-dev-containers` skill to check logs

---

## Version History

- **2025-12-09**: Fixed to drop tables instead of schemas (DigitalOcean managed DB limitation)
  - `witchcity_staging` user cannot drop `public` schema (owned by `doadmin`)
  - Now drops all tables owned by `witchcity_staging` with CASCADE
- **2025-11-05**: Created as automation wrapper for staging database reset
- Extracted from: `docs/functional-areas/deployment/staging-deployment-guide.md`
- Complements: `docs/guides-setup/database-setup.md`

---

**Remember**: This skill is for staging only. Never use on production. Always use `staging-deploy` skill first to ensure latest code is deployed.
