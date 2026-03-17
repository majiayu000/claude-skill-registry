---
name: promotion-pipeline
description: |
  OCI artifact promotion pipeline from PR merge through integration validation to live deployment.

  Use when: (1) Tracing why a change has not reached a cluster, (2) Debugging artifacts stuck in integration,
  (3) Understanding the build/validate/promote lifecycle, (4) Performing manual promotion or rollback,
  (5) Investigating GitHub Actions workflow failures, (6) Checking OCI artifact tags in GHCR.

  Triggers: "promotion", "pipeline", "artifact", "oci", "integration deploy", "live deploy",
  "stuck in integration", "not deploying", "ghcr", "build artifact", "tag validated",
  "repository_dispatch", "canary-checker", "rollback", "semver", "image policy",
  "promotion pipeline", "why isn't live updating"
user-invocable: false
---

# Promotion Pipeline

The homelab uses an OCI artifact promotion pipeline for immutable, auditable deployments. Changes flow through three stages: build, validate in integration, promote to live. This skill covers end-to-end tracing and debugging.

## Pipeline Overview

```
PR merged to main (kubernetes/ changed)
       |
       v
build-platform-artifact.yaml (GHA)
  - Discovers latest stable tag in GHCR, bumps patch
  - Pushes OCI artifact with tag X.Y.Z-rc.N
  - Adds tags: sha-<short>, integration-<short>
       |
       v
Integration Cluster
  - OCIRepository polls GHCR with semver ">= 0.0.0-0" (includes RCs)
  - Detects new X.Y.Z-rc.N (higher than previous stable)
  - Flux reconciles platform Kustomization
       |
       v
Flux Alert (validation-success)
  - Watches platform Kustomization for "Reconciliation finished"
  - Fires repository_dispatch to GitHub (event_type: Kustomization/platform.flux-system)
  - Idempotency guard: workflow skips if artifact already has validated-<sha> tag
       |
       v
tag-validated-artifact.yaml (GHA)
  - Finds integration-<sha> artifact, extracts RC tag
  - Strips RC suffix: X.Y.Z-rc.N --> X.Y.Z
  - Tags artifact: validated-<sha> + X.Y.Z (stable semver)
       |
       v
Live Cluster
  - OCIRepository polls GHCR with semver ">= 0.0.0" (stable only)
  - Detects new X.Y.Z stable tag
  - Flux reconciles platform (production deployment)
```

## Artifact Tagging Strategy

Each artifact accumulates tags as it progresses through the pipeline:

| Tag | Created By | Stage | Purpose |
|-----|-----------|-------|---------|
| `X.Y.Z-rc.N` | build workflow | Build | Pre-release semver for integration polling |
| `sha-<7char>` | build workflow | Build | Immutable commit reference |
| `integration-<7char>` | build workflow | Build | Marks artifact for integration consumption |
| `validated-<7char>` | tag workflow | Promotion | Traceability for validated artifacts |
| `X.Y.Z` | tag workflow | Promotion | Stable semver for live polling |

**Version numbering**: The build workflow queries GHCR for the highest stable `X.Y.Z` tag, bumps patch to `X.Y.(Z+1)`, then creates `X.Y.(Z+1)-rc.N`. When validated, the RC suffix is stripped to produce `X.Y.(Z+1)`.

## Source Types by Cluster

| Cluster | Source Type | Semver Constraint | What It Accepts |
|---------|------------|-------------------|-----------------|
| dev | GitRepository | N/A | Git main branch directly |
| integration | OCIRepository | `>= 0.0.0-0` | All versions including pre-releases (`-rc.N`) |
| live | OCIRepository | `>= 0.0.0` | Stable versions only (no `-rc` suffix) |

The semver constraint is set in the config module (`infrastructure/modules/config/main.tf`) and applied via flux-operator bootstrap. The `-0` suffix in `>= 0.0.0-0` is what allows pre-release versions per semver specification.

## Tracing a Change End-to-End

### Stage 1: GitHub Actions Build

```bash
# Check if build workflow triggered
gh run list --workflow=build-platform-artifact.yaml --limit=5

# View specific run details
gh run view <run-id>

# Check workflow logs
gh run view <run-id> --log
```

The build triggers on push to `main` when `kubernetes/**` files change. If no Kubernetes files changed, the workflow does not run.

### Stage 2: OCI Artifact in GHCR

```bash
# List recent artifacts and their tags
flux list artifact oci://ghcr.io/<owner>/homelab/platform --limit=10

# Find artifact for a specific commit
flux list artifact oci://ghcr.io/<owner>/homelab/platform | grep <short-sha>
```

### Stage 3: Integration Cluster Pickup

