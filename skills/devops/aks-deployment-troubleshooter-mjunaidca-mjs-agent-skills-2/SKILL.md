---
name: aks-deployment-troubleshooter
description: Diagnose and fix Kubernetes deployment failures, especially ImagePullBackOff, CrashLoopBackOff, and architecture mismatches. Battle-tested from 4-hour AKS debugging session with 10+ failure modes resolved.
version: 1.0.0
---

# AKS Deployment Troubleshooter

## Overview

This skill captures systematic approaches to debugging Kubernetes deployments, with specific focus on container image issues. Based on real debugging session resolving 10+ different failure modes.

## When to Use

- Pods stuck in `ImagePullBackOff`
- Pods in `CrashLoopBackOff` with `exec format error`
- "no match for platform in manifest" errors
- Image registry authentication issues
- Helm deployment timeouts

## Quick Diagnosis Flow

```
Pod not running?
    │
    ├─► ImagePullBackOff
    │       │
    │       ├─► "not found" ──► Wrong tag or registry path
    │       ├─► "unauthorized" ──► Auth/imagePullSecrets issue
    │       └─► "no match for platform" ──► Architecture mismatch
    │
    ├─► CrashLoopBackOff
    │       │
    │       ├─► "exec format error" ──► Wrong CPU architecture
    │       ├─► Exit code 1 ──► App startup failure (check logs)
    │       └─► OOMKilled ──► Memory limits too low
    │
    └─► Pending
            │
            ├─► Insufficient CPU/memory ──► Scale cluster or reduce requests
            └─► No matching node ──► Check nodeSelector/tolerations
```

## Diagnostic Commands

### Step 1: Get Pod Status
```bash
kubectl get pods -n <namespace>
```

### Step 2: Describe Failing Pod
```bash
kubectl describe pod <pod-name> -n <namespace> | grep -E "(Image:|Failed|Error|pull)"
```

### Step 3: Check Events
```bash
kubectl get events -n <namespace> --sort-by='.lastTimestamp' | tail -20
```

### Step 4: Check Logs (for CrashLoopBackOff)
```bash
kubectl logs <pod-name> -n <namespace> --tail=50
```

### Step 5: Check Node Architecture
```bash
kubectl get nodes -o jsonpath='{.items[*].status.nodeInfo.architecture}'
```

## Error Resolution Guide

### 1. ImagePullBackOff: "not found"

**Error:**
```
Failed to pull image "ghcr.io/owner/repo/app:abc123": not found
```

**Causes & Solutions:**

| Cause | Solution |
|-------|----------|
| Tag doesn't exist | Verify image was pushed with exact tag |
| Short vs full SHA | Align metadata-action with deploy (use `type=raw,value=${{ github.sha }}`) |
| Builds skipped | Manual trigger or remove path filters |
| Wrong registry | Check `image.repository` in Helm values |

**Diagnostic:**
```bash
# Check what tags exist (requires gh cli and package visibility)
gh api /users/<owner>/packages/container/<package>/versions
```

---

### 2. ImagePullBackOff: "unauthorized"

**Error:**
```
failed to authorize: failed to fetch anonymous token: 401 Unauthorized
```

**Causes & Solutions:**

| Cause | Solution |
|-------|----------|
| Package is private | Make package public in GHCR settings |
| Missing imagePullSecrets | Create docker-registry secret |
| Wrong credentials | Regenerate and update secret |

**Create imagePullSecrets:**
```bash
kubectl create secret docker-registry ghcr-secret \
  --docker-server=ghcr.io \
  --docker-username=<github-username> \
  --docker-password=<github-token> \
  --namespace=<namespace>
```

**Link secret in deployment:**
```yaml
spec:
  imagePullSecrets:
    - name: ghcr-secret
```

---

### 3. ImagePullBackOff: "no match for platform in manifest"

**Error:**
```
no match for platform in manifest: not found
```

**Root Cause:** Image built for wrong CPU architecture OR buildx provenance issue.

**Step 1: Check cluster architecture:**
```bash
kubectl get nodes -o jsonpath='{.items[*].status.nodeInfo.architecture}'
# Output: amd64 amd64  OR  arm64 arm64
```

**Step 2: Match build platform:**
```yaml
# In GitHub Actions docker/build-push-action
- uses: docker/build-push-action@v5
  with:
    platforms: linux/arm64  # or linux/amd64
    provenance: false       # CRITICAL: Disable attestation manifests
    no-cache: true          # Force fresh build
```

**Why `provenance: false`?**
Buildx creates multi-arch manifest lists with attestations. Some container runtimes can't find the actual image in complex manifests. Disabling provenance creates simple single-platform images.

---

### 4. CrashLoopBackOff: "exec format error"

**Error:**
```
exec /usr/local/bin/docker-entrypoint.sh: exec format error
```

