---
name: k8s
description: Kubernetes debugging and troubleshooting skills. Debug pods, check logs, verify platform health.
---

# Kubernetes Debugging Skills

Skills for debugging and troubleshooting Kubernetes deployments.

## Available Sub-Skills

| Skill | Description |
|-------|-------------|
| `k8s:pods` | Troubleshoot pod issues (CrashLoopBackOff, ImagePull, etc.) |
| `k8s:logs` | Query and analyze pod/container logs |
| `k8s:health` | Check platform health and component status |
| `k8s:live-debugging` | Iterative debugging on running clusters |

## Quick Debugging

### Check Pod Status

```bash
# All pods
kubectl get pods -A

# Failed pods
kubectl get pods -A --field-selector=status.phase!=Running,status.phase!=Succeeded

# Specific namespace
kubectl get pods -n team1
```

### View Logs

```bash
# Agent logs
kubectl logs -n team1 deployment/weather-service --tail=100 -f

# Operator logs
kubectl logs -n kagenti-system -l app=kagenti-operator --tail=100
```

### Check Events

```bash
kubectl get events -A --sort-by='.lastTimestamp' | tail -30
```

### Platform Health

```bash
# All deployments
kubectl get deployments -A

# Services
kubectl get svc -A

# HTTPRoutes
kubectl get httproutes -A
```

## Common Issues

- **CrashLoopBackOff**: Check logs, resource limits, configuration
- **ImagePullBackOff**: Check registry auth, image name
- **Pending**: Check resource requests, node capacity
- **Evicted**: Check disk pressure, memory limits
