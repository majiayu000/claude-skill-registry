---
name: diagnose-network-issue
version: "1.0.0"
description: >
  Diagnose network connectivity issues for pods. Checks DNS resolution, service
  connectivity, and network policies. Use when pods cannot communicate with
  other services. Keywords: network issue, DNS, connectivity, service unreachable,
  network policy, CNI.
metadata:
  domain: k8s
  category: diagnostic
  requires-approval: false
  confidence: 0.75
  mcp-servers:
    - kubernetes-mcp-server
---

# Diagnose Network Issue

## Preconditions

Before applying this skill, verify:

- Pod name and namespace are known
- Pod is in Running state
- Network issue symptoms are observed

## Actions

### 1. Get Pod Details

Check pod networking configuration.

```yaml
mcp_tool: kubernetes-mcp-server/pods_get
params:
  name: $pod_name
  namespace: $namespace
timeout: 30s
```

### 2. Check DNS Resolution

Execute DNS lookup inside the pod.

```yaml
mcp_tool: kubernetes-mcp-server/pods_exec
params:
  name: $pod_name
  namespace: $namespace
  command: ["nslookup", "kubernetes.default"]
timeout: 30s
```

### 3. Check Service Connectivity

Test connection to target service.

```yaml
mcp_tool: kubernetes-mcp-server/pods_exec
params:
  name: $pod_name
  namespace: $namespace
  command: ["wget", "-O-", "-T5", "$target_service"]
timeout: 30s
```

### 4. Get Network Policies

Check if network policies affect the pod.

```yaml
mcp_tool: kubernetes-mcp-server/resources_list
params:
  apiVersion: networking.k8s.io/v1
  kind: NetworkPolicy
  namespace: $namespace
timeout: 30s
```

### 5. Check Pod Events

Look for network-related events.

```yaml
mcp_tool: kubernetes-mcp-server/events_list
params:
  namespace: $namespace
timeout: 30s
```

## Success Criteria

The skill succeeds when:

- [ ] DNS resolution works (kubernetes.default resolves)
- [ ] No blocking network policies found
- [ ] Root cause identified

## Failure Handling

If diagnosis is inconclusive:

1. Check CNI plugin logs on the node
2. Verify kube-proxy is running
3. Escalate with gathered diagnostic info

## Examples

**Input Context:**
```json
{
  "pod_name": "web-app-abc123",
  "namespace": "default",
  "target_service": "http://api-service:8080"
}
```

**Output:**
```json
{
  "dns_working": true,
  "service_reachable": false,
  "network_policies": ["deny-external"],
  "diagnosis": "NetworkPolicy 'deny-external' blocking egress traffic",
  "recommendation": "Add egress rule to allow traffic to api-service"
}
```
