---
name: deploying-cloud-k8s
description: |
  Deploys applications to cloud Kubernetes (AKS/GKE/DOKS) with CI/CD pipelines.
  Use when deploying to production, setting up GitHub Actions, troubleshooting deployments.
  Covers build-time vs runtime vars, architecture matching, and battle-tested debugging.
---

# Deploying Cloud K8s

## Quick Start

1. Check cluster architecture: `kubectl get nodes -o jsonpath='{.items[*].status.nodeInfo.architecture}'`
2. Match build platform to cluster (arm64 vs amd64)
3. Set up GitHub Actions with path filters
4. Deploy with Helm, passing secrets via `--set`

## Critical: Build-Time vs Runtime Variables

### The Problem

Next.js `NEXT_PUBLIC_*` variables are **embedded at build time**, not runtime:

```dockerfile
# WRONG: Runtime ENV does nothing for NEXT_PUBLIC_*
ENV NEXT_PUBLIC_API_URL=https://api.example.com

# RIGHT: Must be build ARG
ARG NEXT_PUBLIC_API_URL=https://api.example.com
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL
```

### Build-Time (Next.js)

| Variable | Purpose |
|----------|---------|
| `NEXT_PUBLIC_SSO_URL` | SSO endpoint for browser OAuth |
| `NEXT_PUBLIC_API_URL` | API endpoint for browser fetch |
| `NEXT_PUBLIC_APP_URL` | App URL for redirects |

### Runtime (ConfigMaps/Secrets)

| Variable | Source |
|----------|--------|
| `DATABASE_URL` | Secret (Neon/managed DB) |
| `SSO_URL` | ConfigMap (internal K8s: `http://sso:3001`) |
| `BETTER_AUTH_SECRET` | Secret |

## Architecture Matching

**BEFORE ANY DEPLOYMENT**, check architecture:

```bash
kubectl get nodes -o jsonpath='{.items[*].status.nodeInfo.architecture}'
# Output: arm64 arm64  OR  amd64 amd64
```

### Docker Build

```yaml
- uses: docker/build-push-action@v5
  with:
    platforms: linux/arm64      # MATCH YOUR CLUSTER!
    provenance: false           # Avoid manifest issues
    no-cache: true              # When debugging
```

**Why `provenance: false`?** Buildx attestation creates complex manifest lists that cause "no match for platform" errors.

## GitHub Actions CI/CD

### Selective Builds with Path Filters

```yaml
jobs:
  changes:
    runs-on: ubuntu-latest
    outputs:
      api: ${{ steps.filter.outputs.api }}
      web: ${{ steps.filter.outputs.web }}
    steps:
      - uses: dorny/paths-filter@v3
        id: filter
        with:
          filters: |
            api:
              - 'apps/api/**'
            web:
              - 'apps/web/**'

  build-api:
    needs: changes
    if: needs.changes.outputs.api == 'true'
```

### Next.js Build Args

```yaml
- name: Build and push (web)
  uses: docker/build-push-action@v5
  with:
    build-args: |
      NEXT_PUBLIC_SSO_URL=https://sso.${{ vars.DOMAIN }}
      NEXT_PUBLIC_API_URL=https://api.${{ vars.DOMAIN }}
```

### Helm Deployment

```yaml
- name: Deploy
  run: |
    helm upgrade --install myapp ./helm/myapp \
      --set global.imageTag=${{ github.sha }} \
      --set "secrets.databaseUrl=${{ secrets.DATABASE_URL }}" \
      --set "secrets.authSecret=${{ secrets.BETTER_AUTH_SECRET }}"
```

## Troubleshooting Guide

### Quick Diagnosis Flow

```
Pod not running?
    │
    ├─► ImagePullBackOff
    │       ├─► "not found" ──► Wrong tag or registry
    │       ├─► "unauthorized" ──► Auth/imagePullSecrets
    │       └─► "no match for platform" ──► Architecture mismatch
    │
    ├─► CrashLoopBackOff
    │       ├─► "exec format error" ──► Wrong CPU architecture
    │       ├─► Exit code 1 ──► App startup failure
    │       └─► OOMKilled ──► Memory limits too low
    │
    └─► Pending
            ├─► Insufficient resources ──► Scale cluster
            └─► No matching node ──► Check nodeSelector
```

### Diagnostic Commands

```bash
kubectl get pods -n <namespace>
kubectl describe pod <pod-name> -n <namespace> | grep -E "(Image:|Failed|Error)"
kubectl get events -n <namespace> --sort-by='.lastTimestamp' | tail -20
kubectl logs <pod-name> -n <namespace> --tail=50
```

