---
name: frappe-ops-deployment
description: >
  Use when deploying Frappe/ERPNext to production, configuring Nginx or Supervisor, setting up Docker, enabling SSL, or hardening security.
  Prevents insecure deployments, missing reverse proxy config, and broken process management.
  Covers production setup, Nginx configuration, Supervisor/systemd, Docker Compose, Let's Encrypt SSL, firewall rules, security hardening.
  Keywords: deployment, production, nginx, supervisor, docker, ssl, letsencrypt, security, gunicorn, systemd.
license: MIT
compatibility: "Claude Code, Claude.ai Projects, Claude API. Frappe v14-v16."
metadata:
  author: OpenAEC-Foundation
  version: "2.0"
---

# Production Deployment

Deploy Frappe/ERPNext to production using either traditional (bench + Nginx + Supervisor) or Docker (frappe_docker + Compose). Frappe officially recommends Docker for new deployments.

## Quick Reference

```bash
# Traditional production setup (one command)
sudo bench setup production [frappe-user]

# What it configures:
# 1. Supervisor — process management (gunicorn, workers, Redis, socketio)
# 2. Nginx — reverse proxy, static files, websocket proxy
# 3. Sudoers — allows frappe-user to restart services

# Individual setup commands
bench setup supervisor          # Generate supervisor config
bench setup nginx               # Generate nginx config
bench setup sudoers $(whoami)   # Allow service restarts without password

# Symlink configs into system directories
sudo ln -s $(pwd)/config/supervisor.conf /etc/supervisor/conf.d/frappe-bench.conf
sudo ln -s $(pwd)/config/nginx.conf /etc/nginx/conf.d/frappe-bench.conf

# SSL setup
sudo -H bench setup lets-encrypt [site-name]
sudo -H bench setup lets-encrypt [site-name] --custom-domain [domain]

# DNS multitenancy (multiple sites on port 80/443)
bench config dns_multitenant on
bench setup nginx
sudo service nginx reload
```

---

## Deployment Decision Tree

```
Which deployment method?
|
+-- New server, minimal ops experience?
|   +-- Docker (frappe_docker) — recommended by Frappe
|
+-- Existing server with bench already installed?
|   +-- Traditional (bench setup production)
|
+-- Need custom Frappe apps or complex build?
|   +-- Docker with custom image build
|
+-- Cloud hosting (AWS/GCP/Azure)?
|   +-- Docker on VM or Kubernetes
|   +-- OR Frappe Cloud (managed)
|
+-- Single site or multi-site?
|   +-- Single site: standard setup
|   +-- Multi-site: DNS multitenancy required
```

---

## Traditional Deployment

### Process Architecture

```
Internet → Nginx (port 80/443)
               |
               +-- Static files served directly
               +-- /api, /app → Gunicorn (port 8000)
               +-- /socket.io → Node.js socketio (port 9000)

Supervisor manages:
  - frappe-bench-web (gunicorn)
  - frappe-bench-socketio (node)
  - frappe-bench-worker-short
  - frappe-bench-worker-default
  - frappe-bench-worker-long
  - frappe-bench-redis-cache
  - frappe-bench-redis-queue
  - frappe-bench-schedule (scheduler)
```

### Step-by-Step Setup

```bash
# 1. Install bench (as non-root user)
sudo pip3 install frappe-bench
bench init frappe-bench --frappe-branch version-15
cd frappe-bench

# 2. Create site
bench new-site mysite.example.com
bench --site mysite.example.com install-app erpnext

# 3. Production setup (configures nginx + supervisor + sudoers)
sudo bench setup production $(whoami)

# 4. Verify processes are running
sudo supervisorctl status

# 5. Verify nginx config
sudo nginx -t && sudo systemctl reload nginx
```

### Nginx Configuration

`bench setup nginx` generates `config/nginx.conf` with:
- Server block per site (DNS multitenancy)
- Proxy to gunicorn on port 8000
- WebSocket proxy to socketio on port 9000
- Static file serving from `sites/` directory
- Client max body size (default varies by version)

**ALWAYS disable default nginx site** to avoid port 80 conflicts:
```bash
sudo rm /etc/nginx/sites-enabled/default
# OR disable: sudo mv /etc/nginx/conf.d/default.conf /etc/nginx/conf.d/default.conf.bak
```

### Supervisor Configuration

`bench setup supervisor` generates `config/supervisor.conf` with:
- `--skip-redis` flag to skip Redis if managed externally

For CentOS/RHEL: use `.ini` extension instead of `.conf` for supervisor configs.

---

## SSL / HTTPS

### Let's Encrypt (Recommended)

```bash
# Automated setup with cron renewal
sudo -H bench setup lets-encrypt mysite.example.com

# For custom domain (site name differs from domain)
sudo -H bench setup lets-encrypt mysite.example.com --custom-domain www.example.com

# Manual renewal
sudo bench renew-lets-encrypt
```

**Prerequisites**:
- DNS multitenancy enabled (`bench config dns_multitenant on`)
- Domain resolves to server IP
- Port 80 open for ACME challenge
- Root/sudo access

**Certificate locations**: `/etc/letsencrypt/live/example.com/`
- `fullchain.pem` — certificate + chain
- `privkey.pem` — private key

