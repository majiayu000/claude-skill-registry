---
name: personal-production-ops
description: Comprehensive guide for deploying the Orient to production. Use this skill when deploying changes, updating production, fixing deployment failures, or rolling back. Covers pre-flight checks, environment variables, Docker compose configuration, CI/CD pipeline, smart change detection, and health verification.
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
cd ~/orienter/docker

# Pull and restart (uses v2 compose by default)
sudo docker compose -f docker-compose.v2.yml -f docker-compose.prod.yml -f docker-compose.r2.yml pull
sudo docker compose -f docker-compose.v2.yml -f docker-compose.prod.yml -f docker-compose.r2.yml up -d
```

## Smart Change Detection

The CI/CD pipeline uses intelligent change detection to only rebuild images when their source code changes.

### How It Works

The `detect-changes` job analyzes which files changed and sets build flags:

| Image | Triggered By Changes In |
|-------|------------------------|
| **OpenCode** | `src/**`, `packages/core/**`, `packages/mcp-tools/**`, `docker/Dockerfile.opencode*` |
| **WhatsApp** | `packages/bot-whatsapp/**`, `packages/core/**` |
| **Dashboard** | `packages/dashboard/**`, `packages/core/**` |
| **All Images** | `package.json`, `pnpm-lock.yaml` (dependency changes) |

### Time Savings

| Scenario | Old Pipeline | New Pipeline |
|----------|-------------|--------------|
| Single package change | ~20 min | ~5-8 min |
| Config-only change (nginx, compose) | ~20 min | ~3 min |
| All packages change | ~20 min | ~20 min |

### Workflow Jobs

```
detect-changes (8s)
     ↓
   test (40s)
     ↓
┌────┼────┬────┐
│    │    │    │
↓    ↓    ↓    ↓
build-opencode  build-whatsapp  build-dashboard  (conditional)
     │              │                │
     └──────────────┼────────────────┘
                    ↓
              deploy (2min)
```

## Monitoring Multi-Image Builds

### Watch Build Progress

When deploying changes that trigger multiple image builds, monitor each build's status:

```bash
# Watch deployment in real-time
gh run watch --exit-status

# Check specific build job status
gh run view <run-id> --json jobs --jq '.jobs[] | "\(.name): \(.status) (\(.conclusion // "in_progress"))"'
```

### Typical Build Times

| Image | Local (cached) | CI (cached) | CI (no cache) |
|-------|----------------|-------------|---------------|
| OpenCode | 1-2 min | 3-5 min | 8-12 min |
| WhatsApp | 30s | 2-3 min | 4-6 min |
| Dashboard | 30s | 1-2 min | 3-5 min |
| Slack | 30s | 2-3 min | 4-6 min |

### Handling Partial Deployment Failures

When some images build successfully but others fail, the deployment job is blocked. Common scenario:

```
✓ Build OpenCode Image - Success (10m7s)
✓ Build WhatsApp Image - Success (5m1s)
✗ Build Dashboard Image - Failed (2m6s)
✗ Deploy to Oracle Cloud - Blocked (Dashboard failure)
```

**Understanding the failure:**
- The successful images ARE pushed to the registry
- The deployment job won't run because it requires ALL builds to pass
- Production continues running with old images

**Manual deployment of successful images:**
```bash
# SSH to server and manually deploy the successful images
ssh $OCI_USER@$OCI_HOST

cd ~/orienter/docker
COMPOSE_FILES="-f docker-compose.v2.yml -f docker-compose.prod.yml -f docker-compose.r2.yml"

# Pull only the successfully built images
sudo docker compose ${COMPOSE_FILES} pull opencode whatsapp-bot

# Restart only those services
sudo docker compose ${COMPOSE_FILES} up -d opencode whatsapp-bot

# Verify
sudo docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Image}}'
```

**Fix and retry the failed image:**
1. Investigate the failure: `gh run view <run-id> --log-failed`
2. Fix the issue locally
3. Push a fix commit
4. The new workflow will only rebuild changed images

### Pre-Deployment Dashboard Health Checks

Before deploying changes, verify Dashboard builds correctly locally:

```bash
# 1. Build dashboard locally to catch errors early
docker build -f packages/dashboard/Dockerfile -t dashboard-test . 2>&1 | tail -20

# 2. Quick smoke test
docker run --rm -p 4098:4098 dashboard-test &
sleep 5
curl -sf http://localhost:4098/health && echo "Dashboard healthy"
docker stop $(docker ps -q --filter ancestor=dashboard-test)

# 3. Run dashboard-specific tests
pnpm --filter @orient/dashboard test
```

**Common Dashboard build failures:**
| Error | Cause | Fix |
|-------|-------|-----|
| `Cannot find module '@orient/core'` | Package not built | `pnpm build:packages` first |
| `VITE_API_URL undefined` | Missing env var in build | Check `.env` or build args |
| `path-to-regexp` error | Express 5 wildcard | Use `/{*splat}` not `*` |
| TypeScript errors | Type mismatches | Fix types, run `tsc --noEmit` |

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

### 2. Pre-Deployment Compose Validation

**CRITICAL**: Before deploying compose file changes, verify that production `.env` has explicit overrides for any changed defaults. This prevents breaking production when compose defaults change.

```bash
# Extract defaults from compose files and compare with production .env
ssh $OCI_USER@$OCI_HOST "cat /home/opc/orienter/.env" > /tmp/prod.env

# Check critical variables that may have defaults in compose
echo "=== Compose Default Validation ==="

# 1. POSTGRES_DB - Check if compose default matches production
COMPOSE_DEFAULT=$(grep -E "POSTGRES_DB:-" docker/docker-compose.v2.yml | sed 's/.*:-\([^}]*\)}.*/\1/' | head -1)
PROD_VALUE=$(grep "^POSTGRES_DB=" /tmp/prod.env | cut -d= -f2 | tr -d '"')
echo "POSTGRES_DB: compose_default='${COMPOSE_DEFAULT}' prod_value='${PROD_VALUE}'"
if [ -z "$PROD_VALUE" ] && [ -n "$COMPOSE_DEFAULT" ]; then
  echo "  ⚠️  WARNING: Production missing POSTGRES_DB, will use compose default: $COMPOSE_DEFAULT"
