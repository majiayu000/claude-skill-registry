---
name: vm-ops
description: Safe VM operations (start, stop, destroy) via protected wrapper script
---

# VM Operations Skill

## CRITICAL SAFETY RULE

**NEVER run Proxmox commands directly via SSH.**

Always use the wrapper script `vms/proxmox-ops.sh` which:
- Checks VMIDs against the readonly list before ANY destructive operation
- Protects production VMs (104, 109) from accidental modification
- Provides consistent error handling and logging

## Protected VMs (READONLY)

These VMIDs are protected and the wrapper will REFUSE operations on them:

| VMID | Name | Purpose |
|------|------|---------|
| 104 | doc1 | Main services VM - Docker workloads |
| 109 | igp | Media transcoding with iGPU passthrough |
| 110 | dev | Development VM |

If you need to manage these VMs, they must be moved from `imported` to `managed` in `vms/definitions.nix` first.

## Commands

### View Operations (safe, no protection needed)

```bash
# List all VMs
./vms/proxmox-ops.sh list

# Get VM status
./vms/proxmox-ops.sh status <vmid>

# Get VM configuration
./vms/proxmox-ops.sh config <vmid>

# Get VM IP address
./vms/proxmox-ops.sh get-ip <vmid>

# Get storage status
./vms/proxmox-ops.sh storage

# Get next available VMID
./vms/proxmox-ops.sh next-vmid [start] [end]
```

### Lifecycle Operations (protected)

```bash
# Start VM
./vms/proxmox-ops.sh start <vmid>

# Stop VM (immediate)
./vms/proxmox-ops.sh stop <vmid>

# Shutdown VM (graceful)
./vms/proxmox-ops.sh shutdown <vmid>

# Destroy VM (requires explicit confirmation)
./vms/proxmox-ops.sh destroy <vmid> yes
```

### Configuration Operations (protected)

```bash
# Configure CPU/RAM
./vms/proxmox-ops.sh configure <vmid> <cores> <memory_mb>

# Resize disk
./vms/proxmox-ops.sh resize <vmid> <disk> <size>
# Example: ./vms/proxmox-ops.sh resize 110 scsi0 +10G

# Create disk
./vms/proxmox-ops.sh create-disk <vmid> <size> [storage] [disk]
```

### SSH Operations

```bash
# Wait for SSH to become available
./vms/proxmox-ops.sh wait-ssh <ip> [timeout] [user]
# Example: ./vms/proxmox-ops.sh wait-ssh 192.168.1.163 120 abl030
```

### Serial Console

```bash
# Stream serial console (interactive when run in a real TTY)
./vms/proxmox-ops.sh console <vmid>
```

## Examples

### Restart a managed VM

```bash
./vms/proxmox-ops.sh stop 110
./vms/proxmox-ops.sh start 110
```

### Check if a VM is running

```bash
./vms/proxmox-ops.sh status 110
# Output: status: running
```

### Stream VM serial console

```bash
./vms/proxmox-ops.sh console 9003
```

### Destroy a test VM

```bash
# This will FAIL on protected VMIDs (104, 109)
./vms/proxmox-ops.sh destroy 110 yes
```

### Attempting operation on protected VM

```bash
./vms/proxmox-ops.sh stop 104
# ERROR: VMID 104 is marked as READONLY (imported).
# Operation 'stop' is not allowed on imported VMs.
```

## What NOT to Do

**WRONG - Direct SSH command:**
```bash
ssh root@192.168.1.12 "qm stop 104"  # DANGEROUS - bypasses protection!
```

**RIGHT - Use wrapper:**
```bash
./vms/proxmox-ops.sh stop 104  # Will be blocked with clear error
```

## VMID Ranges

| Range | Purpose |
|-------|---------|
| 100-199 | Production VMs |
| 200-299 | LXC containers |
| 9000-9999 | Templates |

## Related Files

| File | Purpose |
|------|---------|
| `vms/proxmox-ops.sh` | Wrapper script (USE THIS) |
| `vms/definitions.nix` | VM definitions, readonly flags |
