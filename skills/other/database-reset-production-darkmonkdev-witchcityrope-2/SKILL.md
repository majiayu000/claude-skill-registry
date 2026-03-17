---
name: database-reset-production
description: Resets production database with full schema drop. EXTREME CAUTION - deletes all production data. SINGLE SOURCE OF TRUTH for production database reset automation.
---

# Database Reset Production Skill

**Purpose**: Full database schema reset for PRODUCTION environment - drops all schemas and lets migrations rebuild.

**⚠️ EXTREME CAUTION: THIS IS FOR PRODUCTION DATABASE ⚠️**

**When to Use**:
- CRITICAL schema changes that cannot be migrated
- Database corruption beyond repair
- After explicit approval from stakeholders
- During planned maintenance window

**When NOT to Use**:
- You're not 100% certain this is necessary
- Production has live user data (will be permanently deleted)
- You haven't taken a complete database backup
- This is during business hours
- You haven't notified all stakeholders

**Background Documentation**: See `/docs/guides-setup/database-setup.md` (Production Database Management section) for context and manual procedures.

## 🚨 CRITICAL WARNINGS

**This skill performs DESTRUCTIVE operations:**
- ❌ **ALL PRODUCTION DATA WILL BE PERMANENTLY DELETED**
- ❌ User accounts, events, payments, vetting records - EVERYTHING
- ❌ All `public`, `cms`, AND `hangfire` schemas will be DROPPED
- ❌ **CANNOT BE UNDONE**
- ✅ ONLY affects production database (`witchcityrope_production`)
- ✅ Migrations will rebuild schema automatically
- ✅ All users will need to re-register

**Prerequisites:**
- **COMPLETE DATABASE BACKUP VERIFIED**
- Production code already deployed (use `production-deploy` skill first)
- **Stakeholder approval documented**
- **Maintenance window scheduled**
- **Rollback plan prepared**

---

## How to Use This Skill

**Executable Script**: `execute.sh`

```bash
# From project root - with DOUBLE confirmation prompt
bash .claude/skills/database-reset-production/execute.sh

# Skip confirmation prompt (for automation - USE WITH EXTREME CAUTION)
SKIP_CONFIRMATION=true bash .claude/skills/database-reset-production/execute.sh
```

**What the script does**:
1. Shows pre-flight information with EXTREME warnings
2. Requires DOUBLE confirmation before proceeding:
   - First: Type "DELETE PRODUCTION DATA" exactly
   - Second: Type "yes" to final confirmation
3. Validates prerequisites:
   - SSH key accessible
   - PostgreSQL client installed (psql)
   - Server connectivity
4. Retrieves database credentials from production server
5. Stops production containers
6. Drops all database schemas (public + cms + hangfire)
7. Recreates public schema
8. Starts containers (migrations run automatically)
9. Waits for database initialization
10. Verifies schema rebuild
11. Runs health check
12. Reports summary

**Script includes MULTIPLE safety warnings** - this is a DESTRUCTIVE operation that CANNOT be undone.

---

## Manual Override (Emergency Only)

If skill fails, manual steps:

**Prerequisites**: Get DB credentials from server first

**Manual schema drop:**
Connect to database and execute:
```sql
DROP SCHEMA IF EXISTS public CASCADE;
CREATE SCHEMA public;
DROP SCHEMA IF EXISTS cms CASCADE;
DROP SCHEMA IF EXISTS hangfire CASCADE;
```

**Then**: Restart production containers manually

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
2. Check production containers status
3. Verify database port is open (25060)

### Issue: Migrations fail after reset

**Cause**: Old migration state or code/DB mismatch

**Solution**:
1. Check API logs
2. Ensure latest code deployed: `production-deploy` skill
3. Verify no lingering tables: Run query to list all tables

### Issue: Seed data not populating

**Cause**: Seed condition not met

**Solution**:
- API only seeds if `appsettings.Production.json` has `SeedData: true`
- Check environment configuration on server
- Manual trigger: Restart API container

---

## Integration with Process

**Typical workflow:**
1. **BACKUP PRODUCTION DATABASE** (verify backup is restorable)
2. Schedule maintenance window
3. Notify all stakeholders
4. Deploy code: Use `production-deploy` skill
5. Place maintenance page
6. Reset database: Use THIS skill
7. Verify migrations and seed data
8. Test critical endpoints
9. Remove maintenance page
10. Notify stakeholders

---

## Security Considerations

**Database User**: `witchcity_production`
- Environment-specific maintenance user
- Has full permissions on `witchcityrope_production` database ONLY
- Cannot affect other databases
- Follows principle of least privilege

**Connection String**: Uses keyword-value format
- Format: `Host=...;Port=...;Database=...;Username=...;Password=...;`
- Retrieved from `.env.production` on server
- Never stored in version control

---

## Version History

- **2025-11-24**: Created as automation wrapper for production database reset
- Mirrors: `database-reset-staging` skill with enhanced safety
- Complements: `docs/guides-setup/database-setup.md`

---

**Remember**:
- This skill is for PRODUCTION - USE WITH EXTREME CAUTION
- Always take complete database backup first
- Always use `production-deploy` skill first to ensure latest code is deployed
- Always notify stakeholders before and after
- Never use during business hours without explicit approval