fi

# 2. Check port mappings haven't changed
echo ""
echo "=== Port Mappings ==="
docker compose -f docker/docker-compose.v2.yml -f docker/docker-compose.prod.yml config 2>/dev/null | grep -E "^\s+ports:" -A 5

# 3. Check service names match between compose files
echo ""
echo "=== Service Name Consistency ==="
V2_SERVICES=$(docker compose -f docker/docker-compose.v2.yml config --services 2>/dev/null | sort)
PROD_SERVICES=$(docker compose -f docker/docker-compose.prod.yml config --services 2>/dev/null | sort)
echo "v2.yml services: $V2_SERVICES"
echo "prod.yml services: $PROD_SERVICES"

# 4. Verify critical env vars exist in production
echo ""
echo "=== Critical Environment Variables ==="
for VAR in POSTGRES_DB POSTGRES_USER POSTGRES_PASSWORD DATABASE_URL DASHBOARD_JWT_SECRET; do
  if grep -q "^${VAR}=" /tmp/prod.env; then
    echo "✅ $VAR: present"
  else
    echo "❌ $VAR: MISSING"
  fi
done

rm /tmp/prod.env
```

**Quick validation command:**
```bash
# One-liner to check if POSTGRES_DB is explicitly set
ssh $OCI_USER@$OCI_HOST "grep '^POSTGRES_DB=' /home/opc/orienter/.env || echo 'WARNING: POSTGRES_DB not set, using compose default'"
```

### 3. Check Service Names Consistency

The v2 compose uses different service names than v1:

| V1 Service Name | V2 Service Name | Container Name |
|----------------|-----------------|----------------|
| whatsapp-bot | bot-whatsapp | orienter-bot-whatsapp |
| slack-bot | bot-slack | orienter-bot-slack |
| opencode | opencode | orienter-opencode |
| dashboard | dashboard | orienter-dashboard |

**IMPORTANT**: Ensure all compose overlay files (`docker-compose.prod.yml`, `docker-compose.r2.yml`) use v2 service names.

### 4. Dockerfile Path Verification

Check that CI workflow references correct Dockerfiles:

| Service | Dockerfile Path | Notes |
|---------|----------------|-------|
| opencode | docker/Dockerfile.opencode.legacy | Legacy - requires OpenCode binary installation |
| whatsapp-bot | packages/bot-whatsapp/Dockerfile | Per-package build |
| dashboard | packages/dashboard/Dockerfile | Per-package build |

### 5. Environment Variables & GitHub Secrets

**CRITICAL**: Environment variables must be properly configured in three places:
1. `.env.production` file (local reference)
2. GitHub Secrets (for CI/CD)
3. Server `.env` file at `/home/opc/orienter/.env`

#### Managing GitHub Secrets

**Update all secrets from .env.production**:
```bash
# Automated update of all secrets
cat .env.production | grep -E '^[A-Z_][A-Z0-9_]*=' | while IFS='=' read -r key value; do
  value=$(echo "$value" | sed 's/^"//; s/"$//')
  echo "Setting: $key"
  echo "$value" | gh secret set "$key" --repo <your-repo>
