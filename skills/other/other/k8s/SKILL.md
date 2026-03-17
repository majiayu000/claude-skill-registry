---
name: sayt-k8s
description: >
  How to write skaffold.yaml — preview/staging/production profiles, Kind setup,
  Cloud Run patterns.
  Use when setting up deployment pipelines, K8s previews, staging, or production deploys.
user-invocable: false
---

# release / verify — Skaffold Deployment

`sayt release` builds and deploys artifacts. `sayt verify` runs E2E and load tests against deployed artifacts. Both use Skaffold with profile-based progression.

## How It Works

1. `sayt release` delegates to vtr to run the release task
2. `sayt verify` delegates to vtr to run the verify task
3. Both typically invoke Skaffold with appropriate profiles
4. The deployment progresses through environments: preview → staging → production

## Deployment Progression

### Preview (Kubernetes via Kind)

Local Kubernetes cluster for full-stack testing:

```bash
# One-time setup
kind create cluster -n iris

# Deploy to preview
skaffold run -p preview
```

- Isolated deployment with mocked external dependencies
- No outbound internet except for vendored resources
- All services deployed within the cluster
- Code is fully optimized (production-like builds)

### Staging (Cloud)

Shared, long-lived deployment targeted by CI/CD:

```bash
skaffold run -p staging
```

- Built hermetically by CI/CD pipeline
- Pushed to GCP by Skaffold
- Follows main branch on every commit
- Shared environment for team testing

### Production (Cloud)

Manually approved from staging:

```bash
skaffold run -p production
```

- Manually approved promotion from staging
- Modified configuration (production secrets, scaling)
- Crossplane manages infrastructure
- Cloud Run for stateless services
- Cloud SQL for databases

## Skaffold Profile Conventions

### Basic `skaffold.yaml`

```yaml
apiVersion: skaffold/v4beta11
kind: Config
metadata:
  name: my-service

build:
  artifacts:
    - image: my-service
      docker:
        dockerfile: Dockerfile

profiles:
  - name: preview
    deploy:
      kubectl:
        manifests:
          - k8s/*.yaml

  - name: staging
    deploy:
      cloudrun:
        projectid: my-project
        region: us-central1

  - name: production
    deploy:
      cloudrun:
        projectid: my-project-prod
        region: us-central1
```

### Profile-Specific Builds

```yaml
profiles:
  - name: preview
    build:
      local:
        push: false
    deploy:
      kubectl:
        manifests:
          - k8s/preview/*.yaml

  - name: staging
    build:
      googleCloudBuild:
        projectId: my-project
    deploy:
      cloudrun:
        projectid: my-project
        region: us-central1
```

## Kind Cluster Setup

For preview deployments, create a Kind cluster:

```bash
kind create cluster -n iris
```

Kind clusters are ephemeral and can be recreated at any time:

```bash
kind delete cluster -n iris
kind create cluster -n iris
```

## Cloud Run Deployment Pattern

For staging and production with GCP Cloud Run:

```yaml
profiles:
  - name: staging
    deploy:
      cloudrun:
        projectid: my-gcp-project
        region: us-central1
```

## Crossplane for Infrastructure

Production infrastructure is managed via Crossplane operators:

- Database instances (Cloud SQL)
- Storage buckets
- IAM policies
- Network configuration

Crossplane manifests live alongside Kubernetes manifests and are deployed via Skaffold.

## Verification

`sayt verify` runs tests against deployed artifacts:

- **E2E tests**: Playwright or similar against the deployed frontend
- **Load tests**: Verify performance under simulated load
- **Smoke tests**: Basic health checks and critical path validation

### Example verify task in tasks.json

```json
{
  "label": "verify",
  "type": "shell",
  "command": "playwright",
  "args": ["test", "--config", "e2e/playwright.config.ts"],
  "group": { "kind": "test" },
  "problemMatcher": []
}
```

## Writing Good Skaffold Configs

1. **Use profiles** — preview, staging, production as a minimum
2. **Preview builds locally** — Set `push: false` for Kind deployments
3. **Staging uses cloud build** — GCB or similar for hermetic builds
4. **Production is a promotion** — Same image as staging, different config
5. **Keep manifests separate** — Use `k8s/preview/`, `k8s/staging/`, etc.

## Current flags

!`sayt help release 2>&1 || true`
!`sayt help verify 2>&1 || true`
