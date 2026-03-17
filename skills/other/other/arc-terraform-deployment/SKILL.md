---
name: arc-terraform-deployment
description: Deploy ARC (Actions Runner Controller) infrastructure using Terraform on Rackspace Spot. Handles CRD registration, ArgoCD installation, and namespace management. Use when deploying or troubleshooting ARC infrastructure.
allowed-tools:
  - Bash
  - Read
  - Grep
  - Glob
---

# ARC Runner Terraform Deployment Skill

## Overview

This skill covers Terraform patterns for deploying GitHub Actions Runner Controller (ARC) on Rackspace Spot Kubernetes. Key challenge: managing resources that depend on CRDs installed during the same apply.

## Critical Learning: CRD Installation Timing

### The Problem

When deploying ARC, ArgoCD Applications are CRDs that don't exist until ArgoCD Helm chart is installed. Using `kubernetes_manifest` fails:

```
Error: Provider produced inconsistent result after apply
The CRD "applications.argoproj.io" does not exist
```

### The Solution: Use kubectl_manifest Instead

**WRONG** - kubernetes_manifest validates at plan time:
```hcl
resource "kubernetes_manifest" "argocd_app" {
  manifest = {
    apiVersion = "argoproj.io/v1alpha1"
    kind       = "Application"
    # ...
  }
}
# ERROR: CRD doesn't exist during terraform plan
```

**CORRECT** - kubectl_manifest applies at runtime:
```hcl
resource "kubectl_manifest" "argocd_app" {
  yaml_body = yamlencode({
    apiVersion = "argoproj.io/v1alpha1"
    kind       = "Application"
    # ...
  })

  depends_on = [
    helm_release.argocd,
    time_sleep.wait_for_crds
  ]
}
```

### Why This Works

| Provider | Plan Behavior | Apply Behavior | Use Case |
|----------|---------------|----------------|----------|
| `kubernetes_manifest` | Validates CRD exists | Applies manifest | Resources where CRD pre-exists |
| `kubectl_manifest` | No validation | Runs kubectl apply | Resources where CRD installed in same run |

## Pattern: CRD Registration Wait

After installing Helm charts that provide CRDs, add explicit wait:

```hcl
resource "helm_release" "argocd" {
  name       = "argocd"
  chart      = "argo-cd"
  repository = "https://argoproj.github.io/argo-helm"
  namespace  = "argocd"

  # ... chart configuration
}

resource "time_sleep" "wait_for_crds" {
  depends_on = [helm_release.argocd]

  create_duration = "30s"  # Wait for CRDs to register with K8s API
}

resource "kubectl_manifest" "bootstrap_app" {
  yaml_body = yamlencode({
    apiVersion = "argoproj.io/v1alpha1"
    kind       = "Application"
    # ...
  })

  depends_on = [time_sleep.wait_for_crds]
}
```

**Why 30 seconds?**
- CRDs must register with Kubernetes API server
- API server must propagate to all control plane nodes
- 30s provides safe buffer for registration

## Pattern: Namespace Management

### The Conflict

When both Terraform and ArgoCD try to create namespaces:
1. Terraform creates namespace
2. ArgoCD tries to create namespace with `CreateNamespace=true`
3. Namespace already exists → sync drift

### The Solution: Let ArgoCD Own Namespaces

**WRONG** - Terraform creates namespace:
```hcl
resource "kubernetes_namespace" "arc_runners" {
  metadata {
    name = "arc-runners"
  }
}

resource "kubectl_manifest" "argocd_app" {
  yaml_body = yamlencode({
    # ...
    spec = {
      destination = {
        namespace = "arc-runners"  # Already exists
      }
      syncPolicy = {
        syncOptions = ["CreateNamespace=true"]  # Conflict!
      }
    }
  })
}
```

**CORRECT** - ArgoCD creates namespace:
```hcl
resource "kubectl_manifest" "argocd_app" {
  yaml_body = yamlencode({
    apiVersion = "argoproj.io/v1alpha1"
    kind       = "Application"
    metadata = {
      name      = "arc-runners"
      namespace = "argocd"
    }
    spec = {
      destination = {
        namespace = "arc-runners"  # ArgoCD will create this
      }
      syncPolicy = {
        automated = {
          prune    = true
          selfHeal = true
        }
        syncOptions = ["CreateNamespace=true"]  # ArgoCD manages it
      }
    }
  })
}
```

**Exception: Namespace needs pre-created secrets**

If you need to create secrets BEFORE the application deploys:

