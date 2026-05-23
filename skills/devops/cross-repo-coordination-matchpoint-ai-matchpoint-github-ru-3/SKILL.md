---
name: cross-repo-coordination
description: Coordinate changes across project-beta repositories when updating runner configurations. Ensures workflow labels match runner scale set names. Use when changing runnerScaleSetName or deploying new runner pools.
allowed-tools:
  - Bash
  - Read
  - Grep
  - Glob
---

# Cross-Repository Workflow Coordination Skill

## Overview

GitHub Actions workflows in the project-beta ecosystem use self-hosted runners. When runner configurations change, ALL repositories using those runners need coordinated updates.

## Architecture

```
matchpoint-github-runners-helm
├── Defines runnerScaleSetName: "arc-beta-runners"
└── ArgoCD deploys runners with this label

project-beta-frontend
project-beta-api           } Must use: runs-on: arc-beta-runners
project-beta
```

**Critical Rule:** Workflow `runs-on:` MUST EXACTLY match Helm `runnerScaleSetName`

## The Coordination Problem

### Issue #121 Example

**Change:** Update `runnerScaleSetName` from `arc-runners` to `arc-beta-runners`

**Impact:**
```
matchpoint-github-runners-helm
  ✅ runnerScaleSetName: "arc-beta-runners"

project-beta-frontend (15 workflows)
  ❌ runs-on: arc-runners  # OLD label - jobs stuck!

project-beta-api (13 workflows)
  ❌ runs-on: arc-runners  # OLD label - jobs stuck!

project-beta (3 workflows)
  ❌ runs-on: arc-runners  # OLD label - jobs stuck!
```

**Result:** All CI jobs stuck in "queued" state until workflows updated.

## Affected Repositories

| Repository | Workflows | Runner Labels | Priority |
|------------|-----------|---------------|----------|
| project-beta-frontend | 15 files | arc-beta-runners | P0 - Blocks deploys |
| project-beta-api | 13 files | arc-beta-runners | P0 - Blocks deploys |
| project-beta | 3 files | arc-beta-runners | P0 - Blocks infra |

## Coordination Workflow

### Phase 1: Planning

Before changing `runnerScaleSetName`, audit all repositories:

```bash
# Search for current runner label usage
for repo in project-beta-frontend project-beta-api project-beta; do
  echo "=== $repo ==="
  cd /path/to/$repo
  grep -r "runs-on:" .github/workflows/ | grep -v "ubuntu-latest" | sort -u
done
```

**Output example:**
```
=== project-beta-frontend ===
.github/workflows/ci.yaml:    runs-on: arc-runners
.github/workflows/deploy.yaml:    runs-on: arc-runners
...

=== project-beta-api ===
.github/workflows/test.yaml:    runs-on: arc-runners
...
```

**Document the changes needed:**
- Count of files per repository
- Specific workflow files affected
- Any workflows using different labels

### Phase 2: Create Migration Plan

**Option A: Dual Runner Pools (Zero Downtime)**

Deploy BOTH old and new runner pools during transition:

```yaml
# matchpoint-github-runners-helm/argocd/applicationset-runners.yaml
generators:
- list:
    elements:
    - name: arc-runners           # OLD - for existing workflows
      valuesFile: examples/runners-values-old.yaml
    - name: arc-beta-runners      # NEW - for updated workflows
      valuesFile: examples/runners-values-new.yaml
```

**Timeline:**
1. Deploy both runner pools
2. Update workflows in all repos (can be done gradually)
3. Remove old runner pool after all workflows migrated

**Pros:**
- Zero downtime
- Safe rollback (revert workflow changes)
- Can update repos independently

**Cons:**
- 2x runner costs during migration
- Need to track which repos migrated

**Option B: Coordinated Single Cutover**

Update runner AND all workflows simultaneously:

