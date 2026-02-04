---
name: kubernetes-operations
description: Assist with Kubernetes interactions including debugging (kubectl logs, describe, exec, port-forward), resource management (deployments, services, configmaps, secrets), and cluster operations (scaling, rollouts, node management). Use when working with kubectl, pods, deployments, services, or troubleshooting Kubernetes issues.
allowed-tools: Read, Grep, Glob, Bash
---

# Kubernetes Operations

> Comprehensive kubectl assistance for debugging, resource management, and cluster operations with token-efficient scripts.

## BEFORE YOU START

**This skill prevents 5 common errors and saves ~70% tokens.**

| Metric | Without Skill | With Skill |
|--------|--------------|------------|
| Pod Debugging | ~1200 tokens | ~400 tokens |
| Resource Listing | ~800 tokens | ~200 tokens |
| Cluster Health | ~1500 tokens | ~300 tokens |

### Known Issues This Skill Prevents

1. Running kubectl commands in wrong namespace/context
2. Verbose output flooding context with unnecessary data
3. Missing critical debugging steps (events, previous logs)
4. Exposing secrets in plain text output
5. Destructive operations without dry-run verification

## Quick Start

### Step 1: Verify Context

```bash
kubectl config current-context
kubectl config get-contexts
```

**Why this matters:** Running commands in the wrong cluster can cause production incidents.

### Step 2: Debug a Pod

```bash
uv run scripts/debug_pod.py <pod-name> [-n namespace]
```

**Why this matters:** The script combines describe, logs, and events into a condensed summary, saving ~800 tokens.

### Step 3: Check Cluster Health

```bash
uv run scripts/cluster_health.py
```

**Why this matters:** Quick overview of node status and unhealthy pods without verbose output.

## Critical Rules

### Always Do

- Always verify `kubectl config current-context` before operations
- Always use `-n namespace` to be explicit about target
- Always use `--dry-run=client -o yaml` before applying changes
- Always check events when debugging: `kubectl get events --sort-by='.lastTimestamp'`
- Always use `--previous` flag when pod is in CrashLoopBackOff

### Never Do

- Never run `kubectl delete` without `--dry-run` first in production
- Never output secrets without filtering: avoid `kubectl get secret -o yaml`
- Never assume default namespace - always specify `-n`
- Never ignore resource limits when debugging OOMKilled pods
- Never skip `describe` when logs show no errors

### Common Mistakes

**Wrong:**
```bash
kubectl logs my-pod
```

**Correct:**
```bash
kubectl logs my-pod -n my-namespace --tail=100 --timestamps
```

**Why:** Default namespace may not be correct, unlimited logs flood context, timestamps help correlate with events.

## Known Issues Prevention

| Issue | Root Cause | Solution |
|-------|-----------|----------|
| CrashLoopBackOff | App crash on startup | Check `kubectl logs --previous` and describe for exit codes |
| ImagePullBackOff | Registry auth or image tag | Verify image exists and check pull secrets |
| Pending pods | No schedulable nodes | Check node resources and pod affinity/tolerations |
| OOMKilled | Memory limit exceeded | Check container limits vs actual usage with `kubectl top` |
| Connection refused | Service selector mismatch | Verify pod labels match service selector |

## Debugging Workflows

### Pod Not Starting

```bash
# 1. Get pod status and events
kubectl describe pod <name> -n <namespace>

# 2. Check logs (current or previous)
kubectl logs <name> -n <namespace> --tail=100
kubectl logs <name> -n <namespace> --previous  # If restarting

# 3. Check events for scheduling issues
kubectl get events -n <namespace> --sort-by='.lastTimestamp' | grep <name>

# 4. Interactive debugging
kubectl exec -it <name> -n <namespace> -- /bin/sh
```

### Service Connectivity

```bash
# 1. Verify service exists and has endpoints
kubectl get svc <name> -n <namespace>
kubectl get endpoints <name> -n <namespace>

# 2. Check pod labels match service selector
kubectl get pods -n <namespace> --show-labels

# 3. Test from within cluster
kubectl run debug --rm -it --image=busybox -- wget -qO- http://<service>:<port>

# 4. Port-forward for local testing
kubectl port-forward svc/<name> 8080:80 -n <namespace>
```

## Resource Management

