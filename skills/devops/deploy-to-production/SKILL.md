---
name: deploy-to-production
description: Comprehensive guide for deploying Orient to production. Use this skill when deploying changes, updating production, fixing deployment failures, or rolling back. Covers pre-flight checks, environment variables, Docker compose configuration, CI/CD pipeline, smart change detection, and health verification.
---

# Deploy to Production

## Quick Reference

### Deploy via GitHub Actions (Recommended)

```bash
# Push to main triggers automatic deployment
git push origin main

# Watch deployment progress
gh run watch --exit-status

# Check deployment status
gh run list --limit 5
```

### Force Rebuild All Images

When you need to bypass change detection and rebuild everything:

```bash
# Via GitHub Actions UI: Run workflow with "Force rebuild all images" checked
# Or use workflow_dispatch:
gh workflow run deploy.yml -f force_build_all=true
```

### Manual Deployment (Emergency)

```bash
# SSH to server
ssh $OCI_USER@$OCI_HOST

# Navigate to docker directory
cd ~/orient/docker

# IMPORTANT: Always use --env-file to load environment variables
COMPOSE_CMD="sudo docker compose --env-file ../.env -f docker-compose.v2.yml -f docker-compose.prod.yml -f docker-compose.r2.yml"

# Pull latest images
$COMPOSE_CMD pull

# Start services (recreates containers with current .env values)
$COMPOSE_CMD up -d

# Or as single commands:
sudo docker compose --env-file ../.env -f docker-compose.v2.yml -f docker-compose.prod.yml -f docker-compose.r2.yml pull
sudo docker compose --env-file ../.env -f docker-compose.v2.yml -f docker-compose.prod.yml -f docker-compose.r2.yml up -d
```

**Note**: Always pass `--env-file ../.env` to ensure environment variables are loaded. Without it, Docker Compose uses only variables from the shell environment.

## Smart Change Detection

The CI/CD pipeline uses intelligent change detection to only rebuild images when their source code changes.

### How It Works

The `detect-changes` job analyzes which files changed and sets build flags:

| Image          | Triggered By Changes In                                                                                                               |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| **OpenCode**   | `src/**`, `packages/core/**`, `packages/mcp-tools/**`, `packages/mcp-servers/**`, `packages/agents/**`, `docker/Dockerfile.opencode*` |
| **WhatsApp**   | `packages/bot-whatsapp/**`, `packages/core/**`, `packages/database/**`                                                                |
| **Dashboard**  | `packages/dashboard/**`, `packages/dashboard-frontend/**`, `packages/core/**`                                                         |
| **All Images** | `package.json`, `pnpm-lock.yaml` (dependency changes)                                                                                 |

### Time Savings

| Scenario                            | Old Pipeline | New Pipeline |
| ----------------------------------- | ------------ | ------------ |
| Single package change               | ~20 min      | ~5-8 min     |
| Config-only change (nginx, compose) | ~20 min      | ~3 min       |
| All packages change                 | ~20 min      | ~20 min      |

### Workflow Jobs

```
detect-changes (8s)
     |
   test (40s)
     |
+----+----+----+
|    |    |    |
v    v    v    v
build-opencode  build-whatsapp  build-dashboard  (conditional)
     |              |                |
     +------+-------+----------------+
            |
            v
      deploy (2min)
```

## Pre-Deployment Checklist

### 1. Local Validation

Before pushing changes, always verify locally:

```bash
# Run tests (CI mode excludes e2e and eval tests)
pnpm run test:ci

# Run Docker validation tests
pnpm turbo test --filter @orient/core...

# Validate Docker compose syntax
cd docker
docker compose -f docker-compose.v2.yml -f docker-compose.prod.yml -f docker-compose.r2.yml config --services
```

### 2. Check Service Names Consistency

The v2 compose uses specific service names:

| Service   | V2 Service Name | Container Name        |
| --------- | --------------- | --------------------- |
| WhatsApp  | bot-whatsapp    | orienter-bot-whatsapp |
| Slack     | bot-slack       | orienter-bot-slack    |
| OpenCode  | opencode        | orienter-opencode     |
| Dashboard | dashboard       | orienter-dashboard    |

### 3. Environment Variables & GitHub Secrets

**CRITICAL**: Environment variables must be properly configured in three places:

1. `.env.production` file (local reference)
2. GitHub Secrets (for CI/CD)
3. Server `.env` file at `/home/opc/orient/.env`

