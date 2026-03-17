---
name: android-playstore-publishing
description: Complete workflow generation - orchestrates internal, beta, and production deployment workflows
category: android
version: 2.0.0
---

# Android Play Store Publishing

This skill orchestrates complete GitHub Actions workflow generation by running three atomic skills in sequence.

## What This Does

Generates all GitHub Actions workflows for Play Store deployment:
1. **Internal Workflow** - Automatic deployment on push
2. **Beta Workflow** - Manual deployment to alpha/beta tracks
3. **Production Workflows** - Deployment and rollout management

## Prerequisites

- Play Console setup complete (run `android-playstore-setup` first)
- SERVICE_ACCOUNT_JSON_PLAINTEXT in GitHub Secrets
- Signing secrets configured
- Package name known

## Process

This skill runs three sub-skills in order:

### Step 1: Generate Internal Testing Workflow

Follow the skill at: `~/claude-devtools/skills/android-workflow-internal/SKILL.md`

**What it does:**
- Creates deploy-internal.yml
- Triggers on push to main/develop
- Deploys automatically to internal track
- Preserves build artifacts

**Verify before continuing:**
```bash
yamllint .github/workflows/deploy-internal.yml
```

---

### Step 2: Generate Beta Testing Workflow

Follow the skill at: `~/claude-devtools/skills/android-workflow-beta/SKILL.md`

**What it does:**
- Creates deploy-beta.yml
- Manual trigger with track selection (alpha/beta)
- Configurable rollout percentage
- Artifact preservation

**Verify before continuing:**
```bash
yamllint .github/workflows/deploy-beta.yml
```

---

### Step 3: Generate Production Workflows

Follow the skill at: `~/claude-devtools/skills/android-workflow-production/SKILL.md`

**What it does:**
- Creates deploy-production.yml (deployment)
- Creates manage-rollout.yml (rollout control)
- Requires manual approval via environment
- Staged rollout with configurable percentages

**Verify before continuing:**
```bash
yamllint .github/workflows/deploy-production.yml
yamllint .github/workflows/manage-rollout.yml
```

---

## Final Verification (MANDATORY)

After all three skills complete, verify the complete setup:

```bash
# 1. Verify all workflows exist
ls .github/workflows/deploy-*.yml .github/workflows/manage-rollout.yml

# 2. Validate all YAML files
yamllint .github/workflows/deploy-*.yml .github/workflows/manage-rollout.yml

# 3. Verify package names are correct
grep "packageName:" .github/workflows/deploy-*.yml

# 4. Verify workflows use correct secrets
grep "secrets\." .github/workflows/deploy-*.yml
```

**All checks must pass** before marking this skill as complete.

## Completion Criteria

Do NOT mark complete unless ALL are verified:

✅ **Workflows created**
  - [ ] .github/workflows/deploy-internal.yml exists
  - [ ] .github/workflows/deploy-beta.yml exists
  - [ ] .github/workflows/deploy-production.yml exists
  - [ ] .github/workflows/manage-rollout.yml exists

✅ **Validation**
  - [ ] All YAML files are valid
  - [ ] Package names are correct in all files
  - [ ] Workflows reference correct secrets

✅ **Documentation**
  - [ ] .github/workflows/README.md created
  - [ ] Environment setup documented

✅ **GitHub Setup**
  - [ ] "production" environment created
  - [ ] Required reviewers configured

## Summary Report

After completion, provide this summary:

```
✅ Android Play Store Publishing Setup Complete!

📦 Workflows Created:
  ✓ deploy-internal.yml (auto on push)
  ✓ deploy-beta.yml (manual, alpha/beta)
  ✓ deploy-production.yml (staged rollout)
  ✓ manage-rollout.yml (rollout control)

📋 Next Steps:

  1. Create GitHub Environment:
     Repository → Settings → Environments
     Create "production" with required reviewers

  2. Add GitHub Secrets:
     - SERVICE_ACCOUNT_JSON_PLAINTEXT (from Play Console setup)
     - SIGNING_KEY_STORE_BASE64
     - SIGNING_KEY_ALIAS
     - SIGNING_STORE_PASSWORD
     - SIGNING_KEY_PASSWORD

  3. First Deployment:
     git push origin main
     → Deploys to internal automatically

  4. Production Deployment:
     git tag v1.0.0
     git push origin v1.0.0
     → Requires approval, deploys with 5% rollout

📊 Deployment Workflow:
  Development → Internal (auto) → Beta (manual) → Production (approval + staged)

⚠️  CRITICAL:
  - Create "production" environment BEFORE first production deploy
  - Test in internal track before beta/production
  - Use staged rollouts (start at 5%)
  - Monitor crash-free rate before increasing rollout
```

## Integration with Other Skills

This skill completes the deployment pipeline:
- Requires: `android-playstore-setup` - Service account and API
- Requires: `android-release-build-setup` - Signing configuration
- Used by: `android-playstore-pipeline` - Complete orchestration

## Troubleshooting

If any skill fails:
1. Fix the specific issue in that skill
2. Re-run that skill until it completes
3. Continue with remaining skills
4. Run final verification

Common issues:
- **YAML validation fails** → Check indentation (use spaces, not tabs)
- **Package name mismatch** → Verify package name in all workflows
- **Missing secrets** → Add all 5 required secrets to GitHub
- **Environment not found** → Create "production" environment first