### Error: ImagePullBackOff "not found"

**Causes:**
- Tag doesn't exist (short vs full SHA)
- Wrong registry path
- Builds skipped by path filters

**Fix:** Verify image was pushed with exact tag used in deployment

### Error: "no match for platform in manifest"

**Cause:** Image built for wrong architecture OR buildx provenance issue

**Fix:**
```yaml
platforms: linux/arm64  # Match cluster!
provenance: false       # Simple manifest
no-cache: true          # Force rebuild
```

### Error: "exec format error"

**Cause:** Binary architecture doesn't match node

**Fix:** Rebuild with correct platform, use `no-cache: true`

### Error: Helm comma parsing

```
failed parsing --set data: key "com" has no value
```

**Cause:** Helm interprets commas as array separators

**Fix:** Use heredoc values file:
```yaml
- name: Deploy
  run: |
    cat > /tmp/overrides.yaml << EOF
    sso:
      env:
        ALLOWED_ORIGINS: "https://a.com,https://b.com"
    EOF
    helm upgrade --install app ./chart --values /tmp/overrides.yaml
```

### Error: Password authentication failed

**Cause:** Password with special characters (base64 `+/=`)

**Fix:** Use hex passwords:
```bash
# Wrong
openssl rand -base64 16  # Can have +/=

# Right
openssl rand -hex 16     # Alphanumeric only
```

### Error: Logout redirects to 0.0.0.0

**Cause:** `request.url` returns container bind address

**Fix:**
```typescript
const APP_URL = process.env.NEXT_PUBLIC_APP_URL || "http://localhost:3000";
const response = NextResponse.redirect(new URL("/", APP_URL));
```

## Pre-Deployment Checklist

### Architecture
- [ ] Checked cluster node architecture
- [ ] Build platform matches cluster

### Docker Build
- [ ] `provenance: false` set
- [ ] `platforms: linux/<arch>` matches cluster
- [ ] Image tags consistent between build and deploy

### CI/CD
- [ ] All `NEXT_PUBLIC_*` as build args
- [ ] Secrets passed via `--set` (not in values.yaml)
- [ ] Path filters configured

### Helm
- [ ] No commas in `--set` values
- [ ] Internal K8s service names for inter-service communication
- [ ] Password single source of truth in values.yaml

## Production Debugging

### Trace Request Path

```bash
# 1. Frontend logs
kubectl logs deploy/web -n myapp --tail=50

# 2. API logs
kubectl logs deploy/api -n myapp --tail=100 | grep -i error

# 3. Sidecar logs (Dapr, etc.)
kubectl logs deploy/api -n myapp -c daprd --tail=50
```

### Common Bug Patterns

| Error | Likely Cause |
|-------|--------------|
| `AttributeError: no attribute 'X'` | Model/schema mismatch |
| `404 Not Found` on internal call | Wrong endpoint URL |
| Times off by hours | Timezone handling bug |
| `greenlet_spawn not called` | Async SQLAlchemy pattern |

## GitOps with ArgoCD

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: myapp
  namespace: argocd
spec:
  source:
    repoURL: https://github.com/org/repo.git
    path: k8s/overlays/production
  destination:
    server: https://kubernetes.default.svc
    namespace: myapp
  syncPolicy:
    automated:
      prune: true      # Delete resources not in Git
      selfHeal: true   # Fix drift automatically
```

## Observability

```yaml
# ServiceMonitor for Prometheus
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: myapp
spec:
  selector:
    matchLabels:
      app: myapp
  endpoints:
    - port: metrics
      interval: 30s
```

## Security

```yaml
# Pod Security Context
securityContext:
  runAsNonRoot: true
  runAsUser: 1000
  allowPrivilegeEscalation: false
  readOnlyRootFilesystem: true
  capabilities:
    drop: ["ALL"]
```

## Resilience

```yaml
# HPA + PDB
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
spec:
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
---
apiVersion: policy/v1
kind: PodDisruptionBudget
spec:
  minAvailable: 1
```

See [references/production-patterns.md](references/production-patterns.md) for full GitOps, observability, security, and resilience patterns.

## Verification

Run: `python scripts/verify.py`

## Related Skills

- `containerizing-applications` - Docker and Helm charts
- `operating-k8s-local` - Local Kubernetes with Minikube
- `building-nextjs-apps` - Next.js patterns

## References

- [references/production-patterns.md](references/production-patterns.md) - GitOps, ArgoCD, Prometheus, RBAC, HPA, PDB