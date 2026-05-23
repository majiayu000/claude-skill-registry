<!-- Copyright (c) 2026 defconxt. All rights reserved. -->
<!-- Licensed under AGPL-3.0 — see LICENSE file for details. -->
---
name: auditing-kubernetes-rbac
description: >-
  Audit Kubernetes RBAC configurations to detect overly permissive roles, dangerous
  ClusterRoleBindings, and privilege escalation paths in managed and self-hosted clusters.
domain: cybersecurity
subdomain: cloud-security
tags:
  - kubernetes
  - rbac
  - eks
  - aks
  - gke
  - cluster-security
  - pod-security
  - least-privilege
version: "1.0"
author: defconxt
license: AGPL-3.0
metadata:
  mitre-attack: ["T1613"]
---

# Auditing Kubernetes RBAC

## Overview

Kubernetes RBAC misconfigurations are a leading cause of container cluster compromise.
This skill systematically audits Role/ClusterRole definitions, RoleBinding/ClusterRoleBinding
assignments, and service account permissions to identify overly permissive access,
privilege escalation vectors, and violations of least-privilege principles across
EKS, AKS, and GKE clusters.

Mode: `[MODE: BLUE]` — Defensive posture assessment.

## Prerequisites

- `kubectl` configured with cluster access
- RBAC permissions: ability to list Roles, ClusterRoles, RoleBindings, ClusterRoleBindings,
  ServiceAccounts
- Python 3.10+ with `kubernetes` client library
- Optional: `kubeaudit`, `kube-bench`, or `rbac-police` for automated scanning

## Key Concepts

### Dangerous RBAC Permissions

Permissions that grant cluster-admin equivalent access or enable privilege escalation:

| Permission | Risk | ATT&CK |
|-----------|------|--------|
| `*` on `*` resources | Full cluster admin | T1078 |
| `create` on `pods` | Can run arbitrary containers | T1610 |
| `create` on `pods/exec` | Remote code execution in pods | T1609 |
| `get` on `secrets` | Access all cluster secrets | T1552.007 |
| `bind`/`escalate` on `roles` | Self-escalate permissions | T1078 |
| `create` on `serviceaccounts/token` | Mint service account tokens | T1550 |
| `impersonate` on `users/groups` | Impersonate cluster admin | T1550 |

### RBAC Enumeration

```bash
# List all ClusterRoles
kubectl get clusterroles -o json | jq '.items[] |
  select(.rules[]?.resources[]? == "*" and .rules[]?.verbs[]? == "*") |
  .metadata.name'

# List all ClusterRoleBindings
kubectl get clusterrolebindings -o json | jq '.items[] |
  {name: .metadata.name, role: .roleRef.name,
   subjects: [.subjects[]? | {kind, name, namespace}]}'

# Find service accounts with cluster-admin
kubectl get clusterrolebindings -o json | jq '.items[] |
  select(.roleRef.name == "cluster-admin") |
  {binding: .metadata.name, subjects: .subjects}'

# List all service accounts
kubectl get serviceaccounts --all-namespaces -o json | jq '.items[] |
  {namespace: .metadata.namespace, name: .metadata.name,
   automount: .automountServiceAccountToken}'
```

### Pod Security Standards

```bash
# Check pod security admission labels
kubectl get namespaces -o json | jq '.items[] | {
  name: .metadata.name,
  enforce: .metadata.labels["pod-security.kubernetes.io/enforce"] // "none",
  audit: .metadata.labels["pod-security.kubernetes.io/audit"] // "none",
  warn: .metadata.labels["pod-security.kubernetes.io/warn"] // "none"
}'

# Find privileged pods
kubectl get pods --all-namespaces -o json | jq '.items[] |
  select(.spec.containers[]?.securityContext?.privileged == true) |
  {namespace: .metadata.namespace, pod: .metadata.name}'

# Find pods with hostPath mounts
kubectl get pods --all-namespaces -o json | jq '.items[] |
  select(.spec.volumes[]?.hostPath != null) |
  {namespace: .metadata.namespace, pod: .metadata.name,
   paths: [.spec.volumes[] | select(.hostPath) | .hostPath.path]}'
```

### Managed Cluster Specifics

```bash
# EKS — Check aws-auth ConfigMap
kubectl get configmap aws-auth -n kube-system -o yaml

# AKS — Check Azure AD integration
az aks show --resource-group RG --name CLUSTER --query aadProfile

# GKE — Check workload identity
gcloud container clusters describe CLUSTER --zone ZONE --format='get(workloadIdentityConfig)'
```

## Workflow

### Step 1: Enumerate RBAC

```bash
kubectl get clusterroles,clusterrolebindings,roles,rolebindings --all-namespaces -o json > /tmp/rbac_dump.json
```

### Step 2: Run RBAC Audit

```bash
node scripts/agent.js --input /tmp/rbac_dump.json --output /tmp/rbac_findings.json
```

### Step 3: Review Findings

```bash
cat /tmp/rbac_findings.json | jq '.findings[] | select(.severity == "critical")'
```

## Detection

```yaml
title: Auditing Kubernetes Rbac Detection
id: 114e7504-81d9-4c4d-bc5e-c86f55fdc09d
status: experimental
description: Detects suspicious activity related to auditing kubernetes rbac techniques in cloud security context
logsource:
  product: aws
  service: cloudtrail
detection:
  selection:
    eventName: "*Unauthorized*"
  condition: selection
level: medium
tags:
  - attack.t1613
  - attack.credential_access
falsepositives:
  - Automated cloud infrastructure provisioning by approved CI/CD pipelines
```

## Verification

- [ ] No non-system ClusterRoleBindings to `cluster-admin`
- [ ] No wildcard (`*`) verbs on wildcard resources in custom roles
- [ ] Service accounts cannot read all secrets
- [ ] `automountServiceAccountToken: false` on unused service accounts
- [ ] Pod Security Admission enforced at `restricted` or `baseline`
- [ ] No pods running as privileged
- [ ] No pods mounting hostPath `/` or `/etc`

## References

- [Kubernetes RBAC Documentation](https://kubernetes.io/docs/reference/access-authn-authz/rbac/)
- [MITRE ATT&CK — Kubernetes Matrix](https://attack.mitre.org/matrices/enterprise/containers/)
- [CIS Kubernetes Benchmark](https://www.cisecurity.org/benchmark/kubernetes)
- [NSA/CISA Kubernetes Hardening Guide](https://media.defense.gov/2022/Aug/29/2003066362/-1/-1/0/CTR_KUBERNETES_HARDENING_GUIDANCE_1.2_20220829.PDF)
