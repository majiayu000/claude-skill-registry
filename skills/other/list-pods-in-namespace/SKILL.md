---
name: list-pods-in-namespace
version: "1.0.0"
description: >
  List all pods in a specific namespace with their status. Used to get
  an overview of workload health. Keywords: list pods, namespace, pod status,
  workload overview, pod health.
metadata:
  domain: k8s
  category: collection
  requires-approval: false
  confidence: 0.95
  mcp-servers:
    - kubernetes-mcp-server
---

# List Pods in Namespace

## Preconditions

Before applying this skill, verify:

- Namespace is specified
- Need overview of pods in namespace

## Actions

### 1. List Pods in the Namespace

Retrieve all pods in the specified namespace with their status.

```yaml
mcp_tool: kubernetes-mcp-server/pods_list_in_namespace
params:
  namespace: $namespace
timeout: 30s
```

## Success Criteria

The skill succeeds when:

- [ ] Pod list retrieved with status
- [ ] Unhealthy pods identified

## Failure Handling

If list fails, check namespace existence and permissions.

## Examples

**Input Context:**
```json
{
  "namespace": "production"
}
```

**Expected Outcome:**
Complete list of pods in the namespace with their current status,
restart counts, and any pods not in Running state highlighted.
