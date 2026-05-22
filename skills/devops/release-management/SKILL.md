---
name: RTE Agent (Release Train Engineer)
description: Creates pull requests, deployment checklists, and manages release processes
when_to_use: when code is tested, reviewed, and ready for deployment
version: 1.0.0
---

# RTE Agent (Release Train Engineer)

## Overview

The RTE Agent manages the release process from PR creation to deployment. This skill ensures releases are well-documented, properly sequenced, and safely deployed.

## When to Use This Skill

- All tests passing
- Security audit complete
- Documentation updated
- Ready to create PR
- Planning deployment

## Critical Rules

1. **No PR without tests** - All tests must pass first
2. **Deployment checklist mandatory** - Never wing it
3. **Rollback plan required** - Know how to undo
4. **Monitor after deploy** - Watch for issues

## Process

### Step 1: Read All Feature Documentation

**CRITICAL**: Read all feature documentation from files for complete context.

**Files to read**:
```
docs/features/[feature-slug]/01-bsa-analysis.md
docs/features/[feature-slug]/02-architecture-design.md
docs/features/[feature-slug]/03-migration.sql
docs/features/[feature-slug]/04-security-audit.md
docs/features/[feature-slug]/05-documentation-summary.md
docs/features/[feature-slug]/06-test-report.md
```

**What to extract**:
- Feature summary (from BSA)
- Technical changes (from Architecture/Migration)
- Security considerations (from Security Audit)
- Documentation updates (from Documentation Summary)
- Test coverage (from Test Report)

### Step 2: Pre-PR Verification

**Verify checklist** (create TodoWrite todos):
- [ ] All unit tests passing
- [ ] All integration tests passing
- [ ] All E2E tests passing
- [ ] Security audit complete (no HIGH/CRITICAL issues)
- [ ] API documentation updated
- [ ] Governance docs updated (if applicable)
- [ ] ADR created (if applicable)
- [ ] Code reviewed (if team project)
- [ ] No merge conflicts with target branch

### Step 3: Create Pull Request

**PR Structure**:

```markdown
## Summary
[1-3 sentences describing what this PR does and why]

## Changes
- Database: Added `user_exports` table with RLS policies
- API: New POST /api/users/{userId}/exports endpoint
- Background Jobs: Export processing worker
- Email: Notification when export ready
- Cleanup: Automatic deletion after 7 days

## Testing
- ✅ Unit tests (95% coverage)
- ✅ Integration tests (85% coverage)
- ✅ E2E tests (100% user flows)
- ✅ Security tests (all attack scenarios)

## Security Review
- ✅ RLS policies audited (Score: 8/10)
- ✅ Authentication validated
- ✅ Authorization tested
- ✅ Rate limiting implemented
- ⚠️ Note: See security audit for minor recommendations

## Documentation
- ✅ API docs updated (`docs/api/exports.md`)
- ✅ ADR created (`docs/adr/0015-user-data-exports.md`)
- ✅ Governance updated (`docs/governance/data-privacy.md`)

## Deployment Checklist
See below for full deployment steps and verification.

## Rollback Procedure
See below for rollback steps if issues arise.

## Breaking Changes
None - This is a new feature, no existing functionality affected.

---

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

### Step 4: Create Deployment Checklist

```markdown
## Deployment Checklist

### Pre-Deployment (Staging)
- [ ] Merge PR to staging branch
- [ ] Run migrations on staging database
  ```bash
  psql staging -f migrations/20251014_add_user_exports.sql
  ```
- [ ] Deploy application to staging
- [ ] Verify background workers running
  ```bash
  celery inspect active
  ```
- [ ] Run smoke tests
  - [ ] Create export via API
  - [ ] Verify background job processes
  - [ ] Verify email sent
  - [ ] Verify download link works
- [ ] Check monitoring dashboards
  - [ ] No errors in logs
  - [ ] Queue depth normal
  - [ ] Response times normal

### Deployment (Production)
- [ ] Create deployment window announcement
- [ ] Backup production database
  ```bash
  pg_dump production > backup_$(date +%Y%m%d_%H%M%S).sql
  ```
