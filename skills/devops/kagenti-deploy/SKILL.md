---
name: kagenti:deploy
description: Deploy or redeploy the Kagenti Kind cluster using the Python installer - quick redeploy, manual steps, and troubleshooting
---

# Deploy Cluster Skill

This skill guides you through deploying or redeploying the Kagenti Kind cluster using the Python installer.

## When to Use

- Setting up new local development cluster
- Full cluster redeploy after major changes
- Cluster is corrupted or unstable
- Testing clean deployment
- Running E2E tests locally

## Resource Requirements

**Minimum** (from CLAUDE.md):
- 12GB RAM
- 4 CPU cores
- Docker Desktop, Rancher Desktop, or Podman

**Recommended for development**:
- 16GB RAM
- 6 CPU cores
- 50GB free disk space

## Multiple Clusters

You can run multiple Kind clusters:
- **agent-platform** - Created by kagenti-installer (default)
- **kagenti-demo** - Your existing cluster
- Each cluster runs independently with its own name

Check existing clusters:
```bash
kind get clusters
```

## Quick Redeploy (Full Installation)

```bash
# 1. Setup environment (first time only)
cp kagenti/installer/app/.env_template kagenti/installer/app/.env
# Edit .env with:
# - GITHUB_USER=<your-github-username>
# - GITHUB_TOKEN=<ghcr.io-token>
# - OPENAI_API_KEY=<openai-key>
# - AGENT_NAMESPACES=team1,team2

# 2. Full redeploy (creates new cluster + installs everything)
cd kagenti/installer
uv run kagenti-installer

# What it does (15-25 minutes):
# ✓ Creates Kind cluster "agent-platform"
# ✓ Installs registry (optional)
# ✓ Installs Tekton Pipelines
# ✓ Installs Cert-Manager
# ✓ Installs Platform Operator
# ✓ Installs Istio Ambient
# ✓ Installs Gateway API
# ✓ Installs SPIRE
# ✓ Installs MCP Gateway
# ✓ Installs Keycloak + PostgreSQL
# ✓ Installs Addons (Prometheus, Kiali, Phoenix)
# ✓ Installs UI
# ✓ Installs ToolHive
# ✓ Creates agent namespaces (team1, team2)
```

## Use Existing Cluster

```bash
# Install on already running Kind cluster
cd kagenti/installer
uv run kagenti-installer --use-existing-cluster
```

## Cleanup and Fresh Install

```bash
# 1. Delete existing cluster
kind delete cluster --name agent-platform

# 2. Clean Docker images (optional)
docker system prune -a

# 3. Fresh install
cd kagenti/installer
uv run kagenti-installer
```

## Selective Component Installation

Skip components you don't need for faster deployment:

```bash
# Minimal install (no UI, no observability, no auth)
cd kagenti/installer
uv run kagenti-installer \
  --skip-install ui \
  --skip-install addons \
  --skip-install keycloak \
  --skip-install spire

# Skip specific components
uv run kagenti-installer \
  --skip-install tekton \
  --skip-install operator \
  --skip-install gateway \
  --skip-install mcp_gateway

# Install only core platform (for testing)
uv run kagenti-installer \
  --skip-install addons \
  --skip-install ui \
  --skip-install keycloak \
  --skip-install agents
```

**Available components to skip**:
- `registry` - Internal container registry
- `tekton` - Tekton Pipelines (build system)
- `cert_manager` - Certificate management
- `operator` - Platform Operator (deprecated, being replaced by kagenti-operator)
- `istio` - Service mesh
- `gateway` - Kubernetes Gateway API
- `spire` - Workload identity
- `mcp_gateway` - MCP Gateway
- `addons` - Observability (Prometheus, Kiali, Phoenix)
- `ui` - Kagenti UI
- `keycloak` - Authentication
- `agents` - Demo agents
- `metrics_server` - Metrics server
- `inspector` - MCP inspector
- `toolhive` - ToolHive operator

## Deploy Weather Agents (Demo)

```bash
# After platform is installed
kubectl apply -f kagenti/examples/components/
```

