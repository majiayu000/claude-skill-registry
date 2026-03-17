---
name: check-flux-status
version: "1.0.0"
description: >
  Check Flux CD GitOps sync status. Verifies Kustomizations, HelmReleases,
  and GitRepositories are synced and healthy. Use for deployment verification
  and troubleshooting. Keywords: flux, gitops, sync, kustomization, helm,
  reconciliation, status.
metadata:
  domain: general
  category: gitops
  requires-approval: false
  confidence: 0.90
  mcp-servers:
    - kubernetes-mcp-server
---

# Check Flux Status

## Preconditions

Before applying this skill, verify:

- Flux CD installed in cluster
- Access to flux-system namespace
- Kubernetes API access available

## Actions

### 1. Check Kustomizations

List and verify all Kustomizations:
```yaml
command: kubectl get kustomizations -A -o wide
resources:
  - apiVersion: kustomize.toolkit.fluxcd.io/v1
    kind: Kustomization
expected_conditions:
  - type: Ready
    status: "True"
  - type: Healthy (optional)
    status: "True"
```

### 2. Check HelmReleases

Verify all Helm releases are synced:
```yaml
command: kubectl get helmreleases -A -o wide
resources:
  - apiVersion: helm.toolkit.fluxcd.io/v2
    kind: HelmRelease
expected_conditions:
  - type: Ready
    status: "True"
  - type: Released
    status: "True"
```

### 3. Check GitRepositories

Verify source repositories are fetched:
```yaml
command: kubectl get gitrepositories -A -o wide
resources:
  - apiVersion: source.toolkit.fluxcd.io/v1
    kind: GitRepository
expected_conditions:
  - type: Ready
    status: "True"
check_fields:
  - lastAppliedRevision
  - lastAttemptedRevision
```

### 4. Check HelmRepositories

Verify Helm chart sources:
```yaml
command: kubectl get helmrepositories -A -o wide
resources:
  - apiVersion: source.toolkit.fluxcd.io/v1beta2
    kind: HelmRepository
expected_conditions:
  - type: Ready
    status: "True"
```

### 5. Identify Issues

Collect resources that are not ready:
```python
issues = []
for resource in all_flux_resources:
    ready_condition = get_condition(resource, "Ready")
    if ready_condition.status != "True":
        issues.append({
            "resource": f"{resource.kind}/{resource.name}",
            "namespace": resource.namespace,
            "status": ready_condition.status,
            "message": ready_condition.message,
            "reason": ready_condition.reason
        })
```

### 6. Generate Status Summary

Create summary report:
```yaml
status:
  overall: healthy|degraded|unhealthy
  components:
    kustomizations:
      total: N
      ready: N
      not_ready: N
    helm_releases:
      total: N
      ready: N
      not_ready: N
    git_repositories:
      total: N
      ready: N
      not_ready: N
  issues: [...]
  last_sync: timestamp
```

## Success Criteria

The skill succeeds when:

- [ ] All Flux resource types checked
- [ ] Ready conditions evaluated
- [ ] Issues identified and reported
- [ ] Overall status determined

## Failure Handling

If check fails:

1. Flux not installed: Return "flux_not_found" status
2. API access error: Return partial results with error
3. Timeout: Return timeout status with last known state

## Examples

**Input Context:**
```json
{
  "namespace": "flux-system",
  "include_all_namespaces": true
}
```

**Expected Output (Healthy):**
```json
{
  "status": "healthy",
  "components": {
    "kustomizations": {"total": 5, "ready": 5, "not_ready": 0},
    "helm_releases": {"total": 3, "ready": 3, "not_ready": 0},
    "git_repositories": {"total": 2, "ready": 2, "not_ready": 0}
  },
  "issues": [],
  "last_sync": "2024-01-15T10:30:00Z",
  "revision": "main@sha1:abc123"
}
```

**Expected Output (Degraded):**
```json
{
  "status": "degraded",
  "components": {
    "kustomizations": {"total": 5, "ready": 4, "not_ready": 1},
    "helm_releases": {"total": 3, "ready": 3, "not_ready": 0}
  },
  "issues": [
    {
      "resource": "Kustomization/apps",
      "namespace": "flux-system",
      "status": "False",
      "message": "kustomize build failed: ...",
      "reason": "BuildFailed"
    }
  ]
}
```
