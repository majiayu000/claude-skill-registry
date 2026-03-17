---
name: kubernetes-mcp
description: Query Kubernetes resources for diagnostics, verification, and infrastructure validation.
agents: [bolt, tess, rex, grizz, nova]
triggers: [kubernetes, k8s, pod, deployment, service, cluster, kubectl]
---

# Kubernetes MCP (Cluster Operations)

Use Kubernetes MCP tools to query cluster resources for diagnostics and verification.

## Tools

| Tool | Purpose |
|------|---------|
| `kubernetes_listResources` | List resources of a specific type |
| `kubernetes_getResource` | Get detailed resource info |

## Listing Resources

```
# List all pods in a namespace
kubernetes_listResources({
  kind: "Pod",
  namespace: "my-service"
})

# List deployments
kubernetes_listResources({
  kind: "Deployment",
  namespace: "my-service"
})
```

## Getting Resource Details

```
# Get pod details
kubernetes_getResource({
  kind: "Pod",
  name: "my-service-abc123",
  namespace: "my-service"
})

# Get service endpoints
kubernetes_getResource({
  kind: "Service",
  name: "my-service",
  namespace: "my-service"
})
```

## Common Resources

| Resource | Use Case |
|----------|----------|
| **Pod** | Check running containers, logs |
| **Deployment** | Verify replicas, rollout status |
| **Service** | Check endpoints, ports |
| **ConfigMap** | Read configuration values |
| **Secret** | Verify secret existence (not values) |
| **PersistentVolumeClaim** | Check storage provisioning |
| **Cluster** | Database cluster status (CloudNative-PG) |

## Infrastructure Verification

```
# Verify database is ready
kubernetes_getResource({
  kind: "Cluster",
  name: "my-db",
  namespace: "my-service"
})
# Check: status.phase == "Cluster in healthy state"

# Verify Redis is running
kubernetes_listResources({
  kind: "Pod",
  namespace: "my-service",
  labelSelector: "app=redis"
})
```

## Best Practices

1. **Always specify namespace** - Avoid cluster-wide queries
2. **Check status fields** - Not just existence
3. **Use label selectors** - Filter relevant resources
4. **Verify before proceeding** - Wait for Ready status
