---
name: comfyui
description: |
  ComfyUI node-based Stable Diffusion interface. GPU-accelerated image
  generation with custom node support and CivitAI model downloads.
  Use 'ujust comfyui' for configuration, lifecycle management, and
  model/node operations.
---

# ComfyUI - Stable Diffusion Interface

## Overview

ComfyUI is a powerful node-based Stable Diffusion interface for AI image generation. The `comfyui` command manages the ComfyUI container, including configuration, lifecycle management, model downloads, and custom node management.

**Key Concept:** This is a **system command** - run with `ujust` from anywhere on the system. ComfyUI runs as a Podman Quadlet service. By default, data is ephemeral (stored inside the container). Configure volume mounts for persistent storage.

## Quick Reference

| Action | Command | Description |
|--------|---------|-------------|
| Config | `ujust comfyui config [--models-dir=...] [--output-dir=...] [--port=...]` | Configure ComfyUI |
| Start | `ujust comfyui start` | Start ComfyUI server |
| Stop | `ujust comfyui stop` | Stop ComfyUI server |
| Restart | `ujust comfyui restart` | Restart ComfyUI server |
| Status | `ujust comfyui status` | Show status and model counts |
| Logs | `ujust comfyui logs [--lines=...]` | View service logs |
| Open | `ujust comfyui open` | Open UI in browser |
| Shell | `ujust comfyui shell [-- CMD...]` | Open shell in container |
| Download model | `ujust comfyui download --model-url=<url> --model-type=<type>` | Download from CivitAI |
| List models | `ujust comfyui models` | List installed models |
| Install node | `ujust comfyui node-install --node-url=<url>` | Install custom node |
| List nodes | `ujust comfyui node-list` | List custom nodes |
| Update nodes | `ujust comfyui node-update` | Update all nodes |
| Delete | `ujust comfyui delete` | Remove ComfyUI and images |

## Configuration

### Parameters

| Parameter | Long Flag | Short | Default | Description |
|-----------|-----------|-------|---------|-------------|
| Port | `--port` | `-p` | `8188` | Web UI port |
| GPU Type | `--gpu-type` | `-g` | `auto` | GPU: nvidia/amd/intel/auto |
| Image | `--image` | `-i` | (default image) | Container image |
| Tag | `--tag` | `-t` | `stable` | Image tag |
| Models Dir | `--models-dir` | - | (empty) | Path for SD models |
| Output Dir | `--output-dir` | - | (empty) | Path for generated images |
| Input Dir | `--input-dir` | - | (empty) | Path for input images |
| Nodes Dir | `--nodes-dir` | - | (empty) | Path for custom nodes |
| Workspace | `--workspace-dir` | `-w` | (empty) | Optional mount to /workspace |
| Bind | `--bind` | `-b` | `127.0.0.1` | Bind address |
| Lines | `--lines` | `-l` | `50` | Log lines to show |
| Instance | `--instance` | `-n` | `1` | Instance number |

**Important:** All directory parameters default to empty. When empty, data is stored inside the container and will be **lost when the container is recreated**. For persistent storage, provide explicit paths.

### Configuration Examples

```bash
# Ephemeral mode - no persistent storage (data lost on container recreation)
ujust comfyui config

# Persist models only (most common)
ujust comfyui config --models-dir=/data/models

# Persist models and output
ujust comfyui config --models-dir=/data/models --output-dir=/data/output

# Persist models and custom_nodes
ujust comfyui config --models-dir=/data/models --nodes-dir=/data/nodes

# All directories with custom port and GPU
ujust comfyui config --models-dir=/data/models --output-dir=/data/output \
  --input-dir=/data/input --nodes-dir=/data/nodes --port=8189 --gpu-type=nvidia

# With short forms
ujust comfyui config -p 8189 -g nvidia --models-dir=/data/models

# Network-wide access
ujust comfyui config --bind=0.0.0.0
```

### Update Existing Configuration

Running `config` when already configured will update the existing configuration, preserving values not explicitly changed:

```bash
# Initially configured with defaults
ujust comfyui config

# Later, add models directory (other settings preserved)
ujust comfyui config --models-dir=/data/models
```

### Shell Access

```bash
# Interactive bash shell
ujust comfyui shell

# Run specific command (use -- separator)
ujust comfyui shell -- pip list
ujust comfyui shell -- nvidia-smi
```

## Model Downloads

### download

```bash
ujust comfyui download --model-url=<URL> --model-type=<TYPE>
```

| Parameter | Flag | Description |
|-----------|------|-------------|
| URL | `--model-url` | CivitAI URL, model ID, or direct download URL |
| Type | `--model-type` | Model type (see below) |

**Requires:** `--models-dir` must be configured (not ephemeral)

**Model Types:**

| Type | Directory | Description |
|------|-----------|-------------|
| `checkpoint` | checkpoints/ | Main SD models |
| `lora` | loras/ | LoRA adapters |
| `vae` | vae/ | VAE models |
| `embedding` | embeddings/ | Textual inversions |
| `controlnet` | controlnet/ | ControlNet models |
| `upscale` | upscale_models/ | Upscaler models |

### Download Examples

```bash
# By CivitAI URL
ujust comfyui download --model-url=https://civitai.com/models/101055 --model-type=checkpoint

# By model ID
ujust comfyui download --model-url=101055 --model-type=checkpoint

# LoRA model
ujust comfyui download --model-url=123456 --model-type=lora

# Direct URL
ujust comfyui download --model-url=https://example.com/model.safetensors --model-type=vae
```

## Custom Nodes

### node-install

```bash
ujust comfyui node-install --node-url=<GIT_URL>
```

