---
name: argocd
description: GitOps continuous delivery with Argo CD for Kubernetes deployments. Use when implementing declarative GitOps workflows, application sync/rollback, multi-cluster deployments, progressive delivery, or CD automation. Triggers: argocd, argo cd, gitops, application, sync, rollback, app of apps, applicationset, declarative, continuous delivery, CD, deployment automation, kubernetes deployment, multi-cluster, canary deployment, blue-green.
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
---

# Argo CD GitOps Continuous Delivery

## Overview

Argo CD is a declarative, GitOps continuous delivery tool for Kubernetes that automates application deployment and lifecycle management. It follows the GitOps pattern where Git repositories are the source of truth for defining the desired application state.

### Core Concepts

- **Application**: A group of Kubernetes resources defined by a manifest in Git
- **Application Source Type**: The tool/format used to define the application (Helm, Kustomize, plain YAML, Jsonnet)
- **Target State**: The desired state of an application as represented in Git
- **Live State**: The actual state of an application running in Kubernetes
- **Sync Status**: Whether the live state matches the target state
- **Sync**: The process of making the live state match the target state
- **Health**: The health status of application resources
- **Refresh**: Compare the latest code in Git with the live state
- **Project**: A logical grouping of applications with RBAC policies

## Installation and Setup

### Install Argo CD in Kubernetes

```bash
# Create namespace
kubectl create namespace argocd

# Install Argo CD
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Install with HA (production)
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/ha/install.yaml

# Access the UI
kubectl port-forward svc/argocd-server -n argocd 8080:443

# Get initial admin password
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d

# Install CLI
brew install argocd  # macOS
# Or download from https://github.com/argoproj/argo-cd/releases
```

### Initial Configuration

```bash
# Login via CLI
argocd login localhost:8080

# Change admin password
argocd account update-password

# Register external cluster
argocd cluster add my-cluster-context

# Add Git repository
argocd repo add https://github.com/myorg/myrepo.git --username myuser --password mytoken
```

## Repository Structure

### Recommended Directory Layout

```text
gitops-repo/
├── apps/                           # Application definitions
│   ├── base/                       # Base application configs
│   │   ├── app1/
│   │   │   ├── kustomization.yaml
│   │   │   └── deployment.yaml
│   │   └── app2/
│   └── overlays/                   # Environment-specific overlays
│       ├── dev/
│       │   ├── kustomization.yaml
│       │   └── patches/
│       ├── staging/
│       └── production/
├── charts/                         # Helm charts (if using Helm)
│   └── myapp/
│       ├── Chart.yaml
│       ├── values.yaml
│       └── templates/
├── argocd/                         # Argo CD configuration
│   ├── projects/                   # AppProjects
│   ├── applications/               # Application manifests
│   │   ├── app1.yaml
│   │   └── app2.yaml
│   └── applicationsets/            # ApplicationSets
│       ├── cluster-apps.yaml
│       └── tenant-apps.yaml
└── bootstrap/                      # App of apps bootstrap
    └── root-app.yaml
```

### Separation Strategies

#### Mono-repo

Single repository for all environments

- Pros: Simpler management, easier to track changes
- Cons: All teams have access, harder to enforce separation

#### Repo-per-environment

Separate repositories for dev/staging/prod

- Pros: Better security boundaries, clear promotion path
- Cons: More repositories to manage, duplicate configuration

#### Repo-per-team

Separate repositories per team/service

- Pros: Team autonomy, clear ownership
- Cons: Cross-team coordination complexity

## Application Manifests

### Basic Application

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: myapp
  namespace: argocd
  # Finalizer ensures cascade delete
  finalizers:
    - resources-finalizer.argocd.argoproj.io
spec:
  # Project name (default is 'default')
  project: default

  # Source configuration
  source:
    repoURL: https://github.com/myorg/myrepo.git
    targetRevision: HEAD
    path: apps/production/myapp

  # Destination cluster and namespace
  destination:
    server: https://kubernetes.default.svc
    namespace: myapp-production

  # Sync policy
  syncPolicy:
    automated:
      prune: true # Delete resources not in Git
      selfHeal: true # Auto-sync when cluster state differs
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
```

### Application with Helm

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: myapp-helm
  namespace: argocd
spec:
  project: default

  source:
    repoURL: https://github.com/myorg/charts.git
    targetRevision: main
    path: charts/myapp
    helm:
      # Helm values files
      valueFiles:
        - values.yaml
        - values-production.yaml

      # Inline values (highest priority)
      values: |
        replicaCount: 3
        image:
          tag: v1.2.3
        resources:
          limits:
            cpu: 500m
            memory: 512Mi

      # Override specific values
      parameters:
        - name: image.repository
          value: myregistry.io/myapp

      # Skip CRDs installation
      skipCrds: false

      # Release name
      releaseName: myapp

  destination:
    server: https://kubernetes.default.svc
    namespace: myapp

  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
```

### Application with Kustomize

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: myapp-kustomize
  namespace: argocd
spec:
  project: default

  source:
    repoURL: https://github.com/myorg/myrepo.git
    targetRevision: HEAD
    path: apps/overlays/production
    kustomize:
      # Kustomize version
      version: v5.0.0

      # Name prefix/suffix
      namePrefix: prod-
      nameSuffix: -v1

      # Images to override
      images:
        - name: myapp
          newName: myregistry.io/myapp
          newTag: v1.2.3

      # Common labels
      commonLabels:
        environment: production
        managed-by: argocd

      # Common annotations
      commonAnnotations:
        deployed-by: argocd

      # Replicas override
      replicas:
        - name: myapp-deployment
          count: 3

  destination:
    server: https://kubernetes.default.svc
    namespace: myapp-production
