---
name: argocd-bootstrap
description: Deploy and manage ArgoCD using the App-of-Apps pattern. Covers bootstrap Applications, ApplicationSets, and GitOps workflows. Use when setting up or troubleshooting ArgoCD deployments.
allowed-tools:
  - Bash
  - Read
  - Grep
  - Glob
---

# ArgoCD Bootstrap Pattern Skill

## Overview

ArgoCD bootstrap follows the "App-of-Apps" pattern: a root Application that creates other Applications. This enables GitOps-driven deployment of all cluster resources from a single Git repository.

## Architecture

```
Terraform
   ↓
ArgoCD Helm Chart Installation
   ↓
Bootstrap Application (created by Terraform)
   ↓
ApplicationSet (created by Bootstrap)
   ↓
Individual Applications (created by ApplicationSet)
   ↓
Runner Scale Sets (managed by Applications)
```

## Bootstrap Application Pattern

### Level 1: Terraform Creates Bootstrap Application

Terraform creates a single "root" Application that points to the ArgoCD manifests directory:

```hcl
resource "kubectl_manifest" "argocd_bootstrap" {
  yaml_body = yamlencode({
    apiVersion = "argoproj.io/v1alpha1"
    kind       = "Application"
    metadata = {
      name      = "bootstrap"
      namespace = "argocd"
    }
    spec = {
      project = "default"
      source = {
        repoURL        = "https://github.com/Matchpoint-AI/matchpoint-github-runners-helm"
        targetRevision = "main"
        path           = "argocd"  # Directory with ApplicationSets
      }
      destination = {
        server    = "https://kubernetes.default.svc"
        namespace = "argocd"
      }
      syncPolicy = {
        automated = {
          prune    = true
          selfHeal = true
        }
      }
    }
  })

  depends_on = [
    helm_release.argocd,
    time_sleep.wait_for_crds
  ]
}
```

**Key fields:**
- `path: "argocd"` - Directory containing ApplicationSets and Applications
- `targetRevision: "main"` - Git branch to sync (use specific tag for production)
- `automated.prune: true` - Remove resources deleted from Git
- `automated.selfHeal: true` - Revert manual changes to match Git

### Level 2: Bootstrap Creates ApplicationSet

The `argocd/` directory contains ApplicationSet manifests:

```yaml
# argocd/applicationset-runners.yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: github-runners
  namespace: argocd
spec:
  generators:
  - list:
      elements:
      - name: arc-beta-runners
        namespace: arc-runners
        valuesFile: examples/beta-runners-values.yaml
      - name: arc-frontend-runners
        namespace: arc-frontend-runners
        valuesFile: examples/frontend-runners-values.yaml
  template:
    metadata:
      name: '{{name}}'
      namespace: argocd
      finalizers:
      - resources-finalizer.argocd.argoproj.io
    spec:
      project: default
      source:
        repoURL: https://github.com/Matchpoint-AI/matchpoint-github-runners-helm
        targetRevision: main
        path: charts/github-actions-runners
        helm:
          releaseName: '{{name}}'  # CRITICAL: Must match runnerScaleSetName
          valueFiles:
          - '../../{{valuesFile}}'
      destination:
        server: https://kubernetes.default.svc
        namespace: '{{namespace}}'
      syncPolicy:
        automated:
          prune: true
          selfHeal: true
        syncOptions:
        - CreateNamespace=true
        - PruneLast=true
```

**Key concepts:**

**Generators** - Define list of Applications to create:
```yaml
generators:
- list:
    elements:
    - name: arc-beta-runners      # Application name
      namespace: arc-runners       # Target namespace
      valuesFile: examples/beta.yaml  # Helm values file
```

**Template** - Define Application spec using generator variables:
```yaml
template:
  metadata:
    name: '{{name}}'  # Substituted from generator
```

**Helm configuration**:
```yaml
helm:
  releaseName: '{{name}}'  # MUST match runnerScaleSetName in values!
  valueFiles:
  - '../../{{valuesFile}}'  # Path relative to chart directory
```

### Level 3: ApplicationSet Creates Applications

The ApplicationSet generates individual Applications for each runner pool:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: arc-beta-runners
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/Matchpoint-AI/matchpoint-github-runners-helm
    targetRevision: main
    path: charts/github-actions-runners
    helm:
      releaseName: arc-beta-runners
      valueFiles:
      - ../../examples/beta-runners-values.yaml
  destination:
    server: https://kubernetes.default.svc
    namespace: arc-runners
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
    - CreateNamespace=true
