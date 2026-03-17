---
name: arc-runner-troubleshooting
description: Troubleshoot ARC (Actions Runner Controller) runners on Rackspace Spot Kubernetes. Diagnose stuck jobs, scaling issues, and cluster access. Activates on "runner", "ARC", "stuck job", "queued", "GitHub Actions", or "CI stuck".
allowed-tools: Read, Grep, Glob, Bash
---

# ARC Runner Troubleshooting Guide

## Overview

project-beta uses self-hosted GitHub Actions runners deployed via ARC (Actions Runner Controller) on Rackspace Spot Kubernetes. This guide covers common issues and troubleshooting procedures.

## Architecture

### Runner Infrastructure

```
GitHub Actions
      ↓
ARC (Actions Runner Controller)    ← Watches for queued jobs
      ↓
AutoscalingRunnerSet              ← Scales runner pods 0→N
      ↓
Runner Pods                        ← Execute GitHub Actions jobs
      ↓
Rackspace Spot Kubernetes         ← Underlying infrastructure
```

### Runner Pools

| Pool | Target | Namespace | Repository |
|------|--------|-----------|------------|
| `arc-beta-runners` | Org-level | `arc-runners` | All project-beta repos |

**Note:** As of Dec 12, 2025, all workflows use `arc-beta-runners` label. The `runnerScaleSetName` and ArgoCD `releaseName` must both be `arc-beta-runners`.

### CI Validation (Added Dec 12, 2025 - Issue #112)

A CI validation check now prevents releaseName/runnerScaleSetName mismatches:
- `scripts/validate-release-names.sh` - Validation script
- `.github/workflows/validate.yaml` - Runs on PRs touching config files

**Run locally:**
```bash
./scripts/validate-release-names.sh
```

### Key Configuration Files

```
matchpoint-github-runners-helm/
├── examples/
│   ├── beta-runners-values.yaml      ← DEPLOYED Helm values (org-level)
│   └── frontend-runners-values.yaml  ← DEPLOYED Helm values (frontend)
├── values/
│   └── repositories.yaml             ← Documentation (NOT deployed)
├── charts/
│   └── github-actions-runners/       ← Helm chart
└── terraform/
    └── modules/                      ← Infrastructure as Code
```

## Common Issues

### 1. Runners with Empty Labels (CRITICAL - P0)

**Primary Root Cause:** ArgoCD release name ≠ runnerScaleSetName (mismatch causes tracking failure)

**Secondary Root Cause:** `ACTIONS_RUNNER_LABELS` environment variable **does not work with ARC**

**CRITICAL: ArgoCD/Helm Alignment Issue (Dec 12, 2025 Discovery)**

If the ArgoCD helm release name doesn't match `runnerScaleSetName`:
1. ArgoCD tracks resources under the old release name
2. New AutoscalingRunnerSet created with different name
3. Old ARS may not be pruned, resulting in stale runners
4. Stale runners have broken registration → empty labels

**Fix:**
```yaml
# argocd/apps-live/arc-runners.yaml
helm:
  releaseName: arc-beta-runners  # MUST match runnerScaleSetName!

# examples/runners-values.yaml
gha-runner-scale-set:
  runnerScaleSetName: "arc-beta-runners"  # MUST match releaseName!
```

**Diagnosis tip:** Check runner pod names:
- `arc-runners-*-runner-*` → OLD ARS still active (problem!)
- `arc-beta-runners-*-runner-*` → NEW ARS deployed (correct!)

**Symptoms:**
- Runners show empty labels `[]` in GitHub
- Runners show `os: "unknown"` in GitHub API
- ALL jobs stuck in "queued" state indefinitely
- Runners appear online but never pick up jobs

