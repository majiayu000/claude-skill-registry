---
name: drain-node
version: "1.0.0"
description: >
  Safely evict all pods from a node for maintenance. Cordons the node first,
  then evicts pods respecting PodDisruptionBudgets. Use before node maintenance
  or decommissioning. Keywords: drain, evict, node maintenance, pod migration.
metadata:
  domain: k8s
  category: remediation
  requires-approval: true
  confidence: 0.8
  mcp-servers:
    - kubernetes-mcp-server
---

# Drain Node

## Preconditions

Before applying this skill, verify:

- Node name is known
- Other nodes have capacity for evicted pods
- PodDisruptionBudgets won't block critical evictions
- DaemonSet pods are acceptable to ignore

## Actions

### 1. Cordon the Node First

Prevent new pods from scheduling.

```yaml
mcp_tool: kubernetes-mcp-server/resources_create_or_update
params:
  resource: |
    apiVersion: v1
    kind: Node
    metadata:
      name: $node_name
    spec:
      unschedulable: true
timeout: 30s
```

### 2. Get Pods on Node

List all pods running on the node.

```yaml
mcp_tool: kubernetes-mcp-server/pods_list
params:
  labelSelector: ""
timeout: 30s
```

### 3. Evict Each Pod

Delete pods to trigger rescheduling (skip DaemonSets).

```yaml
mcp_tool: kubernetes-mcp-server/pods_delete
params:
  name: $pod_name
  namespace: $pod_namespace
timeout: 30s
```

### 4. Verify Node is Drained

Confirm only DaemonSet pods remain.

```yaml
mcp_tool: kubernetes-mcp-server/pods_list
params:
  labelSelector: ""
timeout: 30s
```

## Success Criteria

The skill succeeds when:

- [ ] Node is cordoned
- [ ] All non-DaemonSet pods evicted
- [ ] Evicted pods rescheduled elsewhere
- [ ] No unexpected errors during eviction

## Failure Handling

If draining fails:

1. Check PodDisruptionBudget constraints
2. Identify stuck pods (finalizers, etc.)
3. May need to force delete specific pods
4. Uncordon if drain aborted

## Examples

**Input Context:**
```json
{
  "node_name": "worker-node-3",
  "ignore_daemonsets": true,
  "force": false
}
```

**Output:**
```json
{
  "node": "worker-node-3",
  "pods_evicted": 12,
  "daemonset_pods_skipped": 3,
  "pods_rescheduled": 12,
  "success": true
}
```
