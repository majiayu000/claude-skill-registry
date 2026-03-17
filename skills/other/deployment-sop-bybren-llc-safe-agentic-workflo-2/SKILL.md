---
name: deployment-sop
description: Deployment workflows, pre-deploy validation, and smoke testing patterns. Use when deploying to staging or production, running smoke tests, or validating deployments.
---

# Deployment SOP Skill

## Purpose

Route to existing deployment SOPs and provide checklists for safe, validated deployments. This skill does NOT duplicate SOP content—it links to authoritative sources.

## When This Skill Applies

Invoke this skill when:

- Deploying to staging or production
- Running pre-deploy validation
- Executing post-deploy smoke tests
- Accessing Linux dev machine for deployment
- Coordinating release activities

## Authoritative References (MUST READ)

| Document                 | Location                                          | Purpose                     |
| ------------------------ | ------------------------------------------------- | --------------------------- |
| Semantic Release SOP     | `docs/ci-cd/Semantic-Release-Deployment-SOP.md`   | Release automation workflow |
| Staging/UAT Release SOP  | `docs/sop/STAGING-UAT-RELEASE-SOP.md`             | UAT validation process      |
| Linux Dev Machine Access | `docs/deployment/LINUX-DEV-MACHINE-ACCESS-SOP.md` | Pop OS dev server access    |
| Production Server Access | `docs/deployment/PRODUCTION-SERVER-ACCESS-SOP.md` | Production deployment       |

## Pre-Deployment Checklist

Before ANY deployment:

- [ ] All CI checks pass (GitHub Actions green)
- [ ] PR merged to target branch (`dev` for staging, `master` for prod)
- [ ] No unresolved blockers in Linear
- [ ] Database migrations tested locally
- [ ] Environment variables verified

```bash
# Validate before deploy
yarn ci:validate
yarn build
```

## Post-Deployment Smoke Test

After deployment completes:

- [ ] Health endpoint responds: `curl https://{domain}/api/health`
- [ ] Database connection verified (check health response)
- [ ] Authentication flow works (sign-in/sign-up)
- [ ] Critical user flows functional
- [ ] No new errors in logs (PostHog/Coolify)

```bash
# Smoke test commands
curl -s https://{domain}/api/health | jq .
# Expected: {"status":"healthy","timestamp":"..."}
```

## Deployment Evidence Template

For Linear ticket attachment:

```markdown
## Deployment Evidence - {TICKET_PREFIX}-XXX

### Environment

- **Target**: Staging / Production
- **Branch**: `{branch_name}`
- **Commit**: `{commit_sha}`

### Pre-Deployment

- [x] CI checks passed
- [x] PR merged
- [x] Migrations verified

### Post-Deployment

- [x] Health check: PASSED
- [x] Auth flow: PASSED
- [x] Smoke tests: PASSED

### Verification

curl -s https://{domain}/api/health
{"status":"healthy","timestamp":"2025-XX-XXTXX:XX:XX.XXXZ"}
```

## Rollback Procedure

If deployment fails:

1. **Identify failure** - Check Coolify logs, PostHog errors
2. **Revert commit** - `git revert {commit_sha}`
3. **Push revert** - Triggers automatic rollback deployment
4. **Verify rollback** - Run smoke tests again
5. **Document incident** - Update Linear ticket with evidence

## Stop-the-Line Conditions

### FORBIDDEN

- Deploying with failing CI checks
- Skipping smoke tests on production
- Deploying database migrations without local testing
- Force-deploying over active incidents

### REQUIRED

- Health check MUST pass within 5 minutes
- Production deployments MUST have staging validation first
- Rollback plan MUST be documented before production deploy

## Branch → Environment Mapping

| Branch   | Environment          | Auto-Deploy |
| -------- | -------------------- | ----------- |
| `dev`    | Staging (Pop OS)     | Manual pull |
| `master` | Production (Coolify) | Automatic   |

**Note**: Merging to `dev` builds Docker image but requires manual `./scripts/dev-docker.sh pull` on Pop OS.
