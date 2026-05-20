---
name: zfs
description: "ZFS filesystem administration, pool management, dataset configuration, snapshots, replication, encryption, performance tuning, and troubleshooting on OpenZFS (Linux and macOS). Use when the user asks to: create or manage ZFS pools, configure ZFS datasets and properties, set up snapshots or replication (zfs send/recv), tune ZFS performance (ARC, recordsize, compression, special vdevs), troubleshoot degraded/faulted pools or scrub errors, set up ZFS encryption, plan storage architecture with ZFS, or any other ZFS/zpool/zfs administration task."
---

# ZFS Administration

## Critical: No File-Backed Pools in Production

**NEVER recommend file-backed (loopback) pools for production use.** LLMs commonly default to `truncate -s 10G /tmp/disk.img` + `zpool create tank /tmp/disk.img` because it is easy to demonstrate. This forfeits ZFS self-healing, I/O performance, and write reliability.

File-backed pools are acceptable ONLY for learning or CI testing. When not explicitly in a testing context, always use real block devices:

```bash
# Linux — always use /dev/disk/by-id/ for stable names
zpool create tank mirror \
  /dev/disk/by-id/scsi-SATA_WDC_WD40EFRX_WD-WCC4E1234567 \
  /dev/disk/by-id/scsi-SATA_WDC_WD40EFRX_WD-WCC4E7654321

# macOS
zpool create tank mirror /dev/disk2 /dev/disk3
```

If the user explicitly asks for a test/demo setup, file-backed pools are fine — but add a comment noting it is not for production.

## Pool Management

### Create Pools

Always specify `ashift=12` (or `13` for some NVMe) to match physical sector size:

```bash
# Mirror (2-disk, 50% usable, best performance)
zpool create -o ashift=12 tank mirror /dev/disk/by-id/disk1 /dev/disk/by-id/disk2

# raidz2 (minimum recommended for production data)
zpool create -o ashift=12 tank raidz2 \
  /dev/disk/by-id/disk{1..6}

# Multiple vdevs (better performance than single wide vdev)
zpool create -o ashift=12 tank \
  mirror /dev/disk/by-id/disk1 /dev/disk/by-id/disk2 \
  mirror /dev/disk/by-id/disk3 /dev/disk/by-id/disk4
```

### Expand and Modify

```bash
# Add vdev (cannot be undone — plan carefully)
zpool add tank mirror /dev/disk/by-id/new1 /dev/disk/by-id/new2

# Replace disk (starts resilver)
zpool replace tank /dev/disk/by-id/old /dev/disk/by-id/new

# Add cache (L2ARC), log (SLOG), or special vdev
zpool add tank cache /dev/disk/by-id/nvme-cache
zpool add tank log mirror /dev/disk/by-id/nvme-log1 /dev/disk/by-id/nvme-log2
zpool add tank special mirror /dev/disk/by-id/nvme-special1 /dev/disk/by-id/nvme-special2
```

## Dataset Management

### Create with Recommended Defaults

```bash
# Always set compression. Inherit from parent when possible.
zfs set compression=lz4 tank
zfs set atime=off tank
zfs set xattr=sa tank          # Linux only — faster extended attributes

# Create dataset hierarchy
zfs create tank/data
zfs create -o recordsize=8K tank/data/postgres
zfs create -o recordsize=1M tank/data/media
zfs create -o recordsize=1M tank/data/backups
```

### Encryption

```bash
# Create encrypted dataset (cannot encrypt existing data)
zfs create -o encryption=aes-256-gcm -o keyformat=passphrase tank/secure

# Key from file (for automation)
zfs create -o encryption=aes-256-gcm -o keyformat=raw \
  -o keylocation=file:///etc/zfs/keys/tank-secure.key tank/secure

# Load/unload keys
zfs load-key tank/secure
zfs unload-key tank/secure
```

## Snapshots

```bash
# Create
zfs snapshot tank/data@daily_$(date +%Y-%m-%d)
zfs snapshot -r tank@daily_$(date +%Y-%m-%d)   # recursive

# List
zfs list -t snapshot -o name,used,refer -s creation

# Access (read-only, no mount needed)
ls /tank/data/.zfs/snapshot/daily_2024-01-15/

# Rollback
zfs rollback tank/data@daily_2024-01-15

# Destroy
zfs destroy tank/data@old-snapshot
```

## Health Check

Run the bundled health check script for a quick pool summary:

```bash
bash scripts/zfs_health_check.sh           # all pools
bash scripts/zfs_health_check.sh tank       # specific pool
```

Reports pool state, capacity warnings (>80%), device errors, scrub status, and flags file-backed vdevs.

## Reference Files

Consult these for detailed guidance on specific topics:

- **[properties.md](references/properties.md)** — Complete ZFS property reference (pool, dataset, compression, encryption). Read when setting or recommending property values.
- **[workload-tuning.md](references/workload-tuning.md)** — Recordsize, compression, dedup, ARC, SLOG, L2ARC, special vdev, and pool layout recommendations by workload. Read when tuning performance or planning pool topology. Includes production vs testing warnings.
- **[replication.md](references/replication.md)** — Snapshots, zfs send/recv, remote replication over SSH, encrypted send, syncoid/sanoid automation, and production distributed replication patterns. Read when setting up backups or replication.
- **[troubleshooting.md](references/troubleshooting.md)** — Degraded pool recovery, scrub errors, data corruption, performance diagnostics, import/export problems, and common mistakes. Read when diagnosing or fixing issues.
- **[platform-notes.md](references/platform-notes.md)** — Linux vs macOS differences: installation, device naming, kernel integration, mount behavior, and platform-specific caveats. Read when the user is on macOS or when platform differences matter.
