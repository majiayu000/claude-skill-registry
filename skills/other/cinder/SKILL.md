---
name: openstack-cinder
description: "OpenStack Cinder block storage service. Provides persistent volume management for cloud instances including volume creation, snapshots, backups, LVM/iSCSI backend, volume types with QoS, encryption (LUKS), volume migration, and multi-backend support. Use for deploying, configuring, operating, and troubleshooting OpenStack block storage."
user-invocable: true
allowed-tools: Read Grep Glob
metadata:
  extensions:
    gsd-skill-creator:
      version: 1
      createdAt: "2026-02-23"
      triggers:
        intents:
          - "cinder"
          - "volume"
          - "block storage"
          - "snapshot"
          - "backup"
          - "LVM"
          - "iSCSI"
          - "volume type"
          - "storage backend"
        contexts:
          - "deploying openstack storage"
          - "managing volumes"
          - "troubleshooting storage"
          - "configuring storage backends"
---

# OpenStack Cinder -- Block Storage Service

Cinder provides persistent block storage volumes that attach to Nova compute instances. Unlike ephemeral storage (which disappears when an instance is deleted), Cinder volumes persist independently of the instance lifecycle. They can be detached from one instance and reattached to another, snapshotted for point-in-time copies, and backed up for disaster recovery.

## Architecture

Cinder uses a **backend driver architecture** that abstracts the underlying storage technology. The storage backend handles the actual block device operations while Cinder provides a uniform API.

- **LVM/iSCSI backend:** The default for single-node deployments. Cinder creates logical volumes in an LVM volume group and exports them over iSCSI to the compute host. Simple, well-understood, and requires no external storage infrastructure.
- **Ceph (RBD) backend:** The standard for multi-node production deployments. Cinder creates RBD images in a Ceph pool. Provides replication, snapshots, and thin provisioning natively.
- **NFS backend:** Mounts NFS shares and creates volume files on them. Useful for environments with existing NFS infrastructure.

**Service components:**

- `cinder-api`: Receives REST API requests and routes them to the scheduler.
- `cinder-scheduler`: Selects the appropriate backend and volume node for each operation using configurable filters and weighers.
- `cinder-volume`: Manages the actual volume lifecycle on the backend. One instance per backend.
- `cinder-backup`: Handles volume backup and restore operations to a backup target (Swift, NFS, Ceph).

## Deploy

### Kolla-Ansible Configuration

Key settings in `globals.yml`:

```yaml
# Enable Cinder
enable_cinder: "yes"

# Enable backup service (optional but recommended)
enable_cinder_backup: "yes"

# LVM backend configuration
cinder_volume_group: "cinder-volumes"

# Backup target (Swift is the default when Swift is enabled)
# cinder_backup_driver: "swift"
# cinder_backup_driver: "nfs"
```

### LVM Volume Group Setup

Before deploying Cinder with the LVM backend, create the volume group:

```bash
# Identify available disk or partition (e.g., /dev/sdb)
lsblk

# Create a physical volume
pvcreate /dev/sdb

# Create the volume group (name must match cinder_volume_group)
vgcreate cinder-volumes /dev/sdb

# Verify
vgs
# Should show cinder-volumes with available space
```

If using a loop device for testing (not recommended for production):

```bash
# Create a backing file
dd if=/dev/zero of=/var/lib/cinder/cinder-volumes.img bs=1M count=20480
losetup /dev/loop0 /var/lib/cinder/cinder-volumes.img
pvcreate /dev/loop0
vgcreate cinder-volumes /dev/loop0
```

### Container Verification

```bash
# List Cinder containers
docker ps --format '{{.Names}}' | grep cinder

# Expected containers:
# cinder_api, cinder_scheduler, cinder_volume, cinder_backup (if enabled)

# Check volume service status
openstack volume service list
# All services should show "up" and "enabled"
```

## Configure

### Volume Types and Extra Specs

Volume types define storage classes with specific capabilities. Extra specs control backend behavior.

```bash
# Create a volume type for the LVM backend
openstack volume type create lvm-standard
openstack volume type set lvm-standard --property volume_backend_name=lvm-1

# Create a high-performance type with IOPS limits
openstack volume type create lvm-performance
openstack volume type set lvm-performance \
  --property volume_backend_name=lvm-1 \
  --property provisioning:type=thick

# Set default volume type
openstack volume type set lvm-standard --property is_default=true
```

### QoS Policies

