---
name: database-reset-dev
description: Resets local development database by deleting all data and restarting API container to trigger auto-seeding. SINGLE SOURCE OF TRUTH for dev database reset automation.
---

# Database Reset Dev Skill

**Purpose**: Full database reset for local development environment - deletes all data and restarts API container to trigger automatic seed data population.

**When to Use**:
- Need fresh seed data for testing
- Database data is corrupted or inconsistent
- After manual data changes that broke the database state
- Testing with clean slate required
- Seed data accidentally modified or deleted

**When NOT to Use**:
- Staging database (use `database-reset-staging` skill instead)
- Production database (NEVER - this is dev only)
- Just need to restart containers without data reset (use `restart-dev-containers` skill)

**Background**: API container automatically seeds database on startup through `DatabaseInitializationService` when database is empty.

## 🚨 CRITICAL WARNINGS

**This skill performs DESTRUCTIVE operations:**
- ❌ ALL data in development database will be DELETED
- ❌ Both `public` AND `cms` schemas will be DROPPED and recreated
- ❌ Cannot be undone
- ✅ ONLY affects local dev database (`witchcityrope_dev`)
- ✅ API container will automatically re-seed on startup

**Prerequisites:**
- Docker containers should be running (or will be started by this skill)
- PostgreSQL client (psql) must be installed locally

---

## How to Use This Skill

**Executable Script**: `execute.sh`

```bash
# From project root - with confirmation prompt
bash .claude/skills/database-reset-dev/execute.sh

# Skip confirmation prompt (for automation)
SKIP_CONFIRMATION=true bash .claude/skills/database-reset-dev/execute.sh
```

**What the script does**:
1. Shows pre-flight information (purpose, when/when NOT to use, destructive operation warnings)
2. Requires confirmation before proceeding (skippable with env var)
3. Validates prerequisites:
   - Docker running
   - Project root directory
   - PostgreSQL client installed (psql)
4. Stops API container
5. Drops all database schemas (public + cms)
6. Recreates public schema
7. Starts API container with dev overlay
8. Waits for API initialization (initial 10 second wait)
9. Checks API container status
10. Verifies no compilation errors in API
11. Waits for migrations and seeding (15 seconds)
12. Verifies API health endpoint (with retry logic - up to 3 attempts)
13. Verifies database health endpoint
14. Verifies seed data populated
15. Reports summary

**Script includes CRITICAL safety warnings** - this is a DESTRUCTIVE operation that cannot be undone.

---

## Database Connection Details

**Local Development Database:**
- Host: localhost
- Port: 5434 (Docker-exposed port - note: NOT standard 5432)
- Database: witchcityrope_dev
- Username: postgres
- Password: devpass123

**Note**: Port 5434 is used to avoid conflicts with other local PostgreSQL instances.

---

## How Auto-Seeding Works

When API container starts with an empty database:
1. `DatabaseInitializationService` runs automatically
2. Applies any pending migrations
3. Detects empty database
4. Calls `SeedCoordinator` to populate seed data:
   - 7 test user accounts (admin, teacher, vetted member, general member, guest, 2 safety coordinators)
   - Sample events and sessions
   - Vetting statuses and workflows
   - Email templates
   - System settings
   - CMS content

**Total seed time**: ~10-15 seconds after container startup

---

## Manual Override (Emergency Only)

If skill fails, manual steps:

**Step 1: Connect to database and drop schemas**
```bash
PGPASSWORD=devpass123 psql -h localhost -p 5434 -U postgres -d witchcityrope_dev -c "DROP SCHEMA IF EXISTS public CASCADE; CREATE SCHEMA public; DROP SCHEMA IF EXISTS cms CASCADE;"
```

**Step 2: Restart containers**
```bash
bash .claude/skills/restart-dev-containers/execute.sh
```

**Step 3: Verify seed data**
```bash
PGPASSWORD=devpass123 psql -h localhost -p 5434 -U postgres -d witchcityrope_dev -c "SELECT COUNT(*) FROM \"Users\" WHERE \"Email\" LIKE '%@witchcityrope.com';"
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

### Issue: Connection refused on port 5434

**Cause**: Docker containers not running

**Solution**:
1. Check Docker status for witchcity containers
2. If no containers: Use restart-dev-containers skill to restart containers

### Issue: Database not found

**Cause**: Database was deleted entirely (not just schemas)

**Solution**:
1. Recreate database manually:
```bash
PGPASSWORD=devpass123 psql -h localhost -p 5434 -U postgres -c "CREATE DATABASE witchcityrope_dev;"
```
2. Run this skill again

### Issue: Seed data not populating after reset

**Cause**: API container seeding disabled or failed

**Solution**:
1. Check API logs for seed-related messages
2. Verify `DatabaseInitializationService` ran
3. Check for errors in initialization
4. Manual restart: Use restart-dev-containers skill to restart containers

### Issue: Health check fails with "API service unhealthy"

**Cause**: API container needs more time to start, or compilation/migration errors

**Solution**:
1. Skill automatically retries health check 3 times with 5-second delays
2. If still failing, check API container logs for recent messages
3. Check for compilation errors in logs
4. Check migrations in logs
5. If API container keeps restarting, fix source code errors first

### Issue: Port 5434 already in use

**Cause**: Another PostgreSQL instance using that port

**Solution**:
1. Find process: `lsof -i :5434`
2. Stop conflicting service
3. Or modify docker-compose.yml to use different port

---

## Integration with Workflow

**Typical usage scenarios**:

**Scenario 1: Clean testing environment**
```
Before E2E tests that require specific seed data state:
1. Run this skill to reset database
2. Run tests immediately
```

**Scenario 2: Database corruption during development**
```
Database in bad state from manual changes:
1. Run this skill to get fresh seed data
2. Continue development
```

**Scenario 3: Testing seed data changes**
```
Modified seed data logic in API:
1. Run this skill
2. Verify new seed data populated correctly
```

---

## Integration with Other Skills

**Related skills:**
- `restart-dev-containers`: Use this if you just need container restart WITHOUT database reset
- `database-reset-staging`: Staging environment equivalent (different database, different procedure)

**When to use which:**
- Need fresh seed data? → Use THIS skill (database-reset-dev)
- Just container issues? → Use `restart-dev-containers`
- Staging database? → Use `database-reset-staging`

---

## Output Format

**On success:**
```
✅ Database Reset Complete
==========================

📊 Summary:
   • Database: witchcityrope_dev
   • Schemas: Dropped and recreated
   • Seed data: Populated
   • Test users: 7 accounts

🎯 Ready for:
   • Development
   • Testing
   • Fresh start
```

**On failure:**
```
❌ Database Reset Failed

Error: [specific error message]

💡 Troubleshooting:
   • Check Docker is running
   • Verify psql client installed
   • Review container logs for errors
   • See: .claude/skills/database-reset-dev/SKILL.md (Common Issues)
```

---

## Version History

- **2025-11-19**: Added comprehensive health checks and retry logic
  - Implemented API container status verification
  - Added compilation error checking
  - Added health endpoint verification with 3-attempt retry logic
  - Added database health check
  - Prevents premature container restart attempts
  - Matches health check rigor of `restart-dev-containers` skill
- **2025-11-18**: Created as single source of truth for dev database reset
- Complements: `restart-dev-containers` skill (container management)
- Complements: `database-reset-staging` skill (staging equivalent)

---

**Remember**: This skill is for development only. Never use on staging or production. Use `restart-dev-containers` skill if you don't need database reset.
