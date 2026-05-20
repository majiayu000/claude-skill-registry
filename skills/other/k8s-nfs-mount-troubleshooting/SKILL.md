---
name: k8s-nfs-mount-troubleshooting
description: |
  Debug Kubernetes NFS volume mount failures. Use when: (1) Pod stuck in ContainerCreating
  for extended time, (2) kubectl describe shows "MountVolume.SetUp failed" with NFS errors,
  (3) Error message shows "Protocol not supported" or "mount.nfs: access denied",
  (4) NFS volume defined in pod spec but container won't start, (5) Container starts but
  gets "Permission denied" writing to NFS volume (non-root container UID mismatch),
  (6) CronJob or init container fails silently when writing to NFS, (7) Pod shows Running
  1/1 but service is unresponsive after a node reboot — stale NFS mount causes frozen
  processes with zero listening sockets. Common root causes are missing NFS export on the
  server, UID mismatch for non-root containers, and stale mounts after node reboots.
author: Claude Code
version: 1.2.0
date: 2026-02-28
---

# Kubernetes NFS Mount Troubleshooting

## Problem
Pods with NFS volumes get stuck in `ContainerCreating` state indefinitely. The error 
messages from `kubectl describe pod` can be misleading, showing protocol or permission 
errors when the actual issue is the NFS export doesn't exist.

## Context / Trigger Conditions
- Pod status shows `ContainerCreating` for more than 1-2 minutes
- `kubectl describe pod` shows events like:
  - `MountVolume.SetUp failed for volume "data" : mount failed: exit status 32`
  - `mount.nfs: Protocol not supported`
  - `mount.nfs: access denied by server`
- Pod spec includes an NFS volume mount
- Other pods on the same node work fine

## Solution

### Step 1: Identify the NFS path
```bash
kubectl describe pod -n <namespace> <pod-name> | grep -A5 "Volumes:"
```
Look for the NFS server and path (e.g., `10.0.10.15:/mnt/main/myservice`)

### Step 2: Verify the export exists on NFS server
SSH to the NFS server and check:
```bash
ssh root@<nfs-server> "ls -la /mnt/main/myservice"
```

### Step 3: If directory doesn't exist, create it
```bash
ssh root@<nfs-server> "mkdir -p /mnt/main/myservice && chmod 777 /mnt/main/myservice"
```

### Step 4: Add to NFS exports (TrueNAS specific)
For TrueNAS, add the path to the NFS share configuration:
1. Add directory to `scripts/nfs_directories.txt`
2. Run `scripts/nfs_exports.sh` to update the share via API

### Step 5: Restart the pod
```bash
kubectl delete pod -n <namespace> -l app=<app-label>
```
The deployment will create a new pod that should now mount successfully.

## Verification
```bash
kubectl get pods -n <namespace>
# Should show 1/1 Running instead of 0/1 ContainerCreating

kubectl exec -n <namespace> <pod-name> -- ls -la /app/data
# Should show the mounted directory contents
```

## Example
**Symptom:**
```
Events:
  Warning  FailedMount  55s (x13 over 11m)  kubelet  MountVolume.SetUp failed for volume "data" : mount failed: exit status 32
  Mounting command: mount
  Mounting arguments: -t nfs 10.0.10.15:/mnt/main/resume /var/lib/kubelet/pods/.../data
  Output: mount.nfs: Protocol not supported
```

**Root Cause:** The directory `/mnt/main/resume` didn't exist on the TrueNAS server.

**Fix:**
```bash
ssh root@10.0.10.15 'mkdir -p /mnt/main/resume && chmod 777 /mnt/main/resume'
# Then add to NFS exports and restart pod
```

## Notes
- The "Protocol not supported" error is misleading - it often means the export path doesn't exist
- Always check the NFS server first before investigating protocol/firewall issues
- For TrueNAS, the NFS share must be updated via API/UI after creating new directories
- NFSv3 vs NFSv4 issues are rare in modern setups; missing paths are more common
- Check that the NFS client packages are installed on Kubernetes nodes if this is a new cluster

## Variant: Non-Root Container UID Permission Denied

### Problem
Container starts and mounts NFS successfully, but gets "Permission denied" when
writing files. The pod appears healthy but operations fail silently.

### Trigger Conditions
- Container logs show "Permission denied" or "client returned ERROR on write"
- Pod is Running (not stuck in ContainerCreating)
- NFS directory exists and is mounted, but owned by root (uid 0)
- Container image runs as a non-root user (e.g., `curlimages/curl` runs as uid 101)
- CronJobs or init containers that write to NFS fail with no obvious error

