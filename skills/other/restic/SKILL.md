---
name: restic
description: >-
  Back up and restore data with Restic. Use when a user asks to set up backups,
  create encrypted backups, back up to S3 or cloud storage, implement a backup
  strategy, restore files from backup, deduplicate backup storage, schedule
  automated backups, back up databases or servers, or set up offsite backups.
  Covers repository initialization, backup/restore operations, snapshot
  management, pruning, encryption, and multiple storage backends (local, S3,
  SFTP, B2, Azure, GCS).
license: Apache-2.0
compatibility: 'Linux, macOS, Windows'
metadata:
  author: terminal-skills
  version: 1.0.0
  category: devops
  tags:
    - restic
    - backup
    - restore
    - encryption
    - deduplication
    - s3
---

# Restic

## Overview

Restic is a fast, secure, and efficient backup program. Every backup is encrypted (AES-256) and deduplicated at the block level, meaning only changed data is stored on subsequent runs. It supports multiple storage backends: local disk, SFTP, S3-compatible storage (AWS, MinIO, Backblaze B2), Azure Blob, Google Cloud Storage, and more. This skill covers repository setup, backup and restore operations, snapshot management, retention policies, and automation.

## Instructions

### Step 1: Installation

```bash
# Ubuntu/Debian
sudo apt install restic

# macOS
brew install restic

# Binary (any Linux)
curl -L https://github.com/restic/restic/releases/latest/download/restic_0.17.3_linux_amd64.bz2 | bunzip2 > /usr/local/bin/restic
chmod +x /usr/local/bin/restic

# Verify
restic version
```

### Step 2: Initialize Repository

```bash
# Local repository
restic init --repo /backups/myrepo

# S3 (AWS or S3-compatible like MinIO)
export AWS_ACCESS_KEY_ID=your-key
export AWS_SECRET_ACCESS_KEY=your-secret
restic init --repo s3:s3.amazonaws.com/my-bucket/restic-repo

# MinIO (self-hosted S3)
restic init --repo s3:http://minio.local:9000/backups/restic-repo

# SFTP
restic init --repo sftp:user@backup-server:/data/restic-repo

# Backblaze B2
export B2_ACCOUNT_ID=your-account
export B2_ACCOUNT_KEY=your-key
restic init --repo b2:my-bucket:restic-repo

# The init command generates a repository password — store it securely!
# Or set it explicitly:
export RESTIC_PASSWORD="your-encryption-password"
restic init --repo /backups/myrepo
```

### Step 3: Create Backups

```bash
# Back up a directory
restic -r /backups/myrepo backup /home/user/documents

# Back up multiple paths
restic -r /backups/myrepo backup /home/user/documents /var/www /etc

# Exclude patterns
restic -r /backups/myrepo backup /home/user \
  --exclude="*.tmp" \
  --exclude=".cache" \
  --exclude="node_modules" \
  --exclude=".git"

# Exclude from file
cat > /etc/restic/excludes.txt << 'EOF'
*.tmp
*.log
.cache
node_modules
__pycache__
.git
EOF
restic -r /backups/myrepo backup /home/user --exclude-file=/etc/restic/excludes.txt

# Back up with tags (for organization)
restic -r /backups/myrepo backup /var/www --tag web --tag production

# Back up stdin (database dumps)
pg_dump mydb | restic -r /backups/myrepo backup --stdin --stdin-filename db_dump.sql
mysqldump mydb | restic -r /backups/myrepo backup --stdin --stdin-filename mysql_dump.sql
```

### Step 4: List and Browse Snapshots

```bash
# List all snapshots
restic -r /backups/myrepo snapshots

# Filter by tag
restic -r /backups/myrepo snapshots --tag web

# Filter by host
restic -r /backups/myrepo snapshots --host production-server

# Browse files in a snapshot
restic -r /backups/myrepo ls latest
restic -r /backups/myrepo ls abc123de --path /var/www

# Compare snapshots
restic -r /backups/myrepo diff abc123 def456
```

### Step 5: Restore Data

