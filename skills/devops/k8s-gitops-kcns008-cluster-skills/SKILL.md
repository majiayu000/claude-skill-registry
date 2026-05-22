---
name: k8s-gitops
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
---

# Kubernetes / OpenShift GitOps & CI/CD

## Command Usage Convention

**IMPORTANT**: This skill uses `kubectl` as the primary command in all examples. When working with:
- **OpenShift/ARO clusters**: Replace all `kubectl` commands with `oc`
- **Standard Kubernetes clusters (AKS, EKS, GKE, etc.)**: Use `kubectl` as shown

The agent will automatically detect the cluster type and use the appropriate command.

GitOps workflows, CI/CD integration, and progressive delivery patterns for cluster-code managed clusters.

## GitOps Principles

1. **Declarative**: Entire system described declaratively in Git
2. **Versioned**: Git as single source of truth with history
3. **Automated**: Changes automatically applied to cluster
4. **Auditable**: All changes tracked via Git commits

## ArgoCD Setup

### Current Versions & Documentation
- **ArgoCD**: v2.13.x (Latest stable as of January 2026)
- **CLI Install**: `brew install argocd` or `curl -sSL -o argocd-linux-amd64 https://github.com/argoproj/argo-cd/releases/latest/download/argocd-linux-amd64`
- **Docs**: https://argo-cd.readthedocs.io/
- **Release Notes**: https://github.com/argoproj/argo-cd/releases

### Installation

```bash
# Create namespace
kubectl create namespace argocd

# Install ArgoCD (v2.13.x - HA for production, non-HA for dev)
# Non-HA (development/testing)
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# HA Installation (production recommended)
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/ha/install.yaml

# Wait for pods
kubectl wait --for=condition=Ready pods --all -n argocd --timeout=300s

# Get initial admin password (ArgoCD 2.x+)
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d

# Install ArgoCD CLI (latest)
# macOS
brew install argocd
# Linux
curl -sSL -o /usr/local/bin/argocd https://github.com/argoproj/argo-cd/releases/latest/download/argocd-linux-amd64
chmod +x /usr/local/bin/argocd

# Login to ArgoCD
argocd login localhost:8080 --username admin --password $(kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d)

# Access UI (port-forward for testing)
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
      namePrefix: ${PREFIX:-}
      nameSuffix: ${SUFFIX:-}
      images:
        - ${IMAGE_NAME}=${NEW_IMAGE}:${TAG}
    # For Helm
    # helm:
    #   releaseName: ${RELEASE_NAME}
    #   valueFiles:
    #     - values-${ENV}.yaml
    #   parameters:
    #     - name: image.tag
    #       value: ${TAG}
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
      - PruneLast=true
    retry:
      limit: 5
      backoff:
        duration: 5s
        factor: 2
        maxDuration: 3m
  revisionHistoryLimit: 10
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
    - 'https://github.com/org/*'
  destinations:
    - namespace: '${NAMESPACE_PREFIX}-*'
      server: https://kubernetes.default.svc
    - namespace: '*'
      server: https://prod-cluster.example.com
  clusterResourceWhitelist:
    - group: ''
      kind: Namespace
  namespaceResourceBlacklist:
    - group: ''
      kind: ResourceQuota
    - group: ''
      kind: LimitRange
  roles:
    - name: developer
      description: Developer access
      policies:
        - p, proj:${PROJECT_NAME}:developer, applications, get, ${PROJECT_NAME}/*, allow
        - p, proj:${PROJECT_NAME}:developer, applications, sync, ${PROJECT_NAME}/*, allow
      groups:
        - ${DEV_GROUP}
```

## Flux CD Setup

### Current Versions & Documentation
- **Flux**: v2.4.x (Latest stable as of January 2026)
- **CLI Install**: `brew install fluxcd/tap/flux` or `curl -s https://fluxcd.io/install.sh | sudo bash`
- **Docs**: https://fluxcd.io/flux/
- **Release Notes**: https://github.com/fluxcd/flux2/releases

### Installation

