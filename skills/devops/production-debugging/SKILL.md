---
name: production-debugging
description: Connect to and debug the Orient production server on Oracle Cloud. Use this skill when asked to check production logs, restart containers, debug deployment issues, SSH into the server, view container status, troubleshoot 502 errors, rollback deployments, fix WhatsApp pairing issues, debug dashboard loading issues, or investigate why production is down. Covers SSH access, Docker container management, log analysis, Express 5 errors, SPA asset issues, and deployment troubleshooting.
---

# Production Server Debugging

Debug and manage the Orient production environment on Oracle Cloud.

## Prerequisites

SSH access requires these environment variables (stored in `.env`):

- `OCI_HOST` - Oracle Cloud server IP (default: `152.70.172.33`)
- `OCI_USER` - SSH username (default: `opc`)
- SSH key configured in `~/.ssh/id_rsa`

**Quick setup** (if not in .env):

```bash
export OCI_HOST=152.70.172.33
export OCI_USER=opc
```

## SSH Connection

### Connect to Production

```bash
ssh -o StrictHostKeyChecking=no $OCI_USER@$OCI_HOST
```

### Run Remote Command

```bash
ssh -o StrictHostKeyChecking=no $OCI_USER@$OCI_HOST "command"
```

### Example: Check if containers are running

```bash
ssh $OCI_USER@$OCI_HOST "docker ps --format 'table {{.Names}}\t{{.Status}}'"
```

## Server Directory Structure

```
~/orient/
├── docker/           # Compose files and configs
│   ├── docker-compose.yml
│   ├── docker-compose.v2.yml
│   ├── docker-compose.prod.yml
│   ├── docker-compose.r2.yml
│   ├── nginx-ssl.conf
│   └── deploy-server.sh
├── data/             # Persistent data (volumes)
├── logs/             # Application logs
├── backups/          # Deployment backups
└── .env              # Environment variables
```

Working directory for Docker commands:

```bash
cd ~/orient/docker
```

## Container Overview

| Container             | Port       | Purpose                        |
| --------------------- | ---------- | ------------------------------ |
| orienter-nginx        | 80, 443    | Reverse proxy, SSL termination |
| orienter-dashboard    | 4098       | Dashboard web app + API        |
| orienter-bot-whatsapp | 4097       | WhatsApp bot + QR/pairing      |
| orienter-opencode     | 4099, 8765 | AI agent API + OAuth callback  |
| orienter-postgres     | 5432       | Database                       |

## Container Logs

### View Recent Logs

```bash
# Core containers
docker logs orienter-dashboard --tail 100
docker logs orienter-bot-whatsapp --tail 100
docker logs orienter-opencode --tail 100
docker logs orienter-nginx --tail 50
```

### Follow Logs in Real-Time

```bash
docker logs -f orienter-dashboard
```

### Logs Since Specific Time

```bash
docker logs orienter-dashboard --since 1h
docker logs orienter-dashboard --since "2024-01-07T10:00:00"
```

### Parse JSON Logs

```bash
docker logs orienter-dashboard --tail 50 2>&1 | jq -R 'fromjson? // .'
```

### Search for Errors

```bash
docker logs orienter-dashboard 2>&1 | grep -i error | tail -20
```

## Quick Debugging Reference

