---
name: virtualization
description: >
  · Create/troubleshoot VMs and hypervisors: Proxmox, QEMU/KVM, libvirt, XCP-ng, vSphere. Triggers: 'proxmox', 'qemu', 'kvm', 'libvirt', 'virsh', 'vm', 'hypervisor', 'cloud-init', 'xcp-ng'. Not for containers (use docker).
license: MIT
compatibility: "Varies by hypervisor. Proxmox: pvesh, qm, pct. Libvirt: virsh, virt-install. Optional: packer, terraform"
metadata:
  source: iuliandita/skills
  date_added: "2026-04-02"
  effort: high
  argument_hint: "[hypervisor-or-task]"
---

# Virtualization: Hypervisors, VMs, and Infrastructure

Create, configure, and manage virtual machines across hypervisors - from single-node Proxmox
setups to multi-node clusters with HA, live migration, and GPU passthrough. The goal is
production-ready VM infrastructure with correct storage, memory, and CPU config that won't
bite you at 3 AM.

**Target versions** (verified May 2026):

| Tool | Version | Release date | Notes |
|------|---------|-------------|-------|
| Proxmox VE | 9.1 | Nov 2025 | Debian 13.2 (trixie), kernel 6.17.2, QEMU 10.1.2 |
| Proxmox Backup Server | 4.1 | Nov 2025 | Dedup, incremental, prune policies |
| bpg/proxmox (Terraform) | 0.100.0 | Apr 2026 | Primary Proxmox IaC provider |
| QEMU | 11.0.1 | Apr 2026 | Stable (11.0 series; GA Apr 22, 2026) |
| libvirt | 12.0.0 | Jan 2026 | Hypervisor abstraction layer |
| XCP-ng | 8.3 LTS | Oct 2024 | Xen-based, LTS since Jun 2025, EOL Nov 2028 |
| VMware ESXi | 8.0 U3i | Feb 2026 | Broadcom-owned, licensing upheaval |
| VirtualBox | 7.2.6 | Jan 2026 | Dev/testing only |
| Packer | 1.15.1 | Mar 2026 | Image builder, multi-platform |
| cloud-init | 26.1 | Feb 2026 | Instance initialization standard |

## When to use

- Creating or configuring VMs on Proxmox, libvirt/KVM, XCP-ng, or VMware
- Provisioning Proxmox VMs with Terraform (bpg/proxmox provider)
- Building VM templates with Packer and cloud-init
- Configuring PCI/GPU passthrough for compute or display GPUs
- Managing storage backends (LVM-thin, ZFS, Ceph, NFS)
- Setting up Proxmox clustering, HA, and live migration
- Troubleshooting VM performance (disk I/O, memory, CPU)
- Planning backup strategies (Proxmox Backup Server, snapshots)
- Tuning disk performance (virtio-scsi, iothread, discard/fstrim)
- Memory management (ballooning, NUMA topology, hugepages)

## When NOT to use

- Kubernetes manifests, Helm charts, container orchestration (use **kubernetes**)
- General Terraform/OpenTofu HCL patterns, state, modules (use **terraform**)
- Network config not hypervisor-specific: DNS, VPNs, reverse proxies (use **networking**)
- Ansible playbooks and configuration management (use **ansible**)
- Docker/container image optimization (use **docker**)
- OPNsense/pfSense firewall management (use **firewall-appliance**)

---

## AI Self-Check

AI tools consistently produce the same VM configuration mistakes. **Before returning any
generated VM config, Terraform HCL, or Packer template, verify against this list:**

- [ ] No hardcoded IPs, passwords, or SSH keys - use variables or cloud-init injection
- [ ] Disk interface is virtio (scsi0 with virtio-scsi controller), not IDE, unless legacy OS
- [ ] `iothread = true` on virtio-scsi disks for SSD-backed storage
- [ ] `ssd = true` emulation enabled when backing store is SSD (enables guest TRIM)
- [ ] `discard = on` on QEMU disk config for thin-provisioned storage (fstrim passthrough)
- [ ] Memory ballooning disabled unless tested on the specific guest OS (Alpine, some BSDs can't
  hotplug DIMMs - balloon changes need full power-cycle, not reboot)