This creates:
- **weather-tool** in team1 namespace
- **weather-service** in team1 namespace

## Check Deployment Health

### Quick Health Check

```bash
# Run the health check script (from CI)
chmod +x .github/scripts/verify_deployment.sh
.github/scripts/verify_deployment.sh

# What it checks:
# ✓ Resource usage (RAM, disk, CPU, containers)
# ✓ Deployment status (weather-tool, weather-service, keycloak, operator)
# ✓ Pod health summary (total, running, pending, failed, crashloop)
# ✓ Failed pod details (events, error logs)
```

### Manual Health Checks

```bash
# All pods
kubectl get pods -A

# Failed pods only
kubectl get pods -A --field-selector=status.phase!=Running,status.phase!=Succeeded

# Specific namespace
kubectl get pods -n team1
kubectl get pods -n keycloak
kubectl get pods -n kagenti-system

# Deployments
kubectl get deployments -A

# Services
kubectl get svc -A
```

## Run E2E Tests Locally

After platform is deployed:

```bash
cd kagenti

# Install test dependencies
uv pip install -r tests/requirements.txt

# Run all deployment health tests
uv run pytest tests/e2e/test_deployment_health.py -v

# Run only critical tests
uv run pytest tests/e2e/test_deployment_health.py -v --only-critical

# Run specific test
uv run pytest tests/e2e/test_deployment_health.py::TestWeatherToolDeployment::test_weather_tool_deployment_ready -v

# Exclude Keycloak tests
uv run pytest tests/e2e/test_deployment_health.py -v --exclude-app=keycloak

# Increase timeout
uv run pytest tests/e2e/test_deployment_health.py -v --app-timeout=600
```

## Run Full CI Workflow Locally

Simulate what runs in CI:

```bash
# 1. Install platform
cd kagenti/installer
uv run kagenti-installer --silent

# 2. Deploy weather agents
cd ../..
kubectl apply -f kagenti/examples/components/

# 3. Wait for deployments
kubectl wait --for=condition=available --timeout=300s deployment/weather-tool -n team1
kubectl wait --for=condition=available --timeout=300s deployment/weather-service -n team1

# 4. Run health check
chmod +x .github/scripts/verify_deployment.sh
.github/scripts/verify_deployment.sh

# 5. Run E2E tests
cd kagenti
uv pip install -r tests/requirements.txt
uv run pytest tests/e2e/test_deployment_health.py -v \
  --timeout=300 \
  --tb=short
```

## Troubleshooting Deployment

### Issue: Installer Timeout or Slow

```bash
# Check Docker resource allocation
docker info | grep -E "CPUs|Total Memory"

# Increase timeout (images can be slow to pull)
# The installer will retry - just re-run:
cd kagenti/installer
uv run kagenti-installer --use-existing-cluster
```

### Issue: "Error loading config file" or kubectl errors

```bash
# Check kubeconfig
kubectl config current-context

# Should show: kind-agent-platform

# If not, set context
kubectl config use-context kind-agent-platform
```

### Issue: Pods stuck in ImagePullBackOff

```bash
# Check if images are available in Kind
docker exec agent-platform-control-plane crictl images

# Reload images (for custom builds)
kind load docker-image <image-name> --name agent-platform

# Check pod description for error
kubectl describe pod <pod-name> -n <namespace>
```

### Issue: Keycloak Connection Issues

```bash
# Restart Keycloak
kubectl delete -n keycloak -f kagenti/installer/app/resources/keycloak.yaml
kubectl apply -n keycloak -f kagenti/installer/app/resources/keycloak.yaml

# Restart Istio ztunnel
kubectl rollout restart daemonset -n istio-system ztunnel

# Restart Gateway
kubectl rollout restart -n kagenti-system deployment http-istio
```

### Issue: Need to Update Secrets

```bash
# Update GitHub token
kubectl -n <namespace> delete secret github-token-secret

# Re-run installer to recreate secrets
cd kagenti/installer
uv run kagenti-installer --use-existing-cluster
```

### Issue: Blank UI on macOS

```bash
# Disable Screen Time Content & Privacy Restrictions
# System Settings > Screen Time > Content & Privacy
```

