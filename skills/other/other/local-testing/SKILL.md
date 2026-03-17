---
name: local:testing
description: Test Kagenti platform locally using Kind. Scripts for deploy, test, and access.
---

# Local Testing Skill

This skill helps you test Kagenti platform locally using Kind (Kubernetes in Docker).

## Overview

The `local-testing/` directory contains scripts that mirror the GitHub Actions CI workflow, allowing you to:
- Deploy the full Kagenti platform locally
- Run E2E tests with Ollama LLM integration
- Access the Kagenti UI and services
- Debug agent and tool deployments

## Prerequisites

Ensure you have:
- Docker Desktop/Rancher Desktop/Podman (12GB RAM, 4 cores minimum)
- Kind, kubectl, helm installed
- Python 3.11+ with uv
- jq for JSON parsing

## Available Scripts

### 1. Cleanup Cluster

Wipes the existing Kind cluster completely:

```bash
./local-testing/cleanup-cluster.sh
```

Use this when you want a fresh start or cluster is in a bad state.

### 2. Deploy Platform

Deploys the full Kagenti platform (takes ~15-20 minutes):

```bash
./local-testing/deploy-platform.sh
```

This script:
- Creates Kind cluster via Ansible installer
- Deploys all platform components (Keycloak, PostgreSQL, Istio, SPIRE)
- Installs Ollama and pulls qwen2.5:0.5b model
- Deploys weather agent and tool

### 3. Run E2E Tests

Runs the E2E test suite:

```bash
./local-testing/run-e2e-tests.sh
```

Validates:
- Platform deployment health
- Agent conversation via A2A protocol
- Ollama LLM integration
- MCP tool invocation

### 4. Access UI

Shows access information and port-forward commands:

```bash
./local-testing/access-ui.sh
```

Then run the suggested command:
```bash
kubectl port-forward -n kagenti-system svc/http-istio 8080:80
```

Visit: http://kagenti-ui.localtest.me:8080

## Typical Workflow

### Full Redeploy and Test

```bash
# 1. Clean up existing cluster
./local-testing/cleanup-cluster.sh

# 2. Deploy platform (wait ~15-20 minutes)
./local-testing/deploy-platform.sh

# 3. Run E2E tests
./local-testing/run-e2e-tests.sh

# 4. Access UI
./local-testing/access-ui.sh
```

### Quick Test Iteration

If platform is already deployed and you just want to rerun tests:

```bash
./local-testing/run-e2e-tests.sh
```

### Development Cycle

1. Make code changes
2. Run `./local-testing/deploy-platform.sh` to redeploy
3. Run `./local-testing/run-e2e-tests.sh` to validate
4. Use `./local-testing/access-ui.sh` to get UI access

## Debugging Commands

### View Logs

```bash
# Agent logs
kubectl logs -n team1 deployment/weather-service --tail=100 -f

# Tool logs
kubectl logs -n team1 deployment/weather-tool --tail=100 -f

# Platform operator
kubectl logs -n kagenti-system deployment/kagenti-platform-operator --tail=100 -f
```

### Check Pod Status

```bash
# All pods
kubectl get pods -A

# Specific namespace
kubectl get all -n team1
kubectl get all -n kagenti-system
```

### View Events

```bash
# Recent events in team1 namespace
kubectl get events -n team1 --sort-by='.lastTimestamp' | tail -30

# All events
kubectl get events -A --sort-by='.lastTimestamp' | tail -50
```

### Ollama Status

```bash
# Check if running
ps aux | grep ollama

# Check models
ollama list

# Test directly
curl http://localhost:11434/api/tags
```

## Troubleshooting

### Platform Not Ready

If deployment times out or components aren't ready:

```bash
# Check pod status
kubectl get pods -A

# Check recent events
kubectl get events -A --sort-by='.lastTimestamp' | tail -50

# Retry deployment
./local-testing/cleanup-cluster.sh
./local-testing/deploy-platform.sh
```

### Test Failures

If E2E tests fail:

1. Check agent logs: `kubectl logs -n team1 deployment/weather-service --tail=100`
2. Check tool logs: `kubectl logs -n team1 deployment/weather-tool --tail=100`
3. Verify Ollama is running: `ps aux | grep ollama`
4. Check Ollama has model: `ollama list | grep qwen2.5`

### UI Access Issues

If UI doesn't load:

1. Verify pod is running: `kubectl get pods -n kagenti-system -l app=kagenti-ui`
2. Check Istio gateway: `kubectl get pods -n kagenti-system -l app=http-istio`
3. Restart port-forward: `kubectl port-forward -n kagenti-system svc/http-istio 8080:80`

## Notes

- These scripts are for local development only (not committed to repo)
- Scripts are in `.gitignore` to avoid accidental commits
- Deployment uses same Ansible installer as CI
- Cluster name is `kagenti` (matches CI workflow)
- Secrets used are test values (not production)

## Files Location

All scripts are in: `local-testing/`
- `cleanup-cluster.sh` - Wipe cluster
- `deploy-platform.sh` - Deploy platform
- `run-e2e-tests.sh` - Run tests
- `access-ui.sh` - Access information
- `README.md` - Full documentation

## Related Skills

- `local:full-test` - Complete test workflows for Kind and HyperShift
- `kind:cluster` - Create/destroy Kind clusters
- `kagenti:deploy` - Deploy platform