```

## ApplicationSets

### Cluster Generator

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: cluster-apps
  namespace: argocd
spec:
  # Generate applications for all registered clusters
  generators:
    - clusters:
        selector:
          matchLabels:
            env: production
          matchExpressions:
            - key: region
              operator: In
              values: [us-east-1, us-west-2]
        values:
          # Default values available in template
          revision: main

  template:
    metadata:
      name: "{{name}}-myapp"
      labels:
        cluster: "{{name}}"
    spec:
      project: default
      source:
        repoURL: https://github.com/myorg/myrepo.git
        targetRevision: "{{values.revision}}"
        path: apps/production/myapp
        helm:
          parameters:
            - name: cluster.name
              value: "{{name}}"
            - name: cluster.region
              value: "{{metadata.labels.region}}"
      destination:
        server: "{{server}}"
        namespace: myapp
      syncPolicy:
        automated:
          prune: true
          selfHeal: true
        syncOptions:
          - CreateNamespace=true
```

### Git Directory Generator

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: git-directory-apps
  namespace: argocd
spec:
  generators:
    - git:
        repoURL: https://github.com/myorg/myrepo.git
        revision: HEAD
        directories:
          - path: apps/production/*
          - path: apps/production/exclude-this
            exclude: true

  template:
    metadata:
      name: "{{path.basename}}"
    spec:
      project: default
      source:
        repoURL: https://github.com/myorg/myrepo.git
        targetRevision: HEAD
        path: "{{path}}"
      destination:
        server: https://kubernetes.default.svc
        namespace: "{{path.basename}}"
      syncPolicy:
        automated:
          prune: true
          selfHeal: true
```

### Git File Generator

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: git-file-apps
  namespace: argocd
spec:
  generators:
    - git:
        repoURL: https://github.com/myorg/myrepo.git
        revision: HEAD
        files:
          - path: apps/*/config.json

  template:
    metadata:
      name: "{{app.name}}"
    spec:
      project: default
      source:
        repoURL: https://github.com/myorg/myrepo.git
        targetRevision: HEAD
        path: "apps/{{app.name}}"
        helm:
          parameters:
            - name: replicaCount
              value: "{{app.replicas}}"
            - name: environment
              value: "{{app.environment}}"
      destination:
        server: https://kubernetes.default.svc
        namespace: "{{app.namespace}}"
```

### Matrix Generator

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: matrix-apps
  namespace: argocd
spec:
  generators:
    # Matrix combines multiple generators
    - matrix:
        generators:
          # First dimension: clusters
          - clusters:
              selector:
                matchLabels:
                  env: production
          # Second dimension: git directories
          - git:
              repoURL: https://github.com/myorg/myrepo.git
              revision: HEAD
              directories:
                - path: apps/*

  template:
    metadata:
      name: "{{path.basename}}-{{name}}"
    spec:
      project: default
      source:
        repoURL: https://github.com/myorg/myrepo.git
        targetRevision: HEAD
        path: "{{path}}"
      destination:
        server: "{{server}}"
        namespace: "{{path.basename}}"
      syncPolicy:
        automated:
          prune: true
          selfHeal: true
```

### List Generator (Multi-tenancy)

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: tenant-apps
  namespace: argocd
spec:
  generators:
    - list:
        elements:
          - tenant: team-a
            namespace: team-a-prod
            repoURL: https://github.com/team-a/apps.git
            quota:
              cpu: "10"
              memory: 20Gi
          - tenant: team-b
            namespace: team-b-prod
            repoURL: https://github.com/team-b/apps.git
            quota:
              cpu: "20"
              memory: 40Gi

  template:
    metadata:
      name: "{{tenant}}-app"
      labels:
        tenant: "{{tenant}}"
    spec:
      project: "{{tenant}}"
      source:
        repoURL: "{{repoURL}}"
        targetRevision: main
        path: production
      destination:
        server: https://kubernetes.default.svc
        namespace: "{{namespace}}"
      syncPolicy:
        automated:
          prune: true
          selfHeal: true
```

## ApplicationSet Patterns

### When to Use ApplicationSets

ApplicationSets automate creation and management of multiple Argo CD applications using generators. Use when:

- Deploying to multiple clusters with same configuration
- Managing multiple tenants or teams
- Discovering applications from Git repository structure
- Implementing environment promotion strategies

### Generator Selection Guide

| Generator         | Use Case                                    | Example                               |
| ----------------- | ------------------------------------------- | ------------------------------------- |
| **Cluster**       | Deploy same app to multiple clusters        | Multi-region deployment               |
| **Git Directory** | Generate apps from repo directory structure | Monorepo with app-per-directory       |
| **Git File**      | Generate apps from config files in Git      | JSON/YAML config per app              |
| **List**          | Static list of parameters                   | Tenant definitions                    |
| **Matrix**        | Combine multiple generators                 | Apps across clusters and environments |
| **Pull Request**  | Preview environments per PR                 | Ephemeral test environments           |
| **SCM Provider**  | Discover repos from GitHub/GitLab           | Org-wide app discovery                |

### Multi-Environment with Git Directory

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: multi-env-apps
  namespace: argocd
spec:
  generators:
    - matrix:
        generators:
          # First: discover apps from directory structure
          - git:
              repoURL: https://github.com/myorg/apps.git
              revision: HEAD
              directories:
                - path: apps/*
          # Second: apply to multiple environments
          - list:
              elements:
                - env: dev
                  cluster: https://dev-cluster.example.com
                  replicas: "1"
                - env: staging
                  cluster: https://staging-cluster.example.com
                  replicas: "2"
                - env: production
                  cluster: https://prod-cluster.example.com
                  replicas: "3"

  template:
    metadata:
      name: "{{path.basename}}-{{env}}"
      labels:
        app: "{{path.basename}}"
        env: "{{env}}"
    spec:
      project: default
      source:
        repoURL: https://github.com/myorg/apps.git
        targetRevision: HEAD
        path: "{{path}}"
        helm:
          parameters:
            - name: environment
              value: "{{env}}"
            - name: replicaCount
              value: "{{replicas}}"
      destination:
        server: "{{cluster}}"
        namespace: "{{path.basename}}-{{env}}"
      syncPolicy:
        automated:
          prune: true
          selfHeal: true
        syncOptions:
          - CreateNamespace=true
```

