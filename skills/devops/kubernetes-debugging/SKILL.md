---
name: kubernetes-debugging
description: "Kubernetes debugging for pod failures and networking."
user-invocable: false
context: fork
agent: kubernetes-helm-engineer
routing:
  triggers:
    - "kubernetes debug"
    - "pod failure"
    - "pod crashloop"
    - "kubectl logs"
    - "OOMKilled"
    - "pod pending"
  category: kubernetes
  pairs_with:
    - kubernetes-security
    - service-health-check
---

# Kubernetes Debugging Skill

Systematic diagnosis of pod failures, networking issues, and resource problems using a structured triage flow: describe, logs, events, exec.

## Reference Loading Table

| Signal | Reference | Size |
|--------|-----------|------|
| CrashLoopBackOff, OOMKilled, config error, health check, liveness probe, ImagePullBackOff, image pull, registry auth, Pending, FailedScheduling, node affinity, taint, PVC | `references/crash-diagnosis.md` | ~140 lines |
| service resolution, DNS, nslookup, CoreDNS, port-forward, NetworkPolicy, ingress, egress | `references/network-debugging.md` | ~50 lines |
| CPU throttling, memory limit, OOMKill, ephemeral storage, DiskPressure, debug container, distroless, kubectl reference, rollout, exec | `references/resource-debugging.md` | ~100 lines |

**Load greedily.** If the user's question touches any signal keyword, load the matching reference before responding. Multiple signals matching = load all matching references.

## Instructions

### Triage Flow

Follow this sequence for every pod or workload issue. Do not skip steps -- many failures (scheduling, image pull, volume mount) are only visible in events and describe output, not in logs, so jumping straight to logs misses them.

Always specify `-n <namespace>` explicitly in every command; never rely on the default context namespace, because the wrong namespace silently returns empty or misleading results.

```bash
# 1. Get an overview of the resource state
kubectl get pods -n <namespace> -o wide

# 2. Describe the resource for events, conditions, and status
kubectl describe pod <pod-name> -n <namespace>

# 3. Check current container logs
kubectl logs <pod-name> -n <namespace> -c <container-name>

# 4. Check previous container logs (critical for CrashLoopBackOff)
# Always check --previous before current logs for crashed containers,
# because deleting or restarting the pod destroys these logs permanently.
kubectl logs <pod-name> -n <namespace> -c <container-name> --previous

# 5. Check namespace events sorted by time
kubectl get events -n <namespace> --sort-by='.lastTimestamp'

# 6. If the container is running, exec in for live inspection
kubectl exec -it <pod-name> -n <namespace> -c <container-name> -- /bin/sh
```

Use read-only commands (describe, logs, get) to gather evidence before proposing any modifications. Never suggest changes based on assumptions -- gather diagnostic output first.

### Diagnosis Routing

Based on triage output, load the appropriate reference and follow its diagnosis flow:

| Symptom | Reference |
|---------|-----------|
| Pod status CrashLoopBackOff, ImagePullBackOff, or Pending | `references/crash-diagnosis.md` |
| Service unreachable, DNS failure, connection refused | `references/network-debugging.md` |
| CPU throttling, OOMKill, disk pressure, need debug container | `references/resource-debugging.md` |

### Error: "no endpoints available for service"
Cause: The Service selector does not match any running pod labels.
Solution: Compare `kubectl get svc <name> -o yaml` selector with `kubectl get pods --show-labels`. Fix the label mismatch.

---

## References

- [kubernetes-security skill](../kubernetes-security/SKILL.md) -- NetworkPolicy patterns and RBAC debugging
