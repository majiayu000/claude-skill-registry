---
name: cluster-health
description: |
  Check Kubernetes cluster health and fix common issues. Use when:
  (1) User asks to check the cluster, check health, or "what's wrong",
  (2) User asks about pod status, node health, or deployment issues,
  (3) User asks to fix stuck pods, evicted pods, or CrashLoopBackOff,
  (4) User mentions "health check", "cluster status", "cluster health",
  (5) User asks "is everything running" or "any problems".
  Runs 8 standard K8s health checks with safe auto-fix for evicted pods
  and stuck CrashLoopBackOff pods.
author: Claude Code
version: 1.0.0
date: 2026-02-21
---

# Cluster Health Check

## Overview

- **Script**: `/workspace/infra/.claude/cluster-health.sh`
- **Schedule**: CronJob runs every 30 minutes in the `openclaw` namespace
- **Slack notifications**: Posts results to the webhook URL in `$SLACK_WEBHOOK_URL`
- **Auto-fix**: Automatically deletes evicted/failed pods and CrashLoopBackOff pods with >10 restarts
- **Exit code**: 0 = healthy, 1 = issues found

## Quick Check

Run the health check interactively:

```bash
# Report only, no Slack notification
bash /workspace/infra/.claude/cluster-health.sh --no-slack

# Full run with Slack notification
bash /workspace/infra/.claude/cluster-health.sh

# Report only, no auto-fix and no Slack
bash /workspace/infra/.claude/cluster-health.sh --no-fix --no-slack
```

## What It Checks

| # | Check | Auto-Fix | Alerts |
|---|-------|----------|--------|
| 1 | **Node Health** — NotReady nodes, MemoryPressure, DiskPressure, PIDPressure | No | Yes |
| 2 | **Pod Health** — CrashLoopBackOff, ImagePullBackOff, ErrImagePull, Error | Yes (CrashLoop >10 restarts) | Yes |
| 3 | **Evicted/Failed Pods** — Pods in `Failed` phase | Yes (deletes all) | Yes |
| 4 | **Failed Deployments** — Deployments with ready != desired replicas | No | Yes |
| 5 | **Pending PVCs** — PersistentVolumeClaims not in `Bound` state | No | Yes |
| 6 | **Resource Pressure** — Node CPU or memory >80% (warn) or >90% (issue) | No | Yes |
| 7 | **CronJob Failures** — Failed CronJob-owned Jobs in the last 24h | No | Yes |
| 8 | **DaemonSet Health** — DaemonSets with desired != ready | No | Yes |

## Safe Auto-Fix Rules

### Safe to auto-fix (the script does these automatically)

1. **Evicted/Failed pods** — These are already terminated and just cluttering the namespace:
   ```bash
   kubectl delete pods -A --field-selector=status.phase=Failed
   ```

2. **CrashLoopBackOff pods with >10 restarts** — The pod is stuck in a crash loop; deleting lets the controller recreate it with a fresh backoff timer:
   ```bash
   kubectl delete pod -n <namespace> <pod-name> --grace-period=0
   ```

### NEVER auto-fix (requires human investigation)

- **NotReady nodes** — Could be network, kubelet, or hardware issue; needs SSH investigation
- **DiskPressure / MemoryPressure / PIDPressure** — Root cause must be identified
- **ImagePullBackOff** — Usually a wrong image tag or registry issue; needs config fix
- **Failed deployments** — Could be resource limits, bad config, missing secrets
- **Pending PVCs** — Usually NFS export missing or storage class issue
- **Resource pressure >90%** — Need to identify which pods are consuming resources
- **CronJob failures** — Need to check job logs to understand why it failed
- **DaemonSet issues** — Could be node taints, resource limits, or image issues

## Deep Investigation

When the health check reports issues, use these commands to investigate further.

### Node Issues

```bash
# Describe the problematic node (events, conditions, capacity)
kubectl describe node <node-name>

# Check resource usage across all nodes
kubectl top nodes

# Check recent events on a specific node
kubectl get events --field-selector involvedObject.name=<node-name> --sort-by='.lastTimestamp'

# SSH to the node for direct inspection
ssh root@<node-ip>
systemctl status kubelet
journalctl -u kubelet --since "30 minutes ago" | tail -100
df -h
free -h
```

### Pod Issues

```bash
# Describe the pod (events, conditions, container statuses)
kubectl describe pod -n <namespace> <pod-name>

# Check current logs
kubectl logs -n <namespace> <pod-name> --tail=100

# Check logs from the previous crashed container
kubectl logs -n <namespace> <pod-name> --previous --tail=100

# Check events in the namespace
kubectl get events -n <namespace> --sort-by='.lastTimestamp' | tail -20

# Check all pods in a namespace
kubectl get pods -n <namespace> -o wide
```

### Deployment Issues

```bash
# Describe the deployment (strategy, conditions, events)
kubectl describe deployment -n <namespace> <deployment-name>

# Check rollout status
kubectl rollout status deployment -n <namespace> <deployment-name>

# Check rollout history
kubectl rollout history deployment -n <namespace> <deployment-name>

# Check the replicaset
kubectl get rs -n <namespace> -l app=<app-label>
```

### PVC Issues

```bash
# Describe the PVC (events, status, storage class)
kubectl describe pvc -n <namespace> <pvc-name>

# Check PVs
kubectl get pv

# Check events related to PVCs
kubectl get events -n <namespace> --field-selector reason=FailedMount --sort-by='.lastTimestamp'

# Verify NFS export exists
showmount -e 10.0.10.15 | grep <service-name>
```

