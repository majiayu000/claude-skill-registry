---
name: check-workflow-health
version: "1.0.0"
description: >
  Check health of Temporal workflows in the cluster. Verifies Temporal server
  pods are running and checks for stuck or failed workflows. Use for monitoring
  workflow orchestration health. Keywords: Temporal, workflow, workflow stuck,
  workflow failed, orchestration.
metadata:
  domain: k8s
  category: diagnostic
  requires-approval: false
  confidence: 0.85
  mcp-servers:
    - kubernetes-mcp-server
---

# Check Workflow Health

## Preconditions

Before applying this skill, verify:

- Temporal is deployed in the cluster
- Temporal namespace is known (default: temporal)

## Actions

### 1. Check Temporal Pods

Verify Temporal server components are running.

```yaml
mcp_tool: kubernetes-mcp-server/pods_list_in_namespace
params:
  namespace: temporal
timeout: 30s
```

### 2. Get Temporal Pod Logs

Check for errors in Temporal server logs.

```yaml
mcp_tool: kubernetes-mcp-server/pods_log
params:
  name: temporal-server-0
  namespace: temporal
  tail: 100
timeout: 30s
```

### 3. Check Worker Pods

Verify worker pods are running and connected.

```yaml
mcp_tool: kubernetes-mcp-server/pods_list_in_namespace
params:
  namespace: ai-agents
  labelSelector: app.kubernetes.io/component=worker
timeout: 30s
```

### 4. Get Temporal Events

Check for any Temporal-related events.

```yaml
mcp_tool: kubernetes-mcp-server/events_list
params:
  namespace: temporal
timeout: 30s
```

## Success Criteria

The skill succeeds when:

- [ ] All Temporal pods are Running
- [ ] No error patterns in recent logs
- [ ] Worker pods are connected

## Failure Handling

If Temporal is unhealthy:

1. Check Temporal UI for workflow status
2. Review server logs for connection issues
3. Verify database connectivity

## Examples

**Output:**
```json
{
  "temporal_pods": {
    "server": "Running",
    "frontend": "Running",
    "history": "Running",
    "matching": "Running"
  },
  "workers": {
    "k8s-monitor": "Running",
    "news-monitor": "Running"
  },
  "recent_errors": [],
  "healthy": true
}
```
