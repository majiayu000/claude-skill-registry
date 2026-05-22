---
name: restart-dev-containers
description: Restarts WitchCityRope Docker DEVELOPMENT containers using the CORRECT procedure. Handles shutdown, rebuild with dev compose overlay, health checks, and compilation verification. Ensures environment is ready for development. SINGLE SOURCE OF TRUTH for dev container restart process. Uses -p witchcityrope-dev for isolation from test containers.
---

# Restart Dev Containers Skill

**Purpose**: Restart Docker DEVELOPMENT containers the RIGHT way - this is the ONLY correct procedure.

**CRITICAL**: This skill is for DEVELOPMENT containers only. For TEST containers, use `restart-test-containers` skill.

**When to Use**:
- After code changes that need container rebuild
- When dev containers are unhealthy
- When "Element not found" errors appear in dev testing (usually means compilation errors)

**When NOT to Use**:
- For test containers - use `restart-test-containers` instead
- For running E2E tests - use `test-environment` skill instead

## CONTAINER ISOLATION

**CRITICAL**: Dev and test containers are isolated using different project names:

- **Dev containers**: `-p witchcityrope-dev`
- **Test containers**: `-p witchcityrope-test`

This prevents operations on one environment from affecting the other.

## SINGLE SOURCE OF TRUTH

**This skill is the ONLY place where dev container restart procedure is documented.**

**If you find container restart instructions elsewhere:**
1. They are outdated or wrong
2. Report to librarian for cleanup
3. Use THIS skill instead

**DO NOT duplicate this procedure in:**
- Agent definitions
- Lessons learned (reference this skill instead)
- Process documentation (reference this skill instead)

---

## The Correct Process

### DON'T Do This:
```bash
# WRONG - Missing dev overlay
docker-compose up -d

# WRONG - Missing project name (will interfere with test containers)
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d

# WRONG - Doesn't check compilation
./dev.sh
# ... immediately runs tests
```

### DO This:

**Use this skill** - it handles everything correctly including project isolation.

---

## How to Use This Skill

**Executable Script**: `execute.sh`

```bash
# From project root
bash .claude/skills/restart-dev-containers/execute.sh

# Skip confirmation prompt (for automation)
SKIP_CONFIRMATION=true bash .claude/skills/restart-dev-containers/execute.sh
```

**What the script does**:
1. Shows pre-flight information (purpose, when/when NOT to use)
2. Requires confirmation before proceeding (skippable with env var)
3. Validates prerequisites (Docker running, project root, dev overlay exists)
4. Stops existing dev containers (using `-p witchcityrope-dev`)
5. Starts containers with dev overlay (`docker-compose.yml + docker-compose.dev.yml`)
6. Checks for compilation errors in Web and API containers
7. Verifies health endpoints (Web, API, Database)
8. Reports status summary

**Script includes safety checks** - it will not run blindly without showing you what it's about to do.

---

## Quick Reference Commands

### Using the Skill (Recommended)
```bash
# From project root - with confirmation prompt
bash .claude/skills/restart-dev-containers/execute.sh

# For automation - skip confirmation
SKIP_CONFIRMATION=true bash .claude/skills/restart-dev-containers/execute.sh
```

### Manual Steps (If execute.sh unavailable)
```bash
# CRITICAL: Always use -p witchcityrope-dev to avoid affecting test containers!

# Stop containers
docker-compose -p witchcityrope-dev -f docker-compose.yml -f docker-compose.dev.yml down

# Start with dev overlay
docker-compose -p witchcityrope-dev -f docker-compose.yml -f docker-compose.dev.yml up -d --build

# Wait and check health
sleep 15
curl http://localhost:5173
curl http://localhost:5655/health
curl http://localhost:5655/api/health/detailed
```

---

## Common Issues & Solutions

### Issue: Containers start but tests fail

**Cause**: Compilation errors in container

**Solution**: Skill automatically checks compilation logs

**Manual check**:
```bash
docker logs witchcity-web --tail 50 | grep -i error
docker logs witchcity-api --tail 50 | grep -i error
```

### Issue: Port already in use

**Cause**: Old containers still running or other process using ports

**Solution**:
```bash
# Kill all witchcity containers
docker ps -a | grep witchcity | awk '{print $1}' | xargs docker rm -f

# Check what's using port 5173
lsof -i :5173
```

### Issue: Health checks fail after compilation succeeds

**Cause**: Services need more time to initialize

**Solution**: Wait longer (skill waits 25 seconds total)

### Issue: Test containers were deleted when restarting dev

**Cause**: Missing `-p witchcityrope-dev` flag

**Solution**: Always use this skill or ensure the project flag is included

---

## Integration with Agents

### react-developer / backend-developer

**After code changes:**
```
I'll restart dev containers to apply my changes.
```
*Skill is invoked automatically*

**Result**: Code changes applied, compilation verified

---

## Output Format

When run via Claude Code, skill returns:

```json
{
  "skill": "restart-dev-containers",
  "status": "success",
  "timestamp": "2025-12-01T15:30:00Z",
  "containers": {
    "running": 4,
    "expected": 4,
    "healthy": true
  },
  "compilation": {
    "web": "clean",
    "api": "clean"
  },
  "healthChecks": {
    "web": "healthy",
    "api": "healthy",
    "database": "healthy"
  },
  "readyForTesting": true,
  "message": "Environment ready for development and testing"
}
```

On failure:
```json
{
  "skill": "restart-dev-containers",
  "status": "failure",
  "error": "Compilation errors in web container",
  "details": "TypeError: Cannot read property 'foo' of undefined at line 42",
  "action": "Fix source code and restart again"
}
```

---

## Related Skills

- **restart-test-containers**: For restarting TEST containers (uses `-p witchcityrope-test`)
- **test-environment**: For running E2E tests (calls restart-test-containers internally)

---

## Maintenance

**This skill is the single source of truth for DEV container restart.**

**To update the restart procedure:**
1. Update THIS file only
2. Test the new procedure
3. DO NOT update process docs, lessons learned, or agent definitions
4. They should reference this skill, not duplicate it

---

## Version History

- **2025-12-02**: Removed seed data check
  - Was failing silently due to wrong database password
  - Unnecessary since API auto-seeds on startup and health checks verify connectivity
- **2025-12-01**: Added `-p witchcityrope-dev` project isolation
  - Updated to 4 containers (includes test-server from dev overlay)
  - Added reference to `restart-test-containers` skill
- **2025-11-04**: Created as single source of truth for container restart

---

**Remember**: This skill is executable automation. Run it, don't copy it.
