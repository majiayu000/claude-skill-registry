---
name: fluxcd
description: GitOps continuous delivery toolkit for Kubernetes with Flux CD. Use when implementing GitOps workflows, declarative deployments, Helm chart automation, Kustomize overlays, image update automation, multi-tenancy, or Git-based continuous delivery. Triggers: flux, fluxcd, gitops, kustomization, helmrelease, gitrepository, helmrepository, imagerepository, imagepolicy, image automation, source controller, continuous delivery, kubernetes deployment automation, helm automation, kustomize automation, git sync, declarative deployment.
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
---

# Flux CD GitOps Toolkit

## Overview

Flux CD is a declarative, GitOps continuous delivery solution for Kubernetes. It automatically ensures that the state of your Kubernetes cluster matches the configuration stored in Git repositories.

**When to use this skill:**
- Implementing GitOps workflows for Kubernetes
- Automating Helm chart deployments and upgrades
- Managing Kustomize overlays across environments
- Automating container image updates from registries
- Setting up multi-tenant Kubernetes with isolated teams
- Integrating Git-based continuous delivery pipelines
- Managing infrastructure and application dependencies
- Implementing progressive delivery with canary deployments

### Core Architecture

Flux is composed of specialized controllers, each handling specific aspects of GitOps:

#### Source Controller

- **GitRepository**: Fetches artifacts from Git repositories
- **HelmRepository**: Fetches Helm charts from chart repositories
- **HelmChart**: Fetches charts from GitRepository or HelmRepository sources
- **Bucket**: Fetches artifacts from S3-compatible storage

#### Kustomize Controller

- **Kustomization**: Applies Kustomize overlays and manages reconciliation
- Supports dependency ordering and health checks
- Handles pruning of deleted resources

#### Helm Controller

- **HelmRelease**: Manages Helm chart installations and upgrades
- Supports automated remediation and testing
- Handles rollbacks on failure

#### Notification Controller

- **Provider**: Defines notification endpoints (Slack, MS Teams, etc.)
- **Alert**: Sends alerts based on resource events
- **Receiver**: Handles webhook notifications from external systems

#### Image Automation Controllers

- **ImageRepository**: Scans container registries for image metadata
- **ImagePolicy**: Defines rules for selecting image tags
- **ImageUpdateAutomation**: Updates Git repository with new image tags

## Installation and Bootstrap

### Prerequisites

```bash

# Install Flux CLI
curl -s https://fluxcd.io/install.sh | sudo bash

# Or using Homebrew
brew install fluxcd/tap/flux

# Verify installation
flux --version
```

### Bootstrap with GitHub

```bash
# Export GitHub personal access token
export GITHUB_TOKEN=<your-token>

# Bootstrap Flux
flux bootstrap github \
  --owner=<github-username> \
  --repository=<repo-name> \
  --branch=main \
  --path=clusters/production \
  --personal \
  --components-extra=image-reflector-controller,image-automation-controller
```

### Bootstrap with GitLab

```bash
export GITLAB_TOKEN=<your-token>

flux bootstrap gitlab \
  --owner=<gitlab-group> \
  --repository=<repo-name> \
  --branch=main \
  --path=clusters/production \
  --personal
```

### Pre-commit Validation

Check your manifests before committing:

```bash
# Validate all Flux resources
flux check

# Check specific resources
kubectl apply --dry-run=server -f clusters/production/
```

## Repository Structure Best Practices

### Standard Layout

```text
├── clusters/
│   ├── production/
│   │   ├── flux-system/           # Flux components (managed by bootstrap)
│   │   ├── infrastructure.yaml    # Infrastructure sources & kustomizations
│   │   └── apps.yaml              # Application sources & kustomizations
│   └── staging/
│       ├── flux-system/
│       ├── infrastructure.yaml
│       └── apps.yaml
├── infrastructure/
│   ├── base/                      # Base infrastructure
│   │   ├── ingress-nginx/
│   │   ├── cert-manager/
│   │   └── sealed-secrets/
│   └── overlays/
│       ├── production/
│       └── staging/
└── apps/
    ├── base/
    │   ├── app1/
    │   └── app2/
    └── overlays/
        ├── production/
        └── staging/
```

### Multi-Tenancy Layout

