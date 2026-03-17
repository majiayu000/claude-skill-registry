---
name: hetzner-cloud-management
description: |
  Use when deploying, managing, or troubleshooting Hetzner Cloud infrastructure via hcloud CLI.
  Triggers: "hetzner cloud", "hcloud", "hetzner server", "create server on hetzner",
  "hetzner network", "hetzner firewall", "hetzner load balancer", "provision hetzner",
  "deploy to hetzner", "hetzner volume", "hetzner floating ip", "hetzner snapshot".
  Provides comprehensive workflows for server management, networking, storage, security,
  and production-ready automation patterns with the official Hetzner Cloud CLI.
---

# Hetzner Cloud Management

Comprehensive management of Hetzner Cloud infrastructure using the official `hcloud` CLI. Covers servers, networks, firewalls, load balancers, volumes, floating IPs, and automation workflows.

## Quick Reference

| Task | Command | Notes |
|------|---------|-------|
| **Create Server** | `hcloud server create --name <name> --type <type> --image <image>` | Add `--ssh-key`, `--network`, `--firewall` for production |
| **List Servers** | `hcloud server list` | Use `--output json` for scripting |
| **Server Control** | `hcloud server [poweron\|shutdown\|reboot\|reset] <name>` | `reset` is hard reset |
| **SSH Access** | `hcloud server ssh <name>` | Direct SSH connection |
| **Create Snapshot** | `hcloud server create-image <name> --type snapshot` | For backups before changes |
| **Create Network** | `hcloud network create --name <name> --ip-range <cidr>` | Private networking |
| **Create Firewall** | `hcloud firewall create --name <name> --rules-file <file>` | JSON format for rules |
| **Create Load Balancer** | `hcloud load-balancer create --name <name> --type <type>` | Add services and targets after |
| **Context Switch** | `hcloud context use <context>` | Multi-project management |
| **JSON Output** | `hcloud <command> --output json` | Pipe to `jq` for parsing |

## Command Categories

The `hcloud` CLI is organized into these main resource types:

| Category | Purpose | Key Commands |
|----------|---------|--------------|
| **server** | Virtual machines | create, list, delete, poweron, shutdown, ssh, create-image |
| **network** | Private networks | create, add-subnet, add-route, expose-routes-to-vswitch |
| **firewall** | Security rules | create, add-rule, apply-to-resource, replace-rules |
| **load-balancer** | Traffic distribution | create, add-service, add-target, change-algorithm |
| **volume** | Block storage | create, attach, detach, resize |
| **floating-ip** | Static IPs | create, assign, unassign, set-rdns |
| **ssh-key** | SSH key management | create, list, delete |
| **placement-group** | Server distribution | create spread, create anti-affinity |
| **primary-ip** | IP management | create, assign, unassign |
| **certificate** | SSL/TLS certs | create, list, delete |
| **datacenter** | View datacenters | list, describe |
| **location** | View locations | list, describe |
| **server-type** | View server types | list, describe |
| **image** | OS images | list, describe, delete |
| **context** | Multi-project auth | create, list, use, active, delete |

## Installation

### Install hcloud CLI

```bash
# macOS (Homebrew)
brew install hcloud

# Linux (snap)
sudo snap install hcloud

# Or download binary from GitHub releases
# https://github.com/hetznercloud/cli/releases
```

### Verify Installation

```bash
hcloud version
# Expected: hcloud v1.60.0 or later
```

## Authentication

### Workflow 1: Initial Setup with API Token

```bash
# 1. Get API token from Hetzner Cloud Console
# https://console.hetzner.cloud → Project → Security → API Tokens
# Create Read & Write token (64 characters)

# 2. Create context (interactive)
hcloud context create my-project
# Paste token when prompted

# 3. Verify authentication
hcloud server list

# 4. Show active context
hcloud context active
```

### Workflow 2: Multiple Projects (Context Management)

```bash
# Create contexts for different projects
hcloud context create production
# Enter production token

hcloud context create staging
# Enter staging token

# List all contexts
hcloud context list

# Switch between contexts
hcloud context use production
hcloud server list  # Lists production servers

hcloud context use staging
hcloud server list  # Lists staging servers

# Show active context
hcloud context active
```

### Workflow 3: CI/CD Authentication (Environment Variable)

