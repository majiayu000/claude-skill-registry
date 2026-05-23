---
name: helm-argocd-gitops
description: Configure ArgoCD Applications and ApplicationSets for GitOps-based Helm deployments with sync policies and multi-environment support. Use when setting up ArgoCD Applications for Helm charts, configuring multi-environment deployments with ApplicationSets, implementing GitOps workflows, configuring sync policies and strategies, or setting up progressive delivery with Argo Rollouts.
version: 1.0.0
---

# Helm ArgoCD GitOps Integration

## Purpose

Guide the configuration of ArgoCD Applications and ApplicationSets for GitOps-based Helm chart deployments with proper sync policies, multi-environment support, and progressive delivery patterns.

## Basic ArgoCD Application Setup

### Step 1: Create Basic Application

```yaml
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
    repoURL: https://github.com/myorg/charts
    targetRevision: main
    path: charts/myapp
    helm:
      releaseName: myapp
      valueFiles:
        - values.yaml
        - values-prod.yaml
      parameters:
        - name: image.tag
          value: v1.0.0

  destination:
    server: https://kubernetes.default.svc
    namespace: myapp

  syncPolicy:
    automated:
      prune: false # Manual approval for deletions
      selfHeal: false # Manual approval for drift correction
    syncOptions:
      - CreateNamespace=true
      - PruneLast=true
    retry:
      limit: 5
      backoff:
        duration: 5s
        factor: 2
        maxDuration: 3m
```

**Key configuration points:**

- ✅ Add finalizer to ensure clean deletion
- ✅ Use multiple value files for environment overrides
- ✅ Set `PruneLast=true` to delete resources in correct order
- ✅ Configure retry with exponential backoff
- ✅ Be cautious with `automated.prune` in production

### Step 2: Deploy Application

```bash
# Create application
kubectl apply -f application.yaml

# Or use argocd CLI
argocd app create myapp \
  --repo https://github.com/myorg/charts \
  --path charts/myapp \
  --dest-server https://kubernetes.default.svc \
  --dest-namespace myapp \
  --values values.yaml \
  --values values-prod.yaml

# Sync application
argocd app sync myapp

# Get application status
argocd app get myapp

# View application diff
argocd app diff myapp
```

## Multi-Environment with ApplicationSet

### ApplicationSet for Multiple Environments

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: myapp-environments
  namespace: argocd
spec:
  generators:
    - list:
        elements:
          - env: dev
            cluster: https://dev.k8s.local
            namespace: myapp-dev
            autoPrune: "true"
            autoHeal: "true"
            imageTag: latest
          - env: staging
            cluster: https://staging.k8s.local
            namespace: myapp-staging
            autoPrune: "true"
            autoHeal: "true"
            imageTag: staging
          - env: prod
            cluster: https://prod.k8s.local
            namespace: myapp-prod
            autoPrune: "false" # Manual approval for prod
            autoHeal: "false"
            imageTag: v1.0.0

  template:
    metadata:
      name: "myapp-{{env}}"
      labels:
        environment: "{{env}}"
    spec:
      project: default
      source:
        repoURL: https://github.com/myorg/charts
        targetRevision: main
        path: charts/myapp
        helm:
          valueFiles:
            - values.yaml
            - environments/{{env}}/values.yaml
          parameters:
            - name: image.tag
              value: "{{imageTag}}"
      destination:
        server: "{{cluster}}"
        namespace: "{{namespace}}"
      syncPolicy:
        automated:
          prune: "{{autoPrune}}"
          selfHeal: "{{autoHeal}}"
        syncOptions:
          - CreateNamespace=true
          - PruneLast=true
```

**ApplicationSet benefits:**

- ✅ Single source of truth for all environments
- ✅ DRY principle - no duplicated manifests
- ✅ Easy to add new environments
- ✅ Consistent configuration with environment-specific overrides

### Git-Based ApplicationSet (Auto-Discovery)

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: cluster-apps
  namespace: argocd
spec:
  generators:
    - git:
        repoURL: https://github.com/myorg/cluster-config
        revision: HEAD
        directories:
          - path: apps/*

  template:
    metadata:
      name: "{{path.basename}}"
    spec:
      project: default
      source:
        repoURL: https://github.com/myorg/cluster-config
        targetRevision: HEAD
        path: "{{path}}"
        helm:
          valueFiles:
            - values.yaml
            - ../common-values.yaml
      destination:
        server: https://kubernetes.default.svc
        namespace: "{{path.basename}}"
      syncPolicy:
        automated:
          prune: true
          selfHeal: true
```

## Sync Policies for Different Environments

### Conservative (Production)

```yaml
syncPolicy:
  automated:
    prune: false # Manual approval for deletions
    selfHeal: false # Manual approval for drift correction
  syncOptions:
    - CreateNamespace=true
    - PruneLast=true
    - ApplyOutOfSyncOnly=true
  retry:
    limit: 5
    backoff:
      duration: 5s
      factor: 2
      maxDuration: 3m
```

### Progressive (Staging)

```yaml
syncPolicy:
  automated:
    prune: true # Auto-delete removed resources
    selfHeal: true # Auto-correct drift
  syncOptions:
    - CreateNamespace=true
    - PruneLast=true
  retry:
    limit: 5
    backoff:
      duration: 5s
      factor: 2
      maxDuration: 3m
```

### Aggressive (Development)

```yaml
syncPolicy:
  automated:
    prune: true
    selfHeal: true
    allowEmpty: false
  syncOptions:
    - CreateNamespace=true
    - PruneLast=true
    - Replace=true # Use replace instead of apply
  retry:
    limit: 2
    backoff:
      duration: 5s
      factor: 2
      maxDuration: 30s
```