```bash
# Create a QoS spec
openstack volume qos create standard-qos \
  --consumer front-end \
  --property read_iops_sec=1000 \
  --property write_iops_sec=500 \
  --property total_bytes_sec=104857600

# Associate QoS with a volume type
openstack volume qos associate standard-qos lvm-standard
```

### Volume Encryption

Cinder supports volume encryption using LUKS (dm-crypt). Requires Nova to have the `os-brick` encryption connector configured.

```bash
# Create an encryption type for a volume type
openstack volume type create encrypted-volumes
openstack volume type set encrypted-volumes --encryption-provider luks \
  --encryption-cipher aes-xts-plain64 \
  --encryption-key-size 256 \
  --encryption-control-location front-end
```

**Note:** Volume encryption requires Barbican (key management) or a static key in `cinder.conf`. For single-node lab deployments, a static key is simpler but less secure.

### Backend Configuration

The LVM backend is configured through Kolla-Ansible's `cinder-volume.conf` override:

```ini
[lvm-1]
volume_driver = cinder.volume.drivers.lvm.LVMVolumeDriver
volume_group = cinder-volumes
volume_backend_name = lvm-1
target_protocol = iscsi
target_helper = lioadm
```

### Oversubscription Ratios

Control how much virtual capacity Cinder can allocate beyond physical capacity:

```ini
# In cinder.conf or volume backend section
max_over_subscription_ratio = 1.0    # No oversubscription (safe default)
# max_over_subscription_ratio = 2.0  # Allow 2x oversubscription for thin provisioning
```

## Operate

### Volume CRUD

```bash
# Create a volume
openstack volume create --size 10 my-volume

# Create from an image (bootable volume)
openstack volume create --size 20 --image cirros --bootable boot-volume

# List volumes
openstack volume list

# Show volume details
openstack volume show my-volume

# Delete a volume (must be detached and not in use)
openstack volume delete my-volume
```

### Attach and Detach

```bash
# Attach a volume to an instance
openstack server add volume my-instance my-volume

# Check attachment
openstack volume show my-volume -c attachments

# Detach
openstack server remove volume my-instance my-volume
```

### Snapshot Management

```bash
# Create a snapshot (volume can be in-use if force is specified)
openstack volume snapshot create --volume my-volume my-snapshot

# Create a volume from a snapshot
openstack volume create --snapshot my-snapshot --size 10 restored-volume

# List and delete snapshots
openstack volume snapshot list
openstack volume snapshot delete my-snapshot
```

### Volume Backup and Restore

```bash
# Create a backup (requires cinder-backup service)
openstack volume backup create my-volume --name my-backup

# Restore a backup to a new volume
openstack volume backup restore my-backup restored-volume

# List backups
openstack volume backup list
```

### Extending Volumes

```bash
# Extend a volume (can be done while attached in some backends)
openstack volume set --size 20 my-volume

# Note: The filesystem inside the instance must be resized separately
# For ext4: resize2fs /dev/vdb
# For XFS: xfs_growfs /mountpoint
```

### Transfer Volumes Between Projects

```bash
# Initiate transfer (source project)
openstack volume transfer request create my-volume --name transfer-1
# Note the transfer ID and auth key

# Accept transfer (destination project)
openstack volume transfer request accept <transfer-id> <auth-key>
```

### Force-Detach Stuck Volumes

```bash
# Reset volume state if stuck in "attaching" or "detaching"
openstack volume set --state available my-volume

# Force-detach from all instances
cinder reset-state --state available --attach-status detached my-volume
```

## Troubleshoot

### Volume Stuck in Creating/Deleting State

**Symptoms:** Volume shows "creating" or "deleting" status indefinitely.

**Diagnostic sequence:**

1. **Check cinder-volume logs:** `docker logs cinder_volume 2>&1 | tail -50`. Look for errors about LVM commands or iSCSI target creation failures.
2. **Check volume group space:** `vgs cinder-volumes`. If VFree is 0, no space to create volumes.
3. **Check LVM directly:** `lvs cinder-volumes`. Look for the logical volume corresponding to the Cinder volume UUID.
4. **Reset state if needed:** `openstack volume set --state error <volume>` then delete, or `openstack volume set --state available <volume>` if the underlying LV exists.
5. **Check iSCSI target:** `targetcli ls` to see if the iSCSI target was created but Cinder lost track of it.

### Volume Attach Failures

**Symptoms:** `openstack server add volume` fails or times out; instance does not see the block device.

**Diagnostic sequence:**

