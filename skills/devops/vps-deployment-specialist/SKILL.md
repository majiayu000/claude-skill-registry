---
name: vps-deployment-specialist
description: |
  Full-stack VPS deployment: Docker, Caddy/Nginx, SSL, CI/CD, monitoring, security hardening.
  Use for server setup, deployment failures, SSL issues, Docker problems,
  reverse proxy config, GitHub Actions CI/CD, permission errors, firewall config.
  Triggers on: "deploy failed", "SSL error", "502 bad gateway", "connection refused",
  "docker build failed", "permission denied", "CI/CD", "Caddy", "Nginx", "firewall",
  "fail2ban", "UFW", "SSH", "server hardening", "reverse proxy".
---

# VPS Deployment Specialist Skill

Full-stack VPS deployment covering server setup, Docker orchestration, reverse proxy (Nginx/Caddy), SSL/TLS, CI/CD pipelines, monitoring, and troubleshooting.

## Trigger Patterns

- Deploy failed / deployment error
- SSL certificate error / HTTPS not working
- 502 Bad Gateway / 503 Service Unavailable
- Connection refused / timeout
- Docker build failed / container won't start
- Permission denied (SSH, Docker, files)
- GitHub Actions CI/CD issues
- Caddy / Nginx configuration
- Firewall / UFW blocking connections
- Server hardening / security setup

## Quick Diagnostics

### First Steps (Always Start Here)

```bash
# 1. Check service status
docker ps                        # Running containers
systemctl status docker          # Docker daemon
systemctl status caddy           # Reverse proxy (if using Caddy)

# 2. Check logs
docker compose logs -f --tail=100  # Container logs
journalctl -u docker -n 50         # Docker daemon logs
tail -f /var/log/syslog            # System logs

# 3. Verify network
curl -I localhost                # Local endpoint
ss -tlnp                         # Listening ports
ufw status                       # Firewall rules

# 4. Check resources
df -h                            # Disk space
free -h                          # Memory
docker system df                 # Docker disk usage
```

---

## 1. Server Initial Setup & Hardening

### Create Deploy User

```bash
# Create user with sudo
adduser deploy
usermod -aG sudo deploy

# Set up SSH key auth
mkdir -p /home/deploy/.ssh
chmod 700 /home/deploy/.ssh
echo "YOUR_PUBLIC_KEY" >> /home/deploy/.ssh/authorized_keys
chmod 600 /home/deploy/.ssh/authorized_keys
chown -R deploy:deploy /home/deploy/.ssh
```

### Harden SSH (/etc/ssh/sshd_config)

```bash
# Disable root login
PermitRootLogin no

# Disable password auth (key only)
PasswordAuthentication no
PubkeyAuthentication yes

# Use strong key types
HostKeyAlgorithms ssh-ed25519,rsa-sha2-512

# Optional: Change port (obscurity, not security)
# Port 2222

# Apply changes
systemctl restart sshd
```

### Install Docker

```bash
# Official Docker install
curl -fsSL https://get.docker.com | sh
usermod -aG docker deploy
# Log out and back in for group to take effect
```

### Configure UFW Firewall

```bash
ufw default deny incoming
ufw default allow outgoing
ufw allow 22/tcp    # SSH (or custom port)
ufw allow 80/tcp    # HTTP
ufw allow 443/tcp   # HTTPS
ufw enable

# Verify
ufw status verbose
```

### Install Fail2ban

```bash
apt install fail2ban -y

# Create jail config
cat > /etc/fail2ban/jail.local << 'EOF'
[sshd]
enabled = true
port = ssh
filter = sshd
logpath = /var/log/auth.log
maxretry = 3
findtime = 600
bantime = 3600
# Progressive: increase ban time on repeat offenders
bantime.increment = true
bantime.factor = 24
EOF

systemctl enable fail2ban
systemctl start fail2ban
```

### Enable Automatic Security Updates

```bash
apt install unattended-upgrades -y
dpkg-reconfigure -plow unattended-upgrades
```

### Set Up Swap (if low RAM)

```bash
fallocate -l 2G /swapfile
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile
echo '/swapfile none swap sw 0 0' >> /etc/fstab
```

---

## 2. Docker Configuration

### Common Issues

| Issue | Solution |
|-------|----------|
| Build context too large | Add `.dockerignore` with node_modules, .git, etc. |
| Layer caching broken | Order Dockerfile: deps first, code last |
| Network in containers | Use Docker networks, check DNS |
| Volume permissions | Match UID/GID or use named volumes |
| Running as root | Add USER directive, create non-root user |

### Multi-stage Build Pattern (Secure)

```dockerfile
# Build stage
FROM node:20-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Production stage
FROM nginx:alpine
# Create non-root user
RUN addgroup -g 1001 -S appgroup && \
    adduser -u 1001 -S appuser -G appgroup
COPY --from=build --chown=appuser:appgroup /app/dist /usr/share/nginx/html
USER appuser
EXPOSE 80
```

### Security Best Practices (2025-2026)

