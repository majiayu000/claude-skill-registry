---
name: kind
description: Manage Kind (Kubernetes in Docker) clusters for local Kagenti development and testing.
---

# Kind Skills

Skills for managing Kind clusters for local development.

## Available Sub-Skills

| Skill | Description |
|-------|-------------|
| `kind:cluster` | Create, destroy, and manage Kind clusters |

## Quick Start

```bash
# Create cluster
./.github/scripts/kind/create-cluster.sh

# Deploy platform
./.github/scripts/kind/deploy-platform.sh

# Run E2E tests
./.github/scripts/kind/run-e2e-tests.sh

# Access UI
./.github/scripts/kind/access-ui.sh
```

## Full Test Workflow

```bash
# Full test: create -> deploy -> test
./.github/scripts/local-setup/kind-full-test.sh
```

## Prerequisites

- Docker Desktop/Rancher Desktop (12GB RAM, 4 cores)
- Kind: `brew install kind`
- kubectl, helm

## Access URLs

After deployment:
- Kagenti UI: http://kagenti-ui.localtest.me:8080
- Keycloak: http://keycloak.localtest.me:8080
- Phoenix: http://phoenix.localtest.me:8080
- Kiali: http://kiali.localtest.me:8080
