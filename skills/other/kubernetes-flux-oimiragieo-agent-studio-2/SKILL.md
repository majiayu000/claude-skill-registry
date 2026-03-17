---
name: kubernetes-flux
description: Kubernetes cluster management and troubleshooting. Query pods, deployments, services, logs, and events. Supports context switching, scaling, and rollout management. Use for Kubernetes debugging, monitoring, and operations.
version: 1.0
model: sonnet
invoked_by: both
user_invocable: true
tools: [Read, Write, Bash]
best_practices:
  - Verify kubectl is configured before operations
  - Use namespace flags for clarity
  - Check current context before cluster operations
  - Avoid destructive operations without confirmation
  - Mask secrets in output
error_handling: graceful
streaming: supported
safety_level: high
---

# Kubernetes Flux Skill

## Installation

The skill invokes the **Flux** CLI. Install:

- **macOS/Linux (Homebrew)**: `brew install fluxcd/tap/flux`
- **macOS/Linux (script)**: `curl -s https://fluxcd.io/install.sh | sudo bash`
- **Windows (winget)**: `winget install -e --id FluxCD.Flux`
- **Windows (Chocolatey)**: `choco install flux`
- **Custom dir**: `curl -s https://fluxcd.io/install.sh | bash -s ~/.local/bin`

Verify: `flux --version`. Then use `flux bootstrap` to deploy controllers if needed.

## Cheat Sheet & Best Practices

**Bootstrap:** `flux bootstrap git --url=ssh://git@host/repo.git --path=clusters/my-cluster`; use `--branch`, `--interval`, `--private-key-file` or `--token-auth` as needed.

**Status:** `flux check` — controllers/CRDs; `flux get all -A` — all resources; `flux get kustomizations`; `flux tree kustomization <name>` — managed objects.

**Hacks:** Use `flux get sources git` and `flux get kustomizations` to see sync state. Reconcile on demand: `flux reconcile kustomization <name> --with-source`. Pin versions with `FLUX_VERSION` on install script. Prefer Git over Helm for app manifests when using GitOps.

## Certifications & Training