- [ ] Set maintenance mode (if needed)
- [ ] Run migrations on production
  ```bash
  psql production -f migrations/20251014_add_user_exports.sql
  ```
- [ ] Deploy application code
- [ ] Restart background workers
- [ ] Remove maintenance mode
- [ ] Verify deployment
  - [ ] Health check endpoint responds
  - [ ] Background workers running
  - [ ] No errors in logs

### Post-Deployment Verification
- [ ] Create test export (with test account)
- [ ] Verify export completes successfully
- [ ] Verify email notification received
- [ ] Verify download link works
- [ ] Check monitoring:
  - [ ] Error rate < 1%
  - [ ] Response time < 200ms
  - [ ] Queue depth < 10
- [ ] Monitor for 1 hour
- [ ] Announce deployment complete

### Environment Variables Required
```bash
# Add to production .env
EXPORT_STORAGE_BUCKET=user-exports-prod
EXPORT_STORAGE_REGION=us-east-1
EXPORT_SIGNED_URL_EXPIRATION=3600
EXPORT_RATE_LIMIT_WINDOW=86400
EXPORT_FILE_MAX_SIZE=104857600  # 100MB
EXPORT_CLEANUP_DAYS=7
```

### Alerts to Configure
```yaml
# Alert: Export processing time exceeds SLA
- name: export_processing_slow
  condition: export_processing_duration_seconds > 300
  severity: warning
  notification: slack-devops

# Alert: Export failure rate high
- name: export_failure_rate_high
  condition: export_failure_rate > 0.05
  severity: critical
  notification: slack-devops, pagerduty

# Alert: Export queue depth high
- name: export_queue_depth_high
  condition: export_queue_depth > 100
  severity: warning
  notification: slack-devops
```
```

### Step 5: Create Rollback Plan

```markdown
## Rollback Procedure

### If Issues Arise Within First Hour

#### Option 1: Quick Rollback (Feature Flag)
```bash
# Disable feature via feature flag (fastest)
psql production -c "UPDATE feature_flags SET enabled = false WHERE name = 'user_exports';"
```
**Impact**: New export requests blocked, existing exports continue processing
**Time**: < 1 minute

#### Option 2: Application Rollback
```bash
# Rollback to previous application version
git checkout [previous-commit]
./deploy.sh production

# Stop new background jobs
celery control shutdown
```
**Impact**: Full feature disabled, pending exports may fail
**Time**: 5-10 minutes

#### Option 3: Database Rollback (LAST RESORT)
```bash
# Only if database corruption or critical data issue
# DO NOT rollback migration if any data has been created

# Stop application first
systemctl stop myapp

# Rollback migration
psql production -f migrations/20251014_add_user_exports.sql --variable=direction=down

# Restart application on previous version
git checkout [previous-commit]
./deploy.sh production
```
**Impact**: All export data lost, feature completely removed
**Time**: 15-20 minutes
**WARNING**: Use only if absolutely necessary

### Decision Tree

```
Issue detected?
├─ Feature flag exists? → Use Option 1 (fastest)
├─ Application bug? → Use Option 2
└─ Database corruption? → Use Option 3 (LAST RESORT)
```

### Monitoring During Rollback
- Watch error rates (should drop immediately)
- Check queue depth (should stabilize)
- Monitor user reports (should cease)
- Verify core functionality unaffected

### Post-Rollback
- [ ] Identify root cause
- [ ] Create fix in new branch
- [ ] Test thoroughly in staging
- [ ] Document what went wrong
- [ ] Schedule re-deployment when ready
```

### Step 6: Create Monitoring Plan

```markdown
## Monitoring

### Metrics to Track

#### Application Metrics
- `export_requests_total` - Counter of export requests
- `export_requests_by_format{format="json|csv"}` - Breakdown by format
- `export_processing_duration_seconds` - Time to generate export
- `export_success_rate` - Percentage of successful exports
- `export_failure_rate` - Percentage of failed exports
- `export_queue_depth` - Number of pending exports

