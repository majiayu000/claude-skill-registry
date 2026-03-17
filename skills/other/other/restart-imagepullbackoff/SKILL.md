---
name: restart-imagepullbackoff
version: "1.0.0"
description: >
  Handle a pod stuck in ImagePullBackOff state. First investigates the image
  pull error, then restarts to retry. Keywords: imagepull, image pull backoff,
  ErrImagePull, registry, container image, pull failed.
metadata:
  domain: k8s
  category: remediation
  requires-approval: false
  confidence: 0.70
  mcp-servers:
    - kubernetes-mcp-server
---

# Handle ImagePullBackOff

## Preconditions

Before applying this skill, verify:

- Pod status is ImagePullBackOff or ErrImagePull
- Pod has been in this state for more than 2 minutes

## Actions

### 1. Get Pod Events

First, get pod events to understand the image pull failure.

```yaml
mcp_tool: kubernetes-mcp-server/events_list
params:
  namespace: $namespace
timeout: 30s
```

### 2. Delete Pod to Trigger Recreation

Delete the pod to trigger recreation and retry the image pull.

```yaml
mcp_tool: kubernetes-mcp-server/pods_delete
params:
  name: $pod_name
  namespace: $namespace
timeout: 30s
```

## Success Criteria

The skill succeeds when:

- [ ] New pod created and image pull succeeds
- [ ] Pod reaches Running state within 5 minutes

## Failure Handling

If image pull continues to fail:

1. Verify image name and tag are correct
2. Check image registry connectivity
3. Verify image pull secrets are configured
4. Escalate to human with registry details

## Examples

**Input Context:**
```json
{
  "pod_name": "myapp-deployment-xyz789",
  "namespace": "production",
  "status": "ImagePullBackOff",
  "image": "registry.example.com/myapp:v1.2.3"
}
```

**Expected Outcome:**
Pod deleted, new pod successfully pulls image and reaches Running state.
