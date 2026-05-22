---
name: implementing-gitops
description: Implement GitOps continuous delivery for Kubernetes using ArgoCD or Flux. Use for automated deployments with Git as single source of truth, pull-based delivery, drift detection, multi-cluster management, and progressive rollouts.
---

# GitOps Workflows

Implement GitOps continuous delivery for Kubernetes using declarative, pull-based deployment models where Git serves as the single source of truth for infrastructure and application configuration.

## When to Use

Use GitOps workflows for:

- **Kubernetes Deployments:** Automating application and infrastructure deployments to Kubernetes clusters
- **Multi-Cluster Management:** Managing deployments across development, staging, production, and edge clusters
- **Continuous Delivery:** Implementing pull-based CD pipelines with automated reconciliation
- **Drift Detection:** Automatically detecting and correcting configuration drift from desired state
- **Audit Requirements:** Maintaining complete audit trails via Git commits for compliance
- **Progressive Delivery:** Implementing canary, blue-green, or rolling deployment strategies
- **Disaster Recovery:** Enabling rapid cluster recovery with GitOps bootstrap processes

Trigger keywords: "deploy to Kubernetes", "ArgoCD setup", "Flux bootstrap", "GitOps pipeline", "environment promotion", "multi-cluster deployment", "automated reconciliation"

## Core GitOps Principles

### 1. Git as Single Source of Truth

All system configuration stored in Git repositories. No manual kubectl apply or cluster modifications. Declarative manifests (YAML) for all Kubernetes resources, environment-specific overlays, infrastructure configuration, and application deployments.

### 2. Pull-Based Deployment

Operators running inside clusters pull changes from Git and apply them automatically. Benefits include no cluster credentials in CI/CD pipelines, support for air-gapped environments, self-healing through continuous reconciliation, and simplified CI/CD.

### 3. Automated Reconciliation

GitOps operators continuously compare actual cluster state with desired state in Git and reconcile differences through a continuous loop: watch Git, compare live state, apply differences, report status, repeat.

### 4. Declarative Configuration

Use declarative Kubernetes manifests (not imperative scripts) to define desired state.

## Tool Selection

### ArgoCD vs Flux

| Decision Factor | Choose ArgoCD | Choose Flux |
|----------------|---------------|-------------|
| **Team Preference** | Visual management with web UI | CLI/API-first workflows |
| **Learning Curve** | Easier onboarding with UI | Steeper but more flexible |
| **Architecture** | Monolithic, stateful controller | Modular, stateless controllers |
| **Multi-Tenancy** | Built-in RBAC and projects | Kubernetes-native RBAC |
| **Resource Usage** | Higher (includes UI components) | Lower (minimal controllers) |
| **Best For** | Transitioning to GitOps | Platform engineering |

**Hybrid Approach:** Some teams use Flux for infrastructure and ArgoCD for applications.

For ArgoCD implementation patterns, see references/argocd-patterns.md
For Flux implementation patterns, see references/flux-patterns.md
For Kustomize overlay patterns, see references/kustomize-overlays.md

## Quick Start

### ArgoCD Installation

```bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

**Basic Application:**
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: myapp
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/org/repo.git
    targetRevision: HEAD
    path: k8s/overlays/prod
  destination:
    server: https://kubernetes.default.svc
    namespace: myapp
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

### Flux Bootstrap

```bash
flux bootstrap github \
  --owner=myorg \
  --repository=fleet-infra \
  --branch=main \
  --path=clusters/production
```

**Basic Kustomization:**
```yaml
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: myapp
  namespace: flux-system
spec:
  interval: 10m
  path: "./k8s/prod"
  prune: true
  sourceRef:
    kind: GitRepository
    name: myapp
```

For complete examples, see examples/argocd/ and examples/flux/

## Environment Promotion

**Branch-Based Strategy:** dev branch → staging branch → main branch (prod)
**Kustomize-Based Strategy:** k8s/base/ → k8s/overlays/{dev,staging,prod}/

**Promotion Process:**
1. Merge code changes to main branch
2. CI builds container image with tag
3. Update image tag in environment overlay (Git commit)
4. GitOps operator detects change and deploys
5. Test in environment
6. Promote to next environment by updating Git

For multi-environment ApplicationSet patterns, see references/argocd-patterns.md

## Multi-Cluster Management

**ArgoCD:** Register external clusters with argocd CLI, use ApplicationSets to generate Applications per cluster, manage from single ArgoCD instance.

**Flux:** Bootstrap Flux per cluster, use same Git repo with cluster-specific paths, configure remote clusters via kubeConfig secrets.

For detailed multi-cluster patterns, see references/multi-cluster.md

## Progressive Delivery

**Canary Deployments:** Gradually shift traffic to new version, monitor metrics during rollout, automated rollback on failures.

**Blue-Green Deployments:** Deploy new version alongside old, switch traffic atomically, instant rollback if issues detected.

**ArgoCD:** Use Argo Rollouts for progressive delivery
**Flux:** Integrate Flagger for automated canary analysis

For progressive delivery strategies and Argo Rollouts examples, see references/progressive-delivery.md

## Secret Management

GitOps requires storing configuration in Git, but secrets must be protected.

| Tool | Approach | Security | Complexity |
|------|----------|----------|------------|
| **Sealed Secrets** | Encrypt secrets for Git | Medium | Low |
| **SOPS** | Encrypt files with KMS | High | Medium |
| **External Secrets** | Reference external vaults | High | Medium |
| **HashiCorp Vault** | Central secret management | Very High | High |

For secret management integration patterns, see references/secret-management.md

## Drift Detection and Remediation

GitOps operators continuously monitor for drift between Git (desired state) and cluster (actual state).

**ArgoCD Automatic Self-Healing:**
```yaml
syncPolicy:
  automated:
    prune: true      # Remove resources not in Git
    selfHeal: true   # Revert manual changes
