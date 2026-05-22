---
name: frappe-ops-backup
description: >
  Use when configuring backups, restoring sites, encrypting backup files, scheduling automated backups, or planning disaster recovery.
  Prevents data loss from missing backups, failed restores, and unencrypted sensitive data.
  Covers bench backup, bench restore, backup encryption, S3/remote storage, scheduled backups, disaster recovery procedures.
  Keywords: backup, restore, encryption, S3, scheduled backup, disaster recovery, bench backup, bench restore.
license: MIT
compatibility: "Claude Code, Claude.ai Projects, Claude API. Frappe v14-v16."
metadata:
  author: OpenAEC-Foundation
  version: "2.0"
---

# Backup & Disaster Recovery

Frappe provides built-in backup and restore commands via bench. ALWAYS back up before updates, migrations, or any destructive operation. A backup that has never been test-restored is NOT a backup.

## Quick Reference

```bash
# Database-only backup (default)
bench backup

# Full backup with public + private files
bench backup --with-files

# Backup specific site
bench --site mysite.com backup --with-files

# Backup with compression (.tgz instead of .tar)
bench backup --with-files --compress

# Backup only specific DocTypes
bench backup --only "Sales Invoice,Purchase Invoice"

# Backup excluding specific DocTypes
bench backup --exclude "Error Log,Activity Log"

# Custom backup path
bench backup --backup-path /mnt/backups/

# Restore from backup
bench --site mysite.com restore /path/to/backup.sql.gz

# Restore with files
bench --site mysite.com restore /path/to/backup.sql.gz \
    --with-public-files /path/to/files.tar \
    --with-private-files /path/to/private-files.tar

# Setup automated backups (cron)
bench setup backups
```

### What Gets Backed Up

| Component | Default | With --with-files | Location |
|---|---|---|---|
| Database (SQL dump) | YES | YES | `sites/{site}/private/backups/` |
| Site config | YES | YES | `sites/{site}/private/backups/` |
| Public files | NO | YES | `sites/{site}/public/files/` |
| Private files | NO | YES | `sites/{site}/private/files/` |

**Backup file naming**: `{datetime}_{hash}_{site}-database.sql.gz`

---

## Backup Decision Tree

```
What do you need to back up?
|
+-- Quick database snapshot before a change?
|   +-- bench backup (database only, fast)
|
+-- Full backup before upgrade or migration?
|   +-- bench backup --with-files --compress
|
+-- Automated daily backups?
|   +-- bench setup backups (cron-based)
|   +-- OR S3 Backup Settings (cloud storage)
|
+-- Offsite / cloud backup?
|   +-- S3 Backup Settings DocType (built-in)
|   +-- OR custom script with rclone/aws-cli
|
+-- Partial backup (specific DocTypes)?
|   +-- bench backup --only "DocType1,DocType2"
|
+-- Disaster recovery?
|   +-- Full backup + files + tested restore procedure
|   +-- See Disaster Recovery section below
```

---

## bench backup — All Options

```bash
bench backup [OPTIONS]

# Path options
--backup-path PATH              # Save all backup files to this directory
--backup-path-db PATH           # Custom path for database dump
--backup-path-conf PATH         # Custom path for site config backup
--backup-path-files PATH        # Custom path for public files archive
--backup-path-private-files PATH # Custom path for private files archive

# Filter options
--only, --include, -i DOCTYPES  # Include ONLY these DocTypes (comma-separated)
--exclude, -e DOCTYPES          # Exclude these DocTypes (comma-separated)
--ignore-backup-conf            # Ignore include/exclude from site config

# Flags
--with-files                    # Include public and private files
--compress                      # Use .tgz format (gzip compressed tar)
--verbose                       # Show detailed output
```

**Safety feature**: If backup fails (any exception), partial files are automatically deleted to avoid consuming disk space with incomplete backups.

---

## bench restore — All Options

