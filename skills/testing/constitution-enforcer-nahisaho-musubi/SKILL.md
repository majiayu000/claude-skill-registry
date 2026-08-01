---
name: constitution-enforcer
description: 'Validates compliance with 9 Constitutional Articles and Phase -1 Gates
  before implementation.Trigger terms: constitution, governance, compliance, validation,
  constitutional compliance,Phase -1 Gates,'
---

---
name: Constitution Enforcer
description: Validate Kubernetes manifests, Helm charts, and Dapr configs against security and governance rules. Use when: (1) Generating K8s manifests, (2) Creating Helm charts, (3) Building Docker configurations, (4) Reviewing Dapr components, (5) After any infrastructure code generation, (6) Before deployment reviews. Validates container security, RBAC policies, resource limits, Dapr standards, and network policies.
---

## Overview

This skill enforces cloud-native governance rules for Kubernetes deployments. Invoke it before and after generating infrastructure code to ensure compliance with security policies.

## Validation Scripts

Use the provided validation scripts for automated checking:

```bash
# Validate Kubernetes manifests
python scripts/validate_k8s.py <manifest-file>

# Validate Helm charts
python scripts/validate_helm.py <chart-directory>

# Validate Dapr components
python scripts/validate_dapr.py <component-file>

# Run all validations
bash scripts/validate_all.sh <directory>
```

## Rule Codes

| Code | Category | Description |
|------|----------|-------------|
| SEC-001 | Security | Missing securityContext |
| SEC-002 | Security | Running as root (UID 0) |
| SEC-003 | Security | Privilege escalation enabled |
| SEC-004 | Security | Writable root filesystem |
| SEC-005 | Security | Capabilities not dropped |
| IMG-001 | Image | Using 'latest' tag |
| IMG-002 | Image | Missing image pull policy |
| NET-001 | Network | Host network enabled |
| NET-002 | Network | Host PID enabled |
| NET-003 | Network | Missing NetworkPolicy |
| RBAC-001 | RBAC | Using default ServiceAccount |
| RBAC-002 | RBAC | ClusterRole for app workload |
| RBAC-003 | RBAC | Wildcard permissions (*) |
| RBAC-004 | RBAC | Forbidden verbs (bind/escalate/impersonate) |
| RBAC-005 | RBAC | cluster-admin binding |
| RES-001 | Resources | Missing CPU request |
| RES-002 | Resources | Missing CPU limit |
| RES-003 | Resources | Missing memory request |
| RES-004 | Resources | Missing memory limit |
| DAPR-001 | Dapr | Missing namespace |
| DAPR-002 | Dapr | Using 'default' namespace |
| DAPR-003 | Dapr | Inline credentials |
| DAPR-004 | Dapr | Missing scopes |
| DAPR-005 | Dapr | mTLS not enabled |
| KAFKA-001 | Kafka | Invalid topic naming |
| KAFKA-002 | Kafka | Missing auth in production |
| KAFKA-003 | Kafka | Low replication factor |
| DB-001 | Database | SSL not enabled |
| DB-002 | Database | Hardcoded credentials |
| DB-003 | Database | Credentials not in Secret |

## Container Security Rules

Every container MUST have these security settings:

```yaml
securityContext:
  runAsNonRoot: true
  runAsUser: 1000
  runAsGroup: 1000
  allowPrivilegeEscalation: false
  readOnlyRootFilesystem: true
  capabilities:
    drop:
      - ALL
```

**Violations that BLOCK deployment:**
- Running as root (UID 0)
- Privilege escalation enabled
- Using `latest` image tag
- Host network or host PID enabled
- Missing security context

## RBAC Policies

| Rule | Requirement |
|------|-------------|
| Dedicated ServiceAccount | Each app has its own SA |
| No default SA | Never use `default` service account |
| Namespace-scoped | Use Role, not ClusterRole |
| Least privilege | Only permissions actually needed |
| No cluster-admin | Never bind cluster-admin to apps |

**Forbidden:**
- Wildcard permissions (`*`)
- ClusterRoleBinding to applications
- `bind`, `escalate`, `impersonate` verbs

## Resource Limits

Every container MUST specify:

```yaml
resources:
  requests:
    cpu: "<value>"
    memory: "<value>"
  limits:
    cpu: "<value>"
    memory: "<value>"
```

**Defaults by component:**

| Component | CPU Req | CPU Limit | Mem Req | Mem Limit |
|-----------|---------|-----------|---------|-----------|
| Frontend | 100m | 500m | 128Mi | 256Mi |
| Backend | 200m | 1000m | 256Mi | 512Mi |
| MCP Server | 100m | 500m | 128Mi | 256Mi |
| Dapr Sidecar | 100m | 300m | 128Mi | 256Mi |

## Dapr Configuration Standards

Every Dapr component MUST have:
- Explicit namespace (never "default")
- Credentials via `secretKeyRef` (never inline)
- Scopes defined (never empty)
- mTLS enabled in Configuration resource

## Kafka Event Governance

- Topic naming: `<domain>.<entity>.<event>` (e.g., `todo.task.created`)
- Auth required in production
- Replication factor 2+ in production

## Database Connection Security

- SSL required: `sslmode=require`
- Credentials in Kubernetes Secret only
- No hardcoded credentials anywhere

## Network Policies

- Default deny all ingress/egress
- Explicit allow rules only for required traffic

## Validation Output Format

When violations found, output:

```
## Constitution Violation Report

### CRITICAL (Must Fix)
1. [RULE-CODE] Description
   - Location: file:line
   - Fix: How to fix

### WARNING (Should Fix)
1. [RULE-CODE] Description

### Status: PASSED / BLOCKED
```

## Compliance Checklist

```
Container Security:
[ ] runAsNonRoot: true
[ ] allowPrivilegeEscalation: false
[ ] No latest tags

RBAC:
[ ] Dedicated ServiceAccount
[ ] Namespace-scoped Role

Resources:
[ ] CPU/Memory limits set

Dapr:
[ ] mTLS enabled
[ ] Scopes defined
[ ] secretKeyRef used

Database:
[ ] SSL enabled
[ ] Credentials in Secret
```