### Pull Request Preview Environments

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: pr-preview
  namespace: argocd
spec:
  generators:
    - pullRequest:
        github:
          owner: myorg
          repo: myapp
          tokenRef:
            secretName: github-token
            key: token
          labels:
            - preview
        requeueAfterSeconds: 60

  template:
    metadata:
      name: "myapp-pr-{{number}}"
      labels:
        preview: "true"
        pr: "{{number}}"
    spec:
      project: default
      source:
        repoURL: https://github.com/myorg/myapp.git
        targetRevision: "{{head_sha}}"
        path: k8s/overlays/preview
        kustomize:
          commonLabels:
            pr: "{{number}}"
          images:
            - name: myapp
              newTag: "pr-{{number}}"
      destination:
        server: https://kubernetes.default.svc
        namespace: "myapp-pr-{{number}}"
      syncPolicy:
        automated:
          prune: true
          selfHeal: true
        syncOptions:
          - CreateNamespace=true
```

### SCM Provider Discovery

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: org-repos
  namespace: argocd
spec:
  generators:
    - scmProvider:
        github:
          organization: myorg
          tokenRef:
            secretName: github-token
            key: token
        filters:
          - repositoryMatch: ".*-service$"
          - pathsExist: [k8s/production]

  template:
    metadata:
      name: "{{repository}}"
    spec:
      project: default
      source:
        repoURL: "{{url}}"
        targetRevision: main
        path: k8s/production
      destination:
        server: https://kubernetes.default.svc
        namespace: "{{repository}}"
      syncPolicy:
        automated:
          prune: true
          selfHeal: true
```

## Sync Strategies

### Strategy Selection Guide

| Strategy                    | Use Case                         | Risk   | Automation  |
| --------------------------- | -------------------------------- | ------ | ----------- |
| **Automated + SelfHeal**    | Non-prod environments            | Low    | Full        |
| **Automated (no SelfHeal)** | Staging with manual intervention | Medium | Partial     |
| **Manual**                  | Production deployments           | High   | None        |
| **Sync Windows**            | Business hours restrictions      | Medium | Scheduled   |
| **Progressive (Rollouts)**  | Gradual production rollout       | Low    | Conditional |

### Automated Sync with Conditions

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: conditional-sync
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/myorg/myrepo.git
    targetRevision: HEAD
    path: apps/myapp
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
      - PruneLast=true
      - PrunePropagationPolicy=foreground
      - RespectIgnoreDifferences=true
      - ApplyOutOfSyncOnly=true

    # Retry with exponential backoff
    retry:
      limit: 5
      backoff:
        duration: 5s
        factor: 2
        maxDuration: 3m

  # Ignore manual changes to specific fields
  ignoreDifferences:
    - group: apps
      kind: Deployment
      jsonPointers:
        - /spec/replicas
    - group: ""
      kind: Service
      jqPathExpressions:
        - .spec.ports[] | select(.nodePort != null) | .nodePort
```

### Sync Windows (Time-Based Deployment Control)

```yaml
apiVersion: argoproj.io/v1alpha1
kind: AppProject
metadata:
  name: production
  namespace: argocd
spec:
  description: Production project with sync windows

  sourceRepos:
    - "*"

  destinations:
    - namespace: "*"
      server: https://prod-cluster.example.com

  # Define sync windows
  syncWindows:
    # Allow syncs during business hours (Monday-Friday 9am-5pm UTC)
    - kind: allow
      schedule: "0 9 * * 1-5"
      duration: 8h
      applications:
        - "*"
      namespaces:
        - production-*
      clusters:
        - https://prod-cluster.example.com

    # Block syncs during peak traffic (daily 12pm-2pm UTC)
    - kind: deny
      schedule: "0 12 * * *"
      duration: 2h
      applications:
        - "*"

    # Emergency sync window (manual override required)
    - kind: allow
      schedule: "* * * * *"
      duration: 1h
      manualSync: true
      applications:
        - critical-app
```

### Selective Sync (Resource-Level Control)

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: selective-sync
  namespace: argocd
  annotations:
    # Sync only specific resource types
    argocd.argoproj.io/sync-options: Prune=false
spec:
  project: default
  source:
    repoURL: https://github.com/myorg/myrepo.git
    targetRevision: HEAD
    path: apps/myapp
  destination:
    server: https://kubernetes.default.svc
    namespace: myapp

  # Ignore specific resources from sync
  ignoreDifferences:
    - group: "*"
      kind: Secret
      name: external-secret
      jsonPointers:
        - /data

  syncPolicy:
    syncOptions:
      - CreateNamespace=true
      # Prune only specific resource types
      - PruneResourcesOnDeletion=true
```