#### Managing GitHub Secrets

**Update all secrets from .env.production**:

```bash
cat .env.production | grep -E '^[A-Z_][A-Z0-9_]*=' | while IFS='=' read -r key value; do
  value=$(echo "$value" | sed 's/^"//; s/"$//')
  echo "Setting: $key"
  echo "$value" | gh secret set "$key" --repo orient-core/orient
done
```

#### Critical Environment Variables

Required for production:

```bash
# Database
DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@postgres:5432/${POSTGRES_DB}

# Dashboard Security (REQUIRED - causes crash loop if missing)
DASHBOARD_JWT_SECRET="<32+ character secure string>"

# Storage (R2)
R2_ACCESS_KEY_ID=
R2_SECRET_ACCESS_KEY=
R2_ACCOUNT_ID=

# OAuth Callbacks (must match registered URLs)
OAUTH_CALLBACK_URL=https://app.orient.bot/oauth/callback
GOOGLE_OAUTH_CALLBACK_URL=https://app.orient.bot/oauth/google/callback

# API Keys
ANTHROPIC_API_KEY=
OPENAI_API_KEY=

# Slack Configuration (optional)
SLACK_BOT_TOKEN=
SLACK_SIGNING_SECRET=
SLACK_APP_TOKEN=
```

#### Applying Environment Variable Changes

**IMPORTANT**: `docker restart` does NOT reload environment variables from `.env`.

```bash
# WRONG - Won't pick up new env vars
ssh $OCI_USER@$OCI_HOST "docker restart orienter-dashboard"

# CORRECT - Recreates container with new env vars
ssh $OCI_USER@$OCI_HOST "cd /home/opc/orient/docker && \
  docker compose --env-file ../.env \
    -f docker-compose.v2.yml \
    -f docker-compose.prod.yml \
    -f docker-compose.r2.yml \
    up -d dashboard"
```

## CI/CD Pipeline

### GitHub Actions Workflow (.github/workflows/deploy.yml)

The deployment pipeline:

1. **Detect Changes** - Determines which images need rebuilding (8s)
2. **Tests** - Runs `pnpm run test:ci` (excludes e2e/eval tests)
3. **Build Images** - Only builds changed packages (conditional)
4. **Deploy** - Syncs files and restarts services

### Common CI Failures

| Issue                                  | Cause                     | Fix                             |
| -------------------------------------- | ------------------------- | ------------------------------- |
| `Cannot find package`                  | Missing devDependency     | Check pnpm-lock.yaml            |
| `No test found in suite`               | Eval tests included       | Use `test:ci` instead of `test` |
| Dockerfile not found                   | Path changed              | Update workflow matrix          |
| Container name conflict                | V1/V2 name mismatch       | Clean up both names             |
| `Missing parameter name at index 1: *` | Express 5 breaking change | Use `/{*splat}` not `*`         |

### Express 5 / path-to-regexp v8 Breaking Changes

Express 5 uses path-to-regexp v8, which has breaking changes:

**Problem**: Bare `*` wildcards no longer work

```typescript
// BROKEN in Express 5
app.get('*', (req, res) => { ... });

// FIXED - use named wildcard
app.get('/{*splat}', (req, res) => { ... });
```

**Error message**: `TypeError: Missing parameter name at index 1: *`

## Health Verification

### Production Health Checks

```bash
# Check all containers
ssh $OCI_USER@$OCI_HOST "docker ps --format 'table {{.Names}}\t{{.Status}}'"

# Check specific services
curl -sf https://app.orient.bot/health        # Nginx
curl -sf https://code.orient.bot/global/health  # OpenCode
curl -sf https://app.orient.bot/dashboard/api/health    # Dashboard
```

### Expected Container Names

- `orienter-nginx`
- `orienter-bot-whatsapp`
- `orienter-opencode`
- `orienter-dashboard`
- `orienter-postgres`

## Rollback Procedure

### Automatic Rollback

The CI pipeline automatically rolls back if health checks fail.

### Manual Rollback

```bash
ssh $OCI_USER@$OCI_HOST

cd ~/orient/docker
COMPOSE_FILES="-f docker-compose.v2.yml -f docker-compose.prod.yml -f docker-compose.r2.yml"

# Find latest backup
ls -t ~/orient/backups | head -5

# Restore
LATEST=$(ls -t ~/orient/backups | head -1)
sudo docker compose ${COMPOSE_FILES} down
cp -f ~/orient/backups/${LATEST}/*.yml .
sudo docker compose ${COMPOSE_FILES} up -d
```

