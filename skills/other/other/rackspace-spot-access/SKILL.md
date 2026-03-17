---
name: rackspace-spot-access
description: Provides step-by-step instructions for accessing the Rackspace Spot Kubernetes cluster to debug ARC runners using spotctl. Covers installation, authentication via GCP Secret Manager, kubeconfig retrieval, and common debugging commands. Activates on "spotctl", "cluster access", "rackspace debug", "kubeconfig", or "spot cluster".
allowed-tools: Read, Grep, Glob, Bash
---

# Rackspace Spot Cluster Access Guide

## Overview

This guide provides instructions for accessing the Matchpoint ARC runners Kubernetes cluster on Rackspace Spot using `spotctl`. The cluster hosts GitHub Actions self-hosted runners managed by Actions Runner Controller (ARC).

## Cluster Information

| Property | Value |
|----------|-------|
| **GCP Project** | `project-beta-407300` |
| **Secret Name** | `rackspace-spot-token` |
| **Organization ID** | `org_z0ELxD9LNTjgYwjc` |
| **Region** | `us-central-dfw-1` |
| **Cloudspace Name** | `matchpoint-runners` |
| **Cluster Purpose** | GitHub Actions ARC runners |

## Prerequisites

### Required Tools

1. **gcloud CLI** - For GCP Secret Manager access
2. **spotctl** - Rackspace Spot CLI for cluster management
3. **kubectl** - Kubernetes CLI
4. **jq** - JSON processor (optional but helpful)

### Required Permissions

- **GCP Secret Manager:** `roles/secretmanager.secretAccessor` on `project-beta-407300`
- **Rackspace Spot:** Valid API token with org access

## Installation Steps

### 1. Install spotctl

```bash
# Install spotctl via pip
pip install spotctl

# Verify installation
spotctl --version
```

**Note:** If `pip` fails, ensure Python 3.8+ is installed:
```bash
python3 --version
pip3 install spotctl
```

### 2. Authenticate with GCP (if not already)

```bash
# Login to GCP
gcloud auth login

# Set project
gcloud config set project project-beta-407300

# Verify access to secret
gcloud secrets versions access latest --secret=rackspace-spot-token
```

## Cluster Access Workflow

### Step 1: Retrieve Rackspace Spot API Token

```bash
# Get the API token from GCP Secret Manager
export RACKSPACE_SPOT_TOKEN=$(gcloud secrets versions access latest \
  --secret=rackspace-spot-token \
  --project=project-beta-407300)

# Verify token retrieved (should show non-empty string)
echo "Token retrieved: ${RACKSPACE_SPOT_TOKEN:0:20}..."
```

**Troubleshooting:**
- **Error: "Permission denied"** - Ensure you have `roles/secretmanager.secretAccessor`
- **Error: "Secret not found"** - Verify project ID and secret name
- **Empty token** - Check secret has a value in GCP Console

### Step 2: Configure spotctl

```bash
# Configure spotctl with organization and token
spotctl configure set organization org_z0ELxD9LNTjgYwjc
spotctl configure set token "$RACKSPACE_SPOT_TOKEN"

# Verify configuration
spotctl configure get organization
spotctl configure get token  # Will show masked token
```

**Alternative: Use environment variable directly**

```bash
# spotctl respects SPOT_TOKEN env var
export SPOT_TOKEN="$RACKSPACE_SPOT_TOKEN"
export SPOT_ORGANIZATION="org_z0ELxD9LNTjgYwjc"
```

### Step 3: Get Kubeconfig

```bash
# List available cloudspaces to confirm access
spotctl cloudspace list

# Get kubeconfig for the matchpoint-runners cluster
spotctl cloudspace kubeconfig matchpoint-runners > /tmp/matchpoint-runners-kubeconfig.yaml

# Set KUBECONFIG environment variable
export KUBECONFIG=/tmp/matchpoint-runners-kubeconfig.yaml

# Verify connectivity
kubectl cluster-info
kubectl get nodes
```

**Expected Output:**
```
NAME                                              STATUS   ROLES    AGE   VERSION
matchpoint-runners-pool-abc123-node-xyz456        Ready    <none>   5d    v1.28.x
matchpoint-runners-pool-abc123-node-xyz789        Ready    <none>   5d    v1.28.x
```

## Common Debugging Commands

### Check ARC Runner Pods

```bash
# List all runner pods across namespaces
kubectl get pods -A -l app.kubernetes.io/component=runner

# Check specific namespace (primary runner namespace)
kubectl get pods -n arc-beta-runners-new -l app.kubernetes.io/component=runner

# Get pod details with node placement
kubectl get pods -n arc-beta-runners-new -o wide
```

### Check Runner Scale Sets