| Issue                        | Command                                                                              |
| ---------------------------- | ------------------------------------------------------------------------------------ |
| Check all containers         | `docker ps -a`                                                                       |
| Container crash loop         | `docker logs <container> --tail 100`                                                 |
| View nginx errors            | `docker logs orienter-nginx --tail 50`                                               |
| Check dashboard logs         | `docker logs orienter-dashboard --tail 100`                                          |
| Check OpenCode logs          | `docker logs orienter-opencode --tail 100`                                           |
| Restart dashboard            | `docker restart orienter-dashboard`                                                  |
| Check database               | `docker exec orienter-postgres psql -U aibot -c "SELECT 1"`                          |
| View env vars                | `cat ~/orient/.env`                                                                  |
| Check container env vars     | `docker exec <container> env \| grep <VAR_NAME>`                                     |
| Missing env var (crash loop) | Add to .env, then `docker compose --env-file ../.env -f compose.yml up -d <service>` |
| Check GitHub Actions         | `gh run list --limit 5` (run locally)                                                |
| WhatsApp pairing stuck       | `docker restart orienter-bot-whatsapp`                                               |
| WhatsApp factory reset       | `rm -rf ~/orient/data/whatsapp-auth/* && docker restart orienter-bot-whatsapp`       |

## Common Production Issues

### 1. Dashboard Container Crash Loop

**Symptoms**: Dashboard shows "Restarting" status, nginx returns 502

**Check logs**:

```bash
ssh $OCI_USER@$OCI_HOST "docker logs orienter-dashboard --tail 100 2>&1"
```

**Common causes**:

#### Express 5 / path-to-regexp Error

**Error**: `TypeError: Missing parameter name at index 1: *`

This happens when using bare `*` wildcards in Express 5 routes:

```typescript
// BROKEN
app.get('*', (req, res) => { ... });

// FIXED
app.get('/{*splat}', (req, res) => { ... });
```

**Fix**: Update the SPA catch-all route in `packages/dashboard/src/server/index.ts`

#### Database Connection Error

**Error**: `ECONNREFUSED` or `connection refused`

```bash
# Check postgres is running
docker ps | grep postgres

# Check DATABASE_URL
docker exec orienter-dashboard env | grep DATABASE_URL
```

### 2. Dashboard Assets Not Loading (text/html error)

**Symptoms**: Browser console shows:

```
Failed to load module script: Expected a JavaScript-or-Wasm module script
but the server responded with a MIME type of "text/html"
```

**Cause**: Nginx is incorrectly proxying asset requests

**Debug**:

```bash
# Check what content-type is returned for JS files
curl -sI "https://app.orient.bot/dashboard/assets/index-*.js" | grep content-type

# Expected: content-type: text/javascript; charset=utf-8
# If: content-type: text/html -> nginx routing issue
```

### 3. 502 Bad Gateway

**Check which service is down**:

```bash
docker ps --format "table {{.Names}}\t{{.Status}}"
```

**Check nginx upstream**:

```bash
docker logs orienter-nginx --tail 20 | grep -i "upstream\|502"
```

**Common causes**:

- Dashboard not started (crash loop)
- Wrong port in nginx config
- Container name mismatch

### 4. WhatsApp Pairing Issues

**Symptoms**:

- Dashboard shows "Connection Closed" when requesting pairing code
- QR code stops refreshing
- Logs show `QR refs attempts ended` error

**Quick fix**:

```bash
ssh $OCI_USER@$OCI_HOST "docker restart orienter-bot-whatsapp"
```

**Full reset**:

```bash
ssh $OCI_USER@$OCI_HOST "rm -rf /home/opc/orient/data/whatsapp-auth/* && docker restart orienter-bot-whatsapp"
```

**Diagnosis**:

```bash
ssh $OCI_USER@$OCI_HOST "docker logs orienter-bot-whatsapp --tail 100 2>&1 | grep -i -E '(pair|code|connection|closed|error)'"
```

### 5. Missing Environment Variables (Crash Loop)

**Symptoms**: Container in crash loop with "Restarting" status, logs show missing environment variable errors

**Example error**:

```
Error: DASHBOARD_JWT_SECRET environment variable is required
```

**Common missing variables**:

- `DASHBOARD_JWT_SECRET` (production) or `DASHBOARD_JWT_SECRET_STAGING` (staging)
- `DATABASE_URL`
- OAuth credentials (`GOOGLE_OAUTH_CLIENT_ID`, etc.)
- API keys (Anthropic, OpenAI, etc.)

