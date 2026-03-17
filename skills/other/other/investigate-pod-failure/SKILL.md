---
name: investigate-pod-failure
version: "1.0.0"
description: >
  Deep investigation of a failing pod. Gathers logs, events, and resource
  status to identify root cause. Keywords: investigate, debug, pod failure,
  troubleshoot, root cause, logs, events.
metadata:
  domain: k8s
  category: diagnostic
  requires-approval: false
  confidence: 0.95
  mcp-servers:
    - kubernetes-mcp-server
---

# Investigate Pod Failure

## Preconditions

Before applying this skill, verify:

- Pod is in a failed or error state
- Pod has been created (not stuck in Pending)

## Actions

### 1. Get Pod Status and Details

Retrieve the full pod specification and current status.

```yaml
mcp_tool: kubernetes-mcp-server/pods_get
params:
  name: $pod_name
  namespace: $namespace
timeout: 30s
```

### 2. Get Pod Logs

Retrieve recent logs from the pod container.

```yaml
mcp_tool: kubernetes-mcp-server/pods_log
params:
  name: $pod_name
  namespace: $namespace
  tail: 100
timeout: 30s
```

### 3. Get Recent Events

Retrieve recent events related to the pod.

```yaml
mcp_tool: kubernetes-mcp-server/events_list
params:
  namespace: $namespace
timeout: 30s
```

## Success Criteria

The skill succeeds when:

- [ ] Root cause identified from logs or events
- [ ] Investigation produces actionable findings

## Failure Handling

If investigation is inconclusive:

1. Check previous container logs (--previous flag)
2. Describe the pod for more context
3. Check node events if pod failed to schedule
4. Escalate with all gathered data

## Examples

**Input Context:**
```json
{
  "pod_name": "backend-api-abc123",
  "namespace": "production",
  "status": "Error",
  "exit_code": 1
}
```

**Expected Outcome:**
Investigation reveals root cause (e.g., missing config, connection refused,
OOM killed) with specific actionable recommendations.