```bash
# Export token (no config file created)
export HCLOUD_TOKEN="your-64-character-api-token"

# Run commands
hcloud server list

# In CI/CD pipelines (GitHub Actions example)
- name: Deploy to Hetzner
  env:
    HCLOUD_TOKEN: ${{ secrets.HETZNER_TOKEN }}
  run: |
    hcloud server create --name ci-server --type cpx11 --image ubuntu-24.04
```

### Configuration File Location

**Default**: `~/.config/hcloud/cli.toml`

```toml
# Global settings
active_context = "production"

[[contexts]]
  name = "production"
  token = "your-64-char-token"
  
[[contexts]]
  name = "staging"
  token = "another-64-char-token"
```

## Server Management

### Workflow 4: Create Basic Server

```bash
# Minimal server creation
hcloud server create \
  --name my-server \
  --type cpx11 \
  --image ubuntu-24.04 \
  --location fsn1

# Server types (common):
# cpx11  - 2 vCPU, 2 GB RAM (shared)
# cpx21  - 3 vCPU, 4 GB RAM (shared)
# cpx31  - 4 vCPU, 8 GB RAM (shared)
# cpx41  - 8 vCPU, 16 GB RAM (shared)
# ccx13  - 2 vCPU, 8 GB RAM (dedicated)
# ccx23  - 4 vCPU, 16 GB RAM (dedicated)

# Locations:
# fsn1 - Falkenstein, Germany
# nbg1 - Nuremberg, Germany
# hel1 - Helsinki, Finland
# ash - Ashburn, USA
# hil - Hillsboro, USA

# Images:
# ubuntu-24.04, ubuntu-22.04
# debian-12, debian-11
# fedora-40, rocky-9, alma-9
```

### Workflow 5: Create Production Server

```bash
# 1. Create SSH key first (if not exists)
hcloud ssh-key create \
  --name deploy-key \
  --public-key-from-file ~/.ssh/id_rsa.pub

# 2. Create network (for private networking)
hcloud network create --name app-network --ip-range 10.0.0.0/16
hcloud network add-subnet app-network \
  --type cloud \
  --network-zone eu-central \
  --ip-range 10.0.1.0/24

# 3. Create firewall rules file
cat > firewall-rules.json <<'EOF'
{
  "rules": [
    {
      "direction": "in",
      "protocol": "tcp",
      "port": "22",
      "source_ips": ["0.0.0.0/0", "::/0"],
      "description": "SSH"
    },
    {
      "direction": "in",
      "protocol": "tcp",
      "port": "80",
      "source_ips": ["0.0.0.0/0", "::/0"],
      "description": "HTTP"
    },
    {
      "direction": "in",
      "protocol": "tcp",
      "port": "443",
      "source_ips": ["0.0.0.0/0", "::/0"],
      "description": "HTTPS"
    }
  ]
}
EOF

# 4. Create firewall
hcloud firewall create --name web-firewall --rules-file firewall-rules.json

# 5. Create server with all options
hcloud server create \
  --name web-01 \
  --type cpx21 \
  --image ubuntu-24.04 \
  --location fsn1 \
  --ssh-key deploy-key \
  --network app-network \
  --firewall web-firewall \
  --labels environment=production,service=web,team=platform \
  --enable-backup \
  --user-data-from-file cloud-init.yaml

# 6. Enable deletion protection
hcloud server enable-protection web-01 --delete

# 7. Get server details
hcloud server describe web-01
```

### Workflow 6: Server Control Operations

```bash
# Power operations
hcloud server poweron my-server      # Start server
hcloud server shutdown my-server     # Graceful shutdown (ACPI)
hcloud server reboot my-server       # Graceful reboot
hcloud server reset my-server        # Hard reset (force)

# Check status
hcloud server describe my-server --output json | jq -r '.status'

# Enable/disable rescue mode
hcloud server enable-rescue my-server --ssh-key deploy-key
hcloud server reboot my-server  # Boot into rescue
# ... do maintenance ...
hcloud server disable-rescue my-server
hcloud server reboot my-server  # Boot normally

# SSH access
hcloud server ssh my-server

# SSH with custom user
hcloud server ssh my-server --user root

# Get server IP
hcloud server describe my-server --output json | jq -r '.public_net.ipv4.ip'
```

### Workflow 7: Snapshots and Backups