**Kubernetes:** [CKA](https://kubernetes.io/training/) / [CKAD](https://www.cncf.io/training/certification/ckad/) (Linux Foundation). **Flux:** [GitOps with Flux (LFS269)](https://training.linuxfoundation.org/training/gitops-continuous-delivery-on-kubernetes-with-flux-lfs269/). **Skill data:** Bootstrap, reconcile, status (`flux check`, `flux get all`), tree; GitOps workflow.

## Hooks & Workflows

**Suggested hooks:** Pre-apply: `flux check`. Post-push (to Git repo used by Flux): optional reconcile trigger. Use with **devops** (always) for GitOps clusters.

**Workflows:** Use with **devops** (always). Flow: bootstrap or reconcile; debug with `flux get all`, `flux tree kustomization`. See `gitops-workflow` skill and enterprise workflows.

## Overview

This skill provides comprehensive Kubernetes cluster management through kubectl, enabling AI agents to inspect, troubleshoot, and manage Kubernetes resources.

## When to Use

- Debugging application pods and containers
- Monitoring deployment rollouts and status
- Analyzing service networking and endpoints
- Investigating cluster events and errors
- Troubleshooting performance issues
- Managing application scaling
- Port forwarding for local development

## Requirements

- kubectl installed and configured
- Valid KUBECONFIG file or default context
- Cluster access credentials
- Appropriate RBAC permissions

## Quick Reference

```bash
# Get pods in current namespace
kubectl get pods

# Get pods in specific namespace
kubectl get pods -n production

# Get pods with labels
kubectl get pods -l app=web -n production

# Describe a pod
kubectl describe pod my-app-123 -n default

# Get pod logs
kubectl logs my-app-123 -n default

# Get logs with tail
kubectl logs my-app-123 -n default --tail=100

# Get logs since time
kubectl logs my-app-123 -n default --since=1h

# List recent events
kubectl get events -n default --sort-by='.lastTimestamp' | tail -20

# Watch events in real-time
kubectl get events -n default -w
```

## Resource Discovery

### Pods

```bash
# List all pods
kubectl get pods -n <namespace>

# List pods with wide output
kubectl get pods -n <namespace> -o wide

# List pods across all namespaces
kubectl get pods -A

# Filter by label
kubectl get pods -l app=nginx -n <namespace>
```

### Deployments

```bash
# List deployments
kubectl get deployments -n <namespace>

# Get deployment details
kubectl describe deployment <name> -n <namespace>

# Check rollout status
kubectl rollout status deployment/<name> -n <namespace>
```

### Services

```bash
# List services
kubectl get svc -n <namespace>

# Describe service
kubectl describe svc <name> -n <namespace>

# Get endpoints
kubectl get endpoints <name> -n <namespace>
```

### ConfigMaps and Secrets

```bash
# List ConfigMaps
kubectl get configmaps -n <namespace>

# Describe ConfigMap
kubectl describe configmap <name> -n <namespace>

# Get ConfigMap data
kubectl get configmap <name> -n <namespace> -o yaml

# List Secrets (names only)
kubectl get secrets -n <namespace>

# Describe Secret (values masked)
kubectl describe secret <name> -n <namespace>
```

### Namespaces

```bash
# List namespaces
kubectl get namespaces

# Get namespace details
kubectl describe namespace <name>
```

## Troubleshooting

### Pod Debugging

```bash
# Describe pod for events and conditions
kubectl describe pod <name> -n <namespace>

# Get pod logs
kubectl logs <pod-name> -n <namespace>

# Get logs from specific container
kubectl logs <pod-name> -c <container-name> -n <namespace>

# Get previous container logs (after crash)
kubectl logs <pod-name> -n <namespace> --previous

# Exec into pod
kubectl exec -it <pod-name> -n <namespace> -- /bin/sh

# Run command in pod
kubectl exec <pod-name> -n <namespace> -- ls -la /app
```

### Events

```bash
# List events sorted by time
kubectl get events -n <namespace> --sort-by='.lastTimestamp'

# Filter warning events
kubectl get events -n <namespace> --field-selector type=Warning

# Watch events live
kubectl get events -n <namespace> -w
```

## Management Operations

### Scaling

```bash
# Scale deployment
kubectl scale deployment <name> --replicas=5 -n <namespace>

# Autoscale deployment
kubectl autoscale deployment <name> --min=2 --max=10 --cpu-percent=80 -n <namespace>
```

### Rollouts

```bash
# Check rollout status
kubectl rollout status deployment/<name> -n <namespace>

# View rollout history
kubectl rollout history deployment/<name> -n <namespace>

# Rollback to previous version
kubectl rollout undo deployment/<name> -n <namespace>

# Rollback to specific revision
kubectl rollout undo deployment/<name> --to-revision=2 -n <namespace>
```

### Port Forwarding

```bash
# Forward local port to pod
kubectl port-forward <pod-name> 8080:80 -n <namespace>

# Forward to service
kubectl port-forward svc/<service-name> 8080:80 -n <namespace>
```

## Context Management

```bash
# Get current context
kubectl config current-context

# List all contexts
kubectl config get-contexts

# Switch context
kubectl config use-context <context-name>

# Set default namespace
kubectl config set-context --current --namespace=<namespace>
```

## Common Workflows

### Troubleshoot a Failing Pod

```bash
# 1. Find the problematic pod
kubectl get pods -n production

# 2. Describe for events
kubectl describe pod <pod-name> -n production

# 3. Check events
kubectl get events -n production --sort-by='.lastTimestamp' | tail -20

# 4. Get logs
kubectl logs <pod-name> -n production --tail=200
```

### Monitor Deployment Rollout

```bash
# 1. Check deployment status
kubectl get deployments -n production

# 2. Watch rollout
kubectl rollout status deployment/<name> -n production

# 3. Watch pods
kubectl get pods -l app=<app-name> -n production -w
```

### Debug Service Connectivity

```bash
# 1. Check service
kubectl describe svc <name> -n <namespace>

# 2. Check endpoints
kubectl get endpoints <name> -n <namespace>

# 3. Check backing pods
kubectl get pods -l <service-selector> -n <namespace>

# 4. Port forward for testing
kubectl port-forward svc/<name> 8080:80 -n <namespace>
```

## Safety Features

### Blocked Operations

The following are dangerous and require confirmation:

- `kubectl delete` commands
- Destructive exec commands (rm, dd, mkfs)
- Scale to 0 replicas in production

### Masked Output

Secret values are always masked. Only metadata shown.

## Error Handling

| Error                       | Cause               | Fix                   |
| --------------------------- | ------------------- | --------------------- |
| `kubectl not found`         | Not installed       | Install kubectl       |
| `Unable to connect`         | Cluster unreachable | Check network/VPN     |
| `Forbidden`                 | RBAC permissions    | Request permissions   |
| `NotFound`                  | Resource missing    | Verify name/namespace |
| `context deadline exceeded` | Timeout             | Check cluster health  |

## Related

- kubectl docs: https://kubernetes.io/docs/reference/kubectl/
- Kubernetes API: https://kubernetes.io/docs/reference/kubernetes-api/

## Memory Protocol (MANDATORY)

**Before starting:**

```bash
cat .claude/context/memory/learnings.md
```

**After completing:** Record any new patterns or exceptions discovered.

> ASSUME INTERRUPTION: Your context may reset. If it's not in memory, it didn't happen.
