---
name: personal-production-debugging
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
~/orienter/
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
cd ~/orienter/docker
```

## Container Overview

| Container | Port | Purpose |
|-----------|------|---------|
| orienter-nginx | 80, 443 | Reverse proxy, SSL termination |
| orienter-dashboard | 4098 | Dashboard web app + API |
| orienter-bot-whatsapp | 4097 | WhatsApp bot + QR/pairing |
| orienter-opencode | 4099, 8765 | AI agent API + OAuth callback |
| orienter-postgres | 5432 | Database |
| orienter-minio | 9000-9001 | Object storage (or R2) |

## Container Logs

**Note:** Container names changed in v2 compose:
- `orienter-whatsapp-bot` → `orienter-bot-whatsapp` (v2)
- `orienter-slack-bot` → `orienter-bot-slack` (v2)

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

| Issue | Command |
|-------|---------|
| Check all containers | `docker ps -a` |
| Container crash loop | `docker logs <container> --tail 100` |
| View nginx errors | `docker logs orienter-nginx --tail 50` |
| Check dashboard logs | `docker logs orienter-dashboard --tail 100` |
| Check OpenCode logs | `docker logs orienter-opencode --tail 100` |
| Restart dashboard | `docker restart orienter-dashboard` |
| Check database | `docker exec orienter-postgres psql -U aibot -c "SELECT 1"` |
| View env vars | `cat ~/orienter/.env` |
| Check container env vars | `docker exec <container> env \| grep <VAR_NAME>` |
| Missing env var (crash loop) | Add to .env, then `docker compose --env-file ../.env -f compose.yml up -d <service>` |
| Check GitHub Actions | `gh run list --limit 5` (run locally) |
| WhatsApp pairing stuck | `docker restart orienter-bot-whatsapp` |
| WhatsApp factory reset | `rm -rf ~/orienter/data/whatsapp-auth/* && docker restart orienter-bot-whatsapp` |

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
// ❌ BROKEN
app.get('*', (req, res) => { ... });

// ✅ FIXED
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
curl -sI "https://ai.proph.bet/dashboard/assets/index-*.js" | grep content-type

# Expected: content-type: text/javascript; charset=utf-8
# If: content-type: text/html → nginx routing issue
```

**Test direct to container**:
```bash
ssh $OCI_USER@$OCI_HOST "curl -sI http://localhost:4098/assets/index-*.js | head -5"
```

**Fix**: Check nginx config `proxy_pass` strips prefixes correctly:
```nginx
# ❌ WRONG
location /dashboard/assets/ {
    proxy_pass http://dashboard_upstream/dashboard/assets/;
}

# ✅ CORRECT
location /dashboard/assets/ {
    proxy_pass http://dashboard_upstream/assets/;
}
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
ssh $OCI_USER@$OCI_HOST "rm -rf /home/opc/orienter/data/whatsapp-auth/* && docker restart orienter-bot-whatsapp"
```

**Diagnosis**:
```bash
ssh $OCI_USER@$OCI_HOST "docker logs orienter-bot-whatsapp --tail 100 2>&1 | grep -i -E '(pair|code|connection|closed|error)'"
```

### 5. Integrations Page "Request Failed" Error

**Symptoms**: Dashboard Integrations page shows "Error - Request failed" for MCP Servers

**Cause**: The MCP routes exist in `src/dashboard/server.ts` (old location) but were NOT migrated to `packages/dashboard/` (new monorepo location) which is what production Docker images use.

| Environment | Dashboard Location | MCP Routes |
|-------------|-------------------|------------|
| **Local dev** | `src/dashboard/server.ts` | ✅ Has MCP routes |
| **Production Docker** | `packages/dashboard/` | ✅ Migrated (packages/dashboard/src/server/routes/mcp.routes.ts) |

**Diagnosis**:
```bash
# Check if endpoint exists in production
ssh $OCI_USER@$OCI_HOST "curl -s http://localhost:4098/api/mcp/servers"
# Returns {"servers": [...]} = route exists
# Returns "Cannot GET /api/mcp/servers" = route not migrated

# Local dev (uses src/dashboard/) should work:
curl -s http://localhost:4098/api/mcp/servers
# Returns {"error":"No authorization header"} = route exists
```

**MCP Routes available**:
- `/api/mcp/servers` - list MCP servers with connection status
- `/api/mcp/oauth/config` - OAuth callback configuration
- `/api/mcp/oauth/authorize/:serverName` - initiate OAuth flow
- `/api/mcp/oauth/complete/:serverName` - complete OAuth flow
- `/api/mcp/oauth/tokens/:serverName` - clear tokens

### 6. Missing Environment Variables (Crash Loop)

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
ssh $OCI_USER@$OCI_HOST "grep DASHBOARD_JWT_SECRET_STAGING /home/opc/orienter/.env"

# Check what env vars the container actually has
ssh $OCI_USER@$OCI_HOST "docker exec orienter-dashboard-staging env | grep DASHBOARD"
```

**Critical knowledge about environment variables**:

1. **Staging uses _STAGING suffix**: Staging containers expect environment variables with `_STAGING` suffix
   - Production: `DASHBOARD_JWT_SECRET`
   - Staging: `DASHBOARD_JWT_SECRET_STAGING`

2. **docker restart does NOT reload .env**: Simply restarting a container won't pick up new environment variables
   ```bash
   # ❌ WRONG - Won't reload env vars
   docker restart orienter-dashboard-staging

   # ✅ CORRECT - Recreates container with new env vars
   cd ~/orienter/docker
   docker compose --env-file ../.env -f docker-compose.v2.yml -f docker-compose.staging.yml up -d dashboard
   ```

3. **docker-compose needs --env-file flag**: When .env is in parent directory, must specify explicitly
   ```bash
   # Compose files are in ~/orienter/docker/
   # .env file is in ~/orienter/.env
   # Must use --env-file to specify the path
   cd ~/orienter/docker
   docker compose --env-file ../.env -f docker-compose.v2.yml -f docker-compose.staging.yml up -d
   ```

**Fix missing environment variables**:
```bash
# 1. Add missing variable to .env file
ssh $OCI_USER@$OCI_HOST "echo 'DASHBOARD_JWT_SECRET_STAGING=\"your-secret-here\"' >> /home/opc/orienter/.env"

# 2. Recreate container with updated env (from docker directory)
ssh $OCI_USER@$OCI_HOST "cd /home/opc/orienter/docker && docker compose --env-file ../.env -f docker-compose.v2.yml -f docker-compose.staging.yml up -d dashboard"

# 3. Verify container is healthy
ssh $OCI_USER@$OCI_HOST "docker ps | grep dashboard"

# 4. Check logs for successful startup
ssh $OCI_USER@$OCI_HOST "docker logs orienter-dashboard-staging --tail 20"
```

### 7. Deployment Failure

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
cd ~/orienter/docker
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
curl -sf https://ai.proph.bet/health && echo "Nginx: OK" || echo "Nginx: FAIL"

# Dashboard
curl -sf https://ai.proph.bet/dashboard/api/health && echo "Dashboard: OK" || echo "Dashboard: FAIL"

# OpenCode
curl -sf https://ai.proph.bet/opencode/global/health && echo "OpenCode: OK" || echo "OpenCode: FAIL"
```

### Check Database
```bash
docker exec orienter-postgres pg_isready -U aibot -d whatsapp_bot
```

## Deployment Management

### Check Deployment Script Options
```bash
~/orienter/docker/deploy-server.sh --help
```

### Rollback to Previous Deployment
```bash
cd ~/orienter/docker
./deploy-server.sh rollback
```

### Manual Full Restart
```bash
cd ~/orienter/docker
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

| Error Message | Likely Cause | Solution |
|--------------|--------------|----------|
| `Missing parameter name at index 1: *` | Express 5 bare wildcard | Use `/{*splat}` instead of `*` |
| `Failed to load module script: text/html` | Nginx proxy_pass wrong | Fix nginx to strip path prefix |
| `Connection Closed` (WhatsApp) | WebSocket died | Restart bot-whatsapp container |
| `ECONNREFUSED postgres` | Database not ready | Wait or restart postgres |
| `502 Bad Gateway` | Upstream container down | Check container status and logs |
| `container is unhealthy` | Health check failing | Check container logs |
| `DASHBOARD_JWT_SECRET [REDACTED] variable is required` | Missing env var | Add to .env, recreate with docker-compose |
| `environment variable is required` | Missing env var in container | Check staging uses _STAGING suffix, use docker-compose up -d (not restart) |

## Session Data Locations

```
/home/opc/orienter/data/
├── whatsapp-auth/     # WhatsApp session files
│   ├── creds.json     # Credentials
│   └── .pairing-mode  # Pairing mode marker
├── media/             # Uploaded media files
└── postgres/          # Database files (volume)
```

## Log Locations

- Container logs: `docker logs <container>`
- Nginx access: `docker exec orienter-nginx cat /var/log/nginx/access.log`
- Application logs: `~/orienter/logs/` (if configured)

## Docker Compose Multi-Stack Management

Production and staging run as separate Docker Compose stacks on the same server. This creates complexity around network isolation, container naming, and DNS resolution.

### Architecture Overview

| Stack | Project Name | Network | Container Prefix |
|-------|--------------|---------|------------------|
| Production | `docker` (default) or `prod` | `docker_orienter-network` or `prod_orienter-network` | `orienter-*` |
| Staging | `staging` | `staging_orienter-network` | `orienter-*-staging` |

**Critical Architecture Requirement**: The production `nginx-ssl.conf` references staging upstreams (e.g., `orienter-opencode-staging:5099`). This means **both stacks must run and share a Docker network** for nginx to start.

### Network Conflicts and DNS Resolution

#### Problem: "host not found in upstream"
```
nginx: [emerg] host not found in upstream "orienter-opencode-staging:5099"
```

**Cause**: Nginx tries to resolve staging container hostnames but they're on a different Docker network.

**Solution**: Connect staging containers to the production network:
```bash
# Check which network nginx is on
docker inspect orienter-nginx --format '{{json .NetworkSettings.Networks}}' | jq 'keys'

# Connect staging containers to that network
docker network connect docker_orienter-network orienter-opencode-staging
docker network connect docker_orienter-network orienter-dashboard-staging
docker network connect docker_orienter-network orienter-bot-whatsapp-staging

# Restart nginx to pick up the DNS changes
docker restart orienter-nginx
```

#### Problem: Multiple Networks Created
Docker Compose creates networks named `<project>_<network>`. Without explicit project names, you get:
- `docker_orienter-network` (default project name is directory)
- `prod_orienter-network` (if using `-p prod`)
- `staging_orienter-network`

**Diagnosis**:
```bash
# List all networks
docker network ls | grep orienter

# See which containers are on which network
docker network inspect docker_orienter-network --format '{{range .Containers}}{{.Name}} {{end}}'
```

### Using Explicit Project Names

Use `-p` flag to isolate compose stacks and prevent container name collisions:

```bash
# Production stack
cd ~/orienter/docker
docker compose -p prod --env-file ../.env \
  -f docker-compose.v2.yml \
  -f docker-compose.prod.yml \
  -f docker-compose.r2.yml \
  up -d

# Staging stack
docker compose -p staging --env-file ../.env \
  -f docker-compose.v2.yml \
  -f docker-compose.staging.yml \
  up -d
```

**Why use explicit project names**:
- Prevents `docker compose up` from recreating/removing containers from other stacks
- Makes container names predictable
- Isolates networks properly
- Allows running both stacks simultaneously

### Database Name Mismatch Issues

#### Problem: Dashboard shows "Initial Setup" page
The compose files default to `whatsapp_bot_0` but the database may be named `whatsapp_bot`.

**Diagnosis**:
```bash
# Check what database the container expects
docker exec orienter-dashboard env | grep DATABASE_URL
# Returns: postgresql://aibot:aibot123@postgres:5432/whatsapp_bot_0

# List actual databases
docker exec orienter-postgres psql -U aibot -d postgres -c '\l'

# Check if expected database exists
docker exec orienter-postgres psql -U aibot -d whatsapp_bot_0 -c 'SELECT 1' 2>&1
# Error: database "whatsapp_bot_0" does not exist
```

**Solution - Migrate data to new database name**:
```bash
# 1. Create the new database
docker exec orienter-postgres psql -U aibot -d postgres -c 'CREATE DATABASE whatsapp_bot_0;'

# 2. Copy all data from old to new
docker exec orienter-postgres bash -c 'pg_dump -U aibot whatsapp_bot | psql -U aibot whatsapp_bot_0'

# 3. Verify users exist
docker exec orienter-postgres psql -U aibot -d whatsapp_bot_0 -c 'SELECT username FROM dashboard_users;'

# 4. Restart services to use new database
docker restart orienter-dashboard orienter-opencode orienter-bot-whatsapp
```

**Why this happens**: The compose files use `${POSTGRES_DB:-whatsapp_bot_0}` but the `.env` file has `POSTGRES_DB=whatsapp_bot`. If `--env-file` isn't specified correctly, the default is used.

### Complete Production Recovery Procedure

When production is down due to multi-stack issues, follow this recovery procedure:

```bash
# 1. Check current state
ssh opc@152.70.172.33 "docker ps -a --format 'table {{.Names}}\t{{.Status}}'"

# 2. Clean up orphaned containers
ssh opc@152.70.172.33 "docker container prune -f"

# 3. Check and clean up networks
ssh opc@152.70.172.33 "docker network prune -f"

# 4. Start production stack with explicit project name
ssh opc@152.70.172.33 "cd /home/opc/orienter/docker && \
  docker compose -p prod --env-file ../.env \
    -f docker-compose.v2.yml \
    -f docker-compose.prod.yml \
    -f docker-compose.r2.yml \
    up -d"

# 5. Start staging stack
ssh opc@152.70.172.33 "cd /home/opc/orienter/docker && \
  docker compose -p staging --env-file ../.env \
    -f docker-compose.v2.yml \
    -f docker-compose.staging.yml \
    up -d"

# 6. Get the production network name
PROD_NETWORK=$(ssh opc@152.70.172.33 "docker inspect orienter-nginx --format '{{range \$k, \$v := .NetworkSettings.Networks}}{{\$k}}{{end}}'")

# 7. Connect staging containers to production network for nginx DNS resolution
ssh opc@152.70.172.33 "docker network connect $PROD_NETWORK orienter-opencode-staging 2>/dev/null || true"
ssh opc@152.70.172.33 "docker network connect $PROD_NETWORK orienter-dashboard-staging 2>/dev/null || true"
ssh opc@152.70.172.33 "docker network connect $PROD_NETWORK orienter-bot-whatsapp-staging 2>/dev/null || true"

# 8. Restart nginx to pick up DNS
ssh opc@152.70.172.33 "docker restart orienter-nginx"

# 9. Verify health
curl -sf https://ai.proph.bet/health && echo "Production OK"
curl -sf https://staging.proph.bet/health && echo "Staging OK"
```

### HSTS and SSL Configuration

#### Problem: Browser shows "Not Secure" despite valid SSL
Chrome may show "Not Secure" if:
1. User accessed via HTTP first and it was cached
2. HSTS header is missing, allowing HTTP fallback

**Add HSTS header to nginx** (`nginx-ssl.conf`):
```nginx
server {
    listen 443 ssl;
    server_name ai.proph.bet;

    # ... SSL config ...

    # HSTS - force HTTPS for 1 year
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

    # ... rest of config ...
}
```

**Apply the change**:
```bash
# Edit the config
ssh opc@152.70.172.33 "vim /home/opc/orienter/docker/nginx-ssl.conf"

# Restart nginx to load new config
ssh opc@152.70.172.33 "docker restart orienter-nginx"

# Verify HSTS header
curl -sI https://ai.proph.bet/ | grep -i strict
# Should show: strict-transport-security: max-age=31536000; includeSubDomains
```

**Clear browser HSTS cache** (if user still sees "Not Secure"):
1. Go to `chrome://net-internals/#hsts`
2. Under "Delete domain security policies", enter `ai.proph.bet`
3. Click "Delete"
4. Visit `https://ai.proph.bet` again

### Multi-Stack Error Pattern Reference

| Error | Cause | Solution |
|-------|-------|----------|
| `host not found in upstream "orienter-*-staging"` | Staging containers not on nginx's network | `docker network connect <prod_network> orienter-*-staging` |
| Container name collision on `up -d` | Multiple compose stacks without project names | Use `-p prod` and `-p staging` flags |
| Database `whatsapp_bot_0` does not exist | Compose defaults vs .env mismatch | Create DB and migrate with `pg_dump` |
| Nginx in "Restarting" loop | Staging containers missing or wrong network | Start staging, connect to prod network |
| "Not Secure" in browser | Missing HSTS header or HTTP cache | Add HSTS header, clear browser cache |
| `--env-file` not working | Wrong path or compose run from wrong directory | Use `--env-file ../.env` from docker/ dir |

## Reference Materials

- See [references/deployment-troubleshooting.md](references/deployment-troubleshooting.md) for advanced deployment troubleshooting
- See [references/containers.md](references/containers.md) for container-specific configuration details
