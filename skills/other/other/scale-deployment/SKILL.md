---
name: scale-deployment
version: "1.0.0"
description: >
  Scale a deployment to a specified number of replicas. Used for both scaling
  up (to handle load) and scaling down. Keywords: scale, replicas, deployment,
  statefulset, horizontal scaling, pod count.
metadata:
  domain: k8s
  category: remediation
  requires-approval: true
  confidence: 0.90
  mcp-servers:
    - kubernetes-mcp-server
---

# Scale Deployment Replicas

## Preconditions

Before applying this skill, verify:

- Resource is a Deployment or StatefulSet
- Target replica count is within configured limits (1-10)
- Current replica count differs from target

## Actions

### 1. Scale the Deployment

Scale the deployment to the target number of replicas.

```yaml
mcp_tool: kubernetes-mcp-server/resources_scale
params:
  apiVersion: apps/v1
  kind: $resource_kind
  name: $deployment_name
  namespace: $namespace
  scale: $target_replicas
timeout: 60s
```

## Success Criteria

The skill succeeds when:

- [ ] Deployment shows target replica count
- [ ] All replicas become Ready within 5 minutes

## Failure Handling

If scaling fails:

1. Check resource quotas in namespace
2. Verify node capacity
3. Check for PVC binding issues
4. Escalate if pods cannot schedule

## Examples

**Input Context:**
```json
{
  "deployment_name": "api-server",
  "namespace": "production",
  "resource_kind": "Deployment",
  "current_replicas": 2,
  "target_replicas": 5
}
```

**Expected Outcome:**
Deployment scaled to 5 replicas, all pods Running within 5 minutes.
