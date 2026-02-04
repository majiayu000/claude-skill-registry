---
name: omni-talos
description: This skill provides operational tooling and guidance for Omni Proxmox
  infrastructure. Use when the user asks to "check provider status", "restart provider",
  "view provider logs", "debug provider registration", "create a machine class",
  "configure Proxmox provider", "set up CEL storage selectors", "create a Talos cluster",
  or needs guidance on Omni + Proxmox infrastructure integration for Talos Kubernetes
  clusters.
---

# Omni + Proxmox Infrastructure Provider

Operational tooling for Talos Linux Kubernetes clusters via Sidero Omni with Proxmox infrastructure provider.

## Provider Operations

Use `${CLAUDE_PLUGIN_ROOT}/skills/omni-talos/scripts/provider-ctl.py` for provider management:

| Task | Command |
|------|---------|
| View logs | `${CLAUDE_PLUGIN_ROOT}/skills/omni-talos/scripts/provider-ctl.py --logs 50` |
| Raw JSON logs | `${CLAUDE_PLUGIN_ROOT}/skills/omni-talos/scripts/provider-ctl.py --logs 50 --raw` |
| Restart provider | `${CLAUDE_PLUGIN_ROOT}/skills/omni-talos/scripts/provider-ctl.py --restart` |

The provider runs on Foxtrot LXC (CT 200) — script handles SSH automatically.

## Current Deployment

| Component | Location | IP | Endpoint |
|-----------|----------|-----|----------|
| Omni | Holly (VMID 101, Quantum) | 192.168.10.20 | omni.spaceships.work |
| Proxmox Provider | Foxtrot LXC (CT 200, Matrix) | 192.168.3.10 | L2 adjacent to Talos VMs |
| Target Cluster | Matrix (Foxtrot/Golf/Hotel) | 192.168.3.{5,6,7} | Proxmox API |
| Storage | CEPH RBD | — | `vm_ssd` pool |

## Quick Reference

**omnictl commands:**

```bash
omnictl cluster status <cluster-name>
omnictl get machines -l omni.sidero.dev/cluster=<cluster-name>
omnictl get machineclasses
omnictl apply -f machine-classes/<name>.yaml
omnictl cluster template sync -f clusters/<name>.yaml
```

Note: `--cluster` flag does not exist. Use label selector `-l` instead.

**MachineClass minimal example:**

```yaml
metadata:
  namespace: default
  type: MachineClasses.omni.sidero.dev
  id: matrix-worker
spec:
  autoprovision:
    providerid: matrix-cluster
    providerdata: |
      cores: 4
      memory: 16384
      disk_size: 100
      storage_selector: name == "vm_ssd"
      node: foxtrot
```

See `references/machine-classes.md` for full field reference.

## Key Constraints

| Constraint | Details |
|------------|---------|
| L2 adjacency | Provider MUST be on same L2 as Talos VMs (Foxtrot LXC) |
| CEL `type` reserved | Use `name` only for storage selectors |
| Hostname bug | Use `:local-fix` tag, not `:latest` |
| No CP pinning | Omni allows only 1 ControlPlane section per template |
| No VM migration | Destroys node state — destroy/recreate instead |
| Split-horizon DNS | `omni.spaceships.work` → 192.168.10.20 (LAN) |

## Reference Files

| File | Content |
|------|---------|
| `references/architecture.md` | Network topology, design decisions |
| `references/machine-classes.md` | Full provider data fields (compute, storage, network, PCI) |
| `references/provider-setup.md` | Provider config, compose setup, credentials |
| `references/cluster-templates.md` | Cluster template structure, patches |
| `references/cel-storage-selectors.md` | CEL syntax and patterns |
| `references/debugging.md` | Common issues |
| `references/recovery-procedures.md` | Recovery from stuck states |
| `references/proxmox-permissions.md` | API token setup |
| `references/omnictl-auth.md` | Authentication methods |

## Examples

| File | Description |
|------|-------------|
| `examples/machineclass-ceph.yaml` | CEPH storage |
| `examples/machineclass-local.yaml` | Local LVM |
| `examples/cluster-template.yaml` | Complete cluster |
| `examples/proxmox-gpu-worker.yaml` | GPU passthrough |
| `examples/proxmox-storage-node.yaml` | Storage node |
| `examples/proxmox-worker-multi-net.yaml` | Multi-network |