```text
├── clusters/
│   └── production/
│       ├── flux-system/
│       ├── tenants/
│       │   ├── team-a.yaml        # Team A namespace and RBAC
│       │   └── team-b.yaml        # Team B namespace and RBAC
│       └── infrastructure.yaml
├── tenants/
│   ├── base/
│   │   ├── team-a/
│   │   │   ├── namespace.yaml
│   │   │   ├── rbac.yaml
│   │   │   └── sync.yaml          # GitRepository + Kustomization for team
│   │   └── team-b/
│   │       ├── namespace.yaml
│   │       ├── rbac.yaml
│   │       └── sync.yaml
│   └── overlays/
│       └── production/
└── teams/                         # Separate repos or paths for each team
    ├── team-a-repo/
    └── team-b-repo/
```

## GitRepository and Kustomization

### Basic GitRepository

```yaml
apiVersion: source.toolkit.fluxcd.io/v1
kind: GitRepository
metadata:
  name: flux-system
  namespace: flux-system
spec:
  interval: 1m0s
  ref:
    branch: main
  url: https://github.com/org/repo
  secretRef:
    name: flux-system
```

### GitRepository with Specific Path

```yaml
apiVersion: source.toolkit.fluxcd.io/v1
kind: GitRepository
metadata:
  name: apps
  namespace: flux-system
spec:
  interval: 5m0s
  ref:
    branch: main
  url: https://github.com/org/apps-repo
  ignore: |
    # Exclude all
    /*
    # Include specific paths
    !/apps/production/
```

### Basic Kustomization

```yaml
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: infrastructure
  namespace: flux-system
spec:
  interval: 10m0s
  sourceRef:
    kind: GitRepository
    name: flux-system
  path: ./infrastructure/production
  prune: true
  wait: true
  timeout: 5m0s
```

### Kustomization with Dependencies

```yaml
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: apps
  namespace: flux-system
spec:
  interval: 10m0s
  dependsOn:
    - name: infrastructure
  sourceRef:
    kind: GitRepository
    name: flux-system
  path: ./apps/production
  prune: true
  wait: true
  timeout: 5m0s
  healthChecks:
    - apiVersion: apps/v1
      kind: Deployment
      name: app-name
      namespace: app-namespace
  postBuild:
    substitute:
      cluster_name: production
      domain: example.com
    substituteFrom:
      - kind: ConfigMap
        name: cluster-vars
```

### Variable Substitution

Create a ConfigMap for cluster-specific variables:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: cluster-vars
  namespace: flux-system
data:
  cluster_name: production
  cluster_region: us-east-1
  domain: example.com
```

Use variables in manifests:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
  namespace: default
data:
  cluster: ${cluster_name}
  region: ${cluster_region}
  url: https://app.${domain}
```

## Multi-Tenancy Patterns

### Namespace Isolation

Flux supports multi-tenant clusters where teams have isolated namespaces with their own GitRepository sources and Kustomizations.

### Tenant Bootstrap Pattern

```yaml
# clusters/production/tenants/team-a.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: team-a
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: team-a-reconciler
  namespace: team-a
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: team-a-reconciler
  namespace: team-a
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-admin
subjects:
  - kind: ServiceAccount
    name: team-a-reconciler
    namespace: team-a
---
apiVersion: source.toolkit.fluxcd.io/v1
kind: GitRepository
metadata:
  name: team-a-repo
  namespace: team-a
spec:
  interval: 1m
  url: https://github.com/org/team-a-repo
  ref:
    branch: main
---
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: team-a-apps
  namespace: team-a
spec:
  interval: 10m
  serviceAccountName: team-a-reconciler
  sourceRef:
    kind: GitRepository
    name: team-a-repo
  path: ./apps
  prune: true
  validation: client
```

### Tenant RBAC Restrictions

Restrict tenant reconcilers to their namespace only:

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: team-a-reconciler
  namespace: team-a
