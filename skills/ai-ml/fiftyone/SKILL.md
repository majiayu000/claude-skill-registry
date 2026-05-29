---
name: fiftyone
description: |
  FiftyOne dataset visualization and curation tool via Podman Quadlet.
  Multi-container architecture with MongoDB sidecar for dataset persistence.
  GPU-accelerated for ML workflows. Use when users need to configure, start,
  or manage FiftyOne for dataset analysis.
---

# FiftyOne - Dataset Visualization & Curation

## Overview

The `fiftyone` command manages FiftyOne dataset visualization using Podman Quadlet containers. It includes a MongoDB sidecar for persistent dataset storage.

**Key Concept:** FiftyOne runs as a multi-container application with a MongoDB sidecar. The main FiftyOne container handles the web UI and processing, while MongoDB stores dataset metadata.

## Quick Reference

| Action | Command | Description |
|--------|---------|-------------|
| Config | `ujust fiftyone config [--port=...] [--bind=...]` | Configure instance |
| Start | `ujust fiftyone start [--instance=N\|all]` | Start FiftyOne + MongoDB |
| Stop | `ujust fiftyone stop [--instance=N\|all]` | Stop FiftyOne + MongoDB |
| Restart | `ujust fiftyone restart [--instance=N\|all]` | Restart all containers |
| Logs | `ujust fiftyone logs [--instance=N] [--lines=...]` | View interleaved logs |
| Status | `ujust fiftyone status [--instance=N]` | Show status (all instances) |
| URL | `ujust fiftyone url [--instance=N]` | Show access URL |
| Shell | `ujust fiftyone shell [--instance=N] [-- CMD...]` | Open shell in container |
| Plugins | `ujust fiftyone plugins [-- CMD...]` | Manage FiftyOne plugins |
| Delete | `ujust fiftyone delete [--instance=N\|all]` | Remove instance(s) and images |

## Parameters

| Parameter | Long Flag | Short | Default | Description |
|-----------|-----------|-------|---------|-------------|
| action | (positional) | - | required | Action: config, start, stop, etc. |
| config_dir | `--config-dir` | `-c` | `~/.config/fiftyone/{N}` | Configuration directory |
| workspace_dir | `--workspace-dir` | `-w` | `""` | Optional mount to /workspace |
| bind | `--bind` | `-b` | `127.0.0.1` | Bind address |
| port | `--port` | `-p` | `5151` | Web UI port |
| image | `--image` | `-i` | `docker.io/voxel51/fiftyone` | Container image |
| tag | `--tag` | `-t` | `latest` | Image tag |
| gpu_type | `--gpu-type` | `-g` | `auto` | GPU type (auto/nvidia/amd/intel/none) |
| lines | `--lines` | `-l` | `50` | Log lines to show |
| instance | `--instance` | `-n` | `1` | Instance number |

## Configuration

```bash
# Default configuration (port 5151, localhost only)
ujust fiftyone config

# Custom port (long form)
ujust fiftyone config --port=5152

# Custom port (short form)
ujust fiftyone config -p 5152

# Network-wide access
ujust fiftyone config --bind=0.0.0.0

# With workspace mount
ujust fiftyone config --workspace-dir=/data/datasets

# Combine parameters (long form)
ujust fiftyone config --port=5152 --bind=0.0.0.0 --workspace-dir=/data

# Combine parameters (short form)
ujust fiftyone config -p 5152 -b 0.0.0.0 -w /data
```

### Update Existing Configuration

Running `config` when already configured will update the existing configuration, preserving values not explicitly changed.

## Lifecycle Commands

### Start/Stop/Restart

```bash
# Start FiftyOne (includes MongoDB sidecar)
ujust fiftyone start

# Start specific instance (long form)
ujust fiftyone start --instance=1

# Start specific instance (short form)
ujust fiftyone start -n 1

# Start all instances
ujust fiftyone start --instance=all

# Stop FiftyOne + MongoDB
ujust fiftyone stop --instance=1

# Restart all containers
ujust fiftyone restart
```

### View Logs

FiftyOne shows interleaved logs from both the main container and MongoDB sidecar:

```bash
# Follow logs (default 50 lines)
ujust fiftyone logs

# More lines (long form)
ujust fiftyone logs --lines=100

# More lines (short form)
ujust fiftyone logs -l 100

# Specific instance
ujust fiftyone logs -n 1 -l 100
```

Log output format:

```
[fiftyone-mongodb] 2024-01-09 10:00:01 MongoDB started
[fiftyone] 2024-01-09 10:00:02 Connecting to database...
[fiftyone] 2024-01-09 10:00:03 FiftyOne App ready on port 5151
```

### Get URL