## Troubleshooting

### GitHub Actions SSH Authentication

#### OCI_SSH_PRIVATE_KEY Secret

**Error**: `Load key "/home/runner/.ssh/id_rsa": error in libcrypto` or `Permission denied (publickey)`

**Cause**: The `OCI_SSH_PRIVATE_KEY` secret is missing or malformed.

**Fix**: Add your SSH private key to GitHub Secrets:

```bash
# Add via gh CLI (recommended)
gh secret set OCI_SSH_PRIVATE_KEY --repo orient-bot/orient < ~/.ssh/id_rsa

# Or copy the key content and add via GitHub UI
cat ~/.ssh/id_rsa | pbcopy
# Then: Settings → Secrets → Actions → New repository secret
```

**Required format**: The full private key including headers:

```
-----BEGIN OPENSSH PRIVATE KEY-----
... key content ...
-----END OPENSSH PRIVATE KEY-----
```

**Note**: The key must match what's authorized on the Oracle server (`~/.ssh/authorized_keys`).

### GHCR Package Access (403 Forbidden)

**Error**: `failed to resolve reference "ghcr.io/orient-bot/orient/dashboard:latest": 403 Forbidden`

**Cause**: GitHub Container Registry packages are private by default, even in public repos.

**Fixes**:

1. **Make packages public** (recommended for open source):
   - Go to https://github.com/orgs/orient-bot/packages
   - Click each package → Settings → Danger Zone → Change visibility → Public

2. **Or use a PAT with `read:packages` scope**:

   ```bash
   # Create a PAT at https://github.com/settings/tokens with read:packages scope
   # Add to GitHub Secrets as GHCR_PAT

   # In workflow, authenticate before pulling:
   echo "${{ secrets.GHCR_PAT }}" | docker login ghcr.io -u USERNAME --password-stdin
   ```

3. **Or authenticate the server permanently**:
   ```bash
   # On the Oracle server
   gh auth token | sudo docker login ghcr.io -u orient-bot --password-stdin
   ```

### Database Migration Failures

#### Role/User Not Found

**Error**: `FATAL: role "orient" does not exist`

**Cause**: Migration script uses hardcoded database user instead of actual configured user.

**Fix**: The workflow now dynamically reads credentials from server `.env`:

```bash
DB_USER=$(grep '^POSTGRES_USER=' ~/orient/.env | cut -d= -f2 | tr -d '"')
DB_NAME=$(grep '^POSTGRES_DB=' ~/orient/.env | cut -d= -f2 | tr -d '"')
```

If migrations still fail, verify server `.env` has correct values:

```bash
ssh opc@152.70.172.33 "grep POSTGRES ~/orient/.env"
# Expected:
# POSTGRES_USER=aibot
# POSTGRES_DB=whatsapp_bot
```

#### Production Down After Failed Deploy

If deployment fails partway through, production containers may be stopped:

```bash
# Check what's running
ssh opc@152.70.172.33 "docker ps --format 'table {{.Names}}\t{{.Status}}'"

# Restart production manually
ssh opc@152.70.172.33 "cd ~/orient/docker && \
  sudo docker compose --env-file ../.env \
    -f docker-compose.v2.yml \
    -f docker-compose.prod.yml \
    -f docker-compose.r2.yml \
    up -d"
```

### Docker Build Failures

#### Missing Directories in Dockerfile

**Error**: `failed to calculate checksum of ref: "/src": not found` or `/credentials": not found`

**Cause**: Dockerfile tries to COPY directories that don't exist in the repo (e.g., `src/`, `credentials/`)

**Fix**: Remove or comment out COPY statements for non-existent directories in `docker/Dockerfile.opencode.legacy`:

```dockerfile
# Remove these lines if directories don't exist:
# COPY src ./src
# COPY credentials ./credentials
```

#### DEPLOY_ENV Build Argument

**Error**: `"/docker/opencode.local.json": not found`

**Cause**: OpenCode Dockerfile defaults to `DEPLOY_ENV=local`, which looks for `opencode.local.json`

**Fix**: Ensure workflow passes `DEPLOY_ENV=prod` build-arg:

