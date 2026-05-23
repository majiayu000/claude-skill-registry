---
name: bootc
description: |
  bootc VM management via bcvk (bootc virtualization kit). Run bootable
  containers as VMs for testing. Supports ephemeral (quick test) and
  persistent modes. Use when users need to test bootable container images
  as virtual machines.
---

# Bootc - bootc-based VM Management

## Overview

The `bootc` command manages bootable container VMs using bcvk (bootc virtualization kit). It converts OCI container images into bootable VMs for testing.

**Key Concept:** Unlike traditional VMs, bootc VMs are created directly from container images. This enables testing bootable containers without building disk images first.

## Quick Reference

| Action | Command | Description |
|--------|---------|-------------|
| Add | `ujust bootc add [NAME]` | Create persistent VM with disk |
| Delete | `ujust bootc delete [NAME]` | Delete VM and its disk |
| Export | `ujust bootc export [IMAGE] [FORMAT]` | Export container as qcow2/raw image |
| Images | `ujust bootc images` | List available bootc images |
| List | `ujust bootc list` | List all bootc VMs |
| Prereqs | `ujust bootc prereqs` | Verify bcvk and dependencies installed |
| SSH | `ujust bootc ssh [NAME]` | SSH connection to VM |
| Start | `ujust bootc start [NAME]` | Start persistent VM |
| Status | `ujust bootc status [NAME]` | Show VM status and info |
| Stop | `ujust bootc stop [NAME]` | Stop running VM |

## Prerequisites

```bash
# Install bcvk
ujust install bcvk

# Verify installation
bcvk --version
```

## Parameters

| Parameter | Long Flag | Short | Default | Description |
|-----------|-----------|-------|---------|-------------|
| action | (positional) | - | required | Action: add, list, status, ssh, etc. |
| vm_name | (positional) | - | `bazzite-bootc` | VM name |
| image | `--image` | `-i` | (varies) | Container image to boot |
| cpus | `--cpus` | - | `2` | Number of CPUs |
| ram | `--ram` | - | `4096` | Memory in MB |
| disk_size | `--disk-size` | - | `20G` | Disk size |
| format | `--format` | `-f` | `qcow2` | Export format (qcow2, raw) |
| ssh_port | `--ssh-port` | - | `2222` | SSH port |
| ssh_user | `--ssh-user` | - | `root` | SSH user |

## Ephemeral Testing

Quick test that auto-deletes VM on exit:

```bash
# Test default bazzite-ai image
ujust test bootc

# Test specific image (long form)
ujust test bootc --image=ghcr.io/org/image:tag

# Test specific image (short form)
ujust test bootc -i ghcr.io/org/image:tag

# Test with more resources
ujust test bootc --image=myimage --cpus=4 --ram=8192

# Short form
ujust test bootc -i myimage --cpus=4 --ram=8192
```

Ephemeral mode:

- Creates temporary VM
- Boots to console
- VM deleted when console exits

## Persistent VMs

Create VMs that persist across sessions:

```bash
# Create VM with default image
ujust bootc add dev

# Create with specific image (long form)
ujust bootc add testing --image=ghcr.io/org/image:testing

# Create with specific image (short form)
ujust bootc add testing -i ghcr.io/org/image:testing

# Custom resources
ujust bootc add heavy --cpus=8 --ram=16384 --disk-size=100G
```

### Manage Persistent VMs

```bash
# Start VM
ujust bootc start dev

# Stop VM
ujust bootc stop dev

# Delete VM
ujust bootc delete dev
```

## Connecting to VMs

### SSH Connection

```bash
# Connect to VM
ujust bootc ssh dev

# Run command (use -- separator)
ujust bootc ssh dev -- systemctl status

# Different user
ujust bootc ssh dev --ssh-user=admin
```

Default: `ssh -p 2222 root@localhost`

### List VMs

```bash
ujust bootc list
```

Output:

```
NAME         STATE    IMAGE
dev          running  ghcr.io/org/image:latest
testing      stopped  ghcr.io/org/image:testing
```

### Check Status

```bash
ujust bootc status dev
```

## Export Disk Images