#### Infrastructure Metrics
- `export_storage_bytes` - Total storage used
- `export_storage_objects` - Number of files in storage
- `celery_worker_active_tasks` - Active background jobs
- `celery_worker_processed_total` - Total jobs processed

### Dashboards

**Create dashboard**: "User Data Exports"

Panels:
1. Export Requests (last 24h)
2. Processing Time (p50, p95, p99)
3. Success Rate (%)
4. Queue Depth
5. Storage Usage (GB)
6. Top Errors

### Alerts

| Alert | Condition | Severity | Action |
|-------|-----------|----------|--------|
| Processing Slow | p95 > 300s | Warning | Check worker capacity |
| High Failure Rate | > 5% | Critical | Investigate logs, potential rollback |
| Queue Backed Up | depth > 100 | Warning | Scale workers |
| Storage Full | > 80% capacity | Warning | Increase storage or reduce retention |

### First 48 Hours

**Enhanced monitoring**:
- Check dashboards every 2 hours
- Review error logs daily
- Track user feedback
- Measure adoption rate
- Verify cleanup job runs

**Success Criteria**:
- Error rate < 1%
- p95 processing time < 5min
- No critical security issues
- User satisfaction positive
```

### Step 7: Save Release Plan

**CRITICAL**: Save release plan to file.

**File location**:
```
docs/features/[feature-slug]/07-release-plan.md
```

**Steps**:
1. Write release plan to file (PR, deployment, rollback, monitoring)
2. Commit to git:
   ```bash
   git add docs/features/[feature-slug]/07-release-plan.md
   git commit -m "docs: release plan for [feature-name]"
   ```

## Output Format

```markdown
# Release Plan: [Feature Name]

## Pull Request
**URL**: [Link to PR]
**Status**: Ready for review
**Target Branch**: develop → main

## Deployment Timeline
- **Staging Deploy**: 2025-10-14 14:00 UTC
- **Staging Verification**: 2025-10-14 14:00-16:00 UTC
- **Production Deploy**: 2025-10-15 09:00 UTC (off-peak)
- **Production Monitoring**: 2025-10-15 09:00-17:00 UTC

## Risk Assessment
**Risk Level**: Medium

**Risks**:
- New background job infrastructure
- First use of object storage in this service
- Email dependency for user notification

**Mitigations**:
- Thorough staging testing
- Feature flag for quick disable
- Monitoring and alerts configured
- Rollback plan documented

## Deployment Checklist
[See Step 3 above]

## Rollback Plan
[See Step 4 above]

## Monitoring
[See Step 5 above]

## Communication Plan
- [ ] Notify team in #engineering channel
- [ ] Update deployment calendar
- [ ] Inform support team of new feature
- [ ] Prepare user-facing announcement

## Sign-Off Required
- [ ] Engineering Lead
- [ ] Security Team
- [ ] DevOps Team
- [ ] Product Owner (if user-facing)

## Post-Deployment
- [ ] Monitor for 48 hours
- [ ] Gather user feedback
- [ ] Review metrics
- [ ] Document lessons learned
- [ ] Close deployment ticket

## Next Steps
- **File saved**: `docs/features/[feature-slug]/07-release-plan.md`
- **Immediate**: Get PR reviews
- **Then**: Schedule staging deployment
- **Then**: Schedule production deployment
```

## Boundaries

**This skill does NOT**:
- Write code (that's implementation)
- Run tests (that's QAS)
- Make deployment decisions (that's DevOps/leads)
- Deploy without approval (get sign-off)

**This skill DOES**:
- **Read all feature documentation from files**
- Create PRs with full context
- Document deployment steps
- Create rollback plans
- Set up monitoring
- Coordinate release process
- **Save release plan to file**

## Related Skills

- QAS Agent (`~/.claude/skills/lifecycle/testing/acceptance_testing/SKILL.md`) - Provides test results
- Agent Dispatcher (`~/.claude/skills/crosscutting/process/agent_dispatch/SKILL.md`) - Coordinates full workflow

## Version History
- 1.0.0 (2025-10-14): Initial skill creation
