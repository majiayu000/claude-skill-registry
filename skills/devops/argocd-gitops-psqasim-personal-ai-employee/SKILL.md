---
name: argocd-gitops
description: Expert guidance for implementing GitOps with ArgoCD to automate Kubernetes deployments from hello-world to production pipelines. Use when working with (1) ArgoCD installation and configuration, (2) Application deployment and management, (3) Sync strategies (auto-sync, manual sync, sync waves), (4) Multi-cluster deployments, (5) ApplicationSets and App of Apps pattern, (6) Progressive delivery (blue-green, canary), (7) GitOps workflows, (8) Production best practices, (9) RBAC and security, (10) Monitoring and troubleshooting.
---

# ArgoCD GitOps

Automate Kubernetes deployments with GitOps - from local development to production CI/CD pipelines.

## Core Concepts

### What is GitOps?

GitOps uses Git as the single source of truth for declarative infrastructure and applications. Changes are made via Git commits, and automated processes sync the desired state to clusters.

**GitOps principles:**
1. **Declarative** - System described declaratively
2. **Versioned** - State stored in Git
3. **Automated** - Changes applied automatically
4. **Continuously reconciled** - Agents ensure desired state

### ArgoCD Architecture

```
┌─────────────┐
│ Git Repo    │ ← Source of Truth
└──────┬──────┘
       │
┌──────▼──────────────────────────┐
│ ArgoCD                           │
│ ├─ API Server (UI/CLI)          │
│ ├─ Repository Server (manifests)│
│ └─ Application Controller (sync)│
└──────┬──────────────────────────┘
       │
┌──────▼──────┐
│ Kubernetes  │
│ Cluster(s)  │
└─────────────┘
```

**Key components:**
- **Application** - Kubernetes resources defined in Git
- **Project** - Logical grouping for multi-tenancy
- **Sync Status** - Comparison of Git vs cluster state
- **Health Status** - Application resource health

## Quick Start

### Installation

```bash
# Create namespace
kubectl create namespace argocd

# Install ArgoCD
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Wait for pods
kubectl wait --for=condition=Ready pods --all -n argocd --timeout=300s

# Get admin password
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d

# Port-forward UI (or use LoadBalancer/Ingress)
kubectl port-forward svc/argocd-server -n argocd 8080:443
```

**Access UI:** https://localhost:8080 (username: `admin`, password from above)

### CLI Setup

```bash
# Download CLI
curl -sSL -o argocd https://github.com/argoproj/argo-cd/releases/latest/download/argocd-linux-amd64
chmod +x argocd
sudo mv argocd /usr/local/bin/

# Login
argocd login localhost:8080 --insecure
```

### Hello World Application

**1. Create Git repository with Kubernetes manifests:**

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: hello-world
spec:
  replicas: 2
  selector:
    matchLabels:
      app: hello-world
  template:
    metadata:
      labels:
        app: hello-world
    spec:
      containers:
      - name: hello
        image: nginx:1.21
        ports:
        - containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: hello-world
spec:
  selector:
    app: hello-world
  ports:
  - port: 80
    targetPort: 80
  type: ClusterIP
```

**2. Create ArgoCD Application:**

```bash
argocd app create hello-world \
  --repo https://github.com/your-org/your-repo.git \
  --path manifests \
  --dest-server https://kubernetes.default.svc \
  --dest-namespace default
```

**3. Sync application:**

```bash
# Manual sync
argocd app sync hello-world

# Check status
argocd app get hello-world
```

See `assets/hello-world-app.yaml` for declarative YAML version.

## Application Management

### Declarative Application

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: myapp
  namespace: argocd
spec:
  project: default

  source:
    repoURL: https://github.com/myorg/myapp.git
    targetRevision: HEAD
    path: k8s/overlays/production

  destination:
    server: https://kubernetes.default.svc
    namespace: myapp

  syncPolicy:
    automated:
      prune: true      # Delete resources not in Git
      selfHeal: true   # Sync when cluster state drifts
    syncOptions:
    - CreateNamespace=true

    retry:
      limit: 5
      backoff:
        duration: 5s
        factor: 2
        maxDuration: 3m
```

### Sync Strategies

**Manual Sync:**

```bash
# Sync entire application
argocd app sync myapp

# Sync specific resources
argocd app sync myapp --resource :Service:my-service
argocd app sync myapp --resource apps:Deployment:my-app

# Dry run
argocd app sync myapp --dry-run

# Force sync (override hooks)
argocd app sync myapp --force
```

