---
name: jellyfin
description: |
  Jellyfin media server management via Podman Quadlet. Supports multi-instance
  deployment, hardware transcoding (NVIDIA/AMD/Intel), and FUSE filesystem
  mounts. Use when users need to set up or manage Jellyfin media servers.
---

# Jellyfin - Media Server Management

## Overview

The `jellyfin` command manages Jellyfin media server instances using Podman Quadlet containers. It supports hardware transcoding and FUSE filesystem compatibility for network mounts.

**Key Concept:** Multi-instance support allows running multiple media libraries. FUSE compatibility enables rclone/sshfs mounts for cloud or remote storage.

## Quick Reference

| Action | Command | Description |
|--------|---------|-------------|
| Config | `ujust jellyfin config` | Configure Jellyfin |
| Delete | `ujust jellyfin delete` | Remove instance config and container |
| Logs | `ujust jellyfin logs [--lines=N]` | View container logs |
| Restart | `ujust jellyfin restart` | Restart server |
| Shell | `ujust jellyfin shell [-- CMD]` | Open shell or execute command in container |
| Start | `ujust jellyfin start` | Start Jellyfin media server |
| Status | `ujust jellyfin status` | Show instance status |
| Stop | `ujust jellyfin stop` | Stop Jellyfin media server |
| URL | `ujust jellyfin url` | Show web UI access URL |

## Configuration

### Parameters

| Parameter | Long Flag | Short | Required | Description |
|-----------|-----------|-------|----------|-------------|
| Config Dir | `--config-dir` | `-c` | Yes | Configuration directory |
| Cache Dir | `--cache-dir` | - | Yes | Cache directory (transcoding) |
| Media Dir | `--media-dir` | - | Yes | Media library path |
| Instance | `--instance` | `-n` | No | Instance number (default: 1) |
| GPU Type | `--gpu-type` | `-g` | No | GPU: nvidia, amd, intel, auto |
| Image | `--image` | `-i` | No | Container image |
| Tag | `--tag` | `-t` | No | Image tag (default: stable) |
| Workspace | `--workspace-dir` | `-w` | No | Optional mount to /workspace |
| Bind | `--bind` | `-b` | No | Bind address |
| Port | `--port` | `-p` | No | Service port |
| Lines | `--lines` | `-l` | No | Log lines to show |

### Configuration Examples

```bash
# Basic installation (long form)
ujust jellyfin config --config-dir=~/jellyfin/config --cache-dir=~/jellyfin/cache --media-dir=~/media

# With NVIDIA GPU for transcoding
ujust jellyfin config -c ~/jellyfin/config --cache-dir=~/jellyfin/cache --media-dir=~/media --gpu-type=nvidia

# Second instance for different library
ujust jellyfin config -c ~/jellyfin2/config --cache-dir=~/jellyfin2/cache --media-dir=~/videos --instance=2

# With short forms
ujust jellyfin config -c ~/config --cache-dir=~/cache --media-dir=~/media -n 1 -g nvidia
```

### Update Existing Configuration

Running `config` when already configured will update the existing configuration, preserving values not explicitly changed.

### Shell Access

```bash
# Interactive bash shell
ujust jellyfin shell

# Run specific command (use -- separator)
ujust jellyfin shell -- df -h

# Shell in specific instance
ujust jellyfin shell --instance=2 -- ls /media
```

## Lifecycle Commands

### Start/Stop

```bash
# Single instance
ujust jellyfin start --instance=1
ujust jellyfin stop --instance=1

# Short form
ujust jellyfin start -n 1
ujust jellyfin stop -n 1

# All instances
ujust jellyfin start --instance=all
ujust jellyfin stop --instance=all
```

### View Logs

```bash
# Follow logs
ujust jellyfin logs

# Specific instance with line count
ujust jellyfin logs --instance=1 --lines=100

# Short form
ujust jellyfin logs -n 1 -l 100
```

### Get URL

```bash
ujust jellyfin url
# Output: http://localhost:8096

# Specific instance
ujust jellyfin url --instance=2
```

## Port Allocation

| Instance | Port |
|----------|------|
| 1 | 8096 |
| 2 | 8097 |
| 3 | 8098 |
| N | 8095+N |

## Hardware Transcoding

### GPU Types

