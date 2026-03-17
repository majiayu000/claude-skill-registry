---
name: helm-release-troubleshooting
description: |
  Troubleshoot and fix Helm release issues managed by Terraform. Use when:
  (1) Terraform applies successfully but K8s resources don't reflect new Helm values,
  (2) New ports/volumes/containers from Helm chart values don't appear in deployed resources,
  (3) helm upgrade --reuse-values doesn't re-render templates for structural changes,
  (4) Terraform thinks Helm release is up-to-date but actual K8s resources are stale,
  (5) terraform apply fails with "another operation (install/upgrade/rollback) is in progress",
  (6) helm history shows status "pending-upgrade" or "pending-rollback",
  (7) a Helm upgrade was interrupted by network timeout, etcd timeout, or VPN drop,
  (8) helm upgrade fails with "an error occurred while finding last successful release".
  Covers force re-rendering via state removal/reimport and stuck release recovery via
  secret cleanup.
author: Claude Code
version: 1.0.0
date: 2026-02-22
---

# Helm Release Troubleshooting

## Force Re-render

### Problem
After changing Helm chart values in a Terraform `helm_release` resource, Terraform applies
successfully but the actual Kubernetes resources (Services, Deployments, etc.) don't reflect
the new values. For example, adding a new port in Helm values doesn't result in that port
appearing in the Service spec.

### Context / Trigger Conditions
- Terraform `helm_release` applies with "1 changed" but `kubectl get svc -o yaml` shows
  the old configuration
- Structural changes to Helm values (new ports, new containers, new volumes) are not
  reflected in deployed resources
- The Helm chart templates need to be fully re-rendered, not just patched
- Common with Traefik, ingress-nginx, and other charts where template logic conditionally
  includes resources based on values

### Root Cause
Terraform's `helm_release` resource uses `helm upgrade` under the hood. When values are
changed, Helm may use `--reuse-values` behavior where it merges new values into existing
ones rather than doing a full template re-render. For structural changes (like enabling
HTTP/3 which adds a new UDP port to the Service template), the templates may not be
re-rendered with the new conditional branches active.

Additionally, Terraform may see the stored Helm release state as matching the desired state
even though the actual Kubernetes resources don't reflect it, creating a state drift that
Terraform doesn't detect.

### Solution

#### Step 1: Verify the Discrepancy

Confirm that K8s resources don't match Helm values:
```bash
# Check the actual resource
kubectl get svc <service-name> -n <namespace> -o yaml

# Check what Helm thinks is deployed
helm get values <release-name> -n <namespace>
helm get manifest <release-name> -n <namespace> | grep -A10 "<expected-config>"
```

#### Step 2: Remove Helm Release from Terraform State

```bash
terraform state rm 'module.kubernetes_cluster.module.<service>.helm_release.<name>'
```

**IMPORTANT**: This only removes from Terraform state. The actual Helm release and K8s
resources remain untouched in the cluster.

#### Step 3: Import the Helm Release Back

```bash
terraform import 'module.kubernetes_cluster.module.<service>.helm_release.<name>' '<namespace>/<release-name>'
```

For Helm releases, the import ID format is `namespace/release-name`.

#### Step 4: Force Apply with Terraform

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

#### Step 5: Manual Helm Force Upgrade (Last Resort)

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

### Verification

```bash
# Check the K8s resources now match expected configuration
kubectl get svc <service-name> -n <namespace> -o yaml
kubectl get deployment <deployment-name> -n <namespace> -o yaml

# Verify Terraform is in sync
terraform plan -target=module.kubernetes_cluster.module.<service>
# Should show "No changes" or minimal expected drift
```

### Example: Traefik HTTP/3 UDP Port Not Appearing

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

### Notes

- This issue is more common with structural Helm value changes (new ports, new sidecars,
  conditional template blocks) than with simple value changes (image tags, replica counts)
- The `helm upgrade --force` flag deletes and recreates resources that have changed,
  which causes brief downtime. Use with caution on production ingress controllers.
