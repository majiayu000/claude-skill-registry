---
name: kubernetes-troubleshooting
description: Diagnose and fix common Kubernetes issues including pod failures, networking problems, and resource constraints.
---

# Kubernetes Troubleshooting

## Overview
You are a Kubernetes troubleshooting expert. Use these procedures to diagnose and fix common Kubernetes issues.

## When to Use
Use this skill when the user reports issues with Kubernetes pods, services, deployments, or cluster resources.

## Diagnostic Procedures

### Pod Not Starting
1. Check pod status: `kubectl get pods -n <namespace>`
2. Describe the pod: `kubectl describe pod <name> -n <namespace>`
3. Check events: `kubectl get events -n <namespace> --sort-by='.lastTimestamp'`
4. Check logs: `kubectl logs <pod-name> -n <namespace> --previous` (if crash-looping)

### Common Causes
- **ImagePullBackOff**: Wrong image name, missing registry credentials, or network issues
- **CrashLoopBackOff**: Application crash — check logs, resource limits, missing config
- **Pending**: Insufficient resources, node affinity/taint issues, PVC not bound
- **OOMKilled**: Increase memory limits in the deployment spec

### Service Not Reachable
1. Verify service exists: `kubectl get svc -n <namespace>`
2. Check endpoints: `kubectl get endpoints <service-name> -n <namespace>`
3. Test DNS resolution: `kubectl run tmp --image=busybox --rm -it -- nslookup <service-name>`
4. Check network policies: `kubectl get networkpolicies -n <namespace>`

### Resource Debugging
- View resource usage: `kubectl top pods -n <namespace>`
- Check node capacity: `kubectl describe nodes | grep -A 5 "Allocated resources"`
- View resource quotas: `kubectl get resourcequota -n <namespace>`

## Best Practices
- Always check events first — they often reveal the root cause immediately
- Use `--previous` flag on logs for crash-looping pods
- Check resource limits before scaling up nodes