Convert bootable container to disk image:

```bash
# Export to QCOW2 (long form)
ujust bootc export --image=ghcr.io/org/image:tag

# Export to QCOW2 (short form)
ujust bootc export -i ghcr.io/org/image:tag

# Export to raw (long form)
ujust bootc export --image=ghcr.io/org/image:tag --format=raw

# Export to raw (short form)
ujust bootc export -i ghcr.io/org/image:tag -f raw
```

Supported formats:

- `qcow2` - QEMU disk image
- `raw` - Raw disk image

## Common Workflows

### Quick Test New Image

```bash
# Test ephemeral (no cleanup needed)
ujust test bootc --image=ghcr.io/myorg/myimage:dev
# Exit console to destroy VM

# Short form
ujust test bootc -i ghcr.io/myorg/myimage:dev
```

### Development Environment

```bash
# Create persistent VM (long form)
ujust bootc add dev --image=ghcr.io/myorg/myimage:latest

# Or short form
ujust bootc add dev -i ghcr.io/myorg/myimage:latest

# Start it
ujust bootc start dev

# SSH in
ujust bootc ssh dev

# Make changes, test...

# Stop when done
ujust bootc stop dev
```

### Test Before Release

```bash
# Test testing branch
ujust test bootc --image=ghcr.io/myorg/myimage:testing

# If good, test stable
ujust test bootc --image=ghcr.io/myorg/myimage:stable
```

### Create Installation Media

```bash
# Export to QCOW2 for cloud (long form)
ujust bootc export --image=ghcr.io/myorg/myimage:stable --format=qcow2

# Export to QCOW2 for cloud (short form)
ujust bootc export -i ghcr.io/myorg/myimage:stable -f qcow2

# Export to raw for disk imaging
ujust bootc export -i ghcr.io/myorg/myimage:stable -f raw
```

## bcvk vs vm Command

| Feature | `ujust bootc` (bcvk) | `ujust vm` (libvirt) |
|---------|----------------------|----------------------|
| Image source | Container images | QCOW2 files |
| Ephemeral mode | Yes | No |
| Export formats | qcow2/raw | N/A |
| SSH port | 2222 (fixed) | 4444 (configurable) |
| Home sharing | No | Yes (virtiofs) |
| Boot time | Faster | Slower |
| Use case | Testing containers | Full VMs |

**Use `bootc` when:**

- Testing bootable container images
- Quick ephemeral tests
- Building disk images from containers

**Use `vm` when:**

- Need persistent VMs with home sharing
- Need configurable ports
- Need full libvirt features

## Troubleshooting

### bcvk Not Found

**Fix:**

```bash
ujust install bcvk
```

### VM Won't Start

**Check:**

```bash
ujust bootc status dev
ujust bootc list
```

**Common causes:**

- Image not pulled
- Resource conflict
- Disk full

**Fix:**

```bash
ujust bootc delete dev
ujust bootc add dev
```

### SSH Connection Failed

**Check:**

```bash
ssh -p 2222 root@localhost
```

**Common causes:**

- VM still booting
- Port conflict (2222 used)
- SSH not started

**Fix:**

```bash
# Wait for boot
sleep 30
ujust bootc ssh dev

# Or check console
ujust test bootc  # Watch boot process
```

### Image Pull Failed

**Check:**

```bash
podman pull ghcr.io/org/image:tag
```

**Common causes:**

- Network issue
- Auth required
- Image doesn't exist

**Fix:**

```bash
# Login to registry
podman login ghcr.io

# Pull manually
podman pull ghcr.io/org/image:tag

# Retry
ujust bootc add dev --image=ghcr.io/org/image:tag
```

## Cross-References

- **Related Skills:** `vm` (traditional VMs), `install` (bcvk installation)
- **Installation:** `ujust install bcvk`
- **bcvk Docs:** <https://github.com/containers/bcvk>

## When to Use This Skill

Use when the user asks about:

- "bootc VM", "bootable container", "test container as VM"
- "bcvk", "bootc virtualization"
- "ephemeral VM", "quick test VM"
- "export to qcow2", "create ISO from container"
