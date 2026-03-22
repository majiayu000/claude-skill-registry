---
name: vps-deployment-stack
description: Deploy production-ready VPS infrastructure with Dokploy (PaaS), Traefik (reverse proxy with auto-TLS), Docker Compose, and Uptime Kuma (monitoring). Use when setting up a new VPS from scratch, configuring automatic HTTPS with Let's Encrypt, deploying Git-based applications with webhooks, or establishing monitoring infrastructure. Covers installation, DNS configuration, TLS setup, and validation from empty VPS to working system with zero-downtime deployments.
---

# VPS Deployment Stack

Deploy Dokploy + Traefik + Docker + Uptime Kuma on a single VPS with automatic HTTPS and monitoring.

## Prerequisites

- Fresh Ubuntu 22.04/24.04 VPS with 2GB+ RAM, 30GB+ disk
- Root/sudo SSH access
- Domain with DNS control (A records)
- Ports 80, 443, 3000 available: `sudo ss -tlnp | grep -E ':(80|443|3000)'`

## Quick Start: Empty VPS → Working System

### 1. Install Docker (5 min)

```bash
# Add Docker repository
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Verify
docker --version && docker compose version
sudo systemctl enable --now docker
```

### 2. Install Dokploy (3 min)

```bash
# Official installer (auto-configures Docker Swarm + Traefik)
curl -sSL https://dokploy.com/install.sh | sh

# Wait for startup
sleep 60

# Verify
docker ps --format "table {{.Names}}\t{{.Status}}"
# Expected: dokploy, traefik containers "Up"
```

Access Dokploy at `http://YOUR_VPS_IP:3000` and complete setup wizard (create admin account).

### 3. Configure DNS (15 min wait)

Add A records in your DNS provider:
```
deploy.yourdomain.com  →  YOUR_VPS_IP
status.yourdomain.com  →  YOUR_VPS_IP
app.yourdomain.com     →  YOUR_VPS_IP
```

Verify propagation:
```bash
dig deploy.yourdomain.com +short
# Should return: YOUR_VPS_IP
```

### 4. Setup Traefik TLS (5 min)

In Dokploy UI:
1. Settings → Server → Traefik Settings
2. Add Certificate Resolver:
   - Name: `letsencrypt`
   - Email: `your-email@example.com`
   - Challenge: TLS-ALPN-01
   - Storage: `/letsencrypt/acme.json`
3. Save and restart Traefik

**For applications, use these Traefik labels:**
```yaml
labels:
  - "traefik.enable=true"
  - "traefik.http.routers.APPNAME.rule=Host(`app.yourdomain.com`)"
  - "traefik.http.routers.APPNAME.entrypoints=websecure"
  - "traefik.http.routers.APPNAME.tls.certresolver=letsencrypt"
  - "traefik.http.services.APPNAME.loadbalancer.server.port=8080"
```

### 5. Deploy Uptime Kuma (5 min)

```bash
mkdir -p ~/kuma-data

cat > ~/docker-compose.kuma.yml << 'EOF'
version: '3.8'
services:
  uptime-kuma:
    image: louislam/uptime-kuma:2
    container_name: uptime-kuma
    restart: always
    volumes:
      - ./kuma-data:/app/data
    networks:
      - dokploy-network
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.kuma.rule=Host(`status.yourdomain.com`)"
      - "traefik.http.routers.kuma.entrypoints=websecure"
      - "traefik.http.routers.kuma.tls.certresolver=letsencrypt"
      - "traefik.http.services.kuma.loadbalancer.server.port=3001"

networks:
  dokploy-network:
    external: true
EOF

docker compose -f ~/docker-compose.kuma.yml up -d
```

### 6. Secure Dokploy Behind HTTPS (3 min)

In Dokploy UI:
- Settings → Server → Server Configuration
- Server Domain: `deploy.yourdomain.com`
- Save and restart Dokploy service

Or via CLI:
```bash
docker service update dokploy \
  --label-add "traefik.http.routers.dokploy.rule=Host(\`deploy.yourdomain.com\`)" \
  --label-add "traefik.http.routers.dokploy.entrypoints=websecure" \
  --label-add "traefik.http.routers.dokploy.tls.certresolver=letsencrypt"
```

### 7. Deploy Test Application (10 min)

In Dokploy UI:
1. New Project → Name: "test-apps"
2. Add Application:
   - Source: GitHub
   - Repository URL: `https://github.com/your-username/your-app`
   - Branch: `main`
   - Build Type: Nixpacks (auto-detect) or Dockerfile
