---
name: virtualization
description: |
  GPU passthrough and virtualization for Bazzite. KVM/VFIO setup, Looking Glass (kvmfr),
  USB hotplug for VMs, and libvirt configuration. Use when users need GPU passthrough
  or advanced virtualization features.
---

# Virtualization - Bazzite GPU Passthrough & KVM

## Overview

Advanced virtualization features for Bazzite including KVM, VFIO GPU passthrough, Looking Glass (kvmfr), and USB hotplug for VMs.

## Quick Reference

| Command | Description |
|---------|-------------|
| `ujust setup-virtualization` | Main virtualization setup |
| `ujust setup-virtualization virt-on` | Enable KVM/libvirt |
| `ujust setup-virtualization virt-off` | Disable KVM/libvirt |
| `ujust setup-virtualization vfio-on` | Enable VFIO passthrough |
| `ujust setup-virtualization vfio-off` | Disable VFIO passthrough |
| `ujust setup-virtualization kvmfr` | Setup Looking Glass |
| `ujust setup-virtualization usbhp-on` | Enable USB hotplug |
| `ujust setup-virtualization usbhp-off` | Disable USB hotplug |

## KVM/Libvirt

### Enable Virtualization

```bash
# Enable KVM and libvirt
ujust setup-virtualization virt-on
```

**Enables:**
- libvirtd service
- User permissions for VMs
- Default network
- QEMU/KVM backend

### Disable Virtualization

```bash
# Disable KVM and libvirt
ujust setup-virtualization virt-off
```

## VFIO GPU Passthrough

### Enable VFIO

```bash
# Enable VFIO for GPU passthrough
ujust setup-virtualization vfio-on
```

**What VFIO does:**
- Isolates GPU from host
- Passes GPU directly to VM
- Near-native GPU performance in VM

**Requirements:**
- Two GPUs (or iGPU + dGPU)
- IOMMU support (VT-d or AMD-Vi)
- Supported GPU

### Disable VFIO

```bash
# Disable VFIO passthrough
ujust setup-virtualization vfio-off
```

Returns GPU to host control.

## Looking Glass (kvmfr)

### Setup kvmfr

```bash
# Setup Looking Glass shared memory
ujust setup-virtualization kvmfr
```

**Looking Glass:**
- Zero-copy GPU framebuffer sharing
- Near-zero latency display
- No GPU encoding needed
- Mouse/keyboard passthrough

**Requirements:**
- Windows VM with GPU passthrough
- Looking Glass host app
- IVSHMEM device in VM

### Using Looking Glass

1. **Host:** Run `looking-glass-client`
2. **VM:** Run Looking Glass host service
3. Connect via shared memory

## USB Hotplug

### Enable USB Hotplug

```bash
# Enable USB device hotplug for VMs
ujust setup-virtualization usbhp-on
```

Allows:
- Hot-add USB devices to running VMs
- Dynamic USB device assignment
- No VM restart needed

### Disable USB Hotplug

```bash
ujust setup-virtualization usbhp-off
```

## Common Workflows

### Basic VM Setup

```bash
# Enable virtualization
ujust setup-virtualization virt-on

# Use virt-manager for GUI
virt-manager
```

### Gaming VM with GPU Passthrough

```bash
# 1. Enable VFIO
ujust setup-virtualization vfio-on

# 2. Reboot (GPU now isolated)
systemctl reboot

# 3. Create VM with GPU
# In virt-manager: Add PCI device (GPU)

# 4. Optional: Setup Looking Glass
ujust setup-virtualization kvmfr
```

### Dynamic USB Access

```bash
# Enable USB hotplug
ujust setup-virtualization usbhp-on

# In running VM:
# - Right-click VM in virt-manager
# - Add Hardware > USB Host Device
# - Select device
```

## IOMMU Groups

### Check IOMMU

```bash
# Verify IOMMU enabled
dmesg | grep -i iommu

# List IOMMU groups
for d in /sys/kernel/iommu_groups/*/devices/*; do
  n=${d#*/iommu_groups/*}; n=${n%%/*}
  printf 'IOMMU Group %s ' "$n"
  lspci -nns "${d##*/}"
done
```

### GPU IOMMU Group

```bash
# Find GPU group
lspci -nn | grep -i nvidia
# or
lspci -nn | grep -i amd
```

Ideal: GPU alone in IOMMU group. If not, may need ACS override patch.

## VM Management

### Virsh Commands

```bash
# List VMs
virsh list --all

# Start VM
virsh start <vm-name>

# Shutdown VM
virsh shutdown <vm-name>

# Force off
virsh destroy <vm-name>
```

### GUI Management

```bash
# virt-manager (GUI)
virt-manager

# GNOME Boxes (simpler)
gnome-boxes
```

## Troubleshooting

### VFIO Not Binding GPU

**Check IOMMU:**

```bash
dmesg | grep -i iommu
# Should show "IOMMU enabled"
```

**Enable in BIOS:**
- Intel: VT-d
- AMD: AMD-Vi / IOMMU

**Check binding:**

```bash
lspci -nnk | grep -A3 "VGA\|Audio"
# Kernel driver should be vfio-pci
```

### Looking Glass Black Screen

**Check IVSHMEM:**

```bash
# In VM, verify IVSHMEM device exists
# Check Looking Glass host logs
```

**Verify shared memory:**

```bash
ls -la /dev/shm/looking-glass
```

### USB Device Not Passing Through

**Check permissions:**

```bash
# User in libvirt group?
groups $USER
```

**Check device:**

```bash
lsusb
# Identify device ID
```

### VM Won't Start After VFIO

**GPU still attached to host:**

```bash
# Verify VFIO binding
lspci -nnk | grep -A3 "VGA"
# Should show: Kernel driver in use: vfio-pci
```

**Reboot may be needed after vfio-on.**

## Cross-References

- **bazzite-ai:vm** - QCOW2 VM management
- **bazzite:gpu** - GPU driver configuration
- **bazzite-ai:configure** - libvirtd service

## When to Use This Skill

Use when the user asks about:
- "GPU passthrough", "VFIO", "pass GPU to VM"
- "Looking Glass", "kvmfr", "VM display"
- "KVM", "libvirt", "virtualization"
- "USB hotplug", "pass USB to VM"
- "gaming VM", "Windows VM", "VM performance"
- "IOMMU", "VT-d", "AMD-Vi"
