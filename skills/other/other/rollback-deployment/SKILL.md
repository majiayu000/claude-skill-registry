---
name: rollback-deployment
version: "1.0.0"
description: >
  Rollback a deployment to its previous revision. Use when a new deployment
  causes issues and needs to be reverted quickly. Keywords: rollback, revert,
  deployment, previous version, undo deployment.
metadata:
  domain: k8s
  category: remediation
  requires-approval: true
  confidence: 0.85
  mcp-servers:
    - kubernetes-mcp-server
---

# Rollback Deployment

## Preconditions

Before applying this skill, verify:

- Deployment name and namespace are known
- Previous revision exists
- Current revision is causing issues

## Actions

### 1. Get Current Deployment

Check current revision and status.

```yaml
mcp_tool: kubernetes-mcp-server/resources_get
params:
  apiVersion: apps/v1
  kind: Deployment
  name: $deployment_name
  namespace: $namespace
timeout: 30s
```

### 2. Get ReplicaSet History

List ReplicaSets to find previous revision.

```yaml
mcp_tool: kubernetes-mcp-server/resources_list
params:
  apiVersion: apps/v1
  kind: ReplicaSet
  namespace: $namespace
  labelSelector: app=$app_label
timeout: 30s
```

### 3. Rollback to Previous Revision

Update deployment to use previous ReplicaSet's spec.

```yaml
mcp_tool: kubernetes-mcp-server/resources_create_or_update
params:
  resource: |
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: $deployment_name
      namespace: $namespace
      annotations:
        kubernetes.io/change-cause: "Rollback by kubani remediator"
    spec:
      template:
        $previous_pod_spec
timeout: 60s
```

### 4. Verify Rollback

Confirm new pods are running with previous spec.

```yaml
mcp_tool: kubernetes-mcp-server/resources_get
params:
  apiVersion: apps/v1
  kind: Deployment
  name: $deployment_name
  namespace: $namespace
timeout: 30s
```

## Success Criteria

The skill succeeds when:

- [ ] Deployment revision incremented
- [ ] New pods running with previous spec
- [ ] All replicas available
- [ ] No pods in error state

## Failure Handling

If rollback fails:

1. Check if previous revision exists
2. Verify resource quotas allow rollback
3. Check for immutable field violations
4. May need manual intervention

## Examples

**Input Context:**
```json
{
  "deployment_name": "api-server",
  "namespace": "production",
  "app_label": "api-server"
}
```

**Output:**
```json
{
  "deployment": "api-server",
  "previous_revision": 5,
  "current_revision": 6,
  "rolled_back_to": 5,
  "replicas_available": 3,
  "success": true
}
```