**Quick checklist for staging environment**:

```bash
# Check if variable exists in .env
ssh $OCI_USER@$OCI_HOST "grep DASHBOARD_JWT_SECRET_STAGING /home/opc/orient/.env"

# Check what env vars the container actually has
ssh $OCI_USER@$OCI_HOST "docker exec orienter-dashboard-staging env | grep DASHBOARD"
```

**Critical knowledge about environment variables**:

1. **Staging uses \_STAGING suffix**: Staging containers expect environment variables with `_STAGING` suffix
   - Production: `DASHBOARD_JWT_SECRET`
   - Staging: `DASHBOARD_JWT_SECRET_STAGING`

2. **docker restart does NOT reload .env**: Simply restarting a container won't pick up new environment variables

   ```bash
   # WRONG - Won't reload env vars
   docker restart orienter-dashboard-staging

   # CORRECT - Recreates container with new env vars
   cd ~/orient/docker
   docker compose --env-file ../.env -f docker-compose.v2.yml -f docker-compose.staging.yml up -d dashboard
   ```

3. **docker-compose needs --env-file flag**: When .env is in parent directory, must specify explicitly

**Fix missing environment variables**:

```bash
# 1. Add missing variable to .env file
ssh $OCI_USER@$OCI_HOST "echo 'DASHBOARD_JWT_SECRET_STAGING=\"your-secret-here\"' >> /home/opc/orient/.env"

# 2. Recreate container with updated env (from docker directory)
ssh $OCI_USER@$OCI_HOST "cd /home/opc/orient/docker && docker compose --env-file ../.env -f docker-compose.v2.yml -f docker-compose.staging.yml up -d dashboard"

# 3. Verify container is healthy
ssh $OCI_USER@$OCI_HOST "docker ps | grep dashboard"

# 4. Check logs for successful startup
ssh $OCI_USER@$OCI_HOST "docker logs orienter-dashboard-staging --tail 20"
```

### 7. SSH Command Not Found (Monitoring Failure)

**Symptoms**: Monitoring page shows "Failed to load server metrics" with error logs showing:

```
/bin/sh: ssh: not found
```

**Cause**: The dashboard container doesn't have `openssh-client` installed. This is required for the monitoring service which SSHes into the production server to collect metrics.

**Quick check**:

```bash
# Verify SSH is available in container
docker exec orienter-dashboard which ssh
# Expected: /usr/bin/ssh
# If empty or "not found": SSH client missing
```

**Fix for Dockerfile**: The `packages/dashboard/Dockerfile` must include `openssh-client` in the alpine packages:

```dockerfile
# In the runner stage
RUN apk add --no-cache curl bash openssh-client
```

**Workaround for staging** (build patched image locally):

```bash
# 1. Build a patched image with SSH support
cd ~/orient
docker build -t dashboard-staging-ssh -f packages/dashboard/Dockerfile .

# 2. Update staging compose to use local image
sed -i 's|image: ghcr.io/orient-code/orient/dashboard:staging|image: dashboard-staging-ssh|' docker/docker-compose.staging.yml

# 3. Recreate container
cd ~/orient/docker
docker compose --env-file ../.env -f docker-compose.v2.yml -f docker-compose.staging.yml up -d dashboard
```

### 8. SSH Key Mounting for Containers

**Problem**: Container needs SSH access to production server for monitoring, but SSH keys need proper permissions.

**Docker Compose configuration**:

```yaml
# In docker-compose.v2.yml
dashboard:
  environment:
    - SSH_KEY_PATH=/app/.ssh/id_rsa
  volumes:
    # Mount SSH key from docker/.ssh directory (NOT ~/.ssh which has permission issues)
    - ./.ssh:/app/.ssh:ro
```

**Setup steps on server**:

```bash
# 1. Create docker/.ssh directory
mkdir -p ~/orient/docker/.ssh

# 2. Generate or copy SSH key (must be readable by container's non-root user)
ssh-keygen -t rsa -f ~/orient/docker/.ssh/id_rsa -N ""

# 3. Set readable permissions (container runs as uid 1001)
chmod 644 ~/orient/docker/.ssh/id_rsa
chmod 644 ~/orient/docker/.ssh/id_rsa.pub

# 4. Add public key to authorized_keys for localhost access
cat ~/orient/docker/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys

# 5. Recreate container to pick up the mount
cd ~/orient/docker
docker compose --env-file ../.env -f docker-compose.v2.yml up -d dashboard
```

**Why `./.ssh` instead of `~/.ssh`?**

- Tilde (`~`) doesn't expand in docker-compose volume paths
- User's `~/.ssh` typically has strict permissions (600) that block container access
- Container runs as non-root user (nodejs, uid 1001), needs readable permissions

**Required environment variables** (in `.env`):

```bash
OCI_HOST=152.70.172.33   # or SSH_HOST
OCI_USER=opc             # or SSH_USER
# SSH_KEY_PATH is set in compose file: /app/.ssh/id_rsa
```

**Verify SSH works from container**:

```bash
docker exec orienter-dashboard ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5 -i /app/.ssh/id_rsa opc@152.70.172.33 'echo SSH works'
```

### 9. Container Environment Variable Reload

**Critical**: `docker restart` does NOT reload environment variables from `.env`. You must recreate the container.