- [ ] In bpg/proxmox Terraform: ballooning is disabled by setting the provider's minimum-memory/balloon field to 0 (verify exact key in the bpg/proxmox docs - commonly `memory_min_mb` or `balloon`; do not invent a field name without checking)
- [ ] CPU type is `host` for production (full feature passthrough), not `kvm64`/`qemu64`
- [ ] NUMA enabled for multi-socket or large-memory VMs
- [ ] QEMU guest agent enabled (cloud-init installs it, but verify)
- [ ] Cloud-init interface specified (bpg/proxmox defaults to ide2 when null)
- [ ] Terraform lifecycle: `prevent_destroy` on VMs, `ignore_changes` on `disk` and `node_name`
- [ ] No disk resize via Terraform - use `qm resize` on host, then update Terraform var to match
- [ ] PCI passthrough: `pcie = false` for standard passthrough, `xvga = false` unless display GPU
- [ ] PCI passthrough: machine type is `q35` when `pcie = true` is needed
- [ ] GPU passthrough: AMD GPUs are prone to reset bugs (vendor-reset kernel module or `pcie_port_pm=off` may be required); NVIDIA generally resets cleanly but verify with your card model before production use
- [ ] BIOS type matches use case: `seabios` default, `ovmf` for UEFI/Secure Boot/Windows 11
- [ ] Backup retention configured (not unlimited snapshots eating storage)
- [ ] Network device uses `virtio` model, not `e1000` or `rtl8139`
- [ ] `fstrim.timer` enabled in guest for thin-provisioned storage (completes the discard chain)
- [ ] SCSI controller explicitly set (`virtio-scsi-single` for high IOPS, `virtio-scsi-pci` default)
- [ ] Machine type matches BIOS: `i440fx` with `seabios`, `q35` with `ovmf` (UEFI). Mixing
  `i440fx` + `ovmf` causes boot failures. `q35` + `seabios` works but wastes q35 features.
- [ ] VGA type matches use case: `serial0` for headless cloud images, `virtio` for GUI VMs,
  omit for PCI passthrough display GPUs (`x-vga=1` replaces the virtual display)
- [ ] **Current source checked**: dated versions, CLI flags, API names, and support windows are verified against primary docs before repeating them
- [ ] **Hidden state identified**: local config, credentials, caches, contexts, branches, cluster targets, or previous runs are made explicit before acting
- [ ] **Verification is real**: final checks exercise the actual runtime, parser, service, or integration point instead of only linting prose or happy paths
- [ ] **Routing overlap checked**: overlapping skills, trigger terms, and "When NOT to use" boundaries are checked before returning guidance
- [ ] **Spec claims verified**: claims about tool behavior, output contracts, or repo conventions are checked against current docs, scripts, or skill files
- [ ] **Hypervisor/version checked**: Proxmox, QEMU/KVM, libvirt, XCP-ng, vSphere, and cloud-init advice matches the target platform
- [ ] **Storage risk gated**: disk format, snapshot, passthrough, and migration commands preserve data and rollback

---

## Performance

- Choose storage format and cache mode based on workload: latency, snapshots, thin provisioning, and backup behavior differ.
- Right-size vCPU, NUMA, memory ballooning, and I/O queues from measured host pressure.
- Use templates and cloud-init for repeatable VM creation instead of manual clone drift.


---

## Best Practices

- Snapshot before guest-agent, disk, boot, passthrough, or hypervisor upgrades, but do not treat snapshots as backups.
- Keep host, guest, and storage backups independently restorable.
- Document PCI/GPU passthrough bindings so kernel updates do not strand the host.


## Workflow

### Step 1: Identify the task