### Blue-Green Sync Strategy

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: myapp-blue-green
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/myorg/myrepo.git
    targetRevision: HEAD
    path: apps/myapp
  destination:
    server: https://kubernetes.default.svc
    namespace: myapp

  syncPolicy:
    # Manual sync for production
    syncOptions:
      - CreateNamespace=true

    # Use sync waves for blue-green
    syncWaves:
      - wave: 0 # Deploy new version (green)
      - wave: 1 # Run smoke tests
      - wave: 2 # Switch traffic
      - wave: 3 # Remove old version (blue)
```

## Rollback Procedures

### Automatic Rollback Strategies

#### Application-Level Rollback

```bash
# View sync history
argocd app history myapp

# Rollback to previous sync
argocd app rollback myapp

# Rollback to specific revision
argocd app rollback myapp 5

# Rollback with prune
argocd app rollback myapp 5 --prune
```

#### Git-Based Rollback (Recommended)

```bash
# Revert Git commit
git revert HEAD
git push origin main

# Argo CD automatically syncs the revert
# This maintains full audit trail in Git
```

### Rollback with Argo Rollouts

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: myapp
  namespace: myapp
spec:
  replicas: 5
  strategy:
    blueGreen:
      activeService: myapp-active
      previewService: myapp-preview
      autoPromotionEnabled: false
      autoPromotionSeconds: 30
      scaleDownDelaySeconds: 300
      scaleDownDelayRevisionLimit: 1

      # Automatic rollback on metric failure
      antiAffinity:
        requiredDuringSchedulingIgnoredDuringExecution: {}

  revisionHistoryLimit: 5

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
          image: myapp:stable
---
# Manual rollback commands
# kubectl argo rollouts abort myapp
# kubectl argo rollouts undo myapp
# kubectl argo rollouts retry myapp
```

### Rollback on Health Check Failure

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: auto-rollback-app
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/myorg/myrepo.git
    targetRevision: HEAD
    path: apps/myapp
  destination:
    server: https://kubernetes.default.svc
    namespace: myapp

  syncPolicy:
    automated:
      prune: true
      selfHeal: false # Disable selfHeal for manual rollback control

    # Retry sync on failure
    retry:
      limit: 3
      backoff:
        duration: 10s
        factor: 2
        maxDuration: 1m

  # Custom health check that triggers rollback
  syncOptions:
    - Validate=true
    - FailOnSharedResource=false


# Use PreSync hook to backup current state
---
apiVersion: batch/v1
kind: Job
metadata:
  name: pre-sync-backup
  namespace: myapp
  annotations:
    argocd.argoproj.io/hook: PreSync
    argocd.argoproj.io/hook-delete-policy: BeforeHookCreation
spec:
  template:
    spec:
      containers:
        - name: backup
          image: kubectl:latest
          command:
            - /bin/sh
            - -c
            - |
              kubectl get all -n myapp -o yaml > /backup/previous-state.yaml
      restartPolicy: Never
---
# Use SyncFail hook for automatic rollback
apiVersion: batch/v1
kind: Job
metadata:
  name: rollback-on-fail
  namespace: myapp
  annotations:
    argocd.argoproj.io/hook: SyncFail
    argocd.argoproj.io/hook-delete-policy: BeforeHookCreation
spec:
  template:
    spec:
      serviceAccountName: argocd-rollback
      containers:
        - name: rollback
          image: argoproj/argocd:latest
          command:
            - /bin/sh
            - -c
            - |
              argocd app rollback myapp --auth-token $ARGOCD_TOKEN
      restartPolicy: Never
```

### Emergency Rollback Runbook

```bash
# 1. Check application status
argocd app get myapp
argocd app history myapp

# 2. Identify last known good revision
argocd app history myapp | grep Succeeded

# 3. Quick rollback to previous revision
argocd app rollback myapp

# 4. If rollback fails, force sync with replace
argocd app sync myapp --force --replace --prune

# 5. If still failing, revert Git and force sync
cd gitops-repo
git revert HEAD --no-commit
git commit -m "Emergency rollback"
git push origin main
argocd app sync myapp --force

# 6. Manual resource cleanup if needed
kubectl delete deployment myapp -n myapp
argocd app sync myapp --force

# 7. Verify health and sync status
argocd app wait myapp --health --timeout 300

# 8. Document incident
echo "Rollback completed at $(date)" >> /var/log/incidents/myapp-rollback.log
```

### Rollback Testing (Pre-Production)

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: rollback-test
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/myorg/myrepo.git
    targetRevision: HEAD
    path: apps/myapp
  destination:
    server: https://kubernetes.default.svc
    namespace: myapp-test

  syncPolicy:
    automated:
      prune: true
      selfHeal: true


# PostSync hook to test rollback capability
---
apiVersion: batch/v1
kind: Job
metadata:
  name: test-rollback
  namespace: myapp-test
  annotations:
    argocd.argoproj.io/hook: PostSync
    argocd.argoproj.io/hook-delete-policy: BeforeHookCreation
spec:
  template:
    spec:
      serviceAccountName: argocd-test
      containers:
        - name: test
          image: argoproj/argocd:latest
          command:
            - /bin/sh
            - -c
            - |
              # Test application health
              argocd app wait rollback-test --health --timeout 60

              # Perform rollback test
              argocd app rollback rollback-test

              # Verify rollback succeeded
              argocd app wait rollback-test --health --timeout 60

              # Re-sync to latest
              argocd app sync rollback-test
      restartPolicy: Never
```

## App of Apps Pattern

