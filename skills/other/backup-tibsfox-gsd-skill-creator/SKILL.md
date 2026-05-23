---
name: openstack-backup
description: "OpenStack backup operations skill for protecting cloud infrastructure through systematic backup strategies and disaster recovery procedures. Covers database backups (MariaDB full and incremental with mariabackup), configuration backups (globals.yml, inventory, Fernet keys), volume snapshots (Cinder LVM snapshots), image exports (Glance), instance snapshots (Nova), backup encryption (GPG/OpenSSL), retention policies (daily/weekly/monthly rotation), restore procedures (database point-in-time recovery, service rebuild), RPO/RTO planning, and disaster recovery drills. Use when planning backup strategy, scheduling automated backups, testing restore procedures, or executing disaster recovery."
user-invocable: true
allowed-tools: Read Grep Glob
metadata:
  extensions:
    gsd-skill-creator:
      version: 1
      createdAt: "2026-02-22"
      triggers:
        intents:
          - "backup"
          - "disaster recovery"
          - "snapshot"
          - "restore"
          - "recovery"
          - "data protection"
          - "backup schedule"
          - "retention"
        contexts:
          - "backing up openstack"
          - "disaster recovery planning"
          - "restoring from backup"
          - "snapshot management"
---

# OpenStack Backup Operations

A cloud without tested backups is a cloud waiting to lose data. Backup operations protect the entire stack -- from the databases that store state, to the configurations that define behavior, to the volumes that hold user data. The backup hierarchy ensures that any component can be recovered independently, from a single Keystone Fernet key to a complete cloud rebuild.

Backup planning starts with two numbers: **RPO (Recovery Point Objective)** -- how much data loss is acceptable (e.g., "no more than 1 hour of changes"), and **RTO (Recovery Time Objective)** -- how long recovery can take (e.g., "service restored within 4 hours"). These numbers drive every decision: backup frequency, storage location, retention depth, and automation investment.

In NASA SE terms, backup maps to **Phase E (Operations & Sustainment)** as a core sustainment activity, and **Phase F (Closeout)** for data archive procedures. The backup hierarchy follows the same defense-in-depth philosophy NASA applies to mission-critical data: multiple copies, multiple formats, verified recoverability.

## Deploy

### Backup Infrastructure Setup

**Backup scripts location:**

```bash
# Create backup directory structure
mkdir -p /opt/openstack-backups/{database,config,volumes,images,snapshots}
mkdir -p /opt/openstack-backups/scripts
mkdir -p /opt/openstack-backups/logs

# Set ownership and permissions
chown -R root:root /opt/openstack-backups
chmod 700 /opt/openstack-backups
```

**Kolla-Ansible built-in database backup:**

```bash
# MariaDB backup (built into Kolla-Ansible)
kolla-ansible -i inventory mariadb_backup

# Backup location: /var/lib/docker/volumes/mariadb/_data/backups/
# File: mysqlbackup-<timestamp>.qp.xb.gz
```

**Cron scheduling for automated backups:**

```bash
# /etc/cron.d/openstack-backup
# Daily database backup at 02:00
0 2 * * * root /opt/openstack-backups/scripts/backup-databases.sh >> /opt/openstack-backups/logs/db-backup.log 2>&1

# Daily config backup at 02:30
30 2 * * * root /opt/openstack-backups/scripts/backup-configs.sh >> /opt/openstack-backups/logs/config-backup.log 2>&1

# Weekly volume snapshots (Sunday 03:00)
0 3 * * 0 root /opt/openstack-backups/scripts/backup-volumes.sh >> /opt/openstack-backups/logs/volume-backup.log 2>&1
```

**Backup storage targets:**

| Target | Use Case | Configuration |
|--------|----------|---------------|
| Local disk | Fast restore, primary copy | `/opt/openstack-backups/` |
| NFS mount | Off-host copy, disaster recovery | Mount at `/mnt/backup-nfs/` |
| Swift (S3-compatible) | Object storage archive, long-term retention | Use `openstack object create` or s3cmd |

## Configure

### MariaDB Backup Strategy

**Full backup (weekly):**

```bash
#!/bin/bash
# backup-databases.sh -- full MariaDB backup with mariabackup
BACKUP_DIR="/opt/openstack-backups/database"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="${BACKUP_DIR}/full_${TIMESTAMP}"

# Use Kolla-Ansible's built-in backup
kolla-ansible -i /etc/kolla/inventory mariadb_backup

# Or manual mariabackup via container
docker exec mariadb mariabackup --backup \
  --target-dir=/backup/full_${TIMESTAMP} \
  --user=root --password=${DB_ROOT_PASSWORD}

echo "Full backup completed: ${BACKUP_FILE}" >> /opt/openstack-backups/logs/db-backup.log
```

