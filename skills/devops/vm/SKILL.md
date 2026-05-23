---
name: vm
description: |
  QCOW2 virtual machine management using libvirt. Creates VMs from pre-built
  images downloaded from R2 CDN with cloud-init customization. Supports SSH,
  VNC, and virtiofs home directory sharing. Use when users need to create,
  manage, or connect to bazzite-ai VMs.
---

# VM - QCOW2 Virtual Machine Management

## Overview

The `vm` command manages bazzite-ai virtual machines using libvirt. VMs are created from pre-built QCOW2 images downloaded from R2 CDN, customized via cloud-init.

**Key Concept:** VMs run in user session (qemu:///session), not requiring root. Home directory is shared via virtiofs at `/workspace` in the VM.

## Quick Reference

| Action | Command | Description |
|--------|---------|-------------|
| Add | `ujust vm add [NAME]` | Add new VM with default image |
| Boot-log | `ujust vm boot-log [NAME]` | Get boot messages via guest agent |
| Create | `ujust vm create [NAME]` | Create VM from existing disk |
| Delete | `ujust vm delete [NAME]` | Delete VM and optionally its disk |
| Diag | `ujust vm diag [NAME]` | Full diagnostic (no SSH required) |
| Download | `ujust vm download [BRANCH]` | Download QCOW2 image |
| Exec | `ujust vm exec [NAME] CMD` | Execute command via guest-agent |
| Recreate | `ujust vm recreate [NAME]` | Recreate VM config preserving disk |
| Seed | `ujust vm seed [NAME]` | Regenerate cloud-init seed ISO |
| Serial | `ujust vm serial [NAME]` | Serial console connection |
| Shell-exec | `ujust vm shell-exec [NAME] CMD` | Execute shell command via guest agent |
| SSH | `ujust vm ssh [NAME]` | SSH connection to VM |
| Start | `ujust vm start [NAME]` | Start VM |
| Status | `ujust vm status [NAME]` | Show VM status |
| Stop | `ujust vm stop [NAME]` | Stop VM |
| Update | `ujust vm update [NAME] WHAT` | Update QCOW2 or seed |
| VNC | `ujust vm vnc [NAME]` | VNC graphical connection |
| Wait-agent | `ujust vm wait-agent [NAME]` | Wait for guest agent to be ready |

## Parameters

| Parameter | Long Flag | Short | Default | Description |
|-----------|-----------|-------|---------|-------------|
| action | (positional) | - | required | Action: add, update, delete, download, etc. |
| vm_name | (positional) | - | `bazzite-ai` | VM name |
| url | `--url` | - | R2 CDN URL | QCOW2 image URL |
| cpus | `--cpus` | - | `4` | Number of CPUs |
| ram | `--ram` | - | `8192` | Memory in MB |
| disk_size | `--disk-size` | - | `100G` | Disk size |
| username | `--username` | `-u` | `$USER` | VM username |
| password | `--password` | - | (empty) | VM password |
| autologin | `--autologin` | - | `true` | Enable autologin |
| ssh_port | `--ssh-port` | - | `4444` | SSH port forwarding |
| vnc_port | `--vnc-port` | - | `5900` | VNC port |
| ssh_user | `--ssh-user` | - | `$USER` | SSH user for connection |
| share_dir | `--share-dir` | - | `$HOME` | Directory to share |
| branch | `--branch` | `-b` | `stable` | Image branch (stable/testing) |
| what | `--what` | - | - | Update target (for update action) |

## Add VM (Full Workflow)

```bash
# Default: bazzite-ai VM with auto-detect settings
ujust vm add

# Named VM with custom config (long form)
ujust vm add myvm --cpus=8 --ram=16384 --disk-size=200G

# Testing branch image
ujust vm add testing-vm --branch=testing

# Short form for branch
ujust vm add testing-vm -b testing

# Different SSH port
ujust vm add dev-vm --ssh-port=4445

# No home sharing
ujust vm add isolated --share-dir=''
```

The `add` command:

1. Downloads QCOW2 image (cached)
2. Creates cloud-init seed ISO
3. Creates libvirt VM
4. Configures port forwarding

## Individual Steps

### Download QCOW2

```bash
# Stable image (default)
ujust vm download

# Testing branch (long form)
ujust vm download --branch=testing

# Testing branch (short form)
ujust vm download -b testing

# Custom URL
ujust vm download --url=https://example.com/custom.qcow2
```

### Create Seed ISO

```bash
# Long form
ujust vm seed myvm --username=developer --password=secret

# Short form for username
ujust vm seed myvm -u developer --password=secret
```

### Create VM

```bash
ujust vm create myvm --cpus=4 --ram=8192
```

## VM Lifecycle

### Start VM

```bash
ujust vm start              # Default VM
ujust vm start myvm         # Named VM
```

Auto-adds VM if it doesn't exist.

### Stop VM

```bash
ujust vm stop              # Graceful shutdown
ujust vm stop myvm         # Named VM
```

### Delete VM

```bash
ujust vm delete myvm        # Remove VM and disk
```

## Connecting to VM

### SSH Connection

```bash
# Connect to default VM
ujust vm ssh

# Named VM
ujust vm ssh myvm

# Different user
ujust vm ssh myvm --ssh-user=root

# Run command (use -- separator)
ujust vm ssh myvm -- ls -la
```

Default SSH: `ssh -p 4444 localhost`

### VNC Connection

```bash
ujust vm vnc              # Opens VNC viewer
ujust vm vnc myvm
```

Default VNC: Port 5900

## Home Directory Sharing

By default, your home directory is shared to the VM at `/workspace` via virtiofs.

```bash
# Default: $HOME -> /workspace
ujust vm add

# Disable sharing
ujust vm add isolated --share-dir=''

# Share specific directory
ujust vm add project --share-dir=/path/to/project
```

Inside VM:

```bash
ls /workspace  # Your home directory
```

## Image Branches

| Branch | Tag | Description |
|--------|-----|-------------|
| `stable` | `:stable` | Production, tested |
| `testing` | `:testing` | Latest features |

```bash
# Long form
ujust vm download --branch=stable
ujust vm download --branch=testing

# Short form
ujust vm download -b stable
ujust vm download -b testing
```

## Storage Locations

| Item | Location |
|------|----------|
| Download cache | `~/.local/share/bazzite-ai/vm/cache/` |
| VM disks | `~/.local/share/libvirt/images/` |
| VM config | `~/.local/share/bazzite-ai/vm/<name>.conf` |
| Seed ISO | `~/.local/share/bazzite-ai/vm/<name>-seed.iso` |

## Common Workflows

### Quick Test VM

```bash
# Add and start default VM
ujust vm add
ujust vm start
ujust vm ssh
```

### Development Environment

```bash
# Create dev VM with more resources
ujust vm add dev --cpus=8 --ram=16384 --disk-size=200G

# Start it
ujust vm start dev

# SSH in
ujust vm ssh dev

# Your home is at /workspace
```

### Testing Branch

```bash
# Test latest features (long form)
ujust vm add testing-vm --branch=testing

# Or short form
ujust vm add testing-vm -b testing

ujust vm start testing-vm
ujust vm ssh testing-vm
```

### Multiple VMs

```bash
# Create VMs on different ports
ujust vm add dev1 --ssh-port=4444
ujust vm add dev2 --ssh-port=4445
ujust vm add dev3 --ssh-port=4446

# Start all (not a built-in command, use loop)
for vm in dev1 dev2 dev3; do ujust vm start $vm; done
```

## Troubleshooting

### VM Won't Start

**Check:**

```bash
ujust vm status myvm
virsh --connect qemu:///session list --all
```

**Common causes:**

- Disk image not found
- Port conflict
- Virtiofs path issue

**Fix:**

```bash
ujust vm delete myvm
ujust vm add myvm
```

### SSH Connection Refused

**Check:**

```bash
ssh -p 4444 localhost
```

**Common causes:**

- VM not fully booted
- Wrong SSH port
- SSH not started in VM

**Fix:**

```bash
# Wait longer after start
sleep 30
ujust vm ssh myvm

# Check VM console via VNC
ujust vm vnc myvm
```

### Virtiofs Not Working

**Symptom:** `/workspace` empty or not mounted

**Cause:** SHARE_DIR path issue (symlinks)

**Fix:**

```bash
# Delete and recreate with canonical path
ujust vm delete myvm
ujust vm add myvm --share-dir=$(readlink -f $HOME)
```

### Out of Disk Space

**Check:**

```bash
qemu-img info ~/.local/share/libvirt/images/myvm.qcow2
```

**Fix:**

```bash
# Create new VM with larger disk
ujust vm delete myvm
ujust vm add myvm --disk-size=200G
```

## Cross-References

- **Related Skills:** `bootc` (alternative: bootc-based VMs)
- **Prerequisites:** `ujust config libvirtd enable`
- **bcvk alternative:** `ujust install bcvk` + `ujust bootc`

## When to Use This Skill

Use when the user asks about:

- "create VM", "add VM", "start VM"
- "ssh to VM", "connect to VM"
- "download qcow2", "VM image"
- "VM not starting", "VM connection failed"
- "share directory with VM", "virtiofs"