```bash
# Install Flux CLI (v2.4.x+)
# macOS
brew install fluxcd/tap/flux

# Linux
curl -s https://fluxcd.io/install.sh | sudo bash

# Verify installation
flux --version

# Check prerequisites
flux check --pre

# Bootstrap with GitHub
flux bootstrap github \
  --owner=${GITHUB_ORG} \
  --repository=${REPO_NAME} \
  --branch=main \
  --path=clusters/${CLUSTER_NAME} \
  --personal

# Bootstrap with GitLab
flux bootstrap gitlab \
  --owner=${GITLAB_GROUP} \
  --repository=${REPO_NAME} \
  --branch=main \
  --path=clusters/${CLUSTER_NAME} \
  --personal

# Check Flux status
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
  postBuild:
    substitute:
      ENV: ${ENV}
      IMAGE_TAG: ${TAG}
```

### Flux Image Automation

```yaml
# Image Repository (watch for new tags)
apiVersion: image.toolkit.fluxcd.io/v1beta2
kind: ImageRepository
metadata:
  name: ${APP_NAME}
  namespace: flux-system
spec:
  image: ${REGISTRY}/${IMAGE_NAME}
  interval: 1m
  secretRef:
    name: ${REGISTRY_SECRET}
---
# Image Policy (select which tags to use)
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
    # Or use timestamp-based
    # alphabetical:
    #   order: asc
    # numerical:
    #   order: asc
---
# Image Update Automation
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
    checkout:
      ref:
        branch: main
    commit:
      author:
        email: flux@example.com
        name: Flux
      messageTemplate: 'chore: update {{.AutomationObject.Name}} to {{.NewTag}}'
    push:
      branch: main
  update:
    path: ./overlays
    strategy: Setters
```

## Kustomize

### Current Versions & Documentation
- **Kustomize**: v5.5.x (Latest stable as of January 2026)
- **Built into kubectl**: `kubectl kustomize` (may lag behind standalone)
- **Standalone Install**: `brew install kustomize` or from GitHub releases
- **Docs**: https://kustomize.io/
- **Catalog**: https://kubectl.docs.kubernetes.io/references/kustomize/

### Kustomize CLI Quick Reference

```bash
# Install standalone Kustomize (v5.5.x+)
brew install kustomize
# OR
curl -s "https://raw.githubusercontent.com/kubernetes-sigs/kustomize/master/hack/install_kustomize.sh" | bash

# Build and preview
kustomize build overlays/prod

# Apply directly
kubectl apply -k overlays/prod
# OR
kustomize build overlays/prod | kubectl apply -f -

# Edit image tags
kustomize edit set image myapp=registry/myapp:v2.0.0

# Set namespace
kustomize edit set namespace production

# Add resources
kustomize edit add resource new-deployment.yaml

# Kustomize v5.x features
# - Improved replacements (replacing vars)
# - Better OpenAPI schema support
# - Enhanced component support
```

### Base Structure

```
app/
├── base/
│   ├── kustomization.yaml
│   ├── deployment.yaml
│   ├── service.yaml
│   └── configmap.yaml
├── components/         # Reusable Kustomize components (v4.1+)
│   ├── monitoring/
│   │   └── kustomization.yaml
│   └── security/
│       └── kustomization.yaml
└── overlays/
    ├── dev/
    │   ├── kustomization.yaml
    │   └── patches/
    ├── staging/
    │   ├── kustomization.yaml
    │   └── patches/
    └── prod/
        ├── kustomization.yaml
        └── patches/
```

### Base kustomization.yaml

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
metadata:
  name: ${APP_NAME}

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

### Overlay kustomization.yaml (Production)

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
    newTag: v1.2.3  # Pin to specific version

replicas:
  - name: ${APP_NAME}
    count: 3

patches:
  - path: patches/resources.yaml
  - path: patches/probes.yaml
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
      - ENABLE_DEBUG=false

secretGenerator:
  - name: ${APP_NAME}-secrets
    type: Opaque
    files:
      - secrets/api-key.txt
    options:
      disableNameSuffixHash: true
```

### Resource Patch Example

```yaml
# patches/resources.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ${APP_NAME}
spec:
  template:
    spec:
      containers:
        - name: ${APP_NAME}
          resources:
            requests:
              cpu: 500m
              memory: 512Mi
            limits:
              cpu: 2000m
              memory: 2Gi
