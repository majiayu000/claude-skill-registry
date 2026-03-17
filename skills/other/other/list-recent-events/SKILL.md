---
name: list-recent-events
version: "1.0.0"
description: >
  Collect recent Kubernetes events to identify issues. Events reveal
  warnings, errors, and state changes. Keywords: events, warnings, errors,
  cluster activity, state changes, recent events.
metadata:
  domain: k8s
  category: collection
  requires-approval: false
  confidence: 0.95
  mcp-servers:
    - kubernetes-mcp-server
---

# List Recent Cluster Events

## Preconditions

Before applying this skill, verify:

- Need to understand recent cluster activity
- Looking for warnings or errors

## Actions

### 1. List Events from All Namespaces

Retrieve recent events from across the cluster.

```yaml
mcp_tool: kubernetes-mcp-server/events_list
params: {}
timeout: 60s
```

## Success Criteria

The skill succeeds when:

- [ ] Events retrieved successfully
- [ ] Warnings/errors identified and categorized

## Failure Handling

If events unavailable, check API server connectivity.

## Examples

**Input Context:**
```json
{
  "reason": "routine health check",
  "time_range": "last 1 hour"
}
```

**Expected Outcome:**
List of recent events with warnings and errors highlighted,
categorized by severity and resource type.