3. Configure:
   - Domains → Add: `app.yourdomain.com`
   - Environment → Add variables
   - General → Port: 3000 (or app-specific)
4. Click "Deploy"
5. Monitor in Deployments tab

## Validation

### Health Checks
```bash
# 1. Containers running
docker ps --format "table {{.Names}}\t{{.Status}}"

# 2. TLS valid
echo | openssl s_client -connect deploy.yourdomain.com:443 2>/dev/null | openssl x509 -noout -dates

# 3. Dokploy API
curl -I https://deploy.yourdomain.com/api/health

# 4. Uptime Kuma
curl -I https://status.yourdomain.com

# 5. Docker Swarm
docker node ls
```

### Smoke Tests
```bash
# HTTP→HTTPS redirect
curl -I http://deploy.yourdomain.com
# Expected: 301/308 redirect

# Webhook deployment (get URL from Dokploy app settings)
curl -X POST https://deploy.yourdomain.com/api/webhooks/YOUR_ID
```

## Top 5 Failure Modes

### 1. Let's Encrypt Certificate Fails
**Symptoms:** Browser shows "Not Secure"

**Fix:**
```bash
# Check DNS resolves
dig deploy.yourdomain.com +short  # Must match VPS IP

# Reset certificates
sudo rm /letsencrypt/acme.json
sudo touch /letsencrypt/acme.json
sudo chmod 600 /letsencrypt/acme.json
docker restart $(docker ps -qf name=traefik)
```

### 2. App Build Fails
**Check:** Deployment logs in Dokploy UI

**Fix:**
- Verify Dockerfile exists at repo root
- Increase build timeout: App Settings → Advanced → 30m
- Check VPS has >1GB free RAM: `free -h`

### 3. 502 Bad Gateway
**Check:**
```bash
docker ps | grep your-app
docker logs your-app --tail 50
```

**Fix:**
- App must listen on `0.0.0.0` (not `127.0.0.1`)
- Verify Traefik label port matches app's actual port
- Ensure app is on `dokploy-network`: `docker network inspect dokploy-network`

### 4. Webhook Not Triggering
**Fix:**
- Test manually: `curl -X POST <webhook-url>`
- Regenerate webhook URL in Dokploy UI
- Check Git provider can reach VPS (firewall)

### 5. Out of Disk Space
**Fix:**
```bash
docker system prune -a -f --volumes
docker image prune -a -f
```

## Security Baseline

### Essential (Do on Day 1)
```bash
# 1. Firewall
sudo ufw allow 22/tcp && sudo ufw allow 80/tcp && sudo ufw allow 443/tcp
sudo ufw enable

# 2. Fix Docker bypassing firewall
sudo tee -a /etc/ufw/after.rules << 'EOF'
*filter
:DOCKER-USER - [0:0]
-A DOCKER-USER -j RETURN -s 10.0.0.0/8
-A DOCKER-USER -j RETURN -s 172.16.0.0/12
-A DOCKER-USER -j RETURN -s 192.168.0.0/16
-A DOCKER-USER -j DROP
COMMIT
EOF
sudo ufw reload

# 3. SSH hardening (see vps-daily-operations skill for full guide)
# Key-only auth, non-root, custom port

# 4. Container scanning
curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh -s -- -b /usr/local/bin
trivy image louislam/uptime-kuma:2
```

### Never Commit Secrets
- Use Dokploy's "Secret" checkbox for sensitive env vars
- Add `.env` to `.gitignore`
- Rotate credentials quarterly

## Monitoring Setup

In Uptime Kuma (https://status.yourdomain.com):

1. Create monitors:
   - Dokploy: HTTPS monitor for `deploy.yourdomain.com`, 60s interval
   - Test App: HTTPS monitor for `app.yourdomain.com`, 60s interval
   - VPS SSH: TCP monitor for `YOUR_VPS_IP:22`, 300s interval

2. Add notifications:
   - Settings → Notifications
   - Configure email/Slack/Discord
   - Test each channel

3. Create status page:
   - Status Pages → Add Page
   - Select monitors to display
   - Share public URL

## Reference Files

- **references/troubleshooting.md** - Extended troubleshooting guide with less common issues
- **references/github-actions-deploy.yml** - Complete CI/CD workflow template

## Related Skills

- **vps-daily-operations** - Daily health checks, backups, incident response, hardening
- **docker-development-workflow** - Local development, image optimization, CI/CD patterns