```bash
bench --site [site-name] restore [OPTIONS] SQL_FILE_PATH

# SQL_FILE_PATH: path to .sql or .sql.gz file
# Can be relative to sites/ directory or absolute path

# Options
--db-root-username USERNAME     # MariaDB/PostgreSQL root username
--db-root-password PASSWORD     # MariaDB/PostgreSQL root password
--db-name NAME                  # Use custom database name
--admin-password PASSWORD       # Set administrator password after restore
--install-app APP_NAME          # Install app after restore
--with-public-files PATH        # Restore public files (.tar or .tgz)
--with-private-files PATH       # Restore private files (.tar or .tgz)

# Flags
--force                         # Bypass downgrade warnings (NOT recommended)
```

**CRITICAL**: Downgrades are NOT supported. Restoring a backup from a newer version onto an older version triggers a warning. NEVER use `--force` to bypass this unless you understand the consequences.

---

## Automated Backups

### Cron-Based (bench setup backups)

```bash
# Sets up daily backup cron job
bench setup backups

# This adds to crontab:
# 0 */6 * * * cd /home/frappe/frappe-bench && bench backup --with-files
```

### S3 Backup Settings (Built-in DocType)

Configure in ERPNext: **Settings > S3 Backup Settings**

| Field | Description |
|---|---|
| Enable | Toggle automated S3 backups |
| S3 Bucket Name | Target bucket |
| AWS Access Key ID | IAM credentials |
| AWS Secret Access Key | IAM secret |
| Region | AWS region (e.g., eu-west-1) |
| Frequency | Daily, Weekly |
| Backup Files | Include public/private files |

```python
# Programmatic S3 backup trigger
from frappe.integrations.offsite_backup_utils import send_email
import frappe

# The S3 backup runs via scheduled job when enabled
# To trigger manually:
from frappe.integrations.doctype.s3_backup_settings.s3_backup_settings import take_backups_s3
take_backups_s3()
```

### Custom Backup Script

```bash
#!/bin/bash
# custom-backup.sh — Daily backup with rotation and offsite copy
set -e

BENCH_DIR="/home/frappe/frappe-bench"
BACKUP_DIR="/mnt/backups/frappe"
RETENTION_DAYS=30
S3_BUCKET="s3://my-frappe-backups"
DATE=$(date +%Y-%m-%d_%H%M)

cd $BENCH_DIR

# Create backup
bench backup --with-files --compress --backup-path "$BACKUP_DIR/$DATE/"

# Sync to S3
aws s3 sync "$BACKUP_DIR/$DATE/" "$S3_BUCKET/$DATE/"

# Remove local backups older than retention period
find "$BACKUP_DIR" -type d -mtime +$RETENTION_DAYS -exec rm -rf {} +

# Verify latest backup exists on S3
aws s3 ls "$S3_BUCKET/$DATE/" || echo "WARNING: S3 sync failed!"
```

---

## Backup Encryption

### Encrypt Backups at Rest

```bash
# Encrypt backup with GPG (symmetric)
bench backup --with-files --compress
gpg --symmetric --cipher-algo AES256 \
    sites/mysite/private/backups/latest-database.sql.gz

# Decrypt for restore
gpg --decrypt backup.sql.gz.gpg > backup.sql.gz
bench --site mysite.com restore backup.sql.gz
```

### Encrypt with OpenSSL

```bash
# Encrypt
openssl enc -aes-256-cbc -salt -pbkdf2 \
    -in backup.sql.gz -out backup.sql.gz.enc

# Decrypt
openssl enc -d -aes-256-cbc -pbkdf2 \
    -in backup.sql.gz.enc -out backup.sql.gz
```

ALWAYS store encryption keys/passwords separately from backups. NEVER store the decryption key in the same location as the encrypted backup.

---

## Restore Procedures

### Full Site Restore

```bash
# 1. Stop services (traditional deployment)
sudo supervisorctl stop all

# 2. Restore database
bench --site mysite.com restore \
    /path/to/20240115_backup-database.sql.gz \
    --db-root-password YOUR_DB_ROOT_PASSWORD \
    --admin-password NEW_ADMIN_PASSWORD

# 3. Restore files
bench --site mysite.com restore \
    /path/to/20240115_backup-database.sql.gz \
    --with-public-files /path/to/20240115_backup-files.tar \
    --with-private-files /path/to/20240115_backup-private-files.tar

# 4. Run migrations (if version differs)
bench --site mysite.com migrate

# 5. Clear cache
bench --site mysite.com clear-cache

# 6. Restart services
sudo supervisorctl start all
```