rules:
  - apiGroups: ["*"]
    resources: ["*"]
    verbs: ["*"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: team-a-reconciler
  namespace: team-a
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: team-a-reconciler
subjects:
  - kind: ServiceAccount
    name: team-a-reconciler
    namespace: team-a
```

### Cross-Tenant Dependencies

Teams can depend on shared infrastructure while maintaining isolation:

```yaml
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: team-a-apps
  namespace: team-a
spec:
  interval: 10m
  dependsOn:
    - name: shared-ingress
      namespace: flux-system
    - name: shared-monitoring
      namespace: flux-system
  sourceRef:
    kind: GitRepository
    name: team-a-repo
  path: ./apps
  prune: true
```

## Helm Integration

Flux provides deep integration with Helm for chart-based deployments.

### Helm Repository and Helm Release

### HelmRepository

```yaml
apiVersion: source.toolkit.fluxcd.io/v1beta2
kind: HelmRepository
metadata:
  name: bitnami
  namespace: flux-system
spec:
  interval: 1h0s
  url: https://charts.bitnami.com/bitnami
```

### HelmRepository with Authentication

```yaml
apiVersion: source.toolkit.fluxcd.io/v1beta2
kind: HelmRepository
metadata:
  name: private-charts
  namespace: flux-system
spec:
  interval: 1h0s
  url: https://charts.example.com
  secretRef:
    name: helm-charts-auth
---
apiVersion: v1
kind: Secret
metadata:
  name: helm-charts-auth
  namespace: flux-system
type: Opaque
stringData:
  username: user
  password: pass
```

### Basic HelmRelease

```yaml
apiVersion: helm.toolkit.fluxcd.io/v2beta2
kind: HelmRelease
metadata:
  name: nginx-ingress
  namespace: ingress-nginx
spec:
  interval: 10m0s
  chart:
    spec:
      chart: ingress-nginx
      version: "4.8.x"
      sourceRef:
        kind: HelmRepository
        name: ingress-nginx
        namespace: flux-system
      interval: 1h0s
  values:
    controller:
      service:
        type: LoadBalancer
```

### HelmRelease with ValuesFrom

```yaml
apiVersion: helm.toolkit.fluxcd.io/v2beta2
kind: HelmRelease
metadata:
  name: my-app
  namespace: apps
spec:
  interval: 10m0s
  chart:
    spec:
      chart: my-app
      version: "1.0.x"
      sourceRef:
        kind: HelmRepository
        name: my-charts
        namespace: flux-system
  values:
    replicas: 2
  valuesFrom:
    - kind: ConfigMap
      name: app-config
      valuesKey: values.yaml
    - kind: Secret
      name: app-secrets
      valuesKey: secrets.yaml
```

### HelmRelease with Testing and Rollback

```yaml
apiVersion: helm.toolkit.fluxcd.io/v2beta2
kind: HelmRelease
metadata:
  name: my-app
  namespace: apps
spec:
  interval: 10m0s
  chart:
    spec:
      chart: my-app
      version: "1.0.x"
      sourceRef:
        kind: HelmRepository
        name: my-charts
        namespace: flux-system
  install:
    remediation:
      retries: 3
  upgrade:
    remediation:
      retries: 3
      remediateLastFailure: true
    cleanupOnFail: true
  test:
    enable: true
  rollback:
    cleanupOnFail: true
    recreate: true
  values:
    image:
      tag: v1.0.0
```

### HelmRelease with Dependencies

```yaml
apiVersion: helm.toolkit.fluxcd.io/v2beta2
kind: HelmRelease
metadata:
  name: my-app
  namespace: apps
spec:
  interval: 10m0s
  dependsOn:
    - name: cert-manager
      namespace: cert-manager
    - name: nginx-ingress
      namespace: ingress-nginx
  chart:
    spec:
      chart: my-app
      version: "1.0.x"
      sourceRef:
        kind: HelmRepository
        name: my-charts
        namespace: flux-system
  values:
    ingress:
      enabled: true
      className: nginx
```

## Secret Management with SOPS

### Install SOPS and Age

```bash
# Install SOPS
brew install sops

# Install Age
brew install age

# Generate Age key
age-keygen -o age.agekey

# Get public key for .sops.yaml
age-keygen -y age.agekey
```

### Configure SOPS

Create `.sops.yaml` in repository root:

```yaml
creation_rules:
  - path_regex: .*/production/.*\.yaml
    encrypted_regex: ^(data|stringData)$
    age: age1ql3z7hjy54pw3hyww5ayyfg7zqgvc7w3j2elw8zmrj2kg5sfn9aqmcac8p
  - path_regex: .*/staging/.*\.yaml
    encrypted_regex: ^(data|stringData)$
    age: age1ql3z7hjy54pw3hyww5ayyfg7zqgvc7w3j2elw8zmrj2kg5sfn9aqmcac8p
```

### Create Encrypted Secret

```bash
# Create secret manifest
cat <<EOF > secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
  namespace: apps
stringData:
  username: admin
  password: supersecret
EOF

# Encrypt with SOPS
sops --encrypt --in-place secret.yaml

# Decrypt for viewing
sops --decrypt secret.yaml
```

### Configure Flux for SOPS Decryption

Create secret with Age private key:

```bash
cat age.agekey | kubectl create secret generic sops-age \
  --namespace=flux-system \
  --from-file=age.agekey=/dev/stdin
```

Configure Kustomization to decrypt:

```yaml
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: apps
  namespace: flux-system
spec:
  interval: 10m0s
  sourceRef:
    kind: GitRepository
    name: flux-system
  path: ./apps/production
  prune: true
  decryption:
    provider: sops
    secretRef:
      name: sops-age
```

### SOPS with Multiple Keys

For team collaboration, add multiple Age keys:

```yaml
creation_rules:
  - path_regex: .*/production/.*\.yaml
    encrypted_regex: ^(data|stringData)$
    age: >-
      age1ql3z7hjy54pw3hyww5ayyfg7zqgvc7w3j2elw8zmrj2kg5sfn9aqmcac8p,
      age1zvkyg2lqzraa2lnjvqej32nkuu0ues2s82hzrye869xeexvn73equnujwj,
      age1penhr3v0pklzv6lqrvt3zyqhfvqffkjn5j2qhzc8xr7q8vpfck4q7n8k3f
```

## Image Automation

Flux can automatically detect new container image versions and update manifests in Git.

### Image Automation Architecture

The image automation workflow consists of three resources:

1. **ImageRepository** - Scans container registry for available tags
2. **ImagePolicy** - Defines tag selection rules (semver, regex, alphabetical)
3. **ImageUpdateAutomation** - Commits updated image tags back to Git

### Image Automation Workflow

```text
Container Registry
       |
       | (scan for tags)
       v
ImageRepository
       |
       | (filter & select)
       v
  ImagePolicy
       |
       | (update manifests)
       v
ImageUpdateAutomation
       |
       | (commit to Git)
       v
   GitRepository
       |
       | (reconcile)
       v
  Kustomization
       |
       v
   Kubernetes Cluster
```

### ImageRepository

```yaml
apiVersion: image.toolkit.fluxcd.io/v1beta2
kind: ImageRepository
metadata:
  name: my-app
  namespace: flux-system
spec:
  image: ghcr.io/org/my-app
  interval: 1m0s
```

### ImageRepository with Authentication

```yaml
apiVersion: image.toolkit.fluxcd.io/v1beta2
kind: ImageRepository
metadata:
  name: my-app
  namespace: flux-system
spec:
  image: registry.example.com/org/my-app
  interval: 1m0s
  secretRef:
    name: registry-credentials
---
apiVersion: v1
kind: Secret
metadata:
  name: registry-credentials
  namespace: flux-system
type: kubernetes.io/dockerconfigjson
data:
  .dockerconfigjson: <base64-encoded-docker-config>
```

### ImagePolicy - Semantic Versioning

```yaml
apiVersion: image.toolkit.fluxcd.io/v1beta2
kind: ImagePolicy
metadata:
  name: my-app
  namespace: flux-system
spec:
  imageRepositoryRef:
    name: my-app
  policy:
    semver:
      range: 1.0.x
```

### ImagePolicy - Alphabetical

```yaml
apiVersion: image.toolkit.fluxcd.io/v1beta2
kind: ImagePolicy
metadata:
  name: my-app-develop
  namespace: flux-system
spec:
  imageRepositoryRef:
    name: my-app
  policy:
    alphabetical:
      order: asc
  filterTags:
    pattern: "^develop-[a-f0-9]+-(?P<ts>[0-9]+)"
    extract: "$ts"
```

### ImagePolicy - Numerical

```yaml
apiVersion: image.toolkit.fluxcd.io/v1beta2
kind: ImagePolicy
metadata:
  name: my-app-build
  namespace: flux-system
spec:
  imageRepositoryRef:
    name: my-app
  policy:
    numerical:
      order: asc
  filterTags:
    pattern: "^build-(?P<num>[0-9]+)"
    extract: "$num"
```

### ImageUpdateAutomation

```yaml
apiVersion: image.toolkit.fluxcd.io/v1beta1
kind: ImageUpdateAutomation
metadata:
  name: my-app
  namespace: flux-system
spec:
  interval: 1m0s
  sourceRef:
    kind: GitRepository
    name: flux-system
  git:
    checkout:
      ref:
        branch: main
    commit:
      author:
        email: fluxcdbot@users.noreply.github.com
        name: fluxcdbot
      messageTemplate: |
        Automated image update

        Automation name: {{ .AutomationObject }}

        Files:
        {{ range $filename, $_ := .Updated.Files -}}
        - {{ $filename }}
        {{ end -}}

        Objects:
        {{ range $resource, $_ := .Updated.Objects -}}
        - {{ $resource.Kind }} {{ $resource.Name }}
        {{ end -}}

        Images:
        {{ range .Updated.Images -}}
        - {{.}}
        {{ end -}}
  update:
    path: ./apps/production
    strategy: Setters
```

### Manifest with Image Update Markers

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
  namespace: apps
spec:
  template:
    spec:
      containers:
        - name: app
          image: ghcr.io/org/my-app:1.0.0 # {"$imagepolicy": "flux-system:my-app"}
```

### Image Automation Best Practices

**Environment Strategy:**
- Enable automation in development/staging first
- Use manual approval for production (PR-based workflow)
- Test policy rules before deploying

**Tag Policies:**
- Use semver for releases (e.g., `1.0.x`, `>=1.0.0`)
- Use regex for branch-based tags (e.g., `^develop-.*`)
- Use numerical for build numbers

**Security:**
- Scan images before deployment (integrate with CI)
- Use private registries with authentication
- Enable image signing verification

### ImageUpdateAutomation with Push Branch

For PR-based workflows:

```yaml
apiVersion: image.toolkit.fluxcd.io/v1beta1
kind: ImageUpdateAutomation
metadata:
  name: my-app
  namespace: flux-system
spec:
  interval: 1m0s
  sourceRef:
    kind: GitRepository
    name: flux-system
  git:
    checkout:
      ref:
        branch: main
    push:
      branch: image-updates
    commit:
      author:
        email: fluxcdbot@users.noreply.github.com
        name: fluxcdbot
      messageTemplate: |
        Automated image update by Flux

        [ci skip]
  update:
    path: ./apps/production
    strategy: Setters
```

## Notifications

### Slack Provider

```yaml
apiVersion: notification.toolkit.fluxcd.io/v1beta3
kind: Provider
metadata:
  name: slack
  namespace: flux-system
spec:
  type: slack
  channel: flux-notifications
  secretRef:
    name: slack-webhook-url
---
apiVersion: v1
kind: Secret
metadata:
  name: slack-webhook-url
  namespace: flux-system
stringData:
  address: https://hooks.slack.com/services/YOUR/WEBHOOK/URL
```

### Alert for Kustomization Failures

```yaml
apiVersion: notification.toolkit.fluxcd.io/v1beta3
kind: Alert
metadata:
  name: kustomization-failures
  namespace: flux-system
spec:
  providerRef:
    name: slack
  eventSeverity: error
  eventSources:
    - kind: Kustomization
      name: "*"
  exclusionList:
    - ".*health check failed.*"
```

### Alert for HelmRelease Events

```yaml
apiVersion: notification.toolkit.fluxcd.io/v1beta3
kind: Alert
metadata:
  name: helm-releases
  namespace: flux-system
spec:
  providerRef:
    name: slack
  eventSeverity: info
  eventSources:
    - kind: HelmRelease
      name: "*"
      namespace: "*"
  summary: "Helm Release {{ .InvolvedObject.name }} in {{ .InvolvedObject.namespace }}"
```

### Microsoft Teams Provider

```yaml
apiVersion: notification.toolkit.fluxcd.io/v1beta3
kind: Provider
metadata:
  name: msteams
  namespace: flux-system
spec:
  type: msteams
  secretRef:
    name: msteams-webhook-url
---
apiVersion: v1
kind: Secret
metadata:
  name: msteams-webhook-url
  namespace: flux-system
stringData:
  address: https://outlook.office.com/webhook/YOUR/WEBHOOK/URL
```

### Receiver for GitHub Webhooks

```yaml
apiVersion: notification.toolkit.fluxcd.io/v1
kind: Receiver
metadata:
  name: github-receiver
  namespace: flux-system
spec:
  type: github
  events:
    - "ping"
    - "push"
  secretRef:
    name: github-webhook-token
  resources:
    - kind: GitRepository
      name: flux-system
---
apiVersion: v1
kind: Secret
metadata:
  name: github-webhook-token
  namespace: flux-system
type: Opaque
stringData:
  token: <webhook-secret>
```

## Multi-Cluster Setup

### Fleet Repository Structure

```text
fleet-infra/
├── clusters/
│   ├── production/
│   │   ├── flux-system/
│   │   └── cluster-config.yaml
│   ├── staging/
│   │   ├── flux-system/
│   │   └── cluster-config.yaml
│   └── development/
│       ├── flux-system/
│       └── cluster-config.yaml
├── infrastructure/
│   ├── base/
│   └── overlays/
│       ├── production/
│       ├── staging/
│       └── development/
└── apps/
    ├── base/
    └── overlays/
        ├── production/
        ├── staging/
        └── development/
```

### Cluster-Specific Configuration

Production cluster (`clusters/production/cluster-config.yaml`):

```yaml
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: infrastructure
  namespace: flux-system
spec:
  interval: 10m0s
  sourceRef:
    kind: GitRepository
    name: flux-system
  path: ./infrastructure/overlays/production
  prune: true
  wait: true
  postBuild:
    substitute:
      cluster_name: production
      cluster_region: us-east-1
      replicas: "3"
---
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: apps
  namespace: flux-system
spec:
  interval: 10m0s
  dependsOn:
    - name: infrastructure
  sourceRef:
    kind: GitRepository
    name: flux-system
  path: ./apps/overlays/production
  prune: true
  postBuild:
    substitute:
      cluster_name: production
      domain: prod.example.com
```

### Multi-Cluster with Cluster API

Manage multiple clusters using Cluster API:

```yaml
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: cluster-staging
  namespace: flux-system
spec:
  interval: 10m0s
  sourceRef:
    kind: GitRepository
    name: flux-system
  path: ./clusters/staging
  prune: true
  kubeConfig:
    secretRef:
      name: staging-kubeconfig
---
apiVersion: v1
kind: Secret
metadata:
  name: staging-kubeconfig
  namespace: flux-system
type: Opaque
data:
  value: <base64-encoded-kubeconfig>
```

## Dependency Management

### Infrastructure Layer Dependencies

```yaml
# Base infrastructure
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: crds
  namespace: flux-system
spec:
  interval: 1h
  sourceRef:
    kind: GitRepository
    name: flux-system
  path: ./infrastructure/crds
  prune: false # Never prune CRDs automatically
---
# Depends on CRDs
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: cert-manager
  namespace: flux-system
spec:
  interval: 10m
  dependsOn:
    - name: crds
  sourceRef:
    kind: GitRepository
    name: flux-system
  path: ./infrastructure/cert-manager
  healthChecks:
    - apiVersion: apps/v1
      kind: Deployment
      name: cert-manager
      namespace: cert-manager
---
# Depends on cert-manager
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: ingress-nginx
  namespace: flux-system
spec:
  interval: 10m
  dependsOn:
    - name: cert-manager
  sourceRef:
    kind: GitRepository
    name: flux-system
  path: ./infrastructure/ingress-nginx
```

### Application Dependencies

```yaml
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: database
  namespace: flux-system
spec:
  interval: 10m
  sourceRef:
    kind: GitRepository
    name: flux-system
  path: ./apps/database
  healthChecks:
    - apiVersion: apps/v1
      kind: StatefulSet
      name: postgresql
      namespace: database
---
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: backend
  namespace: flux-system
spec:
  interval: 5m
  dependsOn:
    - name: database
  sourceRef:
    kind: GitRepository
    name: flux-system
  path: ./apps/backend
---
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: frontend
  namespace: flux-system
spec:
  interval: 5m
  dependsOn:
    - name: backend
  sourceRef:
    kind: GitRepository
    name: flux-system
  path: ./apps/frontend
```

## Best Practices

### 1. Resource Organization

- **Separate concerns**: Keep infrastructure, apps, and cluster configs in separate directories
- **Use overlays**: Leverage Kustomize overlays for environment-specific configurations
- **Namespace isolation**: Use separate namespaces for different teams or applications

### 2. Reconciliation Intervals

- **Infrastructure**: 1h (stable resources that change infrequently)
- **Applications**: 10m (balance between responsiveness and API load)
- **Development**: 1m-5m (faster feedback during active development)
- **Source repos**: 1m-5m (detect changes quickly)

### 3. Pruning Strategy

- **Enable pruning**: Set `prune: true` for Kustomizations to clean up deleted resources
- **CRDs exception**: Set `prune: false` for CRD Kustomizations to prevent accidental deletion
- **Test before production**: Test pruning in non-production environments first

### 4. Health Checks

Always define health checks for critical resources:

```yaml
spec:
  healthChecks:
    - apiVersion: apps/v1
      kind: Deployment
      name: critical-app
      namespace: apps
    - apiVersion: v1
      kind: Service
      name: critical-service
      namespace: apps
```

### 5. Suspend Reconciliation

Temporarily suspend reconciliation when needed:

```bash
# Suspend a Kustomization
flux suspend kustomization apps

# Resume reconciliation
flux resume kustomization apps
```

### 6. Force Reconciliation

Trigger immediate reconciliation:

```bash
# Reconcile a specific Kustomization
flux reconcile kustomization apps --with-source

# Reconcile a HelmRelease
flux reconcile helmrelease my-app -n apps
```

### 7. Monitoring and Debugging

```bash
# Check Flux components status
flux check

# Get all Flux resources
flux get all

# Get specific resource with detailed info
flux get kustomization infrastructure

# View logs
flux logs --level=error --all-namespaces

# Export current cluster state
flux export source git flux-system
flux export kustomization --all
```

### 8. Version Control

- **Commit frequently**: Small, atomic commits are easier to debug
- **Meaningful messages**: Describe what and why, not just what
- **Branch protection**: Require reviews for main/production branches
- **Tag releases**: Use Git tags for application version tracking

### 9. Security

- **Encrypt secrets**: Always use SOPS or external secret managers
- **RBAC**: Implement strict RBAC policies for multi-tenancy
- **Network policies**: Define network policies for namespace isolation
- **Image scanning**: Integrate container image scanning in CI/CD
- **Policy enforcement**: Use tools like OPA Gatekeeper or Kyverno

### 10. Disaster Recovery

```bash

# Backup Flux configuration
flux export source git --all > sources.yaml
flux export kustomization --all > kustomizations.yaml
flux export helmrelease --all > helmreleases.yaml

# Restore from backup
kubectl apply -f sources.yaml
kubectl apply -f kustomizations.yaml
kubectl apply -f helmreleases.yaml
```

## Common Patterns

### Progressive Delivery with Flagger

```yaml
apiVersion: helm.toolkit.fluxcd.io/v2beta2
kind: HelmRelease
metadata:
  name: flagger
  namespace: flagger-system
spec:
  interval: 10m
  chart:
    spec:
      chart: flagger
      version: "1.x"
      sourceRef:
        kind: HelmRepository
        name: flagger
        namespace: flux-system
---
apiVersion: flagger.app/v1beta1
kind: Canary
metadata:
  name: my-app
  namespace: apps
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: my-app
  service:
    port: 80
  analysis:
    interval: 1m
    threshold: 5
    maxWeight: 50
    stepWeight: 10
    metrics:
      - name: request-success-rate
        thresholdRange:
          min: 99
        interval: 1m
```

### External Secrets Operator Integration

```yaml
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: external-secrets
  namespace: flux-system
spec:
  interval: 10m
  sourceRef:
    kind: GitRepository
    name: flux-system
  path: ./infrastructure/external-secrets
  prune: true
---
apiVersion: external-secrets.io/v1beta1
kind: SecretStore
metadata:
  name: aws-secretsmanager
  namespace: apps
spec:
  provider:
    aws:
      service: SecretsManager
      region: us-east-1
      auth:
        jwt:
          serviceAccountRef:
            name: external-secrets-sa
---
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: app-secrets
  namespace: apps
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: aws-secretsmanager
    kind: SecretStore
  target:
    name: app-secrets
    creationPolicy: Owner
  data:
    - secretKey: db-password
      remoteRef:
        key: prod/app/database
        property: password
```

## Troubleshooting

### Common Issues

**Issue**: Kustomization stuck in "Progressing" state

```bash
# Check Kustomization status
flux get kustomization infrastructure

# View detailed events
kubectl describe kustomization infrastructure -n flux-system

# Check logs
kubectl logs -n flux-system deploy/kustomize-controller
```

**Issue**: HelmRelease installation failed

```bash
# Get HelmRelease status
flux get helmrelease my-app -n apps

# View Helm release history
helm history my-app -n apps

# Check Helm controller logs
kubectl logs -n flux-system deploy/helm-controller
```

**Issue**: Image automation not updating manifests

```bash
# Check ImageRepository status
flux get image repository my-app

# Check ImagePolicy status
flux get image policy my-app

# View image automation logs
kubectl logs -n flux-system deploy/image-reflector-controller
kubectl logs -n flux-system deploy/image-automation-controller
```

**Issue**: Source reconciliation failures

```bash
# Check GitRepository status
flux get source git flux-system

# View source controller logs
kubectl logs -n flux-system deploy/source-controller

# Reconcile manually
flux reconcile source git flux-system
```

### Debug Mode

Enable debug logging:

```bash
# Patch controller for debug logging
kubectl patch deployment kustomize-controller \
  -n flux-system \
  --type='json' \
  -p='[{"op": "add", "path": "/spec/template/spec/containers/0/args/-", "value": "--log-level=debug"}]'
```

## Performance Optimization

### Reduce API Server Load

```yaml
spec:
  interval: 1h # Increase for stable resources
  retryInterval: 5m # Retry less frequently on errors
```

### Optimize Git Operations

```yaml
apiVersion: source.toolkit.fluxcd.io/v1
kind: GitRepository
metadata:
  name: flux-system
  namespace: flux-system
spec:
  interval: 5m
  ref:
    branch: main
  url: https://github.com/org/repo
  ignore: |
    # Reduce clone size
    *.md
    docs/
    examples/
```

### Parallel Reconciliation

Enable parallel reconciliation in controllers:

```bash
flux install \
  --components-extra=image-reflector-controller,image-automation-controller \
  --reconcile-interval=1h \
  --kustomize-concurrency=10 \
  --helm-concurrency=10
```

## Summary

Flux CD provides a powerful, declarative approach to managing Kubernetes deployments through GitOps. Key takeaways:

1. **Bootstrap once**: Use `flux bootstrap` to set up Flux in your cluster
2. **Organize thoughtfully**: Structure your repository for clarity and maintainability
3. **Layer dependencies**: Build infrastructure before applications
4. **Secure secrets**: Use SOPS or external secret managers
5. **Monitor actively**: Set up alerts and regularly check Flux status
6. **Automate carefully**: Use image automation for non-production environments first
7. **Multi-tenancy**: Leverage namespaces and RBAC for team isolation
8. **Test changes**: Validate in lower environments before production

### Key Decision Points

**Choose GitRepository vs HelmRepository:**
- GitRepository: For custom manifests, Kustomize overlays, or Helm charts in Git
- HelmRepository: For public/private Helm chart repositories

**Choose Kustomization vs HelmRelease:**
- Kustomization: For raw manifests, ConfigMaps, Secrets, Kustomize overlays
- HelmRelease: For packaged Helm charts with values customization

**Image Automation Strategy:**
- Direct commit: Development/staging environments with rapid iteration
- PR workflow: Production environments requiring review and approval
- Disabled: Mission-critical production with manual deployment gates

**Multi-Tenancy Approach:**
- Namespace isolation: Teams share cluster, separate by namespace
- Cluster isolation: Each team gets dedicated cluster(s)
- Hybrid: Core teams share, external teams isolated

**Secret Management:**
- SOPS: Git-native, age/pgp encryption, good for small teams
- External Secrets Operator: Integrate AWS Secrets Manager, Vault, GCP Secret Manager
- Sealed Secrets: Kubernetes-native, one-way encryption

By following these patterns and practices, you can build reliable, automated deployment pipelines that scale with your organization.