```yaml
# In .github/workflows/deploy.yml
- name: Build and push Docker image
  uses: docker/build-push-action@v5
  with:
    build-args: |
      DEPLOY_ENV=prod
```

### Server .env Configuration

#### Complete .env File Requirements

The server `.env` file at `~/orient/.env` must contain:

```bash
# REQUIRED - Domain Configuration
ORIENT_APP_DOMAIN=app.orient.bot
ORIENT_CODE_DOMAIN=code.orient.bot
ORIENT_STAGING_DOMAIN=staging.orient.bot
ORIENT_CODE_STAGING_DOMAIN=code-staging.orient.bot

# REQUIRED - Database (generates crash loop if missing)
POSTGRES_USER=aibot
POSTGRES_PASSWORD=<secure-password>
POSTGRES_DB=whatsapp_bot
# IMPORTANT: Use container name 'orienter-postgres' not 'postgres' to avoid DNS conflicts with staging
DATABASE_URL=postgresql://aibot:<password>@orienter-postgres:5432/whatsapp_bot

# REQUIRED - Dashboard Security (crash loop if missing)
DASHBOARD_JWT_SECRET=<openssl rand -hex 32>

# REQUIRED - Encryption
ORIENT_MASTER_KEY=<openssl rand -hex 32>

# REQUIRED - MinIO (for local S3-compatible storage)
MINIO_ROOT_USER=minioadmin
MINIO_ROOT_PASSWORD=minioadmin123

# OPTIONAL - API Keys (can be empty initially)
ANTHROPIC_API_KEY=
OPENAI_API_KEY=
R2_ACCESS_KEY_ID=
R2_SECRET_ACCESS_KEY=
```

#### Generate Secrets

```bash
# Generate secure values
openssl rand -hex 32  # For DASHBOARD_JWT_SECRET
openssl rand -hex 32  # For ORIENT_MASTER_KEY
openssl rand -base64 24 | tr -d '/+=' | head -c 24  # For POSTGRES_PASSWORD
```

### PostgreSQL Authentication Failures

**Error**: `password authentication failed for user "aibot"`

**Cause**: PostgreSQL was initialized with a different password than what's in `.env`

**Fix**: Reset the PostgreSQL data volume (WARNING: deletes all data):

```bash
ssh opc@152.70.172.33
cd ~/orient/docker
sudo docker compose --env-file ../.env \
  -f docker-compose.v2.yml -f docker-compose.prod.yml -f docker-compose.r2.yml down -v
sudo docker compose --env-file ../.env \
  -f docker-compose.v2.yml -f docker-compose.prod.yml -f docker-compose.r2.yml up -d
```

### Nginx Upstream Errors

**Error**: `host not found in upstream "orienter-opencode-staging:5099"`

**Cause**: Nginx config references staging containers that don't exist in production-only deployment

**Fix**: Use a production-only nginx config that doesn't define staging upstreams, or make staging upstreams return 503:

```nginx
# Staging servers - return 503 when staging not running
server {
    listen 443 ssl;
    server_name staging.orient.bot code-staging.orient.bot;
    # ... ssl config ...
    location / {
        return 503 'Staging environment not deployed';
    }
}
```

### Container Won't Start

1. Check logs: `docker logs orienter-dashboard --tail 100`
2. Check compose config: `docker compose config`
3. Verify service names match between compose files

### Dashboard Crash Loop

Check for Express 5 errors:

```bash
ssh $OCI_USER@$OCI_HOST "docker logs orienter-dashboard --tail 50 2>&1 | grep -i 'parameter name\|path-to-regexp'"
```

If you see `Missing parameter name at index 1: *`, fix the SPA catch-all route.

### SSL Certificate Issues

```bash
# Check certificate paths
ls -la ~/orient/certbot/conf/live/

# Verify nginx can read certs
docker exec orienter-nginx ls -la /etc/nginx/ssl/
```

### Database Connection Failed

```bash
# Check database health
docker exec orienter-postgres pg_isready -U aibot -d whatsapp_bot

# Check DATABASE_URL in container
docker exec orienter-dashboard env | grep DATABASE_URL
```

### DNS Conflict: Database Does Not Exist

**Error**: `error: database "whatsapp_bot" does not exist` even though the database clearly exists

**Cause**: When production and staging share the same Docker network, both postgres containers have the DNS alias `postgres`. Docker DNS may resolve to the wrong container.

**Diagnosis**:

```bash
# Check both postgres containers have the same alias
docker inspect orienter-postgres --format '{{json .NetworkSettings.Networks}}' | jq '.[] | .DNSNames'
docker inspect orienter-postgres-staging --format '{{json .NetworkSettings.Networks}}' | jq '.[] | .DNSNames'

# If both show "postgres" as an alias, that's the conflict
```

**Fix**: Use container names instead of service aliases in DATABASE_URL:

```bash
# In docker-compose.v2.yml, change:
DATABASE_URL=postgresql://user:pass@postgres:5432/db

# To:
DATABASE_URL=postgresql://user:pass@orienter-postgres:5432/db
```

The compose file (`docker-compose.v2.yml`) should already use `orienter-postgres` (container name) instead of `postgres` (service alias).

### Health Check Race Conditions

**Error**: `dependency failed to start: container orienter-dashboard is unhealthy` during CI/CD deployment

**Cause**: Docker Compose health checks can fail transiently when containers are first created, especially if the database connection takes a moment to establish.

**Solution**: The CI/CD pipeline uses staged deployment:

1. **Stage 1**: Start backend services (dashboard, opencode) and wait for healthy
2. **Stage 2**: Start bot services and wait for healthy
3. **Stage 3**: Start nginx

This is implemented in `.github/workflows/deploy.yml`:

```bash
# Stage 1: Start backend services
docker compose up -d dashboard opencode
# Wait for healthy status before proceeding

# Stage 2: Start bot services
docker compose up -d bot-whatsapp
# Wait for healthy status

# Stage 3: Start nginx
docker compose up -d nginx
```

**Manual Recovery**: If deployment fails mid-way:

```bash
ssh opc@152.70.172.33
cd ~/orient/docker

# Start services in stages manually
COMPOSE="docker compose --env-file ../.env -f docker-compose.v2.yml -f docker-compose.prod.yml -f docker-compose.r2.yml"

# 1. Ensure postgres is running
sudo $COMPOSE up -d postgres
sleep 5

# 2. Start dashboard and opencode
sudo $COMPOSE up -d dashboard opencode
sleep 15

# 3. Check health
docker ps --format 'table {{.Names}}\t{{.Status}}' | grep -E 'dashboard|opencode'

# 4. If healthy, start remaining services
sudo $COMPOSE up -d
```

### WhatsApp Pairing Issues After Deploy

```bash
# Container restart usually fixes pairing issues
docker restart orienter-bot-whatsapp

# Full reset if needed (clears session)
rm -rf ~/orient/data/whatsapp-auth/*
docker restart orienter-bot-whatsapp
```

### Health Endpoint Testing

After deployment, verify all services are accessible:

```bash
# Test health endpoints
curl -sf https://app.orient.bot/health && echo " OK"
curl -sf https://code.orient.bot/health && echo " OK"

# Test dashboard is serving
curl -sf -o /dev/null -w "%{http_code}" https://app.orient.bot/

# Check container health status
ssh opc@152.70.172.33 "docker ps --format 'table {{.Names}}\t{{.Status}}'"
```

Expected output - all containers should show "(healthy)":

```
NAMES                   STATUS
orienter-nginx          Up X minutes (healthy)
orienter-bot-whatsapp   Up X minutes (healthy)
orienter-opencode       Up X minutes (healthy)
orienter-dashboard      Up X minutes (healthy)
orienter-postgres       Up X minutes (healthy)
```

## Quick Commands

```bash
# Check production status
ssh opc@152.70.172.33 "docker ps --format 'table {{.Names}}\t{{.Status}}'"

# View dashboard logs
ssh opc@152.70.172.33 "docker logs orienter-dashboard --tail 100"

# View nginx logs
ssh opc@152.70.172.33 "docker logs orienter-nginx --tail 50"

# Restart dashboard
ssh opc@152.70.172.33 "docker restart orienter-dashboard"

# Full redeploy
git push origin main && gh run watch --exit-status

# Force full rebuild
gh workflow run deploy.yml -f force_build_all=true
```

## Server Details

- **Host**: 152.70.172.33
- **User**: opc
- **Deploy Directory**: ~/orient
- **Docker Directory**: ~/orient/docker
- **Data Directory**: ~/orient/data
- **Domains**:
  - `app.orient.bot` - Dashboard
  - `code.orient.bot` - OpenCode
  - `staging.orient.bot` - Staging Dashboard
  - `code-staging.orient.bot` - Staging OpenCode