### Issue: GitHub Token Errors

```bash
# Ensure token has correct scopes:
# - repo:all
# - write:packages
# - read:packages

# Clear cached credentials
docker logout ghcr.io
```

## Access Platform Services

After deployment, access these services:

```bash
# Kagenti UI
open http://kagenti-ui.localtest.me:8080

# Keycloak Admin Console
open http://keycloak.localtest.me:8080
# Username: admin
# Password: (from Keycloak secret)
kubectl get secret -n keycloak keycloak-initial-admin -o jsonpath='{.data.password}' | base64 -d

# Prometheus (if addons installed)
kubectl port-forward -n observability svc/prometheus 9090:9090
open http://localhost:9090

# Grafana (if addons installed)
kubectl port-forward -n observability svc/grafana 3000:3000
open http://localhost:3000

# Kiali (if addons installed)
kubectl port-forward -n kiali svc/kiali 20001:20001
open http://localhost:20001
```

## Platform Configuration

### Environment Variables (.env file)

Required in `kagenti/installer/app/.env`:

```bash
# GitHub access for ghcr.io
GITHUB_USER=your-username
GITHUB_TOKEN=ghp_xxx  # Classic token with repo:all, write:packages, read:packages

# OpenAI API (for agents)
OPENAI_API_KEY=sk-xxx

# Agent namespaces
AGENT_NAMESPACES=team1,team2

# Optional: Slack (for Slack tool demo)
SLACK_BOT_TOKEN=xoxb-xxx
```

### Cluster Configuration

Edit `kagenti/installer/app/config.py`:

```python
CLUSTER_NAME = "agent-platform"  # Kind cluster name
DOMAIN_NAME = "localtest.me"     # Domain for services
CONTAINER_ENGINE = "docker"      # or "podman"
```

## Manual Step-by-Step Deployment (Advanced)

For debugging or understanding the installer:

```bash
# 1. Create Kind cluster manually
cat <<EOF | kind create cluster --name agent-platform --config=-
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
  extraPortMappings:
  - containerPort: 30080
    hostPort: 8080
  - containerPort: 30443
    hostPort: 9443
EOF

# 2. Set kubeconfig context
kubectl config use-context kind-agent-platform

# 3. Install components one by one
cd kagenti/installer

# Install Tekton
kubectl apply -f https://storage.googleapis.com/tekton-releases/pipeline/previous/v0.66.0/release.yaml

# Install Cert-Manager
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.16.2/cert-manager.yaml

# ... (see installer code for full sequence)
```

## Related Skills

- **k8s:health**: Check comprehensive platform health
- **k8s:logs**: Query logs for debugging
- **k8s:pods**: Debug pod issues

## Pro Tips

1. **Use --use-existing-cluster**: Faster reinstalls without recreating cluster
2. **Skip components**: Use --skip-install for faster iteration
3. **Multiple clusters**: Use different cluster names for parallel testing
4. **Resource allocation**: Ensure Docker/Podman has enough RAM (16GB recommended)
5. **Cache images**: Pulled images are cached - subsequent installs are faster
6. **Silent mode**: Use --silent to skip interactive prompts
7. **Check logs**: If installer fails, check pod logs in kagenti-system namespace

## Common Workflows

### Daily Development
```bash
# Use existing cluster, skip slow components
cd kagenti/installer
uv run kagenti-installer --use-existing-cluster \
  --skip-install addons \
  --skip-install keycloak
```

### Full Test Before PR
```bash
# Fresh cluster, all components, run tests
kind delete cluster --name agent-platform
cd kagenti/installer
uv run kagenti-installer --silent
kubectl apply -f kagenti/examples/components/
.github/scripts/verify_deployment.sh
cd kagenti && uv run pytest tests/e2e/test_deployment_health.py -v
```

### Quick Agent Testing
```bash
# Minimal platform, just enough for agents
cd kagenti/installer
uv run kagenti-installer \
  --skip-install addons \
  --skip-install ui \
  --skip-install keycloak
kubectl apply -f kagenti/examples/components/
```