done
```

**Keep .env.production in sync**:
```bash
# Check for missing keys in .env.production
diff <(grep -E '^[A-Z_]' .env | cut -d= -f1 | sort) \
     <(grep -E '^[A-Z_]' .env.production | cut -d= -f1 | sort)
```

**Note**: GitHub doesn't allow secret names starting with `GITHUB_`. Variables like `GITHUB_TOKEN`, `GITHUB_REPO`, and `GITHUB_BASE_BRANCH` are for local development only. CI/CD uses the built-in `secrets.GITHUB_TOKEN`.

#### Production vs Staging Environment Variables

**Production** uses standard variable names:
```bash
DASHBOARD_JWT_SECRET="production-secret"
SLACK_BOT_TOKEN="xoxb-production-token"
DATABASE_URL="postgresql://...whatsapp_bot"
```

**Staging** uses `_STAGING` suffix:
```bash
DASHBOARD_JWT_SECRET_STAGING="staging-secret"
SLACK_BOT_TOKEN_STAGING="xoxb-staging-token"
DATABASE_URL="postgresql://...whatsapp_bot_staging"
```

The staging compose file (`docker-compose.staging.yml`) expects variables with `_STAGING` suffix.

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
OAUTH_CALLBACK_URL=https://ai.proph.bet/oauth/callback
GOOGLE_OAUTH_CALLBACK_URL=https://ai.proph.bet/oauth/google/callback

# API Keys
ANTHROPIC_API_KEY=
OPENAI_API_KEY=
XAI_API_KEY=

# Slack Configuration
SLACK_BOT_TOKEN=
SLACK_SIGNING_SECRET=
SLACK_APP_TOKEN=
```

#### Applying Environment Variable Changes

**IMPORTANT**: `docker restart` does NOT reload environment variables from `.env`.

```bash
# ❌ WRONG - Won't pick up new env vars
ssh $OCI_USER@$OCI_HOST "docker restart orienter-dashboard"

# ✅ CORRECT - Recreates container with new env vars
ssh $OCI_USER@$OCI_HOST "cd /home/opc/orienter/docker && \
  docker compose --env-file ../.env \
    -f docker-compose.v2.yml \
    -f docker-compose.prod.yml \
    -f docker-compose.r2.yml \
    up -d dashboard"
```

**Why --env-file is needed**: The compose files are in `~/orienter/docker/` but the `.env` file is in the parent directory `~/orienter/.env`. Docker Compose by default only looks in the same directory as the compose file.

#### Common Missing Variables That Cause Crash Loops

| Variable | Service | Symptom |
|----------|---------|---------|
| `DASHBOARD_JWT_SECRET` | dashboard | Restarting loop, "environment variable is required" |
| `DASHBOARD_JWT_SECRET_STAGING` | dashboard (staging) | Restarting loop |
| `DATABASE_URL` | All services | Connection refused errors |
| `ANTHROPIC_API_KEY` | opencode, bots | API call failures |
| `SLACK_BOT_TOKEN` | bot-slack | Slack connection failures |

**Quick diagnosis**:
```bash
# Check if variable is in .env
ssh $OCI_USER@$OCI_HOST "grep DASHBOARD_JWT_SECRET /home/opc/orienter/.env"

# Check if container has the variable
ssh $OCI_USER@$OCI_HOST "docker exec orienter-dashboard env | grep DASHBOARD"
```

## CI/CD Pipeline

### GitHub Actions Workflow (.github/workflows/deploy.yml)

The deployment pipeline:

1. **Detect Changes** - Determines which images need rebuilding (8s)
2. **Tests** - Runs `pnpm run test:ci` (excludes e2e/eval tests)
3. **Build Images** - Only builds changed packages (conditional)
4. **Deploy** - Syncs files and restarts services

### Common CI Failures

| Issue | Cause | Fix |
|-------|-------|-----|
| `Cannot find package 'yaml'` | Missing devDependency | `pnpm add -Dw yaml` |
| `No test found in suite` | Eval tests included | Use `test:ci` instead of `test` |
| Dockerfile not found | Path changed | Update workflow matrix |
| Container name conflict | V1/V2 name mismatch | Clean up both names |
| `Missing parameter name at index 1: *` | Express 5 breaking change | See Express 5 section below |

