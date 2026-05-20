---
name: kind:cluster
description: Manage Kind clusters for local Kagenti testing. Create, destroy, deploy platform, and run E2E tests.
---

# Kind Cluster Management Skill

Manage Kind (Kubernetes in Docker) clusters for local Kagenti development and testing.

## When to Use

- Creating a new local test cluster
- Destroying an existing cluster
- Deploying Kagenti platform to Kind
- Running E2E tests locally
- User asks "create cluster", "deploy locally", or "run tests"

## Quick Start

```bash
# Full workflow: create cluster -> deploy platform -> run tests
./.github/scripts/local-setup/kind-full-test.sh
```

## Individual Scripts

### Create Cluster

```bash
# Create with default name (kagenti)
./.github/scripts/kind/create-cluster.sh

# Create with custom name
./.github/scripts/kind/create-cluster.sh my-cluster

# Or with environment variable
CLUSTER_NAME=my-cluster ./.github/scripts/kind/create-cluster.sh
```

### Destroy Cluster

```bash
# Destroy cluster by name
./.github/scripts/kind/destroy-cluster.sh

# Destroy specific cluster
./.github/scripts/kind/destroy-cluster.sh my-cluster
```

### Deploy Platform

```bash
# Deploy full Kagenti platform to existing cluster
./.github/scripts/kind/deploy-platform.sh
```

This deploys:
- Kagenti platform via Ansible installer
- All platform components (Istio, Keycloak, SPIRE, etc.)
- Ollama LLM (pulls qwen2.5:0.5b model)
- Weather agent and tool demo

### Run E2E Tests

```bash
# Run E2E tests against deployed platform
./.github/scripts/kind/run-e2e-tests.sh
```

Tests include:
- Platform deployment health
- Agent conversation via A2A protocol
- MCP tool invocation
- Ollama LLM integration

### Access UI

```bash
# Show access information and port-forward commands
./.github/scripts/kind/access-ui.sh
```

Then run the suggested command and visit:
- Kagenti UI: http://kagenti-ui.localtest.me:8080
- Keycloak: http://keycloak.localtest.me:8080
- Phoenix: http://phoenix.localtest.me:8080
- Kiali: http://kiali.localtest.me:8080

## Full Test Workflows

### Kind Full Test

```bash
# Full test: create -> deploy -> test (keeps cluster)
./.github/scripts/local-setup/kind-full-test.sh

# Destroy cluster after test
./.github/scripts/local-setup/kind-full-test.sh --include-cluster-destroy
```

### Manual Step-by-Step

```bash
# 1. Create cluster
./.github/scripts/kind/create-cluster.sh

# 2. Deploy platform (~15-20 minutes)
./.github/scripts/kind/deploy-platform.sh

# 3. Run tests
./.github/scripts/kind/run-e2e-tests.sh

# 4. Access UI
./.github/scripts/kind/access-ui.sh
```

## Prerequisites

- Docker Desktop/Rancher Desktop/Podman (12GB RAM, 4 cores minimum)
- Kind: `brew install kind`
- kubectl: `brew install kubectl`
- helm: `brew install helm`
- Python 3.11+ with uv

## Cluster Configuration

Default Kind config: `deployments/ansible/kind/kind-config-registry.yaml`

Custom config:
```bash
KIND_CONFIG=/path/to/config.yaml ./.github/scripts/kind/create-cluster.sh
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `CLUSTER_NAME` | kagenti | Kind cluster name |
| `KIND_CONFIG` | kind-config-registry.yaml | Kind configuration file |
| `SKIP_OLLAMA` | false | Skip Ollama installation |
| `SKIP_AGENTS` | false | Skip agent deployment |

## Debugging

### Check Cluster Status

```bash
# List clusters
kind get clusters

# Check nodes
kubectl get nodes

# Check all pods
kubectl get pods -A
```

### View Logs

```bash
# Agent logs
kubectl logs -n team1 deployment/weather-service --tail=100 -f

# Tool logs
kubectl logs -n team1 deployment/weather-tool --tail=100 -f

# Platform operator
kubectl logs -n kagenti-system deployment/kagenti-platform-operator --tail=100 -f
```

### Check Events

```bash
kubectl get events -A --sort-by='.lastTimestamp' | tail -50
```

### Ollama Status

```bash
# Check if running
ps aux | grep ollama

# List models
ollama list

# Test API
curl http://localhost:11434/api/tags
```

## Troubleshooting

### Cluster Creation Fails

```bash
# Check Docker resources
docker info | grep -E "CPUs|Total Memory"

# Increase Docker Desktop resources to 12GB+ RAM, 4+ CPUs
```

### Platform Deployment Timeout

```bash
# Check pod status
kubectl get pods -A | grep -v Running

# Check events
kubectl get events -A --sort-by='.lastTimestamp' | tail -30

# Retry
./.github/scripts/kind/destroy-cluster.sh
./.github/scripts/kind/create-cluster.sh
./.github/scripts/kind/deploy-platform.sh
```

### E2E Tests Fail

```bash
# Check agent health
kubectl get pods -n team1

# View agent logs
kubectl logs -n team1 deployment/weather-service --tail=100

# Check Ollama
ollama list | grep qwen
```

### UI Not Accessible

```bash
# Check gateway pod
kubectl get pods -n kagenti-system -l app=http-istio

# Restart port-forward
kubectl port-forward -n kagenti-system svc/http-istio 8080:80
```

## Related Skills

- **local:testing**: Detailed local testing guide
- **kagenti:deploy**: Alternative deployment via Python installer
- **k8s:pods**: Debug pod issues
- **k8s:logs**: Query logs

## Related Documentation

- `.github/scripts/local-setup/README.md` - Local setup documentation
- `deployments/ansible/README.md` - Ansible deployment guide
