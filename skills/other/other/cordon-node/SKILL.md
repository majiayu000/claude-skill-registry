---
name: cordon-node
version: "1.0.0"
description: >
  Mark a node as unschedulable to prevent new pods from being scheduled.
  Use when a node is experiencing issues and needs maintenance. Existing
  pods continue running. Keywords: cordon, node maintenance, unschedulable,
  node issues.
metadata:
  domain: k8s
  category: remediation
  requires-approval: true
  confidence: 0.9
  mcp-servers:
    - kubernetes-mcp-server
---

# Cordon Node

## Preconditions

Before applying this skill, verify:

- Node name is known
- Node is currently schedulable
- Cordoning won't cause capacity issues

## Actions

### 1. Verify Node Status

Check current node state before cordoning.

```yaml
mcp_tool: kubernetes-mcp-server/resources_get
params:
  apiVersion: v1
  kind: Node
  name: $node_name
timeout: 30s
```

### 2. Cordon the Node

Mark node as unschedulable using patch.

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

### 3. Verify Cordon Status

Confirm node is now unschedulable.

```yaml
mcp_tool: kubernetes-mcp-server/resources_get
params:
  apiVersion: v1
  kind: Node
  name: $node_name
timeout: 30s
```

## Success Criteria

The skill succeeds when:

- [ ] Node spec.unschedulable is true
- [ ] Node shows SchedulingDisabled condition
- [ ] Existing pods continue running

## Failure Handling

If cordoning fails:

1. Check node exists
2. Verify cluster permissions
3. Check for control plane issues

## Examples

**Input Context:**
```json
{
  "node_name": "worker-node-3"
}
```

**Output:**
```json
{
  "node": "worker-node-3",
  "previous_state": "schedulable",
  "current_state": "unschedulable",
  "running_pods": 15,
  "success": true
}
```
