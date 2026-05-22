---
name: restart-test-containers
description: Restarts WitchCityRope Docker TEST containers using the CORRECT procedure. Handles shutdown, rebuild with test compose overlay (--no-cache by default), health checks, and verification. Ensures environment is ready for testing. SINGLE SOURCE OF TRUTH for test container restart process. Uses -p witchcityrope-test for isolation from dev containers.
---

# Restart Test Containers Skill

**Purpose**: Restart Docker TEST containers the RIGHT way - this is the ONLY correct procedure.

**CRITICAL**: This skill is for TEST containers only. For DEVELOPMENT containers, use `restart-dev-containers` skill.

**When to Use**:
- Before running E2E tests (via test-environment skill)
- When test containers are unhealthy or stopped
- After code changes that need fresh test container build
- When test database needs reset (containers are recreated)

**When NOT to Use**:
- For dev containers - use `restart-dev-containers` instead
- If you just want to run tests and containers are healthy - use `--skip-rebuild` flag

## CONTAINER ISOLATION

**CRITICAL**: Dev and test containers are isolated using different project names:

- **Dev containers**: `-p witchcityrope-dev`
- **Test containers**: `-p witchcityrope-test`

This prevents operations on one environment from affecting the other.

## SINGLE SOURCE OF TRUTH

**This skill is the ONLY place where test container restart procedure is documented.**

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
# WRONG - Missing test overlay
docker-compose up -d

# WRONG - Missing project name (will interfere with dev containers)
docker-compose -f docker-compose.yml -f docker-compose.test.yml up -d

# WRONG - Not using --no-cache for clean test builds
docker-compose -p witchcityrope-test -f docker-compose.yml -f docker-compose.test.yml up -d --build
```

### DO This:

**Use this skill** - it handles everything correctly including project isolation and --no-cache.

---

## How to Use This Skill

**Executable Script**: `execute.sh`

```bash
# From project root - clean rebuild with --no-cache (default, ensures fresh test files)
bash .claude/skills/restart-test-containers/execute.sh

# Skip confirmation prompt (for automation)
SKIP_CONFIRMATION=true bash .claude/skills/restart-test-containers/execute.sh

# Skip rebuild - just restart existing containers (fastest, when code hasn't changed)
bash .claude/skills/restart-test-containers/execute.sh --skip-rebuild

# Use Docker cache for faster rebuilds (when only non-test code changed)
bash .claude/skills/restart-test-containers/execute.sh --use-cache

# Combine flags for automation without rebuild
SKIP_CONFIRMATION=true bash .claude/skills/restart-test-containers/execute.sh --skip-rebuild
```

**What the script does**:
1. Shows pre-flight information (purpose, when/when NOT to use)
2. Requires confirmation before proceeding (skippable with env var)
3. Validates prerequisites (Docker running, project root, test overlay exists)
4. Stops existing test containers (using `-p witchcityrope-test`)
5. Builds and starts containers with test overlay (`docker-compose.yml + docker-compose.test.yml`)
   - Default: Builds with `--no-cache` for clean test images
   - With `--use-cache`: Uses Docker cache for faster builds
   - With `--skip-rebuild`: Skips build entirely, just starts containers
6. Waits for containers to initialize
7. Verifies health endpoints (Web, API, Database, Test Runner)
8. Reports status summary

**Script includes safety checks** - it will not run blindly without showing you what it's about to do.

---

## Quick Reference Commands

### Using the Skill (Recommended)
```bash
# From project root - clean rebuild with --no-cache (default)
bash .claude/skills/restart-test-containers/execute.sh

# For quick restart without rebuild (code hasn't changed)
bash .claude/skills/restart-test-containers/execute.sh --skip-rebuild

# For faster rebuild using Docker cache (when only non-test files changed)
bash .claude/skills/restart-test-containers/execute.sh --use-cache

# For automation - skip confirmation
SKIP_CONFIRMATION=true bash .claude/skills/restart-test-containers/execute.sh
```

### Manual Steps (If execute.sh unavailable)
```bash
# CRITICAL: Always use -p witchcityrope-test to avoid affecting dev containers!

# Stop containers
docker-compose -p witchcityrope-test -f docker-compose.yml -f docker-compose.test.yml down -v

# Start with test overlay and --no-cache
docker-compose -p witchcityrope-test -f docker-compose.yml -f docker-compose.test.yml up -d --build --no-cache

# Wait and check health
sleep 20
docker exec witchcity-api-test curl -f http://localhost:8080/health
docker exec witchcity-web-test curl -f http://localhost:5173
```

---

## Common Issues & Solutions

### Issue: Containers start but tests fail immediately

**Cause**: Compilation errors in container or health not ready

**Solution**: Skill automatically checks container health. If issues persist, check container logs for errors in witchcity-web-test and witchcity-api-test.

### Issue: Network overlap error

**Cause**: Old networks from previous runs or different subnets conflicting

**Solution**:
```bash
# Remove old test networks
docker network ls | grep witchcity | awk '{print $1}' | xargs docker network rm 2>/dev/null

# Try again
bash .claude/skills/restart-test-containers/execute.sh
```

### Issue: Port already in use

**Cause**: Dev containers or other process using same ports

**Note**: Test containers do NOT expose ports externally (internal communication only). This error usually means dev containers are on conflicting networks.

**Solution**: Check if dev containers are running (they should be fine to run alongside). If network conflicts occur, prune unused Docker networks.

### Issue: Dev containers were deleted when restarting test

**Cause**: Missing `-p witchcityrope-test` flag

**Solution**: Always use this skill or ensure the project flag is included

---

## Integration with Other Skills

### test-environment skill

The `test-environment` skill calls `restart-test-containers` with `--skip-rebuild` when containers are already healthy, or without the flag when a fresh build is needed.

```bash
# test-environment internally calls:
bash .claude/skills/restart-test-containers/execute.sh --skip-rebuild
```

### restart-dev-containers skill

For development work, use the dev container skill which uses `-p witchcityrope-dev` project isolation.

---

## Output Format

When run via Claude Code, skill returns:

```json
{
  "skill": "restart-test-containers",
  "status": "success",
  "timestamp": "2025-12-01T15:30:00Z",
  "containers": {
    "running": 5,
    "expected": 5,
    "healthy": true
  },
  "build": {
    "mode": "full",
    "no_cache": true
  },
  "healthChecks": {
    "web": "healthy",
    "api": "healthy",
    "database": "healthy",
    "test_runner": "healthy"
  },
  "readyForTesting": true,
  "message": "Test environment ready"
}
```

On failure:
```json
{
  "skill": "restart-test-containers",
  "status": "failure",
  "error": "Container health check failed",
  "details": "API service did not respond within timeout",
  "action": "Check API container logs for errors"
}
```

---

## Related Skills

- **restart-dev-containers**: For restarting DEVELOPMENT containers (uses `-p witchcityrope-dev`)
- **test-environment**: For running E2E tests (calls restart-test-containers internally)

---

## Maintenance

**This skill is the single source of truth for TEST container restart.**

**To update the restart procedure:**
1. Update THIS file only
2. Test the new procedure
3. DO NOT update process docs, lessons learned, or agent definitions
4. They should reference this skill, not duplicate it

---

## Version History

- **2025-12-01**: Created as new skill for test container isolation
  - Uses `-p witchcityrope-test` project isolation
  - Default build with `--no-cache` for clean test images
  - Added `--skip-rebuild` flag for faster restarts
  - 5 containers (postgres, api, web, test-runner, db-test-helper)
  - Internal network only (no exposed ports)

---

**Remember**: This skill is executable automation. Run it, don't copy it.