**Auto Sync:**

```yaml
syncPolicy:
  automated:
    prune: true
    selfHeal: true
```

**Sync Windows:** Control when syncs can occur.

```yaml
syncPolicy:
  syncOptions:
  - SkipDryRunOnMissingResource=true
```

### Sync Waves

Control deployment order with annotations:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: database
  annotations:
    argocd.argoproj.io/sync-wave: "0"  # Deploy first
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
  annotations:
    argocd.argoproj.io/sync-wave: "1"  # Deploy after DB
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend
  annotations:
    argocd.argoproj.io/sync-wave: "2"  # Deploy last
```

### Hooks

Execute tasks at specific points in sync lifecycle:

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: db-migration
  annotations:
    argocd.argoproj.io/hook: PreSync
    argocd.argoproj.io/hook-delete-policy: BeforeHookCreation
spec:
  template:
    spec:
      containers:
      - name: migrate
        image: myapp/migrator:v1
        command: ["./migrate.sh"]
      restartPolicy: Never
```

**Hook types:**
- `PreSync` - Before sync
- `Sync` - During sync
- `PostSync` - After sync
- `SyncFail` - On sync failure
- `Skip` - Skip resource in sync

## Multi-Source Applications

Combine multiple Git sources:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: multi-source-app
spec:
  sources:
  - repoURL: https://github.com/myorg/base-manifests.git
    path: base
    targetRevision: main
  - repoURL: https://github.com/myorg/overlay-configs.git
    path: overlays/production
    targetRevision: main
  - repoURL: https://charts.helm.sh/stable
    chart: postgresql
    targetRevision: 11.1.0
    helm:
      values: |
        replicaCount: 3
```

## ApplicationSets

Deploy to multiple clusters/environments declaratively.

### List Generator

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: multi-env
spec:
  generators:
  - list:
      elements:
      - cluster: dev
        url: https://dev.k8s.local
        namespace: dev
      - cluster: staging
        url: https://staging.k8s.local
        namespace: staging
      - cluster: prod
        url: https://prod.k8s.local
        namespace: prod
  template:
    metadata:
      name: 'myapp-{{cluster}}'
    spec:
      project: default
      source:
        repoURL: https://github.com/myorg/myapp.git
        path: 'overlays/{{cluster}}'
        targetRevision: HEAD
      destination:
        server: '{{url}}'
        namespace: '{{namespace}}'
      syncPolicy:
        automated:
          prune: true
```

### Cluster Generator

Automatically deploy to all registered clusters:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: cluster-apps
spec:
  generators:
  - cluster:
      selector:
        matchLabels:
          environment: production
  template:
    metadata:
      name: '{{name}}-myapp'
    spec:
      source:
        repoURL: https://github.com/myorg/myapp.git
        path: manifests
      destination:
        server: '{{server}}'
        namespace: myapp
```

### Git Generator

Deploy based on Git directory structure:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: git-apps
spec:
  generators:
  - git:
      repoURL: https://github.com/myorg/apps.git
      revision: HEAD
      directories:
      - path: apps/*
  template:
    metadata:
      name: '{{path.basename}}'
    spec:
      source:
        repoURL: https://github.com/myorg/apps.git
        path: '{{path}}'
      destination:
        server: https://kubernetes.default.svc
        namespace: '{{path.basename}}'
```

## App of Apps Pattern

Manage multiple applications as a single unit:

```yaml
# root-app.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: root-app
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/myorg/infrastructure.git
    path: apps
    targetRevision: HEAD
  destination:
    server: https://kubernetes.default.svc
    namespace: argocd
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

**Directory structure:**

```
apps/
├── app1.yaml
├── app2.yaml
├── app3.yaml
└── ...
```

Each file defines an Application CR.

## Progressive Delivery

### Blue-Green Deployment

```yaml
# With Argo Rollouts integration
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: myapp
spec:
  replicas: 3
  strategy:
    blueGreen:
      activeService: myapp-active
      previewService: myapp-preview
      autoPromotionEnabled: false
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
        image: myapp:v2
```

### Canary Deployment

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: myapp
spec:
  replicas: 10
  strategy:
    canary:
      steps:
      - setWeight: 20
      - pause: {duration: 1m}
      - setWeight: 40
      - pause: {duration: 1m}
      - setWeight: 60
      - pause: {duration: 1m}
      - setWeight: 80
      - pause: {duration: 1m}
```