```

## Critical Configuration: releaseName vs runnerScaleSetName

### The Mismatch Problem

**Issue #112 Root Cause:** ApplicationSet `releaseName` didn't match Helm chart `runnerScaleSetName`:

```yaml
# ApplicationSet
releaseName: arc-runners  # ❌ Kubernetes resource name

# examples/runners-values.yaml
runnerScaleSetName: "arc-beta-runners"  # ✅ GitHub label
```

**Impact:**
- ArgoCD tracks resources under `arc-runners`
- AutoScalingRunnerSet created with name `arc-beta-runners`
- Resource tracking fails → stale runners with empty labels

### The Fix

**BOTH must match:**

```yaml
# argocd/applicationset-runners.yaml
generators:
- list:
    elements:
    - name: arc-beta-runners  # Used for releaseName

template:
  spec:
    source:
      helm:
        releaseName: '{{name}}'  # = arc-beta-runners

# examples/beta-runners-values.yaml
gha-runner-scale-set:
  runnerScaleSetName: "arc-beta-runners"  # MUST MATCH releaseName
```

**Workflow must also match:**
```yaml
# .github/workflows/ci.yaml
jobs:
  build:
    runs-on: arc-beta-runners  # MUST MATCH runnerScaleSetName
```

## ApplicationSet Features

### 1. List Generator

Static list of elements:

```yaml
generators:
- list:
    elements:
    - name: app1
      env: prod
    - name: app2
      env: staging
```

### 2. Git Generator

Generate from files in Git repository:

```yaml
generators:
- git:
    repoURL: https://github.com/org/repo
    revision: main
    files:
    - path: "apps/*/config.yaml"
```

### 3. Matrix Generator

Combine multiple generators:

```yaml
generators:
- matrix:
    generators:
    - list:
        elements:
        - cluster: prod
        - cluster: staging
    - list:
        elements:
        - app: frontend
        - app: backend
# Creates: prod-frontend, prod-backend, staging-frontend, staging-backend
```

## Sync Policies

### Automated Sync

```yaml
syncPolicy:
  automated:
    prune: true      # Delete resources removed from Git
    selfHeal: true   # Revert manual kubectl changes
```

**Use when:**
- Production with confidence in CI/CD
- Infrastructure as Code discipline enforced
- Changes only via Git

### Manual Sync

```yaml
syncPolicy: {}  # No automated sync
```

**Use when:**
- Testing/staging environments
- Manual approval required for changes
- Debugging configuration issues

### Sync Options

```yaml
syncOptions:
- CreateNamespace=true  # Create destination namespace if missing
- PruneLast=true        # Delete old resources after new ones ready
- Replace=true          # Use kubectl replace instead of apply
```

## Directory Structure

```
matchpoint-github-runners-helm/
├── argocd/
│   ├── applicationset-runners.yaml   # Creates runner Applications
│   ├── applications/                  # Individual Applications (legacy)
│   │   └── arc-controller.yaml       # ARC controller Application
│   └── apps-live/                     # Alternative app definitions (not used)
├── charts/
│   └── github-actions-runners/       # Helm chart deployed by Applications
└── examples/
    ├── beta-runners-values.yaml      # Values for arc-beta-runners
    └── frontend-runners-values.yaml  # Values for arc-frontend-runners
```

**Active paths:**
- `argocd/applicationset-runners.yaml` - Generates runner Applications
- `argocd/applications/arc-controller.yaml` - Deploys ARC controller

**Inactive paths:**
- `argocd/apps-live/` - Old structure, not referenced by bootstrap

## Common Patterns

### Pattern 1: Single Application (ARC Controller)

For resources that don't need templating:

```yaml
# argocd/applications/arc-controller.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: arc-controller
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/Matchpoint-AI/matchpoint-github-runners-helm
    targetRevision: main
    path: charts/github-actions-controller
  destination:
    server: https://kubernetes.default.svc
    namespace: arc-systems
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
    - CreateNamespace=true
