---
name: gitops-patterns
description: Provides GitOps best practices for ArgoCD, Flux, Argo Rollouts, and progressive delivery strategies. Use when setting up GitOps workflows, configuring continuous delivery, managing Kubernetes deployments declaratively, or when user mentions 'gitops', 'argocd', 'flux', 'progressive delivery', 'reconciliation', 'argo rollouts', 'canary', 'sealed secrets'.
---

# GitOps Patterns

Best practices for operating infrastructure and applications through Git as the single source of truth. Covers ArgoCD, Flux, Argo Rollouts, environment promotion, secret management, and progressive delivery.

## GitOps Principles

GitOps extends Infrastructure as Code by adding a reconciliation loop that continuously ensures the live system matches the declared state in Git.

| Principle | Description | Implementation |
|-----------|-------------|----------------|
| Declarative | Entire system described declaratively | Kubernetes manifests, Helm charts, Kustomize overlays |
| Versioned and immutable | Desired state stored in Git | Git commits as audit trail, tags for releases |
| Pulled automatically | Software agents pull desired state | ArgoCD, Flux controllers watch Git repos |
| Continuously reconciled | Agents correct drift automatically | Reconciliation loop detects and fixes divergence |

| GitOps vs Traditional CI/CD | GitOps | Traditional CI/CD |
|-----------------------------|--------|-------------------|
| Deployment trigger | Git commit (pull-based) | Pipeline step (push-based) |
| Source of truth | Git repository | Pipeline state / manual |
| Drift handling | Auto-corrected | Undetected until next deploy |
| Rollback method | `git revert` | Re-run pipeline with old version |
| Audit trail | Git log | Pipeline logs (often ephemeral) |
| Credential exposure | Cluster-only (no CI secrets) | CI system has deploy credentials |

## Repository Structure

Separate application source code from deployment manifests. This is the most critical architectural decision in GitOps.

```
# Deployment repo (gitops-deploy) -- separate from application source
gitops-deploy/
  apps/
    backend/
      base/
        deployment.yaml
        service.yaml
        kustomization.yaml
      overlays/
        dev/
          kustomization.yaml       # image: backend:dev-abc1234
        staging/
          kustomization.yaml       # image: backend:staging-def5678
        prod/
          kustomization.yaml       # image: backend:v1.2.3
          patches/
            replicas.yaml
            hpa.yaml
    frontend/
      base/
      overlays/
  infrastructure/
    cert-manager/
    ingress-nginx/
    monitoring/
  clusters/
    dev/
      kustomization.yaml          # References apps/*/overlays/dev
    staging/
      kustomization.yaml
    prod/
      kustomization.yaml
```

| Structure Pattern | When to Use | Trade-offs |
|-------------------|------------|------------|
| Monorepo (app + deploy) | Small teams, single app | Simple but couples build and deploy |
| Separate repos | Multiple teams, compliance needs | Clean separation, more repos to manage |
| Branch-per-env | Simple promotion model | Risk of branch divergence, merge conflicts |
| Directory-per-env | Kustomize overlays | Recommended: explicit, reviewable, no branch drift |

## ArgoCD Application Manifest

ArgoCD watches Git repositories and synchronizes Kubernetes cluster state to match.

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: backend-prod
  namespace: argocd
  finalizers:
    - resources-finalizer.argocd.argoproj.io
spec:
  project: production

  source:
    repoURL: https://github.com/myorg/gitops-deploy.git
    targetRevision: main
    path: apps/backend/overlays/prod
    kustomize:
      images:
        - backend=ghcr.io/myorg/backend:v1.2.3

  destination:
    server: https://kubernetes.default.svc
    namespace: backend

  syncPolicy:
    automated:
      prune: true          # Delete resources removed from Git
      selfHeal: true       # Revert manual changes in cluster
      allowEmpty: false
    syncOptions:
      - CreateNamespace=true
      - PrunePropagationPolicy=foreground
      - PruneLast=true
    retry:
      limit: 3
      backoff:
        duration: 5s
        factor: 2
        maxDuration: 3m

  ignoreDifferences:
    - group: apps
      kind: Deployment
      jsonPointers:
        - /spec/replicas   # Ignore HPA-managed replica count
