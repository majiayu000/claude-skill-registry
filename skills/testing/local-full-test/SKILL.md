---
name: local:full-test
description: Run full end-to-end test workflows for Kagenti. Supports Kind and HyperShift clusters with automated setup and testing.
---

# Local Full Test Skill

Run complete end-to-end test workflows that create clusters, deploy Kagenti, and run tests.

## When to Use

- Running full CI-like workflow locally
- Testing before submitting PR
- Validating changes on real clusters
- User asks "run full test", "test everything", or "validate deployment"

## Quick Start

### Kind (Local Docker)

```bash
# Full test with Kind cluster
./.github/scripts/local-setup/kind-full-test.sh
```

### OpenShift (Standard RHOCP)

```bash
# Login to any OpenShift cluster
oc login https://api.your-cluster.example.com:6443 -u kubeadmin -p <password>

# Full test (no AWS/.env needed)
./.github/scripts/local-setup/openshift-full-test.sh

# Show help
./.github/scripts/local-setup/openshift-full-test.sh --help
```

### HyperShift (AWS OpenShift)

```bash
# Setup first (one-time)
./.github/scripts/hypershift/preflight-check.sh
./.github/scripts/hypershift/setup-hypershift-ci-credentials.sh
./.github/scripts/hypershift/local-setup.sh

# Full test with HyperShift cluster (keeps cluster after)
source .env.kagenti-hypershift-custom
./.github/scripts/local-setup/hypershift-full-test.sh --skip-cluster-destroy

# With custom suffix
./.github/scripts/local-setup/hypershift-full-test.sh pr123 --skip-cluster-destroy

# Include cleanup after test
./.github/scripts/local-setup/hypershift-full-test.sh --include-cluster-destroy

# Show help
./.github/scripts/local-setup/hypershift-full-test.sh --help
```

## Kind Full Test Workflow

The `kind-full-test.sh` script runs:

1. **Cleanup** - Remove existing cluster (optional)
2. **Create Cluster** - Create Kind cluster
3. **Deploy Platform** - Deploy Kagenti via Ansible
4. **Deploy Agents** - Build and deploy demo agents
5. **Run E2E Tests** - Execute test suite
6. **Show Access** - Display UI access information

### Options

```bash
# Keep cluster after test (default)
./.github/scripts/local-setup/kind-full-test.sh

# Destroy cluster after test
./.github/scripts/local-setup/kind-full-test.sh --include-cluster-destroy

# Skip specific phases
SKIP_DEPLOY=true ./.github/scripts/local-setup/kind-full-test.sh
SKIP_TESTS=true ./.github/scripts/local-setup/kind-full-test.sh
```

## HyperShift Full Test Workflow

The `hypershift-full-test.sh` script runs:

1. **Create Cluster** - Create HyperShift cluster on AWS (~15 min)
2. **Deploy Platform** - Deploy Kagenti via Ansible
3. **Wait for CRDs** - Wait for Kagenti CRDs
4. **Apply Pipelines** - Apply Tekton pipeline templates
5. **Build Tools** - Build weather tool via Tekton
6. **Deploy Agents** - Deploy weather agent and tool
7. **Run E2E Tests** - Execute test suite
8. **Cleanup** (optional) - Destroy cluster

### Options

```bash
# With custom cluster suffix
./.github/scripts/local-setup/hypershift-full-test.sh pr529

# Keep cluster (default with --skip-cluster-destroy)
./.github/scripts/local-setup/hypershift-full-test.sh --skip-cluster-destroy

# Destroy cluster after test
./.github/scripts/local-setup/hypershift-full-test.sh --include-cluster-destroy
```

## Manual Step-by-Step

### Kind Workflow

```bash
# 1. Create cluster
./.github/scripts/kind/create-cluster.sh

# 2. Deploy platform
./.github/scripts/kind/deploy-platform.sh

# 3. Run E2E tests
./.github/scripts/kind/run-e2e-tests.sh

# 4. Access UI
./.github/scripts/kind/access-ui.sh
```

### HyperShift Workflow

