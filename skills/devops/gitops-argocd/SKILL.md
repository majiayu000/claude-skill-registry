---
name: GitOps with ArgoCD
description: Implementing GitOps workflows for Kubernetes deployments using ArgoCD.
---

# GitOps with ArgoCD

## Overview

ArgoCD implements GitOps for Kubernetes by continuously reconciling cluster
state to the desired state defined in Git. It provides visibility, drift
detection, and controlled deployments.

## Table of Contents

1. [GitOps Principles](#gitops-principles)
2. [ArgoCD Architecture](#argocd-architecture)
3. [Installation and Setup](#installation-and-setup)
4. [Application CRD](#application-crd)
5. [Sync Strategies](#sync-strategies)
6. [Application Sets](#application-sets)
7. [Sync Waves and Hooks](#sync-waves-and-hooks)
8. [Health Checks](#health-checks)
9. [Resource Hooks](#resource-hooks)
10. [Secrets Management](#secrets-management)
11. [Multi-Tenancy and RBAC](#multi-tenancy-and-rbac)
12. [SSO Integration](#sso-integration)
13. [Notifications](#notifications)
14. [ArgoCD vs Flux](#argocd-vs-flux)
15. [CI/CD Integration](#cicd-integration)
16. [Rollback Strategies](#rollback-strategies)
17. [Monitoring](#monitoring)
18. [Disaster Recovery](#disaster-recovery)
19. [Best Practices](#best-practices)

---

## GitOps Principles

- Git is the single source of truth.
- Declarative configuration for infrastructure and apps.
- Automated reconciliation.
- Auditable change history.

## ArgoCD Architecture

- **Application Controller**: Reconciles desired and live state.
- **API Server**: UI/CLI access.
- **Repository Server**: Fetches and renders manifests.
- **Dex**: Optional SSO provider.

## Installation and Setup

High-level steps:
- Install ArgoCD in a dedicated namespace.
- Configure repository access (SSH keys or tokens).
- Create Applications for target workloads.

## Application CRD

Defines source repo, path, destination cluster/namespace, and sync policy.

Example skeleton:
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: payments-service
spec:
  source:
    repoURL: https://github.com/org/repo
    path: apps/payments
    targetRevision: main
  destination:
    server: https://kubernetes.default.svc
    namespace: payments
  syncPolicy:
    automated: {}
```

## Sync Strategies

- **Automated**: Auto-sync on changes.
- **Manual**: Operator-initiated sync.
- **Self-heal**: Reverts drift.
- **Prune**: Removes orphaned resources.

## Application Sets

Use ApplicationSets for:
- Multi-cluster deployment
- Monorepo with multiple apps
- Template-based app generation

## Sync Waves and Hooks

Use sync waves to order resources (e.g., DB before app).
Use hooks for migrations or setup tasks.

## Health Checks

Configure custom health checks for CRDs and critical services to avoid false
positives in deployment status.

## Resource Hooks

Hooks:
- **PreSync**: migrations or backups
- **Sync**: data initialization
- **PostSync**: smoke tests

## Secrets Management

Options:
- External secrets controller
- Sealed Secrets
- SOPS with KMS

Avoid storing plaintext secrets in Git.

## Multi-Tenancy and RBAC

- Use projects to isolate teams.
- Restrict repos, clusters, and namespaces per project.
- Use ArgoCD RBAC for fine-grained access.

## SSO Integration

Configure Dex or external OIDC provider (Okta, Azure AD).

## Notifications

Use ArgoCD Notifications for sync status and drift alerts:
- Slack
- Email
- Webhooks

## ArgoCD vs Flux

- **ArgoCD**: UI-driven, strong app concept.
- **Flux**: GitOps toolkit, more modular.

Pick based on operator preferences and ecosystem fit.

## CI/CD Integration

Common pattern:
- CI builds artifacts and updates Git (image tags).
- ArgoCD pulls changes.
- Promotion via PRs and branch policies.

## Rollback Strategies

- Roll back Git commit.
- Use previous image tags.
- Pause automated sync for investigation.

## Monitoring

- Monitor ArgoCD controller health.
- Track sync status and drift.
- Alert on repeated sync failures.

## Disaster Recovery

Backup:
- Application CRDs
- Projects and RBAC
- Repository credentials

Restore ArgoCD in a clean cluster and reapply configs.

## Best Practices

- Keep manifests small and composable.
- Use separate repos or directories per environment.
- Enforce review on Git changes.
- Restrict write access to production branches.

## Related Skills
- `15-devops-infrastructure/kubernetes-helm`
- `15-devops-infrastructure/github-actions`
- `15-devops-infrastructure/terraform-iac`