1. **Check iSCSI initiator (compute host):** `iscsiadm -m session` to list active iSCSI sessions. If the volume target is not connected, check `iscsid` service.
2. **Check target availability:** `targetcli ls` on the volume host. The target should be listed with the correct LUN.
3. **Check Nova compute logs:** `docker logs nova_compute 2>&1 | grep <volume-id>`. Look for os-brick connector errors.
4. **Check multipath (if configured):** `multipath -ll`. Misconfigured multipath can cause attach failures or device conflicts.
5. **Check device busy:** If a previous detach did not clean up, the device may still be in use. Check `lsblk` and `dmsetup ls` for stale mappings.

### Snapshot Failures

**Symptoms:** Snapshot creation fails or produces a zero-size snapshot.

**Diagnostic sequence:**

1. **Check VG space:** Snapshots (LVM COW) consume space from the volume group. `vgs cinder-volumes` to check free space.
2. **COW overflow:** If the volume changes faster than the snapshot can track, the COW snapshot becomes invalid. Check `lvs` for snapshot status (should show active, not "invalid").
3. **Volume in use:** Some backends require the volume to be detached for consistent snapshots. Check `openstack volume show <volume> -c status`.
4. **Check cinder-volume logs:** `docker logs cinder_volume 2>&1 | grep snapshot`. Look for LVM errors.

### Backup Failures

**Symptoms:** Backup creation fails, times out, or backup service is not available.

**Diagnostic sequence:**

1. **Check backup service:** `openstack volume service list | grep backup`. Must show status "up" and state "enabled".
2. **Check backup container:** `docker ps | grep cinder_backup`. If not running, check `docker logs cinder_backup`.
3. **Check backup storage:** If backing up to Swift, verify Swift is operational. If NFS, verify the NFS mount is accessible.
4. **Check space:** Backup target must have sufficient space. For Swift: `openstack object store account show`. For NFS: `df -h <nfs-mount>`.
5. **Check cinder-backup logs:** `docker logs cinder_backup 2>&1 | tail -50`.

### Volume Group Not Found

**Symptoms:** cinder-volume fails to start or reports "VG cinder-volumes not found."

**Diagnostic sequence:**

1. **Check VG exists:** `vgs` on the host. If `cinder-volumes` is not listed, it was never created or the disk failed.
2. **Check VG name match:** Compare `cinder_volume_group` in `globals.yml` with the actual VG name. They must match exactly.
3. **Check physical volume:** `pvs` to verify the underlying disk/partition is still a PV. Disk failure or partition table changes can remove PV metadata.
4. **Loop device (if used):** Check `losetup -l` to verify the loop device is still attached. Loop devices do not persist across reboots without explicit configuration.
5. **Recreate if needed:** `pvcreate /dev/<disk> && vgcreate cinder-volumes /dev/<disk>`. Warning: this destroys any existing data on the device.

## Integration Points

- **Keystone:** All Cinder API calls require Keystone authentication. Cinder registers `volumev3` service and endpoint in the Keystone catalog. Service user `cinder` authenticates for internal operations.
- **Nova:** Nova uses os-brick to connect Cinder volumes to instances. When `openstack server add volume` is called, Nova coordinates with Cinder to export the volume (iSCSI target) and connect it to the hypervisor (iSCSI initiator). The `nova-compute` service must have access to the iSCSI network.
- **Glance:** Cinder can create bootable volumes directly from Glance images (`openstack volume create --image`). Glance can also use Cinder as a backend store for image data.
- **Swift:** When `cinder_backup_driver: swift` is configured, Cinder stores volume backups as objects in Swift containers. This provides object-level redundancy for backup data.

## NASA SE Cross-References

| SE Phase | Cinder Activity | Reference |
|----------|----------------|-----------|
| Phase B (Preliminary Design) | Design storage backend: LVM vs Ceph trade study. Plan volume group sizing. Define volume types and QoS requirements. Design backup strategy. | SP-6105 SS 4.3-4.4 |
| Phase C (Final Design & Build) | Create LVM volume group. Configure `globals.yml` storage parameters. Define volume types and encryption policies. Configure backup target. | SP-6105 SS 5.1 |
| Phase D (Integration & Test) | Verify volume creation, attachment to instances, snapshot operations, and backup/restore cycle. Test volume resize. Verify bootable volume creation from Glance images. | SP-6105 SS 5.2-5.3 |
| Phase E (Operations) | Day-2 volume management: provision volumes, manage snapshots and backups, handle stuck volumes, monitor VG capacity, transfer volumes between projects, extend volumes. | SP-6105 SS 5.4-5.5 |
