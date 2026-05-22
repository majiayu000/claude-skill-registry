---
name: argocd-gitops
description: ArgoCD GitOps patterns including sync waves, app-of-apps, multi-source applications, and Helm value overlays.
agents: [bolt]
triggers: [argocd, gitops, sync, app-of-apps, helm, deploy, application]
---

# ArgoCD GitOps Patterns

Core GitOps workflow patterns for declarative infrastructure management.

## Sync Wave Ordering

Sync waves control deployment order. Lower numbers deploy first.

| Wave | Purpose | Examples |
|------|---------|----------|
| `-10` | Storage (CSI) | Mayastor |
| `-3` | Secrets vault | OpenBao |
| `-2` | Secrets sync | External Secrets |
| `-1` | Observability, VPN | Jaeger, Kilo |
| `0` | Default | Most operators |
| `1` | Application layer | KubeAI, apps |
| `2` | Dependent services | Harbor |

```yaml
metadata:
  annotations:
    argocd.argoproj.io/sync-wave: "-2"
```

## App-of-Apps Pattern

Parent application deploys child applications:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: platform-apps
  namespace: argocd
spec:
  project: platform
  source:
    repoURL: https://github.com/5dlabs/cto
    targetRevision: develop
    path: infra/gitops/applications/platform
    directory:
      recurse: false
  destination:
    server: https://kubernetes.default.svc
    namespace: argocd
```

## Multi-Source Applications

Combine Helm chart with local manifests:

```yaml
spec:
  sources:
    # Source 1: Helm chart
    - repoURL: https://charts.example.io
      chart: myapp
      targetRevision: 1.0.0
      helm:
        values: |
          replicas: 2

    # Source 2: Supplementary manifests
    - repoURL: https://github.com/5dlabs/cto
      targetRevision: develop
      path: infra/gitops/manifests/myapp
      directory:
        include: "*.yaml"
```

## Helm Values Configuration

Inline values in ArgoCD Application:

```yaml
spec:
  source:
    repoURL: https://charts.example.io
    chart: myapp
    targetRevision: 1.0.0
    helm:
      values: |
        # Pod labels for log collection
        podLabels:
          platform.5dlabs.io/log-collection: enabled
        
        # Resource limits
        resources:
          requests:
            cpu: 100m
            memory: 256Mi
          limits:
            cpu: 500m
            memory: 512Mi
```

## ignoreDifferences Patterns

Prevent spurious diffs from dynamic fields:

```yaml
spec:
  ignoreDifferences:
    # Webhook CA bundles (managed by cert-manager)
    - group: admissionregistration.k8s.io
      kind: ValidatingWebhookConfiguration
      jsonPointers:
        - /webhooks/0/clientConfig/caBundle
    
    # StatefulSet volumeClaimTemplates (K8s normalizes)
    - group: apps
      kind: StatefulSet
      jsonPointers:
        - /spec/volumeClaimTemplates
    
    # CRD annotations (managed by operator)
    - group: apiextensions.k8s.io
      kind: CustomResourceDefinition
      jsonPointers:
        - /metadata/annotations
```

## Sync Policy

Standard sync policy for automated GitOps:

```yaml
spec:
  syncPolicy:
    automated:
      prune: true        # Remove resources not in git
      selfHeal: true     # Revert manual changes
      allowEmpty: false  # Prevent accidental deletion
    
    syncOptions:
      - CreateNamespace=true
      - ServerSideApply=true
      - PrunePropagationPolicy=foreground
      - RespectIgnoreDifferences=true
    
    retry:
      limit: 5
      backoff:
        duration: 10s
        factor: 2
        maxDuration: 3m
```

## Project Configuration

Define allowed sources and destinations:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: AppProject
metadata:
  name: platform
  namespace: argocd
spec:
  sourceRepos:
    - https://github.com/5dlabs/*
    - https://charts.external-secrets.io
  destinations:
    - namespace: '*'
      server: https://kubernetes.default.svc
  clusterResourceWhitelist:
    - group: '*'
      kind: '*'
```

## Validation Commands

```bash
# Check application status
argocd app get <app-name>
argocd app diff <app-name>

# Sync manually (if needed)
argocd app sync <app-name>

# Check sync waves
kubectl get applications -n argocd -o custom-columns=\
'NAME:.metadata.name,WAVE:.metadata.annotations.argocd\.argoproj\.io/sync-wave'
```

## Best Practices

1. **Use sync waves** - Deploy dependencies before dependents
2. **Define ignoreDifferences** - Prevent unnecessary reconciliation
3. **Enable selfHeal** - Auto-revert manual drift
4. **Use ServerSideApply** - Better handling of large manifests
5. **Set retry policies** - Handle transient failures gracefully
6. **Label for observability** - Add `platform.5dlabs.io/log-collection: enabled`
