---
name: deployment-checklist
description: Pre-deployment verification steps and checks
---

# Deployment Checklist Skill

Systematic verification to ensure code is ready for deployment.

## Pre-Deployment Checklist

### 1. Code Quality

```bash
# Lint check
npm run lint

# Type check
npm run build
# or: npx tsc --noEmit
```

- [ ] No lint errors
- [ ] No type errors
- [ ] Build succeeds without warnings

### 2. Test Suite

```bash
# Run all tests
npm test

# Check coverage (if configured)
npm run test:coverage
```

- [ ] All tests pass
- [ ] No skipped tests without reason
- [ ] Coverage meets threshold (if required)

### 3. Security

```bash
# Audit dependencies
npm audit --audit-level=high
```

- [ ] No high/critical vulnerabilities
- [ ] No hardcoded secrets in code
- [ ] Environment variables documented
- [ ] Sensitive routes are protected

### 4. Database

- [ ] Migrations are ready and tested
- [ ] Migrations are reversible
- [ ] No destructive migrations without approval
- [ ] Indexes added for new queries
- [ ] Backup verified (if applicable)

### 5. Configuration

- [ ] Environment variables updated in deployment config
- [ ] Feature flags configured correctly
- [ ] API keys/secrets rotated if compromised
- [ ] Third-party service limits checked

### 6. Documentation

- [ ] README updated if setup changed
- [ ] API documentation updated
- [ ] CHANGELOG updated
- [ ] Release notes prepared

### 7. Performance

- [ ] No N+1 queries introduced
- [ ] Large queries are paginated
- [ ] Caching configured appropriately
- [ ] Load testing done (for major features)

### 8. Monitoring

- [ ] Error tracking operational
- [ ] Key metrics have alerts
- [ ] Logging is appropriate (not excessive)
- [ ] Health check endpoints working

## Deployment Process

### Before Deployment

1. **Create deployment branch/tag**
   ```bash
   git tag -a v1.2.3 -m "Release 1.2.3"
   ```

2. **Run full verification**
   ```bash
   npm run lint && npm run build && npm test
   ```

3. **Notify team**
   - Announce deployment window
   - Ensure someone is available for rollback

### During Deployment

1. **Monitor deployment pipeline**
2. **Watch error rates**
3. **Check health endpoints**
4. **Verify core functionality**

### After Deployment

1. **Smoke test critical paths**
   - [ ] User can log in
   - [ ] Core features work
   - [ ] No error spikes

2. **Monitor for 15-30 minutes**
   - Error rates
   - Response times
   - Resource usage

3. **Document the release**
   - Update status page
   - Notify stakeholders

## Rollback Plan

### Triggers for Rollback

- Error rate > 5% increase
- Core functionality broken
- Security vulnerability discovered
- Data integrity issues

### Rollback Process

1. **Communicate** - Alert team
2. **Rollback** - Revert to previous version
3. **Verify** - Confirm previous version works
4. **Document** - Record what happened
5. **Investigate** - Find root cause before retrying

## Output Format

```markdown
## Deployment Readiness Report

**Version:** [version number]
**Date:** [deployment date]

### Checklist Results

| Category | Status | Notes |
|----------|--------|-------|
| Code Quality | PASS/FAIL | [details] |
| Tests | PASS/FAIL | [details] |
| Security | PASS/FAIL | [details] |
| Database | PASS/FAIL | [details] |
| Config | PASS/FAIL | [details] |
| Docs | PASS/FAIL | [details] |

### Overall Status
[ ] Ready to deploy
[ ] Not ready - see issues below

### Issues to Address
1. [Issue description]

### Rollback Plan
[Brief description of rollback procedure]
```

## Quick Verification Script

```bash
#!/bin/bash
echo "Running pre-deployment checks..."

echo "1. Lint check..."
npm run lint || exit 1

echo "2. Type check..."
npm run build || exit 1

echo "3. Test suite..."
npm test || exit 1

echo "4. Security audit..."
npm audit --audit-level=high || echo "Review audit results"

echo "All checks passed!"
```