```hcl
resource "kubernetes_namespace" "arc_runners" {
  metadata {
    name = "arc-runners"
  }
}

resource "kubernetes_secret" "github_token" {
  metadata {
    name      = "arc-org-github-secret"
    namespace = kubernetes_namespace.arc_runners.metadata[0].name
  }

  data = {
    github_token = var.github_token
  }

  type = "Opaque"
}

resource "kubectl_manifest" "argocd_app" {
  yaml_body = yamlencode({
    # ...
    spec = {
      destination = {
        namespace = "arc-runners"
      }
      syncPolicy = {
        syncOptions = []  # Do NOT include CreateNamespace - we created it
      }
    }
  })

  depends_on = [
    kubernetes_namespace.arc_runners,
    kubernetes_secret.github_token
  ]
}
```

## Common Deployment Patterns

### Pattern 1: ArgoCD Installation

```hcl
module "argocd" {
  source = "./modules/argocd"

  kubeconfig_path     = module.cloudspace.kubeconfig_path
  github_token_secret = var.github_token
  bootstrap_repo_url  = "https://github.com/Matchpoint-AI/matchpoint-github-runners-helm"
}
```

**Module responsibilities:**
1. Install ArgoCD Helm chart
2. Wait for CRDs to register
3. Create bootstrap Application (App-of-Apps)

### Pattern 2: Runner Scale Set Deployment

ArgoCD manages runner deployments via ApplicationSet:

```yaml
# argocd/applicationset.yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: github-runners
spec:
  generators:
  - list:
      elements:
      - name: arc-beta-runners
        valuesFile: examples/beta-runners-values.yaml
  template:
    metadata:
      name: '{{name}}'
    spec:
      source:
        repoURL: https://github.com/Matchpoint-AI/matchpoint-github-runners-helm
        targetRevision: main
        path: charts/github-actions-runners
        helm:
          releaseName: '{{name}}'  # CRITICAL: Must match runnerScaleSetName
          valueFiles:
          - '../../{{valuesFile}}'
```

## Troubleshooting

### Error: "Provider produced inconsistent result"

**Symptom:**
```
Error: Provider produced inconsistent result after apply
The CRD "applications.argoproj.io" does not exist
```

**Fix:** Change from `kubernetes_manifest` to `kubectl_manifest`

### Error: "Namespace already exists"

**Symptom:**
```
ArgoCD sync failed: namespace "arc-runners" already exists
```

**Fix:** Remove `CreateNamespace=true` from ArgoCD Application if Terraform created the namespace

### Error: "Application CRD not found"

**Symptom:**
```
kubectl_manifest failed: no matches for kind "Application"
```

**Fix:** Add `time_sleep` resource after ArgoCD Helm release:
```hcl
resource "time_sleep" "wait_for_crds" {
  depends_on      = [helm_release.argocd]
  create_duration = "30s"
}
```

## Diagnostic Commands

```bash
# Check if ArgoCD CRDs are registered
kubectl api-resources | grep argoproj

# Verify ArgoCD installation
kubectl get pods -n argocd

# Check Application CRD definition
kubectl get crd applications.argoproj.io

# View terraform state for ArgoCD resources
cd terraform
terraform state list | grep argocd

# Check for orphaned kubernetes resources
terraform state list | grep kubernetes_
```

## Best Practices

1. **Always use kubectl_manifest for ArgoCD Applications** - They depend on CRDs from the same apply
2. **Add time_sleep after Helm releases that install CRDs** - 30s is safe default
3. **Let ArgoCD manage namespaces when possible** - Reduces terraform/ArgoCD conflicts
4. **Use depends_on explicitly** - Makes dependencies clear and prevents race conditions
5. **Separate infrastructure from application config** - Terraform for infra, ArgoCD for apps

## Related Skills

- [infrastructure-cd](../infrastructure-cd/SKILL.md) - CD workflows for terraform
- [argocd-bootstrap](../argocd-bootstrap/SKILL.md) - App-of-Apps pattern
- [terraform-state-recovery](../terraform-state-recovery/SKILL.md) - Cleaning orphaned state

## Related Issues

- #121 - releaseName/runnerScaleSetName mismatch
- #122 - ApplicationSet fix
- #112 - CI jobs stuck investigation

## References

- [kubectl provider docs](https://registry.terraform.io/providers/gavinbunney/kubectl/latest/docs)
- [Terraform time_sleep](https://registry.terraform.io/providers/hashicorp/time/latest/docs/resources/sleep)
- [ArgoCD Application CRD](https://argo-cd.readthedocs.io/en/stable/operator-manual/declarative-setup/)
