---
name: helm-stuck-release-recovery
description: |
  Fix Helm releases stuck in pending-upgrade, pending-rollback, or pending-install states.
  Use when: (1) terraform apply fails with "another operation (install/upgrade/rollback) is
  in progress", (2) helm history shows status "pending-upgrade" or "pending-rollback",
  (3) a Helm upgrade was interrupted by network timeout, etcd timeout, or VPN drop,
  (4) helm upgrade fails with "an error occurred while finding last successful release".
  Covers manual secret cleanup to restore Helm release to a deployable state.
author: Claude Code
version: 1.0.0
date: 2026-02-15
---

# Helm Stuck Release Recovery

## Problem
Helm releases can get stuck in `pending-upgrade`, `pending-rollback`, or `pending-install`
states when an upgrade is interrupted (network drop, etcd timeout, resource exhaustion).
Subsequent upgrades or terraform applies fail because Helm thinks an operation is in progress.

## Context / Trigger Conditions
- `terraform apply` fails with: `another operation (install/upgrade/rollback) is in progress`
- `helm history <release> -n <namespace>` shows `pending-upgrade`, `pending-rollback`, or `pending-install`
- A previous Helm upgrade was interrupted by network timeout, VPN drop, or etcd timeout
- `helm upgrade` fails with: `an error occurred while finding last successful release`

## Solution

### Step 1: Identify the stuck release
```bash
helm --kubeconfig $(pwd)/config history <release> -n <namespace> | tail -5
```

Look for revisions with status `pending-upgrade`, `pending-rollback`, or `pending-install`.

### Step 2: Delete the stuck Helm release secrets
Each Helm revision is stored as a Kubernetes secret named `sh.helm.release.v1.<release>.v<revision>`.
Delete all stuck revisions:

```bash
# Delete specific stuck revision (e.g., revision 5)
kubectl --kubeconfig $(pwd)/config delete secret sh.helm.release.v1.<release>.v5 -n <namespace>

# If multiple stuck revisions exist, delete all of them
kubectl --kubeconfig $(pwd)/config delete secret sh.helm.release.v1.<release>.v6 -n <namespace>
```

### Step 3: Verify the release is clean
```bash
helm --kubeconfig $(pwd)/config history <release> -n <namespace> | tail -3
```

The latest revision should now show `deployed` status.

### Step 4: Retry the upgrade
```bash
terraform apply -target=module.kubernetes_cluster.module.<service> -var="kube_config_path=$(pwd)/config" -auto-approve
```

## Important Notes

- **Never patch the secret labels** (e.g., changing `status: pending-rollback` to `status: failed`).
  This changes the label but not the encoded release data inside the secret, leaving Helm in an
  inconsistent state. Always delete the stuck secrets entirely.
- If the failed upgrade partially applied changes to the cluster (e.g., modified a Deployment),
  the next successful upgrade will reconcile the state.
- When VPN/network is unstable, prefer direct `helm upgrade --reuse-values --set key=value`
  over `terraform apply`, since Helm upgrades are faster than the full Terraform refresh cycle.

## Verification
After deleting stuck secrets and re-applying:
- `helm history` shows the new revision as `deployed`
- `terraform apply` completes without errors

## Example
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