**Wrong approach** (env vars won't update):

```bash
# This won't pick up new .env values!
docker restart orienter-dashboard
```

**Correct approach** (recreates container with fresh env):

```bash
cd ~/orient/docker
docker compose --env-file ../.env -f docker-compose.v2.yml -f docker-compose.prod.yml up -d dashboard
```

**For staging containers**:

```bash
cd ~/orient/docker
docker compose --env-file ../.env -f docker-compose.v2.yml -f docker-compose.staging.yml up -d dashboard
```

**Verify environment variables loaded**:

```bash
# Check specific variable
docker exec orienter-dashboard env | grep SSH_KEY_PATH
docker exec orienter-dashboard env | grep OCI_HOST

# For staging
docker exec orienter-dashboard-staging env | grep SSH_KEY_PATH
```

**Common mistake with staging**: Forgetting the `_STAGING` suffix for environment variables:

- Production uses: `DASHBOARD_JWT_SECRET`
- Staging uses: `DASHBOARD_JWT_SECRET_STAGING`

### 6. Deployment Failure

**Check recent GitHub Actions**:

```bash
gh run list --limit 5
gh run view <run-id>
```

**Check which images were built**:

```bash
gh run view <run-id> | grep -E "Build.*Image"
```

If builds show `0s` with `-` prefix, they were skipped (no changes detected).

**Force rebuild if needed**:

```bash
gh workflow run deploy.yml -f force_build_all=true
```

## Container Management

### List Running Containers

```bash
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

### Restart a Container

```bash
docker restart orienter-dashboard
docker restart orienter-bot-whatsapp
docker restart orienter-opencode
docker restart orienter-nginx
```

### Restart All Services

```bash
cd ~/orient/docker
COMPOSE_FILES="-f docker-compose.v2.yml -f docker-compose.prod.yml -f docker-compose.r2.yml"
docker compose ${COMPOSE_FILES} restart
```

### Execute Command in Container

```bash
docker exec -it orienter-dashboard sh
docker exec -it orienter-opencode bash
docker exec orienter-postgres psql -U aibot -d whatsapp_bot
```

### Check Container Files

```bash
# Check dashboard assets exist
docker exec orienter-dashboard ls -la /app/packages/dashboard/public/assets/

# Check nginx config
docker exec orienter-nginx cat /etc/nginx/conf.d/default.conf
```

### View Container Resource Usage

```bash
docker stats --no-stream
```

### Inspect Container

```bash
docker inspect orienter-dashboard | jq '.[0].State'
```

## Health Checks

### Verify All Services

```bash
# Nginx
curl -sf https://app.orient.bot/health && echo "Nginx: OK" || echo "Nginx: FAIL"

# Dashboard
curl -sf https://app.orient.bot/dashboard/api/health && echo "Dashboard: OK" || echo "Dashboard: FAIL"

# OpenCode
curl -sf https://code.orient.bot/global/health && echo "OpenCode: OK" || echo "OpenCode: FAIL"
```

### Check Database

```bash
docker exec orienter-postgres pg_isready -U aibot -d whatsapp_bot
```

## Deployment Management

### Check Deployment Script Options

```bash
~/orient/docker/deploy-server.sh --help
```

### Rollback to Previous Deployment

```bash
cd ~/orient/docker
./deploy-server.sh rollback
```

### Manual Full Restart

```bash
cd ~/orient/docker
COMPOSE_FILES="-f docker-compose.v2.yml -f docker-compose.prod.yml -f docker-compose.r2.yml"
docker compose ${COMPOSE_FILES} down
docker compose ${COMPOSE_FILES} up -d
```

### Check Disk Space

```bash
df -h /home
docker system df
```

### Clean Up Docker Resources

```bash
docker system prune -f
docker image prune -a -f --filter "until=168h"  # Remove images older than 7 days
```

## Error Pattern Reference

| Error Message                               | Likely Cause                 | Solution                                                                    |
| ------------------------------------------- | ---------------------------- | --------------------------------------------------------------------------- |
| `Missing parameter name at index 1: *`      | Express 5 bare wildcard      | Use `/{*splat}` instead of `*`                                              |
| `Failed to load module script: text/html`   | Nginx proxy_pass wrong       | Fix nginx to strip path prefix                                              |
| `Connection Closed` (WhatsApp)              | WebSocket died               | Restart bot-whatsapp container                                              |
| `ECONNREFUSED postgres`                     | Database not ready           | Wait or restart postgres                                                    |
| `502 Bad Gateway`                           | Upstream container down      | Check container status and logs                                             |
| `container is unhealthy`                    | Health check failing         | Check container logs                                                        |
| `DASHBOARD_JWT_SECRET variable is required` | Missing env var              | Add to .env, recreate with docker-compose                                   |
| `environment variable is required`          | Missing env var in container | Check staging uses \_STAGING suffix, use docker-compose up -d (not restart) |
| `/bin/sh: ssh: not found`                   | Missing openssh-client       | Add `openssh-client` to Dockerfile, rebuild image                           |
| `SSH command failed` (monitoring)           | SSH key or config missing    | Mount SSH key to /app/.ssh, set OCI_HOST in .env                            |
| `Permission denied (publickey)`             | SSH key permissions wrong    | chmod 644 on mounted key, ensure container can read it                      |

## Session Data Locations

```
/home/opc/orient/data/
├── whatsapp-auth/     # WhatsApp session files
│   ├── creds.json     # Credentials
│   └── .pairing-mode  # Pairing mode marker
├── media/             # Uploaded media files
├── oauth-tokens/      # OAuth tokens
└── postgres/          # Database files (volume)
```

## Log Locations

- Container logs: `docker logs <container>`
- Nginx access: `docker exec orienter-nginx cat /var/log/nginx/access.log`
- Application logs: `~/orient/logs/` (if configured)

## Server Details

- **Host**: 152.70.172.33
- **User**: opc
- **SSH Key**: `~/.ssh/id_rsa`
- **Deploy Directory**: ~/orient
- **Docker Directory**: ~/orient/docker
- **Domains**:
  - `app.orient.bot` - Dashboard
  - `code.orient.bot` - OpenCode
  - `staging.orient.bot` - Staging Dashboard
  - `code-staging.orient.bot` - Staging OpenCode
