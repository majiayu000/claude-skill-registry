---
name: helm-release-force-rerender
description: |
  Fix for Helm releases managed by Terraform where changing Helm values doesn't update
  the actual Kubernetes resources. Use when: (1) Terraform applies successfully but
  K8s resources (Service, Deployment) don't reflect new Helm values,
  (2) New ports/volumes/containers from Helm chart values don't appear in the deployed resources,
  (3) helm upgrade --reuse-values doesn't re-render templates for structural changes,
  (4) Terraform thinks Helm release is up-to-date but actual K8s resources are stale.
  Solution involves removing from Terraform state, reimporting, and force upgrading.
author: Claude Code
version: 1.0.0
date: 2026-02-07
---

# Helm Release Force Re-render via Terraform

## Problem
After changing Helm chart values in a Terraform `helm_release` resource, Terraform applies
successfully but the actual Kubernetes resources (Services, Deployments, etc.) don't reflect
the new values. For example, adding a new port in Helm values doesn't result in that port
appearing in the Service spec.

## Context / Trigger Conditions
- Terraform `helm_release` applies with "1 changed" but `kubectl get svc -o yaml` shows
  the old configuration
- Structural changes to Helm values (new ports, new containers, new volumes) are not
  reflected in deployed resources
- The Helm chart templates need to be fully re-rendered, not just patched
- Common with Traefik, ingress-nginx, and other charts where template logic conditionally
  includes resources based on values

## Root Cause
Terraform's `helm_release` resource uses `helm upgrade` under the hood. When values are
changed, Helm may use `--reuse-values` behavior where it merges new values into existing
ones rather than doing a full template re-render. For structural changes (like enabling
HTTP/3 which adds a new UDP port to the Service template), the templates may not be
re-rendered with the new conditional branches active.

Additionally, Terraform may see the stored Helm release state as matching the desired state
even though the actual Kubernetes resources don't reflect it, creating a state drift that
Terraform doesn't detect.

## Solution

### Step 1: Verify the Discrepancy

Confirm that K8s resources don't match Helm values:
```bash
# Check the actual resource
kubectl get svc <service-name> -n <namespace> -o yaml

# Check what Helm thinks is deployed
helm get values <release-name> -n <namespace>
helm get manifest <release-name> -n <namespace> | grep -A10 "<expected-config>"
```

### Step 2: Remove Helm Release from Terraform State

```bash
terraform state rm 'module.kubernetes_cluster.module.<service>.helm_release.<name>'
```

**IMPORTANT**: This only removes from Terraform state. The actual Helm release and K8s
resources remain untouched in the cluster.

### Step 3: Import the Helm Release Back

```bash
terraform import 'module.kubernetes_cluster.module.<service>.helm_release.<name>' '<namespace>/<release-name>'
```

For Helm releases, the import ID format is `namespace/release-name`.

### Step 4: Force Apply with Terraform

After reimporting, run terraform apply. Terraform should now detect the drift between
the desired Helm values and the actual release state:

```bash
terraform apply -target=module.kubernetes_cluster.module.<service>
```

If Terraform still shows "no changes", you may need to taint the resource:
```bash
terraform taint 'module.kubernetes_cluster.module.<service>.helm_release.<name>'
terraform apply -target=module.kubernetes_cluster.module.<service>
```

### Step 5: Manual Helm Force Upgrade (Last Resort)

If Terraform still doesn't fix it, use Helm directly as a one-time fix, then reimport:

```bash
# Get the current values file
helm get values <release-name> -n <namespace> -o yaml > /tmp/values.yaml

# Edit /tmp/values.yaml to include the correct values, or use --set flags

# Force upgrade (re-renders all templates)
helm upgrade --force <release-name> <chart> -n <namespace> -f /tmp/values.yaml

# Then reimport into Terraform
terraform state rm 'module.kubernetes_cluster.module.<service>.helm_release.<name>'
terraform import 'module.kubernetes_cluster.module.<service>.helm_release.<name>' '<namespace>/<release-name>'
terraform apply -target=module.kubernetes_cluster.module.<service>
```

**WARNING**: Direct Helm operations bypass Terraform. Always reimport into Terraform state
afterward, and use `terraform apply` to verify Terraform is back in sync.

## Verification

```bash
# Check the K8s resources now match expected configuration
kubectl get svc <service-name> -n <namespace> -o yaml
kubectl get deployment <deployment-name> -n <namespace> -o yaml

# Verify Terraform is in sync
terraform plan -target=module.kubernetes_cluster.module.<service>
# Should show "No changes" or minimal expected drift
```

## Example: Traefik HTTP/3 UDP Port Not Appearing

**Problem**: Added `http3.enabled=true` to Traefik Helm values. Terraform applied
successfully, but the Traefik Service only had TCP port 443, missing the expected
UDP port 443 (`websecure-http3`).

**Fix**:
```bash
# 1. Remove from state
terraform state rm 'module.kubernetes_cluster.module.traefik.helm_release.traefik'

# 2. Reimport
terraform import 'module.kubernetes_cluster.module.traefik.helm_release.traefik' 'traefik/traefik'

# 3. Apply (Terraform now detects the drift)
terraform apply -target=module.kubernetes_cluster.module.traefik

# 4. Verify
kubectl get svc traefik -n traefik -o yaml | grep -A3 "websecure-http3"
# Should show: port: 443, protocol: UDP
```

## Notes

- This issue is more common with structural Helm value changes (new ports, new sidecars,
  conditional template blocks) than with simple value changes (image tags, replica counts)
- The `helm upgrade --force` flag deletes and recreates resources that have changed,
  which causes brief downtime. Use with caution on production ingress controllers.
- Always verify with `terraform plan` after fixing to ensure Terraform state is consistent
- This is different from the `terraform-state-identity-mismatch` skill, which covers
  provider-level identity errors. This skill covers Helm template rendering issues where
  the state looks correct but the actual resources don't match.

## See Also

- `terraform-state-identity-mismatch` - For Terraform provider identity errors
- `traefik-http3-quic` - For enabling HTTP/3 on Traefik (common trigger for this issue)

## References

- [Terraform helm_release Resource](https://registry.terraform.io/providers/hashicorp/helm/latest/docs/resources/release)
- [Helm Upgrade Documentation](https://helm.sh/docs/helm/helm_upgrade/)
- [Helm --force Flag](https://helm.sh/docs/helm/helm_upgrade/#options)
