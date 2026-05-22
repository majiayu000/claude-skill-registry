---
name: kubernetes-gitops
description: |
  GitOps workflows and CI/CD pipeline integration for Kubernetes and OpenShift. Use this skill when:
  (1) Setting up ArgoCD or Flux for GitOps deployment
  (2) Creating CI/CD pipelines for K8s workloads (GitHub Actions, GitLab CI, Tekton)
  (3) Implementing progressive delivery (Canary, Blue-Green, A/B testing)
  (4) Configuring Kustomize overlays for multi-environment deployments
  (5) Creating Helm charts or managing Helm releases
  (6) Setting up image automation and promotion workflows
  (7) Implementing policy-as-code (Kyverno, OPA Gatekeeper)
  (8) Secret management in GitOps (Sealed Secrets, External Secrets, SOPS)
  (9) Multi-cluster GitOps configurations
  (10) OpenShift Pipelines (Tekton) and GitOps Operator setup
metadata:
  author: cluster-skills
  version: "1.0.0"
---

# Kubernetes / OpenShift GitOps & CI/CD

GitOps workflows, CI/CD integration, and progressive delivery patterns for production clusters.

## Current Versions (January 2026)

| Tool | Version | Documentation |
|------|---------|---------------|
| **ArgoCD** | v2.13.x | https://argo-cd.readthedocs.io/ |
| **Flux** | v2.4.x | https://fluxcd.io/flux/ |
| **Kustomize** | v5.5.x | https://kustomize.io/ |
| **Helm** | v3.16.x | https://helm.sh/docs/ |
| **Tekton** | v0.65.x | https://tekton.dev/ |

## Command Usage Convention

**IMPORTANT**: This skill uses `kubectl` as the primary command. When working with:
- **OpenShift/ARO clusters**: Replace `kubectl` with `oc`
- **Standard Kubernetes (AKS, EKS, GKE)**: Use `kubectl` as shown

## GitOps Principles

1. **Declarative**: Entire system described declaratively in Git
2. **Versioned**: Git as single source of truth with history
3. **Automated**: Changes automatically applied to cluster
4. **Auditable**: All changes tracked via Git commits

## ArgoCD Setup (v2.13.x)

### Installation

```bash
# Create namespace
kubectl create namespace argocd

# Install ArgoCD (Non-HA for dev)
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# HA Installation (production)
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/ha/install.yaml

# Wait for pods
kubectl wait --for=condition=Ready pods --all -n argocd --timeout=300s

# Get initial admin password
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d

# Install CLI
brew install argocd

# Access UI
kubectl port-forward svc/argocd-server -n argocd 8080:443
```

### ArgoCD Application

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: ${APP_NAME}
  namespace: argocd
  finalizers:
    - resources-finalizer.argocd.argoproj.io
spec:
  project: default
  source:
    repoURL: ${GIT_REPO_URL}
    targetRevision: ${BRANCH:-main}
    path: ${MANIFEST_PATH}
    # For Kustomize
    kustomize:
      images:
        - ${IMAGE_NAME}=${NEW_IMAGE}:${TAG}
    # For Helm (uncomment)
    # helm:
    #   releaseName: ${RELEASE_NAME}
    #   valueFiles:
    #     - values-${ENV}.yaml
  destination:
    server: https://kubernetes.default.svc
    namespace: ${NAMESPACE}
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
      allowEmpty: false
    syncOptions:
      - CreateNamespace=true
      - PrunePropagationPolicy=foreground
    retry:
      limit: 5
      backoff:
        duration: 5s
        factor: 2
        maxDuration: 3m
```

### ArgoCD ApplicationSet (Multi-Environment)

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: ${APP_NAME}-appset
  namespace: argocd
spec:
  generators:
    - list:
        elements:
          - env: dev
            namespace: ${APP_NAME}-dev
            cluster: https://kubernetes.default.svc
          - env: staging
            namespace: ${APP_NAME}-staging
            cluster: https://kubernetes.default.svc
          - env: prod
            namespace: ${APP_NAME}-prod
            cluster: https://prod-cluster.example.com
  template:
    metadata:
      name: '${APP_NAME}-{{env}}'
    spec:
      project: default
      source:
        repoURL: ${GIT_REPO_URL}
        targetRevision: main
        path: 'overlays/{{env}}'
      destination:
        server: '{{cluster}}'
        namespace: '{{namespace}}'
      syncPolicy:
        automated:
          prune: true
          selfHeal: true
```

### ArgoCD Project (RBAC)