### Progressive Sync (ApplicationSet)

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: progressive-rollout
spec:
  strategy:
    type: RollingSync
    rollingSync:
      steps:
      - matchExpressions:
        - key: environment
          operator: In
          values: [dev]
      - matchExpressions:
        - key: environment
          operator: In
          values: [staging]
      - matchExpressions:
        - key: environment
          operator: In
          values: [prod]
        maxUpdate: 10%  # Update 10% at a time
```

## Production Deployment

### High Availability

See [PRODUCTION_GUIDE.md](references/PRODUCTION_GUIDE.md) for complete HA setup.

**Key components:**
- Multiple replicas of all components
- Redis for HA
- External database (PostgreSQL)
- Load balancer for API server

### Declarative Setup

Store ArgoCD configuration in Git:

```
infrastructure/
├── argocd/
│   ├── install.yaml
│   ├── projects/
│   │   ├── team-a.yaml
│   │   └── team-b.yaml
│   ├── applications/
│   │   ├── app1.yaml
│   │   └── app2.yaml
│   └── applicationsets/
│       └── multi-cluster.yaml
```

### RBAC

```yaml
# AppProject with RBAC
apiVersion: argoproj.io/v1alpha1
kind: AppProject
metadata:
  name: team-a
spec:
  description: Team A applications
  sourceRepos:
  - 'https://github.com/myorg/team-a-*'
  destinations:
  - namespace: 'team-a-*'
    server: https://kubernetes.default.svc
  clusterResourceWhitelist:
  - group: ''
    kind: Namespace
  namespaceResourceWhitelist:
  - group: '*'
    kind: '*'
```

## Tool Support

ArgoCD supports multiple configuration tools:

- **Plain YAML** - Standard Kubernetes manifests
- **Kustomize** - Overlays and patches
- **Helm** - Chart deployments with values
- **Jsonnet** - Programmatic generation
- **Custom plugins** - Extend with any tool

### Kustomize Example

```yaml
source:
  repoURL: https://github.com/myorg/myapp.git
  path: k8s/overlays/production
  targetRevision: HEAD
  kustomize:
    images:
    - myapp=myapp:v1.2.3
```

### Helm Example

```yaml
source:
  repoURL: https://charts.helm.sh/stable
  chart: nginx-ingress
  targetRevision: 1.41.3
  helm:
    releaseName: nginx
    values: |
      controller:
        replicaCount: 3
    parameters:
    - name: service.type
      value: LoadBalancer
```

## Best Practices

1. **One Git repo per application** - Clear ownership
2. **Use ApplicationSets for multi-env** - DRY principle
3. **Enable auto-sync cautiously** - Start manual, automate gradually
4. **Always set prune and selfHeal** - Keep clusters clean
5. **Use Projects for multi-tenancy** - Isolate teams
6. **Implement sync waves** - Control deployment order
7. **Use hooks for migrations** - Database changes, etc.
8. **Monitor sync status** - Alert on OutOfSync
9. **Version everything in Git** - Including ArgoCD config
10. **Test in dev before prod** - Progressive rollouts

## Troubleshooting

### Application OutOfSync

```bash
# Check differences
argocd app diff myapp

# Force sync
argocd app sync myapp --force

# Ignore differences
argocd app set myapp --sync-option IgnoreDifferences=all
```

### Sync Failures

```bash
# Check sync status
argocd app get myapp

# View logs
kubectl logs -n argocd -l app.kubernetes.io/name=argocd-application-controller

# Retry sync
argocd app sync myapp --retry-limit 5
```

### Common Issues

**Resource stuck in Progressing:**
- Check resource events: `kubectl describe <resource>`
- Verify health checks
- Check sync waves order

**Prune not working:**
- Ensure `prune: true` in syncPolicy
- Check for `Preserve` annotation
- Verify resource ownership

See [TROUBLESHOOTING.md](references/TROUBLESHOOTING.md) for detailed diagnostics.

## Reference Files

- **[PRODUCTION_GUIDE.md](references/PRODUCTION_GUIDE.md)** - HA setup, security, disaster recovery
- **[APPLICATIONSETS_GUIDE.md](references/APPLICATIONSETS_GUIDE.md)** - Advanced ApplicationSet patterns
- **[TROUBLESHOOTING.md](references/TROUBLESHOOTING.md)** - Common issues and solutions

## Example Assets

Templates ready to use:

- `hello-world-app.yaml` - Simple application
- `multi-env-appset.yaml` - Multi-environment ApplicationSet
- `app-of-apps.yaml` - App of Apps pattern
- `progressive-rollout.yaml` - Progressive delivery
