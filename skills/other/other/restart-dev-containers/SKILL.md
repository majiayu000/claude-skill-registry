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

**Common mistakes** (DO NOT do these):
- Running `docker-compose up -d` without the dev overlay
- Running compose without `-p witchcityrope-dev` (will interfere with test containers)
- Running `./dev.sh` then immediately running tests without checking compilation

**Instead**: Always use `execute.sh` -- it handles overlay, project isolation, compilation checks, and health verification.

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

## Quick Reference

```bash
# From project root - with confirmation prompt
bash .claude/skills/restart-dev-containers/execute.sh

# For automation - skip confirmation
SKIP_CONFIRMATION=true bash .claude/skills/restart-dev-containers/execute.sh
```

**No manual steps documented here** -- all logic lives in `execute.sh`. If the script is unavailable, read `execute.sh` directly for the correct procedure.

---

## Common Issues & Solutions

### Issue: Containers start but tests fail

**Cause**: Compilation errors in container. The skill automatically checks compilation logs and reports errors.

### Issue: Port already in use

**Cause**: Old containers still running or other process using ports. Check running containers and kill orphans, or use `lsof` to find what's occupying the port.

### Issue: Health checks fail after compilation succeeds

**Cause**: Services need more time to initialize. The skill retries health checks for up to 60 seconds.

### Issue: Test containers were deleted when restarting dev

**Cause**: Missing project isolation flag. Always use this skill which includes the correct `-p witchcityrope-dev` flag.

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
    "running": 3,
    "expected": 3,
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

- **2026-02-24**: Removed test-server from dev compose
  - test-server does not belong in dev environment; test infrastructure is handled by restart-test-containers skill
  - Reduced expected container count from 4 to 3 (postgres, api, web)
- **2025-12-02**: Removed seed data check
  - Was failing silently due to wrong database password
  - Unnecessary since API auto-seeds on startup and health checks verify connectivity
- **2025-12-01**: Added `-p witchcityrope-dev` project isolation
  - Added reference to `restart-test-containers` skill
- **2025-11-04**: Created as single source of truth for container restart

---

**Remember**: This skill is executable automation. Run it, don't copy it.
