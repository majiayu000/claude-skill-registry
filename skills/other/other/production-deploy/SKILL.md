---
name: production-deploy
description: Deploys WitchCityRope to production environment on DigitalOcean. Automates build, registry push, server deployment, database migrations (if needed), health verification, and rollback capability. SINGLE SOURCE OF TRUTH for production deployment automation.
---

# Production Deployment Skill

**Purpose**: Deploy to production environment safely and correctly - this is the automation wrapper.

**When to Use**:
- After staging validation passes
- When promoting tested features to production
- After critical hotfixes (tested in staging first)
- When requested by user/orchestrator

**Background Documentation**: See `/docs/functional-areas/deployment/production-deployment-guide.md` for context and manual procedures.

## 🚨 SINGLE SOURCE OF TRUTH

**This skill is the ONLY automated deployment procedure.**

**Division of responsibility:**
- **This skill**: Executable automation (bash script)
- **Deployment guide** (`/docs/functional-areas/deployment/production-deployment-guide.md`): Context, manual procedures, troubleshooting

**DO NOT duplicate deployment automation in:**
- ❌ Agent definitions
- ❌ Lessons learned (reference this skill instead)
- ❌ Process documentation (already has guide, references this skill)

---

## How to Use This Skill

**Executable Script**: `execute.sh`

```bash
# From project root - with confirmation prompt
bash .claude/skills/production-deploy/execute.sh

# Skip confirmation prompt (for automation)
SKIP_CONFIRMATION=true bash .claude/skills/production-deploy/execute.sh
```

**What the script does**:
1. Shows pre-flight information (purpose, when/when NOT to use, shared server warning)
2. Requires confirmation before proceeding (skippable with env var)
3. Validates prerequisites:
   - Tests passing (requires 90%+ pass rate - standardized format)
   - Git clean (no uncommitted changes)
   - Branch verification (main or production recommended)
   - SSH key accessible
   - Docker running
   - Registry access check
4. Builds production images (API and Web) with proper tagging
5. Pushes to DigitalOcean Container Registry (:latest and :git-sha tags)
6. Tests server connectivity
7. Pulls new images on production server
8. Deploys containers (with verification they were actually recreated)
9. Runs health checks (Web, API, Database)
10. Runs smoke tests (homepage, events API)
11. Reports deployment summary

**Script includes comprehensive safety checks** - it will not run blindly and verifies prerequisites before deployment.

---

## Rollback Procedure

**Separate skill**: `production-rollback.md`

Quick rollback:
```bash
ssh -i /home/chad/.ssh/id_ed25519_witchcityrope witchcity@104.131.165.14
cd /opt/witchcityrope/production

# Pull and restart previous :latest images
docker-compose -f docker-compose.production.yml pull
docker-compose -f docker-compose.production.yml up -d

# Or specify previous SHA
# docker-compose -f docker-compose.production.yml pull witchcityrope-api:<previous-sha>
# docker-compose -f docker-compose.production.yml up -d
```

---

## Critical Deployment Notes

### ⚠️ Shared Server Warning

**IMPORTANT**: Server hosts multiple applications.

**NEVER DO**:
```bash
# ❌ WRONG - Stops ALL containers on server
docker stop $(docker ps -q)
docker-compose down
```

**ALWAYS DO**:
```bash
# ✅ RIGHT - Only affects WitchCityRope containers
docker-compose -f docker-compose.production.yml down
docker-compose -f docker-compose.production.yml up -d
```

### 🚨 Image Tagging Convention

**Image Tagging**: The skill automatically tags images as `:latest` for production deployment.

**Why**: `docker-compose.production.yml` uses `image: ${REGISTRY}/witchcityrope-api:${IMAGE_TAG:-latest}` which defaults to `latest`.

**Note**: Use the `production-deploy` skill for all builds - it handles correct tagging automatically.

---

## Common Issues & Solutions

### Issue: Build fails locally

**Cause**: Missing dependencies, compilation errors

**Solution**:
1. Fix build errors
2. Test locally first: `docker build -f apps/api/Dockerfile .`
3. Ensure all tests passing before deploying

### Issue: Push to registry fails

**Cause**: Docker not logged into DigitalOcean registry

**Solution**:
```bash
# Login to DO registry (one-time)
doctl registry login
```

### Issue: Health checks fail after deployment

**Cause**: Services need more time, or deployment has errors

**Solution**:
1. Wait longer (skill waits 30 seconds)
2. Check logs via SSH to server and inspect container logs
3. If serious: Rollback

### Issue: Smoke tests fail

**Cause**: Specific endpoints broken

**Solution**:
1. Review which endpoint failed
2. Check API logs for errors
3. Consider rollback if critical functionality broken

---

## Integration with Agents

### git-manager / librarian

**After Phase 5 validation:**
```
I'll deploy to production for testing.
```
*Skill is invoked automatically*

**Result**: Code deployed to production safely

### test-executor

**After successful test run:**
```
All tests passed. Production deployment can proceed.
```

---

## Integration with Process Documentation

**Deployment guide should reference this skill:**

```markdown
# Production Deployment Process

After Phase 5 validation passes:

1. Use `production-deploy` skill (automated)
2. Skill handles:
   - Build verification
   - Image push
   - Server deployment
   - Health checks
   - Smoke tests
3. Manual testing of critical flows
4. If issues: Use `production-rollback` skill

**Automation**: `/.claude/skills/production-deploy.md`
**Manual procedures**: This guide (for troubleshooting)
```

---

## Output Format

```json
{
  "productionDeploy": {
    "status": "success",
    "timestamp": "2025-11-04T15:30:00Z",
    "gitSha": "abc123f",
    "build": {
      "api": "success",
      "web": "success"
    },
    "registry": {
      "api": "pushed",
      "web": "pushed",
      "tags": ["latest", "abc123f"]
    },
    "deployment": {
      "server": "104.131.165.14",
      "containersRestarted": true,
      "startTime": "2025-11-04T15:28:00Z",
      "endTime": "2025-11-04T15:30:00Z",
      "duration": "2m"
    },
    "healthChecks": {
      "web": "healthy",
      "api": "healthy",
      "database": "healthy"
    },
    "smokeTests": {
      "homepage": "pass",
      "eventsApi": "pass",
      "passed": 2,
      "failed": 0
    },
    "url": "https://production.notfai.com, https://prod.witchcityrope.com",
    "rollbackAvailable": true,
    "previousSha": "def456g"
  }
}
```

On failure:
```json
{
  "productionDeploy": {
    "status": "failure",
    "phase": "health_checks",
    "error": "API health check failed",
    "action": "Review logs and consider rollback",
    "rollbackCommand": "bash .claude/skills/production-rollback.md"
  }
}
```

---

## Maintenance

**This skill is the automation wrapper.**

**Division of labor:**
- **This skill**: Executable bash script (automation)
- **Deployment guide**: Context, manual steps, troubleshooting

**To update deployment procedure:**
1. If automation changes: Update THIS skill
2. If context/background changes: Update deployment guide
3. Test changes before committing

**To verify no duplication:**
- Use `single-source-validator` skill to check for duplicated commands

---

## Version History

- **2025-11-05**: Fixed reliability - replaced SSH heredocs with direct commands, added container age verification
- **2025-11-04**: Created as automation wrapper for production deployment

---

**Remember**: This skill automates deployment. The deployment guide provides context and manual procedures for troubleshooting.