**Requires:** `--nodes-dir` must be configured (not ephemeral)

| Parameter | Flag | Description |
|-----------|------|-------------|
| GIT_URL | `--node-url` | Git repository URL for custom node |

### Popular Custom Nodes

```bash
# ComfyUI-Manager (recommended)
ujust comfyui node-install --node-url=https://github.com/ltdrdata/ComfyUI-Manager

# Impact Pack
ujust comfyui node-install --node-url=https://github.com/ltdrdata/ComfyUI-Impact-Pack

# ControlNet Aux
ujust comfyui node-install --node-url=https://github.com/Fannovel16/comfyui_controlnet_aux

# List installed nodes
ujust comfyui node-list

# Update all nodes
ujust comfyui node-update
```

## Data Storage

### Ephemeral Mode (Default)

When no directories are configured, ComfyUI uses internal container directories:

- Data is stored inside the container
- **All data is lost** when container is recreated
- Suitable for testing or temporary use

### Persistent Mode

When directories are configured, they are mounted into the container:

```
/path/to/models/           # Your MODELS_DIR
├── checkpoints/           # Main SD models (.safetensors, .ckpt)
├── loras/                 # LoRA adapters
├── vae/                   # VAE models
├── embeddings/            # Textual inversions
├── controlnet/            # ControlNet models
└── upscale_models/        # Upscaler models

/path/to/output/           # Your OUTPUT_DIR - generated images
/path/to/input/            # Your INPUT_DIR - input images for img2img
/path/to/custom_nodes/     # Your CUSTOM_NODES_DIR - node extensions
```

## Common Workflows

### Initial Setup (Persistent)

```bash
# 1. Configure with persistent models directory
ujust comfyui config --models-dir=/data/comfyui/models

# 2. Download a checkpoint model
ujust comfyui download --model-url=https://civitai.com/models/101055 --model-type=checkpoint

# 3. Start ComfyUI
ujust comfyui start

# 4. Open in browser
ujust comfyui open
```

### Quick Test (Ephemeral)

```bash
# 1. Configure with defaults (ephemeral)
ujust comfyui config

# 2. Start ComfyUI
ujust comfyui start

# 3. Open in browser
ujust comfyui open

# Note: Download models via the UI - they will be lost on container recreation
```

### Daily Usage

```bash
# Start ComfyUI
ujust comfyui start

# Open in browser
ujust comfyui open

# View logs
ujust comfyui logs

# Stop when done
ujust comfyui stop
```

## GPU Support

ComfyUI automatically detects and configures GPU acceleration:

| GPU | Configuration | Performance |
|-----|---------------|-------------|
| **NVIDIA** | CDI device passthrough | Full CUDA acceleration |
| **AMD** | /dev/dri + /dev/kfd | ROCm acceleration |
| **Intel** | /dev/dri | oneAPI acceleration |
| **CPU** | Fallback mode | Very slow (not recommended) |

### NVIDIA Setup

If NVIDIA GPU is not detected:

```bash
# Generate CDI specification
sudo nvidia-ctk cdi generate --output=/etc/cdi/nvidia.yaml

# Reconfigure ComfyUI
ujust comfyui delete
ujust comfyui config /data/models
```

## Troubleshooting

### Model/Node Commands Fail

**Symptom:** "No MODELS_DIR configured" or "No CUSTOM_NODES_DIR configured"

**Cause:** Using ephemeral mode (no directories configured)

**Fix:** Reconfigure with persistent directories:

```bash
# Add models directory
ujust comfyui config --models-dir=/path/to/models

# Or add both models and custom_nodes
ujust comfyui config --models-dir=/path/to/models --nodes-dir=/path/to/nodes
```

### Model Not Appearing

**Symptom:** Downloaded model not visible in ComfyUI

**Fix:**

```bash
# Restart ComfyUI to reload models
ujust comfyui restart

# Verify model is in correct directory
ls /path/to/your/models/checkpoints/
```

### CivitAI Download Fails

**Symptom:** Cannot download from CivitAI

**Cause:** Model requires authentication or is restricted

**Fix:**

```bash
# Download manually and place in appropriate directory
mv ~/Downloads/model.safetensors /path/to/models/checkpoints/
```

### Out of Memory

**Symptom:** CUDA out of memory error

**Fix:** Check logs and consider using smaller models or lower precision:

```bash
ujust comfyui logs
```

### Service Won't Start

**Symptom:** ComfyUI fails to start

**Fix:**

```bash
# Check logs for errors
ujust comfyui logs

# Verify GPU access
nvidia-smi

# Delete and reconfigure
ujust comfyui delete
ujust comfyui config --models-dir=/data/models
```

## Configuration Files

| File | Purpose | Location |
|------|---------|----------|
| Instance config | Settings | `~/.config/comfyui/1.env` |
| Quadlet file | Service definition | `~/.config/containers/systemd/comfyui-1.container` |

## Cross-References

- **Related Skills:** `ollama` (LLM inference), `jupyter` (notebooks)
- **Pod Building:** See `/bazzite-ai-dev:build` skill for developers
- **ComfyUI Docs:** <https://github.com/comfyanonymous/ComfyUI>
- **ComfyUI-Manager:** <https://github.com/ltdrdata/ComfyUI-Manager>
- **CivitAI:** <https://civitai.com/>

## When to Use This Skill

Use when the user asks about:

- "comfyui", "stable diffusion", "image generation"
- "download model", "civitai", "checkpoint", "lora"
- "custom nodes", "comfyui manager"
- "ujust comfyui", "start comfyui", "configure comfyui"
- "gpu image generation", "ai art"
