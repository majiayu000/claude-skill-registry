---
name: cluster-audit
description: Full cluster state audit. Use when asked for cluster status, health check, or infrastructure audit. Produces comprehensive report of all nodes, pods, services, PVCs, GPUs, and issues.
allowed-tools: Bash, Read
---

# Cluster Audit

Run a comprehensive audit of the Kaizen K8s cluster. Execute ALL of these in sequence:

1. **Nodes**: `kubectl get nodes -o wide`
2. **All Pods**: `kubectl get pods -A -o wide`
3. **Problem Pods**: `kubectl get pods -A --field-selector=status.phase!=Running,status.phase!=Succeeded`
4. **Services**: `kubectl get svc -A`
5. **PVCs**: `kubectl get pvc -A`
6. **GPU Allocation**: `kubectl describe nodes | grep -A5 "nvidia.com/gpu"`
7. **Recent Events**: `kubectl get events -A --sort-by=.lastTimestamp --no-headers | tail -20`
8. **Inference Health**: `curl -s --max-time 3 http://10.10.10.10:30000/v1/models` and `curl -s --max-time 3 http://10.10.10.10:30001/v1/models`
9. **Cognitive Health**: `curl -s --max-time 3 http://10.10.10.10:30800/health` and `curl -s --max-time 3 http://10.10.10.10:30810/health`

Produce a summary table:
| Component | Status | Details |
|-----------|--------|---------|

Flag any CrashLoopBackOff, OOMKilled, or Pending pods. Note GPU utilization vs allocation.