1. Prepare PRs in ALL repositories (don't merge)
2. Merge runner config change
3. Wait for ArgoCD sync (~3 min)
4. Merge ALL workflow PRs quickly
5. Monitor for stuck jobs

**Pros:**
- No extra runner costs
- Clean cutover

**Cons:**
- ~3-5 minute CI outage
- Requires coordination across repos
- Risky if issues arise

**Recommended:** Option A for production, Option B for dev/test

### Phase 3: Update Workflows

For each repository, create a PR that updates ALL workflow files:

```bash
# Script: update-runner-labels.sh
#!/bin/bash

OLD_LABEL="arc-runners"
NEW_LABEL="arc-beta-runners"
REPO=$1

cd /path/to/$REPO

# Find all workflow files
WORKFLOWS=$(find .github/workflows -name "*.ya*ml")

# Update each file
for workflow in $WORKFLOWS; do
  if grep -q "runs-on: $OLD_LABEL" "$workflow"; then
    echo "Updating: $workflow"
    sed -i "s/runs-on: $OLD_LABEL/runs-on: $NEW_LABEL/g" "$workflow"
  fi
done

# Create PR
git checkout -b fix/update-runner-label-to-$NEW_LABEL
git add .github/workflows/
git commit -m "ci: Update runner label from $OLD_LABEL to $NEW_LABEL

Aligns with runner configuration change in matchpoint-github-runners-helm.

Refs: matchpoint-ai/matchpoint-github-runners-helm#121"

git push -u origin fix/update-runner-label-to-$NEW_LABEL

gh pr create \
  --title "ci: Update runner label from $OLD_LABEL to $NEW_LABEL" \
  --body "Updates all workflows to use the new runner label \`$NEW_LABEL\`.

## Context
matchpoint-github-runners-helm changed \`runnerScaleSetName\` to \`$NEW_LABEL\`.

## Changes
- Updates all \`.github/workflows/*.yaml\` files
- Changes \`runs-on: $OLD_LABEL\` → \`runs-on: $NEW_LABEL\`

## Testing
- [ ] Verify workflows use correct runner label
- [ ] Confirm CI jobs execute (not stuck in queue)

Related: matchpoint-ai/matchpoint-github-runners-helm#121"
```

**Usage:**
```bash
./update-runner-labels.sh project-beta-frontend
./update-runner-labels.sh project-beta-api
./update-runner-labels.sh project-beta
```

### Phase 4: Verification

After merging workflow updates:

```bash
# Check that runners are picking up jobs
gh run list --repo Matchpoint-AI/project-beta-frontend --limit 5

# Verify no jobs stuck in queue
gh run list --repo Matchpoint-AI/project-beta-frontend --status queued

# Check runner status
gh api /orgs/Matchpoint-AI/actions/runners --jq '.runners[] | {name, status, busy, labels: [.labels[].name]}'
```

**Success criteria:**
- ✅ No jobs stuck in "queued" for > 2 minutes
- ✅ Jobs transition to "in_progress" quickly
- ✅ Runners show "busy: true" when jobs running

## Common Scenarios

### Scenario 1: Adding New Runner Pool

**Example:** Add dedicated runners for frontend with GPU support

**Steps:**
1. Add runner pool in matchpoint-github-runners-helm:
   ```yaml
   # argocd/applicationset-runners.yaml
   - name: arc-frontend-gpu
     valuesFile: examples/frontend-gpu-values.yaml
   ```

2. Update ONLY affected workflows in project-beta-frontend:
   ```yaml
   # .github/workflows/e2e-visual-tests.yaml
   jobs:
     visual-tests:
       runs-on: arc-frontend-gpu  # NEW pool
   ```

3. Keep other workflows on existing pool:
   ```yaml
   # .github/workflows/ci.yaml
   jobs:
     test:
       runs-on: arc-beta-runners  # Existing pool
   ```

**Impact:** Only workflows explicitly updated use new pool

### Scenario 2: Removing Runner Pool

**Example:** Deprecate `arc-runners` in favor of `arc-beta-runners`

**Steps:**
1. Ensure NO workflows reference old label:
   ```bash
   for repo in project-beta-frontend project-beta-api project-beta; do
     cd /path/to/$repo
     grep -r "runs-on: arc-runners" .github/workflows/ && echo "❌ Found old label in $repo"
   done
   ```

2. Remove runner pool from matchpoint-github-runners-helm:
   ```yaml
   # argocd/applicationset-runners.yaml
   # Remove the arc-runners entry
   ```

3. Verify no queued jobs after removal:
   ```bash
   gh run list --status queued --limit 20
   ```

### Scenario 3: Emergency Runner Failover

**Example:** Primary runner pool down, need to switch to backup

**Steps:**
1. Deploy backup runner pool (if not already deployed):
   ```bash
   # Quick deploy via ArgoCD
   kubectl apply -f argocd/applications/arc-backup-runners.yaml
   ```

2. Bulk update workflows in critical repo:
   ```bash
   # Emergency script
   find .github/workflows -name "*.yaml" -exec sed -i 's/runs-on: arc-beta-runners/runs-on: arc-backup-runners/g' {} \;
   git add .github/workflows/
   git commit -m "EMERGENCY: Switch to backup runners"
   git push
   ```

3. Monitor job execution:
   ```bash
   watch -n 5 'gh run list --limit 10'
   ```

## Validation Scripts

### Pre-Merge Validation

Run before merging runner configuration changes:

```bash
#!/bin/bash
# scripts/validate-runner-labels.sh

set -euo pipefail

RUNNER_LABEL=$1
REPOS=("project-beta-frontend" "project-beta-api" "project-beta")

echo "🔍 Checking if workflows use runner label: $RUNNER_LABEL"

for repo in "${REPOS[@]}"; do
  echo ""
  echo "=== $repo ==="

  if [ ! -d "../$repo" ]; then
    echo "⚠️  Repository not found: ../$repo"
    continue
  fi

  cd "../$repo"

  MATCHES=$(grep -r "runs-on: $RUNNER_LABEL" .github/workflows/ 2>/dev/null | wc -l)

  if [ "$MATCHES" -gt 0 ]; then
    echo "✅ Found $MATCHES workflow jobs using $RUNNER_LABEL"
    grep -r "runs-on: $RUNNER_LABEL" .github/workflows/ | head -5
  else
    echo "❌ No workflows use $RUNNER_LABEL"
  fi

  cd - > /dev/null
done
```

**Usage:**
```bash
cd matchpoint-github-runners-helm
./scripts/validate-runner-labels.sh arc-beta-runners
```

### Post-Merge Validation

Run after merging workflow updates:

```bash
#!/bin/bash
# scripts/verify-ci-not-stuck.sh

set -euo pipefail

REPOS=("Matchpoint-AI/project-beta-frontend" "Matchpoint-AI/project-beta-api" "Matchpoint-AI/project-beta")

echo "🔍 Checking for stuck CI jobs..."

for repo in "${REPOS[@]}"; do
  echo ""
  echo "=== $repo ==="

  QUEUED=$(gh run list --repo "$repo" --status queued --limit 50 --json databaseId,createdAt,status | jq -r '.[] | select(.status == "queued") | "\(.databaseId) - queued since \(.createdAt)"')

  if [ -z "$QUEUED" ]; then
    echo "✅ No queued jobs"
  else
    echo "⚠️  Found queued jobs:"
    echo "$QUEUED"

    # Check if any queued > 5 minutes
    STUCK=$(echo "$QUEUED" | jq -r 'select(now - (.createdAt | fromdateiso8601) > 300)')
    if [ -n "$STUCK" ]; then
      echo "❌ Jobs stuck for > 5 minutes!"
    fi
  fi
done
```

**Usage:**
```bash
./scripts/verify-ci-not-stuck.sh
```

## Troubleshooting

### Error: Jobs Stuck After Runner Change

**Symptom:** CI jobs stuck in "queued" after runner label change

**Diagnosis:**
```bash
# Check what label runners have
kubectl get autoscalingrunnerset -A -o jsonpath='{.items[*].spec.runnerScaleSetName}'

# Check what label workflows use
for repo in project-beta-frontend project-beta-api project-beta; do
  cd ../$repo
  grep -h "runs-on:" .github/workflows/* | sort -u
done
```

**Fix:**
```bash
# If mismatch found, update workflows
cd ../project-beta-frontend
find .github/workflows -name "*.yaml" -exec sed -i 's/runs-on: OLD_LABEL/runs-on: NEW_LABEL/g' {} \;
git commit -am "fix: Update runner label to match deployed runners"
git push
```

### Error: Some Repos Updated, Others Not

**Symptom:** CI works in some repos but not others

**Diagnosis:**
```bash
# Check each repo's workflows
for repo in project-beta-frontend project-beta-api project-beta; do
  echo "=== $repo ==="
  cd ../$repo
  grep -h "runs-on:" .github/workflows/* | sort -u
  cd -
done
```

**Fix:** Update remaining repos using update script

### Error: Runners Deployed But Not Registering

**Symptom:** Runners deployed but GitHub doesn't show them

**Diagnosis:**
```bash
# Check GitHub runners
gh api /orgs/Matchpoint-AI/actions/runners --jq '.runners[] | {name, labels: [.labels[].name]}'

# Check Kubernetes runners
kubectl get pods -n arc-beta-runners -l app.kubernetes.io/component=runner
```

**Fix:** See [arc-runner-troubleshooting](../arc-runner-troubleshooting/SKILL.md)

## Best Practices

1. **Plan multi-repo changes in advance** - Don't surprise developers with stuck CI
2. **Use dual runner pools during migration** - Eliminates downtime
3. **Communicate changes** - Post in team chat before merging
4. **Verify in dev first** - Test runner changes in development repo
5. **Monitor after deployment** - Watch for queued jobs for 30 minutes post-change
6. **Document runner labels** - Keep README updated with current label names
7. **Automate validation** - Run validation scripts in CI for runner config changes

## Coordination Checklist

Before changing `runnerScaleSetName`:

- [ ] Audit all repos for workflow label usage
- [ ] Document count of files per repo needing updates
- [ ] Choose migration strategy (dual pool vs cutover)
- [ ] Prepare PRs for all affected repos
- [ ] Communicate change timeline to team
- [ ] Deploy runner config change
- [ ] Wait for ArgoCD sync (verify runners online)
- [ ] Merge workflow PRs
- [ ] Verify CI jobs execute successfully
- [ ] Monitor for stuck jobs (30 minutes)
- [ ] Clean up old runner pool (if dual pool strategy)

## Related Skills

- [arc-runner-troubleshooting](../arc-runner-troubleshooting/SKILL.md) - Runner registration issues
- [argocd-bootstrap](../argocd-bootstrap/SKILL.md) - Runner deployment via ArgoCD
- [infrastructure-cd](../infrastructure-cd/SKILL.md) - Automated deployment workflow

## Related Issues

- #121 - releaseName/runnerScaleSetName mismatch causing empty labels
- #123 - Cross-repo label update coordination
- #112 - CI jobs stuck investigation
- project-beta-api#798 - Workflow label update
- project-beta-frontend#886 - CI blocked by label mismatch

## References

- [GitHub Actions: runs-on](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions#jobsjob_idruns-on)
- [ARC: Using Runners in Workflows](https://docs.github.com/en/actions/hosting-your-own-runners/managing-self-hosted-runners-with-actions-runner-controller/using-actions-runner-controller-runners-in-a-workflow)