| Task | Start with | Reference |
|------|------------|-----------|
| **Proxmox VM creation** | CLI (qm) or API (pvesh), cloud-init | `references/proxmox.md` |
| **Terraform provisioning** | bpg/proxmox provider, lifecycle rules | `references/proxmox.md` (Terraform section) |
| **Image building** | Packer + cloud-init templates | `references/image-building.md` |
| **libvirt/KVM management** | virsh, XML domain definitions | `references/libvirt-qemu-kvm.md` |
| **GPU/PCI passthrough** | IOMMU groups, vfio-pci | `references/proxmox.md` (PCI section) |
| **Performance tuning** | Disk, memory, CPU config | This file + references |
| **Migration to Proxmox** | From VMware, XCP-ng, or bare metal | `references/proxmox.md` |

### Step 2: Gather requirements

Before creating or modifying VMs:

- **Hypervisor and version** - Proxmox VE 9.x? libvirt? VMware migration?
- **Guest OS** - Linux distro, Windows, BSD? (affects virtio drivers, ballooning, agent)
- **CPU** - core count, type (host vs emulated), pinning needs, NUMA topology
- **Memory** - dedicated amount, ballooning (usually: don't), hugepages for databases
- **Storage** - backend (LVM-thin, ZFS, Ceph, NFS), disk size, format (raw vs qcow2)
- **Network** - bridge, VLAN tag, virtio, firewall
- **Passthrough** - GPU/PCI devices, USB, serial ports
- **Provisioning method** - manual, Terraform, Packer template + cloud-init
- **HA requirements** - clustered? live migration? fencing?
- **Backup strategy** - PBS, snapshots, vzdump, frequency

### Step 3: Build

Follow the domain-specific reference file. Key principles:

- **Use cloud-init for provisioning.** Don't manually configure VMs after creation. Inject SSH
  keys, network config, packages, and user accounts via cloud-init.
- **Use virtio everywhere.** Disk (virtio-scsi), network (virtio-net), display (virtio-gpu for
  headless). IDE and e1000 exist for legacy OS compatibility only.
- **Pin CPU type to `host`.** Emulated CPU types (kvm64, qemu64) hide features the guest needs
  (AES-NI, AVX, SSE4). Use `host` unless you need live migration across heterogeneous hardware.
- **Test disk config changes with stop/start, not reboot.** Guest reboot doesn't restart QEMU -
  disk config changes (discard, cache, iothread) only take effect after `qm stop` + `qm start`.

### Step 4: Validate

| What to validate | How |
|-----------------|-----|
| VM boots and agent responds | `qm agent <vmid> ping` (Proxmox) |
| Cloud-init completed | `cloud-init status --wait` in guest |
| Disk performance | `fio --name=test --rw=randread --bs=4k --direct=1 --numjobs=4 --runtime=30` |
| TRIM/discard working | `fstrim -v /` in guest, check thin pool data_percent on host |
| PCI passthrough | `lspci` in guest shows passed device, driver loaded |
| Network connectivity | `ping gateway`, check `ip addr` matches cloud-init config |
| Memory | `free -h` in guest matches expected (not balloon-reduced) |
| Live migration | Test with `qm migrate <vmid> <target> --online` on non-critical VM first |

---

## Quick Task: VM from Cloud Image (Proxmox)

The fastest path to a production-ready VM. Skip Packer and ISO installs for standard setups.

1. Download a cloud image to the Proxmox node (note: the URL below points to a daily/testing image; prefer a stable release image - daily images may have cloud-init metadata gaps causing first-boot surprises):
   `wget -P /var/lib/vz/template/iso/ https://cloud.debian.org/images/cloud/trixie/daily/latest/debian-13-generic-amd64.qcow2`
2. Create the VM shell:
   `qm create 100 --name myvm --memory 2048 --cores 2 --cpu host --net0 virtio,bridge=vmbr0 --agent enabled=1 --scsihw virtio-scsi-pci`
3. Import and attach the disk with SSD optimizations:
   `qm importdisk 100 debian-13-generic-amd64.qcow2 local-lvm`
   `qm set 100 --scsi0 local-lvm:vm-100-disk-0,discard=on,iothread=1,ssd=1 --boot order=scsi0`
4. Add cloud-init drive and configure:
   `qm set 100 --ide2 local-lvm:cloudinit`
   `qm set 100 --ciuser admin --sshkeys ~/.ssh/id_ed25519.pub --ipconfig0 ip=10.10.10.100/24,gw=10.10.10.1`
5. Start: `qm start 100`
6. Verify: `qm agent 100 ping` (may take 1-2 min on first boot while cloud-init runs)

To make a reusable template, stop the VM after verification and run `qm template 100`.
Clone with `qm clone 100 101 --name new-vm --full`.

---

## Proxmox VE Quick Reference

Read `references/proxmox.md` for full coverage of API, CLI, storage backends, clustering,
HA, migration, PCI passthrough, backup, and Terraform patterns.

### Essential CLI

```bash
# VM management
qm list                              # List all VMs
qm create 100 --name test --memory 2048 --cores 2 --net0 virtio,bridge=vmbr0
qm start/stop/shutdown/reset 100     # Power operations
qm config 100                        # Show VM config
qm set 100 --memory 4096             # Modify config (some need stop/start)
qm resize 100 scsi0 +10G             # Extend disk (can't shrink)
qm agent 100 ping                    # Test QEMU agent
qm migrate 100 pve2 --online --with-local-disks  # Live migrate

# Container management
pct list                              # List LXC containers
pct create 200 local:vztmpl/debian-12-standard_12.7-1_amd64.tar.zst

# Storage
pvesm status                          # Storage pool overview
lvs -a -o+devices                     # LVM thin pool status (on LVM backend)

# Cluster
pvecm status                          # Cluster status
pvecm nodes                           # Node list
ha-manager status                     # HA status
```

### Critical gotchas (battle-tested)

These come from production Proxmox environments and will save hours of debugging:

**Stop/start vs reboot:** Guest `reboot` does NOT restart the QEMU process. Disk config
changes (discard, cache mode, iothread, bus type) only apply when QEMU starts fresh.
Always use `qm stop` then `qm start` for hardware config changes. This also applies to
memory balloon device changes.

**LVM thin pool at 100%:** When data_percent hits 100%, ALL VM I/O on that pool fails
instantly - guests hang, no graceful degradation. Recovery requires `lvextend` on the
thin pool or migrating VMs off. Monitor thin pool usage and alert well before 100% (80%
warning, 90% critical). `data_percent` measures blocks ever written, not current filesystem
usage - a VM that wrote then deleted 50GB still shows that 50GB in data_percent until
fstrim reclaims it.

**Live migration via SSH:** `qm migrate` runs in the foreground. If the SSH session drops,
the migration aborts. For large VMs (32GB+ disk), use:
```bash
nohup qm migrate <vmid> <target> --online --with-local-disks \
  > /tmp/migrate-<vmid>.log 2>&1 &
```
Migration is abort-safe: source VM stays running on failure, target LVs are cleaned up.

**KVM ballooning:** The balloon device lets the host reclaim unused guest memory. Sounds
great, causes pain. Alpine Linux (and some BSDs) can't hotplug DIMMs - balloon changes
need full power-cycle (stop/start, not reboot). Even on Debian, balloon behavior is
unpredictable under memory pressure. Recommendation: disable ballooning (`memory_min_mb = 0`
in Terraform, or set balloon to 0 in qm) and provision VMs with the memory they actually need.

**fail2ban on Proxmox (Debian 13):** `/var/log/daemon.log` doesn't exist under journald.
Use `backend = systemd` with `journalmatch = _COMM=pvedaemon` in the jail config.

**openipmi on non-IPMI hardware:** Fails on boot, generates spurious alerts. Safe to
`systemctl mask openipmi` on nodes without BMC/IPMI hardware. Masking survives package
updates; disabling doesn't.

---

## Storage Performance

| Backend | Best for | Thin provision | Snapshot | Live migration |
|---------|----------|---------------|----------|----------------|
| LVM-thin | Local SSDs, production | Yes | Yes (copy-on-write) | With --with-local-disks |
| ZFS | Data integrity, compression | Yes | Yes (native) | With replication |
| Ceph/RBD | Multi-node shared storage | Yes | Yes | Native (shared) |
| NFS | ISOs, templates, backups | Depends on NAS | Depends | Yes (shared) |
| local (dir) | Small/test | No (file-based) | qcow2 only | No |

**Disk interface hierarchy** (fastest to slowest):
1. **virtio-scsi-single** + iothread - one controller per disk, best IOPS
2. **virtio-scsi-pci** + iothread - shared controller, good for most workloads
3. **virtio-blk** - legacy virtio, good performance but fewer features
4. **IDE** - legacy only, needed for some old OSes

**SSD optimization checklist:**
- [ ] `ssd = 1` on disk config (tells guest it's on SSD, enables TRIM in guest)
- [ ] `discard = on` on QEMU disk (passes TRIM/UNMAP to storage backend)
- [ ] `fstrim.timer` enabled in guest (weekly by default on systemd distros)
- [ ] Verify with: `fstrim -v /` in guest, then check `lvs -o data_percent` on host

**Disk resize (the Terraform trap):** Can't resize disks via the bpg/proxmox Terraform
provider. The correct procedure:
1. `qm resize <vmid> scsi0 +10G` on the Proxmox host
2. `growpart /dev/sda 1` in the guest (expand partition)
3. `resize2fs /dev/sda1` in the guest (expand filesystem)
4. Update the `disk_size_gb` variable in Terraform to match

---

## GPU / PCI Passthrough Quick Reference

Full details (IOMMU groups, ACS override, Terraform patterns) in `references/proxmox.md`.
The minimum viable path for a Windows 11 + NVIDIA desktop GPU on Proxmox VE 9.x:

1. **Host prereqs.** Enable VT-d / AMD-Vi in BIOS. Add `intel_iommu=on` (or `amd_iommu=on`)
   plus `iommu=pt` to the kernel command line (`/etc/kernel/cmdline` on PVE with systemd-boot,
   `/etc/default/grub` on legacy). Run `proxmox-boot-tool refresh` (or `update-grub`) and reboot.
2. **Bind to vfio-pci.** `lspci -nn | grep -i nvidia` to find vendor:device IDs, then:
   `echo "options vfio-pci ids=10de:XXXX,10de:YYYY" > /etc/modprobe.d/vfio-pci.conf` (GPU +
   its audio function). Blacklist `nouveau` and `nvidia`. `update-initramfs -u` and reboot.
   Verify with `lspci -nnk | grep -A3 NVIDIA` - driver in use must be `vfio-pci`.
3. **VM settings for Windows 11.** Machine type `q35`, BIOS `ovmf` (add an EFI disk), TPM v2.0
   state disk, `cpu: host`, `hidden=1` to dodge NVIDIA's Code 43 on older drivers. Example:
   `qm set 100 --machine q35 --bios ovmf --cpu host,hidden=1 --efidisk0 local-lvm:1,format=raw`
4. **Attach the GPU.** Prefer hardware mappings (PVE 8.1+) for migration safety:
   `pvesh create /cluster/mapping/pci --id gpu-rtx4070 --map 'node=pve1,path=0000:01:00.0'`
   then `qm set 100 --hostpci0 mapping=gpu-rtx4070,pcie=1,x-vga=1`. Legacy form:
   `--hostpci0 01:00,pcie=1,x-vga=1`. Drop `x-vga` for compute-only passthrough.
5. **Check IOMMU groups** with `find /sys/kernel/iommu_groups/ -type l | sort -V` before
   anything else - every device in the target group gets passed through together. Single-GPU
   hosts need early vfio binding (initramfs) or the host driver claims it first.

**Reset bug:** NVIDIA consumer cards (including RTX 4070) usually reset cleanly, but verify
with two successive VM restarts before production. AMD RX 5000/6000 series often need the
`vendor-reset` kernel module or `pcie_port_pm=off`. If the second VM start hangs, you hit it.

---

## Memory Management

**Ballooning - the short version:** Don't use it unless you've tested it on your exact
guest OS and workload. Disable with `balloon: 0` in VM config.

**NUMA:** Enable for VMs with 4+ cores or 8GB+ RAM. Proxmox: `numa: 1` in VM config.
QEMU auto-creates NUMA nodes matching the host topology.

**Hugepages:** 2MB or 1GB pages reduce TLB misses. Significant for databases and
memory-intensive workloads. Configure on the host:
```bash
# Reserve 1024 x 2MB hugepages (2GB total)
echo 1024 > /proc/sys/vm/nr_hugepages
# Persistent: add to /etc/sysctl.d/
vm.nr_hugepages = 1024
```
Then enable in VM config. Note: hugepages memory can't be shared or ballooned.

**CPU hotplug vs memory hotplug:** CPU hotplug works live on most modern Linux guests.
Memory hotplug (adding DIMMs at runtime) is fragile - Alpine can't do it at all, and even
Debian requires specific kernel config. Size memory correctly at creation time.

---

## libvirt/QEMU Quick Start

For libvirt/KVM without Proxmox, the fastest path to a running VM:

```bash
# Download a Debian cloud image and resize it
wget -O /var/lib/libvirt/images/myvm.qcow2 \
  https://cloud.debian.org/images/cloud/bookworm/latest/debian-12-generic-amd64.qcow2
qemu-img resize /var/lib/libvirt/images/myvm.qcow2 20G

# Boot from the cloud image with cloud-init
virt-install --name myvm --ram 2048 --vcpus 2 --cpu host \
  --disk path=/var/lib/libvirt/images/myvm.qcow2,bus=virtio \
  --network network=default,model=virtio \
  --cloud-init user-data=user-data.yaml,meta-data=meta-data.yaml \
  --import --os-variant debian12 --noautoconsole
```

Build the cloud-init ISO with `cloud-localds cidata.iso user-data.yaml meta-data.yaml` and attach
it as a second disk, or use the `--cloud-init` flag shown above (virt-install 4.0+).

**Reusable template pattern:** keep the downloaded cloud image as a read-only golden image
(`/var/lib/libvirt/images/debian-13-template.qcow2`) and create each VM disk as a qcow2
overlay backed by it - `qemu-img create -f qcow2 -b debian-13-template.qcow2 -F qcow2
myvm.qcow2`. Overlays only store per-VM changes and boot in seconds. Regenerate the base
when you need a new OS minor. Validate first boot with `cloud-init status --wait` inside
the guest. Never set `password:` or `chpasswd:` with plaintext values in user-data - use
`ssh_authorized_keys` and rely on `lock_passwd: true` (the cloud-image default).

`virsh list --all` to confirm state; `virsh console myvm` to attach. For full XML domain
definitions, network and storage pool management, and virsh lifecycle commands, see
`references/libvirt-qemu-kvm.md`.

---

## Hypervisor Selection

| Hypervisor | Type | Best for | Avoid when |
|------------|------|----------|------------|
| **Proxmox VE** | Type 1 (KVM+LXC) | Homelab, SMB, API-driven automation | Need VMware ecosystem tooling |
| **libvirt/KVM** | Type 1 (bare) | Custom setups, OpenStack, direct control | Want a GUI or clustering OOB |
| **XCP-ng** | Type 1 (Xen) | Xen-based infra, XenOrchestra UI | KVM-specific features (virtio-fs) |
| **VMware ESXi** | Type 1 | Enterprise with existing VMware investment | Post-Broadcom: licensing costs exploded |
| **VirtualBox** | Type 2 | Dev workstations, testing | Production. Ever. |

**VMware post-Broadcom (2026):** Broadcom acquired VMware (closed Nov 2023). Perpetual
licenses eliminated, subscription-only model, free ESXi discontinued then partially
reinstated (ESXi 8.0 U3e "free hypervisor", April 2025). Many organizations are
migrating to Proxmox or XCP-ng. The migration path from VMware is well-documented
but non-trivial for large estates.

---

## Reference Files

- `references/proxmox.md` - Proxmox VE deep-dive: API, CLI, storage, clustering, HA,
  live migration, PCI passthrough, Proxmox Backup Server, and Terraform (bpg/proxmox
  provider patterns, lifecycle gotchas, cloud-init)
- `references/libvirt-qemu-kvm.md` - libvirt/QEMU/KVM: virsh commands, XML domain
  definitions, QEMU command-line, KVM modules, disk formats, networking
- `references/image-building.md` - Packer templates, cloud-init configuration,
  cloud image workflows, template management
- `references/gotchas.md` - Battle-tested pitfalls and failure modes from production
  Proxmox/KVM environments. Read this before any non-trivial change.

---

## Output Contract

See `skills/_shared/output-contract.md` for the full contract.

- **Skill name:** VIRTUALIZATION
- **Deliverable bucket:** `audits`
- **Mode:** conditional. When invoked to **analyze, review, audit, or improve** existing repo content, emit the full contract - boxed inline header, body summary inline plus per-finding detail in the deliverable file, boxed conclusion, conclusion table - and write the deliverable to `docs/local/audits/virtualization/<YYYY-MM-DD>-<slug>.md`. When invoked to **answer a question, teach a concept, build a new artifact, or generate content**, respond freely without the contract.
- **Severity scale:** `P0 | P1 | P2 | P3 | info` (see shared contract; only used in audit/review mode).

## Related Skills

- **terraform** - owns HCL patterns, module design, state management. This skill owns
  Proxmox-specific provider patterns (bpg/proxmox lifecycle rules, cloud-init interface,
  disk resize workarounds). Use terraform for general IaC; this skill for Proxmox-specific
  Terraform.
- **kubernetes** - for container orchestration running on top of VMs. This skill provisions
  the VM infrastructure; kubernetes manages what runs inside the cluster.
- **networking** - for network config not specific to hypervisors (DNS, VPNs, reverse
  proxies, nftables). This skill covers VM networking (bridges, VLANs, virtio-net).
- **ansible** - for day-2 configuration of VMs after provisioning. This skill creates the
  VM; ansible configures what runs on it.
- **docker** - for container image optimization. This skill manages VMs that may host
  Docker/container workloads.

---

## Rules

These are non-negotiable. Violating any of these is a bug.

1. **virtio for everything.** Disk (virtio-scsi), network (virtio-net). IDE and e1000 are
   for legacy OS compatibility only.
2. **CPU type `host` in production.** Emulated types hide features. Only use emulated types
   for live migration across heterogeneous CPU generations.
3. **Stop/start for hardware changes, not reboot.** Guest reboot doesn't restart QEMU. Disk,
   memory, and device config changes need `qm stop` + `qm start`.
4. **No disk resize via Terraform.** Use `qm resize` on host, growpart/resize2fs in guest,
   then update the Terraform variable.
5. **Disable ballooning by default.** Enable only after testing on the specific guest OS.
6. **Monitor thin pool data_percent.** Alert at 80%, critical at 90%. At 100%, all I/O fails.
7. **nohup for long migrations.** SSH disconnect kills foreground `qm migrate`.
8. **`prevent_destroy` + `ignore_changes` on Terraform VMs.** Protect disk and node_name
   from accidental destruction and migration drift.
9. **Run the AI self-check.** Every generated VM config gets verified against the checklist
   above before returning.
10. **Test before production.** New VM configs, passthrough setups, storage backends - test
    on a non-critical VM first.