```bash
ujust fiftyone url
# Output: http://localhost:5151

# Specific instance
ujust fiftyone url --instance=2
```

## Shell Access

```bash
# Interactive shell
ujust fiftyone shell

# Run specific command (use -- separator)
ujust fiftyone shell -- fiftyone --version
ujust fiftyone shell -- pip list

# Specific instance
ujust fiftyone shell --instance=2 -- python -c "import fiftyone as fo; print(fo.__version__)"

# Short form
ujust fiftyone shell -n 2 -- ls -la
```

## Plugin Management

```bash
# List installed plugins
ujust fiftyone plugins -- list

# Install a plugin
ujust fiftyone plugins -- install <plugin-name>

# Update plugins
ujust fiftyone plugins -- update
```

## Multi-Container Architecture

FiftyOne runs with a MongoDB sidecar:

```
+-------------------+        +-------------------+
|    FiftyOne       |        |     MongoDB       |
|   (fiftyone-1)    | -----> | (fiftyone-mongodb-1) |
|   Port 5151       |        |   Port 27017      |
+-------------------+        +-------------------+
         |                            |
         +---- bazzite-ai network ----+
```

**Container Names:**
- `fiftyone-{N}` - Main FiftyOne container
- `fiftyone-mongodb-{N}` - MongoDB sidecar

**Lifecycle:**
- `start` starts MongoDB first, then FiftyOne
- `stop` stops FiftyOne first, then MongoDB
- `logs` shows interleaved output from both

## Port Allocation

| Instance | FiftyOne Port | MongoDB Port |
|----------|---------------|--------------|
| 1 | 5151 | 27017 |
| 2 | 5152 | 27018 |
| N | 5150+N | 27016+N |

## GPU Support

FiftyOne supports GPU acceleration for ML model inference:

```bash
# Auto-detect GPU (default)
ujust fiftyone config

# Explicit NVIDIA (long form)
ujust fiftyone config --gpu-type=nvidia

# Explicit NVIDIA (short form)
ujust fiftyone config -g nvidia
```

## Configuration Files

| File | Purpose | Location |
|------|---------|----------|
| Instance config | Per-instance settings | `~/.config/fiftyone/instance-{N}.env` |
| Quadlet unit (main) | Service definition | `~/.config/containers/systemd/fiftyone-{N}.container` |
| Quadlet unit (MongoDB) | Sidecar definition | `~/.config/containers/systemd/fiftyone-mongodb-{N}.container` |

## Common Workflows

### Initial Setup

```bash
# 1. Configure FiftyOne with dataset directory
ujust fiftyone config --workspace-dir=/data/datasets

# 2. Start FiftyOne
ujust fiftyone start

# 3. Get URL
ujust fiftyone url

# 4. Open in browser
# http://localhost:5151
```

### Dataset Analysis

```bash
# Start FiftyOne
ujust fiftyone start

# Open shell for interactive work
ujust fiftyone shell

# Inside container:
# import fiftyone as fo
# dataset = fo.load_dataset("my_dataset")
# session = fo.launch_app(dataset)
```

### Network Access

```bash
# Configure for network access
ujust fiftyone config --bind=0.0.0.0

# Restart to apply
ujust fiftyone restart

# Access from other machines
# http://<hostname>:5151
```

## Troubleshooting

### FiftyOne Won't Start

**Check:**

```bash
ujust fiftyone status
ujust fiftyone logs --lines=50
```

**Common causes:**

- Port 5151 already in use
- MongoDB failed to start
- GPU driver issues

**Fix:**

```bash
# Delete and reconfigure
ujust fiftyone delete
ujust fiftyone config --port=5152
ujust fiftyone start
```

### MongoDB Connection Failed

**Symptom:** FiftyOne logs show "Connection refused" to MongoDB

**Check:**

```bash
# Check MongoDB container
podman ps | grep fiftyone-mongodb
ujust fiftyone logs | grep mongodb
```

**Fix:**

```bash
# Restart both containers
ujust fiftyone restart
```

### Datasets Not Persisting

**Symptom:** Datasets disappear after restart

**Check:**

- Verify config_dir is properly set
- Check MongoDB volume mounts

**Fix:**

```bash
# Reconfigure with explicit config directory
ujust fiftyone config --config-dir=/data/fiftyone
```

## Cross-References

- **Related Skills:** `jupyter` (ML notebooks), `ollama` (LLM inference)
- **FiftyOne Docs:** <https://docs.voxel51.com/>
- **GPU Setup:** `ujust config gpu setup`

## When to Use This Skill

Use when the user asks about:

- "fiftyone", "dataset visualization", "dataset curation"
- "ML datasets", "computer vision datasets"
- "data labeling", "annotation tool"
- "start fiftyone", "configure fiftyone"
