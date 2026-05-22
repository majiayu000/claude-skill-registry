---
name: infrastructure-backup-restore
description: |
  Performs backup and restoration operations for network infrastructure including Docker
  volumes (Pi-hole, Caddy certificates), configuration files, and .env secrets. Use when
  backing up infrastructure before changes, preparing for disaster recovery, migrating
  to new server, or restoring after failure. Triggers on "backup infrastructure", "restore
  from backup", "disaster recovery", "backup before upgrade", or "migrate infrastructure".
  Works with Docker volumes (caddy_data, pihole_data), configuration files, and .env
  secrets management.
allowed-tools:
  - Read
  - Bash
  - Grep
---

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

1. [When to Use This Skill](#1-when-to-use-this-skill)
2. [What This Skill Does](#2-what-this-skill-does)
3. [Instructions](#3-instructions)
   - 3.1 Full Infrastructure Backup
   - 3.2 Backup Docker Volumes
   - 3.3 Backup Configuration Files
   - 3.4 Restore Full Infrastructure
   - 3.5 Restore Specific Components
   - 3.6 Disaster Recovery Procedure
   - 3.7 Backup Management and Retention
4. [Supporting Files](#4-supporting-files)
5. [Expected Outcomes](#5-expected-outcomes)
6. [Requirements](#6-requirements)
7. [Red Flags to Avoid](#7-red-flags-to-avoid)

## 1. When to Use This Skill

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

## 2. What This Skill Does

1. **Full Backup** - Creates complete infrastructure backup (volumes + config)
2. **Volume Backup** - Backs up Docker volumes (Pi-hole data, Caddy certificates)
3. **Config Backup** - Backs up configuration files and .env secrets
4. **Full Restore** - Restores complete infrastructure from backup
5. **Partial Restore** - Restores specific components (volume or config only)
6. **Disaster Recovery** - Complete rebuild procedure from backups
7. **Backup Management** - Retention policies and cleanup procedures

## 3. Instructions

### 3.1 Full Infrastructure Backup

**Complete backup including all components:**

```bash
# Set backup directory
backup_dir="/home/dawiddutoit/projects/network/backups/full-backup-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$backup_dir"

echo "Creating full infrastructure backup..."
echo "Backup location: $backup_dir"

# Backup Pi-hole data
echo "Backing up Pi-hole data..."
tar -czf "$backup_dir/pihole_data.tar.gz" \
  -C /var/lib/docker/volumes/network_pihole_data/_data .

# Backup Caddy data (certificates)
echo "Backing up Caddy certificates..."
tar -czf "$backup_dir/caddy_data.tar.gz" \
  -C /var/lib/docker/volumes/network_caddy_data/_data .

# Backup configuration files
echo "Backing up configuration files..."
cp /home/dawiddutoit/projects/network/docker-compose.yml "$backup_dir/"
cp /home/dawiddutoit/projects/network/domains.toml "$backup_dir/"
cp -r /home/dawiddutoit/projects/network/caddy "$backup_dir/"
cp -r /home/dawiddutoit/projects/network/config "$backup_dir/"
cp -r /home/dawiddutoit/projects/network/scripts "$backup_dir/"

# Backup .env (SENSITIVE - secure this!)
echo "Backing up .env secrets..."
cp /home/dawiddutoit/projects/network/.env "$backup_dir/.env"

# Backup systemd services
echo "Backing up systemd services..."
mkdir -p "$backup_dir/systemd"
cp /etc/systemd/system/infrastructure-monitor.* "$backup_dir/systemd/" 2>/dev/null || true

# Create backup manifest
cat > "$backup_dir/MANIFEST.txt" << EOF
Infrastructure Backup Manifest
Created: $(date)
Hostname: $(hostname)
User: $(whoami)

Contents:
- pihole_data.tar.gz (Pi-hole configuration and data)
- caddy_data.tar.gz (Caddy certificates and data)
- docker-compose.yml (Service definitions)
- domains.toml (Domain configuration)
- caddy/ (Caddyfile and Dockerfile)
- config/ (Webhook and Caddy configs)
- scripts/ (Management scripts)
- .env (SENSITIVE - all secrets and tokens)
- systemd/ (Monitoring service files)

⚠️  SECURITY WARNING:
This backup contains sensitive data:
- API tokens (Cloudflare, Google OAuth)
- Passwords (Pi-hole)
- Webhook secrets
- Access tokens

Store securely and encrypt for off-site storage.
EOF

# Show backup summary
echo ""
echo "✅ Backup completed successfully!"
echo "Location: $backup_dir"
echo ""
echo "Backup contents:"
ls -lh "$backup_dir"
echo ""
echo "Total size: $(du -sh "$backup_dir" | cut -f1)"
```

**What's included:**
- Pi-hole configuration and blocklists
- Caddy SSL certificates
- All configuration files
- All secrets (.env)
- Management scripts
- Systemd service definitions

### 3.2 Backup Docker Volumes

**Backup individual volumes:**

```bash
backup_dir="/home/dawiddutoit/projects/network/backups"
mkdir -p "$backup_dir"

# Backup Pi-hole data
echo "Backing up Pi-hole data..."
tar -czf "$backup_dir/pihole-backup-$(date +%Y%m%d).tar.gz" \
  -C /var/lib/docker/volumes/network_pihole_data/_data .

# Backup Caddy certificates
echo "Backing up Caddy certificates..."
tar -czf "$backup_dir/caddy-backup-$(date +%Y%m%d).tar.gz" \
  -C /var/lib/docker/volumes/network_caddy_data/_data .

echo "Volume backups completed"
ls -lh "$backup_dir"/*-backup-$(date +%Y%m%d).tar.gz
```

**Note on Caddy certificates:**
- Certificates can be re-obtained automatically via DNS-01 challenge
- Backup not strictly necessary if Cloudflare API token is valid
- Useful for immediate restoration without waiting for ACME

### 3.3 Backup Configuration Files

**Backup configuration without Docker volumes:**

```bash
backup_dir="/home/dawiddutoit/projects/network/backups/config-$(date +%Y%m%d)"
mkdir -p "$backup_dir"

# Backup configuration
tar -czf "$backup_dir/network-config.tar.gz" \
  -C /home/dawiddutoit/projects/network \
  docker-compose.yml domains.toml caddy/ config/ scripts/ .env

echo "Configuration backup completed: $backup_dir/network-config.tar.gz"
```

### 3.4 Restore Full Infrastructure

**Complete restoration procedure:**

```bash
# Set backup location
backup_dir="/home/dawiddutoit/projects/network/backups/full-backup-20260120-143000"

echo "Starting full infrastructure restore..."
echo "Backup source: $backup_dir"

# Stop all services
echo "Stopping services..."
cd /home/dawiddutoit/projects/network
docker compose down

# Restore Pi-hole data
echo "Restoring Pi-hole data..."
docker volume rm network_pihole_data
docker volume create network_pihole_data
tar -xzf "$backup_dir/pihole_data.tar.gz" \
  -C /var/lib/docker/volumes/network_pihole_data/_data

# Restore Caddy certificates
echo "Restoring Caddy certificates..."
docker volume rm network_caddy_data
docker volume create network_caddy_data
tar -xzf "$backup_dir/caddy_data.tar.gz" \
  -C /var/lib/docker/volumes/network_caddy_data/_data

# Restore configuration files
echo "Restoring configuration files..."
cp "$backup_dir/docker-compose.yml" /home/dawiddutoit/projects/network/
cp "$backup_dir/domains.toml" /home/dawiddutoit/projects/network/
cp -r "$backup_dir/caddy" /home/dawiddutoit/projects/network/
cp -r "$backup_dir/config" /home/dawiddutoit/projects/network/
cp -r "$backup_dir/scripts" /home/dawiddutoit/projects/network/

# Restore .env
echo "Restoring .env secrets..."
cp "$backup_dir/.env" /home/dawiddutoit/projects/network/.env

# Restore systemd services
echo "Restoring systemd services..."
if [ -d "$backup_dir/systemd" ]; then
  sudo cp "$backup_dir/systemd/infrastructure-monitor."* /etc/systemd/system/
  sudo systemctl daemon-reload
  sudo systemctl enable infrastructure-monitor.timer
fi

# Start services
echo "Starting services..."
docker compose up -d

# Wait for services to start
echo "Waiting for services to initialize..."
sleep 10

# Verify services running
echo ""
echo "Verifying services..."
docker compose ps

echo ""
echo "✅ Restoration completed!"
echo ""
echo "Next steps:"
echo "1. Verify services are running: docker compose ps"
echo "2. Test DNS resolution: dig @192.168.68.136 pihole.temet.ai"
echo "3. Test HTTPS certificates: curl -I https://pihole.temet.ai"
echo "4. Test tunnel connectivity: docker logs cloudflared | grep 'Registered tunnel'"
```

### 3.5 Restore Specific Components

**Restore only Pi-hole data:**

```bash
backup_file="/home/dawiddutoit/projects/network/backups/pihole-backup-20260120.tar.gz"

# Stop Pi-hole
docker compose -f /home/dawiddutoit/projects/network/docker-compose.yml down pihole

# Restore volume
docker volume rm network_pihole_data
docker volume create network_pihole_data
tar -xzf "$backup_file" \
  -C /var/lib/docker/volumes/network_pihole_data/_data

# Start Pi-hole
docker compose -f /home/dawiddutoit/projects/network/docker-compose.yml up -d pihole

echo "Pi-hole data restored"
```

**Restore only Caddy certificates:**

```bash
backup_file="/home/dawiddutoit/projects/network/backups/caddy-backup-20260120.tar.gz"

# Stop Caddy
docker compose -f /home/dawiddutoit/projects/network/docker-compose.yml down caddy

# Restore volume
docker volume rm network_caddy_data
docker volume create network_caddy_data
tar -xzf "$backup_file" \
  -C /var/lib/docker/volumes/network_caddy_data/_data

# Start Caddy
docker compose -f /home/dawiddutoit/projects/network/docker-compose.yml up -d caddy

echo "Caddy certificates restored"
```

**Restore only configuration:**

```bash
backup_file="/home/dawiddutoit/projects/network/backups/config-20260120/network-config.tar.gz"

# Extract to project directory
tar -xzf "$backup_file" \
  -C /home/dawiddutoit/projects/network

# Restart services to pick up changes
docker compose -f /home/dawiddutoit/projects/network/docker-compose.yml restart

echo "Configuration restored"
```

### 3.6 Disaster Recovery Procedure

**Complete rebuild from scratch:**

**Scenario:** New server, fresh OS, need to restore infrastructure

**Step 1: Install Docker**

```bash
# Install Docker (Ubuntu/Debian)
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo apt install docker-compose-plugin -y
```

**Step 2: Restore Project Directory**

```bash
# Create project directory
mkdir -p /home/dawiddutoit/projects/network
cd /home/dawiddutoit/projects/network

# Extract backup
backup_dir="/path/to/backup/full-backup-20260120-143000"
cp -r "$backup_dir"/* .
```

**Step 3: Restore Docker Volumes**

```bash
# Create volumes
docker volume create network_pihole_data
docker volume create network_caddy_data

# Restore Pi-hole data
tar -xzf pihole_data.tar.gz \
  -C /var/lib/docker/volumes/network_pihole_data/_data

# Restore Caddy certificates
tar -xzf caddy_data.tar.gz \
  -C /var/lib/docker/volumes/network_caddy_data/_data
```

**Step 4: Restore Systemd Services**

```bash
# Copy systemd service files
sudo cp systemd/infrastructure-monitor.* /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now infrastructure-monitor.timer
```

**Step 5: Start Services**

```bash
# Start all services
docker compose up -d

# Monitor startup
docker compose logs -f
```

**Step 6: Verify Recovery**

```bash
# Check all services running
docker compose ps

# Test DNS
dig @192.168.68.136 pihole.temet.ai

# Test HTTPS
curl -I https://pihole.temet.ai

# Test tunnel
docker logs cloudflared | grep "Registered tunnel"

# Run health check
./scripts/health-check.sh
```

**Recovery time:** 15-30 minutes depending on internet speed

### 3.7 Backup Management and Retention

**Backup retention policy:**

```bash
backup_base="/home/dawiddutoit/projects/network/backups"

# Keep last 7 daily backups
find "$backup_base" -name "full-backup-*" -mtime +7 -delete

# Keep last 3 monthly backups (first of month)
# Manual: Review and delete old monthly backups

# Always keep latest full backup
```

**Automated backup script:**

```bash
#!/bin/bash
# /home/dawiddutoit/projects/network/scripts/backup-infrastructure.sh

backup_dir="/home/dawiddutoit/projects/network/backups/auto-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$backup_dir"

# Backup volumes
tar -czf "$backup_dir/pihole_data.tar.gz" \
  -C /var/lib/docker/volumes/network_pihole_data/_data .
tar -czf "$backup_dir/caddy_data.tar.gz" \
  -C /var/lib/docker/volumes/network_caddy_data/_data .

# Backup configuration
cp /home/dawiddutoit/projects/network/.env "$backup_dir/.env"
cp /home/dawiddutoit/projects/network/docker-compose.yml "$backup_dir/"
cp /home/dawiddutoit/projects/network/domains.toml "$backup_dir/"

# Delete backups older than 7 days
find /home/dawiddutoit/projects/network/backups -name "auto-*" -mtime +7 -delete

echo "Backup completed: $backup_dir"
```

**Schedule with cron:**

```bash
# Add to crontab
crontab -e

# Daily backup at 2 AM
0 2 * * * /home/dawiddutoit/projects/network/scripts/backup-infrastructure.sh >> /var/log/infrastructure-backup.log 2>&1
```

**Off-site backup:**

```bash
# Encrypt backup for off-site storage
backup_file="/home/dawiddutoit/projects/network/backups/full-backup-20260120.tar.gz"

tar -czf - /path/to/backup | \
  gpg --symmetric --cipher-algo AES256 > backup-encrypted.tar.gz.gpg

# Upload to cloud storage (example)
# rclone copy backup-encrypted.tar.gz.gpg remote:backups/
```

## 4. Supporting Files

| File | Purpose |
|------|---------|
| `references/reference.md` | Backup strategies, retention policies, encryption |
| `scripts/backup-infrastructure.sh` | Automated backup script |
| `scripts/restore-infrastructure.sh` | Automated restore script |
| `examples/examples.md` | Example backup/restore scenarios |

## 5. Expected Outcomes

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

## 6. Requirements

- Sufficient disk space for backups (recommend 2GB free)
- Root/sudo access for Docker volume access
- Backup storage location with appropriate permissions
- For disaster recovery: Same Docker version or compatible

## 7. Red Flags to Avoid

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