```bash
# List AutoscalingRunnerSets
kubectl get autoscalingrunnerset -A

# Describe specific scale set
kubectl get autoscalingrunnerset arc-beta-runners -n arc-beta-runners-new -o yaml

# Check scaling status
kubectl get autoscalingrunnerset -A -o custom-columns=\
NAME:.metadata.name,\
NAMESPACE:.metadata.namespace,\
MIN:.spec.minRunners,\
MAX:.spec.maxRunners,\
CURRENT:.status.currentRunners
```

### Check ARC Controller

```bash
# Check controller pods
kubectl get pods -n arc-systems

# View controller logs
kubectl logs -n arc-systems deployment/arc-gha-rs-controller --tail=100 --follow

# Check for errors in controller
kubectl logs -n arc-systems deployment/arc-gha-rs-controller | grep -i error
```

### Check Runner Logs

```bash
# Get logs from a specific runner pod
kubectl logs -n arc-beta-runners-new <pod-name>

# Follow logs in real-time
kubectl logs -n arc-beta-runners-new <pod-name> -f

# Get logs from all containers in a pod (if using DinD sidecar)
kubectl logs -n arc-beta-runners-new <pod-name> --all-containers

# Get previous container logs (if pod restarted)
kubectl logs -n arc-beta-runners-new <pod-name> --previous
```

### Check Events

```bash
# Get recent events in runner namespace
kubectl get events -n arc-beta-runners-new --sort-by='.lastTimestamp' | tail -20

# Check for scaling events
kubectl get events -n arc-beta-runners-new --field-selector reason=ScalingReplicaSet

# Check for pod errors
kubectl get events -A --field-selector type=Warning
```

### Check Nodes and Resources

```bash
# List nodes with capacity
kubectl get nodes -o wide

# Check node resource usage
kubectl top nodes

# Check pod resource usage
kubectl top pods -n arc-beta-runners-new

# Describe node for detailed info
kubectl describe node <node-name>
```

### Check Secrets and ConfigMaps

```bash
# List secrets in runner namespace
kubectl get secrets -n arc-beta-runners-new

# Check GitHub token secret exists
kubectl get secret arc-beta-runners-gha-rs-github-secret -n arc-beta-runners-new

# List ConfigMaps
kubectl get configmaps -n arc-beta-runners-new
```

### Exec into Runner Pod

```bash
# Get shell in runner pod (for debugging)
kubectl exec -it -n arc-beta-runners-new <pod-name> -- /bin/bash

# Run specific command in runner
kubectl exec -n arc-beta-runners-new <pod-name> -- env | grep RUNNER

# Check Docker availability (if DinD enabled)
kubectl exec -n arc-beta-runners-new <pod-name> -- docker version
```

## Troubleshooting

### spotctl Installation Issues

**Error: `pip: command not found`**
```bash
# Install pip
sudo apt install python3-pip  # Debian/Ubuntu
brew install python3          # macOS
```

**Error: `spotctl: command not found` after install**
```bash
# Check if installed in user site-packages
python3 -m site --user-site

# Add to PATH
export PATH="$HOME/.local/bin:$PATH"

# Or use full path
python3 -m spotctl --version
```

### Authentication Issues

**Error: `Invalid token`**
```bash
# Verify token from GCP Secret Manager is correct
gcloud secrets versions access latest --secret=rackspace-spot-token --project=project-beta-407300

# Re-configure spotctl
spotctl configure set token "$RACKSPACE_SPOT_TOKEN"
```

**Error: `Organization not found`**
```bash
# Verify organization ID
spotctl configure get organization
# Should show: org_z0ELxD9LNTjgYwjc

# Reset if wrong
spotctl configure set organization org_z0ELxD9LNTjgYwjc
```

### Kubeconfig Issues

**Error: `Unable to connect to cluster`**
```bash
# Verify kubeconfig is set correctly
echo $KUBECONFIG
# Should show: /tmp/matchpoint-runners-kubeconfig.yaml

# Test connectivity with verbose output
kubectl cluster-info --v=8

# Check if kubeconfig is valid YAML
cat $KUBECONFIG | kubectl config view --minify
```

**Error: `Token expired`**

Rackspace Spot kubeconfig tokens expire after 3 days. Regenerate:
```bash
# Get fresh kubeconfig
spotctl cloudspace kubeconfig matchpoint-runners > /tmp/matchpoint-runners-kubeconfig.yaml
export KUBECONFIG=/tmp/matchpoint-runners-kubeconfig.yaml
```

**Alternative: Use Terraform-managed kubeconfig**