```

### ArgoCD ApplicationSet for Multi-Environment

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: backend
  namespace: argocd
spec:
  generators:
    - list:
        elements:
          - env: dev
            cluster: https://dev-cluster.example.com
            autoSync: true
          - env: staging
            cluster: https://staging-cluster.example.com
            autoSync: true
          - env: prod
            cluster: https://prod-cluster.example.com
            autoSync: false   # Prod requires manual sync
  template:
    metadata:
      name: 'backend-{{env}}'
    spec:
      project: '{{env}}'
      source:
        repoURL: https://github.com/myorg/gitops-deploy.git
        targetRevision: main
        path: 'apps/backend/overlays/{{env}}'
      destination:
        server: '{{cluster}}'
        namespace: backend
      syncPolicy:
        automated:
          prune: '{{autoSync}}'
          selfHeal: '{{autoSync}}'
```

## Flux Kustomization

Flux uses native Kubernetes custom resources and supports multi-tenancy out of the box.

```yaml
# Source: Git repository to watch
apiVersion: source.toolkit.fluxcd.io/v1
kind: GitRepository
metadata:
  name: gitops-deploy
  namespace: flux-system
spec:
  interval: 1m
  url: https://github.com/myorg/gitops-deploy.git
  ref:
    branch: main
  secretRef:
    name: gitops-deploy-auth

---
# Kustomization: what to deploy from that source
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: backend-prod
  namespace: flux-system
spec:
  interval: 5m
  retryInterval: 2m
  timeout: 5m
  sourceRef:
    kind: GitRepository
    name: gitops-deploy
  path: ./apps/backend/overlays/prod
  prune: true
  targetNamespace: backend
  healthChecks:
    - apiVersion: apps/v1
      kind: Deployment
      name: backend
      namespace: backend
  dependsOn:
    - name: infrastructure
  postBuild:
    substituteFrom:
      - kind: ConfigMap
        name: cluster-config

---
# Image automation: watch for new tags, update Git
apiVersion: image.toolkit.fluxcd.io/v1beta2
kind: ImagePolicy
metadata:
  name: backend
  namespace: flux-system
spec:
  imageRepositoryRef:
    name: backend
  policy:
    semver:
      range: '>=1.0.0'
```

## Progressive Delivery with Argo Rollouts

Argo Rollouts extends Kubernetes Deployments with canary releases, blue-green deployments, and automated analysis.

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: backend
spec:
  replicas: 10
  selector:
    matchLabels:
      app: backend
  template:
    metadata:
      labels:
        app: backend
    spec:
      containers:
        - name: backend
          image: ghcr.io/myorg/backend:v1.2.3
          ports:
            - containerPort: 8080
          resources:
            requests: { cpu: 100m, memory: 128Mi }
            limits: { cpu: 500m, memory: 512Mi }

  strategy:
    canary:
      canaryService: backend-canary
      stableService: backend-stable
      trafficRouting:
        istio:
          virtualServices:
            - name: backend-vsvc
              routes: [primary]
      steps:
        - setWeight: 5
        - pause: { duration: 2m }
        - analysis:
            templates:
              - templateName: success-rate
        - setWeight: 25
        - pause: { duration: 5m }
        - analysis:
            templates:
              - templateName: success-rate
        - setWeight: 50
        - pause: { duration: 5m }
        - setWeight: 100

---
# AnalysisTemplate -- automated success criteria
apiVersion: argoproj.io/v1alpha1
kind: AnalysisTemplate
metadata:
  name: success-rate
