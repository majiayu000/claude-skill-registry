---
name: kubelet-static-pod-manifest-update
description: |
  Force kubelet to pick up changes to static pod manifests in /etc/kubernetes/manifests/.
  Use when: (1) edited kube-apiserver.yaml but the running process still has old flags,
  (2) kubelet restart doesn't pick up manifest changes, (3) touching the manifest file
  doesn't trigger pod recreation, (4) killing the API server process results in the
  same old args on restart, (5) the pod's config.hash annotation doesn't match the
  file's hash. Requires a full cycle: remove manifest, stop kubelet, remove containers,
  re-add manifest, start kubelet.
author: Claude Code
version: 1.0.0
date: 2026-02-17
---

# Kubelet Static Pod Manifest Update

## Problem
After editing a static pod manifest (e.g., `/etc/kubernetes/manifests/kube-apiserver.yaml`
to add OIDC or audit flags), kubelet continues running the pod with the old configuration.
Standard approaches like `touch`, `systemctl restart kubelet`, or `kubectl delete pod`
do not force kubelet to reconcile the new manifest.

## Context / Trigger Conditions
- Edited `/etc/kubernetes/manifests/kube-apiserver.yaml` (or other static pod manifests)
- The running process (`ps aux | grep kube-apiserver`) shows old flags
- `kubectl get pod -n kube-system kube-apiserver-* -o jsonpath='{.metadata.annotations.kubernetes\.io/config\.hash}'` returns a stale hash
- Any of these actions failed to apply the changes:
  - `touch /etc/kubernetes/manifests/kube-apiserver.yaml`
  - `systemctl restart kubelet`
  - `kubectl delete pod kube-apiserver-*`
  - Killing the API server process directly

## Root Cause
Kubelet maintains an internal cache of static pod specs keyed by a hash of the manifest.
When the manifest changes, kubelet should detect the new hash and recreate the pod.
However, in practice (observed on Kubernetes 1.34.x), kubelet can get stuck with the
old hash if:
- The pod's mirror object in the API server still exists with the old hash
- Kubelet's internal pod cache wasn't cleared between restarts
- The container runtime (containerd) still has the old container running

## Solution

Full restart cycle on the master node:

```bash
# 1. Back up the manifest
sudo cp /etc/kubernetes/manifests/kube-apiserver.yaml /tmp/kube-apiserver.yaml.bak

# 2. Remove the manifest (kubelet will stop the pod)
sudo rm /etc/kubernetes/manifests/kube-apiserver.yaml

# 3. Stop kubelet
sudo systemctl stop kubelet

# 4. Wait for the API server container to stop
sleep 5

# 5. Force-remove any remaining API server containers
sudo crictl rm -f $(sudo crictl ps -aq --name kube-apiserver 2>/dev/null) 2>/dev/null

# 6. Re-add the manifest (with your changes)
sudo cp /tmp/kube-apiserver.yaml.bak /etc/kubernetes/manifests/kube-apiserver.yaml

# 7. Start kubelet
sudo systemctl start kubelet

# 8. Wait for API server to come up (30-60 seconds)
sleep 45

# 9. Verify new flags are active
sudo cat /proc/$(pgrep -f 'kube-apiserver --' | head -1)/cmdline | tr '\0' '\n' | grep 'your-new-flag'
```

**Critical:** The order matters. Removing the manifest BEFORE stopping kubelet ensures
kubelet processes the removal. Then clearing containers ensures no stale state. Finally,
re-adding the manifest with kubelet running triggers a fresh pod creation.

## What Does NOT Work

| Approach | Why it fails |
|----------|-------------|
| `touch manifest.yaml` | Kubelet may not detect mtime-only changes |
| `systemctl restart kubelet` | Kubelet reuses cached pod spec if hash matches |
| `kubectl delete pod` | Deletes mirror pod but kubelet recreates from cached spec |
| `kill <apiserver-pid>` | Container runtime restarts the same container with old args |
| Moving manifest away and back without stopping kubelet | Kubelet may cache the old spec in memory |

## Verification

```bash
# Check the running process has new flags
ps aux | grep kube-apiserver | grep -v grep | grep 'your-new-flag'

# Check the config hash changed
kubectl get pod -n kube-system kube-apiserver-$(hostname) \
  -o jsonpath='{.metadata.annotations.kubernetes\.io/config\.hash}'

# Check API server logs for successful startup
kubectl logs -n kube-system kube-apiserver-$(hostname) | tail -5
```

## Notes
- This applies to ALL static pods, not just kube-apiserver (etcd, controller-manager, scheduler)
- The cluster will be briefly unavailable during the restart (30-60 seconds)
- On single-master clusters, kubectl commands will fail during the restart — use `sudo kubectl --kubeconfig=/etc/kubernetes/admin.conf` from the master
- Always validate the YAML before removing the manifest: `python3 -c "import yaml; yaml.safe_load(open('/etc/kubernetes/manifests/kube-apiserver.yaml'))"`
- See also: `authentik-oidc-kubernetes` skill for the full OIDC setup context