```

## Helm

### Current Versions & Documentation
- **Helm**: v3.16.x (Latest stable as of January 2026)
- **CLI Install**: `brew install helm` or `curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash`
- **Docs**: https://helm.sh/docs/
- **Hub**: https://artifacthub.io/

### Helm CLI Quick Reference

```bash
# Install Helm (v3.16.x+)
brew install helm
# OR
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# Add common repositories
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo add jetstack https://charts.jetstack.io
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

# Search charts
helm search repo nginx
helm search hub prometheus

# Install/Upgrade with values
helm upgrade --install ${RELEASE} ${CHART} \
  --namespace ${NAMESPACE} --create-namespace \
  -f values-${ENV}.yaml \
  --set image.tag=${TAG} \
  --wait --timeout 10m

# OCI registry support (Helm 3.8+)
helm pull oci://registry.example.com/charts/myapp --version 1.0.0
helm push myapp-1.0.0.tgz oci://registry.example.com/charts
```

### Chart Structure

```
${CHART_NAME}/
├── Chart.yaml
├── Chart.lock          # Dependency lock file (Helm 3.x+)
├── values.yaml
├── values.schema.json  # JSON Schema for values validation
├── values-dev.yaml
├── values-prod.yaml
├── templates/
│   ├── _helpers.tpl
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   ├── configmap.yaml
│   ├── secret.yaml
│   ├── hpa.yaml
│   ├── pdb.yaml
│   ├── serviceaccount.yaml
│   ├── servicemonitor.yaml  # For Prometheus Operator
│   └── NOTES.txt
├── charts/             # Dependencies
└── crds/               # Custom Resource Definitions
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
dependencies:
  - name: postgresql
    version: "12.x.x"
    repository: "https://charts.bitnami.com/bitnami"
    condition: postgresql.enabled
```

### values.yaml

```yaml
# Default values
replicaCount: 1

image:
  repository: ${REGISTRY}/${IMAGE_NAME}
  tag: "latest"
  pullPolicy: IfNotPresent

nameOverride: ""
fullnameOverride: ""

serviceAccount:
  create: true
  name: ""
  annotations: {}

service:
  type: ClusterIP
  port: 80
  targetPort: 8080

ingress:
  enabled: false
  className: nginx
  annotations: {}
  hosts:
    - host: chart-example.local
      paths:
        - path: /
          pathType: Prefix
  tls: []

resources:
  requests:
    cpu: 100m
    memory: 128Mi
  limits:
    cpu: 500m
    memory: 512Mi

autoscaling:
  enabled: false
  minReplicas: 2
  maxReplicas: 10
  targetCPUUtilizationPercentage: 70

nodeSelector: {}
tolerations: []
affinity: {}

# Application-specific
config:
  logLevel: info
  environment: development

# External services
postgresql:
  enabled: false
  auth:
    database: app
    username: app
```

### Template Example (deployment.yaml)

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "${CHART_NAME}.fullname" . }}
  labels:
    {{- include "${CHART_NAME}.labels" . | nindent 4 }}
spec:
  {{- if not .Values.autoscaling.enabled }}
  replicas: {{ .Values.replicaCount }}
  {{- end }}
  selector:
    matchLabels:
      {{- include "${CHART_NAME}.selectorLabels" . | nindent 6 }}
  template:
    metadata:
      annotations:
        checksum/config: {{ include (print $.Template.BasePath "/configmap.yaml") . | sha256sum }}
      labels:
        {{- include "${CHART_NAME}.selectorLabels" . | nindent 8 }}
    spec:
      serviceAccountName: {{ include "${CHART_NAME}.serviceAccountName" . }}
      securityContext:
        runAsNonRoot: true
        seccompProfile:
          type: RuntimeDefault
      containers:
        - name: {{ .Chart.Name }}
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag | default .Chart.AppVersion }}"
          imagePullPolicy: {{ .Values.image.pullPolicy }}
          securityContext:
            allowPrivilegeEscalation: false
            readOnlyRootFilesystem: true
            capabilities:
              drop:
                - ALL
          ports:
            - name: http
              containerPort: {{ .Values.service.targetPort }}
              protocol: TCP
          env:
            - name: LOG_LEVEL
              value: {{ .Values.config.logLevel | quote }}
          envFrom:
            - configMapRef:
                name: {{ include "${CHART_NAME}.fullname" . }}-config
          livenessProbe:
            httpGet:
              path: /healthz
              port: http
          readinessProbe:
            httpGet:
              path: /ready
              port: http
          resources:
            {{- toYaml .Values.resources | nindent 12 }}
          volumeMounts:
            - name: tmp
              mountPath: /tmp
      volumes:
        - name: tmp
          emptyDir: {}
      {{- with .Values.nodeSelector }}
      nodeSelector:
        {{- toYaml . | nindent 8 }}
      {{- end }}
```