### Common Non-Root Container UIDs
| Image | UID | User |
|-------|-----|------|
| `curlimages/curl` | 101 | curl_user |
| `nginx` (unprivileged) | 101 | nginx |
| `node` | 1000 | node |
| `python` (slim) | 0 | root (safe) |
| `grafana/grafana` | 472 | grafana |

### Solution
Fix permissions on the NFS server:
```bash
# Option 1: World-writable (simplest, suitable for non-sensitive data)
ssh root@10.0.10.15 "chmod -R 777 /mnt/main/<service>/<subdir>"

# Option 2: Match container UID (more secure)
ssh root@10.0.10.15 "chown -R <uid>:<gid> /mnt/main/<service>/<subdir>"

# Option 3: Use securityContext in pod spec to run as root
spec:
  securityContext:
    runAsUser: 0
```

### Debugging
```bash
# Check what UID the container runs as
kubectl exec -n <namespace> <pod> -- id

# Test write access from inside container
kubectl exec -n <namespace> <pod> -- sh -c 'echo test > /path/to/nfs/testfile'

# Check NFS directory ownership on server
ssh root@10.0.10.15 "ls -la /mnt/main/<service>/"
```

## Variant: Stale NFS Mounts After Node Reboot (Ghost Running Pods)

### Problem
After a node reboot (e.g., from kured rolling kernel updates), pods are rescheduled and
show `Running 1/1` status, but the application process is frozen/hung. The service is
completely unresponsive despite appearing healthy to Kubernetes.

### Trigger Conditions
- Node was recently rebooted (check `kubectl get nodes` for age, or kured logs)
- Pod shows `Running 1/1` with 0 restarts (looks perfectly healthy)
- Service is unresponsive — Uptime Kuma or curl shows timeout/connection refused
- `kubectl exec <pod> -- ss -tlnp` shows **zero listening sockets** (the process started but is hung)
- Pod uses NFS volumes (inline `nfs {}` or PVC backed by NFS)
- Multiple pods across different namespaces all exhibit the same symptom simultaneously
- `kubectl describe pod` shows no warnings or errors — everything looks normal

### Root Cause
When a node reboots, the NFS client mounts go stale. If the pod is rescheduled to the
same or different node before NFS fully recovers, the application process starts but
immediately hangs when it tries to access the NFS-mounted filesystem. The process is
stuck in an uninterruptible I/O wait (D state) but Kubernetes sees the container as
running because the PID exists and liveness probes (if any) may not exercise the NFS path.

### Solution
Force-delete the affected pods to trigger a clean reschedule with fresh NFS mounts:

```bash
# Identify hung pods — Running but no listening sockets
kubectl exec -n <namespace> <pod> -- ss -tlnp 2>/dev/null
# If output is empty or shows no expected ports, the pod is hung

# Force-delete to skip graceful shutdown (hung process won't respond to SIGTERM)
kubectl delete pod -n <namespace> <pod> --force --grace-period=0

# The deployment controller creates a new pod with fresh NFS mounts
kubectl get pods -n <namespace> -w
```

For bulk remediation after a cluster-wide event:
```bash
# Find all pods with NFS volumes that might be hung
# Check each service's expected port — if ss -tlnp shows nothing, force-delete
for ns in calibre stirling-pdf send speedtest n8n paperless-ngx; do
  pod=$(kubectl get pod -n $ns -o name | head -1)
  sockets=$(kubectl exec -n $ns ${pod} -- ss -tlnp 2>/dev/null | wc -l)
  if [ "$sockets" -le 1 ]; then
    echo "HUNG: $ns/$pod (no listening sockets)"
    kubectl delete ${pod} -n $ns --force --grace-period=0
  fi
done
```

### Verification
```bash
# New pod should have listening sockets
kubectl exec -n <namespace> <new-pod> -- ss -tlnp
# Should show the application's expected port (e.g., *:8080)

# Service should respond
kubectl exec -n <namespace> <new-pod> -- curl -sI http://localhost:<port>/
# Should return HTTP response
```

### Key Diagnostic Insight
The critical signal is **Running 1/1 but zero listening sockets**. Normal healthy pods
always have at least one listening socket for their application port. If `ss -tlnp`
returns nothing, the process is hung on a stale NFS mount, not crashed — that's why
Kubernetes thinks it's fine.

### Prevention
- Add **liveness probes** that hit the application's HTTP endpoint (not just TCP connect):
  ```hcl
  liveness_probe {
    http_get {
      path = "/"
      port = 8080
    }
    initial_delay_seconds = 60
    period_seconds        = 30
    timeout_seconds       = 5
  }
  ```
- This ensures Kubernetes detects hung pods and restarts them automatically.

## See Also
- TrueNAS NFS configuration documentation
- Kubernetes NFS volume documentation
- k8s-limitrange-oom-silent-kill (for OOM issues often confused with NFS hangs)