```bash
# Create snapshot (manual backup)
hcloud server create-image my-server \
  --type snapshot \
  --description "Before upgrade to v2.0" \
  --labels version=1.9,backup_type=manual

# Enable automatic backups (daily, 7-day retention)
hcloud server enable-backup my-server

# Disable backups
hcloud server disable-backup my-server

# List snapshots
hcloud image list --type snapshot

# List backups
hcloud image list --type backup

# Delete old snapshot
hcloud image delete snapshot-123456

# Restore from snapshot (create new server from image)
hcloud server create \
  --name my-server-restored \
  --image snapshot-123456 \
  --type cpx21 \
  --location fsn1
```

### Workflow 8: Server Scaling and Resize

```bash
# List available server types
hcloud server-type list

# Power off server (required for resize)
hcloud server shutdown my-server

# Wait for shutdown
while [ "$(hcloud server describe my-server -o json | jq -r '.status')" != "off" ]; do
  echo "Waiting for shutdown..."
  sleep 2
done

# Change server type (upgrade/downgrade)
hcloud server change-type my-server --upgrade-disk cpx31

# Power on
hcloud server poweron my-server

# Note: --upgrade-disk increases disk size permanently (cannot shrink)
# Without --upgrade-disk, disk size stays the same
```

## Network Infrastructure

### Workflow 9: Private Network Setup

```bash
# 1. Create private network
hcloud network create \
  --name app-network \
  --ip-range 10.0.0.0/16 \
  --labels environment=production

# 2. Add cloud subnet (for Hetzner Cloud servers)
hcloud network add-subnet app-network \
  --type cloud \
  --network-zone eu-central \
  --ip-range 10.0.1.0/24

# 3. Add another subnet for different services
hcloud network add-subnet app-network \
  --type cloud \
  --network-zone eu-central \
  --ip-range 10.0.2.0/24

# 4. Add route (for external gateway)
hcloud network add-route app-network \
  --destination 192.168.0.0/16 \
  --gateway 10.0.1.1

# 5. Attach existing server to network
hcloud server attach-to-network my-server \
  --network app-network \
  --ip 10.0.1.10

# 6. Detach server from network
hcloud server detach-from-network my-server --network app-network

# 7. List network details
hcloud network describe app-network
```

### Workflow 10: Firewall Management

```bash
# 1. Create firewall with rules file
cat > app-firewall.json <<'EOF'
{
  "rules": [
    {
      "direction": "in",
      "protocol": "tcp",
      "port": "22",
      "source_ips": ["YOUR_IP/32"],
      "description": "SSH from office"
    },
    {
      "direction": "in",
      "protocol": "tcp",
      "port": "443",
      "source_ips": ["0.0.0.0/0", "::/0"],
      "description": "HTTPS"
    },
    {
      "direction": "in",
      "protocol": "icmp",
      "source_ips": ["0.0.0.0/0", "::/0"],
      "description": "Ping"
    }
  ]
}
EOF

hcloud firewall create --name app-firewall --rules-file app-firewall.json

# 2. Apply firewall to server
hcloud firewall apply-to-resource app-firewall \
  --type server \
  --server web-01

# 3. Apply firewall to all servers with label
hcloud firewall apply-to-resource app-firewall \
  --type label \
  --label environment=production

# 4. Add individual rule
hcloud firewall add-rule app-firewall \
  --direction in \
  --protocol tcp \
  --port 8080 \
  --source-ips 10.0.0.0/16 \
  --description "Internal API"

# 5. Remove rule (by index, get from describe)
hcloud firewall describe app-firewall
hcloud firewall delete-rule app-firewall --index 2

# 6. Replace all rules
hcloud firewall replace-rules app-firewall --rules-file new-rules.json

# 7. Remove firewall from resource
hcloud firewall remove-from-resource app-firewall \
  --type server \
  --server web-01

# 8. List firewalls
hcloud firewall list
```

### Workflow 11: Load Balancer Setup