```

**Flux Automatic Reconciliation:**
```yaml
spec:
  interval: 10m    # Check every 10 minutes
  prune: true      # Remove resources not in Git
  force: true      # Force apply on conflicts
```

**Manual Operations:**
```bash
# ArgoCD
argocd app get myapp           # View sync status
argocd app diff myapp          # Show differences
argocd app sync myapp          # Manually trigger sync

# Flux
flux get kustomizations              # View sync status
flux reconcile kustomization myapp   # Force immediate sync
```

For drift detection strategies and troubleshooting, see references/drift-remediation.md

## Sync Hooks and Lifecycle

Execute operations before/after syncs using hooks.

**PreSync Hook (Database Migration):**
```yaml
apiVersion: batch/v1
kind: Job
metadata:
  annotations:
    argocd.argoproj.io/hook: PreSync
    argocd.argoproj.io/hook-delete-policy: HookSucceeded
```

**PostSync Hook (Smoke Test):**
```yaml
apiVersion: batch/v1
kind: Job
metadata:
  annotations:
    argocd.argoproj.io/hook: PostSync
```

For complete sync hook examples, see examples/argocd/sync-hooks.yaml

## Monitoring and Observability

### Key Metrics

- **Sync Status:** OutOfSync, Synced, Unknown
- **Sync Frequency:** How often reconciliation occurs
- **Drift Detection:** Time to detect configuration drift
- **Sync Duration:** Time to apply changes
- **Failure Rate:** Failed syncs and causes

**ArgoCD Metrics:** Exposed at `/metrics` endpoint (`argocd_app_sync_total`, `argocd_app_info`)
**Flux Metrics:** From controllers (`gotk_reconcile_condition`, `gotk_reconcile_duration_seconds`)

## Troubleshooting

### Common Issues

**Sync Stuck/OutOfSync:**
- Check Git repository accessibility
- Verify manifests are valid YAML
- Review sync logs for errors
- Check resource finalizers

**Self-Heal Not Working:**
- Verify selfHeal enabled in syncPolicy
- Check operator has write permissions
- Review resource ownership labels

**Secrets Not Decrypting:**
- Verify SOPS/ESO controllers installed
- Check KMS/Vault credentials
- Review encryption key configuration

## CLI Quick Reference

### ArgoCD Commands

```bash
argocd app create <name>          # Create application
argocd app get <name>              # View status
argocd app sync <name>             # Trigger sync
argocd app diff <name>             # Show drift
argocd app list                    # List all applications
```

### Flux Commands

```bash
flux create source git <name>      # Create Git source
flux create kustomization <name>   # Create kustomization
flux get all                       # View all resources
flux reconcile <kind> <name>       # Force reconciliation
flux logs                          # View controller logs
```

### Kustomize Commands

```bash
kustomize build k8s/overlays/prod  # Preview generated YAML
kubectl apply -k k8s/overlays/prod # Apply directly
kubectl diff -k k8s/overlays/prod  # Show differences
```

## Installation Scripts

Use the provided installation scripts for quick setup:

```bash
# Install ArgoCD
./scripts/install-argocd.sh

# Bootstrap Flux
export GITHUB_TOKEN=<token>
export GITHUB_OWNER=<org>
export GITHUB_REPO=fleet-infra
./scripts/install-flux.sh

# Check for drift
./scripts/check-drift.sh

# Promote environment
./scripts/promote-env.sh dev staging
```

## Example Files

Complete working examples provided in examples/ directory:

**ArgoCD Examples:**
- examples/argocd/application.yaml - Basic Application
- examples/argocd/applicationset.yaml - Multi-environment ApplicationSet
- examples/argocd/progressive-rollout.yaml - Progressive rollout strategy
- examples/argocd/sync-hooks.yaml - PreSync/PostSync hooks

**Flux Examples:**
- examples/flux/gitrepository.yaml - Git source configuration
- examples/flux/kustomization.yaml - Kustomization controller
- examples/flux/helmrelease.yaml - Helm release management
- examples/flux/ocirepository.yaml - OCI artifact source

**Kustomize Examples:**
- examples/kustomize/base/ - Base configuration
- examples/kustomize/overlays/{dev,staging,prod}/ - Environment overlays

**Rollout Examples:**
- examples/rollouts/canary.yaml - Canary deployment with Argo Rollouts
- examples/rollouts/blue-green.yaml - Blue-green deployment strategy

## Related Skills

- **kubernetes-operations:** Kubernetes fundamentals and resource management
- **infrastructure-as-code:** Provisioning clusters that GitOps deploys to
- **building-ci-pipelines:** CI builds images, GitOps deploys them
- **secret-management:** Vault/ESO integration with GitOps
- **deploying-applications:** GitOps as the deployment mechanism

## Summary

GitOps provides automated, declarative continuous delivery for Kubernetes with Git as the single source of truth. Choose ArgoCD for UI-driven workflows or Flux for CLI/API-first approaches. Implement automated reconciliation, drift detection, and progressive delivery for reliable deployments at scale. Integrate secret management, multi-cluster orchestration, and disaster recovery for production-grade GitOps workflows.