```bash
# 1. Create cluster
./.github/scripts/hypershift/create-cluster.sh

# 2. Set kubeconfig
export KUBECONFIG=~/clusters/hcp/<cluster-name>/auth/kubeconfig

# 3. Deploy platform
./.github/scripts/kagenti-operator/30-run-installer.sh --env ocp
./.github/scripts/kagenti-operator/41-wait-crds.sh
./.github/scripts/kagenti-operator/42-apply-pipeline-template.sh

# 4. Deploy agents
./.github/scripts/kagenti-operator/71-build-weather-tool.sh
./.github/scripts/kagenti-operator/72-deploy-weather-tool.sh
./.github/scripts/kagenti-operator/73-patch-weather-tool.sh
./.github/scripts/kagenti-operator/74-deploy-weather-agent.sh

# 5. Run E2E tests
export AGENT_URL="https://$(oc get route -n team1 weather-service -o jsonpath='{.spec.host}')"
export KAGENTI_CONFIG_FILE=deployments/envs/ocp_values.yaml
./.github/scripts/kagenti-operator/90-run-e2e-tests.sh

# 6. Cleanup (when done)
./.github/scripts/hypershift/destroy-cluster.sh <suffix>
```

## Show Services

```bash
# Show all deployed services and access URLs
./.github/scripts/local-setup/show-services.sh
```

Output includes:
- Kagenti UI URL
- Keycloak URL
- Phoenix URL
- Kiali URL
- Agent endpoints
- Port-forward commands

## Deploy Kagenti Operator Only

For testing just the operator:

```bash
./.github/scripts/local-setup/deploy-kagenti-operator.sh
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `SKIP_DEPLOY` | Skip platform deployment |
| `SKIP_TESTS` | Skip E2E tests |
| `SKIP_OLLAMA` | Skip Ollama installation (Kind) |
| `SKIP_LLAMA` | Skip Ollama in HyperShift tests |
| `CLUSTER_NAME` | Custom cluster name |
| `KUBECONFIG` | Kubernetes config file (management cluster for HyperShift) |
| `HOSTED_KUBECONFIG` | Hosted cluster kubeconfig (for running middle phases only) |

## HyperShift: Dual Kubeconfig

HyperShift workflows use **two separate kubeconfigs**:

| Kubeconfig | Purpose | Location |
|------------|---------|----------|
| **Management cluster** | Create/destroy hosted clusters | Set via `KUBECONFIG` in `.env.kagenti-hypershift-custom` |
| **Hosted cluster** | Deploy Kagenti, run tests | `~/clusters/hcp/<cluster-name>/auth/kubeconfig` |

The script automatically switches between them at phase boundaries.

### Simplified Usage (Middle Phases Only)

When only running install/agents/test (skipping create/destroy), you can set just `HOSTED_KUBECONFIG`:

```bash
# No need to source .env - just set the hosted cluster kubeconfig
export HOSTED_KUBECONFIG=~/clusters/hcp/kagenti-hypershift-custom-ladas/auth/kubeconfig
./.github/scripts/local-setup/hypershift-full-test.sh --skip-cluster-create --skip-cluster-destroy
```

## Prerequisites

### Kind

- Docker Desktop/Rancher Desktop (12GB RAM, 4 cores)
- Kind, kubectl, helm
- Python 3.11+ with uv

### HyperShift

- AWS CLI with admin credentials
- OpenShift CLI (oc)
- Ansible
- HyperShift credentials configured

## Debugging Failed Tests

### Check Pod Status

```bash
# All namespaces
kubectl get pods -A | grep -v Running

# Specific namespace
kubectl get pods -n team1
kubectl get pods -n kagenti-system
```

### View Logs

```bash
# Agent logs
kubectl logs -n team1 deployment/weather-service --tail=100

# Operator logs
kubectl logs -n kagenti-system -l app=kagenti-operator --tail=100
```

### Check Events

```bash
kubectl get events -A --sort-by='.lastTimestamp' | tail -30
```

### Retry Tests

```bash
# Just rerun tests (don't redeploy)
./.github/scripts/kind/run-e2e-tests.sh

# Or for HyperShift
./.github/scripts/kagenti-operator/90-run-e2e-tests.sh
```

## Comparison: Kind vs HyperShift

| Aspect | Kind | HyperShift |
|--------|------|------------|
| Setup time | ~15 min | ~25 min |
| Cost | Free | AWS costs |
| Platform | Docker | AWS |
| Use case | Dev, quick tests | Real OCP testing |
| Cleanup | Instant | ~5 min |
| Resources | Local machine | AWS EC2 |

## Related Skills

- **kind:cluster**: Manage Kind clusters
- **hypershift:cluster**: Manage HyperShift clusters
- **kagenti:operator**: Deploy Kagenti operator
- **local:testing**: Detailed local testing guide

## Related Documentation

- `.github/scripts/local-setup/README.md` - Local setup documentation