**Diagnosis:**
```bash
# Check runner labels via GitHub API
gh api /orgs/Matchpoint-AI/actions/runners --jq '.runners[] | {name, status, labels: [.labels[].name], os}'

# Bad output (empty labels):
{
  "name": "arc-runners-w74pg-runner-2xppt",
  "status": "online",
  "labels": [],
  "os": "unknown"
}

# Good output (proper labels):
{
  "name": "arc-beta-runners-xxxxx-runner-yyyyy",
  "status": "online",
  "labels": ["arc-beta-runners", "self-hosted", "Linux", "X64"],
  "os": "Linux"
}
```

**Root Cause Explanation:**

Per [GitHub's official documentation](https://docs.github.com/en/actions/hosting-your-own-runners/managing-self-hosted-runners-with-actions-runner-controller/using-actions-runner-controller-runners-in-a-workflow):

> "You cannot use additional labels to target runners created by ARC. You can only use the installation name of the runner scale set that you specified during the installation or by defining the value of the `runnerScaleSetName` field in your values.yaml file."

**How ARC Labels Work:**
1. ARC uses ONLY the `runnerScaleSetName` as the GitHub label
2. Cannot add custom labels via `ACTIONS_RUNNER_LABELS` environment variable
3. ARC automatically adds `self-hosted`, OS, and architecture labels
4. Cannot have multiple custom labels on a single scale set

**Fix:**
```yaml
# examples/runners-values.yaml or frontend-runners-values.yaml
gha-runner-scale-set:
  runnerScaleSetName: "arc-beta-runners"  # This becomes the GitHub label

  template:
    spec:
      containers:
      - name: runner
        env:
        # DO NOT SET ACTIONS_RUNNER_LABELS - it's ignored by ARC!
        # Only runnerScaleSetName matters
        - name: RUNNER_NAME_PREFIX
          value: "arc-beta"
```

**Deployment Steps:**
1. Ensure `runnerScaleSetName` matches workflow `runs-on:` labels
2. Remove any `ACTIONS_RUNNER_LABELS` env vars
3. Merge configuration changes
4. Wait for ArgoCD auto-sync (3-5 minutes)
5. Force runner re-registration:
   ```bash
   kubectl delete pods -n arc-runners -l app.kubernetes.io/component=runner
   ```
6. Verify fix after 1-2 minutes

**References:**
- [Troubleshooting Guide](https://github.com/Matchpoint-AI/matchpoint-github-runners-helm/blob/main/docs/TROUBLESHOOTING_EMPTY_LABELS.md)
- Issue #89 in matchpoint-github-runners-helm

### 2. ArgoCD ApplicationSet Conflicting Parameters (CRITICAL - P0)

**Root Cause:** ArgoCD ApplicationSet injects Helm `parameters` that conflict with values file.

**CRITICAL: Dec 12, 2025 Discovery**

The ApplicationSet (`argocd/applicationset.yaml`) was injecting:
```yaml
parameters:
  - name: gha-runner-scale-set.githubConfigSecret.github_token
    value: "$ARGOCD_ENV_GITHUB_TOKEN"
```

But the values file uses:
```yaml
githubConfigSecret: arc-org-github-secret  # String reference to pre-created secret
```

**The Conflict:**
- Helm `--set gha-runner-scale-set.githubConfigSecret.github_token=` expects `githubConfigSecret` to be a map
- Values file defines `githubConfigSecret` as a string (secret name reference)
- Result: `interface conversion: interface {} is string, not map[string]interface {}`

**Symptoms:**
- ArgoCD Application shows `ComparisonError` in conditions
- Manifest generation fails repeatedly
- Runners may appear to work but sync is broken
- Application status shows `Unknown` sync status

**Diagnosis:**
```bash
# Check ArgoCD Application status
kubectl get application arc-runners -n argocd -o jsonpath='{.status.conditions[*]}'

# Look for error like:
# "failed parsing --set data: unable to parse key: interface conversion: interface {} is string, not map[string]interface {}"

# Check ApplicationSet for conflicting parameters
kubectl get applicationset github-runners -n argocd -o jsonpath='{.spec.template.spec.source.helm}'
```

**Fix:**
1. Remove `parameters` section from `argocd/applicationset.yaml`
2. Use pre-created secrets referenced in values file

```yaml
# argocd/applicationset.yaml - DO NOT include parameters
helm:
  releaseName: '{{name}}'
  valueFiles:
    - '../../{{valuesFile}}'
  # NO parameters section - values file handles secrets

# examples/runners-values.yaml
githubConfigSecret: arc-org-github-secret  # Pre-created in cluster
```

**Apply Fix to Cluster:**
```bash
# kubectl apply may not remove fields - use replace
kubectl replace -f argocd/applicationset.yaml --force

# Verify parameters removed
kubectl get applicationset github-runners -n argocd -o jsonpath='{.spec.template.spec.source.helm}'
```

**Secret Setup:**
```bash
# Create the secret manually in the cluster
kubectl create secret generic arc-org-github-secret \
  --namespace=arc-runners \
  --from-literal=github_token='ghp_...'
```

**References:**
- PR #94 in matchpoint-github-runners-helm (the fix)
- Issue #89 in matchpoint-github-runners-helm

### 3. Jobs Stuck in Queued State (2-5+ minutes)

**Root Cause:** `minRunners: 0` causes cold-start delays

**Symptoms:**
- Jobs stuck in "queued" status for 2-5+ minutes
- First job of the day takes significantly longer
- Parallel PRs cause cascading delays

**Diagnosis:**
```bash
# Check current Helm values
cat /home/pselamy/repositories/matchpoint-github-runners-helm/examples/beta-runners-values.yaml | grep minRunners

# Check if issue is minRunners: 0
# If minRunners: 0 → cold start on every job
```

**Fix:**
```yaml
# examples/beta-runners-values.yaml
minRunners: 2      # Changed from 0 - keep 2 runners pre-warmed
maxRunners: 20
```

**Why This Happens:**
```
With minRunners: 0:
Job Queued → ARC detects → Schedule pod → Pull image →
Start container → Register runner → Job starts
Total: 120-300 seconds

With minRunners: 2:
Job Queued → Assign to pre-warmed runner → Job starts
Total: 5-10 seconds
```

### 4. Cluster Access Issues

**Problem:** Cannot connect to Rackspace Spot cluster

**Common Errors:**
```
error: You must be logged in to the server (the server has asked for the client to provide credentials)
error: unknown command "oidc-login" for "kubectl"
dial tcp: lookup hcp-xxx.spot.rackspace.com: no such host
```

**CRITICAL: Kubeconfig Token Expiration (Dec 13, 2025 Discovery)**

Rackspace Spot kubeconfig JWT tokens expire after **3 days**. This is why:
- Downloaded kubeconfig "goes stale after a day or two"
- Manual downloads from Rackspace console have the same problem
- The DNS lookup failure is often a red herring - the token is expired, not the cluster

**Verify token expiration:**
```bash
# Decode JWT to check expiration
TOKEN=$(grep "token:" kubeconfig.yaml | head -1 | awk '{print $2}')
echo $TOKEN | cut -d. -f2 | base64 -d 2>/dev/null | python3 -c "
import json, sys
from datetime import datetime
payload = json.load(sys.stdin)
exp = datetime.fromtimestamp(payload['exp'])
print(f'Token expires: {exp}')
print(f'Expired: {datetime.now() > exp}')
"
```

**Solutions:**

**Option A: Get kubeconfig from Terraform State (RECOMMENDED)**

This is the preferred method - it gets a fresh kubeconfig from the terraform state.

```bash
# 1. Get GitHub token from gh CLI config
export TF_HTTP_PASSWORD=$(cat ~/.config/gh/hosts.yml | grep oauth_token | awk '{print $2}')

# 2. Navigate to terraform directory
cd /home/pselamy/repositories/matchpoint-github-runners-helm/terraform

# 3. Initialize terraform (reads state only, no changes)
terraform init -input=false

# 4. Get kubeconfig from terraform output (read-only operation)
terraform output -raw kubeconfig_raw > /tmp/runners-kubeconfig.yaml

# 5. Use the kubeconfig
export KUBECONFIG=/tmp/runners-kubeconfig.yaml
kubectl get pods -A
```

**Why this works:**
- `terraform output` reads from cached state in tfstate.dev
- State is refreshed every 2 days by scheduled workflow (PR #137)
- No Rackspace Spot API token needed to read outputs

**Note:** A scheduled workflow (`refresh-kubeconfig.yml`) runs every 2 days to refresh the token in terraform state before the 3-day expiration.

**Option B: Use token-based auth (ngpc-user)**
```bash
# Check if token expired
kubectl config view --minify -o jsonpath='{.users[0].user.token}' | cut -d. -f2 | base64 -d | jq .exp
# Compare with current timestamp

# Get new kubeconfig from Rackspace Spot console
# 1. Login to https://spot.rackspace.com
# 2. Select cloudspace
# 3. Download kubeconfig
```

**Option C: Install oidc-login plugin**
```bash
# Install krew (kubectl plugin manager)
brew install krew  # or appropriate package manager

# Install oidc-login
kubectl krew install oidc-login

# Use OIDC context
kubectl config use-context tradestreamhq-tradestream-cluster-oidc
```

**Option D: Use ngpc CLI**
```bash
# Install ngpc CLI from Rackspace
pip install ngpc-cli

# Login and refresh credentials
ngpc login
ngpc kubeconfig get <cloudspace-name>
```

### 5. DNS Resolution Failures

**Problem:** Cluster hostname not resolving

```
dial tcp: lookup hcp-xxx.spot.rackspace.com: no such host
```

**Causes:**
1. Cluster was deleted/migrated (most common)
2. Using stale kubeconfig file that points to old cluster
3. DNS propagation delay
4. Wrong cluster endpoint

**Solution:**
Use terraform to get kubeconfig for the CURRENT active cluster:

```bash
# Get fresh kubeconfig from terraform (see Option A above)
export TF_HTTP_PASSWORD="<github-token>"
cd /home/pselamy/repositories/matchpoint-github-runners-helm/terraform
terraform init
terraform output -raw kubeconfig_raw > /tmp/runners-kubeconfig.yaml
```

**Note:** The `kubeconfig-matchpoint-runners-prod.yaml` file in the repo root may be stale if the cluster was recreated. Always use `terraform output` to get the current kubeconfig.

**Diagnosis:**
```bash
# Check terraform state for current cloudspace
cd /home/pselamy/repositories/matchpoint-github-runners-helm/terraform
export TF_HTTP_PASSWORD="<github-token>"
terraform init
terraform state list | grep cloudspace

# View cloudspace details
terraform state show module.cloudspace.spot_cloudspace.main
```

### 6. Missing Tools (wget, curl, Docker CLI)

**Problem:** CI workflows fail with "command not found" for common tools

**CRITICAL: Custom Runner Image (Dec 13, 2025 Discovery)**

Two runner images exist:
1. `ghcr.io/actions/actions-runner:latest` - **Generic** (missing many tools)
2. `ghcr.io/matchpoint-ai/arc-runner:latest` - **Custom** (has all tools)

**Symptoms:**
```
/bin/bash: wget: command not found
/bin/bash: docker: command not found
```

**Root Cause:** Configuration may be using the generic image instead of custom.

**Diagnosis:**
```bash
# Check which image is configured
grep -r "ghcr.io" examples/*.yaml values/*.yaml | grep -v "#"

# Check which image is actually running
kubectl get pods -n arc-runners -o jsonpath='{.items[0].spec.containers[0].image}'
```

**Custom Image Includes:**
| Tool | Version |
|------|---------|
| wget, curl, jq | latest |
| Node.js | 20 LTS |
| Python | 3.12 + pip + poetry |
| Docker CLI | 24.x |
| Terraform | 1.9.x |
| PostgreSQL client | 16 |
| Build tools | make, gcc, etc. |

**Fix:**
```yaml
# examples/runners-values.yaml
containers:
- name: runner
  image: ghcr.io/matchpoint-ai/arc-runner:latest  # NOT actions-runner!
```

**Note:** The custom image is built from `images/arc-runner/Dockerfile` in this repo. The build workflow runs on pushes to `images/arc-runner/**`.

**Reference:** Issue #135, PR #138

### 7. Docker-in-Docker (DinD) Issues

**Problem:** Docker commands fail even though DinD sidecar is configured

**Symptoms:**
```
Cannot connect to the Docker daemon at tcp://localhost:2375
```

**Diagnosis:**
```bash
# Check pod has 2 containers (runner + dind)
kubectl get pods -n arc-runners -o jsonpath='{.items[*].spec.containers[*].name}'
# Should show: runner dind

# Check DinD logs
kubectl logs -n arc-runners <pod-name> -c dind --tail=50
# Should show: "API listen on [::]:2375"

# Verify DOCKER_HOST env var
kubectl get pods -n arc-runners -o jsonpath='{.items[0].spec.containers[0].env}' | jq '.[] | select(.name=="DOCKER_HOST")'
# Should show: tcp://localhost:2375
```

**Common Issues:**
1. **DinD not running:** Check if privileged mode is allowed in cluster
2. **Wrong DOCKER_HOST:** Should be `tcp://localhost:2375`
3. **Missing sidecar:** Check pod template in values file

**Verify DinD is healthy:**
```bash
kubectl exec -n arc-runners <pod-name> -c runner -- docker version
kubectl exec -n arc-runners <pod-name> -c runner -- docker info
```

### 8. Configuration Mismatch

**Problem:** Documentation says one thing, deployed config is different

**Key Insight:** The `examples/*.yaml` files are what actually gets deployed. The `values/repositories.yaml` is documentation/reference only.

**Audit Configuration:**
```bash
# Check what's ACTUALLY deployed
cat examples/beta-runners-values.yaml | grep -E "(minRunners|maxRunners)"

# vs what documentation says
cat values/repositories.yaml | grep -E "(minRunners|maxRunners)"
```

## Monitoring Commands

### Check Workflow Status

```bash
# List queued workflows
gh run list --repo Matchpoint-AI/project-beta-api --status queued

# List in-progress workflows
gh run list --repo Matchpoint-AI/project-beta-api --status in_progress

# View specific run
gh run view <RUN_ID> --repo Matchpoint-AI/project-beta-api
```

### Check Runner Status (when cluster accessible)

```bash
# Set kubeconfig
export KUBECONFIG=/path/to/kubeconfig.yaml

# Check runner scale set
kubectl get autoscalingrunnerset -n arc-beta-runners-new

# Check runner pods
kubectl get pods -n arc-beta-runners-new -l app.kubernetes.io/component=runner

# Check ARC controller logs
kubectl logs -n arc-systems deployment/arc-gha-rs-controller --tail=50

# Check for scaling events
kubectl get events -n arc-beta-runners-new --sort-by='.lastTimestamp' | tail -20
```

### Check GitHub Registration

```bash
# List registered runners
gh api /orgs/Matchpoint-AI/actions/runners --jq '.runners[] | {name, status, busy}'

# Check runner groups
gh api /orgs/Matchpoint-AI/actions/runner-groups --jq '.runner_groups[].name'
```

## Troubleshooting Checklist

### For Stuck Jobs

1. [ ] Check `minRunners` in deployed Helm values
2. [ ] Verify ArgoCD sync status
3. [ ] Check if pods are scheduling (kubectl get pods)
4. [ ] Verify GitHub runner registration
5. [ ] Check node capacity and resources
6. [ ] Review ARC controller logs for errors

### For Cluster Access

1. [ ] Check kubeconfig context (kubectl config current-context)
2. [ ] Verify token expiration
3. [ ] Try different auth method (token vs OIDC)
4. [ ] Check if cluster hostname resolves (nslookup)
5. [ ] Verify cluster still exists in Rackspace console

### For Configuration Issues

1. [ ] Compare examples/*.yaml with values/repositories.yaml
2. [ ] Check ArgoCD for deployed values
3. [ ] Verify Helm release values

## Related Issues

| Issue/PR | Repository | Description |
|----------|------------|-------------|
| #135 | matchpoint-github-runners-helm | Epic: ARC runner environment limitations (Dec 2025) |
| #136 | matchpoint-github-runners-helm | Document troubleshooting learnings in skills |
| #137 | matchpoint-github-runners-helm | PR: Auto-refresh kubeconfig token workflow |
| #138 | matchpoint-github-runners-helm | PR: Use custom runner image with pre-installed tools |
| #112 | matchpoint-github-runners-helm | CI jobs stuck - PR #98 broke alignment |
| #113 | matchpoint-github-runners-helm | CI validation feature request |
| #114 | matchpoint-github-runners-helm | PR: Fix releaseName alignment + CI validation |
| #89 | matchpoint-github-runners-helm | Empty runner labels investigation |
| #91 | matchpoint-github-runners-helm | PR: Change release name (superseded) |
| #93 | matchpoint-github-runners-helm | PR: Revert to arc-runners naming - MERGED |
| #94 | matchpoint-github-runners-helm | PR: Remove ApplicationSet parameters - MERGED |
| #97 | matchpoint-github-runners-helm | PR: Standardize labels to arc-beta-runners |
| #98 | matchpoint-github-runners-helm | PR: Update runnerScaleSetName (broke alignment!) |
| #798 | project-beta-api | PR: Update workflow labels to arc-runners |
| #72 | matchpoint-github-runners-helm | Root cause analysis for queuing |
| #77 | matchpoint-github-runners-helm | Fix PR (minRunners: 0 → 2) - MERGED |
| #76 | matchpoint-github-runners-helm | Investigation state file |
| #1624 | project-beta | ARC runners stuck (closed) |
| #1577 | project-beta | P0: ARC unavailable (closed) |
| #1521 | project-beta | Runners stuck (closed) |

## Cost Considerations

| Setting | Cost Impact | Recommendation |
|---------|-------------|----------------|
| `minRunners: 0` | Lowest ($0 idle) | Development/low-traffic |
| `minRunners: 2` | ~$150-300/mo | Production/high-traffic |
| `minRunners: 5` | ~$400-700/mo | Enterprise/critical CI |

**ROI Calculation:**
- 2 pre-warmed runners save ~2-5 min per job
- 50+ PRs/week × 3 min saved = 150+ min/week
- Developer time saved >> runner cost

## Emergency Procedures

### Runners Completely Down

1. **Check ArgoCD sync status** via Argo UI or CLI
2. **Force sync** if needed: `argocd app sync arc-beta-runners`
3. **Check node availability** in Rackspace console
4. **Manual pod restart**: `kubectl rollout restart deployment -n arc-beta-runners-new`

### Fallback to GitHub-hosted runners

```yaml
# Temporarily switch workflow to GitHub-hosted
jobs:
  build:
    runs-on: ubuntu-latest  # Instead of self-hosted
```

## References

- Helm Chart: `matchpoint-github-runners-helm/charts/github-actions-runners/`
- Terraform: `matchpoint-github-runners-helm/terraform/`
- ArgoCD: <https://argocd.matchpointai.com> (internal)
- Rackspace Spot: <https://spot.rackspace.com>
- ARC Documentation: <https://github.com/actions/actions-runner-controller>