### Root Application (Bootstrap)

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: root-app
  namespace: argocd
  finalizers:
    - resources-finalizer.argocd.argoproj.io
spec:
  project: default

  source:
    repoURL: https://github.com/myorg/gitops.git
    targetRevision: HEAD
    path: argocd/applications
    directory:
      recurse: true

  destination:
    server: https://kubernetes.default.svc
    namespace: argocd

  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
```

### Infrastructure Apps

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: infrastructure
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/myorg/gitops.git
    targetRevision: HEAD
    path: argocd/infrastructure
    directory:
      recurse: true
  destination:
    server: https://kubernetes.default.svc
    namespace: argocd
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
```

### Layered App of Apps

```text
root-app
├── infrastructure (sync-wave: 0)
│   ├── cert-manager
│   ├── ingress-nginx
│   └── external-dns
├── platform (sync-wave: 1)
│   ├── monitoring
│   ├── logging
│   └── security
└── applications (sync-wave: 2)
    ├── app1
    ├── app2
    └── app3
```

## Sync Waves and Hooks

### Sync Waves for Ordering

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: myapp
  annotations:
    # Lower numbers sync first
    argocd.argoproj.io/sync-wave: "0"
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: myapp-config
  namespace: myapp
  annotations:
    argocd.argoproj.io/sync-wave: "1"
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
  namespace: myapp
  annotations:
    argocd.argoproj.io/sync-wave: "2"
---
apiVersion: v1
kind: Service
metadata:
  name: myapp
  namespace: myapp
  annotations:
    argocd.argoproj.io/sync-wave: "3"
```

### Resource Hooks

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: db-migration
  namespace: myapp
  annotations:
    # Hook types: PreSync, Sync, PostSync, SyncFail, Skip
    argocd.argoproj.io/hook: PreSync

    # Hook deletion policy
    argocd.argoproj.io/hook-delete-policy: HookSucceeded
    # Options: HookSucceeded, HookFailed, BeforeHookCreation

    # Sync wave for hooks
    argocd.argoproj.io/sync-wave: "1"
spec:
  template:
    spec:
      containers:
        - name: migrate
          image: myapp:migrations
          command: ["./migrate.sh"]
      restartPolicy: Never
  backoffLimit: 3
---
apiVersion: batch/v1
kind: Job
metadata:
  name: smoke-test
  namespace: myapp
  annotations:
    argocd.argoproj.io/hook: PostSync
    argocd.argoproj.io/hook-delete-policy: HookSucceeded
spec:
  template:
    spec:
      containers:
        - name: test
          image: myapp:tests
          command: ["./smoke-test.sh"]
      restartPolicy: Never
```

## Health Checks and Resource Customizations

### Custom Health Checks

```yaml
# ConfigMap in argocd namespace
apiVersion: v1
kind: ConfigMap
metadata:
  name: argocd-cm
  namespace: argocd
data:
  # Custom health check for CRDs
  resource.customizations.health.argoproj.io_Application: |
    hs = {}
    hs.status = "Progressing"
    hs.message = ""
    if obj.status ~= nil then
      if obj.status.health ~= nil then
        hs.status = obj.status.health.status
        if obj.status.health.message ~= nil then
          hs.message = obj.status.health.message
        end
      end
    end
    return hs

  # Custom health check for Certificates
  resource.customizations.health.cert-manager.io_Certificate: |
    hs = {}
    if obj.status ~= nil then
      if obj.status.conditions ~= nil then
        for i, condition in ipairs(obj.status.conditions) do
          if condition.type == "Ready" and condition.status == "False" then
            hs.status = "Degraded"
            hs.message = condition.message
            return hs
          end
          if condition.type == "Ready" and condition.status == "True" then
            hs.status = "Healthy"
            hs.message = condition.message
            return hs
          end
        end
      end
    end
    hs.status = "Progressing"
    hs.message = "Waiting for certificate"
    return hs
```

### Resource Ignoring

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: argocd-cm
  namespace: argocd
data:
  # Ignore differences in specific fields
  resource.customizations.ignoreDifferences.apps_Deployment: |
    jsonPointers:
      - /spec/replicas
    jqPathExpressions:
      - .spec.template.spec.containers[].env[] | select(.name == "DYNAMIC_VAR")

  # Ignore differences for all resources
  resource.customizations.ignoreDifferences.all: |
    managedFieldsManagers:
      - kube-controller-manager
```

### Known Types Configuration

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: argocd-cm
  namespace: argocd
data:
  # Resource tracking method
  application.resourceTrackingMethod: annotation+label

  # Exclude resources from sync
  resource.exclusions: |
    - apiGroups:
      - "*"
      kinds:
      - ProviderConfigUsage
      clusters:
      - "*"
```

## RBAC Configuration

### AppProject with RBAC