- Always verify with `terraform plan` after fixing to ensure Terraform state is consistent

---

## Stuck Release Recovery

### Problem
Helm releases can get stuck in `pending-upgrade`, `pending-rollback`, or `pending-install`
states when an upgrade is interrupted (network drop, etcd timeout, resource exhaustion).
Subsequent upgrades or terraform applies fail because Helm thinks an operation is in progress.

### Context / Trigger Conditions
- `terraform apply` fails with: `another operation (install/upgrade/rollback) is in progress`
- `helm history <release> -n <namespace>` shows `pending-upgrade`, `pending-rollback`, or `pending-install`
- A previous Helm upgrade was interrupted by network timeout, VPN drop, or etcd timeout
- `helm upgrade` fails with: `an error occurred while finding last successful release`

### Solution

#### Step 1: Identify the stuck release
```bash
helm --kubeconfig $(pwd)/config history <release> -n <namespace> | tail -5
```

Look for revisions with status `pending-upgrade`, `pending-rollback`, or `pending-install`.

#### Step 2: Delete the stuck Helm release secrets
Each Helm revision is stored as a Kubernetes secret named `sh.helm.release.v1.<release>.v<revision>`.
Delete all stuck revisions:

```bash
# Delete specific stuck revision (e.g., revision 5)
kubectl --kubeconfig $(pwd)/config delete secret sh.helm.release.v1.<release>.v5 -n <namespace>

# If multiple stuck revisions exist, delete all of them
kubectl --kubeconfig $(pwd)/config delete secret sh.helm.release.v1.<release>.v6 -n <namespace>
```

#### Step 3: Verify the release is clean
```bash
helm --kubeconfig $(pwd)/config history <release> -n <namespace> | tail -3
```

The latest revision should now show `deployed` status.

#### Step 4: Retry the upgrade
```bash
terraform apply -target=module.kubernetes_cluster.module.<service> -var="kube_config_path=$(pwd)/config" -auto-approve
```

### Important Notes

- **Never patch the secret labels** (e.g., changing `status: pending-rollback` to `status: failed`).
  This changes the label but not the encoded release data inside the secret, leaving Helm in an
  inconsistent state. Always delete the stuck secrets entirely.
- If the failed upgrade partially applied changes to the cluster (e.g., modified a Deployment),
  the next successful upgrade will reconcile the state.
- When VPN/network is unstable, prefer direct `helm upgrade --reuse-values --set key=value`
  over `terraform apply`, since Helm upgrades are faster than the full Terraform refresh cycle.

### Verification
After deleting stuck secrets and re-applying:
- `helm history` shows the new revision as `deployed`
- `terraform apply` completes without errors

### Example
```bash
# Helm history shows stuck state
$ helm history nextcloud -n nextcloud | tail -3
4  deployed        nextcloud-8.8.1  Upgrade complete
5  failed          nextcloud-8.8.1  Upgrade failed: etcd timeout
6  pending-rollback nextcloud-8.8.1 Rollback to 4

# Fix: delete stuck revisions
$ kubectl delete secret sh.helm.release.v1.nextcloud.v5 sh.helm.release.v1.nextcloud.v6 -n nextcloud

# Verify clean state
$ helm history nextcloud -n nextcloud | tail -1
4  deployed  nextcloud-8.8.1  Upgrade complete

# Re-apply
$ terraform apply -target=module.kubernetes_cluster.module.nextcloud -auto-approve
```

---

## See Also

- `terraform-state-identity-mismatch` - For Terraform provider identity errors
- `traefik-http3-quic` - For enabling HTTP/3 on Traefik (common trigger for force re-render)

## References

- [Terraform helm_release Resource](https://registry.terraform.io/providers/hashicorp/helm/latest/docs/resources/release)
- [Helm Upgrade Documentation](https://helm.sh/docs/helm/helm_upgrade/)
- [Helm --force Flag](https://helm.sh/docs/helm/helm_upgrade/#options)