```yaml
apiVersion: argoproj.io/v1alpha1
kind: AppProject
metadata:
  name: ${PROJECT_NAME}
  namespace: argocd
spec:
  description: ${DESCRIPTION}
  sourceRepos:
    - ${GIT_REPO_URL}
  destinations:
    - namespace: '${NAMESPACE_PREFIX}-*'
      server: https://kubernetes.default.svc
  clusterResourceWhitelist:
    - group: ''
      kind: Namespace
  roles:
    - name: developer
      description: Developer access
      policies:
        - p, proj:${PROJECT_NAME}:developer, applications, get, ${PROJECT_NAME}/*, allow
        - p, proj:${PROJECT_NAME}:developer, applications, sync, ${PROJECT_NAME}/*, allow
```

## Flux CD Setup (v2.4.x)

### Installation

```bash
# Install CLI
brew install fluxcd/tap/flux

# Check prerequisites
flux check --pre

# Bootstrap with GitHub
flux bootstrap github \
  --owner=${GITHUB_ORG} \
  --repository=${REPO_NAME} \
  --branch=main \
  --path=clusters/${CLUSTER_NAME} \
  --personal

# Check status
flux check
flux get all -A
```

### Flux GitRepository

```yaml
apiVersion: source.toolkit.fluxcd.io/v1
kind: GitRepository
metadata:
  name: ${APP_NAME}
  namespace: flux-system
spec:
  interval: 1m
  url: ${GIT_REPO_URL}
  ref:
    branch: main
  secretRef:
    name: ${GIT_SECRET}
```

### Flux Kustomization

```yaml
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: ${APP_NAME}
  namespace: flux-system
spec:
  interval: 10m
  targetNamespace: ${NAMESPACE}
  sourceRef:
    kind: GitRepository
    name: ${APP_NAME}
  path: ./overlays/${ENV}
  prune: true
  healthChecks:
    - apiVersion: apps/v1
      kind: Deployment
      name: ${APP_NAME}
      namespace: ${NAMESPACE}
  timeout: 2m
```

### Flux Image Automation

```yaml
apiVersion: image.toolkit.fluxcd.io/v1beta2
kind: ImageRepository
metadata:
  name: ${APP_NAME}
  namespace: flux-system
spec:
  image: ${REGISTRY}/${IMAGE_NAME}
  interval: 1m
---
apiVersion: image.toolkit.fluxcd.io/v1beta2
kind: ImagePolicy
metadata:
  name: ${APP_NAME}
  namespace: flux-system
spec:
  imageRepositoryRef:
    name: ${APP_NAME}
  policy:
    semver:
      range: '>=1.0.0'
---
apiVersion: image.toolkit.fluxcd.io/v1beta1
kind: ImageUpdateAutomation
metadata:
  name: ${APP_NAME}
  namespace: flux-system
spec:
  interval: 1m
  sourceRef:
    kind: GitRepository
    name: ${APP_NAME}
  git:
    commit:
      author:
        email: flux@example.com
        name: Flux
      messageTemplate: 'chore: update image to {{.NewTag}}'
    push:
      branch: main
  update:
    path: ./overlays
    strategy: Setters
```

## Kustomize (v5.5.x)

### Directory Structure

```
app/
├── base/
│   ├── kustomization.yaml
│   ├── deployment.yaml
│   ├── service.yaml
│   └── configmap.yaml
└── overlays/
    ├── dev/
    │   └── kustomization.yaml
    ├── staging/
    │   └── kustomization.yaml
    └── prod/
        └── kustomization.yaml
```

### Base kustomization.yaml

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
  - deployment.yaml
  - service.yaml
  - configmap.yaml

commonLabels:
  app.kubernetes.io/name: ${APP_NAME}
  app.kubernetes.io/managed-by: kustomize

images:
  - name: ${APP_NAME}
    newName: ${REGISTRY}/${IMAGE_NAME}
    newTag: latest
```

### Production Overlay

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

namespace: ${APP_NAME}-prod

resources:
  - ../../base
  - hpa.yaml
  - pdb.yaml
  - networkpolicy.yaml

namePrefix: prod-

commonLabels:
  environment: production

images:
  - name: ${APP_NAME}
    newName: ${REGISTRY}/${IMAGE_NAME}
    newTag: v1.2.3

replicas:
  - name: ${APP_NAME}
    count: 3

patches:
  - path: patches/resources.yaml
  - target:
      kind: Deployment
      name: ${APP_NAME}
    patch: |-
      - op: add
        path: /spec/template/spec/affinity
        value:
          podAntiAffinity:
            requiredDuringSchedulingIgnoredDuringExecution:
              - labelSelector:
                  matchLabels:
                    app.kubernetes.io/name: ${APP_NAME}
                topologyKey: kubernetes.io/hostname

configMapGenerator:
  - name: ${APP_NAME}-config
    behavior: merge
    literals:
      - LOG_LEVEL=warn
```

