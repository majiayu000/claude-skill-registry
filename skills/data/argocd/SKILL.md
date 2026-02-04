---
name: argocd
description: GitOps continuous delivery for Kubernetes with ArgoCD. Use when creating/managing ArgoCD Applications, ApplicationSets, App of Apps patterns, Helm/Kustomize deployments, sync configurations, RBAC/projects setup, notifications, health checks, or private repository configuration.
---

# ArgoCD

Declarative GitOps continuous delivery for Kubernetes. ArgoCD continuously monitors Git repositories and automatically syncs application state to match desired configuration.

## Quick Start

**Install ArgoCD:**
```bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

**Access UI:**
```bash
kubectl port-forward svc/argocd-server -n argocd 8080:443
# Get initial admin password
argocd admin initial-password -n argocd
```

**CLI Login:**
```bash
argocd login localhost:8080 --insecure
```

## Core Concepts

| Concept | Description |
|---------|-------------|
| **Application** | Kubernetes resource tracking a Git repo path to a cluster/namespace |
| **AppProject** | Logical grouping with source/destination restrictions and RBAC |
| **ApplicationSet** | Template for generating multiple Applications from generators |
| **Sync** | Process of applying Git manifests to cluster |
| **Health** | Status assessment of deployed resources |

## Task Reference

### Application Management
- Create, sync, delete Applications → [references/applications.md](references/applications.md)
- App of Apps pattern → [references/applications.md](references/applications.md)

### Multi-Cluster & Templating
- ApplicationSets with generators → [references/applicationsets.md](references/applicationsets.md)
- List, Cluster, Git, Matrix generators → [references/applicationsets.md](references/applicationsets.md)

### Manifest Tools
- Helm charts, values, OCI registries → [references/helm.md](references/helm.md)
- Kustomize overlays, patches → [references/kustomize.md](references/kustomize.md)

### Sync Configuration
- Sync waves, hooks, phases → [references/sync-options.md](references/sync-options.md)
- Prune, replace, server-side apply → [references/sync-options.md](references/sync-options.md)

### Operations & Admin
- RBAC policies, roles → [references/operations.md](references/operations.md)
- Projects, health checks, notifications → [references/operations.md](references/operations.md)

### Repository Setup
- Private repos, SSH, HTTPS, GitHub App → [references/repositories.md](references/repositories.md)
- Credential templates, certificates → [references/repositories.md](references/repositories.md)

### Troubleshooting
- Common issues, FAQ → [references/troubleshooting.md](references/troubleshooting.md)

## Common CLI Commands

```bash
# Application management
argocd app create <name> --repo <url> --path <path> --dest-server https://kubernetes.default.svc --dest-namespace <ns>
argocd app sync <name>
argocd app get <name>
argocd app delete <name>
argocd app list

# Cluster management
argocd cluster add <context-name>
argocd cluster list

# Repository management
argocd repo add <url> [--ssh-private-key-path | --username/--password]
argocd repo list

# Project management
argocd proj create <name> -d <server>,<namespace> -s <repo-url>
argocd proj list
```

## Minimal Application Example

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
    path: manifests
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

## Official Documentation
- [ArgoCD Docs](https://argo-cd.readthedocs.io/en/stable/)
- [Application Spec](https://argo-cd.readthedocs.io/en/stable/user-guide/application-specification/)
- [CLI Reference](https://argo-cd.readthedocs.io/en/stable/user-guide/commands/argocd/)
