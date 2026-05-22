---
activation_code: DEPLOYMENT_ROLLBACK_V1
phase: 12
version: 1.0.0
trigger: DEPLOYMENT_FAILED signal or manual invocation
---

# Deployment Rollback Skill

## Purpose

This skill provides automated rollback capabilities when deployments fail. It ensures that failed deployments don't leave systems in broken states and provides clear recovery paths.

## Activation Triggers

### Automatic Triggers
- `DEPLOYMENT_FAILED` signal detected
- Health check failures after deployment
- Smoke test failures

### Manual Triggers
- User says: "rollback deployment"
- User says: "revert to previous version"
- User says: "undo deployment"

---

## Rollback Process

### Phase 1: Assessment (30 seconds)

1. **Identify Failure Type**
   ```
   [ ] Deployment never completed
   [ ] Deployment completed but health check failed
   [ ] Deployment completed but smoke tests failed
   [ ] Deployment completed but user reported issues
   ```

2. **Gather Context**
   - Previous successful deployment version
   - Current failed deployment version
   - Error messages and logs
   - Affected services/components

### Phase 2: Rollback Strategy Selection

Based on assessment, select appropriate strategy:

#### Strategy A: Container Rollback (Docker/K8s)
```bash
# Kubernetes rollback
kubectl rollout undo deployment/<deployment-name>

# Docker Compose rollback
docker-compose down
docker-compose -f docker-compose.previous.yml up -d
```

#### Strategy B: Git-based Rollback
```bash
# Identify last good commit
git log --oneline -10

# Revert to previous tag
git checkout <previous-tag>

# Or revert specific commits
git revert <bad-commit>
```

#### Strategy C: Database Rollback (if applicable)
```bash
# Check for pending migrations
./manage.py showmigrations

# Rollback migrations
./manage.py migrate <app> <previous-migration>
```

#### Strategy D: Feature Flag Disable
```bash
# Disable problematic feature
curl -X POST https://api.example.com/flags \
  -d '{"feature": "new-feature", "enabled": false}'
```

### Phase 3: Execute Rollback

1. **Pre-rollback Checkpoint**
   ```bash
   # Create checkpoint of current (failed) state for analysis
   ./lib/pipeline-recovery.sh checkpoint "pre-rollback-$(date +%s)"
   ```

2. **Execute Selected Strategy**
   - Run rollback commands
   - Monitor for errors
   - Capture output

3. **Verify Rollback**
   ```bash
   # Run health checks
   ./hooks/docker-health-check.sh

   # Run smoke tests
   ./scripts/smoke-test.sh
   ```

### Phase 4: Post-Rollback

1. **Signal Rollback Complete**
   ```bash
   ./lib/signal-manager.sh create ROLLBACK_COMPLETE \
     '{"reason": "<failure-reason>", "rolled_back_to": "<version>"}'
   ```

2. **Generate Incident Report**
   - What failed
   - Why it failed (if known)
   - What was rolled back
   - Time to recovery
   - Recommended fixes

3. **Notify Stakeholders**
   - Log incident
   - Update deployment status
   - Create follow-up task

---

## Rollback Checklist

```markdown
## Pre-Rollback
- [ ] Confirmed deployment failure
- [ ] Identified rollback target (previous working version)
- [ ] Created checkpoint of failed state
- [ ] Notified team (if production)

## Rollback Execution
- [ ] Executed rollback command(s)
- [ ] Verified no errors during rollback
- [ ] Confirmed services restarted

## Post-Rollback Verification
- [ ] Health checks passing
- [ ] Smoke tests passing
- [ ] Key functionality verified
- [ ] No error spikes in logs

## Documentation
- [ ] Incident documented
- [ ] Root cause identified (or investigation task created)
- [ ] Rollback signal created
- [ ] Team notified of resolution
```

---

## Signals

### Input Signals
| Signal | Description |
|--------|-------------|
| `DEPLOYMENT_FAILED` | Triggers automatic rollback assessment |
| `HEALTH_CHECK_FAILED` | May trigger rollback if persistent |

### Output Signals
| Signal | Description |
|--------|-------------|
| `ROLLBACK_STARTED` | Rollback process initiated |
| `ROLLBACK_COMPLETE` | Rollback successful |
| `ROLLBACK_FAILED` | Rollback unsuccessful (escalate!) |
| `MANUAL_INTERVENTION_REQUIRED` | Cannot auto-rollback |

---

## Integration with Pipeline

```
Phase 11 (Deployment)
       ↓
    Success? ────Yes────→ PHASE11_COMPLETE
       ↓ No
DEPLOYMENT_FAILED
       ↓
[ACTIVATE:DEPLOYMENT_ROLLBACK_V1]
       ↓
Phase 12 (Rollback)
       ↓
ROLLBACK_COMPLETE
       ↓
Return to Phase 7 (implementation fix)
```

---

## Automatic Recovery Patterns

### Pattern 1: Quick Retry
For transient failures (network issues, timing):
```bash
# Wait and retry deployment
sleep 30
./deploy.sh --retry
```

### Pattern 2: Configuration Rollback
For config-related failures:
```bash
# Restore previous config
cp config/app.previous.yml config/app.yml
./deploy.sh --config-only
```

### Pattern 3: Partial Rollback
For multi-service deployments:
```bash
# Rollback only failed service
kubectl rollout undo deployment/failed-service
# Keep other services at new version
```

---

## Escalation Criteria

Escalate to manual intervention when:

1. **Multiple rollback attempts fail**
   - 3+ rollback attempts unsuccessful
   - Different strategies tried

2. **Data corruption detected**
   - Database in inconsistent state
   - File system corruption

3. **Infrastructure issues**
   - Cloud provider outage
   - Network partition

4. **Security incident**
   - Potential breach detected
   - Credentials exposed

---

## Example Rollback Session

```
Claude: Deployment health check failed. Initiating rollback assessment.

Assessment Results:
- Failed Version: v2.3.1
- Last Good Version: v2.3.0
- Failure Type: Application crash on startup
- Error: "Missing environment variable: API_KEY"

Recommended Strategy: Git-based rollback + Config fix

Executing rollback...
✓ Checkout v2.3.0
✓ Restart services
✓ Health check passing
✓ Smoke tests passing

Rollback complete. Root cause: Missing API_KEY in deployment config.

Action Items:
1. Add API_KEY to deployment checklist
2. Update CI/CD to validate required env vars
3. Retry deployment after config fix
```

---

## Related Skills

- `deployment-validator` - Pre-deployment checks
- `security-validator` - Security scanning
- `pipeline-recovery` - General recovery tools

---

*Skill Version: 1.0*
*Created: 2025-12-19*
