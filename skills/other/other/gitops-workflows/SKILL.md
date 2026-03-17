---
name: gitops-workflows
description: GitOps workflows and patterns using ArgoCD and Flux for declarative Kubernetes deployments. Use when implementing CI/CD for Kubernetes, managing multi-environment deployments, or adopting declarative infrastructure practices.
---

# GitOps Workflows

Expert guidance for implementing production-grade GitOps workflows using ArgoCD and Flux CD, covering declarative deployment patterns, progressive delivery strategies, multi-environment management, and secure secret handling for Kubernetes infrastructure.

## When to Use This Skill

- Implementing GitOps principles for Kubernetes deployments
- Automating continuous delivery from Git repositories
- Managing multi-cluster or multi-environment deployments
- Implementing progressive delivery (canary, blue-green) strategies
- Configuring automated sync policies and reconciliation
- Managing secrets securely in GitOps workflows
- Setting up environment promotion workflows
- Designing repository structures for GitOps (monorepo vs multi-repo)
- Implementing rollback strategies and disaster recovery
- Establishing compliance and audit trails through Git

## Core Concepts

### The Four Principles

1. **Declarative**: Entire system state expressed in code
2. **Versioned**: Canonical state stored in Git with full history
3. **Pulled Automatically**: Agents pull desired state (no push to prod)
4. **Continuously Reconciled**: Automatic drift detection and correction

### Key Benefits

- Complete deployment history and audit trail
- Fast rollback via Git operations
- Enhanced security (no cluster credentials in CI)
- Self-healing infrastructure
- Multi-cluster consistency
- Familiar Git workflows for infrastructure changes

## Quick Reference

| Task | Load reference |
| --- | --- |
| GitOps principles and benefits | `skills/gitops-workflows/references/core-principles.md` |
| Repository structure patterns (monorepo, multi-repo, branches) | `skills/gitops-workflows/references/repository-structures.md` |
| ArgoCD setup, Applications, ApplicationSets | `skills/gitops-workflows/references/argocd-implementation.md` |
| Flux bootstrap, sources, Kustomizations, HelmReleases | `skills/gitops-workflows/references/flux-implementation.md` |
| Environment promotion strategies | `skills/gitops-workflows/references/environment-promotion.md` |
| Secret management (Sealed Secrets, ESO, SOPS) | `skills/gitops-workflows/references/secret-management.md` |
| Progressive delivery (canary, blue-green) | `skills/gitops-workflows/references/progressive-delivery.md` |
| Rollback strategies and disaster recovery | `skills/gitops-workflows/references/rollback-strategies.md` |
| Best practices and patterns | `skills/gitops-workflows/references/best-practices.md` |

## Workflow Steps

### 1. Choose Repository Structure

**Decision factors:**
- Team size and organization structure
- Application coupling and dependencies
- Access control requirements
- Deployment frequency and independence

**Options:**
- **Monorepo**: Single repo, unified platform teams, shared infrastructure
- **Multi-repo**: Separate repos per app/team, independent release cycles
- **Environment branches**: Git flow style, simple mental model

### 2. Select GitOps Tool

**ArgoCD:**
- UI-focused with visual application management
- App of Apps pattern for hierarchical deployments
- ApplicationSets for multi-cluster deployments
- Strong RBAC and project isolation

**Flux:**
- CLI-first, GitOps Toolkit architecture
- Native Kustomize and Helm support
- Automated image updates
- Lighter weight, cloud-native

### 3. Configure Secret Management

**Never commit unencrypted secrets to Git**

**Options:**
- **Sealed Secrets**: Client-side encryption, simple workflow
- **External Secrets Operator**: Sync from external secret stores (AWS, Vault, GCP)
- **SOPS**: File-based encryption with age or cloud KMS

### 4. Implement Sync Policies

**Non-production environments:**
- Automated sync with `prune` and `selfHeal`
- Frequent reconciliation (1-5 minutes)
- Fail fast with immediate feedback

**Production environments:**
- Manual approval or gated automation
- Health checks and wait conditions
- Progressive delivery for high-risk changes
- Sync windows for maintenance periods

### 5. Set Up Environment Promotion

**Promotion strategies:**
- **Git-based**: Tag or branch promotion with Git operations
- **Kustomize overlays**: Update image tags in environment-specific overlays
- **Automated updates**: Flux ImageUpdateAutomation for semver policies

### 6. Configure Progressive Delivery

**For high-risk changes:**
- **ArgoCD Rollouts**: Canary deployments with automated analysis
- **Flagger**: Progressive delivery with metric-based promotion
- Traffic shifting with Istio or other service mesh
- Automated rollback on failed analysis

### 7. Establish Rollback Procedures

**Git rollback:**
- `git revert` for specific commits
- Tag-based rollback by updating targetRevision
- Fast and declarative

**Tool-specific:**
- ArgoCD: `argocd app rollback` with revision history
- Flux: Suspend automation, manual rollback, resume

## Common Mistakes

1. **Committing unencrypted secrets** - Always use secret management solution
2. **No automated sync in non-prod** - Slows development feedback
3. **Automated sync in production without gates** - High risk of breaking changes
4. **Ignoring drift detection** - Manual changes should be reconciled or alerted
5. **No health checks** - Sync succeeds but app is unhealthy
6. **Missing dependency ordering** - Apps deploy before infrastructure ready
7. **No rollback testing** - Discover issues during actual incidents
8. **Inconsistent environments** - Staging differs too much from production
9. **No promotion testing** - Manual errors during environment promotion
10. **Weak RBAC** - Too many permissions for GitOps service accounts

## Resources

- **OpenGitOps**: https://opengitops.dev/
- **ArgoCD Documentation**: https://argo-cd.readthedocs.io/
- **Flux Documentation**: https://fluxcd.io/docs/
- **ArgoCD Rollouts**: https://argoproj.github.io/argo-rollouts/
- **Flagger**: https://docs.flagger.app/
- **External Secrets Operator**: https://external-secrets.io/
- **Sealed Secrets**: https://github.com/bitnami-labs/sealed-secrets
- **SOPS**: https://github.com/mozilla/sops
