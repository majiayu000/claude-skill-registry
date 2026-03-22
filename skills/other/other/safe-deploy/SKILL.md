---
name: vibe-safe-deploy
description: Performs deployment with pre-flight checks, atomic replacement, post-deploy verification, and automatic rollback. Use before any deployment to staging or production.
user-invocable: true
---

# vibe-safe-deploy

Ship with confidence. Every deployment should be verifiable and reversible.

## When to Use This Skill

- Deploying to staging or production environments
- Releasing a new version
- Deploying infrastructure changes

## When NOT to Use This Skill

- Local development builds
- CI/CD that already handles these checks
- Deploying documentation (low risk)

## Pre-Flight Checklist

Before deploying, verify:
- [ ] All tests pass (including integration tests)
- [ ] Linting is clean
- [ ] No uncommitted changes in working tree
- [ ] No secrets in the diff (`grep -r 'API_KEY\|SECRET\|PASSWORD'`)
- [ ] Build succeeds
- [ ] Database migrations are reversible (if applicable)

## Steps

1. **Pre-flight checks** — Run all items in checklist. Stop if any fail.

2. **Backup current state**:
   ```bash
   cp -r current_deploy/ current_deploy.prev/
   # or: docker tag app:current app:rollback
   ```

3. **Deploy using atomic operations**:
   ```bash
   # Use 'install' not 'cp' for atomic file replacement
   install -m 755 new_binary /path/to/binary
   # or: docker tag app:new app:current && docker-compose up -d
   ```

4. **Health check** (within 60s timeout):
   - Service starts successfully
   - Health endpoint returns 200
   - Key functionality works (smoke test)
   - No error spikes in logs

5. **If health check fails → automatic rollback**:
   ```bash
   cp -r current_deploy.prev/ current_deploy/
   # Restart services with previous version
   ```

6. **Report status**: success / failed / rolled-back

## Output Format

### Deployment Report

**Status**: SUCCESS / FAILED / ROLLED_BACK
**Version**: [version or commit hash]
**Duration**: [time]

| Step | Status | Duration |
|------|--------|----------|
| Pre-flight | ✓ | 5s |
| Backup | ✓ | 2s |
| Deploy | ✓ | 10s |
| Health check | ✓ | 15s |

### Post-Deploy Verification
- Service running: ✓
- Health endpoint: 200 OK
- Log errors: 0 in last 60s