spec:
  args:
    - name: service-name
  metrics:
    - name: success-rate
      interval: 30s
      count: 5
      successCondition: result[0] >= 0.95
      failureLimit: 3
      provider:
        prometheus:
          address: http://prometheus.monitoring:9090
          query: |
            sum(rate(http_requests_total{service="{{args.service-name}}",status=~"2.."}[2m]))
            /
            sum(rate(http_requests_total{service="{{args.service-name}}"}[2m]))
    - name: p99-latency
      interval: 30s
      count: 5
      successCondition: result[0] <= 500
      failureLimit: 3
      provider:
        prometheus:
          address: http://prometheus.monitoring:9090
          query: |
            histogram_quantile(0.99,
              sum(rate(http_request_duration_ms_bucket{service="{{args.service-name}}"}[2m])) by (le)
            )
```

## Reconciliation Loop

The reconciliation loop is the core mechanism that makes GitOps self-healing.

```
         +----------------+
         |   Git Repo     |
         | (desired state)|
         +-------+--------+
                 |  poll / webhook
         +-------+--------+
         |  GitOps Agent   |
         | (ArgoCD / Flux) |
         +-------+--------+
                 |  compare desired vs actual
         +-------+--------+
         |   Diff Engine   |----> No diff? Sleep, poll again.
         +-------+--------+
                 |  diff detected
         +-------+--------+
         |  Apply Changes  |
         +-------+--------+
                 |
         +-------+--------+
         | Health Checks   |----> Unhealthy? Retry or alert.
         +-------+--------+
                 |  healthy
         +-------+--------+
         |  Mark Synced    |
         +----------------+
```

| Setting | ArgoCD | Flux |
|---------|--------|------|
| Poll interval | 3m default | `spec.interval` per resource |
| Webhook support | Yes (GitHub, GitLab) | Yes (Receiver CRD) |
| Self-heal | `selfHeal: true` | `spec.force: true` |
| Prune removed resources | `prune: true` | `spec.prune: true` |
| Retry on failure | `retry.limit` with backoff | `retryInterval` |

## Environment Promotion Strategies

| Strategy | Mechanism | Pros | Cons |
|----------|-----------|------|------|
| PR-based promotion | CI opens PR to update image tag | Full review, audit trail | Manual merge step |
| Automated promotion | Flux image automation or CI script | Fast, no manual gates | Needs strong automated tests |
| Git tag promotion | Tag commit for promotion | Clear versioning | Complex tag management |
| Branch promotion | Merge dev -> staging -> prod | Familiar Git workflow | Branch drift, merge conflicts |

### PR-Based Promotion Pipeline

```yaml
name: Promote
on:
  workflow_dispatch:
    inputs:
      image_tag:
        description: 'Image tag to promote'
        required: true
      target_env:
        type: choice
        options: [staging, prod]

jobs:
  promote:
    runs-on: ubuntu-latest
    permissions:
      contents: write
      pull-requests: write
    steps:
      - uses: actions/checkout@v4
        with:
          repository: myorg/gitops-deploy
          token: ${{ secrets.GITOPS_PAT }}

      - name: Update image tag
        run: |
          cd apps/backend/overlays/${{ inputs.target_env }}
          kustomize edit set image \
            backend=ghcr.io/myorg/backend:${{ inputs.image_tag }}

      - uses: peter-evans/create-pull-request@v6
        with:
          title: "promote: backend ${{ inputs.image_tag }} to ${{ inputs.target_env }}"
          branch: "promote/backend-${{ inputs.target_env }}-${{ inputs.image_tag }}"
          labels: promotion,${{ inputs.target_env }}
```

## Secret Management in GitOps

Secrets cannot be stored in plain text in Git. Multiple solutions exist with different trade-offs.

| Solution | Encryption | Where Decrypted | External Deps | Complexity |
|----------|-----------|-----------------|---------------|------------|
| Sealed Secrets | Asymmetric (cluster key) | In-cluster controller | None | Low |
| SOPS + age/KMS | Symmetric or KMS | CI or GitOps agent | KMS optional | Medium |
| External Secrets Operator | None (fetched at runtime) | In-cluster controller | Vault, AWS SM | Medium |
| Vault CSI Provider | None (injected at runtime) | Sidecar / CSI driver | HashiCorp Vault | High |

### Sealed Secrets

```bash
# Create a regular secret, then seal it for safe Git storage
kubectl create secret generic db-credentials \
  --from-literal=username=admin \
  --from-literal=password=s3cret \
  --dry-run=client -o yaml | \
  kubeseal --format yaml \
    --controller-name sealed-secrets \
    --controller-namespace flux-system \
    > apps/backend/overlays/prod/sealed-db-credentials.yaml