**Root Cause:** Binary architecture doesn't match node architecture.

**Example:** Built `linux/amd64` image, deployed to `arm64` nodes.

**Solution:**
1. Check node architecture: `kubectl get nodes -o jsonpath='{.items[*].status.nodeInfo.architecture}'`
2. Update build platform to match
3. Rebuild WITHOUT cache (cached layers may have wrong arch)

```yaml
platforms: linux/arm64  # Match your cluster!
no-cache: true          # Force complete rebuild
provenance: false       # Simple manifest
```

---

### 5. Helm --set Comma Parsing Error

**Error:**
```
failed parsing --set data: key "com" has no value (cannot end with ,)
```

**Root Cause:** Helm interprets commas as array separators in `--set`.

**Wrong:**
```bash
--set "origins=https://a.com,https://b.com"
```

**Solution: Use heredoc values file:**
```yaml
# In GitHub Actions
- name: Deploy
  run: |
    cat > /tmp/overrides.yaml << EOF
    sso:
      env:
        ALLOWED_ORIGINS: "https://a.com,https://b.com"
    EOF

    helm upgrade --install app ./chart \
      --values /tmp/overrides.yaml
```

---

### 6. Azure Login "No subscriptions found"

**Error:**
```
Error: No subscriptions found for ***
```

**Root Cause:** Missing `subscriptionId` in AZURE_CREDENTIALS.

**Solution:** Use `--sdk-auth` format:
```bash
az ad sp create-for-rbac \
  --name "github-actions" \
  --role contributor \
  --scopes /subscriptions/<subscription-id>/resourceGroups/<rg-name> \
  --sdk-auth
```

**Required JSON structure:**
```json
{
  "clientId": "xxx",
  "clientSecret": "xxx",
  "subscriptionId": "xxx",  // MUST be present
  "tenantId": "xxx"
}
```

---

### 7. GHCR 403 Forbidden

**Error:**
```
403 Forbidden: permission_denied: write_package
```

**Solutions:**
1. Make package public: GHCR → Package Settings → Change visibility
2. Link package to repository: Package Settings → Connect Repository
3. Ensure workflow has `packages: write` permission:
```yaml
permissions:
  contents: read
  packages: write
```

---

## Docker Build Best Practices for K8s

### Buildx Configuration for Reliability

```yaml
- name: Set up Docker Buildx
  uses: docker/setup-buildx-action@v3

- name: Build and push
  uses: docker/build-push-action@v5
  with:
    context: .
    push: true
    platforms: linux/arm64        # Match cluster architecture!
    provenance: false             # Avoid manifest complexity
    no-cache: true                # For debugging; remove in production
    tags: |
      ghcr.io/owner/repo:${{ github.sha }}
      ghcr.io/owner/repo:latest
```

### Image Tag Strategy

**Problem:** Short SHA vs Full SHA mismatch

```yaml
# docker/metadata-action default: short SHA (7 chars)
type=sha,prefix=  # Creates: ghcr.io/repo:abc1234

# github.sha is full SHA (40 chars)
${{ github.sha }}  # Is: abc1234567890abcdef...
```

**Solution: Use explicit full SHA:**
```yaml
tags: |
  type=raw,value=${{ github.sha }}
  type=raw,value=latest,enable={{is_default_branch}}
```

---

## Pre-Deployment Checklist

### Architecture
- [ ] Checked cluster node architecture (`kubectl get nodes -o jsonpath='{.items[*].status.nodeInfo.architecture}'`)
- [ ] Build platform matches cluster (arm64 vs amd64)

### Docker Build
- [ ] `provenance: false` set
- [ ] `platforms: linux/<arch>` matches cluster
- [ ] Image tags are consistent between build and deploy

### Registry
- [ ] Packages are public OR imagePullSecrets configured
- [ ] Workflow has `packages: write` permission

### Helm
- [ ] No commas in `--set` values (use values file instead)
- [ ] Image repository and tag are correctly templated

### Azure/Cloud
- [ ] Credentials include subscriptionId
- [ ] Service principal has correct role assignments

---

## Debugging Workflow

1. **Identify error type** from `kubectl describe pod`
2. **Match to resolution guide** above
3. **Fix ONE thing at a time**
4. **Verify fix locally if possible** before pushing
5. **Check builds completed** before checking deploy

---

## Common Mistakes (Lessons Learned)

1. **Assuming amd64** - Always check actual node architecture first
2. **Rerunning failed workflows** - Old workflows use old code; trigger new run
3. **Multiple fixes per commit** - Makes debugging harder; one fix at a time
4. **Ignoring build job status** - Deploy can start before builds finish
5. **Caching issues** - When stuck, try `no-cache: true`

---

## Related Skills

- `cloud-deploy-blueprint` - Full deployment setup
- `helm-charts` - Helm chart patterns
- `containerize-apps` - Dockerfile best practices
