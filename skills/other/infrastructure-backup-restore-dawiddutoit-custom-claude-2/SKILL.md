---
name: infrastructure-backup-restore
description: |
  Creates automated backup procedures, executes restoration operations, and implements disaster
  recovery workflows for network infrastructure. Use when backing up infrastructure before
  changes, preparing for disaster recovery, migrating to new server, or restoring after failure.
  Triggers on "backup infrastructure", "restore from backup", "disaster recovery", "backup before
  upgrade", or "migrate infrastructure". Works with Docker volumes (caddy_data, pihole_data),
  configuration files (docker-compose.yml, domains.toml), and .env secrets using tar archives
  and docker compose commands.
allowed-tools:
  - Read
  - Bash
  - Grep
---

Works with Docker volumes (caddy_data, pihole_data), configuration files, and .env secrets.
# Infrastructure Backup and Restore Skill

Complete backup and disaster recovery procedures for network infrastructure including Docker volumes, configuration files, and secrets.

## Quick Start

Quick full backup:

```bash
# Create backup directory
backup_dir="/home/dawiddutoit/projects/network/backups/full-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$backup_dir"

# Backup Docker volumes
tar -czf "$backup_dir/pihole_data.tar.gz" \
  -C /var/lib/docker/volumes/network_pihole_data/_data .
tar -czf "$backup_dir/caddy_data.tar.gz" \
  -C /var/lib/docker/volumes/network_caddy_data/_data .

# Backup configuration
cp -r /home/dawiddutoit/projects/network/docker-compose.yml "$backup_dir/"
cp -r /home/dawiddutoit/projects/network/caddy "$backup_dir/"
cp -r /home/dawiddutoit/projects/network/config "$backup_dir/"
cp -r /home/dawiddutoit/projects/network/.env "$backup_dir/.env"

echo "Backup completed: $backup_dir"
```

## Table of Contents

1. [When to Use This Skill](#when-to-use-this-skill)
2. [What This Skill Does](#what-this-skill-does)
3. [Instructions](#instructions)
   - Full Infrastructure Backup
   - Restore Full Infrastructure
   - Disaster Recovery
4. [Supporting Files](#supporting-files)
5. [Expected Outcomes](#expected-outcomes)
6. [Requirements](#requirements)
7. [Red Flags to Avoid](#red-flags-to-avoid)

## When to Use This Skill

**Explicit Triggers:**
- "Backup infrastructure"
- "Restore from backup"
- "Disaster recovery"
- "Backup before upgrade"
- "Migrate to new server"

**Implicit Triggers:**
- Planning major infrastructure changes
- Before OS upgrade or Docker upgrade
- Hardware failure requiring migration
- Testing disaster recovery procedures

**Debugging Triggers:**
- "What should I backup?"
- "How to restore from backup?"
- "Disaster recovery plan?"

## What This Skill Does

1. **Full Backup** - Creates complete infrastructure backup (volumes + config)
2. **Volume Backup** - Backs up Docker volumes (Pi-hole data, Caddy certificates)
3. **Config Backup** - Backs up configuration files and .env secrets
4. **Full Restore** - Restores complete infrastructure from backup
5. **Partial Restore** - Restores specific components (volume or config only)
6. **Disaster Recovery** - Complete rebuild procedure from backups
7. **Backup Management** - Retention policies and cleanup procedures

## Instructions

Use this skill to create and restore infrastructure backups. The skill provides workflows for:
- Full infrastructure backups (volumes + configuration + secrets)
- Partial backups (volumes only or configuration only)
- Full restoration from backups
- Disaster recovery from scratch on new hardware
- Automated backup scheduling and retention

See detailed procedures in sections below and `references/backup-procedures.md` for comprehensive guides.

### Full Infrastructure Backup

Create complete backup with all components:

```bash
backup_dir="/home/dawiddutoit/projects/network/backups/full-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$backup_dir"

# Backup Docker volumes
tar -czf "$backup_dir/pihole_data.tar.gz" \
  -C /var/lib/docker/volumes/network_pihole_data/_data .
tar -czf "$backup_dir/caddy_data.tar.gz" \
  -C /var/lib/docker/volumes/network_caddy_data/_data .

# Backup configuration
cp /home/dawiddutoit/projects/network/docker-compose.yml "$backup_dir/"
cp /home/dawiddutoit/projects/network/.env "$backup_dir/.env"
cp -r /home/dawiddutoit/projects/network/caddy "$backup_dir/"
cp -r /home/dawiddutoit/projects/network/config "$backup_dir/"

echo "Backup completed: $backup_dir"
```

**What's backed up:** Pi-hole data, Caddy certificates, configuration files, secrets (.env)

### Restore Full Infrastructure

Restore from complete backup:

```bash
backup_dir="/home/dawiddutoit/projects/network/backups/full-backup-20260120"

# Stop services
cd /home/dawiddutoit/projects/network
docker compose down

# Restore volumes
docker volume rm network_pihole_data network_caddy_data
docker volume create network_pihole_data
docker volume create network_caddy_data
tar -xzf "$backup_dir/pihole_data.tar.gz" \
  -C /var/lib/docker/volumes/network_pihole_data/_data
tar -xzf "$backup_dir/caddy_data.tar.gz" \
  -C /var/lib/docker/volumes/network_caddy_data/_data

# Restore configuration
cp "$backup_dir/docker-compose.yml" .
cp "$backup_dir/.env" .
cp -r "$backup_dir/caddy" .
cp -r "$backup_dir/config" .

# Start services
docker compose up -d
```

### Disaster Recovery

For complete rebuild on new hardware, see `references/backup-procedures.md` section "Disaster Recovery".

**Quick overview:**
1. Install Docker on new server
2. Restore configuration files
3. Restore Docker volumes
4. Start services
5. Verify connectivity and certificates

**Recovery time:** 15-30 minutes

## Supporting Files

| File | Purpose |
|------|---------|
| `references/backup-procedures.md` | Detailed backup/restore procedures, disaster recovery, retention policies |

## Expected Outcomes

**Success:**
- Full backup created with all components
- Backup size reasonable (< 500MB typical)
- Restoration completes without errors
- All services running after restore
- Configuration matches original

**Partial Success:**
- Backup created but missing some components (check manifest)
- Restore successful but services need manual restart

**Failure Indicators:**
- Backup fails due to permissions (need sudo for volumes)
- Restoration fails (volume path incorrect)
- Services don't start after restore (check docker compose logs)

## Requirements

- Sufficient disk space for backups (recommend 2GB free)
- Root/sudo access for Docker volume access
- Backup storage location with appropriate permissions
- For disaster recovery: Same Docker version or compatible

## Red Flags to Avoid

- [ ] Do not store .env backups unencrypted (contains secrets)
- [ ] Do not commit backups to git (contains sensitive data)
- [ ] Do not delete original backup before verifying restore works
- [ ] Do not restore to running services (stop first with docker compose down)
- [ ] Do not skip verifying services after restore
- [ ] Do not forget to backup .env file (critical for restoration)
- [ ] Do not rely solely on certificate backups (can be re-obtained)

## Notes

- Backup Docker volumes while services are running (Docker handles consistency)
- .env file is most critical (contains all secrets and tokens)
- Certificates can be re-obtained if Cloudflare API token valid
- Pi-hole data includes blocklists, custom DNS, whitelist
- Full backup typically < 500MB (mostly Pi-hole blocklists)
- Restoration requires docker and docker-compose installed
- Test disaster recovery procedure periodically (quarterly recommended)
- Consider encrypted off-site backups for true disaster recovery
- Use backup-infrastructure script from existing skills if available
