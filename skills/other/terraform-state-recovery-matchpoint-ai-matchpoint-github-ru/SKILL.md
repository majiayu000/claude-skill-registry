---
name: terraform-state-recovery
description: Recover from Terraform state issues after infrastructure recreation. Handles orphaned resources, state drift, and cluster recovery. Use when terraform apply fails with resource conflicts.
allowed-tools:
  - Bash
  - Read
  - Grep
---

# Terraform State Recovery Skill

## Overview

When Kubernetes clusters are recreated (e.g., Rackspace Spot cloudspace deleted and recreated), Terraform state contains references to resources that no longer exist. This causes apply failures that require manual state cleanup.

## The Problem

### Scenario: Cluster Recreated

1. Initial state: Cluster A with ArgoCD, namespaces, secrets
2. Cluster deleted (spot preemption, manual deletion, provider issue)
3. Cluster B created with same name
4. Terraform apply fails:

```
Error: Resource already exists in state

Resource kubernetes_namespace.arc_runners already exists in state, but the
underlying Kubernetes cluster has been recreated. The resource exists in
terraform state but not in the actual cluster.
```

### Why This Happens

Terraform tracks resources by their Terraform resource ID, not by the underlying infrastructure:

```hcl
resource "kubernetes_namespace" "arc_runners" {
  # State: terraform_resource_id_123
  # Points to: Cluster A (no longer exists)
}
```

