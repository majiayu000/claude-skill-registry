---
name: push-to-cloud
description: "Deploy projects to OCI-Dev cloud instance with full automation. Handles rsync, systemd service creation, and optional DNS/Traefik setup. Use when user says 'deploy', 'push to cloud', 'host this', or 'run externally'."
allowed-tools: Read, Write, Edit, Bash, Glob
---

# Push to Cloud

You are an expert at deploying projects to the OCI-Dev cloud instance.

## When To Use

- User says "Deploy this to cloud", "Push to OCI"
- User says "Run this externally", "Host this publicly"
- Project needs to run 24/7 outside homelab
- Lightweight Python/Node service needs cloud hosting

> **Homelab Alternative**: For services running on homelab, consider using
> **Tailscale Funnel + Cloudflare Worker** instead. Simpler setup, no port
> forwarding, automatic HTTPS. See [docs/public-access.md](../../../docs/public-access.md).

## Target Machine: OCI-Dev

| Property | Value |
|----------|-------|
| Hostname | oci-dev (instance-first) |
| Tailscale IP | 100.126.13.70 |
| Public IP | 141.148.146.79 |
| OS | Ubuntu 24.04 LTS (ARM64) |
| Free Storage | ~77GB |
| Free RAM | ~22GB |

### OCI Always Free Tier Limits

| Resource | Hard Limit |
|----------|-----------|
| vCPUs | 4 OCPU (ARM) |
| RAM | 24 GB |
| Storage | 200 GB boot volume |
| Outbound Data | 10 TB/month |

## What CAN Be Deployed

- Lightweight Python APIs (FastAPI, Flask)
- Static sites / simple web apps
- Background workers / cron jobs
- Webhook receivers
- Chat bots (Telegram, Discord)
- Small databases (SQLite, Redis)

## What Should NOT Be Deployed

- Heavy ML models (use homelab GPU)
- Large databases (PostgreSQL with big datasets)
- High-traffic production apps
- Anything requiring >4GB RAM per process

## Prerequisites Check

```bash
ssh ubuntu@100.126.13.70 << 'CHECK'
echo "=== OCI-Dev Prerequisites ==="
python3 --version
pip3 --version
systemctl --version | head -1
df -h / | awk 'NR==2 {print "Disk: " $4 " available"}'
free -h | awk '/Mem:/ {print "RAM: " $4 " available"}'
CHECK
```

## Quick Deploy Script

```bash
# Variables
PROJECT_NAME="my-project"
PORT="8080"
ENTRY_POINT="app.py"

# 1. Push code
rsync -avz --exclude='.venv' --exclude='node_modules' \
  --exclude='__pycache__' --exclude='.git' \
  ./ ubuntu@100.126.13.70:~/dev/${PROJECT_NAME}/

# 2. Setup on remote
ssh ubuntu@100.126.13.70 << REMOTE
cd ~/dev/${PROJECT_NAME}

# Create venv and install
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Create systemd service
sudo tee /etc/systemd/system/${PROJECT_NAME}.service > /dev/null << SERVICE
[Unit]
Description=${PROJECT_NAME}
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/dev/${PROJECT_NAME}
ExecStart=/home/ubuntu/dev/${PROJECT_NAME}/venv/bin/python ${ENTRY_POINT}
Restart=always
RestartSec=5
Environment=PORT=${PORT}

[Install]
WantedBy=multi-user.target
SERVICE

sudo systemctl daemon-reload
sudo systemctl enable ${PROJECT_NAME}
sudo systemctl restart ${PROJECT_NAME}

# Verify
sleep 2
systemctl is-active --quiet ${PROJECT_NAME} && echo "✅ Running" || echo "❌ Failed"
REMOTE
```

## Inputs Required

| Input | Description | Example |
|-------|-------------|---------|
| PROJECT_NAME | Directory name on oci-dev | my-api |
| PORT | Port the app listens on | 8080 |
| ENTRY_POINT | Main Python/Node file | app.py |
| SUBDOMAIN | (Optional) For public access | api |
| DOMAIN | (Optional) Domain | khamel.com |

## Outputs

- Project deployed to `~/dev/${PROJECT_NAME}/`
- Systemd service running and enabled
- (Optional) DNS record created
- (Optional) Traefik config for HTTPS

## Service Management

```bash
# Check status
ssh ubuntu@100.126.13.70 "systemctl status ${PROJECT_NAME}"

# View logs
ssh ubuntu@100.126.13.70 "journalctl -u ${PROJECT_NAME} -f"

# Restart
ssh ubuntu@100.126.13.70 "sudo systemctl restart ${PROJECT_NAME}"

# Stop
ssh ubuntu@100.126.13.70 "sudo systemctl stop ${PROJECT_NAME}"
```

## Adding Public Domain (Optional)

### 1. Cloudflare DNS

```bash
curl -X POST "https://api.cloudflare.com/client/v4/zones/${ZONE_ID}/dns_records" \
  -H "Authorization: Bearer ${CF_TOKEN}" \
  -d '{"type":"A","name":"${SUBDOMAIN}","content":"100.112.130.100","ttl":1,"proxied":false}'
```

### 2. Traefik Config

Create `~/github/homelab/services/traefik/config/${PROJECT_NAME}.yml`:

```yaml
http:
  routers:
    ${PROJECT_NAME}:
      rule: "Host(`${SUBDOMAIN}.${DOMAIN}`)"
      entryPoints:
        - websecure
      tls:
        certResolver: cloudflare
      service: ${PROJECT_NAME}
  services:
    ${PROJECT_NAME}:
      loadBalancer:
        servers:
          - url: "http://100.126.13.70:${PORT}"
```

## Rollback

```bash
# Stop and disable
ssh ubuntu@100.126.13.70 "sudo systemctl stop ${PROJECT_NAME} && sudo systemctl disable ${PROJECT_NAME}"

# Remove service file
ssh ubuntu@100.126.13.70 "sudo rm /etc/systemd/system/${PROJECT_NAME}.service && sudo systemctl daemon-reload"

# Remove project
ssh ubuntu@100.126.13.70 "rm -rf ~/dev/${PROJECT_NAME}"
```

## Anti-Patterns

- Deploying without testing locally first
- Hardcoding secrets (use environment variables)
- Not checking if port is already in use
- Forgetting to restart Traefik after config change
- Deploying large apps (use homelab for heavy workloads)

## Keywords

deploy, push to cloud, OCI, host, cloud, run externally, public, server