### Deployments

```bash
# List deployments
kubectl get deployments -n <namespace>

# Scale
kubectl scale deployment <name> --replicas=3 -n <namespace>

# Rollout status
kubectl rollout status deployment/<name> -n <namespace>

# Rollback
kubectl rollout undo deployment/<name> -n <namespace>

# History
kubectl rollout history deployment/<name> -n <namespace>
```

### ConfigMaps and Secrets

```bash
# List
kubectl get configmaps -n <namespace>
kubectl get secrets -n <namespace>

# View ConfigMap data
kubectl get configmap <name> -n <namespace> -o jsonpath='{.data}'

# View Secret keys (NOT values)
kubectl get secret <name> -n <namespace> -o jsonpath='{.data}' | jq 'keys'

# Create from file
kubectl create configmap <name> --from-file=<path> -n <namespace> --dry-run=client -o yaml
```

## Cluster Operations

### Node Management

```bash
# List nodes with status
kubectl get nodes -o wide

# Node details
kubectl describe node <name>

# Cordon (prevent scheduling)
kubectl cordon <node>

# Drain (evict pods)
kubectl drain <node> --ignore-daemonsets --delete-emptydir-data

# Uncordon
kubectl uncordon <node>
```

### Resource Usage

```bash
# Node resources
kubectl top nodes

# Pod resources
kubectl top pods -n <namespace>

# Sort by memory
kubectl top pods -n <namespace> --sort-by=memory
```

## Bundled Resources

### Scripts

Located in `scripts/`:
- `debug_pod.py` - Comprehensive pod debugging with condensed output
- `get_resources.py` - Resource summary using jsonpath for minimal tokens
- `cluster_health.py` - Quick cluster status overview

### References

Located in `references/`:
- [`kubectl-cheatsheet.md`](references/kubectl-cheatsheet.md) - Condensed command reference
- [`jsonpath-patterns.md`](references/jsonpath-patterns.md) - Common JSONPath expressions
- [`debugging-flowchart.md`](references/debugging-flowchart.md) - Decision tree for pod issues

> **Note:** For deep dives on specific topics, see the reference files above.

## Dependencies

### Required

| Package | Version | Purpose |
|---------|---------|---------|
| kubectl | 1.25+ | Kubernetes CLI |
| jq | 1.6+ | JSON parsing for scripts |

### Optional

| Package | Version | Purpose |
|---------|---------|---------|
| k9s | 0.27+ | Terminal UI for Kubernetes |
| stern | 1.25+ | Multi-pod log tailing |

## Official Documentation

- [kubectl Quick Reference](https://kubernetes.io/docs/reference/kubectl/quick-reference/)
- [JSONPath Support](https://kubernetes.io/docs/reference/kubectl/jsonpath/)
- [kubectl Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)
- [Debug Running Pods](https://kubernetes.io/docs/tasks/debug/debug-application/debug-running-pod/)

## Troubleshooting

### kubectl command not found

**Symptoms:** `command not found: kubectl`

**Solution:**
```bash
# macOS
brew install kubectl

# Verify
kubectl version --client
```

### Context not set

**Symptoms:** `error: no context is currently set`

**Solution:**
```bash
# List available contexts
kubectl config get-contexts

# Set context
kubectl config use-context <context-name>
```

### Permission denied

**Symptoms:** `Error from server (Forbidden)`

**Solution:**
```bash
# Check current user
kubectl auth whoami

# Check permissions
kubectl auth can-i get pods -n <namespace>
kubectl auth can-i --list -n <namespace>
```

### Timeout connecting to cluster

**Symptoms:** `Unable to connect to the server: dial tcp: i/o timeout`

**Solution:**
```bash
# Check cluster endpoint
kubectl cluster-info

# Verify network connectivity
curl -k https://<cluster-api-endpoint>/healthz

# Check kubeconfig
cat ~/.kube/config
```

## Setup Checklist

Before using this skill, verify:

- [ ] `kubectl` installed (`kubectl version --client`)
- [ ] Kubeconfig configured (`~/.kube/config` exists)
- [ ] Context set to correct cluster (`kubectl config current-context`)
- [ ] Permissions verified (`kubectl auth can-i get pods`)
- [ ] `jq` installed for JSON parsing (`jq --version`)
