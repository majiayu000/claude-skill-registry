---
name: restart-crashloop
version: "1.0.0"
description: >
  Restart a pod stuck in CrashLoopBackOff. Use when pod has crashed 3+ times
  and a restart might resolve transient issues. Keywords: crashloop, restart,
  pod failure, container crash, pod stuck, pod crashing.
metadata:
  domain: k8s
  category: remediation
  requires-approval: false
  confidence: 0.85
  mcp-servers:
    - kubernetes-mcp-server
---

# Restart CrashLoopBackOff Pod

## Preconditions

Before applying this skill, verify:

- Pod status is CrashLoopBackOff
- Pod has restarted more than 3 times
- Pod is NOT part of a Job or CronJob
- No OOMKilled events in last 10 minutes

## Actions

### 1. Delete Pod to Trigger Recreation

Use the kubernetes-mcp-server to delete the pod. The deployment controller
will automatically create a replacement pod.

```yaml
mcp_tool: kubernetes-mcp-server/pods_delete
params:
  name: $pod_name
  namespace: $namespace
timeout: 30s
```

## Success Criteria

The skill succeeds when:

- [ ] New pod created within 30 seconds
- [ ] New pod reaches Running state within 2 minutes
- [ ] No CrashLoopBackOff within 5 minutes of restart

## Failure Handling

If the pod does not reach Running state:

1. Check events for the new pod
2. Check logs from the new pod
3. Escalate to human if pattern repeats 3 times

## Examples

**Input Context:**
```json
{
  "pod_name": "nginx-deployment-abc123",
  "namespace": "default",
  "restart_count": 5,
  "status": "CrashLoopBackOff"
}
```

**Expected Outcome:**
Pod deleted, new pod reaches Running within 2 minutes.