## Helm (v3.16.x)

### Chart Structure

```
${CHART_NAME}/
├── Chart.yaml
├── values.yaml
├── values-dev.yaml
├── values-prod.yaml
├── templates/
│   ├── _helpers.tpl
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   └── NOTES.txt
└── charts/
```

### Chart.yaml

```yaml
apiVersion: v2
name: ${CHART_NAME}
description: ${DESCRIPTION}
type: application
version: 0.1.0
appVersion: "1.0.0"
maintainers:
  - name: ${MAINTAINER}
    email: ${EMAIL}
```

### Helm Commands

```bash
# Add repositories
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update

# Install/Upgrade
helm upgrade --install ${RELEASE} ${CHART} \
  --namespace ${NAMESPACE} --create-namespace \
  -f values-${ENV}.yaml \
  --set image.tag=${TAG} \
  --wait --timeout 10m

# List releases
helm list -A

# Rollback
helm rollback ${RELEASE} ${REVISION} -n ${NAMESPACE}
```

## GitHub Actions CI/CD

```yaml
name: Deploy to Kubernetes

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    outputs:
      image_tag: ${{ steps.meta.outputs.tags }}
    steps:
      - uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Login to Container Registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=sha,prefix=
            type=ref,event=branch
            type=semver,pattern={{version}}

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: ${{ github.event_name != 'pull_request' }}
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  deploy:
    needs: build
    if: github.event_name != 'pull_request'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Kustomize
        uses: imranismail/setup-kustomize@v2

      - name: Update image tag
        run: |
          cd overlays/prod
          kustomize edit set image app=${{ needs.build.outputs.image_tag }}

      - name: Commit and push
        run: |
          git config user.name "GitHub Actions"
          git config user.email "actions@github.com"
          git add -A
          git commit -m "chore: update image to ${{ needs.build.outputs.image_tag }}"
          git push
```

## Progressive Delivery

### Argo Rollouts - Canary

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: ${APP_NAME}
spec:
  replicas: 5
  strategy:
    canary:
      canaryService: ${APP_NAME}-canary
      stableService: ${APP_NAME}-stable
      steps:
        - setWeight: 10
        - pause: {duration: 5m}
        - setWeight: 30
        - pause: {duration: 5m}
        - setWeight: 50
        - pause: {duration: 5m}
      analysis:
        templates:
          - templateName: success-rate
        startingStep: 2
  selector:
    matchLabels:
      app: ${APP_NAME}
  template:
    # Pod template here
```

### Argo Rollouts - Blue-Green

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: ${APP_NAME}
spec:
  replicas: 3
  strategy:
    blueGreen:
      activeService: ${APP_NAME}-active
      previewService: ${APP_NAME}-preview
      autoPromotionEnabled: false
      prePromotionAnalysis:
        templates:
          - templateName: smoke-tests
  selector:
    matchLabels:
      app: ${APP_NAME}
  template:
    # Pod template here
```

## OpenShift GitOps

### Install OpenShift GitOps Operator

```bash
# Via CLI
oc apply -f - <<EOF
apiVersion: operators.coreos.com/v1alpha1
kind: Subscription
metadata:
  name: openshift-gitops-operator
  namespace: openshift-operators
spec:
  channel: latest
  installPlanApproval: Automatic
  name: openshift-gitops-operator
  source: redhat-operators
  sourceNamespace: openshift-marketplace
EOF

# Wait for ArgoCD instance
oc wait --for=condition=Available deployment/openshift-gitops-server -n openshift-gitops --timeout=300s

# Get ArgoCD admin password
oc extract secret/openshift-gitops-cluster -n openshift-gitops --to=-

# Access ArgoCD route
oc get route openshift-gitops-server -n openshift-gitops
```

## Secret Management in GitOps

### Sealed Secrets

```bash
# Create sealed secret
kubeseal --format=yaml < secret.yaml > sealed-secret.yaml

# Commit sealed-secret.yaml to Git (safe!)
git add sealed-secret.yaml
git commit -m "Add sealed secret"
git push
```

### External Secrets with GitOps

```yaml
# ExternalSecret in Git repository
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: app-secrets
  namespace: ${NAMESPACE}
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: vault-backend
    kind: ClusterSecretStore
  target:
    name: app-secrets
  data:
    - secretKey: DATABASE_URL
      remoteRef:
        key: apps/${APP_NAME}
        property: database_url
```
