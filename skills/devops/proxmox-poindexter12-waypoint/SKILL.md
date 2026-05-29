---
name: proxmox
description: |
  Proxmox VE virtualization platform reference for VM/LXC management, clustering,
  storage, and networking. Includes Terraform and Ansible integration patterns.
  Use when working with Proxmox configurations, CLI commands, troubleshooting
  VMs/containers, or planning resource allocation.
  Triggers: proxmox, qemu, kvm, lxc, pve, vm, container, cluster, vzdump, qm, pct.
agent: proxmox-expert
---

# Proxmox Skill

Proxmox VE virtualization platform reference for VM management, containers, clustering, and homelab infrastructure.

## Quick Reference

```bash
# VM management (qm)
qm list                           # List all VMs
qm status <vmid>                  # Check VM status
qm start <vmid>                   # Start VM
qm stop <vmid>                    # Stop VM (graceful)
qm shutdown <vmid>                # Shutdown VM (ACPI)
qm unlock <vmid>                  # Remove lock
qm config <vmid>                  # Show VM config

# Container management (pct)
pct list                          # List all containers
pct status <ctid>                 # Check container status
pct start <ctid>                  # Start container
pct stop <ctid>                   # Stop container
pct enter <ctid>                  # Enter container shell

# Cluster management (pvecm)
pvecm status                      # Cluster status and quorum
pvecm nodes                       # List cluster nodes

# API shell (pvesh)
pvesh get /nodes                  # List nodes via API
pvesh get /nodes/<node>/status    # Node resource status

# Backup (vzdump)
vzdump <vmid> --mode snapshot --storage <storage>
vzdump --all --compress zstd
```

## Reference Files

Load on-demand based on task:

| Topic | File | When to Load |
|-------|------|--------------|
| VM vs LXC | [vm-lxc.md](references/vm-lxc.md) | Choosing virtualization type |
| Docker Hosting | [docker-hosting.md](references/docker-hosting.md) | Running Docker on Proxmox |
| Networking | [networking.md](references/networking.md) | Bridges, VLANs, SDN, firewall |
| Storage | [storage.md](references/storage.md) | Storage backends, content types |
| Cloud-init | [cloud-init-templates.md](references/cloud-init-templates.md) | VM provisioning with cloud-init |
| Clustering | [clustering.md](references/clustering.md) | HA, quorum, fencing |
| Backup | [backup.md](references/backup.md) | vzdump modes, restore |
| CLI Tools | [cli-tools.md](references/cli-tools.md) | qm, pct, pvecm, pvesh commands |
| Troubleshooting | [troubleshooting.md](references/troubleshooting.md) | Common errors, diagnostics |
| Automation Tools | [automation-tools.md](references/automation-tools.md) | Terraform/Ansible integration |

## Validation Checklist

Before deploying VMs/containers:

- [ ] Cluster status healthy (`pvecm status`)
- [ ] Node resources available (CPU, RAM, disk)
- [ ] Storage accessible and mounted
- [ ] Network bridges configured correctly
- [ ] VLAN tags match network design
- [ ] Resource allocation within node limits
- [ ] HA configuration correct (if enabled)
- [ ] Backup schedule in place
- [ ] Naming convention followed

## VM vs LXC Quick Decision

| Factor | Use VM | Use LXC |
|--------|--------|---------|
| OS | Windows, BSD, any | Linux only |
| Isolation | Full kernel isolation | Shared kernel |
| Performance | Good | Better (lighter) |
| Startup | Slower | Fast |
| Density | Lower | Higher |
| Complexity | Any workload | Simple services |

## Homelab Network VLANs

| VLAN | Purpose | Proxmox Bridge |
|------|---------|----------------|
| 5 | Management (Web UI, API, SSH) | vmbr5 |
| 1 | Trusted network | vmbr0 |
| 11 | Storage (NFS/Ceph, MTU 9000) | vmbr11 |
| 12 | High-speed transfers | vmbr12 |
