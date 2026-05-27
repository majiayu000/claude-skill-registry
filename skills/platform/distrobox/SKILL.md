---
name: distrobox
description: |
  Distrobox container management for Bazzite. Create containers from manifests,
  custom containers, app-specific containers (brew), and DaVinci Resolve installation.
  Use when users need to work with distrobox containers.
---

# Distrobox - Container Management

## Overview

Distrobox lets you run any Linux distribution inside containers with seamless host integration. This skill covers creating and managing distrobox containers on Bazzite.

## Quick Reference

| Command | Description |
|---------|-------------|
| `ujust distrobox-assemble` | Create containers from distrobox.ini |
| `ujust assemble` | Alias for distrobox-assemble |
| `ujust distrobox-new` | Create custom distrobox container |
| `ujust distrobox` | Alias for distrobox-new |
| `ujust setup-distrobox-app` | Install app containers (brew) |
| `ujust install-resolve` | Install DaVinci Resolve |
| `ujust install-davinci` | Alias for install-resolve |
| `ujust install-davinci-resolve` | Alias for install-resolve |
| `ujust install-resolve-studio` | Install DaVinci Resolve Studio |

## Container Creation

### From Manifest

```bash
# Create containers defined in distrobox.ini
ujust distrobox-assemble
```

Reads `~/.config/distrobox/distrobox.ini` and creates all defined containers.

**Example distrobox.ini:**

```ini
[ubuntu]
image=ubuntu:22.04
pull=true
init=true

[fedora]
image=fedora:39
pull=true
```

### Custom Container

```bash
# Interactive container creation
ujust distrobox-new
```

Prompts for:
- Container name
- Base image
- Additional options

### Manual Creation

```bash
# Direct distrobox command
distrobox create --name mybox --image ubuntu:22.04
distrobox enter mybox
```

## App Containers

### Homebrew Container

```bash
# Setup brew in a container
ujust setup-distrobox-app brew
```

Creates a dedicated container with Homebrew installed.

**Usage after setup:**

```bash
distrobox enter brew
brew install <package>
```

## DaVinci Resolve

### Free Version

```bash
# Install DaVinci Resolve in container
ujust install-resolve

# Aliases
ujust install-davinci
ujust install-davinci-resolve
```

### Studio Version

```bash
# Install DaVinci Resolve Studio
ujust install-resolve-studio
```

Requires license/dongle for Studio features.

**Process:**
1. Downloads Resolve installer
2. Creates Fedora-based container
3. Installs dependencies
4. Installs Resolve
5. Creates desktop entry

## Common Workflows

### Development Environment

```bash
# Create Ubuntu dev container
distrobox create --name dev --image ubuntu:22.04
distrobox enter dev

# Inside container
sudo apt update
sudo apt install build-essential python3-pip
```

### Multiple Distros

```bash
# Create distrobox.ini
cat > ~/.config/distrobox/distrobox.ini << EOF
[arch]
image=archlinux:latest
pull=true

[debian]
image=debian:bookworm
pull=true
EOF

# Create all containers
ujust distrobox-assemble
```

### Video Editing Setup

```bash
# Install DaVinci Resolve
ujust install-resolve

# Launch from applications menu or:
distrobox enter resolve
resolve
```

## Container Management

### List Containers

```bash
distrobox list
```

### Enter Container

```bash
distrobox enter <name>
```

### Stop Container

```bash
distrobox stop <name>
```

### Remove Container

```bash
distrobox rm <name>
```

### Export Application

```bash
# Export app to host
distrobox enter <name>
distrobox-export --app <application>
```

## Troubleshooting

### Container Won't Start

**Check:**

```bash
# Container status
podman ps -a

# Logs
podman logs <container-id>
```

**Fix:**

```bash
# Recreate container
distrobox rm <name>
distrobox create --name <name> --image <image>
```

### Resolve Won't Launch

**Check NVIDIA drivers:**

```bash
nvidia-smi
```

**Check GPU access in container:**

```bash
distrobox enter resolve
nvidia-smi
```

### GUI Apps Not Working

**Verify Wayland/X11:**

```bash
echo $XDG_SESSION_TYPE
echo $DISPLAY
```

**Try X11 forwarding:**

```bash
distrobox create --name <name> --image <image> --additional-flags "--env DISPLAY=$DISPLAY"
```

## Cross-References

- **bazzite:gpu** - GPU driver configuration
- **bazzite-ai:configure** - Docker/Podman configuration
- **bazzite:apps** - Third-party application installation

## When to Use This Skill

Use when the user asks about:
- "distrobox", "create container", "linux container"
- "ubuntu on bazzite", "arch container", "debian box"
- "distrobox.ini", "assemble containers", "manifest"
- "brew on bazzite", "homebrew", "brew container"
- "DaVinci Resolve", "video editing", "Resolve Studio"
- "run other distro", "different distribution"