```bash
# Check OCIRepository status (is it seeing the new artifact?)
KUBECONFIG=~/.kube/integration.yaml kubectl get ocirepository -n flux-system -o wide

# Check what version is currently deployed
KUBECONFIG=~/.kube/integration.yaml kubectl get ocirepository flux-system -n flux-system -o jsonpath='{.status.artifact.revision}'

# Check platform Kustomization reconciliation
KUBECONFIG=~/.kube/integration.yaml kubectl get kustomization platform -n flux-system

# Force reconciliation if stuck
KUBECONFIG=~/.kube/integration.yaml flux reconcile source oci flux-system -n flux-system
```

### Stage 4: Validation Alert

```bash
# Check the validation-success Alert status
KUBECONFIG=~/.kube/integration.yaml kubectl describe alert validation-success -n flux-system

# Check the github-dispatch Provider
KUBECONFIG=~/.kube/integration.yaml kubectl get providers -n flux-system

# Check if Alert fired recently (events)
KUBECONFIG=~/.kube/integration.yaml kubectl get events -n flux-system --field-selector involvedObject.name=validation-success
```

### Stage 5: Tag Workflow

```bash
# Check if tag workflow triggered
gh run list --workflow=tag-validated-artifact.yaml --limit=5

# If using workflow_dispatch for manual promotion
gh workflow run tag-validated-artifact.yaml -f artifact_sha=<7char-sha>
```

### Stage 6: Live Cluster Pickup

```bash
# Check OCIRepository status
KUBECONFIG=~/.kube/live.yaml kubectl get ocirepository -n flux-system -o wide

# Check current deployed version
KUBECONFIG=~/.kube/live.yaml kubectl get ocirepository flux-system -n flux-system -o jsonpath='{.status.artifact.revision}'

# Check platform Kustomization
KUBECONFIG=~/.kube/live.yaml kubectl get kustomization platform -n flux-system
```

## Debugging: Artifact Stuck in Integration

```
Is the OCI artifact in GHCR?
|
+-- NO --> Check build-platform-artifact workflow
|          - Did the workflow trigger? (push to main with kubernetes/ changes)
|          - Check GHCR auth: GITHUB_TOKEN must have packages:write
|          - Check workflow logs for "flux push artifact" errors
|
+-- YES -> Is integration OCIRepository seeing it?
           |
           +-- NO --> Check semver constraint
           |          - Must be ">= 0.0.0-0" to accept RC versions
           |          - Run: kubectl get ocirepository -n flux-system -o yaml | grep semver
           |          - Check OCIRepository .status.conditions for errors
           |
           +-- YES -> Is platform Kustomization reconciling?
                      |
                      +-- NO --> Check Kustomization status
                      |          - kubectl describe kustomization platform -n flux-system
                      |          - Look for dependency failures, schema errors
                      |
                      +-- YES -> Is the Alert firing repository_dispatch?
                                 |
                                 +-- NO --> Check Alert and Provider
                                 |          - Alert "validation-success" must watch platform Kustomization
                                 |          - Provider "github-dispatch" needs flux-system secret with GitHub token
                                 |          - Token needs repo scope for repository_dispatch
                                 |
                                 +-- YES -> Check tag-validated-artifact workflow
                                            - Idempotency guard: already has validated-<sha> tag?
                                            - Check workflow logs for tag errors
```

## Debugging: Live Not Updating

```
Is the artifact tagged with stable semver (X.Y.Z)?
|
+-- NO --> Promotion did not complete
|          - Check tag-validated-artifact workflow ran successfully
|          - Verify it created both validated-<sha> and X.Y.Z tags
|
+-- YES -> Is live OCIRepository seeing the stable tag?
           |
           +-- NO --> Check semver constraint
           |          - Must be ">= 0.0.0" (excludes pre-releases)
           |          - Verify the stable tag is higher than current deployed version
           |          - Force poll: flux reconcile source oci flux-system -n flux-system
           |
           +-- YES -> Is Kustomization reconciling?
                      |
                      +-- NO --> Check Kustomization status and dependencies
                      +-- YES -> Deployment should be in progress
                                 - Check HelmRelease statuses: flux get helmreleases -A
                                 - Check for failing health checks blocking rollout
```

## Canary-Checker Validation

The `platform-validation` Canary in the monitoring namespace runs health checks every 60 seconds:

| Check | Type | What It Validates |
|-------|------|-------------------|
| `kubernetes-api` | HTTP | Kubernetes API responds (200 or 401) |
| `flux-pods-healthy` | Kubernetes | All Flux pods in Running state with Ready condition |

```bash
# Check canary status
KUBECONFIG=~/.kube/integration.yaml kubectl get canaries -n monitoring

# Check individual check results
KUBECONFIG=~/.kube/integration.yaml kubectl describe canary platform-validation -n monitoring

# Check canary-checker metrics in Prometheus
# canary_check{name="platform-validation"} == 0 means healthy
```