Certificates expire every 90 days. The setup command adds a monthly cron for renewal.

### Custom SSL Certificate

```bash
# 1. Place certificate files
sudo mkdir -p /etc/nginx/conf.d/ssl
sudo cp certificate.crt /etc/nginx/conf.d/ssl/
sudo cp private.key /etc/nginx/conf.d/ssl/
sudo chmod 600 /etc/nginx/conf.d/ssl/private.key

# 2. Configure site
bench set-config ssl_certificate "/etc/nginx/conf.d/ssl/certificate.crt"
bench set-config ssl_certificate_key "/etc/nginx/conf.d/ssl/private.key"

# 3. Regenerate and reload
bench setup nginx
sudo systemctl reload nginx
```

All HTTP traffic is automatically redirected to HTTPS after SSL is configured.

---

## DNS Multitenancy (Multi-Site)

```bash
# Enable DNS-based site routing
bench config dns_multitenant on

# Create sites with domain names
bench new-site site1.example.com
bench new-site site2.example.com

# Regenerate nginx (creates server blocks per site)
bench setup nginx
sudo systemctl reload nginx
```

ALWAYS use the actual domain as the site name. Nginx routes requests to the correct site based on the `Host` header.

---

## Docker Deployment

### Architecture (frappe_docker)

```
Docker Compose Services:
  - configurator  — initializes DB/Redis config (runs once)
  - backend       — Frappe/ERPNext application server (gunicorn)
  - frontend      — Nginx reverse proxy
  - websocket     — Node.js Socket.IO server
  - queue-short   — RQ worker for short jobs
  - queue-long    — RQ worker for long jobs
  - (external)    — MariaDB/PostgreSQL + Redis (separate containers or managed)

Shared Volume:
  - sites:/home/frappe/frappe-bench/sites (persistent data)
```

### Production Docker Compose

```bash
# Clone frappe_docker
git clone https://github.com/frappe/frappe_docker.git
cd frappe_docker

# Use compose.yaml for production
# Key environment variables:
#   DB_HOST, DB_PORT — database connection
#   REDIS_CACHE, REDIS_QUEUE — Redis endpoints
#   FRAPPE_SITE_NAME_HEADER — for multi-site routing
#   PROXY_READ_TIMEOUT — upstream timeout
#   CLIENT_MAX_BODY_SIZE — upload limit (default 50m)

docker compose -f compose.yaml up -d
```

### Custom Image Build

```bash
# Build custom image with your apps
export APPS_JSON='[
  {"url":"https://github.com/frappe/erpnext","branch":"version-15"},
  {"url":"https://github.com/your-org/custom-app","branch":"main"}
]'

docker build \
  --build-arg APPS_JSON_BASE64=$(echo $APPS_JSON | base64 -w 0) \
  --tag your-registry/custom-erpnext:latest \
  images/custom/
```

---

## Security Hardening

### Firewall (UFW)

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
# NEVER expose ports 8000, 9000, 6379, 3306 to the internet
```

### Fail2Ban

```bash
sudo apt install fail2ban
sudo systemctl enable fail2ban

# /etc/fail2ban/jail.local
# [sshd]
# enabled = true
# maxretry = 5
# bantime = 3600
```

### Redis Authentication

```bash
# Secure Redis for multi-bench environments
bench create-rq-users --set-admin-password
# Generates unique passwords per bench for Redis auth
```

### Additional Hardening

- ALWAYS disable root SSH login (`PermitRootLogin no` in `/etc/ssh/sshd_config`)
- ALWAYS use SSH key authentication, disable password auth
- NEVER run bench as root — create a dedicated `frappe` user
- ALWAYS keep system packages updated (`sudo apt update && sudo apt upgrade`)
- ALWAYS set `ALLOW_CORS` only to trusted domains in `site_config.json`

---

## Zero-Downtime Updates

```bash
# Traditional deployment
bench update --pull --patch --build --requirements
# Supervisor auto-restarts workers after update

# Docker deployment
# 1. Pull new image
docker compose pull
# 2. Recreate containers (rolling)
docker compose up -d --no-deps backend websocket queue-short queue-long
# 3. Run migrations
docker compose exec backend bench --site mysite.example.com migrate
```

---

## Version Differences

| Feature | v14 | v15 | v16 |
|---|---|---|---|
| Docker recommended | No | Official recommendation | Yes |
| `create-rq-users` | No | Yes | Yes |
| ARM64 Docker images | No | Yes | Yes |
| Site-level logs | v13+ | Yes | Yes |
| `extend_doctype_class` | No | No | Yes |

---

## Reference Files

| File | Contents |
|---|---|
| [examples.md](references/examples.md) | Complete deployment scripts and configs |
| [anti-patterns.md](references/anti-patterns.md) | Common deployment mistakes |
| [workflows.md](references/workflows.md) | Step-by-step deployment workflows |

## Related Skills

- `frappe-ops-backup` — Backup and disaster recovery
- `frappe-ops-performance` — Performance tuning
- `frappe-ops-bench` — Bench CLI reference
- `frappe-ops-upgrades` — Version upgrade procedures