```dockerfile
# Use specific versions, not :latest
FROM node:20.10-alpine AS build

# Enable BuildKit for faster builds
# DOCKER_BUILDKIT=1 docker build .

# Use cache mounts for package managers
RUN --mount=type=cache,target=/root/.npm npm ci

# Health check
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost/ || exit 1
```

### Image Scanning

```bash
# Docker Scout (built-in)
docker scout cves <image>

# Trivy (popular open source)
trivy image <image>
```

### Docker Content Trust (signed images)

```bash
export DOCKER_CONTENT_TRUST=1
docker pull nginx:alpine  # Only pulls if signed
```

---

## 3. Reverse Proxy (Caddy)

**Why Caddy:** Automatic HTTPS (Let's Encrypt/ZeroSSL), HTTP/3 support, ~15-25% the config size of nginx, built-in health checks, graceful reloads.

### Production Setup with Health Checks

```caddyfile
example.com {
    reverse_proxy app:80 {
        health_uri /health
        health_interval 30s
        health_timeout 5s
    }
    encode gzip zstd

    header {
        Strict-Transport-Security "max-age=31536000; includeSubDomains"
        X-Content-Type-Options "nosniff"
        X-Frame-Options "DENY"
        Referrer-Policy "strict-origin-when-cross-origin"
        -Server  # Remove server header
    }
}
```

### WebSocket + API Routing

```caddyfile
example.com {
    handle /api/* {
        reverse_proxy backend:3000
    }
    handle /ws/* {
        reverse_proxy backend:3000 {
            header_up Connection {http.request.header.Connection}
            header_up Upgrade {http.request.header.Upgrade}
        }
    }
    handle {
        reverse_proxy frontend:80
    }
}
```

### Rate Limiting & Circuit Breaking

```caddyfile
example.com {
    # Rate limit: 100 requests per minute per IP
    rate_limit {remote.ip} 100r/m

    reverse_proxy app:80 {
        lb_try_duration 5s
        lb_try_interval 250ms
        fail_duration 30s
    }
}
```

### Trusted Proxies (important for real IP)

```caddyfile
{
    servers {
        trusted_proxies static 10.0.0.0/8 172.16.0.0/12 192.168.0.0/16
    }
}
```

### Local SSL with sslip.io

```caddyfile
# Use IP-based domain for automatic SSL
flowstate.84.46.253.137.sslip.io {
    reverse_proxy app:80
}
```

---

## 4. Reverse Proxy (Nginx)

### Basic Setup

```nginx
server {
    listen 80;
    server_name example.com;

    location / {
        proxy_pass http://app:80;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### SSL with Let's Encrypt

```nginx
server {
    listen 443 ssl http2;
    server_name example.com;

    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;

    # Modern SSL config
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;
    ssl_prefer_server_ciphers off;

    location / {
        proxy_pass http://app:80;
    }
}
```

### WebSocket Support

```nginx
location /ws/ {
    proxy_pass http://backend:3000;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
}
```

---

## 5. SSL/TLS Configuration

### Caddy (Automatic)

Caddy handles SSL automatically. Just use a domain name:

```caddyfile
example.com {
    reverse_proxy app:80
}
# SSL is automatically configured
```

### Manual with Certbot (Nginx)

```bash
# Install
apt install certbot python3-certbot-nginx -y

# Generate cert
certbot --nginx -d example.com

# Auto-renewal (in cron)
0 0 * * * certbot renew --quiet
```

### Testing SSL

```bash
# Check certificate
openssl s_client -connect example.com:443 -servername example.com

# Test configuration
curl -vI https://example.com

# Check expiry
echo | openssl s_client -connect example.com:443 2>/dev/null | openssl x509 -noout -dates
```

---

## 6. GitHub Actions CI/CD

### CRITICAL: Supply Chain Security (March 2025)

The tj-actions/changed-files action was compromised, exposing secrets for 23,000+ repos. **Best practices:**
- Pin actions to SHA, not version tags
- Review third-party actions before use
- Use OIDC instead of long-lived secrets

### Secure Deploy Workflow

```yaml
name: Deploy to VPS
on:
  push:
    branches: [master]

# Explicitly declare minimal permissions
permissions:
  contents: read

jobs:
  deploy:
    runs-on: ubuntu-latest
    # Use environment for production secrets
    environment: production
    steps:
      # Pin to SHA for security
      - uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11 # v4.1.1

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Build
        run: |
          npm ci
          npm run build

      - name: Deploy via SSH
        uses: appleboy/ssh-action@v1
        with:
          host: ${{ secrets.VPS_HOST }}
          username: ${{ secrets.VPS_USER }}
          key: ${{ secrets.SSH_PRIVATE_KEY }}
          script: |
            cd /app
            docker compose pull
            docker compose up -d --build
```

### Secrets Best Practices (2025-2026)

| Practice | Why |
|----------|-----|
| Rotate every 30-90 days | Limits exposure window |
| Use OIDC over long-lived tokens | Eliminates static credentials |
| Environment secrets for prod | Requires reviewer approval |
| Never use structured data (JSON/YAML) | May not be redacted in logs |
| Pin actions to SHA | Prevents supply chain attacks |

### OIDC for Cloud Providers (no secrets needed)

```yaml
permissions:
  id-token: write
  contents: read

jobs:
  deploy:
    steps:
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::123456789:role/github-actions
          aws-region: us-east-1
```

---

## 7. Docker Compose Production

```yaml
version: '3.8'

services:
  caddy:
    image: caddy:alpine
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./Caddyfile:/etc/caddy/Caddyfile:ro
      - caddy_data:/data
      - caddy_config:/config
    depends_on:
      app:
        condition: service_healthy

  app:
    build: .
    restart: unless-stopped
    environment:
      - NODE_ENV=production
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost/"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: '0.5'

volumes:
  caddy_data:
  caddy_config:
```

---

## 8. Monitoring & Health Checks

### Docker Health Check (Dockerfile)

```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s \
  CMD curl -f http://localhost/ || exit 1
```

### Log Aggregation

```bash
# View all compose logs
docker compose logs -f

# Specific service with timestamps
docker compose logs -f --timestamps app

# Last 100 lines
docker compose logs --tail=100 app
```

### Fail2ban Monitoring

```bash
# Check banned IPs
fail2ban-client status sshd

# Unban an IP
fail2ban-client set sshd unbanip 1.2.3.4

# View ban log
tail -f /var/log/fail2ban.log
```

### Resource Monitoring

```bash
# Disk usage (alert at 80%)
df -h | awk '$5 > 80 {print}'

# Memory usage
free -h

# Docker disk usage
docker system df

# Clean up unused resources
docker system prune -a --volumes
```

### Simple Uptime Monitoring

- **Uptime Kuma** - Self-hosted, easy setup
- **Better Uptime** - SaaS with free tier
- Simple curl check in cron:

```bash
*/5 * * * * curl -sf https://example.com/health || echo "Site down" | mail -s "Alert" admin@example.com
```

---

## 9. Troubleshooting Decision Tree

```
Deployment failed
├── Build failed?
│   ├── npm ci failed → Check package-lock.json, clear cache
│   ├── Docker build failed → Check Dockerfile, .dockerignore
│   └── Out of space → docker system prune, expand disk
├── Deploy succeeded but site down?
│   ├── 502 Bad Gateway → App container not running/healthy
│   │   └── Check: docker ps, docker compose logs app
│   ├── Connection refused → Firewall, wrong port binding
│   │   └── Check: ufw status, ss -tlnp
│   ├── SSL error → Certificate expired/misconfigured
│   │   └── Check: openssl s_client, certbot certificates
│   └── Timeout → Resource exhaustion, infinite loop
│       └── Check: free -h, top, docker stats
├── SSH failed?
│   ├── Permission denied → Check key, known_hosts, sshd_config
│   └── Connection timeout → Firewall, wrong IP, SSH port
└── Works locally but not on VPS?
    ├── Environment variables missing → Check .env on VPS
    ├── Port conflicts → ss -tlnp, check other services
    └── Different file paths → Check absolute paths in config
```

---

## 10. Quick Commands Reference

| Task | Command |
|------|---------|
| Check running containers | `docker ps` |
| View logs | `docker compose logs -f` |
| Rebuild and restart | `docker compose up -d --build` |
| Check disk space | `df -h` |
| Check memory | `free -h` |
| Check listening ports | `ss -tlnp` |
| Test local endpoint | `curl -I localhost` |
| Restart compose stack | `docker compose restart` |
| Remove unused images | `docker image prune -a` |
| Check firewall | `ufw status` |
| Check fail2ban | `fail2ban-client status` |
| View SSH attempts | `journalctl -u sshd -n 50` |

---

## 11. Rollback Strategy

```bash
# Option 1: Git-based rollback
git checkout <previous-commit>
docker compose up -d --build

# Option 2: Docker image tags (if using registry)
docker compose pull  # Gets :latest
docker compose up -d

# Option 3: Keep backup of working state
cp docker-compose.yml docker-compose.yml.backup
cp Caddyfile Caddyfile.backup

# Restore from backup
cp docker-compose.yml.backup docker-compose.yml
docker compose up -d --build
```

---

## Related Skills

- `supabase-debugger` - Database and Supabase-specific issues
- `dev-debugging` - Application-level Vue/Pinia debugging
- `tauri-debugger` - Desktop app deployment issues

## Sources

- [Docker Best Practices 2025](https://thinksys.com/devops/docker-best-practices/)
- [Container Security 2026](https://jeevisoft.com/blogs/2025/10/container-security-best-practices-for-2025/)
- [Caddy Documentation](https://caddyserver.com/docs/caddyfile/patterns)
- [GitHub Actions Security](https://www.stepsecurity.io/blog/github-actions-security-best-practices)
- [VPS Security Hardening 2025](https://retzor.com/blog/vps-security-hardening-25-point-checklist-for-2025/)
- [Fail2ban VPS Guide](https://vps.do/fail2ban-vps/)