Alerts fire if canary checks fail:

| Alert | Condition | Severity |
|-------|-----------|----------|
| `CanaryCheckFailure` | `canary_check == 1` for 2m | critical |
| `CanaryCheckHighFailureRate` | >20% failure rate over 15m | warning |

## Manual Promotion (Emergency)

When automatic promotion fails, manually tag the artifact:

```bash
# Authenticate to GHCR
echo $GITHUB_TOKEN | docker login ghcr.io -u $GITHUB_USER --password-stdin

# Find the integration artifact
flux list artifact oci://ghcr.io/<owner>/homelab/platform | grep integration

# Tag manually (replace <sha> with 7-char commit SHA)
flux tag artifact \
  oci://ghcr.io/<owner>/homelab/platform:integration-<sha> \
  --tag validated-<sha>

flux tag artifact \
  oci://ghcr.io/<owner>/homelab/platform:integration-<sha> \
  --tag <X.Y.Z>  # The stable semver to assign
```

Alternatively, use `workflow_dispatch` to trigger the tag workflow manually:

```bash
gh workflow run tag-validated-artifact.yaml -f artifact_sha=<7char-sha>
```

## Rollback Procedure

### Option 1: Pin OCIRepository to a Specific Version

```bash
# Find previous stable artifact
flux list artifact oci://ghcr.io/<owner>/homelab/platform | grep -E '^\d+\.\d+\.\d+$'

# Patch live OCIRepository to pin a specific tag
KUBECONFIG=~/.kube/live.yaml kubectl patch ocirepository flux-system -n flux-system \
  --type=merge \
  -p '{"spec":{"ref":{"tag":"<previous-stable-tag>"}}}'
```

**Remember to revert the pin** after fixing the issue -- otherwise new promotions will be ignored.

### Option 2: Revert the PR and Let Pipeline Run

The safest rollback is to revert the breaking PR on main. The pipeline will build a new artifact with the reverted state, which will naturally promote through integration to live.

### Option 3: Re-tag a Previous Artifact

```bash
# Tag a known-good artifact with a higher stable semver
flux tag artifact \
  oci://ghcr.io/<owner>/homelab/platform:validated-<old-sha> \
  --tag <higher-X.Y.Z>
```

This works because the live OCIRepository picks the highest semver. Ensure the new tag is higher than the current one.

## Common Failure Modes

| Symptom | Cause | Fix |
|---------|-------|-----|
| Build succeeds, integration does not update | OCIRepository semver does not match RC tags | Verify `>= 0.0.0-0` in OCIRepository spec |
| Validation passes, live does not update | Tag workflow did not create stable semver tag | Check tag-validated-artifact workflow logs |
| `repository_dispatch` not received by GHA | GitHub token in flux-system secret lacks `repo` scope | Update token with correct scopes |
| Tag workflow fires repeatedly (~10min) | Alert fires on every Flux reconciliation cycle | Normal -- idempotency guard skips already-validated artifacts |
| Artifact push fails in build workflow | GHCR auth issue | Check `GITHUB_TOKEN` has `packages:write` permission |
| Live picks up wrong version | Semver ordering issue with RC numbering | Verify stable tag is strictly higher than current |
| Integration shows "no matching artifact" | OCIRepository URL or semver misconfigured | Check `oci_url` and `oci_semver` in cluster bootstrap config |

## Key Files Reference

| File | Purpose |
|------|---------|
| `.github/workflows/build-platform-artifact.yaml` | Build and push OCI artifact on merge to main |
| `.github/workflows/tag-validated-artifact.yaml` | Promote validated artifact (tag stable semver) |
| `kubernetes/platform/config/flux-notifications/canary-alert.yaml` | Alert that triggers repository_dispatch |
| `kubernetes/platform/config/flux-notifications/github-provider.yaml` | GitHub dispatch provider for Flux alerts |
| `kubernetes/platform/config/canary-checker/platform-health.yaml` | Platform health validation checks |
| `infrastructure/modules/config/main.tf` | OCI semver constraints per cluster |
| `infrastructure/modules/bootstrap/resources/instance-oci.yaml.tftpl` | OCIRepository bootstrap template |

## Cross-References

| Document | Focus |
|----------|-------|
| `.github/CLAUDE.md` | Complete pipeline architecture and debugging guide |
| `kubernetes/clusters/CLAUDE.md` | Per-cluster source types and promotion path |
| `kubernetes/platform/CLAUDE.md` | Flux patterns, version management |
| `flux-gitops` skill | Adding Helm releases and ResourceSet patterns |
