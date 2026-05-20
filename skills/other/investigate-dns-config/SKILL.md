---
name: investigate-dns-config
version: "1.0.0"
description: >
  Investigate DNSConfigForming warnings on pods. Analyzes DNS policy configuration,
  host network settings, and nameserver limits. Use when pods show DNSConfigForming
  events or DNS-related warnings. Keywords: DNS, DNSConfigForming, nameserver limit,
  resolv.conf, dnsPolicy, hostNetwork.
metadata:
  domain: k8s
  category: diagnostic
  requires-approval: false
  confidence: 0.85
  mcp-servers:
    - kubernetes-mcp-server
---

# Investigate DNS Configuration Issues

## Preconditions

Before applying this skill, verify:

- Event shows DNSConfigForming reason
- Pod name and namespace are known from event
- Pod may have been recreated (check for similar pods)

## Actions

### 1. Get Related Events

Gather all DNS-related events in the namespace for context.

```yaml
mcp_tool: kubernetes-mcp-server/events_list
params:
  namespace: $namespace
timeout: 30s
```

**Analysis**: Look for DNSConfigForming events, note affected pods and messages.

### 2. List Affected Pods

Find pods managed by the same controller (may have been recreated).

```yaml
mcp_tool: kubernetes-mcp-server/pods_list_in_namespace
params:
  namespace: $namespace
  labelSelector: $label_selector
timeout: 30s
```

**Analysis**: Identify running pods that may be affected.

### 3. Get Controller Configuration

Get the DaemonSet/Deployment/StatefulSet that manages the pod.

```yaml
mcp_tool: kubernetes-mcp-server/resources_get
params:
  apiVersion: apps/v1
  kind: $controller_kind
  name: $controller_name
  namespace: $namespace
timeout: 30s
```

**Analysis**: Check for:
- `hostNetwork: true` - Pod uses host networking
- `dnsPolicy` - Current DNS policy setting

### 4. Determine Root Cause

Based on findings, identify the root cause:

| Condition | Root Cause | Recommendation |
|-----------|-----------|----------------|
| `hostNetwork: true` + `dnsPolicy: ClusterFirst` | Nameserver limit exceeded when combining cluster DNS with host DNS | Change to `dnsPolicy: ClusterFirstWithHostNet` |
| `hostNetwork: true` + no explicit dnsPolicy | Same as above (ClusterFirst is default) | Set `dnsPolicy: ClusterFirstWithHostNet` |
| `hostNetwork: false` + DNSConfigForming | Node has >3 nameservers | Usually benign, first 3 nameservers are used |

## Success Criteria

The skill succeeds when:

- [ ] Root cause of DNSConfigForming identified
- [ ] Controller configuration analyzed
- [ ] Remediation recommendation provided

## Failure Handling

If investigation is inconclusive:

1. Check node's /etc/resolv.conf via node logs
2. Verify CoreDNS is running correctly
3. Escalate with gathered diagnostic info

## Examples

**Input Context:**
```json
{
  "namespace": "monitoring",
  "pod_name": "prometheus-node-exporter-abc123",
  "event_reason": "DNSConfigForming",
  "event_message": "Nameserver limits were exceeded, some nameservers have been omitted"
}
```

**Investigation Output:**
```json
{
  "affected_pods": ["prometheus-node-exporter-abc123", "prometheus-node-exporter-def456"],
  "controller": {
    "kind": "DaemonSet",
    "name": "prometheus-prometheus-node-exporter",
    "hostNetwork": true,
    "dnsPolicy": "ClusterFirst"
  },
  "root_cause": "DaemonSet uses hostNetwork: true with default dnsPolicy: ClusterFirst, causing nameserver limit conflicts",
  "recommendation": {
    "action": "Update Helm values to set dnsPolicy: ClusterFirstWithHostNet",
    "requires_approval": false,
    "gitops_path": "gitops/apps/monitoring/prometheus-helmrelease.yaml"
  }
}
```

## Remediation Notes

For Helm-managed resources:
1. Identify the HelmRelease in GitOps
2. Add `dnsPolicy: ClusterFirstWithHostNet` to the subchart values
3. Commit and let Flux CD apply the change

For direct Kubernetes resources:
1. Patch the controller with updated dnsPolicy
2. Pods will be recreated with correct DNS configuration
