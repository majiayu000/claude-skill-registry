---
name: terraform-state-identity-mismatch
description: |
  Fix Terraform "Unexpected Identity Change" errors during plan/apply. Use when:
  (1) Terraform fails with "the Terraform Provider unexpectedly returned a different 
  identity", (2) State refresh shows identity mismatch between stored and current values,
  (3) Resource was created but terraform apply timed out, leaving state inconsistent.
  Solution involves removing and reimporting the affected resource.
author: Claude Code
version: 1.0.0
date: 2026-01-28
---

# Terraform State Identity Mismatch Fix

## Problem
Terraform fails during plan or apply with an "Unexpected Identity Change" error, 
indicating the stored state identity doesn't match what the provider returns when 
reading the resource.

## Context / Trigger Conditions
- Error message contains: "Unexpected Identity Change: During the read operation, 
  the Terraform Provider unexpectedly returned a different identity"
- Often occurs after a terraform apply times out mid-creation
- Resource exists in the cluster/cloud but state is corrupted
- Common with Kubernetes provider after deployment rollout timeouts

## Solution

### Step 1: Identify the affected resource
The error message includes the resource address:
```
with module.kubernetes_cluster.module.resume["resume"].kubernetes_deployment.resume
```

### Step 2: Remove from state
```bash
terraform state rm 'module.kubernetes_cluster.module.resume["resume"].kubernetes_deployment.resume'
```
Note: Use single quotes around the address to handle brackets properly.

### Step 3: Import the resource back
```bash
terraform import 'module.kubernetes_cluster.module.resume["resume"].kubernetes_deployment.resume' <namespace>/<name>
```
For Kubernetes deployments, the import ID is `namespace/deployment-name`.

### Step 4: Verify with plan
```bash
terraform plan -target=<module-path>
```
Should show minimal or no changes if import was successful.

### Step 5: Apply to sync any drift
```bash
terraform apply -target=<module-path>
```

## Verification
- `terraform plan` runs without identity errors
- `terraform apply` completes successfully
- Resource still exists and functions correctly

## Example
**Error:**
```
Error: Unexpected Identity Change

Current Identity: cty.ObjectVal(map[string]cty.Value{"api_version":cty.NullVal...})
New Identity: cty.ObjectVal(map[string]cty.Value{"api_version":cty.StringVal("apps/v1")...})

with module.kubernetes_cluster.module.resume["resume"].kubernetes_deployment.resume
```

**Fix:**
```bash
terraform state rm 'module.kubernetes_cluster.module.resume["resume"].kubernetes_deployment.resume'
# Output: Removed ... Successfully removed 1 resource instance(s).

terraform import 'module.kubernetes_cluster.module.resume["resume"].kubernetes_deployment.resume' resume/resume
# Output: Import successful!

terraform apply -target=module.kubernetes_cluster.module.resume -auto-approve
# Output: Apply complete! Resources: 0 added, 1 changed, 0 destroyed.
```

## Notes
- This is a provider bug, not user error - consider reporting to provider maintainers
- The resource continues to work fine; only the terraform state is affected
- Always verify the resource exists before importing (don't import non-existent resources)
- For Kubernetes resources, import IDs are typically `namespace/name`
- For AWS resources, import IDs vary by resource type (check provider docs)
- Consider adding `-lock=false` if state locking causes issues during recovery

## See Also
- Terraform state management documentation
- Kubernetes provider import documentation
