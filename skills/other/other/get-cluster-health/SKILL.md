---
name: get-cluster-health
version: "1.0.0"
description: >
  Get overall cluster health status. Checks node readiness, system pod health,
  and control plane components. Use for periodic health checks or incident
  investigation. Keywords: cluster health, node status, cluster status, health check.
metadata:
  domain: k8s
  category: collection
  requires-approval: false
  confidence: 0.9
  mcp-servers:
    - kubernetes-mcp-server
---

# Get Cluster Health

## Preconditions

Before applying this skill, verify:

- Kubernetes cluster is accessible
- kubectl/MCP has cluster-admin or read permissions

## Actions

### 1. Get Node Status

List all nodes and their readiness status.

```yaml
mcp_tool: kubernetes-mcp-server/resources_list
params:
  apiVersion: v1
  kind: Node
timeout: 30s
```

### 2. Get System Pod Health

Check pods in kube-system namespace for any issues.

```yaml
mcp_tool: kubernetes-mcp-server/pods_list_in_namespace
params:
  namespace: kube-system
timeout: 30s
```

### 3. Get Recent Events

Check for warning events across the cluster.

```yaml
mcp_tool: kubernetes-mcp-server/events_list
params: {}
timeout: 30s
```

## Success Criteria

The skill succeeds when:

- [ ] All nodes are in Ready state
- [ ] All kube-system pods are Running
- [ ] No critical warning events in last hour

## Failure Handling

If nodes are NotReady or pods are failing:

1. Capture current state for analysis
2. Trigger diagnostic skills for specific issues
3. Escalate if multiple nodes or critical pods affected

## Examples

**Output:**
```json
{
  "nodes": {
    "total": 3,
    "ready": 3,
    "not_ready": 0
  },
  "system_pods": {
    "total": 12,
    "running": 12,
    "failed": 0
  },
  "warnings": 0,
  "healthy": true
}
```