## CI/CD Pipelines

### GitHub Actions

**Current Versions & Documentation:**
- **GitHub Actions Docs**: https://docs.github.com/en/actions
- **Reusable Workflows**: https://docs.github.com/en/actions/using-workflows/reusing-workflows
- **OIDC for Cloud**: https://docs.github.com/en/actions/deployment/security-hardening-your-deployments

```yaml
# .github/workflows/ci-cd.yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

# Recommended: Use OIDC for cloud provider authentication (no long-lived secrets)
permissions:
  contents: read
  packages: write
  id-token: write  # Required for OIDC

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '22'
          cache: 'npm'
      
      - name: Run tests
        run: |
          npm ci
          npm test

  build:
    needs: test
    runs-on: ubuntu-latest
    outputs:
      image-tag: ${{ steps.meta.outputs.tags }}
      digest: ${{ steps.build.outputs.digest }}
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up QEMU
        uses: docker/setup-qemu-action@v3
      
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
            type=raw,value=latest,enable=${{ github.ref == 'refs/heads/main' }}
      
      - name: Build and push
        id: build
        uses: docker/build-push-action@v6
        with:
          context: .
          platforms: linux/amd64,linux/arm64
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
          provenance: true
          sbom: true

  deploy-dev:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/develop'
    steps:
      - uses: actions/checkout@v4
      
      - name: Update Kustomize image tag
        run: |
          cd overlays/dev
          kustomize edit set image ${IMAGE_NAME}=${REGISTRY}/${IMAGE_NAME}:${{ github.sha }}
      
      - name: Commit and push
        run: |
          git config user.name "GitHub Actions"
          git config user.email "actions@github.com"
          git add .
          git commit -m "chore: update dev image to ${{ github.sha }}"
          git push

  deploy-prod:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    environment: production
    steps:
      - uses: actions/checkout@v4
      
      - name: Update Kustomize image tag
        run: |
          cd overlays/prod
          kustomize edit set image ${IMAGE_NAME}=${REGISTRY}/${IMAGE_NAME}:${{ github.sha }}
      
      - name: Create PR for production
        uses: peter-evans/create-pull-request@v5
        with:
          title: "Deploy ${{ github.sha }} to production"
          body: "Auto-generated PR to deploy commit ${{ github.sha }}"
          branch: deploy/prod-${{ github.sha }}
```

### Tekton Pipeline (OpenShift)

**Current Versions & Documentation:**
- **Tekton Pipelines**: v0.67.x (Latest stable as of January 2026)
- **OpenShift Pipelines**: Based on Tekton, included in OCP 4.14+
- **Docs**: https://tekton.dev/docs/
- **OpenShift Docs**: https://docs.openshift.com/pipelines/
- **CLI (tkn)**: `brew install tektoncd-cli` or from OpenShift

```bash
# Install Tekton CLI
brew install tektoncd-cli
# OR on OpenShift
oc get tkn  # Pre-installed with OpenShift Pipelines operator

# List pipelines and runs
tkn pipeline list
tkn pipelinerun list

# Start a pipeline
tkn pipeline start ${PIPELINE_NAME} -p param1=value1

# View logs
tkn pipelinerun logs ${PIPELINERUN_NAME} -f
```

