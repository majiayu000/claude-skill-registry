---
name: kubectl
description: "Manage Kubernetes clusters, deployments, pods, and services using kubectl."
metadata: {"thinkfleetbot":{"emoji":"☸️","requires":{"bins":["kubectl"]}}}
---

# kubectl

Manage Kubernetes clusters using kubectl CLI.

## Environment Variables

- `KUBECONFIG` - Path to kubeconfig file (optional, defaults to `~/.kube/config`)

## Cluster info

```bash
kubectl cluster-info
```

```bash
kubectl get nodes -o wide
```

## List resources

```bash
kubectl get pods -A --no-headers | head -30
```

```bash
kubectl get deployments -n default
```

```bash
kubectl get services -n default
```

```bash
kubectl get namespaces
```

## Describe a resource

```bash
kubectl describe pod my-pod -n default
```

```bash
kubectl describe deployment my-app -n default
```

## View logs

```bash
kubectl logs deployment/my-app -n default --tail=50
```

```bash
kubectl logs my-pod -n default -c my-container --tail=100
```

## Scale deployment

```bash
kubectl scale deployment my-app --replicas=3 -n default
```

## Restart deployment (rolling)

```bash
kubectl rollout restart deployment/my-app -n default
```

## Rollout status

```bash
kubectl rollout status deployment/my-app -n default
```

## Rollout history

```bash
kubectl rollout history deployment/my-app -n default
```

## Apply manifest

```bash
kubectl apply -f /tmp/manifest.yaml
```

## Get resource as YAML

```bash
kubectl get deployment my-app -n default -o yaml
```

## Port forward

```bash
kubectl port-forward svc/my-service 8080:80 -n default &
```

## Get events

```bash
kubectl get events -n default --sort-by='.lastTimestamp' | tail -20
```

## Top (resource usage)

```bash
kubectl top pods -n default
```

```bash
kubectl top nodes
```

## Notes

- Always specify `-n namespace` to avoid operating on the wrong namespace.
- Use `--dry-run=client -o yaml` to preview changes before applying.
- Confirm before running destructive operations (delete, scale to 0, drain).
- For multi-cluster setups, use `kubectl config use-context` to switch contexts.
