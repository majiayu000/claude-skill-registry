---
name: gitops-workflows
description: "GitOps deployment patterns with ArgoCD and Flux. Use when implementing Git-based infrastructure management, continuous deployment, or declarative operations."
---

# GitOps Workflows

Git as the single source of truth for declarative infrastructure and applications.

## When to Use

- Implementing continuous deployment to Kubernetes
- Managing infrastructure changes through Git
- Setting up ArgoCD or Flux
- Designing promotion workflows (dev → staging → prod)
- Implementing drift detection and remediation

## Core Principles

| Principle | Description |
|-----------|-------------|
| Declarative | Desired state described in Git |
| Versioned | Full history of changes |
| Automated | Changes applied automatically |
| Auditable | Git commits = audit trail |

## Repository Structure

### Monorepo Pattern

```
gitops-repo/
├── apps/
│   ├── base/                    # Base manifests
│   │   └── myapp/
│   │       ├── deployment.yaml
│   │       ├── service.yaml
│   │       └── kustomization.yaml
│   └── overlays/
│       ├── development/
│       │   └── kustomization.yaml
│       ├── staging/
│       │   └── kustomization.yaml
│       └── production/
│           └── kustomization.yaml
│
├── infrastructure/
│   ├── base/
│   │   ├── cert-manager/
│   │   ├── ingress-nginx/
│   │   └── monitoring/
│   └── overlays/
│       └── production/
│
└── clusters/
    ├── development/
    │   └── apps.yaml            # ArgoCD Application
    ├── staging/
    └── production/
```

## ArgoCD

### Installation

```bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

### Application Definition

```yaml
# clusters/production/myapp.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: myapp
  namespace: argocd
  finalizers:
    - resources-finalizer.argocd.argoproj.io
spec:
  project: default

  source:
    repoURL: https://github.com/org/gitops-repo.git
    targetRevision: main
    path: apps/overlays/production

  destination:
    server: https://kubernetes.default.svc
    namespace: myapp

  syncPolicy:
    automated:
      prune: true
      selfHeal: true
      allowEmpty: false
    syncOptions:
      - CreateNamespace=true
      - PrunePropagationPolicy=foreground
      - PruneLast=true
    retry:
      limit: 5
      backoff:
        duration: 5s
        factor: 2
        maxDuration: 3m

  # Health checks
  ignoreDifferences:
    - group: apps
      kind: Deployment
      jsonPointers:
        - /spec/replicas  # Ignore HPA changes
```

### ApplicationSet (Multi-Environment)

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: myapp
  namespace: argocd
spec:
  generators:
    - list:
        elements:
          - cluster: development
            url: https://dev-cluster.example.com
          - cluster: staging
            url: https://staging-cluster.example.com
          - cluster: production
            url: https://prod-cluster.example.com

  template:
    metadata:
      name: 'myapp-{{cluster}}'
    spec:
      project: default
      source:
        repoURL: https://github.com/org/gitops-repo.git
        targetRevision: main
        path: 'apps/overlays/{{cluster}}'
      destination:
        server: '{{url}}'
        namespace: myapp
      syncPolicy:
        automated:
          prune: true
          selfHeal: true
```

## Flux

### Installation

```bash
flux bootstrap github \
  --owner=my-org \
  --repository=gitops-repo \
  --branch=main \
  --path=clusters/production \
  --personal
```

### GitRepository Source

```yaml
apiVersion: source.toolkit.fluxcd.io/v1
kind: GitRepository
metadata:
  name: gitops-repo
  namespace: flux-system
spec:
  interval: 1m
  url: https://github.com/org/gitops-repo
  ref:
    branch: main
  secretRef:
    name: github-token
```

### Kustomization

