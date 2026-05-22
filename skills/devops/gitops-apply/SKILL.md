---
name: gitops-apply
description: Guide proper GitOps workflow for Kubernetes changes instead of direct kubectl mutations. Identifies resources, locates/creates manifests, commits to git, and syncs via ArgoCD/Flux. Use when kubectl mutation is blocked.
version: 1.0.0
---

# GitOps Apply Skill

## Purpose

Guide users through proper GitOps workflow when they attempt to mutate Kubernetes resources with kubectl. Replaces imperative kubectl commands with declarative manifests in git, ensuring all cluster changes are auditable, reviewable, and recoverable.

## Why GitOps Over kubectl

**kubectl apply/create/delete:**

- ❌ No audit trail of who changed what
- ❌ No peer review process
- ❌ Difficult rollback (manual undo)
- ❌ Configuration drift (cluster != git)
- ❌ No disaster recovery story
- ❌ Imperative (how), not declarative (what)

**GitOps workflow:**

- ✅ Full audit trail in git log
- ✅ Peer review via pull requests
- ✅ Easy rollback via git revert
- ✅ Single source of truth (git)
- ✅ Disaster recovery via git clone
- ✅ Declarative manifests (desired state)
- ✅ Automatic sync via ArgoCD/Flux
- ✅ Drift detection and correction

## Workflow Steps

### Quick GitOps Workflow

1. **Identify Resource** - Determine K8s resource to modify
2. **Locate Manifest** - Find YAML in git (charts/, manifests/, k8s/)
3. **Edit Manifest** - Update YAML file
4. **Commit Changes** - Use conventional commits
5. **Sync via GitOps** - ArgoCD/Flux syncs automatically OR trigger manually

**For detailed step-by-step workflow with commands, verification, and examples, see `references/WORKFLOW-STEPS.md`.**

## Bootstrap Exception (ArgoCD Only)

When kubectl targets ArgoCD itself, normal GitOps cannot apply - ArgoCD cannot sync itself. Use the bootstrap workflow instead.

### Decision Tree

**ONE-OFF scenarios (skip bootstrap script):**

- Temporary debugging
- One-time migration step
- Testing that won't be repeated

**RECOVERY-NEEDED scenarios (MUST add to bootstrap):**

- New cluster initialization
- Disaster recovery procedures
- Repeatable infrastructure setup
- Changes needed on future servers

### Bootstrap Workflow

1. **Edit bootstrap scripts:**
   - `scripts/bootstrap.sh` - Run once during initial setup
   - `scripts/bootstrap-idempotent.sh` - Safe to re-run anytime

2. **Add kubectl command with idempotency pattern:**

   ```bash
   kubectl create namespace argocd 2>/dev/null || true
   kubectl apply -n argocd -f argocd/install.yaml
   kubectl wait --for=condition=available deployment/argocd-server \
     -n argocd --timeout=300s || true
   ```

3. **Commit bootstrap script changes** (conventional commit format)

4. **Execute kubectl** (now allowed after bootstrap update)

**For detailed bootstrap patterns and examples, see `references/BOOTSTRAP-WORKFLOW.md`.**

## Related Skills

- **check-history** - Review git history before making changes
