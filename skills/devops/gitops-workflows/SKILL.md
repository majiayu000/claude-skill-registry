---
name: gitops-workflows
description: GitOps deployment workflows with ArgoCD and Flux. Use for setting up
  GitOps (ArgoCD 3.x, Flux 2.7), designing repository structures (monorepo/polyrepo,
  app-of-apps), multi-cluster deployments (Applica
---

---
name: gitops-workflows
description: GitOps deployment workflows with ArgoCD and Flux. Use for setting up GitOps (ArgoCD 3.x, Flux 2.7), designing repository structures (monorepo/polyrepo, app-of-apps), multi-cluster deployments (ApplicationSets, hub-spoke), secrets management (SOPS+age, Sealed Secrets, External Secrets Operator), progressive delivery (Argo Rollouts, Flagger), troubleshooting sync issues, and OCI artifact management. Covers latest 2024-2025 features: ArgoCD annotation-based tracking, fine-grained RBAC, Flux OCI artifacts GA, image automation, source-watcher.
---

# GitOps Workflows

## Overview

This skill provides comprehensive GitOps workflows for continuous deployment to Kubernetes using ArgoCD 3.x and Flux 2.7+.

**When to use this skill**:
- Setting up GitOps from scratch (ArgoCD or Flux)
- Designing Git repository structures
- Multi-cluster deployments
- Troubleshooting sync/reconciliation issues
- Implementing secrets management
- Progressive delivery (canary, blue-green)
- Migrating between GitOps tools

---

## Core Workflow: GitOps Implementation

Use this decision tree to determine your starting point:

```
Do you have GitOps installed?
├─ NO → Need to choose a tool
│   └─ Want UI + easy onboarding? → ArgoCD (Workflow 1)
│   └─ Want modularity + platform engineering? → Flux (Workflow 2)
└─ YES → What's your goal?
    ├─ Sync issues / troubleshooting → Workflow 7
    ├─ Multi-cluster deployment → Workflow 4
    ├─ Secrets management → Workflow 5
    ├─ Progressive delivery → Workflow 6
    ├─ Repository structure → Workflow 3
    └─ Tool comparison → Read references/argocd_vs_flux.md
```

---

## 1. Initial Setup: ArgoCD 3.x

**Latest Version**: v3.1.9 (stable), v3.2.0-rc4 (October 2025)

### Quick Install

```bash
# Create namespace
kubectl create namespace argocd

# Install ArgoCD 3.x
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/v3.1.9/manifests/install.yaml

# Get admin password
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d

# Port forward to access UI
kubectl port-forward svc/argocd-server -n argocd 8080:443
# Access: https://localhost:8080
```

**→ Template**: [assets/argocd/install-argocd-3.x.yaml](assets/argocd/install-argocd-3.x.yaml)

### ArgoCD 3.x New Features

**Breaking Changes**:
- ✅ Annotation-based tracking (default, was labels)
- ✅ RBAC logs enforcement enabled
- ✅ Legacy metrics removed

**New Features**:
- ✅ Fine-grained RBAC (per-resource permissions)
- ✅ Better defaults (resource exclusions for performance)
- ✅ Secrets operators endorsement

### Deploy Your First Application

```bash
# CLI method
argocd app create guestbook \
  --repo https://github.com/argoproj/argocd-example-apps.git \
  --path guestbook \
  --dest-server https://kubernetes.default.svc \
  --dest-namespace default

# Sync application
argocd app sync guestbook
```

### Health Check

```bash
# Check application health
python3 scripts/check_argocd_health.py \
  --server https://argocd.example.com \
  --token $ARGOCD_TOKEN
```

**→ Script**: [scripts/check_argocd_health.py](scripts/check_argocd_health.py)

---

## 2. Initial Setup: Flux 2.7

**Latest Version**: v2.7.1 (October 2025)

### Quick Install

```bash
# Install Flux CLI
brew install fluxcd/tap/flux  # macOS
# or: curl -s https://fluxcd.io/install.sh | sudo bash

# Check prerequisites
flux check --pre

# Bootstrap Flux (GitHub)
export GITHUB_TOKEN=<your-token>
flux bootstrap github \
  --owner=<org> \
  --repository=fleet-infra \
  --branch=main \
  --path=clusters/production \
  --personal

# Enable source-watcher (Flux 2.7+)
flux install --components-extra=source-watcher
```

**→ Template**: [assets/flux/flux-bootstrap-github.sh](assets/flux/flux-bootstrap-github.sh)

### Flux 2.7 New Features

- ✅ Image automation GA
- ✅ ExternalArtifact and ArtifactGenerator APIs
- ✅ Source-watcher component for better performance
- ✅ OpenTelemetry tracing support
- ✅ CEL expressions for readiness evaluation

### Deploy Your First Application

```yaml
# gitrepository.yaml
apiVersion: source.toolkit.fluxcd.io/v1
kind: GitRepository
metadata:
  name: podinfo
  namespace: flux-system
spec:
  interval: 1m
  url: https://github.com/stefanprodan/podinfo
  ref:
    branch: master
---
# kustomization.yaml
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: podinfo
  namespace: flux-system
spec:
  interval: 5m
  path: "./kustomize"
  prune: true
  sourceRef:
    kind: GitRepository
    name: podinfo
```

### Health Check

```bash
# Check Flux health
python3 scripts/check_flux_health.py --namespace flux-system
```

**→ Script**: [scripts/check_flux_health.py](scripts/check_flux_health.py)

---

## 3. Repository Structure Design

**Decision: Monorepo or Polyrepo?**

### Monorepo Pattern

**Best for**: Startups, small teams (< 20 apps), single team

```
gitops-repo/
├── apps/
│   ├── frontend/
│   ├── backend/
│   └── database/
├── infrastructure/
│   ├── ingress/
│   ├── monitoring/
│   └── secrets/
└── clusters/
    ├── dev/
    ├── staging/
    └── production/
```

### Polyrepo Pattern

**Best for**: Large orgs, multiple teams, clear boundaries

```
infrastructure-repo/     (Platform team)
app-team-1-repo/        (Team 1)
app-team-2-repo/        (Team 2)
```

### Environment Structure (Kustomize)

```
app/
├── base/
│   ├── deployment.yaml
│   ├── service.yaml
│   └── kustomization.yaml
└── overlays/
    ├── dev/
    │   ├── kustomization.yaml
    │   └── replica-patch.yaml
    ├── staging/
    └── production/
```

**→ Reference**: [references/repo_patterns.md](references/repo_patterns.md)

### Validate Repository Structure

```bash
python3 scripts/validate_gitops_repo.py /path/to/repo
```

**→ Script**: [scripts/validate_gitops_repo.py](scripts/validate_gitops_repo.py)

---

## 4. Multi-Cluster Deployments

### ArgoCD ApplicationSets

**Cluster Generator** (deploy to all clusters):

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
        repoURL: https://github.com/org/apps
        path: myapp
      destination:
        server: '{{server}}'
```

**→ Template**: [assets/applicationsets/cluster-generator.yaml](assets/applicationsets/cluster-generator.yaml)

**Performance Benefit**: 83% faster deployments (30min → 5min)

### Generate ApplicationSets

```bash
# Cluster generator
python3 scripts/applicationset_generator.py cluster \
  --name my-apps \
  --repo-url https://github.com/org/repo \
  --output appset.yaml

# Matrix generator (cluster x apps)
python3 scripts/applicationset_generator.py matrix \
  --name my-apps \
  --cluster-label production \
  --directories app1,app2,app3 \
  --output appset.yaml
```

**→ Script**: [scripts/applicationset_generator.py](scripts/applicationset_generator.py)

### Flux Multi-Cluster

**Hub-and-Spoke**: Management cluster manages all clusters

```bash
# Bootstrap each cluster
flux bootstrap github --context prod-cluster --path clusters/production
flux bootstrap github --context staging-cluster --path clusters/staging
```

**→ Reference**: [references/multi_cluster.md](references/multi_cluster.md)

---

## 5. Secrets Management

**Never commit plain secrets to Git.** Choose a solution:

### Decision Matrix

| Solution | Complexity | Best For | 2025 Trend |
|----------|-----------|----------|------------|
| **SOPS + age** | Medium | Git-centric, flexible | ↗️ Preferred |
| **External Secrets Operator** | Medium | Cloud-native, dynamic | ↗️ Growing |
| **Sealed Secrets** | Low | Simple, GitOps-first | → Stable |

### Option 1: SOPS + age (Recommended 2025)

**Setup**:
```bash
# Generate age key
age-keygen -o key.txt
# Public key: age1...

# Create .sops.yaml
cat <<EOF > .sops.yaml
creation_rules:
  - path_regex: .*.yaml
    encrypted_regex: ^(data|stringData)$
    age: age1ql3z7hjy54pw3hyww5ayyfg7zqgvc7w3j2elw8zmrj2kg5sfn9aqmcac8p
EOF

# Encrypt secret
kubectl create secret generic my-secret --dry-run=client -o yaml \
  --from-literal=password=supersecret > secret.yaml
sops -e secret.yaml > secret.enc.yaml

# Commit encrypted version
git add secret.enc.yaml .sops.yaml
```

**→ Template**: [assets/secrets/sops-age-config.yaml](assets/secrets/sops-age-config.yaml)

### Option 2: External Secrets Operator (v0.20+)

**Best for**: Cloud-native apps, dynamic secrets, automatic rotation

### Option 3: Sealed Secrets

**Best for**: Simple setup, static secrets, no external dependencies

**→ Reference**: [references/secret_management.md](references/secret_management.md)

### Audit Secrets

```bash
python3 scripts/secret_audit.py /path/to/repo
```

**→ Script**: [scripts/secret_audit.py](scripts/secret_audit.py)

---

## 6. Progressive Delivery

### Argo Rollouts (with ArgoCD)

**Canary Deployment**:
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: my-app
spec:
  strategy:
    canary:
      steps:
      - setWeight: 20
      - pause: {duration: 2m}
      - setWeight: 50
      - pause: {duration: 2m}
      - setWeight: 100
```

**→ Template**: [assets/progressive-delivery/argo-rollouts-canary.yaml](assets/progressive-delivery/argo-rollouts-canary.yaml)

### Flagger (with Flux)

**Canary with Metrics Analysis**:
```yaml
apiVersion: flagger.app/v1beta1
kind: Canary
metadata:
  name: my-app
spec:
  analysis:
    interval: 1m
    threshold: 5
    maxWeight: 50
    stepWeight: 10
    metrics:
    - name: request-success-rate
      thresholdRange:
        min: 99
```

**→ Reference**: [references/progressive_delivery.md](references/progressive_delivery.md)

---

## 7. Troubleshooting

### Common Issues

**ArgoCD OutOfSync**:
```bash
# Check differences
argocd app diff my-app

# Sync application
argocd app sync my-app

# Check health
python3 scripts/check_argocd_health.py --server https://argocd.example.com --token $TOKEN
```

**Flux Not Reconciling**:
```bash
# Check resources
flux get all

# Check specific kustomization
flux get kustomizations
kubectl describe kustomization my-app -n flux-system

# Force reconcile
flux reconcile kustomization my-app
```

**Detect Drift**:
```bash
# ArgoCD drift detection
python3 scripts/sync_drift_detector.py --argocd --app my-app

# Flux drift detection
python3 scripts/sync_drift_detector.py --flux
```

**→ Script**: [scripts/sync_drift_detector.py](scripts/sync_drift_detector.py)

**→ Reference**: [references/troubleshooting.md](references/troubleshooting.md)

---

## 8. OCI Artifacts (Flux 2.6+)

**GA Status**: Flux v2.6 (June 2025)

### Use OCIRepository for Helm Charts

```yaml
apiVersion: source.toolkit.fluxcd.io/v1beta2
kind: OCIRepository
metadata:
  name: podinfo-oci
spec:
  interval: 5m
  url: oci://ghcr.io/stefanprodan/charts/podinfo
  ref:
    semver: ">=6.0.0"
  verify:
    provider: cosign
```

**→ Template**: [assets/flux/oci-helmrelease.yaml](assets/flux/oci-helmrelease.yaml)

### Verify OCI Artifacts

```bash
python3 scripts/oci_artifact_checker.py \
  --verify ghcr.io/org/app:v1.0.0 \
  --provider cosign
```

**→ Script**: [scripts/oci_artifact_checker.py](scripts/oci_artifact_checker.py)

**→ Reference**: [references/oci_artifacts.md](references/oci_artifacts.md)

---

## Quick Reference Commands

### ArgoCD

```bash
# List applications
argocd app list

# Get application details
argocd app get <app-name>

# Sync application
argocd app sync <app-name>

# View diff
argocd app diff <app-name>

# Delete application
argocd app delete <app-name>
```

### Flux

```bash
# Check Flux status
flux check

# Get all resources
flux get all

# Reconcile immediately
flux reconcile source git <name>
flux reconcile kustomization <name>

# Suspend/Resume
flux suspend kustomization <name>
flux resume kustomization <name>

# Export resources
flux export source git --all > sources.yaml
```

---

## Resources Summary

### Scripts (automation and diagnostics)
- `check_argocd_health.py` - Diagnose ArgoCD sync issues (3.x compatible)
- `check_flux_health.py` - Diagnose Flux reconciliation issues (2.7+ compatible)
- `validate_gitops_repo.py` - Validate repository structure and manifests
- `sync_drift_detector.py` - Detect drift between Git and cluster
- `secret_audit.py` - Audit secrets management (SOPS, Sealed Secrets, ESO)
- `applicationset_generator.py` - Generate ApplicationSet manifests
- `promotion_validator.py` - Validate environment promotion workflows
- `oci_artifact_checker.py` - Validate Flux OCI artifacts and verify signatures

### References (deep-dive documentation)
- `argocd_vs_flux.md` - Comprehensive comparison (2024-2025), decision matrix
- `repo_patterns.md` - Monorepo vs polyrepo, app-of-apps, environment structures
- `secret_management.md` - SOPS+age, Sealed Secrets, ESO (2025 best practices)
- `progressive_delivery.md` - Argo Rollouts, Flagger, canary/blue-green patterns
- `multi_cluster.md` - ApplicationSets, Flux multi-tenancy, hub-spoke patterns
- `troubleshooting.md` - Common sync issues, debugging commands
- `best_practices.md` - CNCF GitOps principles, security, 2025 recommendations
- `oci_artifacts.md` - Flux OCI artifacts (GA v2.6), signature verification

### Templates (production-ready configurations)
- `argocd/install-argocd-3.x.yaml` - ArgoCD 3.x installation with best practices
- `applicationsets/cluster-generator.yaml` - Multi-cluster ApplicationSet example
- `flux/flux-bootstrap-github.sh` - Flux 2.7 bootstrap script
- `flux/oci-helmrelease.yaml` - OCI artifact + HelmRelease example
- `secrets/sops-age-config.yaml` - SOPS + age configuration
- `progressive-delivery/argo-rollouts-canary.yaml` - Canary deployment with analysis
