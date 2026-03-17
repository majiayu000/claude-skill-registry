---
name: check-pod-resources
version: "1.0.0"
description: >
  Check resource usage (CPU, memory) for pods. Used to identify pods
  consuming excessive resources. Keywords: pod resources, cpu, memory,
  consumption, metrics, resource usage, top pods.
metadata:
  domain: k8s
  category: diagnostic
  requires-approval: false
  confidence: 0.95
  mcp-servers:
    - kubernetes-mcp-server
---

# Check Pod Resource Usage

## Preconditions

Before applying this skill, verify:

- Metrics server is available
- Need to understand pod resource consumption

## Actions

### 1. Get Resource Usage for Pods

Retrieve CPU and memory usage metrics for pods in the namespace.

```yaml
mcp_tool: kubernetes-mcp-server/pods_top
params:
  namespace: $namespace
timeout: 30s
```

## Success Criteria

The skill succeeds when:

- [ ] Pod resource metrics retrieved successfully
- [ ] High resource consumers identified if present

## Failure Handling

If metrics unavailable:

1. Check if metrics-server is deployed
2. Fall back to resource requests/limits from pod spec

## Examples

**Input Context:**
```json
{
  "namespace": "production",
  "reason": "investigating high memory usage"
}
```

**Expected Outcome:**
Pod metrics retrieved showing CPU and memory usage for each pod,
with any pods consuming excessive resources clearly identified.