### Express 5 / path-to-regexp v8 Breaking Changes

Express 5 uses path-to-regexp v8, which has breaking changes:

**Problem**: Bare `*` wildcards no longer work
```typescript
// ❌ BROKEN in Express 5
app.get('*', (req, res) => { ... });

// ✅ FIXED - use named wildcard
app.get('/{*splat}', (req, res) => { ... });
```

**Error message**: `TypeError: Missing parameter name at index 1: *`

**Where to check**: Any SPA catch-all routes in:
- `packages/dashboard/src/server/index.ts`
- `src/dashboard/server.ts`

## Nginx Configuration for SPAs

When proxying SPA routes, ensure the `proxy_pass` strips prefixes correctly:

```nginx
# ❌ WRONG - passes /dashboard/assets/ to server expecting /assets/
location /dashboard/assets/ {
    proxy_pass http://dashboard_upstream/dashboard/assets/;
}

# ✅ CORRECT - strips /dashboard prefix
location /dashboard/assets/ {
    proxy_pass http://dashboard_upstream/assets/;
}
```

**Symptom**: Browser shows "Failed to load module script: Expected JavaScript but got text/html"

**Debug**:
```bash
# Check content-type of assets
curl -sI "https://ai.proph.bet/dashboard/assets/index-*.js" | grep content-type

# Should be: content-type: text/javascript; charset=utf-8
# If it's: content-type: text/html → nginx routing issue
```

## Health Verification

### Production Health Checks

```bash
# Check all containers
ssh $OCI_USER@$OCI_HOST "docker ps --format 'table {{.Names}}\t{{.Status}}'"

# Check specific services
curl -sf https://ai.proph.bet/health        # Nginx
curl -sf https://ai.proph.bet/opencode/global/health  # OpenCode
curl -sf https://ai.proph.bet/dashboard/api/health    # Dashboard
```

### Expected Container Names (v2)
- `orienter-nginx`
- `orienter-bot-whatsapp` (not `orienter-whatsapp-bot`)
- `orienter-opencode`
- `orienter-dashboard`
- `orienter-postgres`
- `orienter-minio` (or using R2)

## Rollback Procedure

### Automatic Rollback
The CI pipeline automatically rolls back if health checks fail.

### Handling Deployment Verification Timeouts

The CI/CD pipeline has a health verification step that can trigger false-negative rollbacks if services haven't fully started.

**Root cause**: The verification step uses a 10-second wait + 10-second timeout, but nginx and other services may need more time to become healthy.

**Timing requirements**:
| Service | Time to Healthy After Container Start |
|---------|--------------------------------------|
| Postgres | ~5s (healthcheck interval) |
| Dashboard | ~5-10s |
| OpenCode | ~10-15s |
| Nginx | ~10-15s (depends on upstream resolution) |

**Critical dependency**: The production nginx config references staging upstreams (`orienter-opencode-staging:5099`, etc.). **Both production AND staging stacks must be running on a shared Docker network** for nginx to start.

**When verification fails but services are actually healthy**:
```bash
# 1. Check actual container health
ssh $OCI_USER@$OCI_HOST "docker ps --format 'table {{.Names}}\t{{.Status}}'"

# 2. If nginx is in restart loop, check for staging DNS issues
ssh $OCI_USER@$OCI_HOST "docker logs orienter-nginx --tail 20 2>&1 | grep -i 'host not found'"

# 3. If staging containers are missing, start them
ssh $OCI_USER@$OCI_HOST "cd /home/opc/orienter/docker && \
  docker compose -p staging --env-file ../.env \
    -f docker-compose.v2.yml \
    -f docker-compose.staging.yml \
    up -d"

# 4. Connect staging to production network
PROD_NETWORK="docker_orienter-network"
ssh $OCI_USER@$OCI_HOST "docker network connect $PROD_NETWORK orienter-opencode-staging 2>/dev/null || true"
ssh $OCI_USER@$OCI_HOST "docker network connect $PROD_NETWORK orienter-dashboard-staging 2>/dev/null || true"
ssh $OCI_USER@$OCI_HOST "docker network connect $PROD_NETWORK orienter-bot-whatsapp-staging 2>/dev/null || true"

# 5. Restart nginx to resolve staging hostnames
ssh $OCI_USER@$OCI_HOST "docker restart orienter-nginx"

# 6. Verify production health
curl -sf https://ai.proph.bet/health && echo "Nginx: OK"
curl -sf https://ai.proph.bet/dashboard/api/health && echo "Dashboard: OK"
```