```yaml
# Note: Tekton v0.50+ uses v1 API, older clusters may need v1beta1
apiVersion: tekton.dev/v1
kind: Pipeline
metadata:
  name: build-and-deploy
  namespace: ${NAMESPACE}
spec:
  params:
    - name: git-url
      type: string
    - name: git-revision
      type: string
      default: main
    - name: image-name
      type: string
    - name: deployment-namespace
      type: string
  
  workspaces:
    - name: shared-workspace
    - name: docker-credentials
  
  tasks:
    - name: git-clone
      taskRef:
        name: git-clone
        kind: ClusterTask
      params:
        - name: url
          value: $(params.git-url)
        - name: revision
          value: $(params.git-revision)
      workspaces:
        - name: output
          workspace: shared-workspace
    
    - name: build-image
      taskRef:
        name: buildah
        kind: ClusterTask
      runAfter:
        - git-clone
      params:
        - name: IMAGE
          value: $(params.image-name):$(tasks.git-clone.results.commit)
        - name: DOCKERFILE
          value: ./Dockerfile
      workspaces:
        - name: source
          workspace: shared-workspace
        - name: dockerconfig
          workspace: docker-credentials
    
    - name: update-manifest
      taskRef:
        name: kustomize-update
      runAfter:
        - build-image
      params:
        - name: image
          value: $(params.image-name):$(tasks.git-clone.results.commit)
        - name: overlay-path
          value: overlays/$(params.deployment-namespace)
      workspaces:
        - name: source
          workspace: shared-workspace
    
    - name: deploy
      taskRef:
        name: kubernetes-actions
        kind: ClusterTask
      runAfter:
        - update-manifest
      params:
        - name: script
          value: |
            kubectl apply -k overlays/$(params.deployment-namespace)
            kubectl rollout status deployment/${APP_NAME} -n $(params.deployment-namespace)
```

## Progressive Delivery

### Argo Rollouts - Canary

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: ${APP_NAME}
  namespace: ${NAMESPACE}
spec:
  replicas: 5
  selector:
    matchLabels:
      app: ${APP_NAME}
  template:
    metadata:
      labels:
        app: ${APP_NAME}
    spec:
      containers:
        - name: ${APP_NAME}
          image: ${IMAGE}:${TAG}
          ports:
            - containerPort: 8080
  strategy:
    canary:
      canaryService: ${APP_NAME}-canary
      stableService: ${APP_NAME}-stable
      trafficRouting:
        nginx:
          stableIngress: ${APP_NAME}-ingress
      steps:
        - setWeight: 5
        - pause: {duration: 2m}
        - setWeight: 20
        - pause: {duration: 5m}
        - setWeight: 50
        - pause: {duration: 5m}
        - setWeight: 80
        - pause: {duration: 5m}
      analysis:
        templates:
          - templateName: success-rate
        startingStep: 2
        args:
          - name: service-name
            value: ${APP_NAME}-canary
---
apiVersion: argoproj.io/v1alpha1
kind: AnalysisTemplate
metadata:
  name: success-rate
spec:
  args:
    - name: service-name
  metrics:
    - name: success-rate
      interval: 1m
      successCondition: result[0] >= 0.95
      failureLimit: 3
      provider:
        prometheus:
          address: http://prometheus:9090
          query: |
            sum(rate(http_requests_total{service="{{args.service-name}}",status=~"2.."}[5m]))
            /
            sum(rate(http_requests_total{service="{{args.service-name}}"}[5m]))
```

### Argo Rollouts - Blue-Green

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: ${APP_NAME}
  namespace: ${NAMESPACE}
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ${APP_NAME}
  template:
    metadata:
      labels:
        app: ${APP_NAME}
    spec:
      containers:
        - name: ${APP_NAME}
          image: ${IMAGE}:${TAG}
  strategy:
    blueGreen:
      activeService: ${APP_NAME}-active
      previewService: ${APP_NAME}-preview
      autoPromotionEnabled: false
      scaleDownDelaySeconds: 30
      prePromotionAnalysis:
        templates:
          - templateName: smoke-test
      postPromotionAnalysis:
        templates:
          - templateName: success-rate
        args:
          - name: service-name
            value: ${APP_NAME}-active
```

