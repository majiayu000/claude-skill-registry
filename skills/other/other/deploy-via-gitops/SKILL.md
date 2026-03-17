---
name: deploy-via-gitops
version: "1.0.0"
description: >
  Deploy application changes via GitOps workflow. Updates manifests in Git,
  triggers Flux reconciliation, and verifies deployment. Use for safe,
  auditable deployments. Keywords: deploy, gitops, flux, reconcile, release,
  rollout, git, manifest.
metadata:
  domain: general
  category: gitops
  requires-approval: true
  confidence: 0.80
  mcp-servers:
    - kubernetes-mcp-server
---

# Deploy via GitOps

## Preconditions

Before applying this skill, verify:

- GitOps repository access configured
- Flux CD watching the repository
- Target namespace exists
- Image exists in registry

## Actions

### 1. Prepare Manifest Changes

Identify files to update:
```yaml
manifest_paths:
  - gitops/apps/{app-name}/deployment.yaml
  - gitops/apps/{app-name}/kustomization.yaml
changes:
  - type: image_tag
    field: spec.template.spec.containers[*].image
    new_value: "{registry}/{image}:{tag}"
  - type: replicas
    field: spec.replicas
    new_value: N
```

### 2. Update Git Repository

Commit changes to GitOps repo:
```python
# Clone or update repository
repo = git.Repo(gitops_path)
repo.remotes.origin.pull()

# Make changes
update_deployment_image(deployment_path, new_image)

# Commit and push
repo.index.add([deployment_path])
repo.index.commit(f"chore(gitops): Update {app_name} to {tag}")
repo.remotes.origin.push()
```

### 3. Trigger Flux Reconciliation

Force immediate sync:
```yaml
command: flux reconcile kustomization {kustomization-name} --with-source
options:
  - --namespace=flux-system
  - --timeout=5m
wait_for:
  - type: Ready
    status: "True"
```

### 4. Monitor Rollout

Watch deployment progress:
```python
# Wait for rollout
while not deployment_ready:
    status = get_deployment_status(app_name, namespace)
    if status.ready_replicas == status.replicas:
        deployment_ready = True
    elif status.conditions.has_failure:
        raise DeploymentFailed(status.conditions.message)
    await asyncio.sleep(5)
```

### 5. Verify Deployment

Confirm successful deployment:
```yaml
verifications:
  - check: deployment_ready
    resource: deployment/{app-name}
    condition: availableReplicas >= desiredReplicas
  - check: pods_healthy
    selector: app={app-name}
    condition: all pods Running/Ready
  - check: endpoint_responding
    url: http://{service-name}/health
    expected_status: 200
```

### 6. Record Deployment Result

Log deployment outcome:
```yaml
deployment_record:
  app: string
  version: string
  previous_version: string
  status: success|failed|rolled_back
  timestamp: datetime
  duration_seconds: number
  commit_sha: string
  deployed_by: agent|user
```

## Success Criteria

The skill succeeds when:

- [ ] Manifest changes committed to Git
- [ ] Flux reconciliation completed
- [ ] Deployment rollout successful
- [ ] Verification checks passed

## Failure Handling

If deployment fails:

1. Git push failed: Retry with backoff, report auth error
2. Reconciliation failed: Check Flux logs, report Kustomize errors
3. Rollout failed: Auto-rollback if configured, notify
4. Verification failed: Consider rollback, alert operators

## Rollback Procedure

If rollback needed:
```yaml
rollback_steps:
  1. git_revert:
     command: git revert HEAD
     push: true
  2. force_reconcile:
     command: flux reconcile kustomization {name} --with-source
  3. verify_rollback:
     check: previous version running
  4. notify:
     channel: discord
     message: "Rolled back {app} due to: {reason}"
```

## Examples

**Input Context:**
```json
{
  "app_name": "k8s-monitor",
  "namespace": "ai-agents",
  "new_image": "registry.almckay.io/k8s-monitor:0.2.0-abc1234",
  "gitops_path": "gitops/apps/ai-agents/k8s-monitor"
}
```

**Expected Output:**
```json
{
  "success": true,
  "deployment": {
    "app": "k8s-monitor",
    "version": "0.2.0-abc1234",
    "previous_version": "0.1.9-def5678",
    "namespace": "ai-agents"
  },
  "git": {
    "commit_sha": "abc123def456",  # pragma: allowlist secret
    "branch": "main",
    "message": "chore(gitops): Update k8s-monitor to 0.2.0-abc1234"
  },
  "flux": {
    "reconciled": true,
    "kustomization": "apps",
    "duration_seconds": 45
  },
  "verification": {
    "deployment_ready": true,
    "pods_healthy": true,
    "ready_replicas": 1
  }
}
```