**Why automatic rollback can fail**:
1. Rollback restarts production containers
2. Nginx tries to resolve staging upstream hostnames
3. If staging containers aren't running, nginx crashes with "host not found"
4. The rollback appears to complete but nginx is in a restart loop

**Prevention**: Ensure staging stack is always running on production server, or modify nginx config to not require staging upstreams.

### Manual Rollback
```bash
ssh $OCI_USER@$OCI_HOST

cd ~/orienter/docker
COMPOSE_FILES="-f docker-compose.v2.yml -f docker-compose.prod.yml -f docker-compose.r2.yml"

# Find latest backup
ls -t ~/orienter/backups | head -5

# Restore
LATEST=$(ls -t ~/orienter/backups | head -1)
sudo docker compose ${COMPOSE_FILES} down
cp -f ~/orienter/backups/${LATEST}/*.yml .
sudo docker compose ${COMPOSE_FILES} up -d
```

### Rollback to Legacy (v1 Compose)
If v2 causes issues, temporarily revert:
```bash
export USE_V2_COMPOSE=0
./deploy-server.sh deploy
```

## Troubleshooting

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

### Dashboard Assets Not Loading

1. Check nginx routing:
   ```bash
   curl -sI "https://ai.proph.bet/dashboard/assets/index-*.js" | grep content-type
   ```

2. If returning `text/html`, fix nginx `proxy_pass` to strip `/dashboard` prefix

3. Verify assets exist in container:
   ```bash
   ssh $OCI_USER@$OCI_HOST "docker exec orienter-dashboard ls -la /app/packages/dashboard/public/assets/"
   ```

### SSL Certificate Issues

```bash
# Check certificate paths
ls -la ~/orienter/certbot/conf/live/

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

### WhatsApp Pairing Issues After Deploy

```bash
# Container restart usually fixes pairing issues
docker restart orienter-bot-whatsapp

