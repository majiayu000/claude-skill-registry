---
name: openshift
description: OpenShift-specific operations including routes, operators, and platform features
---

# OpenShift Skills

OpenShift-specific operations that extend Kubernetes capabilities.

## Sub-Skills

| Skill | Description |
|-------|-------------|
| `openshift:debug` | Debug OpenShift-specific resources and operators |
| `openshift:routes` | Manage OpenShift routes and ingress |
| `openshift:trusted-ca-bundle` | Use OpenShift's trusted CA bundle for TLS |

## When to Use

- Working with OpenShift clusters (RHOCP, OKD)
- Managing OpenShift-specific resources (Routes, DeploymentConfigs, etc.)
- Debugging OpenShift operators
- Working with OpenShift console and authentication

## Quick Commands

```bash
# Check cluster info
oc whoami
oc project
oc cluster-info

# Get OpenShift-specific resources
oc get routes -A
oc get clusteroperators
oc get clusterversion

# Check operator status
oc get csv -A
oc get installplans -A
```

## Difference from k8s/ Skills

| Skill | Use For |
|-------|---------|
| `k8s/*` | Standard Kubernetes resources (pods, deployments, services) |
| `openshift:*` | OpenShift-specific resources (routes, operators, builds) |

Both work on OpenShift clusters, but `openshift:*` skills use `oc` commands and understand OpenShift-specific concepts.