## Policy as Code

### Kyverno Policies

**Current Versions & Documentation:**
- **Kyverno**: v1.13.x (Latest stable as of January 2026)
- **Install**: `helm install kyverno kyverno/kyverno -n kyverno --create-namespace`
- **Docs**: https://kyverno.io/docs/
- **Policy Library**: https://kyverno.io/policies/
- **CLI**: `brew install kyverno` or from GitHub releases

```bash
# Install Kyverno via Helm (v1.13.x+)
helm repo add kyverno https://kyverno.github.io/kyverno/
helm repo update
helm install kyverno kyverno/kyverno -n kyverno --create-namespace \
  --set replicaCount=3 \
  --set resources.limits.memory=512Mi

# Install Kyverno CLI
brew install kyverno

# Test policy locally before applying
kyverno apply policy.yaml --resource deployment.yaml

# Validate policies
kyverno test .
```

```yaml
# Require resource limits (Kyverno v1.10+ syntax)
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: require-resource-limits
spec:
  validationFailureAction: enforce
  rules:
    - name: require-limits
      match:
        resources:
          kinds:
            - Pod
      validate:
        message: "Resource limits are required"
        pattern:
          spec:
            containers:
              - resources:
                  limits:
                    memory: "?*"
                    cpu: "?*"
---
# Add default labels
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: add-default-labels
spec:
  rules:
    - name: add-labels
      match:
        resources:
          kinds:
            - Pod
      mutate:
        patchStrategicMerge:
          metadata:
            labels:
              managed-by: cluster-code
---
# Require non-root
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: require-run-as-non-root
spec:
  validationFailureAction: enforce
  rules:
    - name: run-as-non-root
      match:
        resources:
          kinds:
            - Pod
      validate:
        message: "Containers must run as non-root"
        pattern:
          spec:
            securityContext:
              runAsNonRoot: true
            containers:
              - securityContext:
                  allowPrivilegeEscalation: false
```

### OPA Gatekeeper

**Current Versions & Documentation:**
- **Gatekeeper**: v3.18.x (Latest stable as of January 2026)
- **Install**: `helm install gatekeeper gatekeeper/gatekeeper -n gatekeeper-system --create-namespace`
- **Docs**: https://open-policy-agent.github.io/gatekeeper/
- **Constraint Library**: https://github.com/open-policy-agent/gatekeeper-library
- **Rego Playground**: https://play.openpolicyagent.org/

```bash
# Install Gatekeeper via Helm (v3.18.x+)
helm repo add gatekeeper https://open-policy-agent.github.io/gatekeeper/charts
helm repo update
helm install gatekeeper gatekeeper/gatekeeper -n gatekeeper-system --create-namespace \
  --set replicas=3 \
  --set audit.replicas=1

# Check Gatekeeper status
kubectl get pods -n gatekeeper-system
kubectl get constrainttemplates
kubectl get constraints

# View violations
kubectl get constraints -o json | jq '.items[].status.violations'
```

```yaml
# Constraint Template (Gatekeeper v3.x)
apiVersion: templates.gatekeeper.sh/v1
kind: ConstraintTemplate
metadata:
  name: k8srequiredlabels
spec:
  crd:
    spec:
      names:
        kind: K8sRequiredLabels
      validation:
        openAPIV3Schema:
          type: object
          properties:
            labels:
              type: array
              items:
                type: string
  targets:
    - target: admission.k8s.gatekeeper.sh
      rego: |
        package k8srequiredlabels

        violation[{"msg": msg}] {
          provided := {label | input.review.object.metadata.labels[label]}
          required := {label | label := input.parameters.labels[_]}
          missing := required - provided
          count(missing) > 0
          msg := sprintf("Missing required labels: %v", [missing])
        }
---
# Constraint
apiVersion: constraints.gatekeeper.sh/v1beta1
kind: K8sRequiredLabels
metadata:
  name: require-app-labels
spec:
  match:
    kinds:
      - apiGroups: ["apps"]
        kinds: ["Deployment"]
  parameters:
    labels:
      - "app.kubernetes.io/name"
      - "app.kubernetes.io/managed-by"
```
