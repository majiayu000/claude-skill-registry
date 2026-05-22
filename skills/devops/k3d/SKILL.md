---
name: k3d
description: |
  k3d Kubernetes cluster management - lightweight k3s clusters running in Podman
  containers on the bazzite-ai network. Supports GPU passthrough, multi-instance,
  and service discovery with other bazzite-ai pods. Use when users need to run
  Kubernetes workloads or deploy k8s-based applications locally.
---

# k3d - Kubernetes Clusters

## Overview

The `k3d` command manages lightweight Kubernetes (k3s) clusters running in Podman containers. Clusters are joined to the bazzite-ai network, enabling DNS-based service discovery with other pods (ollama, jupyter, etc.).

**Key Concept:** k3d wraps k3s (lightweight Kubernetes) in containers, providing fast cluster creation with full Kubernetes API compatibility. GPU passthrough is supported via NVIDIA device plugin.

## Quick Reference

| Action | Command | Description |
|--------|---------|-------------|
| Config | `ujust k3d config [--port=...] [--agents=...]` | Create k3d cluster on bazzite-ai network |
| Start | `ujust k3d start [--instance=N]` | Start k3d cluster |
| Stop | `ujust k3d stop [--instance=N]` | Stop k3d cluster |
| Restart | `ujust k3d restart [--instance=N]` | Restart k3d cluster |
| Logs | `ujust k3d logs [--instance=N] [--lines=N]` | View k3s server logs |
| Status | `ujust k3d status [--instance=N]` | Show cluster status and nodes |
| Shell | `ujust k3d shell [--instance=N] [-- CMD]` | Execute kubectl commands |
| GPU | `ujust k3d gpu [--instance=N]` | Setup GPU support (NVIDIA device plugin) |
| Kubeconfig | `ujust k3d kubeconfig [--instance=N]` | Show kubeconfig path |
| List | `ujust k3d list` | List all k3d clusters |
| Delete | `ujust k3d delete [--instance=N]` | Remove k3d cluster and cleanup |

## Parameters

| Parameter | Long Flag | Short | Default | Description |
|-----------|-----------|-------|---------|-------------|
| action | (positional) | - | required | Action: config, start, stop, etc. |
| port | `--port` | `-p` | `6443` | Kubernetes API port |
| bind | `--bind` | `-b` | `127.0.0.1` | Bind address for API server |
| agents | `--agents` | `-a` | `0` | Number of agent (worker) nodes |
| instance | `--instance` | `-n` | `1` | Cluster instance number |
| gpu_type | `--gpu-type` | `-g` | `auto` | GPU type (auto/nvidia/amd/intel/none) |
| lines | `--lines` | `-l` | `50` | Log lines to show |
| http_port | `--http-port` | - | `80` | Traefik HTTP ingress port |
| https_port | `--https-port` | - | `443` | Traefik HTTPS ingress port |
| k3s_version | `--k3s-version` | - | (latest) | Specific k3s version |
| disable_traefik | `--disable-traefik` | - | `false` | Disable built-in Traefik ingress |
| disable_servicelb | `--disable-servicelb` | - | `false` | Disable built-in ServiceLB (Klipper) |

## Configuration

```bash
# Default: Single-node cluster, port 6443, auto-detect GPU
ujust k3d config

# Custom API port (long form)
ujust k3d config --port=6444

# Custom API port (short form)
ujust k3d config -p 6444

# Add 2 agent (worker) nodes
ujust k3d config --agents=2

# With GPU support (NVIDIA)
ujust k3d config --gpu-type=nvidia

# Combine parameters (short form)
ujust k3d config -p 6444 -a 2 -g nvidia

# Network-wide API access
ujust k3d config --bind=0.0.0.0

# Custom ingress ports
ujust k3d config --http-port=8080 --https-port=8443

# Disable built-in components
ujust k3d config --disable-traefik --disable-servicelb

# Specific k3s version
ujust k3d config --k3s-version=v1.28.5+k3s1
```

### Update Existing Configuration

Running `config` when already configured will recreate the cluster with new settings. Data is not preserved - export important resources first.

## Lifecycle Commands

### Start/Stop/Restart

```bash
# Start cluster (instance 1 default)
ujust k3d start

# Start specific instance (long form)
ujust k3d start --instance=1

# Start specific instance (short form)
ujust k3d start -n 1

# Stop cluster
ujust k3d stop

# Restart cluster
ujust k3d restart
```

### View Logs

```bash
# View k3s server logs (default 50 lines)
ujust k3d logs

# More lines (long form)
ujust k3d logs --lines=100

# More lines (short form)
ujust k3d logs -l 100

# Specific instance
ujust k3d logs -n 2 -l 100
```

### Status

```bash
# Show cluster status and node list
ujust k3d status

# List all clusters
ujust k3d list
```

## Shell Access (kubectl)

Execute kubectl commands directly in the cluster context:

```bash
# Interactive shell with kubectl available
ujust k3d shell

# Run kubectl commands (use -- separator)
ujust k3d shell -- kubectl get nodes
ujust k3d shell -- kubectl get pods -A
ujust k3d shell -- kubectl apply -f deployment.yaml

# Specific instance
ujust k3d shell -n 2 -- kubectl get services
```

## GPU Support

