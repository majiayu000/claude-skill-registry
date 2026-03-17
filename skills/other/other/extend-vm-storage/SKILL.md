---
name: extend-vm-storage
description: |
  Extend disk storage on a Kubernetes node VM (Proxmox-hosted).
  Use when: (1) User wants to increase disk space on a k8s node VM,
  (2) A node is running low on disk, (3) User says "extend storage"
  or "add disk space". Automates: drain → shutdown → resize → boot →
  expand filesystem → uncordon.
author: Claude Code
version: 1.0.0
date: 2025-01-01
---

# Extend VM Storage Skill

**Purpose**: Extend disk storage on a Kubernetes node VM (Proxmox-hosted).

**When to use**: User wants to increase disk space on a k8s node VM, or a node is running low on disk.

## Workflow

### 1. Identify the Node

Ask the user which node needs more storage and how much to add.

Valid nodes: `k8s-master`, `k8s-node1`, `k8s-node2`, `k8s-node3`, `k8s-node4`

### 2. Run the Script

```bash
./scripts/extend_vm_storage.sh <node-name> <size-increment>
```

**Example**:
```bash
./scripts/extend_vm_storage.sh k8s-node2 +64G
```

### 3. What the Script Does

1. Validates inputs (node name and size format)
2. Resolves node IP via kubectl
3. Prompts for confirmation
4. Drains the node (evicts pods)
5. Shuts down the VM in Proxmox
6. Resizes the disk (`scsi0`) by the given increment
7. Starts the VM and waits for SSH
8. Expands the filesystem inside the guest (auto-detects LVM vs direct partition)
9. Uncordons the node
10. Shows verification output (`df -h` and node status)

### 4. Update Terraform (if needed)

If you want Terraform to reflect the new disk size, update the VM definition in `main.tf` or `modules/create-vm/` so that a future `terraform apply` doesn't revert the change. Check if the VM disk size is managed by Terraform:

```bash
grep -A5 "disk" main.tf | grep -i size
```

If managed, update the size value to match the new total.

### 5. Verification

After the script completes, verify:
```bash
kubectl --kubeconfig $(pwd)/config get nodes
ssh wizard@<node-ip> "df -h /"
```

## Recovery

If the script fails mid-way:
1. Check VM status: `ssh root@192.168.1.127 "qm status <vmid>"`
2. Start VM if stopped: `ssh root@192.168.1.127 "qm start <vmid>"`
3. Uncordon node: `kubectl --kubeconfig $(pwd)/config uncordon <node-name>`

## Constants

| Setting | Value |
|---------|-------|
| Proxmox host | `root@192.168.1.127` |
| VM SSH user | `wizard` |
| Disk name | `scsi0` |
| Shutdown timeout | 300s |
| SSH wait timeout | 300s |

## Questions to Ask User

1. Which node needs more storage?
2. How much storage to add? (e.g., +64G)
