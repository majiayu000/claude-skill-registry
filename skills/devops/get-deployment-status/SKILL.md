---
name: get-deployment-status
version: "1.0.0"
description: >
  Get deployment health and replica status. Checks if deployment has desired
  replicas, available pods, and recent rollout status. Use to verify deployments
  are healthy. Keywords: deployment status, replica count, rollout, deployment health.
metadata:
  domain: k8s
  category: collection
  requires-approval: false
  confidence: 0.9
  mcp-servers:
    - kubernetes-mcp-server
---

# Get Deployment Status

## Preconditions

Before applying this skill, verify:

- Deployment name is known
- Namespace is specified

## Actions

### 1. Get Deployment Details

Retrieve deployment specification and status.

```yaml
mcp_tool: kubernetes-mcp-server/resources_get
params:
  apiVersion: apps/v1
  kind: Deployment
  name: $deployment_name
  namespace: $namespace
timeout: 30s
```

### 2. Get ReplicaSet Status

Check current and previous ReplicaSets.

```yaml
mcp_tool: kubernetes-mcp-server/resources_list
params:
  apiVersion: apps/v1
  kind: ReplicaSet
  namespace: $namespace
  labelSelector: app=$app_label
timeout: 30s
```

### 3. Get Pod Status

Check status of pods owned by deployment.

```yaml
mcp_tool: kubernetes-mcp-server/pods_list_in_namespace
params:
  namespace: $namespace
  labelSelector: app=$app_label
timeout: 30s
```

## Success Criteria

The skill succeeds when:

- [ ] Deployment exists and is accessible
- [ ] Desired replicas equals available replicas
- [ ] All pods are in Running state

## Failure Handling

If deployment is unhealthy:

1. Return current vs desired replica counts
2. List any failing pods
3. Return recent events for the deployment

## Examples

**Input Context:**
```json
{
  "deployment_name": "nginx",
  "namespace": "default",
  "app_label": "nginx"
}
```

**Output:**
```json
{
  "deployment": "nginx",
  "namespace": "default",
  "desired": 3,
  "available": 3,
  "ready": 3,
  "healthy": true,
  "strategy": "RollingUpdate"
}
```