```

### Pattern 2: ApplicationSet (Runner Pools)

For resources that need multiple instances with different configurations:

```yaml
# argocd/applicationset-runners.yaml
# (See full example above)
```

## Troubleshooting

### Error: "Application CRD not found"

**Symptom:**
```
error: unable to recognize "argocd/bootstrap.yaml": no matches for kind "Application"
```

**Cause:** ArgoCD CRDs not registered yet

**Fix:**
```hcl
resource "time_sleep" "wait_for_crds" {
  depends_on      = [helm_release.argocd]
  create_duration = "30s"
}
```

### Error: "Application OutOfSync"

**Symptom:**
```
kubectl get application arc-beta-runners -n argocd
# Status: OutOfSync
```

**Diagnosis:**
```bash
kubectl describe application arc-beta-runners -n argocd
# Check status.conditions for error details
```

**Common causes:**
1. `targetRevision` branch doesn't exist
2. `path` directory not found in repo
3. `valueFiles` path incorrect
4. Helm chart rendering failed

**Fix:**
```bash
# Force refresh
kubectl annotate application arc-beta-runners -n argocd \
  argocd.argoproj.io/refresh="hard" --overwrite

# Manual sync
kubectl patch application arc-beta-runners -n argocd \
  -p '{"operation":{"initiatedBy":{"automated":true}}}' --type=merge
```

### Error: "Helm template failed"

**Symptom:**
```
ComparisonError: failed to render manifests: helm template failed
```

**Diagnosis:**
```bash
# Get error details
kubectl get application arc-beta-runners -n argocd -o yaml | grep -A 10 conditions

# Test helm template locally
helm template arc-beta-runners ./charts/github-actions-runners \
  -f examples/beta-runners-values.yaml \
  --namespace arc-runners
```

**Common causes:**
1. Invalid YAML in values file
2. Missing required values
3. Helm chart syntax error

### Sync Stuck: "PruneLast" Waiting

**Symptom:** Application stuck syncing, old resources not deleted

**Cause:** `PruneLast=true` waits for new resources to be Ready before deleting old ones

**Fix:**
```bash
# Check pod status
kubectl get pods -n arc-runners

# If pods stuck, check events
kubectl get events -n arc-runners --sort-by='.lastTimestamp' | tail -20

# If safe to force delete old resources
kubectl delete application arc-beta-runners -n argocd
kubectl apply -f argocd/applicationset-runners.yaml
```

## Diagnostic Commands

```bash
# List all Applications
kubectl get applications -n argocd

# List all ApplicationSets
kubectl get applicationset -n argocd

# Check Application status
kubectl describe application arc-beta-runners -n argocd

# View Application manifest
kubectl get application arc-beta-runners -n argocd -o yaml

# Check ApplicationSet generators
kubectl get applicationset github-runners -n argocd -o yaml | grep -A 20 generators

# View ArgoCD controller logs
kubectl logs -n argocd -l app.kubernetes.io/name=argocd-application-controller --tail=100

# Force Application refresh
kubectl annotate application arc-beta-runners -n argocd argocd.argoproj.io/refresh="hard" --overwrite
```

## Best Practices

1. **Use ApplicationSet for similar apps** - Runner pools, microservices
2. **Use individual Applications for unique apps** - ARC controller, databases
3. **Always set targetRevision** - Prevents unexpected updates from main
4. **Enable automated sync in production** - Ensures Git is source of truth
5. **Use PruneLast for stateful apps** - Prevents downtime during updates
6. **Match releaseName and runnerScaleSetName** - Critical for ARC runners
7. **Keep bootstrap simple** - One root Application pointing to ArgoCD directory

## Related Skills

- [arc-terraform-deployment](../arc-terraform-deployment/SKILL.md) - Terraform patterns for ArgoCD
- [infrastructure-cd](../infrastructure-cd/SKILL.md) - CI/CD workflows
- [arc-runner-troubleshooting](../arc-runner-troubleshooting/SKILL.md) - Runner issues

## Related Issues

- #121 - releaseName/runnerScaleSetName mismatch
- #122 - ApplicationSet parameters fix
- #112 - Empty labels investigation

## References

- [ArgoCD App-of-Apps](https://argo-cd.readthedocs.io/en/stable/operator-manual/cluster-bootstrapping/)
- [ApplicationSet Documentation](https://argo-cd.readthedocs.io/en/stable/user-guide/application-set/)
- [ArgoCD Sync Options](https://argo-cd.readthedocs.io/en/stable/user-guide/sync-options/)