**Incremental backup (daily, between full backups):**

```bash
# Incremental based on last full backup
LAST_FULL=$(ls -d ${BACKUP_DIR}/full_* | sort | tail -1)
docker exec mariadb mariabackup --backup \
  --target-dir=/backup/inc_${TIMESTAMP} \
  --incremental-basedir=${LAST_FULL} \
  --user=root --password=${DB_ROOT_PASSWORD}
```

### Service-Specific Backups

**RabbitMQ definitions export:**

```bash
# Export queue definitions, exchanges, bindings
docker exec rabbitmq rabbitmqctl export_definitions /tmp/rabbitmq_definitions.json
docker cp rabbitmq:/tmp/rabbitmq_definitions.json \
  /opt/openstack-backups/config/rabbitmq_definitions_$(date +%Y%m%d).json
```

**Keystone Fernet key backup:**

```bash
# Critical: Fernet keys are required to validate existing tokens
docker cp keystone_api:/etc/kolla/keystone/fernet-keys/ \
  /opt/openstack-backups/config/fernet-keys_$(date +%Y%m%d)/
```

**Cinder volume snapshot policies:**

```bash
# Create snapshot of all in-use volumes
for vol_id in $(openstack volume list --status in-use -f value -c ID); do
  openstack volume snapshot create --volume ${vol_id} \
    --description "Scheduled backup $(date +%Y%m%d)" \
    backup_${vol_id}_$(date +%Y%m%d)
done
```

**Glance image export:**

```bash
# Export critical images (base OS, golden images)
for image_id in $(openstack image list --status active -f value -c ID); do
  openstack image save --file /opt/openstack-backups/images/${image_id}.raw ${image_id}
done
```

**Nova instance snapshot:**

```bash
# Snapshot critical instances
openstack server image create --name "backup_$(date +%Y%m%d)" <instance-id>
```

### Configuration File Backup

```bash
#!/bin/bash
# backup-configs.sh -- backup all Kolla-Ansible configurations
BACKUP_DIR="/opt/openstack-backups/config/kolla_$(date +%Y%m%d)"
mkdir -p ${BACKUP_DIR}

# Core configuration files
cp /etc/kolla/globals.yml ${BACKUP_DIR}/
cp /etc/kolla/passwords.yml ${BACKUP_DIR}/
cp -r /etc/kolla/inventory ${BACKUP_DIR}/
cp /etc/kolla/admin-openrc.sh ${BACKUP_DIR}/

# Per-service configuration overrides
for svc in keystone nova neutron cinder glance swift heat horizon; do
  [ -d /etc/kolla/${svc} ] && cp -r /etc/kolla/${svc} ${BACKUP_DIR}/
done

# Encrypt sensitive files
gpg --symmetric --cipher-algo AES256 \
  --output ${BACKUP_DIR}/passwords.yml.gpg \
  ${BACKUP_DIR}/passwords.yml
rm ${BACKUP_DIR}/passwords.yml

echo "Config backup completed: ${BACKUP_DIR}"
```

### Backup Encryption

**GPG encryption for backup files:**

```bash
# Encrypt a backup file
gpg --symmetric --cipher-algo AES256 \
  --batch --passphrase-file /root/.backup-passphrase \
  --output backup.tar.gz.gpg backup.tar.gz

# Decrypt
gpg --decrypt --batch --passphrase-file /root/.backup-passphrase \
  --output backup.tar.gz backup.tar.gz.gpg
```

**OpenSSL alternative:**

```bash
# Encrypt
openssl enc -aes-256-cbc -salt -pbkdf2 \
  -in backup.tar.gz -out backup.tar.gz.enc \
  -pass file:/root/.backup-passphrase

# Decrypt
openssl enc -aes-256-cbc -d -pbkdf2 \
  -in backup.tar.gz.enc -out backup.tar.gz \
  -pass file:/root/.backup-passphrase
```

### Retention Policies

| Tier | Frequency | Retention | Storage Target |
|------|-----------|-----------|---------------|
| Daily | Every day at 02:00 | 7 days | Local disk |
| Weekly | Sunday 03:00 (full DB) | 4 weeks | NFS mount |
| Monthly | First Sunday of month | 12 months | Swift/S3 archive |

**Rotation script:**

```bash
# Purge backups older than retention period
find /opt/openstack-backups/database -name "*.gz" -mtime +7 -delete
find /mnt/backup-nfs/database -name "*.gz" -mtime +28 -delete
# Monthly backups on Swift are managed by object expiry headers
```

### Backup Storage Sizing