k3d supports GPU passthrough for NVIDIA GPUs via the NVIDIA device plugin.

### Setup GPU

```bash
# Install NVIDIA device plugin in cluster
ujust k3d gpu

# Specific instance
ujust k3d gpu --instance=2
```

### Verify GPU Access

```bash
# Check device plugin is running
ujust k3d shell -- kubectl get pods -n kube-system | grep nvidia

# Run GPU test pod
ujust k3d shell -- kubectl run gpu-test --image=nvidia/cuda:12.0-base \
  --restart=Never --rm -it --command -- nvidia-smi
```

### GPU Pod Example

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: gpu-pod
spec:
  containers:
  - name: cuda-container
    image: nvidia/cuda:12.0-base
    resources:
      limits:
        nvidia.com/gpu: 1
```

## bazzite-ai Network Integration

k3d clusters join the `bazzite-ai` network, enabling service discovery:

```bash
# From inside k8s pods, access other bazzite-ai services:
curl http://ollama:11434/api/tags
curl http://jupyter:8888/
```

**Available DNS names:**
- `ollama:11434` - Ollama API
- `jupyter:8888` - JupyterLab
- `openwebui:3000` - Open WebUI
- `comfyui:8188` - ComfyUI

## Multi-Instance

Run multiple k3d clusters simultaneously:

```bash
# Create first cluster
ujust k3d config -n 1 -p 6443

# Create second cluster with different port
ujust k3d config -n 2 -p 6444

# List all clusters
ujust k3d list

# Interact with specific cluster
ujust k3d shell -n 2 -- kubectl get nodes
```

| Instance | API Port | Cluster Name |
|----------|----------|--------------|
| 1 | 6443 | k3d-1 |
| 2 | 6444 | k3d-2 |
| N | 6442+N | k3d-N |

## Built-in Components

k3d includes these components by default:

| Component | Purpose | Disable Flag |
|-----------|---------|--------------|
| **Traefik** | Ingress controller | `--disable-traefik` |
| **ServiceLB (Klipper)** | LoadBalancer support | `--disable-servicelb` |
| **Local Path Provisioner** | Persistent volumes | (always enabled) |
| **CoreDNS** | Cluster DNS | (always enabled) |

## Common Workflows

### Initial Setup

```bash
# 1. Create cluster
ujust k3d config

# 2. Start cluster
ujust k3d start

# 3. Verify nodes
ujust k3d shell -- kubectl get nodes

# 4. Deploy application
ujust k3d shell -- kubectl apply -f my-app.yaml
```

### GPU ML Workloads

```bash
# 1. Create cluster with GPU
ujust k3d config --gpu-type=nvidia

# 2. Start and setup GPU support
ujust k3d start
ujust k3d gpu

# 3. Deploy GPU workload
ujust k3d shell -- kubectl apply -f gpu-deployment.yaml
```

### Development Cluster

```bash
# Fast local cluster for testing
ujust k3d config -a 1  # 1 server + 1 agent

# Deploy test app
ujust k3d shell -- kubectl create deployment nginx --image=nginx
ujust k3d shell -- kubectl expose deployment nginx --port=80 --type=LoadBalancer

# Access via traefik
curl http://localhost
```

## Troubleshooting

### Cluster Won't Start

**Check:**

```bash
ujust k3d status
ujust k3d logs --lines=100
```

**Common causes:**

- Port already in use
- Podman not running
- Insufficient resources

**Fix:**

```bash
# Use different port
ujust k3d delete
ujust k3d config --port=6444
ujust k3d start
```

### GPU Not Available in Pods

**Symptom:** Pods requesting GPU resources stay Pending

**Check:**

```bash
ujust k3d shell -- kubectl describe pod <pod-name>
ujust k3d shell -- kubectl get pods -n kube-system | grep nvidia
```

**Fix:**

```bash
# Reinstall device plugin
ujust k3d gpu

# Or recreate cluster with GPU
ujust k3d delete
ujust k3d config --gpu-type=nvidia
ujust k3d start
ujust k3d gpu
```

### Service Discovery Fails

**Symptom:** Can't reach ollama:11434 from k8s pods

**Check:**

```bash
# Verify network membership
podman network inspect bazzite-ai
```

**Fix:**

```bash
# Recreate cluster (joins network)
ujust k3d delete
ujust k3d config
ujust k3d start
```

### kubectl Connection Refused

**Symptom:** kubectl commands fail with "connection refused"

**Check:**

```bash
ujust k3d status
```

**Fix:**

```bash
# Restart cluster
ujust k3d restart
```

## Configuration Files

| File | Purpose | Location |
|------|---------|----------|
| kubeconfig | kubectl config | `~/.kube/config` (merged) |
| k3d config | Cluster settings | Managed by k3d |

## Cross-References

- **Related Skills:** `portainer` (container UI), `ollama` (LLM inference)
- **k3d Docs:** <https://k3d.io/>
- **k3s Docs:** <https://docs.k3s.io/>
- **GPU Setup:** `ujust config gpu setup`

## When to Use This Skill

Use when the user asks about:

- "kubernetes", "k8s", "k3d", "k3s"
- "local kubernetes", "dev cluster"
- "kubectl", "deploy to kubernetes"
- "kubernetes GPU", "GPU pods"
- "start k3d", "configure k3d", "k3d not working"