```yaml
apiVersion: argoproj.io/v1alpha1
kind: AppProject
metadata:
  name: team-a
  namespace: argocd
spec:
  description: Team A project

  # Source repositories
  sourceRepos:
    - "https://github.com/team-a/*"
    - "https://charts.team-a.com"

  # Destination clusters and namespaces
  destinations:
    - namespace: "team-a-*"
      server: https://kubernetes.default.svc
    - namespace: team-a-shared
      server: https://prod-cluster.example.com

  # Cluster resource whitelist (what CAN be deployed)
  clusterResourceWhitelist:
    - group: ""
      kind: Namespace
    - group: "rbac.authorization.k8s.io"
      kind: ClusterRole

  # Namespace resource blacklist (what CANNOT be deployed)
  namespaceResourceBlacklist:
    - group: ""
      kind: ResourceQuota
    - group: ""
      kind: LimitRange

  # Roles for project
  roles:
    - name: developer
      description: Developer role
      policies:
        - p, proj:team-a:developer, applications, get, team-a/*, allow
        - p, proj:team-a:developer, applications, sync, team-a/*, allow
      groups:
        - team-a-developers

    - name: admin
      description: Admin role
      policies:
        - p, proj:team-a:admin, applications, *, team-a/*, allow
        - p, proj:team-a:admin, repositories, *, team-a/*, allow
      groups:
        - team-a-admins

  # Orphaned resources monitoring
  orphanedResources:
    warn: true
    ignore:
      - group: ""
        kind: ConfigMap
        name: ignore-this-cm
```

### Global RBAC Policies

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: argocd-rbac-cm
  namespace: argocd