```bash
# 1. Create load balancer
hcloud load-balancer create \
  --name app-lb \
  --type lb11 \
  --location fsn1 \
  --labels service=frontend

# Load balancer types:
# lb11 - Up to 20,000 connections
# lb21 - Up to 40,000 connections
# lb31 - Up to 60,000 connections

# 2. Add HTTP service
hcloud load-balancer add-service app-lb \
  --protocol http \
  --listen-port 80 \
  --destination-port 8080 \
  --http-sticky-sessions

# 3. Add HTTPS service with certificate
hcloud certificate create \
  --name app-cert \
  --type managed \
  --domain example.com \
  --domain www.example.com

hcloud load-balancer add-service app-lb \
  --protocol https \
  --listen-port 443 \
  --destination-port 8080 \
  --http-certificates app-cert \
  --http-sticky-sessions \
  --http-redirect-http

# 4. Add health check
hcloud load-balancer update-service app-lb \
  --listen-port 80 \
  --health-check-protocol http \
  --health-check-port 8080 \
  --health-check-interval 15 \
  --health-check-timeout 10 \
  --health-check-retries 3 \
  --health-check-http-path /health

# 5. Add server targets
hcloud load-balancer add-target app-lb --type server --server web-01
hcloud load-balancer add-target app-lb --type server --server web-02

# 6. Or add target by label (auto-includes all matching servers)
hcloud load-balancer add-target app-lb \
  --type label \
  --label service=web

# 7. Change algorithm
hcloud load-balancer change-algorithm app-lb --type round_robin
# Options: round_robin, least_connections

# 8. Get metrics
hcloud load-balancer metrics app-lb --type open_connections
hcloud load-balancer metrics app-lb --type requests_per_second

# 9. Enable deletion protection
hcloud load-balancer enable-protection app-lb --delete
```

## Storage Management

### Workflow 12: Volume Management

```bash
# 1. Create volume
hcloud volume create \
  --name data-vol \
  --size 50 \
  --location fsn1 \
  --format ext4 \
  --labels service=database

# 2. Attach volume to server
hcloud volume attach data-vol --server db-01

# 3. Mount volume (on server)
# SSH into server and mount
hcloud server ssh db-01
sudo mkdir -p /mnt/data
sudo mount /dev/disk/by-id/scsi-0HC_Volume_* /mnt/data

# 4. Detach volume
hcloud volume detach data-vol

# 5. Resize volume (server must be off or volume detached)
hcloud volume resize data-vol --size 100

# 6. Enable protection
hcloud volume enable-protection data-vol --delete

# 7. List volumes
hcloud volume list

# 8. Delete volume
hcloud volume delete data-vol
```

### Workflow 13: Floating IP Management

```bash
# 1. Create floating IP
hcloud floating-ip create \
  --type ipv4 \
  --home-location fsn1 \
  --description "Primary web IP" \
  --labels service=web

# 2. Create IPv6
hcloud floating-ip create \
  --type ipv6 \
  --home-location fsn1

# 3. Assign to server
hcloud floating-ip assign 1.2.3.4 --server web-01

# 4. Configure on server (manual step)
# SSH into server and add IP to network interface
hcloud server ssh web-01
sudo ip addr add 1.2.3.4/32 dev eth0

# 5. Set reverse DNS
hcloud floating-ip set-rdns 1.2.3.4 --hostname web.example.com

# 6. Unassign from server
hcloud floating-ip unassign 1.2.3.4

# 7. Enable protection
hcloud floating-ip enable-protection 1.2.3.4 --delete

# 8. List floating IPs
hcloud floating-ip list
```

## Automation Patterns

### Workflow 14: Complete Infrastructure Provisioning

