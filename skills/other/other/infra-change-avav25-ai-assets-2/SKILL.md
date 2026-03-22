---
name: infra-change
description: Infrastructure change workflow — Terraform plan/apply, Helm diff/upgrade, Kubernetes manifest changes with mandatory approval gates. Applies DevOps role. Safe-by-default with plan review before any mutation.
disable-model-invocation: true
argument-hint: [description of infrastructure change]
---

# Infrastructure Change

Safe infrastructure change workflow for Terraform, Helm, and Kubernetes. Every mutation requires explicit user approval after reviewing the plan/diff. Applies `Agent(devops-engineer)` for all steps.

**⚠️ SAFETY: No `apply`, `upgrade`, `delete`, or `scale` command runs without explicit user APPROVE.**

## 1. Define the Change

Ask the user (or extract from parent workflow context):

- **What needs to change?** (resource scaling, new service, config update, network change, secret rotation)
- **Which tool?** Terraform, Helm, kubectl, or combination
- **Environment**: dev / staging / production
- **Risk level**: Low (config), Medium (scaling, new resource), High (destroy, DB, auth, prod)

If Risk = HIGH or Environment = production:
```
⚠️ HIGH-RISK INFRASTRUCTURE CHANGE
Destructive actions require explicit "APPROVE" before execution.
Affected: [list resources/services]
```

## 2. Apply Roles

Apply `Agent(devops-engineer)`. For production changes, also apply `Agent(sre-engineer)` for SLO impact assessment. For cloud infrastructure design (landing zones, networking topology, IAM), consult `Agent(cloud-architect)`. For CI/CD pipeline architecture changes, consult `Agent(devops-architect)`.

## 3. Review Current State

Before making changes, capture the current state:

### 3a. Terraform State (if applicable)

```
// turbo
terraform validate
terraform fmt -check -recursive
```

Review relevant `.tf` files and current state:
```
// turbo
terraform plan -out=tfplan
```

### 3b. Helm State (if applicable)

```
// turbo
helm list -n <namespace>
helm get values <release-name> -n <namespace>
```

### 3c. Kubernetes State (if applicable)

```
// turbo
kubectl get deployments,services,ingress -n <namespace>
kubectl get pods -n <namespace> -o wide
```

**Record**: Current resource counts, versions, replicas, config values as baseline.

## 4. Implement Changes

Make the infrastructure code changes following `Agent(devops-engineer)` standards:

**For Terraform:**
- Modify `.tf` files as needed
- Run format and validate:
```
// turbo
terraform fmt -recursive
terraform validate
```

**For Helm:**
- Modify `values.yaml` or chart templates
- Lint the chart:
```
// turbo
helm lint <chart-path>
```

**For raw Kubernetes manifests:**
- Modify YAML files
- Validate with dry-run:
```
kubectl apply --dry-run=client -f <manifest>
```

## 5. Plan Review — MANDATORY BEFORE APPLY

### 5a. Terraform Plan

```
terraform plan -out=tfplan
```

Present the plan summary:

```
## Terraform Plan Summary
| Action  | Count | Resources |
|---------|-------|-----------|
| Add     | X     | [list]    |
| Change  | X     | [list]    |
| Destroy | X     | [list]    |

⚠️ DESTROY/REPLACE resources:
- [resource] — [reason]

Data loss risk: [yes/no]
Estimated cost impact: [if applicable]
```

### 5b. Helm Diff

```
helm diff upgrade <release> <chart-path> -n <namespace> -f <values-file>
```

Present the diff summary:

```
## Helm Diff Summary
| Object | Action | Key Changes |
|--------|--------|-------------|
| Deployment/X | changed | replicas: 1→2, image: v1→v2 |
| Service/Y | added | port 8080 |
| Secret/Z | changed | keys modified |

⚠️ Critical changes:
- [deployment restart expected]
- [secret reference changed]

Downtime risk: [yes/no]
```

### 5c. Kubectl Dry-Run

```
kubectl diff -f <manifest>
```

**⚠️ STOP. Present plan/diff summary and request APPROVE before proceeding to Step 6.**

## 6. Apply — REQUIRES EXPLICIT APPROVE

Only after the user explicitly approves:

**Terraform:**
```
terraform apply tfplan
```

**Helm:**
```
helm upgrade <release> <chart-path> -n <namespace> -f <values-file>
```

**Kubectl:**
```
kubectl apply -f <manifest>
```

**Rules:**
- Never auto-run apply/upgrade commands
- User must explicitly type "APPROVE" or equivalent
- If the plan changed since review — re-run Step 5

## 7. Verify

After applying, verify the changes took effect:

```
// turbo
kubectl get pods -n <namespace> -o wide
kubectl get events -n <namespace> --sort-by='.lastTimestamp' --field-selector type!=Normal
```

**Check:**
- [ ] All pods healthy (Running, no CrashLoopBackOff)
- [ ] Expected replica counts match
- [ ] No warning/error events
- [ ] Services responding (health check endpoints)
- [ ] Logs clean (no new errors)

If production — monitor SLIs for 5–10 minutes after apply.

## 8. Rollback Plan

Document the rollback before considering the change complete:

**Terraform:**
```
# Revert the .tf file changes and re-apply
terraform plan -out=tfplan-rollback
terraform apply tfplan-rollback
```

**Helm:**
```
helm rollback <release> <previous-revision> -n <namespace>
```

**Kubectl:**
```
kubectl rollout undo deployment/<name> -n <namespace>
```

## 9. Summary

```
## Infrastructure Change Summary
- **Change**: [what was changed]
- **Tool**: [Terraform / Helm / kubectl]
- **Environment**: [dev / staging / production]
- **Risk**: [low / medium / high]
- **Plan reviewed**: [yes — summary of add/change/destroy]
- **Applied**: [yes/no — with APPROVE]
- **Verification**: [pass/fail]
- **Rollback plan**: [documented above]
- **Next steps**: [monitoring, follow-up changes]
```

## Integration

- **Roles**: `Agent(devops-engineer)` (primary), `Agent(sre-engineer)` (review), `Agent(cloud-architect)` (cloud design review), `Agent(devops-architect)` (CI/CD pipeline architecture)
- **Preceded by**: `/feature-plan` (infra work stream), `/architecture` (cloud architecture design)
- **Followed by**: `/deploy-staging`, `/deploy-production`