```bash
# Restore entire snapshot to a directory
restic -r /backups/myrepo restore latest --target /restore

# Restore specific path from snapshot
restic -r /backups/myrepo restore latest --target /restore --include /var/www

# Restore specific file
restic -r /backups/myrepo restore latest --target /restore --include /etc/nginx/nginx.conf

# Restore stdin backup (database)
restic -r /backups/myrepo dump latest db_dump.sql | psql mydb

# Mount snapshots as filesystem (browse interactively)
mkdir /mnt/restic
restic -r /backups/myrepo mount /mnt/restic
# Now browse /mnt/restic/snapshots/ like a normal filesystem
```

### Step 6: Retention Policies (Pruning)

```bash
# Remove old snapshots by policy
restic -r /backups/myrepo forget \
  --keep-daily 7 \        # keep 1 snapshot per day for 7 days
  --keep-weekly 4 \       # keep 1 per week for 4 weeks
  --keep-monthly 12 \     # keep 1 per month for 12 months
  --keep-yearly 3 \       # keep 1 per year for 3 years
  --prune                  # also remove unreferenced data blobs

# Dry run first (see what would be removed)
restic -r /backups/myrepo forget --keep-daily 7 --keep-weekly 4 --dry-run

# Remove specific snapshot
restic -r /backups/myrepo forget abc123de --prune
```

### Step 7: Automation Script

```bash
#!/bin/bash
# backup.sh — Automated backup script for cron
# Run daily: 0 2 * * * /opt/scripts/backup.sh >> /var/log/backup.log 2>&1

export RESTIC_REPOSITORY="s3:http://minio.local:9000/backups/server1"
export RESTIC_PASSWORD_FILE="/etc/restic/password"
export AWS_ACCESS_KEY_ID="minio-access-key"
export AWS_SECRET_ACCESS_KEY="minio-secret-key"

echo "=== Backup started: $(date) ==="

# Back up application data
restic backup /var/www /home --exclude-file=/etc/restic/excludes.txt --tag app

# Back up databases
pg_dump -h localhost production_db | restic backup --stdin --stdin-filename production_db.sql --tag database

# Apply retention policy
restic forget --keep-daily 7 --keep-weekly 4 --keep-monthly 12 --prune

# Verify backup integrity (run weekly, not every time)
if [ "$(date +%u)" = "1" ]; then
  restic check
fi

echo "=== Backup completed: $(date) ==="
```

## Examples

### Example 1: Set up encrypted daily backups to S3
**User prompt:** "Back up my production server to S3 every night. Include /var/www, /home, and PostgreSQL dumps. Keep 7 daily, 4 weekly, and 12 monthly snapshots."

The agent will:
1. Install restic and initialize an S3 repository with a strong password.
2. Create an exclude file for temporary/cache files.
3. Write a backup script that backs up directories + database dump via stdin.
4. Add retention policy with forget/prune.
5. Set up cron for 2 AM daily execution.
6. Add a weekly integrity check with `restic check`.

### Example 2: Restore a deleted file from yesterday's backup
**User prompt:** "I accidentally deleted /var/www/config/production.env. Restore it from the most recent backup."

The agent will:
1. List recent snapshots with `restic snapshots`.
2. Find the file: `restic ls latest --path /var/www/config/`.
3. Restore just that file: `restic restore latest --target /tmp/restore --include /var/www/config/production.env`.
4. Copy the restored file back to its original location.

## Guidelines

- Store the repository password in a secure location (password manager, secrets manager, or encrypted file). If you lose the password, the backup data is unrecoverable — there is no recovery mechanism.
- Always run `restic check` periodically (weekly) to verify backup integrity. Catch corruption early, before you need to restore.
- Use `--exclude-file` for consistent exclusions across manual and automated runs. Common excludes: node_modules, .git, __pycache__, *.tmp, .cache.
- For database backups, pipe dumps through stdin (`pg_dump | restic backup --stdin`) instead of dumping to a file first — it saves disk space and is atomic.
- Deduplication is automatic — running the same backup twice only stores changed blocks. Daily full backups are efficient because restic deduplicates at the block level.
- Test restores regularly. A backup you've never tested restoring from is not a backup — it's a hope.