### Resource Pressure

```bash
# Top nodes (CPU and memory usage)
kubectl top nodes

# Top pods sorted by memory (cluster-wide)
kubectl top pods -A --sort-by=memory | head -20

# Top pods sorted by CPU (cluster-wide)
kubectl top pods -A --sort-by=cpu | head -20

# Check resource requests/limits in a namespace
kubectl describe resourcequota -n <namespace>
kubectl describe limitrange -n <namespace>
```

## Common Remediation

### Persistent CrashLoopBackOff

A pod keeps crashing even after the auto-fix deletes it.

1. **Check logs from the crashed container**:
   ```bash
   kubectl logs -n <namespace> <pod-name> --previous --tail=200
   ```

2. **Check the pod description for clues**:
   ```bash
   kubectl describe pod -n <namespace> <pod-name>
   ```
   Look for:
   - `OOMKilled` in Last State — the container ran out of memory
   - `Error` with exit code 1 — application error (bad config, missing env var, DB connection failure)
   - `Error` with exit code 137 — killed by OOM killer or liveness probe
   - `Error` with exit code 143 — SIGTERM (graceful shutdown failure)

3. **Common causes**:
   - **OOMKilled**: Increase memory limits in Terraform (see below)
   - **Bad config**: Check environment variables, secrets, config maps
   - **DB connection failure**: Verify the database pod is running (`kubectl get pods -n dbaas`)
   - **NFS mount failure**: Verify NFS export exists (`showmount -e 10.0.10.15`)
   - **Missing secret**: Check if TLS secret or other secrets exist in the namespace

### OOMKilled

The container was killed because it exceeded its memory limit.

1. **Check current limits**:
   ```bash
   kubectl describe pod -n <namespace> <pod-name> | grep -A 5 "Limits"
   ```

2. **Fix in Terraform** — Edit `modules/kubernetes/<service>/main.tf` and increase the memory limit:
   ```hcl
   resources {
     limits = {
       memory = "2Gi"  # Increase from current value
     }
   }
   ```

3. **Apply the change**:
   ```bash
   cd /workspace/infra
   terraform apply -target=module.kubernetes_cluster.module.<service> -auto-approve
   ```

### ImagePullBackOff

The container image cannot be pulled.

1. **Check the exact error**:
   ```bash
   kubectl describe pod -n <namespace> <pod-name> | grep -A 5 "Events"
   ```

2. **Common causes**:
   - **Wrong image tag**: Verify the tag exists on the registry (Docker Hub, ghcr.io, etc.)
   - **Private registry without credentials**: Check if imagePullSecrets are configured
   - **Pull-through cache issue**: The registry cache at `10.0.20.10` may have a stale entry
     ```bash
     # Check pull-through cache ports:
     # 5000 = docker.io, 5010 = ghcr.io, 5020 = quay.io, 5030 = registry.k8s.io
     curl -s http://10.0.20.10:5000/v2/_catalog | python3 -m json.tool
     ```
   - **Registry rate limit**: Docker Hub free tier has pull limits; pull-through cache helps avoid this

3. **Fix**: Update the image tag in the service's Terraform module and re-apply.

### Node NotReady

A node has gone NotReady.

1. **Check node conditions**:
   ```bash
   kubectl describe node <node-name> | grep -A 20 "Conditions"
   ```

2. **SSH to the node and check kubelet**:
   ```bash
   ssh root@<node-ip>
   systemctl status kubelet
   journalctl -u kubelet --since "10 minutes ago" | tail -50
   ```

3. **Check resources**:
   ```bash
   # On the node
   df -h          # Disk space
   free -h        # Memory
   top -bn1       # CPU/processes
   ```

4. **Node IPs** (for SSH):
   - `10.0.20.100` — k8s-master
   - `10.0.20.101` — k8s-node1 (GPU)
   - `10.0.20.102` — k8s-node2
   - `10.0.20.103` — k8s-node3
   - `10.0.20.104` — k8s-node4

## Slack Webhook

The script posts results to the Slack incoming webhook URL in `$SLACK_WEBHOOK_URL`. The message format uses Slack mrkdwn:
- All clear: green checkmark with node/pod count
- Warnings only: warning icon with details
- Issues found: red alert icon with auto-fixes applied and remaining issues

The webhook URL is passed as an environment variable from `openclaw_skill_secrets` in `terraform.tfvars`.

## Infrastructure

| Component | Path / Location |
|-----------|----------------|
| Health check script | `/workspace/infra/.claude/cluster-health.sh` (in-pod) or `.claude/cluster-health.sh` (repo) |
| Terraform module | `modules/kubernetes/openclaw/main.tf` |
| CronJob definition | Defined in the OpenClaw Terraform module |
| Existing full healthcheck | `scripts/cluster_healthcheck.sh` (local-only, 24 checks with color output) |
| Infra repo (in pod) | `/workspace/infra` |
| kubectl (in pod) | `/tools/kubectl` |
| terraform (in pod) | `/tools/terraform` |

## Notes

1. This script is designed to run inside the OpenClaw pod where kubectl is pre-configured via the ServiceAccount
2. The full `scripts/cluster_healthcheck.sh` script runs 24 checks and is meant for local interactive use; this skill's script runs 8 core checks optimized for automated CronJob execution
3. When investigating issues interactively, prefer running commands directly rather than re-running the script
4. All Terraform changes must go through the `.tf` files — never use `kubectl apply/edit/patch` for persistent changes