| GPU | Flag Value | Transcoding |
|-----|------------|-------------|
| NVIDIA | `--gpu-type=nvidia` or `-g nvidia` | NVENC/NVDEC |
| AMD | `--gpu-type=amd` or `-g amd` | VAAPI |
| Intel | `--gpu-type=intel` or `-g intel` | QuickSync |

### Enable GPU

```bash
ujust jellyfin config -c ~/config --cache-dir=~/cache --media-dir=~/media --gpu-type=nvidia
```

### Verify GPU

```bash
# Check inside container
ujust jellyfin shell -- nvidia-smi  # or vainfo for AMD/Intel
```

## FUSE Filesystem Support

Jellyfin containers support FUSE mounts (rclone, sshfs) for remote storage.

### Mount Before Starting

```bash
# Mount cloud storage
rclone mount gdrive:media ~/media --daemon

# Then start Jellyfin
ujust jellyfin start 1
```

### Why Host Networking?

Jellyfin uses host networking for:

- DLNA discovery
- mDNS/Bonjour
- Chromecast

## Configuration Files

| File | Purpose | Location |
|------|---------|----------|
| Quadlet unit | Service definition | `~/.config/containers/systemd/jellyfin-1.container` |
| Instance config | Settings | `~/.config/jellyfin/instance-1.env` |
| Jellyfin data | Libraries, users | `<CONFIG>/` |
| Transcoding cache | Temp files | `<CACHE>/` |

## Common Workflows

### Initial Setup

```bash
# 1. Create directories
mkdir -p ~/jellyfin/{config,cache}

# 2. Configure Jellyfin
ujust jellyfin config -c ~/jellyfin/config --cache-dir=~/jellyfin/cache --media-dir=~/media --gpu-type=nvidia

# 3. Start it
ujust jellyfin start

# 4. Access web UI
ujust jellyfin url
# Open http://localhost:8096
```

### Multiple Libraries

```bash
# Movies library
ujust jellyfin config -c ~/jellyfin-movies/config --cache-dir=~/jellyfin-movies/cache --media-dir=~/movies -n 1

# TV library
ujust jellyfin config -c ~/jellyfin-tv/config --cache-dir=~/jellyfin-tv/cache --media-dir=~/tv -n 2

# Start both
ujust jellyfin start --instance=all
```

### Cloud Storage

```bash
# 1. Mount cloud storage
rclone mount gdrive:media ~/cloud-media --daemon --vfs-cache-mode writes

# 2. Configure Jellyfin pointing to mount
ujust jellyfin config -c ~/jellyfin/config --cache-dir=~/jellyfin/cache --media-dir=~/cloud-media

# 3. Start
ujust jellyfin start
```

## Initial Configuration

First-time setup via web UI:

1. Open `http://localhost:8096`
2. Create admin user
3. Add media libraries
4. Configure transcoding (if GPU)
5. Set up remote access

## Troubleshooting

### Jellyfin Won't Start

**Check:**

```bash
ujust jellyfin status
ujust jellyfin logs --lines=50
```

**Common causes:**

- Port conflict (8096 in use)
- Invalid paths
- GPU driver issues

### Transcoding Fails

**Check:**

```bash
# View logs for transcoding errors
ujust jellyfin logs | grep -i transcode
```

**Common causes:**

- GPU not passed through
- Missing codec support

**Fix:**

```bash
# Reconfigure with GPU
ujust jellyfin delete
ujust jellyfin config -c ~/config --cache-dir=~/cache --media-dir=~/media --gpu-type=nvidia
```

### Media Not Found

**Check:**

- Media directory exists
- Correct path in config
- Permissions

**Fix:**

```bash
# Verify path
ls ~/media

# Reconfigure with correct path
ujust jellyfin delete
ujust jellyfin config -c ~/config --cache-dir=~/cache --media-dir=/correct/path
```

### DLNA Not Working

**Cause:** Network isolation

Jellyfin uses host networking, but ensure:

- Firewall allows mDNS (5353/udp)
- Same network as clients

## Cross-References

- **Related Skills:** `configure gpu` (GPU setup)
- **Jellyfin Docs:** <https://jellyfin.org/docs/>
- **Web UI:** [http://localhost:8096](http://localhost:8096)

## When to Use This Skill

Use when the user asks about:

- "install jellyfin", "setup media server"
- "jellyfin not working", "jellyfin transcoding"
- "jellyfin GPU", "hardware transcoding"
- "multiple jellyfin", "jellyfin instances"
