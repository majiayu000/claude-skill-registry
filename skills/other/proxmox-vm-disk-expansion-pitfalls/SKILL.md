---
name: proxmox-vm-disk-expansion-pitfalls
description: |
  Troubleshoot common failures when expanding Proxmox VM disks on Ubuntu 24.04
  cloud-init images and draining Kubernetes nodes. Use when: (1) growpart fails
  with "command not found" on Ubuntu cloud-init VMs, (2) grep -P fails on macOS
  with "invalid option -- P", (3) kubectl drain times out with pods stuck
  terminating, (4) filesystem shows old size after qm resize. Covers
  cloud-guest-utils installation, macOS-portable regex parsing, drain timeout
  tuning, and recovery from partial failures.
author: Claude Code
version: 1.0.0
date: 2026-02-13
---

# Proxmox VM Disk Expansion Pitfalls

## Problem

Expanding disk storage on Proxmox-hosted Ubuntu 24.04 cloud-init VMs (used as
Kubernetes nodes) fails at multiple points due to missing tools, cross-platform
incompatibilities, and Kubernetes drain timeouts.

## Context / Trigger Conditions

- Running disk expansion scripts from macOS against Proxmox + Ubuntu VMs
- Ubuntu 24.04 cloud-init images (the default k8s node template)
- Kubernetes nodes with many pods or stateful workloads
- Using `scripts/extend_vm_storage.sh` or similar automation

## Issues and Solutions

### 1. `growpart: command not found` on Ubuntu 24.04

**Symptom**: After `qm resize`, SSH into VM, run `growpart /dev/sda 1` — fails
with "command not found". `resize2fs` then reports "Nothing to do!" because the
partition table hasn't been updated.

**Root cause**: Ubuntu 24.04 cloud-init images don't include `cloud-guest-utils`
by default. The `growpart` tool (which updates the partition table to use new
disk space) is in this package.

**Fix**:
```bash
sudo apt-get update -qq && sudo apt-get install -y -qq cloud-guest-utils
sudo growpart /dev/sda 1
sudo resize2fs /dev/sda1
```

**Prevention**: Check for `growpart` before attempting partition expansion:
```bash
if ! command -v growpart &>/dev/null; then
    sudo apt-get update -qq && sudo apt-get install -y -qq cloud-guest-utils
fi
```

### 2. `grep -P` (PCRE) not available on macOS

**Symptom**: Script running on macOS fails with `grep: invalid option -- P`.

**Root cause**: macOS ships BSD grep, which doesn't support `-P` (Perl-compatible
regex). GNU grep (from Homebrew) does, but scripts shouldn't assume it's installed.

**Fix**: Replace `grep -oP 'pattern\Kcapture'` with portable `sed`:
```bash
# BAD (GNU grep only):
CURRENT_SIZE=$(echo "$LINE" | grep -oP 'size=\K[0-9]+G')

# GOOD (portable):
CURRENT_SIZE=$(echo "$LINE" | sed -n 's/.*size=\([0-9]*G\).*/\1/p')
```

**General rule**: In scripts that run on macOS, avoid `grep -P`, `sed -i ''`
vs `sed -i` differences, and `date` flag differences. Use `sed` with basic
regex or bash built-in `[[ =~ ]]` for pattern matching.

### 3. `kubectl drain` timeout with stuck pods

**Symptom**: `kubectl drain --timeout=120s` fails with "context deadline exceeded"
for multiple pods. Pods are evicted but don't terminate in time.

**Root cause**: Some pods (stateful services like ClickHouse, Paperless-ngx,
OnlyOffice) need more time to shut down gracefully. 120s isn't enough when many
pods are draining simultaneously.

**Fix**: Use `--force` flag and a longer timeout, or retry:
```bash
# First attempt with standard timeout
kubectl drain <node> --ignore-daemonsets --delete-emptydir-data --timeout=120s

# If it fails, force with longer timeout (pods already evicting)
kubectl drain <node> --ignore-daemonsets --delete-emptydir-data --timeout=300s --force
```

**Note**: After a failed drain, the node is already cordoned. A second drain
attempt only needs to wait for already-evicting pods to finish.

### 4. Recovery from partial failure

If the script fails mid-way (after drain but before uncordon):

```bash
# Check VM status
ssh root@192.168.1.127 "qm status <vmid>"

# Start VM if stopped
ssh root@192.168.1.127 "qm start <vmid>"

# Uncordon node
kubectl --kubeconfig $(pwd)/config uncordon <node-name>
```

## Verification

After successful expansion:
```bash
# On the VM
df -h /
# Should show new size (128G disk → ~126G usable for ext4)

# On the cluster
kubectl get node <name>
# Should show Ready status
```

## Notes

- The k8s node VMs use direct partition layout (`/dev/sda1`), not LVM, despite
  the script handling both paths
- `growpart` returns exit code 1 for "NOCHANGE" (partition already at max) —
  this is not an error
- Proxmox `qm resize` uses `scsi0` as the disk identifier for these VMs
- SSH host keys may change if VMs are recreated or network changes — use
  `-o StrictHostKeyChecking=no` in automated scripts

See also: `extend-vm-storage.md` (the operational skill for running the script)