When Cluster B is created:
- Terraform state still references Cluster A resources
- `terraform plan` shows resources "already exist" (in state)
- `terraform apply` fails when trying to create them (they don't exist in Cluster B)

## Common Orphaned Resources

After cluster recreation, these resources are typically orphaned:

### Kubernetes Resources

```bash
# Check for orphaned Kubernetes resources
terraform state list | grep kubernetes_

# Common orphans:
kubernetes_namespace.arc_runners
kubernetes_namespace.arc_systems
kubernetes_secret.github_token
kubernetes_secret.argocd_secret
kubernetes_config_map_v1_data.argocd_cm
```

### Helm Releases

```bash
# Check for orphaned Helm releases
terraform state list | grep helm_release

# Common orphans:
helm_release.argocd
helm_release.arc_controller
```

### kubectl_manifest Resources

```bash
# Check for orphaned kubectl manifests
terraform state list | grep kubectl_manifest

# Common orphans:
kubectl_manifest.argocd_bootstrap
kubectl_manifest.argocd_app_arc_controller
```

## Recovery Procedure

### Step 1: Identify Orphaned Resources

```bash
cd terraform
export TF_HTTP_PASSWORD="<github-token>"
terraform init

# List all resources in state
terraform state list > /tmp/state-resources.txt

# Check which cluster the state references
terraform state show module.cloudspace.spot_cloudspace.main | grep cloudspace_id

# Compare with actual cloudspace
spotctl cloudspaces list --org matchpoint-ai -o table
```

### Step 2: Remove Orphaned Resources

**CRITICAL:** Only remove resources from OLD cluster. Do NOT remove:
- `spot_cloudspace.main` (the cluster itself)
- `spot_nodepool.*` (node pools)
- `data.spot_kubeconfig.*` (kubeconfig data sources)

```bash
# Remove Helm releases (they don't exist in new cluster)
terraform state rm helm_release.argocd

# Remove Kubernetes namespaces
terraform state rm kubernetes_namespace.arc_runners
terraform state rm kubernetes_namespace.arc_systems

# Remove Kubernetes secrets
terraform state rm kubernetes_secret.github_token
terraform state rm kubernetes_secret.argocd_secret

# Remove ConfigMaps
terraform state rm kubernetes_config_map_v1_data.argocd_cm

# Remove kubectl manifests
terraform state rm kubectl_manifest.argocd_bootstrap
terraform state rm kubectl_manifest.argocd_app_arc_controller
```

### Step 3: Verify State is Clean

```bash
# List remaining resources
terraform state list

# Should see:
# - module.cloudspace.spot_cloudspace.main
# - module.nodepool.spot_nodepool.*
# - data.spot_kubeconfig.this
# Should NOT see:
# - kubernetes_* resources
# - helm_release.* resources
# - kubectl_manifest.* resources
```

### Step 4: Re-Apply

```bash
# Plan should show creating all Kubernetes resources
terraform plan -var-file=prod.tfvars

# Apply to recreate resources in new cluster
terraform apply -var-file=prod.tfvars
```

## Automated Recovery Script

```bash
#!/bin/bash
# terraform/scripts/clean-orphaned-state.sh

set -euo pipefail

echo "🔍 Identifying orphaned Kubernetes resources..."

# Get list of Kubernetes resources in state
ORPHANED=$(terraform state list | grep -E "(kubernetes_|helm_release|kubectl_manifest)" || true)

if [ -z "$ORPHANED" ]; then
  echo "✅ No orphaned resources found"
  exit 0
fi

echo "📋 Found orphaned resources:"
echo "$ORPHANED"
echo ""

read -p "Remove these resources from state? (yes/no): " CONFIRM

if [ "$CONFIRM" != "yes" ]; then
  echo "❌ Aborted"
  exit 1
fi

echo "$ORPHANED" | while read -r resource; do
  echo "🗑️  Removing: $resource"
  terraform state rm "$resource"
done

echo "✅ State cleanup complete"
echo ""
echo "Next steps:"
echo "1. Run: terraform plan -var-file=prod.tfvars"
echo "2. Verify plan shows creating resources (not updating)"
echo "3. Run: terraform apply -var-file=prod.tfvars"
```

**Usage:**
```bash
cd terraform
export TF_HTTP_PASSWORD="<github-token>"
terraform init
./scripts/clean-orphaned-state.sh
```

## Diagnosis: Is State Orphaned?

### Check 1: Cluster ID Mismatch

```bash
# Get cloudspace ID from terraform state
terraform state show module.cloudspace.spot_cloudspace.main | grep cloudspace_id

# Get actual cloudspace ID
spotctl cloudspaces get --name matchpoint-runners-prod --org matchpoint-ai -o json | jq -r .cloudspaceId

# If different → cluster was recreated
```

### Check 2: Resource Shows "Not Found" in Plan

```bash
terraform plan -var-file=prod.tfvars

# Look for:
# ~ resource "kubernetes_namespace" "arc_runners" {
#     # Warning: resource not found in cluster
# }
```

### Check 3: kubectl Confirms Resources Don't Exist

```bash
# Get fresh kubeconfig
terraform output -raw kubeconfig_raw > /tmp/kubeconfig.yaml
export KUBECONFIG=/tmp/kubeconfig.yaml

# Check if resources exist
kubectl get namespace arc-runners
# Error: namespace "arc-runners" not found → Orphaned in state

# But terraform state shows:
terraform state show kubernetes_namespace.arc_runners
# Shows resource in state → State is stale
```

## Prevention Strategies

### Strategy 1: Use Data Sources Where Possible

Instead of managing resources in Terraform, reference them as data sources:

```hcl
# FRAGILE - resource managed by Terraform
resource "kubernetes_namespace" "arc_runners" {
  metadata {
    name = "arc-runners"
  }
}

# ROBUST - reference namespace created by ArgoCD
data "kubernetes_namespace" "arc_runners" {
  metadata {
    name = "arc-runners"
  }
}
```

Data sources don't persist in state, so they can't become orphaned.

### Strategy 2: Let ArgoCD Manage Application Resources

```hcl
# Terraform manages infrastructure
resource "spot_cloudspace" "main" { }
resource "helm_release" "argocd" { }

# ArgoCD manages applications
# - Namespaces
# - Secrets (via SealedSecrets or external-secrets)
# - ConfigMaps
# - Deployments
```

This separation means:
- Cluster recreation only affects Terraform resources (infrastructure)
- Application resources recreated automatically by ArgoCD sync

### Strategy 3: Use Remote State Locking

Prevent concurrent applies that can corrupt state:

```hcl
# backend.tf
terraform {
  backend "http" {
    address        = "https://state.tfstate.dev/github/v1"
    lock_address   = "https://state.tfstate.dev/github/v1/lock"
    unlock_address = "https://state.tfstate.dev/github/v1/lock"
  }
}
```

## Troubleshooting

### Error: "Resource not found"

**Symptom:**
```
Error: reading Kubernetes Namespace "arc-runners": namespaces "arc-runners" not found
```

**Cause:** Resource exists in state but not in cluster

**Fix:**
```bash
terraform state rm kubernetes_namespace.arc_runners
terraform apply
```

### Error: "State lock timeout"

**Symptom:**
```
Error: Error acquiring the state lock
Lock Info:
  ID:        abc-123-def
  Operation: OperationTypeApply
  Who:       user@host
  Created:   2024-01-01 12:00:00 UTC
```

**Cause:** Previous terraform apply crashed or was interrupted

**Fix:**
```bash
# Verify no terraform process running
ps aux | grep terraform

# Force unlock (only if safe)
terraform force-unlock abc-123-def
```

### Error: "Provider configuration changed"

**Symptom:**
```
Error: Provider configuration changed

The provider configuration for provider["kubernetes"] has changed. This may
be because the kubeconfig references a different cluster.
```

**Cause:** Kubeconfig points to new cluster but state references old cluster

**Fix:**
```bash
# Get fresh kubeconfig for current cluster
terraform output -raw kubeconfig_raw > /tmp/kubeconfig.yaml
export KUBECONFIG=/tmp/kubeconfig.yaml

# Remove orphaned Kubernetes resources
./scripts/clean-orphaned-state.sh

# Re-apply
terraform apply -var-file=prod.tfvars
```

## Advanced Recovery: Import Resources

If resources exist in the NEW cluster but not in state:

```bash
# Import namespace
terraform import kubernetes_namespace.arc_runners arc-runners

# Import secret
terraform import kubernetes_secret.github_token arc-runners/arc-org-github-secret

# Import Helm release
terraform import helm_release.argocd argocd/argocd
```

**When to use import:**
- Resources manually created in cluster
- Need to bring them under Terraform management
- Alternative to destroying and recreating

**When NOT to use import:**
- Resources don't exist (use `terraform state rm` instead)
- Resources managed by ArgoCD (let ArgoCD manage them)

## Diagnostic Commands

```bash
# List all resources in state
terraform state list

# Show specific resource details
terraform state show kubernetes_namespace.arc_runners

# Pull current state to local file
terraform state pull > /tmp/terraform.tfstate

# Inspect state JSON
jq '.resources[] | select(.type == "kubernetes_namespace")' /tmp/terraform.tfstate

# Check cluster connectivity
terraform output -raw kubeconfig_raw > /tmp/kubeconfig.yaml
export KUBECONFIG=/tmp/kubeconfig.yaml
kubectl cluster-info

# Verify state backend connection
terraform init -backend-config="password=$TF_HTTP_PASSWORD"
```

## State File Forensics

### Understanding State Structure

```json
{
  "resources": [
    {
      "mode": "managed",
      "type": "kubernetes_namespace",
      "name": "arc_runners",
      "provider": "provider[\"kubernetes\"]",
      "instances": [
        {
          "attributes": {
            "metadata": [{"name": "arc-runners"}]
          }
        }
      ]
    }
  ]
}
```

**Key fields:**
- `mode: "managed"` - Terraform manages this resource
- `mode: "data"` - Terraform only reads this resource
- `instances[].attributes` - Current resource configuration

### Finding Orphaned Resources

```bash
# Extract all Kubernetes resources
terraform state pull | jq -r '.resources[] | select(.type | startswith("kubernetes_")) | .type + "." + .name'

# Compare with actual cluster resources
kubectl get namespaces -o name
kubectl get secrets -A -o name
```

## Related Skills

- [arc-terraform-deployment](../arc-terraform-deployment/SKILL.md) - Avoiding orphaned state
- [infrastructure-cd](../infrastructure-cd/SKILL.md) - Automated terraform workflow
- [argocd-bootstrap](../argocd-bootstrap/SKILL.md) - Separating app management

## Related Issues

- #115 - Cluster DNS not resolving (cluster recreation scenario)
- #121 - State cleanup after ApplicationSet fix
- #119 - Namespace creation conflicts

## References

- [Terraform State](https://developer.hashicorp.com/terraform/language/state)
- [Terraform State Commands](https://developer.hashicorp.com/terraform/cli/commands/state)
- [Kubernetes Provider](https://registry.terraform.io/providers/hashicorp/kubernetes/latest/docs)