# Full reset if needed (clears session)
rm -rf ~/orienter/data/whatsapp-auth/*
docker restart orienter-bot-whatsapp
```

### Staging Deployment Port Conflicts

**Symptom**: Staging deployment fails with:
```
Error response from daemon: Bind for 0.0.0.0:5432 failed: port is already allocated
```

**Cause**: Staging and production share the same Oracle Cloud server. When staging compose tries to bind to ports already used by production (postgres:5432, dashboard:4098, etc.), it fails.

**Known limitation**: The current staging compose files use the same ports as production, making simultaneous staging and production deployments impossible on the same host.

**Workarounds**:
1. **Use different ports for staging** (requires compose file changes):
   ```yaml
   # docker-compose.staging.yml
   postgres:
     ports:
       - "5433:5432"  # Different host port
   dashboard:
     ports:
       - "4198:4098"  # Different host port
   ```

2. **Deploy staging when production is stopped** (not recommended for live systems)

3. **Use separate staging infrastructure** (recommended for production systems)

4. **Skip staging and deploy directly to production** (acceptable for low-risk changes like documentation or minor fixes)

**Current approach**: For changes that only affect packages/dashboard or other isolated components, verify locally with `./run.sh dev`, then deploy directly to main/production after confirming the Docker image builds successfully.

## Lessons Learned

### 1. Always Use test:ci in CI Pipeline
The `pnpm test` command runs ALL tests including eval tests which require external services. Use `pnpm test:ci` which excludes e2e and eval tests.

### 2. Service Name Consistency
When migrating compose files, ensure ALL overlay files (prod, r2, local) use the same service names. Mismatches cause "service not found" errors.

### 3. Express 5 Breaking Changes
Express 5 uses path-to-regexp v8 which doesn't allow bare `*` wildcards. Always use named wildcards like `/{*splat}` for catch-all routes.

### 4. Nginx SPA Routing
When proxying SPA applications, ensure `proxy_pass` correctly strips path prefixes. The dashboard serves assets at `/assets/`, not `/dashboard/assets/`.

### 5. Smart Change Detection
Config-only changes (nginx, compose files) don't require image rebuilds. The pipeline automatically skips builds when only config files change.

### 6. Force Rebuild When Needed
If change detection misses something, use the "Force rebuild all images" option in the GitHub Actions workflow dispatch.

### 7. Dependency Changes Require CI Build
If you add dependencies locally (e.g., `pnpm add -Dw yaml`), commit and push the package.json and lockfile changes for CI to use them.

### 8. Environment Variables Require Container Recreation
`docker restart` does NOT reload environment variables. Always use `docker compose up -d` to recreate containers when env vars change. Use `--env-file` flag when .env is in a different directory.

### 9. Keep GitHub Secrets in Sync
Maintain three sources of truth: `.env.production` (local), GitHub Secrets (CI/CD), and server `.env` (runtime). Update all three when adding new environment variables.

### 10. Staging Uses _STAGING Suffix
Staging environment expects environment variables with `_STAGING` suffix. Missing staging-specific variables cause crash loops even if production variables exist.

### 11. Database Name Defaults in Compose Files
When compose files change default values (like `POSTGRES_DB` changing from `whatsapp_bot` to `whatsapp_bot_0` for multi-instance support), production may break if the `.env` doesn't have an explicit override. Always check existing database names on production before deploying compose changes, and add explicit `POSTGRES_DB=<existing_name>` to `.env` to maintain backward compatibility.

### 12. Build Workspace Packages Before Tests in CI
When using `pnpm run test:ci` in CI pipelines with monorepo structure, tests may fail with:
```
Error: Failed to resolve entry for package "@orient/agents"
```

This happens because workspace packages need to be built before tests can import them. The deploy workflow must include a build step:
```yaml
- name: Build workspace packages
  run: pnpm turbo build --filter="@orient/*"
  env:
    NODE_OPTIONS: "--max-old-space-size=4096"

- name: Run tests
  run: pnpm run test:ci
```

**Note:** This was added to `.github/workflows/deploy.yml` after encountering this issue in production.

### 13. Monorepo Workspace Package Exports
When creating packages in a pnpm monorepo, ensure `package.json` has proper exports configuration:

```json
{
  "name": "@orient/core",
  "main": "./dist/index.js",
  "types": "./dist/index.d.ts",
  "exports": {
    ".": {
      "import": "./dist/index.js",
      "types": "./dist/index.d.ts"
    }
  }
}
```

**Common issues:**
- Missing `exports` field causes "Failed to resolve entry for package" errors
- Missing `types` field breaks TypeScript imports
- `main` pointing to `src/` instead of `dist/` causes unbuild code to be imported

### 14. Code Migration Gaps (src/ vs packages/)
When migrating from a monolithic structure (`src/`) to monorepo packages (`packages/`), some code may not be migrated:

| Symptom | Cause |
|---------|-------|
| Feature works locally but not in production Docker | Local dev uses `src/` but Docker uses `packages/` |
| API endpoint returns 404 in production | Routes exist in old location but not new |
| Tests pass locally but feature broken in prod | Test runs against `src/`, prod runs `packages/` |

**Debug pattern:**
```bash
# Check if endpoint exists in production
ssh $OCI_USER@$OCI_HOST "curl -s http://localhost:4098/api/your-endpoint"
# Returns "Cannot GET /api/your-endpoint" = route not migrated

# Check local (uses src/)
curl -s http://localhost:4098/api/your-endpoint
# Returns auth error or data = route exists locally
```

**Known migration gaps:**
- MCP routes (`/api/mcp/*`) - migrated to `packages/dashboard/src/server/routes/mcp.routes.ts`

**Prevention:** When adding features to `src/`, also add them to the corresponding `packages/` directory. Better yet, deprecate `src/` paths and only develop in `packages/`.

### 15. Partial Deployment Failures
When deploying changes that trigger multiple image builds, some may succeed while others fail. The CI pipeline requires ALL images to build successfully before deploying:

- Successful images ARE pushed to the registry
- The deployment job won't run because it requires ALL builds to pass
- Production continues running with old images

**Recovery:** Manually deploy successful images via SSH, then fix and retry the failed image. See "Handling Partial Deployment Failures" section above.

This prevents partial deployments where some services get updated but not others, which could cause compatibility issues.

### 16. Deployment Verification Timeouts and Staging Dependencies
The CI/CD verification step can timeout while services are still starting, triggering unnecessary rollbacks. Key points:
- Nginx needs 10-15 seconds after container start to become healthy
- The verification window (10s wait + 10s timeout) may not be enough
- **Critical**: Production nginx requires staging containers on a shared Docker network to resolve upstream hostnames
- If staging isn't running, nginx enters a restart loop with "host not found in upstream" errors
- After any deployment or rollback, ensure staging stack is started and connected to the production network

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