| Component | Typical Size | Growth Rate | 30-day Estimate |
|-----------|-------------|-------------|-----------------|
| MariaDB full | 500MB-2GB | ~50MB/day | ~3.5GB |
| MariaDB incremental | 50-200MB | Per day | ~4.2GB |
| Kolla configs | 10-50MB | Stable | ~50MB |
| Fernet keys | <1MB | Stable | <1MB |
| Volume snapshots | Varies by usage | Per volume | Plan per tenant |
| Glance images | 1-10GB per image | Per upload | Plan per image |

## Operate

### Scheduled Backup Verification

**Restore test procedure (monthly):**

```bash
# 1. Create isolated test database container
docker run -d --name mariadb_restore_test \
  -e MYSQL_ROOT_PASSWORD=testpass \
  mariadb:latest

# 2. Restore latest backup into test container
docker exec mariadb_restore_test mariabackup --prepare \
  --target-dir=/backup/latest_full

docker exec mariadb_restore_test mariabackup --copy-back \
  --target-dir=/backup/latest_full

# 3. Verify data integrity
docker exec mariadb_restore_test mysql -u root -ptestpass \
  -e "SELECT COUNT(*) FROM keystone.project; SELECT COUNT(*) FROM nova.instances;"

# 4. Clean up
docker rm -f mariadb_restore_test
```

### Disaster Recovery Drill Procedures

**Full restore from backup (complete cloud rebuild):**

1. Redeploy infrastructure: `kolla-ansible -i inventory bootstrap-servers`
2. Restore MariaDB from latest full + incremental backups
3. Restore Kolla configuration files from config backup
4. Deploy services: `kolla-ansible -i inventory deploy`
5. Restore Fernet keys (critical for existing tokens)
6. Verify all services: `openstack token issue`, `openstack service list`
7. Restore volume snapshots as needed
8. Verify user data access

**Partial service restore (single service rebuild):**

```bash
# Example: rebuild Nova after database corruption
# 1. Restore Nova database
docker exec -i mariadb mysql -u root -p nova < nova_backup.sql

# 2. Redeploy Nova only
kolla-ansible -i inventory deploy --tags nova

# 3. Verify
openstack server list  # Should show existing instances
openstack compute service list  # All services should be up
```

**Database point-in-time recovery:**

```bash
# 1. Prepare full backup
mariabackup --prepare --target-dir=/backup/full_base

# 2. Apply incrementals in order
mariabackup --prepare --target-dir=/backup/full_base \
  --incremental-dir=/backup/inc_001
mariabackup --prepare --target-dir=/backup/full_base \
  --incremental-dir=/backup/inc_002

# 3. Copy back to data directory
mariabackup --copy-back --target-dir=/backup/full_base
```

### Backup Catalog Maintenance

Maintain a catalog of all backups with metadata:

```bash
# Append to backup catalog after each successful backup
echo "$(date -u +%Y-%m-%dT%H:%M:%SZ),database,full,${BACKUP_FILE},$(du -sh ${BACKUP_FILE} | cut -f1),$(sha256sum ${BACKUP_FILE} | cut -d' ' -f1)" \
  >> /opt/openstack-backups/catalog.csv
```

Catalog format: `timestamp,type,level,path,size,checksum`

### Backup Rotation Execution

```bash
#!/bin/bash
# rotate-backups.sh -- enforce retention policies
DAILY_KEEP=7
WEEKLY_KEEP=28
MONTHLY_KEEP=365

# Remove old daily backups
find /opt/openstack-backups/database/daily -mtime +${DAILY_KEEP} -delete -print >> /opt/openstack-backups/logs/rotation.log

# Remove old weekly backups
find /opt/openstack-backups/database/weekly -mtime +${WEEKLY_KEEP} -delete -print >> /opt/openstack-backups/logs/rotation.log

# Update catalog
grep -v "DELETED" /opt/openstack-backups/catalog.csv > /opt/openstack-backups/catalog.csv.tmp
mv /opt/openstack-backups/catalog.csv.tmp /opt/openstack-backups/catalog.csv

echo "Rotation completed: $(date)" >> /opt/openstack-backups/logs/rotation.log
```

## Troubleshoot

### 1. MariaDB Backup Failure

**Symptoms:** `kolla-ansible mariadb_backup` exits non-zero. No backup file created.

| Cause | Diagnosis | Fix |
|-------|-----------|-----|
| Disk full | `df -h /var/lib/docker/volumes/mariadb/` shows >95% used | Free space: purge old backups, extend volume |
| Lock timeout | Backup log: `Lock wait timeout exceeded` | Retry during low-activity period; increase `innodb_lock_wait_timeout` |
| Connection refused | Backup log: `Can't connect to local MySQL server` | Verify MariaDB running: `docker ps --filter name=mariadb`; restart if needed |
| Insufficient privileges | Backup log: `Access denied` | Verify backup user has RELOAD, LOCK TABLES, PROCESS, REPLICATION CLIENT grants |

