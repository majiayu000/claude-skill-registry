---
name: kagenti:operator
description: Deploy and manage Kagenti operator, agents, and tools on Kubernetes. Handles installer, CRDs, pipelines, and demo deployments.
---

# Kagenti Operator Skill

Deploy and manage Kagenti operator, agents, and tools on Kubernetes clusters.

## When to Use

- Deploying Kagenti platform to a cluster
- Building and deploying agents/tools
- Running E2E tests
- User asks "deploy kagenti", "build agent", or "run e2e tests"

## Quick Deploy (Kind)

```bash
# Deploy everything to Kind cluster
./.github/scripts/kagenti-operator/30-run-installer.sh

# Wait for CRDs and apply pipeline template
./.github/scripts/kagenti-operator/41-wait-crds.sh
./.github/scripts/kagenti-operator/42-apply-pipeline-template.sh
```

## Quick Deploy (OpenShift/HyperShift)

```bash
# Set kubeconfig for target cluster
export KUBECONFIG=~/clusters/hcp/<cluster-name>/auth/kubeconfig

# Deploy with OCP values
./.github/scripts/kagenti-operator/30-run-installer.sh --env ocp

# Wait for CRDs and apply pipeline template
./.github/scripts/kagenti-operator/41-wait-crds.sh
./.github/scripts/kagenti-operator/42-apply-pipeline-template.sh
```

## Deploy Demo Agents

Full demo deployment workflow:

```bash
# 1. Setup team1 namespace (if not exists)
./.github/scripts/kagenti-operator/70-setup-team1-namespace.sh

# 2. Build weather tool (Tekton pipeline)
./.github/scripts/kagenti-operator/71-build-weather-tool.sh

# 3. Deploy weather tool
./.github/scripts/kagenti-operator/72-deploy-weather-tool.sh

# 4. Patch weather tool (HTTPRoute, MCP config)
./.github/scripts/kagenti-operator/73-patch-weather-tool.sh

# 5. Deploy weather agent
./.github/scripts/kagenti-operator/74-deploy-weather-agent.sh
```

## Run E2E Tests

```bash
# Set agent URL (Kind)
export AGENT_URL="http://localhost:8000"
kubectl port-forward -n team1 svc/weather-service 8000:8000 &

# Set agent URL (OpenShift)
export AGENT_URL="https://$(oc get route -n team1 weather-service -o jsonpath='{.spec.host}')"

# Set config file
export KAGENTI_CONFIG_FILE=deployments/envs/dev_values.yaml  # Kind
export KAGENTI_CONFIG_FILE=deployments/envs/ocp_values.yaml  # OpenShift

# Run tests
./.github/scripts/kagenti-operator/90-run-e2e-tests.sh
```

## Script Reference

### Core Deployment

| Script | Description |
|--------|-------------|
| `30-run-installer.sh` | Run Ansible installer for Kagenti platform |
| `41-wait-crds.sh` | Wait for Kagenti CRDs to be available |
| `42-apply-pipeline-template.sh` | Apply Tekton pipeline templates |

### Namespace Setup

| Script | Description |
|--------|-------------|
| `70-setup-team1-namespace.sh` | Setup team1 namespace with required resources |

### Agent/Tool Deployment

| Script | Description |
|--------|-------------|
| `71-build-weather-tool.sh` | Build weather tool via Tekton pipeline |
| `72-deploy-weather-tool.sh` | Deploy weather tool Component CR |
| `73-patch-weather-tool.sh` | Patch weather tool with HTTPRoute/MCP config |
| `74-deploy-weather-agent.sh` | Deploy weather agent Component CR |
| `75-deploy-weather-tool-shipwright.sh` | Alternative: deploy with Shipwright |

### Testing

| Script | Description |
|--------|-------------|
| `90-run-e2e-tests.sh` | Run E2E test suite |

## Environment Variables

### Installer

| Variable | Default | Description |
|----------|---------|-------------|
| `--env` | dev | Environment (dev, ocp, test) |
| `KUBECONFIG` | ~/.kube/config | Kubernetes config |

### E2E Tests

| Variable | Default | Description |
|----------|---------|-------------|
| `AGENT_URL` | required | Agent endpoint URL |
| `KAGENTI_CONFIG_FILE` | required | Values file for config |
| `PHOENIX_URL` | (optional) | Phoenix observability URL |

## Installer Options

```bash
# View all options
./.github/scripts/kagenti-operator/30-run-installer.sh --help

# Common options:
./.github/scripts/kagenti-operator/30-run-installer.sh --env dev     # Kind/local
./.github/scripts/kagenti-operator/30-run-installer.sh --env ocp     # OpenShift
./.github/scripts/kagenti-operator/30-run-installer.sh --env test    # CI testing
```

## Debugging

### Check Operator Status

```bash
# Operator pods
kubectl get pods -n kagenti-system -l app=kagenti-operator

# Operator logs
kubectl logs -n kagenti-system -l app=kagenti-operator --tail=100

# CRDs
kubectl get crd | grep kagenti
```

### Check Agent/Tool Status

```bash
# All components
kubectl get components -A

# Agent builds
kubectl get agentbuilds -A

# Deployments
kubectl get deployments -n team1
```

### Check Tekton Pipelines

```bash
# Pipeline runs
kubectl get pipelineruns -n team1

# Task runs
kubectl get taskruns -n team1

# Pipeline logs
tkn pipelinerun logs -n team1 <pipeline-run-name>
```

### Check Routes/Ingress

```bash
# Kind (HTTPRoutes)
kubectl get httproutes -A

# OpenShift (Routes)
oc get routes -A
```

## Troubleshooting

### Installer Fails

```bash
# Check Ansible logs
# (Logs are output during run)

# Check namespace
kubectl get ns kagenti-system

# Check pods
kubectl get pods -n kagenti-system
```

### CRDs Not Available

```bash
# Check CRD installation
kubectl get crd | grep kagenti

# Re-run wait script
./.github/scripts/kagenti-operator/41-wait-crds.sh
```

### Build Fails

```bash
# Check Tekton pipeline run
kubectl get pipelineruns -n team1

# View pipeline logs
kubectl logs -n team1 -l tekton.dev/pipelineRun=<run-name>

# Check Tekton controller
kubectl logs -n tekton-pipelines deployment/tekton-pipelines-controller --tail=100
```

### Agent Not Responding

```bash
# Check pod status
kubectl get pods -n team1 -l app=weather-service

# View agent logs
kubectl logs -n team1 deployment/weather-service --tail=100

# Check service
kubectl get svc -n team1 weather-service

# Test connectivity
kubectl port-forward -n team1 svc/weather-service 8000:8000
curl http://localhost:8000/.well-known/agent.json
```

## Related Skills

- **kind:cluster**: Manage Kind clusters
- **hypershift:cluster**: Manage HyperShift clusters
- **k8s:pods**: Debug pod issues
- **k8s:logs**: Query logs

## Related Documentation

- `deployments/ansible/README.md` - Ansible deployment guide
- `docs/install.md` - Installation guide
- `docs/components.md` - Component details