```

### External Secrets Operator

```yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: db-credentials
  namespace: backend
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: aws-secrets-manager
    kind: ClusterSecretStore
  target:
    name: db-credentials
    creationPolicy: Owner
  data:
    - secretKey: username
      remoteRef:
        key: prod/backend/db
        property: username
    - secretKey: password
      remoteRef:
        key: prod/backend/db
        property: password
```

### SOPS with Flux Decryption

```yaml
# Flux Kustomization with SOPS decryption
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: backend-prod
  namespace: flux-system
spec:
  interval: 5m
  sourceRef:
    kind: GitRepository
    name: gitops-deploy
  path: ./apps/backend/overlays/prod
  prune: true
  decryption:
    provider: sops
    secretRef:
      name: sops-age-key   # Secret containing the age private key
```

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| Storing plain-text secrets in Git | Credentials exposed in repo history forever | Use Sealed Secrets, SOPS, or External Secrets Operator |
| Push-based deploys alongside GitOps | CI `kubectl apply` bypasses reconciliation | Remove all `kubectl apply` from CI; only update Git |
| Single repo for app code and manifests | Every code commit triggers deploy; noisy history | Separate application and deployment repositories |
| Branch-per-environment | Branches diverge, merge conflicts, unclear state | Use directory-per-environment with Kustomize overlays |
| Disabling self-heal / auto-prune | Manual changes accumulate, cluster drifts from Git | Enable `selfHeal: true` and `prune: true` |
| No health checks in sync policy | Sync marked complete before app is actually ready | Add health checks for Deployments, StatefulSets, Jobs |
| Manual `kubectl` in GitOps clusters | Reverted on next reconciliation or causes drift | All changes through Git PRs; restrict kubectl to read-only |
| Deploying directly to prod | No validation in lower environments | Require promotion path: dev -> staging -> prod |
| No RBAC on GitOps tool | Any developer can sync any app to any namespace | Use ArgoCD AppProjects or Flux multi-tenancy |
| Image tag `latest` in manifests | Non-deterministic deploys, no rollback possible | Use immutable tags (SHA, semver, build ID) |
| No notification on sync failure | Failed deployments go unnoticed for hours | Configure alerts to Slack, PagerDuty, or email |
| Reconciliation interval too long | Drift persists, delayed deployments | Set interval to 1-5 minutes; use webhooks for instant sync |

## GitOps Readiness Checklist

- [ ] All application manifests stored in a Git repository (not applied manually)
- [ ] Deployment repository is separate from application source code
- [ ] Directory-per-environment structure with Kustomize overlays or Helm values
- [ ] ArgoCD or Flux installed and configured to watch the deployment repo
- [ ] Auto-sync enabled with self-heal and prune for all environments
- [ ] Health checks configured for all synced applications
- [ ] Secret management solution deployed (Sealed Secrets, SOPS, or External Secrets)
- [ ] No plain-text secrets committed to any Git repository
- [ ] Environment promotion workflow defined (PR-based or automated)
- [ ] Image tags are immutable (semver, SHA, or build ID -- never `latest`)
- [ ] RBAC configured: AppProjects (ArgoCD) or namespaced Kustomizations (Flux)
- [ ] Notifications configured for sync failures and degraded health
- [ ] `kubectl` write access restricted in GitOps-managed clusters
- [ ] Rollback tested: `git revert` triggers successful rollback deployment
- [ ] Disaster recovery plan: GitOps agent recovery, state rebuild from Git
- [ ] Progressive delivery configured for production (canary or blue-green)