```bash
#!/bin/bash
set -euo pipefail

# Configuration
PROJECT="my-app"
LOCATION="fsn1"
NETWORK_CIDR="10.0.0.0/16"
SUBNET_CIDR="10.0.1.0/24"

# 1. Create private network
echo "Creating network..."
hcloud network create --name "${PROJECT}-network" --ip-range "$NETWORK_CIDR"
hcloud network add-subnet "${PROJECT}-network" \
  --type cloud \
  --network-zone eu-central \
  --ip-range "$SUBNET_CIDR"

# 2. Create firewall
echo "Creating firewall..."
cat > firewall.json <<'EOF'
{
  "rules": [
    {"direction": "in", "protocol": "tcp", "port": "22", "source_ips": ["0.0.0.0/0", "::/0"], "description": "SSH"},
    {"direction": "in", "protocol": "tcp", "port": "80", "source_ips": ["0.0.0.0/0", "::/0"], "description": "HTTP"},
    {"direction": "in", "protocol": "tcp", "port": "443", "source_ips": ["0.0.0.0/0", "::/0"], "description": "HTTPS"}
  ]
}
EOF
hcloud firewall create --name "${PROJECT}-firewall" --rules-file firewall.json

# 3. Create SSH key
echo "Creating SSH key..."
hcloud ssh-key create --name "${PROJECT}-key" --public-key-from-file ~/.ssh/id_rsa.pub || true

# 4. Create web servers
echo "Creating web servers..."
for i in 1 2 3; do
  hcloud server create \
    --name "${PROJECT}-web-${i}" \
    --type cpx21 \
    --image ubuntu-24.04 \
    --location "$LOCATION" \
    --network "${PROJECT}-network" \
    --firewall "${PROJECT}-firewall" \
    --ssh-key "${PROJECT}-key" \
    --labels "app=${PROJECT},role=web,index=${i}" \
    --enable-backup &
done
wait

# 5. Wait for servers to be ready
echo "Waiting for servers..."
for i in 1 2 3; do
  while [ "$(hcloud server describe "${PROJECT}-web-${i}" -o json | jq -r '.status')" != "running" ]; do
    sleep 2
  done
  echo "${PROJECT}-web-${i} is running"
done

# 6. Create load balancer
echo "Creating load balancer..."
hcloud load-balancer create \
  --name "${PROJECT}-lb" \
  --type lb11 \
  --location "$LOCATION"

# 7. Add HTTP service
hcloud load-balancer add-service "${PROJECT}-lb" \
  --protocol http \
  --listen-port 80 \
  --destination-port 80 \
  --health-check-protocol http \
  --health-check-port 80 \
  --health-check-http-path /health

# 8. Add targets by label (automatically includes all web servers)
hcloud load-balancer add-target "${PROJECT}-lb" \
  --type label \
  --label "role=web"

# 9. Output summary
echo ""
echo "Infrastructure created:"
echo "======================"
hcloud server list --output columns=name,ipv4,status | grep "${PROJECT}"
echo ""
LB_IP=$(hcloud load-balancer describe "${PROJECT}-lb" -o json | jq -r '.public_net.ipv4.ip')
echo "Load Balancer IP: $LB_IP"
echo ""
echo "Test: curl http://$LB_IP"
```

### Workflow 15: Server Monitoring and Health Checks

```bash
#!/bin/bash
# Monitor server health and send alerts

# Get all production servers
SERVERS=$(hcloud server list -o json | jq -r '.[] | select(.labels.environment == "production") | .name')

for server in $SERVERS; do
  STATUS=$(hcloud server describe "$server" -o json | jq -r '.status')
  
  if [ "$STATUS" != "running" ]; then
    echo "⚠️  $server is $STATUS"
    # Send alert (example: Slack webhook)
    # curl -X POST -H 'Content-type: application/json' \
    #   --data "{\"text\":\"Server $server is $STATUS\"}" \
    #   "$SLACK_WEBHOOK_URL"
  else
    echo "✅ $server is running"
  fi
  
  # Check server metrics (CPU)
  CPU=$(hcloud server metrics "$server" --type cpu --start=$(date -u -d '5 minutes ago' +%s) -o json | jq -r '.time_series.cpu.values[-1][1]')
  echo "   CPU: ${CPU}%"
  
  if (( $(echo "$CPU > 90" | bc -l) )); then
    echo "   ⚠️  High CPU usage!"
  fi
done
```

### Workflow 16: Cleanup and Resource Management

```bash
#!/bin/bash
# Clean up temporary/stopped resources

# Delete stopped servers with 'temp' label
echo "Cleaning up temporary servers..."
hcloud server list -o json | jq -r '.[] | select(.labels.temp == "true") | select(.status == "off") | .name' | while read server; do
  echo "Deleting $server..."
  hcloud server delete "$server"
done

# Delete unattached volumes older than 7 days
echo "Cleaning up unattached volumes..."
hcloud volume list -o json | jq -r '.[] | select(.server == null) | "\(.id) \(.created)"' | while read id created; do
  AGE=$(( ($(date +%s) - $(date -d "$created" +%s)) / 86400 ))
  if [ $AGE -gt 7 ]; then
    echo "Deleting volume $id (${AGE} days old)..."
    hcloud volume delete "$id"
  fi
done

# Delete old snapshots (keep last 3)
echo "Cleaning up old snapshots..."
hcloud image list --type snapshot -o json | \
  jq -r 'sort_by(.created) | reverse | .[3:] | .[] | .id' | \
  while read image_id; do
    echo "Deleting snapshot $image_id..."
    hcloud image delete "$image_id"
  done
```

### Workflow 17: Batch Operations with JSON