### 2. Volume Snapshot Stuck in "creating" State

**Symptoms:** `openstack volume snapshot list` shows status "creating" indefinitely.

| Cause | Diagnosis | Fix |
|-------|-----------|-----|
| Cinder backend issue | `docker logs cinder_volume 2>&1 \| tail -50` | Check LVM: `lvs` for snapshot overflow; extend VG if needed |
| LVM snapshot overflow | `lvs -o lv_name,snap_percent` shows >100% | Delete overflow snapshot: `openstack volume snapshot delete <id> --force`; increase snapshot reserve |
| iSCSI target locked | `iscsiadm -m session` shows stale sessions | Clear stale sessions; restart target service |
| Cinder volume service down | `openstack volume service list` shows disabled | Enable service: `openstack volume service set --enable <host> cinder-volume` |

### 3. Restore Fails

**Symptoms:** Backup restoration exits with errors. Database or service does not come up cleanly.

| Cause | Diagnosis | Fix |
|-------|-----------|-----|
| Incompatible backup version | mariabackup: `This backup is from a different version` | Restore using matching mariabackup version; or use mysqldump (logical backup) |
| Corrupted backup | mariabackup --prepare fails with checksum error | Use previous backup; verify checksums before relying on backups |
| Missing encryption key | gpg: `decryption failed: No secret key` | Locate key file; restore from secure key backup location |
| Filesystem permission mismatch | Service fails to start after restore: `Permission denied` | `chown -R mysql:mysql /var/lib/mysql/`; verify container user mapping |

### 4. Backup Storage Full

**Symptoms:** Backup scripts fail with "No space left on device". Retention not enforced.

| Cause | Diagnosis | Fix |
|-------|-----------|-----|
| Retention not enforced | Old backups still present: `find /opt/openstack-backups -mtime +30 -ls` | Run rotation script manually; fix cron schedule |
| Unexpected growth | Single large backup: `du -sh /opt/openstack-backups/*` | Investigate cause (large DB tables, uncompressed backups); add compression |
| NFS mount disconnected | `df -h /mnt/backup-nfs/` shows local mount | Remount NFS; check network connectivity to NFS server |

### 5. Incremental Backup Chain Broken

**Symptoms:** Cannot restore because intermediate incremental backup is missing or corrupted.

| Cause | Diagnosis | Fix |
|-------|-----------|-----|
| Missing parent backup | `mariabackup --prepare` fails: `missing incremental base` | Start new full backup; rebuild incremental chain from new base |
| Backup file corrupted | Checksum mismatch in catalog | Use last known-good full backup; accept data loss to RPO of that backup |
| Catalog out of sync | Backup files exist but catalog references wrong paths | Rebuild catalog from filesystem: scan backup directories and regenerate |

## Integration Points

Backup connects to every data-bearing component of the cloud stack:

**Core OpenStack services:** Backs up databases and configuration files for all 8 services. Each service's database (keystone, nova, neutron, cinder, glance, swift, heat, horizon) is included in the MariaDB backup set. Service-specific configs are backed up from `/etc/kolla/<service>/`.

**Monitoring skill:** Backup job success/failure metrics feed Prometheus alerting. Monitoring tracks backup duration, storage consumption, and schedule adherence. Alert on backup failures or missed backup windows.

**Security skill:** Backup encryption protects sensitive data at rest (passwords.yml, Fernet keys, database dumps). Credential backup requires secure storage with access controls. Security audit includes backup access review.

**Capacity skill:** Backup storage consumption is included in capacity planning models. Growth rate of backup storage drives storage provisioning decisions.

**Kolla-ansible-ops skill:** Backup is a prerequisite before upgrade and reconfigure operations. The upgrade procedure mandates a verified backup before any destructive changes. `kolla-ansible mariadb_backup` is the first step in upgrade runbooks.

## NASA SE Cross-References

| SE Phase | Backup Activity | Reference |
|----------|-----------------|-----------|
| Phase B (Preliminary Design) | Define backup requirements: RPO/RTO targets, storage requirements, retention policies | SP-6105 SS 4.3-4.4 |
| Phase E (Operations & Sustainment) | Execute backup schedules, verify restore procedures, maintain backup catalog, conduct DR drills | SP-6105 SS 5.4-5.5 |
| Phase E (Technical Data Management) | Backup as data management activity: ensure all operational data is recoverable per retention policy | SP-6105 SS 6.5 |
| Phase F (Closeout) | Data archive procedures: export and archive all cloud data before decommission, verify archive integrity | SP-6105 SS 6.1 |
