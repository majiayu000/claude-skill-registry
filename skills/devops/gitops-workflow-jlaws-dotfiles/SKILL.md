---
name: gitops-workflow
description: GitOps workflow patterns with ArgoCD and Flux for declarative Kubernetes deployments. Use when implementing GitOps, automating deployments, or setting up progressive delivery.
---

# GitOps Workflow

## ArgoCD vs Flux

| Factor | ArgoCD | Flux |
|--------|--------|------|
| **UI** | Full web UI + CLI | CLI only (Weave GitOps for UI) |
| **Multi-cluster** | Built-in multi-cluster support | One Flux per cluster |
| **App of Apps** | Native pattern | Kustomization dependencies |
| **Helm support** | Native | HelmRelease CRD |
| **RBAC** | Project-based RBAC, SSO | Kubernetes-native RBAC |
| **Best for** | Teams wanting visibility/UI | GitOps purists, simpler setup |

**Default choice**: ArgoCD for most teams (UI is valuable for debugging). Flux when you want minimal footprint or Kubernetes-native approach.

## Repository Structure

```
gitops-repo/
├── apps/
│   ├── production/
│   │   ├── app1/kustomization.yaml
│   │   └── app2/kustomization.yaml
│   └── staging/
├── infrastructure/
│   ├── ingress-nginx/
│   ├── cert-manager/
│   └── monitoring/
└── argocd/
    ├── applications/    # Application manifests
    └── projects/        # RBAC boundaries
```

**Opinion**: Separate app config repo from source code repo. Source repo CI builds image + updates image tag in gitops repo.

## ArgoCD Patterns

### Application Manifest
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: my-app
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/org/gitops-repo
    targetRevision: main
    path: apps/production/my-app
  destination:
    server: https://kubernetes.default.svc
    namespace: production
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
    - CreateNamespace=true
```

### App of Apps
Bootstrap pattern: one root Application points to a directory of Application manifests. ArgoCD manages itself.

### Sync Policy Opinions
- **`prune: true`**: Always. Resources removed from Git should be removed from cluster.
- **`selfHeal: true`**: Always in production. Reverts manual kubectl changes.
- **`allowEmpty: false`**: Prevents accidental deletion of all resources.
- **Retry**: Always configure. Transient failures are common.
```yaml
retry:
  limit: 5
  backoff: { duration: 5s, factor: 2, maxDuration: 3m }
```

### Sync Windows
- Block deploys during off-hours in production
- Allow deploys only during business hours: `schedule: "0 8 * * 1-5"`, `duration: 10h`
- Emergency override via ArgoCD admin role

### Useful Sync Options
- `ApplyOutOfSyncOnly=true` -- only apply changed resources (faster for large apps)
- `PruneLast=true` -- delete after create (safer for resource dependencies)
- `CreateNamespace=true` -- auto-create target namespace

## Flux Patterns

### GitRepository + Kustomization
```yaml
apiVersion: source.toolkit.fluxcd.io/v1
kind: GitRepository
metadata:
  name: my-app
  namespace: flux-system
spec:
  interval: 1m
  url: https://github.com/org/my-app
  ref: { branch: main }
---
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: my-app
  namespace: flux-system
spec:
  interval: 5m
  path: ./deploy
  prune: true
  sourceRef: { kind: GitRepository, name: my-app }
```

## Progressive Delivery

### Canary with Argo Rollouts
```yaml
strategy:
  canary:
    steps:
    - setWeight: 20
    - pause: { duration: 1m }
    - setWeight: 50
    - pause: { duration: 2m }
    - setWeight: 100
```

### Blue-Green
```yaml
strategy:
  blueGreen:
    activeService: my-app
    previewService: my-app-preview
    autoPromotionEnabled: false
```

**Opinions:**
- Use canary for most services -- lower risk than blue-green
- Blue-green for databases or stateful services where you need instant rollback
- Always define automatic rollback criteria (error rate, latency thresholds)
- Pair with Prometheus metrics analysis for automated promotion

## Secret Management in GitOps

Never commit plaintext secrets. Options:

| Tool | Approach | Best For |
|------|----------|----------|
| **External Secrets Operator** | Syncs from AWS SM/Vault/GCP SM | Cloud-native, team already uses secret manager |
| **Sealed Secrets** | Encrypt in Git, decrypt in cluster | Simple, self-contained |
| **SOPS** | Encrypt files with KMS/PGP | Works with any Git workflow |

**Default**: External Secrets Operator if using cloud provider. Sealed Secrets for simplicity.

## Troubleshooting

```bash
argocd app get my-app              # App status + sync state
argocd app diff my-app             # What would change
argocd app sync my-app --prune     # Force sync with pruning
argocd app sync my-app --force     # Force sync (recreates resources)
```

## Cross-References

- **devops:pipeline-design** -- CI/CD pipeline structure, approval gates, DORA metrics
- **devops:github-actions-patterns** -- reusable workflows, OIDC auth for cloud deploys
- **devops:docker-patterns** -- container builds, multi-stage images for GitOps pipelines