```bash
# Get IPs of all running web servers
hcloud server list -o json | \
  jq -r '.[] | select(.labels.role == "web") | select(.status == "running") | "\(.name): \(.public_net.ipv4.ip)"'

# Generate Ansible inventory
echo "[web_servers]"
hcloud server list -o json | \
  jq -r '.[] | select(.labels.role == "web") | "\(.public_net.ipv4.ip) hostname=\(.name)"'

# Shutdown all dev servers
hcloud server list -o json | \
  jq -r '.[] | select(.labels.environment == "dev") | .name' | \
  xargs -I {} hcloud server shutdown {}

# Apply firewall to all servers with label
FIREWALL="prod-firewall"
hcloud server list -o json | \
  jq -r '.[] | select(.labels.environment == "production") | .name' | \
  while read server; do
    hcloud firewall apply-to-resource "$FIREWALL" --type server --server "$server"
  done
```

## Best Practices

### Resource Organization

```bash
# Use consistent labeling scheme
--labels environment=production,service=api,team=platform,version=v2.0

# Label-based operations
hcloud server list --selector environment=production
hcloud server list --selector service=web

# Use descriptive names
--name prod-web-01  # Good
--name server-123   # Bad

# Enable protection on critical resources
hcloud server enable-protection prod-db-01 --delete --rebuild
hcloud volume enable-protection prod-data --delete
```

### Security Hardening

```bash
# 1. Restrict SSH to specific IPs
{
  "rules": [
    {
      "direction": "in",
      "protocol": "tcp",
      "port": "22",
      "source_ips": ["YOUR_OFFICE_IP/32"],
      "description": "SSH from office only"
    }
  ]
}

# 2. Use private networks for inter-server communication
# Don't expose databases/APIs on public internet

# 3. Enable backups on critical servers
hcloud server enable-backup prod-db-01

# 4. Use SSH keys, never passwords
hcloud ssh-key create --name deploy-key --public-key-from-file ~/.ssh/id_rsa.pub

# 5. Regular security updates (cloud-init example)
#cloud-config
package_upgrade: true
packages:
  - unattended-upgrades
```

### Cost Optimization

```bash
# 1. Use appropriate server types (don't over-provision)
hcloud server-type list  # Review pricing

# 2. Shutdown dev/staging servers when not in use
hcloud server shutdown dev-*

# 3. Use snapshots instead of keeping servers running
hcloud server create-image dev-server --type snapshot --description "Dev environment"
hcloud server delete dev-server
# Restore when needed

# 4. Clean up old snapshots/backups
hcloud image list --type snapshot
hcloud image delete old-snapshot-id

# 5. Use placement groups to reduce costs
# Spread: Distributes across physical hosts (HA)
# Max 10 servers per spread group
hcloud placement-group create spread --name ha-group
```

### High Availability Patterns

```bash
# 1. Use multiple locations
hcloud server create --name web-fsn1 --location fsn1
hcloud server create --name web-nbg1 --location nbg1

# 2. Use load balancers with health checks
hcloud load-balancer add-service app-lb \
  --health-check-protocol http \
  --health-check-retries 3 \
  --health-check-interval 15

# 3. Use floating IPs for failover
# Assign floating IP to primary
hcloud floating-ip assign 1.2.3.4 --server primary
# On failure, reassign to secondary
hcloud floating-ip assign 1.2.3.4 --server secondary

# 4. Use placement groups for distribution
hcloud placement-group create spread --name web-spread
hcloud server create --placement-group web-spread

# 5. Enable backups
hcloud server enable-backup prod-server
```

## Troubleshooting

### Authentication Issues

```bash
# Check active context
hcloud context active

# List all contexts
hcloud context list

# Verify token works
hcloud server list
# If error: "unable to authenticate", token is invalid

# Re-authenticate
hcloud context delete my-project
hcloud context create my-project
# Enter new token

# Check config file
cat ~/.config/hcloud/cli.toml
```

### Server Creation Failures

```bash
# Check location capacity
hcloud location list
hcloud server-type list

# Check if server type available in location
hcloud datacenter list

# Common errors:
# "insufficient resources" - Try different location
# "placement_group_limit_reached" - Max 10 servers per spread group
# "limit_reached" - Check project limits in console

# Verbose output for debugging
hcloud server create --name test --type cpx11 --image ubuntu-24.04 --debug
```

### Network Connectivity Issues