The terraform state maintains a fresh kubeconfig (auto-refreshed every 2 days):
```bash
# Get GitHub token from gh CLI config
export TF_HTTP_PASSWORD=$(cat ~/.config/gh/hosts.yml | grep oauth_token | awk '{print $2}')

# Navigate to terraform directory
cd /home/pselamy/repositories/matchpoint-github-runners-helm/terraform

# Initialize terraform
terraform init -input=false

# Get kubeconfig from output
terraform output -raw kubeconfig_raw > /tmp/runners-kubeconfig.yaml
export KUBECONFIG=/tmp/runners-kubeconfig.yaml

# Test
kubectl get nodes
```

See the `rackspace-spot-best-practices` skill for more details on kubeconfig token expiration.

### Cluster Not Found

**Error: `Cloudspace not found`**
```bash
# List all cloudspaces in org
spotctl cloudspace list

# Verify cloudspace name matches
# Expected: matchpoint-runners
# Region: us-central-dfw-1

# If using different region, specify explicitly
spotctl configure set region us-central-dfw-1
```

## Quick Reference

### One-Liner Setup

```bash
# Complete setup in one command sequence
export RACKSPACE_SPOT_TOKEN=$(gcloud secrets versions access latest --secret=rackspace-spot-token --project=project-beta-407300) && \
spotctl configure set organization org_z0ELxD9LNTjgYwjc && \
spotctl configure set token "$RACKSPACE_SPOT_TOKEN" && \
spotctl cloudspace kubeconfig matchpoint-runners > /tmp/matchpoint-runners-kubeconfig.yaml && \
export KUBECONFIG=/tmp/matchpoint-runners-kubeconfig.yaml && \
kubectl get nodes
```

### Common Checks After Access

```bash
# Quick health check
kubectl get pods -A -l app.kubernetes.io/component=runner
kubectl get autoscalingrunnerset -A
kubectl logs -n arc-systems deployment/arc-gha-rs-controller --tail=20
kubectl get events -n arc-beta-runners-new --sort-by='.lastTimestamp' | tail -10
```

### Verify Runner Registration with GitHub

```bash
# Check runners registered with GitHub (requires gh CLI)
gh api /orgs/Matchpoint-AI/actions/runners --jq '.runners[] | {name, status, busy, labels: [.labels[].name]}'

# Count online runners
gh api /orgs/Matchpoint-AI/actions/runners --jq '[.runners[] | select(.status=="online")] | length'
```

## Security Best Practices

### Token Management

1. **Never commit tokens to git**
   - Always use GCP Secret Manager
   - Never hardcode in scripts

2. **Use short-lived sessions**
   - Export token in current shell only
   - Don't persist to `~/.bashrc` or `~/.zshrc`

3. **Rotate tokens regularly**
   - Update secret in GCP Secret Manager
   - Invalidate old tokens in Rackspace Spot console

### Kubeconfig Security

1. **Use temporary files**
   ```bash
   # Store in /tmp (cleared on reboot)
   spotctl cloudspace kubeconfig matchpoint-runners > /tmp/kubeconfig.yaml
   ```

2. **Set restrictive permissions**
   ```bash
   chmod 600 /tmp/matchpoint-runners-kubeconfig.yaml
   ```

3. **Clean up after use**
   ```bash
   # When done debugging
   unset KUBECONFIG
   rm /tmp/matchpoint-runners-kubeconfig.yaml
   ```

## Related Skills and Documentation

- **arc-runner-troubleshooting** - Diagnose ARC runner issues
- **rackspace-spot-best-practices** - Best practices for Rackspace Spot (includes kubeconfig token expiration details)
- **arc-terraform-deployment** - Infrastructure deployment

## Related Issues

| Issue/PR | Description |
|----------|-------------|
| #135 | Epic: ARC runner environment limitations |
| #136 | Document troubleshooting learnings in skills |
| #137 | PR: Auto-refresh kubeconfig token workflow |
| #142 | This skill - Rackspace Spot cluster access guide |

## References

- [Rackspace Spot Documentation](https://docs.rackspace.com/spot/)
- [spotctl GitHub Repository](https://github.com/spotinst/spotctl)
- [GCP Secret Manager](https://cloud.google.com/secret-manager/docs)
- [ARC Documentation](https://github.com/actions/actions-runner-controller)

## Validation Checklist

Use this checklist to verify cluster access is working:

- [ ] `spotctl` installed and in PATH
- [ ] GCP authentication successful (`gcloud auth list`)
- [ ] Rackspace Spot token retrieved from Secret Manager
- [ ] `spotctl configure` set with org and token
- [ ] Cloudspace `matchpoint-runners` visible in `spotctl cloudspace list`
- [ ] Kubeconfig retrieved and exported to `$KUBECONFIG`
- [ ] `kubectl get nodes` returns nodes successfully
- [ ] `kubectl get pods -A` returns pods successfully
- [ ] ARC controller pods running in `arc-systems` namespace
- [ ] Runner pods visible in `arc-beta-runners-new` namespace