data:
  policy.default: role:readonly

  policy.csv: |
    # Format: p, subject, resource, action, object, effect

    # Grant admin role to group
    g, platform-team, role:admin

    # Custom role: app-deployer
    p, role:app-deployer, applications, get, */*, allow
    p, role:app-deployer, applications, sync, */*, allow
    p, role:app-deployer, applications, override, */*, allow
    p, role:app-deployer, repositories, get, *, allow

    # Grant app-deployer role to groups
    g, deployer-team, role:app-deployer

    # Specific permissions
    p, user:jane@example.com, applications, *, default/*, allow
    p, user:john@example.com, clusters, get, https://prod-cluster, allow

    # Project-scoped permissions
    p, role:project-viewer, applications, get, */*, allow
    p, role:project-viewer, applications, sync, */*, deny

  scopes: "[groups, email]"
```

## Sync Policies and Strategies

### Automated Sync

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: auto-sync-app
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/myorg/myrepo.git
    targetRevision: HEAD
    path: apps/myapp
  destination:
    server: https://kubernetes.default.svc
    namespace: myapp

  syncPolicy:
    automated:
      # Auto-sync when Git changes
      prune: true # Remove resources deleted from Git
      selfHeal: true # Revert manual changes to cluster
      allowEmpty: false # Prevent syncing if path is empty

    syncOptions:
      # Create namespace if missing
      - CreateNamespace=true

      # Validate resources before sync
      - Validate=true

      # Use server-side apply (kubectl apply --server-side)
      - ServerSideApply=true

      # Prune resources in foreground
      - PrunePropagationPolicy=foreground

      # Prune resources last (after new resources created)
      - PruneLast=true

      # Replace resource instead of applying
      - Replace=false

      # Respect ignore differences
      - RespectIgnoreDifferences=true

    # Retry policy
    retry:
      limit: 5
      backoff:
        duration: 5s
        factor: 2
        maxDuration: 3m
```

### Manual Sync with Selective Resources

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: manual-sync-app
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/myorg/myrepo.git
    targetRevision: HEAD
    path: apps/myapp
  destination:
    server: https://kubernetes.default.svc
    namespace: myapp

  # No automated sync policy - manual only
  syncPolicy:
    syncOptions:
      - CreateNamespace=true
      - PruneLast=true

  # Ignore differences for specific resources
  ignoreDifferences:
    - group: apps
      kind: Deployment
      jsonPointers:
        - /spec/replicas
    - group: ""
      kind: Service
      managedFieldsManagers:
        - kube-controller-manager
```

## Secret Management

### Sealed Secrets Integration

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: myapp-with-sealed-secrets
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/myorg/myrepo.git
    targetRevision: HEAD
    path: apps/myapp
    # Sealed secrets stored in Git
    # SealedSecret CRD automatically decrypted by controller
  destination:
    server: https://kubernetes.default.svc
    namespace: myapp
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

### External Secrets Operator

```yaml
# ExternalSecret in Git repo
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: myapp-secrets
  namespace: myapp
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: aws-secrets-manager
    kind: SecretStore
  target:
    name: myapp-secret
    creationPolicy: Owner
  data:
    - secretKey: db-password
      remoteRef:
        key: myapp/production/db
        property: password
```

### ArgoCD Vault Plugin

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: myapp-vault
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/myorg/myrepo.git
    targetRevision: HEAD
    path: apps/myapp
    plugin:
      name: argocd-vault-plugin
      env:
        - name: AVP_TYPE
          value: vault
        - name: AVP_AUTH_TYPE
          value: k8s
        - name: AVP_K8S_ROLE
          value: argocd
  destination:
    server: https://kubernetes.default.svc
    namespace: myapp
```

### Secrets in Helm Values (Encrypted)

```yaml
# Use SOPS or git-crypt to encrypt values files
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: myapp-helm-secrets
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/myorg/charts.git
    targetRevision: HEAD
    path: charts/myapp
    helm:
      valueFiles:
        - values.yaml
        # Encrypted with SOPS, decrypted by plugin
        - secrets://values-secrets.yaml
  destination:
    server: https://kubernetes.default.svc
    namespace: myapp
```

## Multi-tenancy Best Practices

### Tenant Isolation with AppProjects

```yaml
apiVersion: argoproj.io/v1alpha1
kind: AppProject
metadata:
  name: tenant-alpha
  namespace: argocd
spec:
  description: Tenant Alpha isolated project

  sourceRepos:
    - "https://github.com/tenant-alpha/*"

  destinations:
    - namespace: "tenant-alpha-*"
      server: https://kubernetes.default.svc

  clusterResourceWhitelist:
    - group: ""
      kind: Namespace

  namespaceResourceWhitelist:
    - group: "*"
      kind: "*"

  namespaceResourceBlacklist:
    - group: ""
      kind: ResourceQuota
    - group: ""
      kind: LimitRange
    - group: "rbac.authorization.k8s.io"
      kind: "*"

  roles:
    - name: tenant-admin
      policies:
        - p, proj:tenant-alpha:tenant-admin, applications, *, tenant-alpha/*, allow
      groups:
        - tenant-alpha-admins
```

### Resource Quotas per Tenant

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: tenant-alpha-quota
  namespace: tenant-alpha-prod
spec:
  hard:
    requests.cpu: "100"
    requests.memory: 200Gi
    limits.cpu: "200"
    limits.memory: 400Gi
    persistentvolumeclaims: "10"
    services.loadbalancers: "5"
```

### Network Policies for Tenant Isolation

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: tenant-isolation
  namespace: tenant-alpha-prod
spec:
  podSelector: {}
  policyTypes:
    - Ingress
    - Egress
  ingress:
    # Allow from same namespace
    - from:
        - podSelector: {}
    # Allow from ingress controller
    - from:
        - namespaceSelector:
            matchLabels:
              name: ingress-nginx
  egress:
    # Allow to same namespace
    - to:
        - podSelector: {}
    # Allow DNS
    - to:
        - namespaceSelector:
            matchLabels:
              name: kube-system
      ports:
        - protocol: UDP
          port: 53
```

## Progressive Delivery

### Argo Rollouts Integration

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: myapp-rollout
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/myorg/myrepo.git
    targetRevision: HEAD
    path: apps/myapp-rollout
  destination:
    server: https://kubernetes.default.svc
    namespace: myapp
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
---
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: myapp
  namespace: myapp
spec:
  replicas: 5
  strategy:
    canary:
      steps:
        - setWeight: 20
        - pause: { duration: 10m }
        - setWeight: 40
        - pause: { duration: 10m }
        - setWeight: 60
        - pause: { duration: 10m }
        - setWeight: 80
        - pause: { duration: 10m }
      analysis:
        templates:
          - templateName: success-rate
        startingStep: 2
      trafficRouting:
        istio:
          virtualService:
            name: myapp-vsvc
            routes:
              - primary
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
          image: myapp:stable
```

## Monitoring and Observability

### Prometheus Metrics

```yaml
apiVersion: v1
kind: Service
metadata:
  name: argocd-metrics
  namespace: argocd
  labels:
    app.kubernetes.io/name: argocd-metrics
spec:
  ports:
    - name: metrics
      port: 8082
      protocol: TCP
      targetPort: 8082
  selector:
    app.kubernetes.io/name: argocd-server
---
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: argocd-metrics
  namespace: argocd
spec:
  selector:
    matchLabels:
      app.kubernetes.io/name: argocd-metrics
  endpoints:
    - port: metrics
      interval: 30s
```

### Notification Templates

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: argocd-notifications-cm
  namespace: argocd
data:
  service.slack: |
    token: $slack-token

  template.app-deployed: |
    message: |
      Application {{.app.metadata.name}} is now running new version.
    slack:
      attachments: |
        [{
          "title": "{{ .app.metadata.name}}",
          "title_link":"{{.context.argocdUrl}}/applications/{{.app.metadata.name}}",
          "color": "#18be52",
          "fields": [
          {
            "title": "Sync Status",
            "value": "{{.app.status.sync.status}}",
            "short": true
          },
          {
            "title": "Repository",
            "value": "{{.app.spec.source.repoURL}}",
            "short": true
          }
          ]
        }]

  template.app-health-degraded: |
    message: |
      Application {{.app.metadata.name}} has degraded health.
    slack:
      attachments: |
        [{
          "title": "{{ .app.metadata.name}}",
          "title_link": "{{.context.argocdUrl}}/applications/{{.app.metadata.name}}",
          "color": "#f4c030",
          "fields": [
          {
            "title": "Health Status",
            "value": "{{.app.status.health.status}}",
            "short": true
          },
          {
            "title": "Message",
            "value": "{{.app.status.health.message}}",
            "short": false
          }
          ]
        }]

  trigger.on-deployed: |
    - when: app.status.operationState.phase in ['Succeeded']
      send: [app-deployed]

  trigger.on-health-degraded: |
    - when: app.status.health.status == 'Degraded'
      send: [app-health-degraded]
```

### Application Annotations for Notifications

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: myapp
  namespace: argocd
  annotations:
    notifications.argoproj.io/subscribe.on-deployed.slack: my-channel
    notifications.argoproj.io/subscribe.on-health-degraded.slack: alerts-channel
spec:
  project: default
  source:
    repoURL: https://github.com/myorg/myrepo.git
    targetRevision: HEAD
    path: apps/myapp
  destination:
    server: https://kubernetes.default.svc
    namespace: myapp
```

## CLI Operations

### Application Management

```bash
# Create application
argocd app create myapp \
  --repo https://github.com/myorg/myrepo.git \
  --path apps/myapp \
  --dest-server https://kubernetes.default.svc \
  --dest-namespace myapp \
  --sync-policy automated \
  --auto-prune \
  --self-heal

# List applications
argocd app list

# Get application details
argocd app get myapp

# Sync application
argocd app sync myapp

# Sync specific resources
argocd app sync myapp --resource apps:Deployment:myapp

# Rollback to previous version
argocd app rollback myapp

# Delete application
argocd app delete myapp

# Delete application and cascade delete resources
argocd app delete myapp --cascade

# Diff local changes
argocd app diff myapp

# Wait for sync to complete
argocd app wait myapp --health

# Set application parameters
argocd app set myapp --helm-set replicaCount=3
```

### Repository Management

```bash
# Add repository
argocd repo add https://github.com/myorg/myrepo.git \
  --username myuser \
  --password mytoken

# Add private repo with SSH
argocd repo add git@github.com:myorg/myrepo.git \
  --ssh-private-key-path ~/.ssh/id_rsa

# List repositories
argocd repo list

# Remove repository
argocd repo rm https://github.com/myorg/myrepo.git
```

### Cluster Management

```bash
# Add cluster
argocd cluster add my-cluster-context

# List clusters
argocd cluster list

# Remove cluster
argocd cluster rm https://my-cluster.example.com
```

### Project Management

```bash
# Create project
argocd proj create myproject \
  --description "My project" \
  --src https://github.com/myorg/* \
  --dest https://kubernetes.default.svc,myapp-*

# Add role to project
argocd proj role create myproject developer

# Add policy to role
argocd proj role add-policy myproject developer \
  --action get --permission allow \
  --object 'applications'

# List projects
argocd proj list

# Get project details
argocd proj get myproject
```

## Best Practices

### Repository Organization

1. **Separate config from code**: Keep application code and Kubernetes manifests in separate repositories
2. **Environment branches or directories**: Use either branch-per-environment or directory-per-environment strategy
3. **Immutable tags**: Use Git commit SHAs or immutable tags for production deployments
4. **PR-based deployments**: Require pull requests for changes to production manifests

### Application Design

1. **One app per microservice**: Create separate Argo CD applications for each microservice
2. **Use AppProjects**: Group related applications and enforce RBAC boundaries
3. **Implement sync waves**: Order resource creation with sync waves and hooks
4. **Health checks**: Define custom health checks for CRDs and custom resources
5. **Resource limits**: Always define resource requests and limits

### Security

1. **Least privilege RBAC**: Grant minimum necessary permissions per team/project
2. **Encrypted secrets**: Never commit plain-text secrets to Git
3. **Separate credentials**: Use different Git credentials for different environments
4. **Audit logging**: Enable and monitor Argo CD audit logs
5. **Network policies**: Restrict network access to Argo CD components

### Sync Strategies

1. **Automated sync for non-prod**: Enable auto-sync and self-heal for dev/staging
2. **Manual sync for production**: Require manual approval for production syncs
3. **Prune with caution**: Use prune: true carefully, consider PruneLast option
4. **Sync windows**: Configure sync windows to prevent deployments during business hours
5. **Progressive rollouts**: Use Argo Rollouts for canary and blue-green deployments

### Multi-cluster Management

1. **Cluster naming**: Use consistent naming conventions for clusters
2. **Cluster labels**: Label clusters by environment, region, purpose
3. **ApplicationSets**: Use ApplicationSets to manage apps across clusters
4. **Cluster secrets**: Rotate cluster credentials regularly
5. **Disaster recovery**: Maintain Argo CD configuration in Git for easy recovery

### Observability

1. **Metrics**: Export Prometheus metrics and create dashboards
2. **Notifications**: Configure notifications for sync failures and health degradation
3. **Logging**: Centralize Argo CD logs for troubleshooting
4. **Tracing**: Enable distributed tracing for complex deployments
5. **Alerts**: Set up alerts for out-of-sync applications

### Performance

1. **Resource limits**: Set appropriate resource limits for Argo CD components
2. **Sharding**: Use controller sharding for large-scale deployments (1000+ apps)
3. **Cache optimization**: Configure Redis for improved performance
4. **Webhook-based sync**: Use Git webhooks instead of polling for faster syncs
5. **Selective sync**: Use resource inclusions/exclusions to reduce sync scope

### Disaster Recovery

1. **Backup configuration**: Store all Argo CD configuration in Git
2. **Multiple Argo CD instances**: Run separate instances for different environments
3. **Export applications**: Regularly export application definitions
4. **Document procedures**: Maintain runbooks for disaster recovery
5. **Test recovery**: Periodically test disaster recovery procedures

## Troubleshooting

### Common Issues

#### Application stuck in progressing state

```bash
# Check application status
argocd app get myapp

# Check sync status and health
kubectl get application myapp -n argocd -o yaml

# Manual sync with replace
argocd app sync myapp --replace
```

#### Out of sync despite no changes

```bash
# Hard refresh
argocd app get myapp --hard-refresh

# Check for ignored differences
argocd app diff myapp
```

#### Permission denied errors

```bash
# Check project permissions
argocd proj get myproject

# Verify RBAC policies
kubectl get cm argocd-rbac-cm -n argocd -o yaml
```

#### Sync fails with validation errors

```bash
# Skip validation
argocd app sync myapp --validate=false

# Or add to syncOptions
syncOptions:
  - Validate=false
```

### Debug Commands

```bash
# Enable debug logging
argocd app sync myapp --loglevel debug

# Get application events
kubectl get events -n argocd --field-selector involvedObject.name=myapp

# Check controller logs
kubectl logs -n argocd deployment/argocd-application-controller

# Check server logs
kubectl logs -n argocd deployment/argocd-server

# Get resource details
argocd app resources myapp
```

## References

- [Argo CD Documentation](https://argo-cd.readthedocs.io/)
- [Argo CD Best Practices](https://argo-cd.readthedocs.io/en/stable/user-guide/best_practices/)
- [GitOps Principles](https://opengitops.dev/)
- [Argo Rollouts](https://argoproj.github.io/argo-rollouts/)