```bash
# Check firewall rules
hcloud firewall describe my-firewall

# Check server network attachment
hcloud server describe my-server -o json | jq '.private_net'

# Check network routes
hcloud network describe my-network

# Test connectivity (from server)
hcloud server ssh my-server
ping -c 3 10.0.1.10  # Test private network

# Check if firewall is applied
hcloud firewall list
hcloud server describe my-server -o json | jq '.firewall_ids'
```

### Performance Issues

```bash
# Check server metrics
hcloud server metrics my-server --type cpu
hcloud server metrics my-server --type network
hcloud server metrics my-server --type disk

# Check load balancer metrics
hcloud load-balancer metrics my-lb --type open_connections
hcloud load-balancer metrics my-lb --type requests_per_second

# Review server type specs
hcloud server-type describe cpx21

# Consider upgrading
hcloud server shutdown my-server
hcloud server change-type my-server --upgrade-disk cpx31
hcloud server poweron my-server
```

### Common Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| `unable to authenticate` | Invalid/expired token | Re-create context with valid token |
| `server not found` | Wrong context or server name | Check `hcloud context active` |
| `insufficient resources` | Location at capacity | Try different location |
| `limit_reached` | Project limit exceeded | Contact support or upgrade |
| `protected` | Resource has deletion protection | Disable protection first |
| `server_already_attached` | Already in network | Detach first, then re-attach |
| `ip_not_available` | IP already assigned | Unassign from other resource |

## Output Formats for Scripting

```bash
# JSON output (recommended for scripts)
hcloud server list --output json

# Parse with jq
hcloud server list -o json | jq '.[] | {name: .name, ip: .public_net.ipv4.ip}'

# YAML output
hcloud server describe my-server --output yaml

# Custom Go template
hcloud server list --output format='{{range .}}{{.Name}}: {{.PublicNet.IPv4.IP}}{{"\n"}}{{end}}'

# Table without header (for parsing)
hcloud server list --output noheader

# Select specific columns
hcloud server list --output columns=name,ipv4,status

# Combine options
hcloud server list -o noheader -o columns=name,ipv4 | while read name ip; do
  echo "Server: $name -> $ip"
done
```

## Advanced Use Cases

### Placement Groups

```bash
# Create spread group (HA - different physical hosts)
hcloud placement-group create spread --name ha-web

# Create servers in group
hcloud server create --name web-01 --placement-group ha-web --type cpx21
hcloud server create --name web-02 --placement-group ha-web --type cpx21

# Max 10 servers per spread group
# Use multiple groups for larger deployments
```

### Primary IPs

```bash
# Create primary IPv4 (replaces default server IP)
hcloud primary-ip create \
  --type ipv4 \
  --assignee-type server \
  --datacenter fsn1-dc14 \
  --name web-primary-ip

# Assign to server during creation
hcloud server create \
  --name my-server \
  --type cpx11 \
  --image ubuntu-24.04 \
  --primary-ipv4 web-primary-ip

# Benefit: Keep IP when recreating server
```

### User Data (Cloud-Init)

```bash
# Create cloud-init file
cat > cloud-init.yaml <<'EOF'
#cloud-config
package_upgrade: true
packages:
  - docker.io
  - git
  - curl

write_files:
  - path: /etc/docker/daemon.json
    content: |
      {"log-driver": "json-file", "log-opts": {"max-size": "10m"}}

runcmd:
  - systemctl enable docker
  - systemctl start docker
  - usermod -aG docker ubuntu
EOF

# Create server with user data
hcloud server create \
  --name docker-server \
  --type cpx21 \
  --image ubuntu-24.04 \
  --user-data-from-file cloud-init.yaml
```

### DNS Integration (Experimental)

```bash
# Create DNS zone
hcloud zone create --name example.com

# Add records
hcloud zone add-record example.com --type A --name www --value 1.2.3.4
hcloud zone add-record example.com --type AAAA --name www --value 2001:db8::1

# List zones
hcloud zone list

# Export zone
hcloud zone export example.com
```

## Resources

- **Official CLI Repository**: https://github.com/hetznercloud/cli
- **Hetzner Cloud API Docs**: https://docs.hetzner.cloud/
- **Hetzner Cloud Console**: https://console.hetzner.cloud/
- **Community Forum**: https://community.hetzner.com/
- **API Changelog**: https://docs.hetzner.cloud/changelog/

## Version Information

This skill is based on `hcloud` CLI **v1.60.0** (January 2026).