## Sync Waves for Ordered Deployment

**Control deployment order with sync waves:**

```yaml
# Wave -1: Prerequisites (namespaces, CRDs)
apiVersion: v1
kind: Namespace
metadata:
  name: myapp
  annotations:
    argocd.argoproj.io/sync-wave: "-1"

---
# Wave 0: Configuration (ConfigMaps, Secrets)
apiVersion: v1
kind: ConfigMap
metadata:
  name: myapp-config
  annotations:
    argocd.argoproj.io/sync-wave: "0"

---
# Wave 1: Core services (Databases)
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgres
  annotations:
    argocd.argoproj.io/sync-wave: "1"

---
# Wave 2: Application deployments
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
  annotations:
    argocd.argoproj.io/sync-wave: "2"

---
# Wave 3: Ingress and routing
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: myapp
  annotations:
    argocd.argoproj.io/sync-wave: "3"
```

## Resource Hooks for Lifecycle Management

### Pre-Sync: Database Migration

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: myapp-migration
  annotations:
    argocd.argoproj.io/hook: PreSync
    argocd.argoproj.io/hook-delete-policy: HookSucceeded
spec:
  template:
    spec:
      containers:
        - name: migrate
          image: myapp:v1.0.0
          command: ["./migrate"]
      restartPolicy: Never
```

### Post-Sync: Smoke Test

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: myapp-smoke-test
  annotations:
    argocd.argoproj.io/hook: PostSync
    argocd.argoproj.io/hook-delete-policy: HookSucceeded
spec:
  template:
    spec:
      containers:
        - name: test
          image: curlimages/curl:latest
          command:
            - sh
            - -c
            - |
              curl -f http://myapp:80/healthz || exit 1
      restartPolicy: Never
```

## Helm Value File Structure for GitOps

**Organize values for multi-environment:**

```
charts/myapp/
├── values.yaml                    # Base defaults
├── environments/
│   ├── dev/
│   │   ├── values.yaml           # Dev overrides
│   │   └── secrets.enc.yaml      # Encrypted secrets
│   ├── staging/
│   │   ├── values.yaml
│   │   └── secrets.enc.yaml
│   └── prod/
│       ├── values.yaml
│       └── secrets.enc.yaml
└── clusters/
    ├── cluster-1-values.yaml
    └── cluster-2-values.yaml
```

**ArgoCD Application references:**

```yaml
helm:
  valueFiles:
    - values.yaml # Base
    - environments/{{env}}/values.yaml # Environment
    - clusters/{{cluster}}-values.yaml # Cluster-specific
```

## App of Apps Pattern

**Root application that manages other applications:**

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: root-app
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/myorg/cluster-config
    targetRevision: HEAD
    path: apps
  destination:
    server: https://kubernetes.default.svc
    namespace: argocd
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

## Monitoring ArgoCD Deployments

### Check Application Status

```bash
# Get application details
argocd app get myapp

# List all applications
argocd app list

# View sync history
argocd app history myapp

# View application events
argocd app events myapp
```

### Prometheus Metrics

```
# Application sync status
argocd_app_sync_status{name="myapp",namespace="argocd"}

# Application health
argocd_app_health_status{name="myapp",namespace="argocd"}

# Sync operation duration
argocd_app_sync_duration_seconds{name="myapp"}
```

### Alerting Rules

```yaml
groups:
  - name: argocd
    rules:
      - alert: ApplicationOutOfSync
        expr: argocd_app_sync_status{sync_status="OutOfSync"} == 1
        for: 15m
        annotations:
          summary: "Application {{ $labels.name }} is out of sync"

      - alert: ApplicationUnhealthy
        expr: argocd_app_health_status{health_status="Degraded"} == 1
        for: 5m
        annotations:
          summary: "Application {{ $labels.name }} is unhealthy"
```

## Troubleshooting Common Issues

### Issue: Application stuck in "OutOfSync"

**Diagnosis:**

```bash
# Check app details
argocd app get myapp

# View diff
argocd app diff myapp

# Check sync status
argocd app sync myapp --dry-run
```

**Common causes:**

- Resource field managed by controller (add to `ignoreDifferences`)
- Invalid Helm template syntax
- Missing CRD
- Namespace doesn't exist

### Issue: Sync fails with "resource already exists"

**Solution:**

```yaml
# Add annotation to take ownership
metadata:
  annotations:
    argocd.argoproj.io/sync-options: Replace=true
```

### Issue: Helm values not being applied

**Diagnosis:**

```bash
# Check rendered values
argocd app manifests myapp

# Verify value file exists in repo
# Check Application spec for correct valueFiles path
```

## Common ArgoCD Commands

```bash
# Create application
argocd app create myapp \
  --repo https://github.com/myorg/charts \
  --path charts/myapp \
  --dest-server https://kubernetes.default.svc \
  --dest-namespace myapp

# Sync application
argocd app sync myapp

# Sync with prune
argocd app sync myapp --prune

# Delete application
argocd app delete myapp

# Rollback to previous version
argocd app rollback myapp

# View application logs
argocd app logs myapp

# Set application parameters
argocd app set myapp --parameter image.tag=v2.0.0
```

## Resources

- [ArgoCD Documentation](https://argo-cd.readthedocs.io/)
- [ApplicationSet Documentation](https://argocd-applicationset.readthedocs.io/)
- [Argo Rollouts](https://argoproj.github.io/argo-rollouts/)
- [GitOps Principles](https://opengitops.dev/)

---

## Related Agent

For comprehensive Helm/Kubernetes guidance that coordinates this and other Helm skills, use the **`helm-kubernetes-expert`** agent.