```yaml
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: myapp
  namespace: flux-system
spec:
  interval: 10m
  targetNamespace: myapp
  sourceRef:
    kind: GitRepository
    name: gitops-repo
  path: ./apps/overlays/production
  prune: true
  healthChecks:
    - apiVersion: apps/v1
      kind: Deployment
      name: myapp
      namespace: myapp
  timeout: 2m
```

### HelmRelease

```yaml
apiVersion: helm.toolkit.fluxcd.io/v2beta1
kind: HelmRelease
metadata:
  name: myapp
  namespace: myapp
spec:
  interval: 5m
  chart:
    spec:
      chart: myapp
      version: "1.x"
      sourceRef:
        kind: HelmRepository
        name: myrepo
        namespace: flux-system
  values:
    replicas: 3
    image:
      tag: v1.0.0
  valuesFrom:
    - kind: ConfigMap
      name: myapp-values
```

## Promotion Strategies

### Environment Promotion

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ Development │────▶│   Staging   │────▶│ Production  │
│             │     │             │     │             │
│  Auto-sync  │     │  Auto-sync  │     │ Manual/Gate │
│  on commit  │     │  on merge   │     │  approval   │
└─────────────┘     └─────────────┘     └─────────────┘
```

### Image Update Automation (Flux)

```yaml
apiVersion: image.toolkit.fluxcd.io/v1beta1
kind: ImageRepository
metadata:
  name: myapp
  namespace: flux-system
spec:
  image: registry.example.com/myapp
  interval: 1m
---
apiVersion: image.toolkit.fluxcd.io/v1beta1
kind: ImagePolicy
metadata:
  name: myapp
  namespace: flux-system
spec:
  imageRepositoryRef:
    name: myapp
  policy:
    semver:
      range: 1.x
---
apiVersion: image.toolkit.fluxcd.io/v1beta1
kind: ImageUpdateAutomation
metadata:
  name: myapp
  namespace: flux-system
spec:
  interval: 1m
  sourceRef:
    kind: GitRepository
    name: gitops-repo
  git:
    checkout:
      ref:
        branch: main
    commit:
      author:
        email: flux@example.com
        name: Flux
      messageTemplate: 'Update {{.AutomationObject.Name}} to {{.NewVersion}}'
    push:
      branch: main
  update:
    path: ./apps/overlays/production
    strategy: Setters
```

## Kustomize Overlays

### Base Deployment

```yaml
# apps/base/myapp/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 1
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
        - name: myapp
          image: myapp:latest
          ports:
            - containerPort: 8080
          resources:
            requests:
              cpu: 100m
              memory: 128Mi
```

### Production Overlay

```yaml
# apps/overlays/production/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
namespace: myapp-prod

resources:
  - ../../base/myapp

replicas:
  - name: myapp
    count: 5

images:
  - name: myapp
    newTag: v1.2.3

patches:
  - patch: |-
      - op: replace
        path: /spec/template/spec/containers/0/resources
        value:
          requests:
            cpu: 500m
            memory: 512Mi
          limits:
            cpu: 1000m
            memory: 1Gi
    target:
      kind: Deployment
      name: myapp

configMapGenerator:
  - name: myapp-config
    literals:
      - LOG_LEVEL=info
      - ENV=production
```

## Best Practices

1. **Separate app and infra repos** for different change velocities
2. **Use sealed-secrets or external-secrets** for secrets in Git
3. **Implement branch protection** on GitOps repos
4. **Use PR reviews** for production changes
5. **Set up notifications** for sync failures
6. **Implement rollback procedures** via Git revert

## Troubleshooting

```bash
# ArgoCD
argocd app list
argocd app get myapp
argocd app sync myapp
argocd app history myapp
argocd app rollback myapp <revision>

# Flux
flux get all
flux reconcile kustomization myapp
flux logs --follow
flux events
```

## Integration

Works with:
- `/k8s` - Kubernetes manifests
- `/terraform` - Infrastructure provisioning
- `/devops` - CI/CD pipelines
- `policy-as-code` skill - Pre-commit validation