### Restore to New Site

```bash
# Create new site from backup (useful for staging/testing)
bench new-site staging.example.com \
    --db-root-password YOUR_DB_ROOT_PASSWORD \
    --admin-password STAGING_PASSWORD

bench --site staging.example.com restore \
    /path/to/production-backup.sql.gz \
    --with-public-files /path/to/files.tar \
    --with-private-files /path/to/private-files.tar

bench --site staging.example.com migrate
```

### Docker Restore

```bash
# Copy backup into container
docker cp backup.sql.gz frappe-backend:/tmp/

# Restore
docker compose exec backend \
    bench --site mysite.com restore /tmp/backup.sql.gz \
    --db-root-password $DB_ROOT_PASSWORD

# Cleanup
docker compose exec backend rm /tmp/backup.sql.gz
```

---

## Backup Verification

ALWAYS test restores regularly. A backup is only valid if it can be successfully restored.

```bash
#!/bin/bash
# verify-backup.sh — Test restore to verify backup integrity
set -e

BACKUP_SQL="/mnt/backups/frappe/latest/database.sql.gz"
TEST_SITE="backup-test.localhost"
BENCH_DIR="/home/frappe/frappe-bench"

cd $BENCH_DIR

# Create temporary test site
bench new-site $TEST_SITE --db-root-password $DB_ROOT_PASSWORD --admin-password test

# Restore backup
bench --site $TEST_SITE restore $BACKUP_SQL --db-root-password $DB_ROOT_PASSWORD

# Run basic verification
bench --site $TEST_SITE migrate
bench --site $TEST_SITE console <<'EOF'
import frappe
count = frappe.db.count("User")
print(f"User count: {count}")
assert count > 0, "No users found — backup may be corrupt"
print("Backup verification PASSED")
EOF

# Cleanup test site
bench drop-site $TEST_SITE --db-root-password $DB_ROOT_PASSWORD --force

echo "Backup verification complete"
```

---

## Multi-Site Backup Strategy

```bash
#!/bin/bash
# backup-all-sites.sh — Backup every site in the bench
set -e

BENCH_DIR="/home/frappe/frappe-bench"
cd $BENCH_DIR

for site in $(bench --site all list-apps 2>/dev/null | grep -oP '^\S+'); do
    echo "Backing up $site..."
    bench --site "$site" backup --with-files --compress
done
```

---

## Disaster Recovery Plan Template

```
1. PREVENTION
   - Automated daily backups (bench setup backups OR S3)
   - Offsite copies (S3, GCS, or remote server)
   - Encrypted backups for sensitive data
   - Backup retention: minimum 30 days

2. DETECTION
   - Monitor backup cron job (check /var/log/syslog)
   - Verify backup file sizes (alert if < expected)
   - Weekly automated restore test

3. RECOVERY (RTO target: < 4 hours)
   a. Provision new server (or use standby)
   b. Install Frappe/ERPNext (same version as backup)
   c. Restore from latest verified backup
   d. Run migrations
   e. Update DNS to point to new server
   f. Verify functionality

4. DOCUMENTATION
   - Backup locations and credentials
   - Encryption key storage (separate from backups)
   - Step-by-step restore procedure
   - Contact list for escalation
```

---

## Version Differences

| Feature | v14 | v15 | v16 |
|---|---|---|---|
| `--compress` flag | Yes | Yes | Yes |
| `--only` / `--exclude` | Yes | Yes | Yes |
| S3 Backup Settings | Yes | Yes | Yes |
| Site-level logs | v13+ | Yes | Yes |
| `partial-restore` command | No | Yes | Yes |

---

## Reference Files

| File | Contents |
|---|---|
| [examples.md](references/examples.md) | Complete backup/restore scripts |
| [anti-patterns.md](references/anti-patterns.md) | Common backup mistakes |
| [workflows.md](references/workflows.md) | Step-by-step backup workflows |

## Related Skills

- `frappe-ops-deployment` — Production deployment (includes backup in update workflow)
- `frappe-ops-performance` — Performance tuning
- `frappe-ops-bench` — Bench CLI reference
- `frappe-ops-upgrades` — Version upgrade procedures (backup required)
