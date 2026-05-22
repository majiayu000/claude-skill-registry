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
| Website-only change (Docusaurus)    | ~20 min      | ~2-3 min     |
| All packages change                 | ~20 min      | ~20 min      |

### Website-Only Deployments

When you modify only website files (Docusaurus documentation), the deployment is extremely fast because:

**What Gets Skipped:**

- No Docker image builds (OpenCode, WhatsApp, Dashboard)
- No image pushes to GHCR
- No container recreation on the server

**What Still Runs:**

1. **Detect Changes** (~8s) - Identifies website-only changes
2. **Run Tests** (~40s) - Runs test suite
3. **Deploy to Oracle Cloud** (~2min) - Only syncs website files and restarts nginx

**Files That Trigger Website-Only Deployment:**

- `website/docs/**` - Documentation markdown files
- `website/src/**` - Custom React pages (e.g., privacy.tsx, terms.tsx)
- `website/docusaurus.config.ts` - Site configuration
- `website/static/**` - Static assets
- `website/sidebars.ts` - Navigation configuration

**Example Deployment:**

```bash
# Change detection output for website-only changes
changes_opencode: false
changes_whatsapp: false
changes_dashboard: false
changes_website: true

# Build jobs are skipped
Build OpenCode Image: skipped
Build WhatsApp Bot Image: skipped
Build Dashboard Image: skipped

# Deploy job syncs website files
Deploy to Oracle Cloud: success (2min)
```

**What Gets Deployed:**
The deploy job syncs the `website/` directory to the server and runs:

```bash
# Build static Docusaurus site
cd ~/orient/website && npm run build

# Nginx serves the built site from website/build/
# No container restarts needed (except nginx reload for config changes)
```

**Quick Website Updates:**
For documentation or content changes, this means you can deploy in under 3 minutes total - perfect for rapid iterations on privacy policies, terms, blog posts, or documentation updates.

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

| Issue                                       | Cause                     | Fix                             |
| ------------------------------------------- | ------------------------- | ------------------------------- |
| `Cannot find package`                       | Missing devDependency     | Check pnpm-lock.yaml            |
| `No test found in suite`                    | Eval tests included       | Use `test:ci` instead of `test` |
| Dockerfile not found                        | Path changed              | Update workflow matrix          |
| Container name conflict                     | V1/V2 name mismatch       | Clean up both names             |
| `Missing parameter name at index 1: *`      | Express 5 breaking change | Use `/{*splat}` not `*`         |
| `SKILL.md file(s) with invalid frontmatter` | Missing YAML metadata     | Add `---` delimited frontmatter |

### Skill File Validation Failures

The CI pipeline validates all SKILL.md files have proper YAML frontmatter metadata.

**Error Example:**

```
Error: Found 2 SKILL.md file(s) with invalid frontmatter:
  - .claude/skills/personal-vite-jsx-caching-fix/SKILL.md: File does not start with frontmatter delimiter (---)
  - .claude/skills/personal-crypto-secrets-management/SKILL.md: File does not start with frontmatter delimiter (---)
```

**Required YAML Frontmatter Format:**

```yaml
---
name: my-skill-name
description: "Brief description of what this skill does"
---

# Skill Title
... rest of skill content ...
```

**Common Issues with Multi-Repo Setups:**

When using a personal fork (e.g., `orient-core/orient`) that has additional skills not in the OSS repo (`orient-bot/orient`):

1. **Personal skills are gitignored in OSS** - Files starting with `personal-` are in `.gitignore`
2. **Tests run on ALL skill files** - Including personal skills that may lack frontmatter
3. **OSS repo passes, personal repo fails** - Because personal skills weren't tested upstream

**Recovery Workflow:**

```bash
# 1. Checkout the failing repo's main branch
git fetch deploy main
git checkout -B fix-skill-frontmatter deploy/main

# 2. Find skills missing frontmatter
grep -L "^---" .claude/skills/*/SKILL.md

# 3. Add frontmatter to each file
# File must START with --- (no content before it)

# 4. Commit and push fix
git add .claude/skills/
git commit -m "fix(skills): add YAML frontmatter to skill files"
git push deploy fix-skill-frontmatter:main

# 5. Re-trigger deployment
gh workflow run deploy.yml -f force_build_all=true --repo YOUR_ORG/YOUR_REPO
```

**Validation Test Location:** `tests/config/skill-files.test.ts`

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

### Multi-Repository Deployment (Self-Hosted Runners)

#### Jobs Stuck in "Queued" State

**Error**: Docker build jobs show "queued" status for 10+ minutes without starting.

**Cause**: The workflow requires self-hosted ARM64 runners (`runs-on: [self-hosted, linux, arm64]`), but you triggered the workflow on a repository that doesn't have the runner registered.

**Diagnosis**:

```bash
# Check your git remotes
git remote -v

# Example output showing two repos:
# deploy	https://github.com/orient-core/orient.git (fetch/push)  ← Has self-hosted runner
# origin	https://github.com/orient-bot/orient.git (fetch/push)   ← OSS repo, no runner

# Check which repo the runner is registered to
ssh opc@152.70.172.33 "systemctl status actions.runner.* 2>/dev/null | head -5"
# Look for: actions.runner.orient-core-orient.oracle-arm64.service
#                          ^^^^^^^^^^^^ This shows the org/repo
```

**Fix**: Trigger the workflow on the repository that has the self-hosted runner:

```bash
# Cancel the stuck workflow
gh run cancel <run_id> --repo orient-bot/orient

# Trigger on the correct repo (orient-core/orient has the runner)
gh workflow run deploy.yml -f force_build_all=true --repo orient-core/orient

# Monitor the new workflow
gh run list --repo orient-core/orient --limit 3
gh run watch <new_run_id> --repo orient-core/orient --exit-status
```

**Understanding the Two Repositories**:

| Repository           | Remote   | Purpose                 | Self-Hosted Runner |
| -------------------- | -------- | ----------------------- | ------------------ |
| `orient-bot/orient`  | `origin` | Open source repo        | ❌ No              |
| `orient-core/orient` | `deploy` | Private deployment repo | ✅ Yes (ARM64)     |

**Key Points**:

- The OSS repo (`orient-bot/orient`) doesn't have self-hosted runners - Docker builds will never start
- Production deployments must be triggered on `orient-core/orient` where the ARM64 runner is registered
- The runner is running on the Oracle Cloud server as a systemd service
- GitHub-hosted runners won't work because the workflow specifies `[self-hosted, linux, arm64]`

**Verifying Runner Status**:

```bash
# Check if the runner service is running on the server
ssh opc@152.70.172.33 "systemctl status actions.runner.orient-core-orient.oracle-arm64.service"

# Should show:
# Active: active (running)
# ... Listening for Jobs

# Check recent job history
ssh opc@152.70.172.33 "journalctl -u actions.runner.orient-core-orient.oracle-arm64.service --since '1 hour ago' | grep -E '(Running job|completed)'"
```

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

### ESM Module Import Resolution Issues

When running tests in CI or locally, you may encounter module resolution errors for subpath exports.

#### Subpath Export Resolution Failures

**Error**: `Cannot find package '@orient/integrations/google' imported from '...'`

**Cause**: Vitest/tsx may not correctly resolve package subpath exports (e.g., `@orient/integrations/google`) even when the `exports` field in package.json is properly configured.

**Fix**: Use the main export instead of subpath exports:

```typescript
// BROKEN - subpath export may not resolve in vitest
import { getGoogleOAuthService } from '@orient/integrations/google';

// FIXED - use main export (re-exports all submodules)
import { getGoogleOAuthService } from '@orient/integrations';
```

**Why This Happens**: The package.json exports field specifies `./dist/...` paths for subpath exports. While Node.js resolves these correctly at runtime, vitest/tsx running TypeScript directly may fail to resolve them during tests.

#### Stray .js Files in Source Directories

**Error**: Tests fail with old code even after fixing TypeScript source files.

**Cause**: Compiled `.js` files accidentally exist in `src/` directories alongside `.ts` files. Vitest may load the stale compiled files instead of the updated TypeScript sources.

**Diagnosis**:

```bash
# Find stray .js files in source directories
find packages/*/src -name "*.js" -type f

# Check if the error points to a .js file in src/
grep -r "integrations/google" packages/*/src/*.js
```

**Fix**:

```bash
# Remove stray compiled files from source directories
rm packages/dashboard/src/server/routes/*.js
rm packages/dashboard/src/server/routes/*.js.map

# These should only exist in dist/, not src/
```

**Prevention**: Add to `.gitignore`:

```
# Ignore compiled JS in source directories
packages/*/src/**/*.js
packages/*/src/**/*.js.map
```

#### Test Failure Diagnosis Workflow

When CI tests fail with import errors across multiple service files:

1. **Check the actual error location**:

   ```bash
   gh run view RUN_ID --log-failed | grep -A5 "Cannot find"
   ```

2. **Verify the import in source files**:

   ```bash
   grep -r "integrations/google" packages/*/src/
   ```

3. **Look for stray compiled files**:

   ```bash
   find packages -path "*/src/*.js" -type f
   ```

4. **Rebuild after fixing**:
   ```bash
   pnpm turbo build --filter=@orient/dashboard
   pnpm test:ci
   ```

#### Docker Compose Test Updates for Multi-Instance Support

When container naming schemes change (e.g., adding instance IDs for multi-instance support), existing docker compose tests may fail.

**Error**: `expected 'orienter-bot-whatsapp-${AI_INSTANCE_ID:-0}' to be 'orienter-bot-whatsapp'`

**Cause**: Tests expect fixed container names but compose files now use instance-aware naming.

**Fix**: Update `tests/docker/compose.test.ts` to expect the new naming pattern:

```typescript
// OLD - fixed names
expect(compose.services['bot-whatsapp'].container_name).toBe('orienter-bot-whatsapp');

// NEW - instance-aware names
expect(compose.services['bot-whatsapp'].container_name).toBe(
  'orienter-bot-whatsapp-${AI_INSTANCE_ID:-0}'
);
```

### Worktree Checkout Conflicts

When working in a git worktree, you may encounter branch checkout conflicts when trying to merge PRs.

**Error:**

```
fatal: 'main' is already used by worktree at '/path/to/other-worktree'
```

**Cause:** Git prevents checking out a branch that's already checked out in another worktree. This happens when:

- You try to run `gh pr merge` which attempts to checkout the target branch (main)
- Another worktree already has the `main` branch checked out
- Git's safety mechanism prevents conflicts between worktrees

**Workaround Options:**

**Option 1: Use GitHub API (Recommended)**

Merge PRs without checking out the target branch:

```bash
# Merge PR with squash
gh api repos/orient-bot/orient/pulls/PR_NUMBER/merge -X PUT \
  -f merge_method=squash \
  -f commit_title="Your commit title (#PR_NUMBER)"

# Example
gh api repos/orient-bot/orient/pulls/50/merge -X PUT \
  -f merge_method=squash \
  -f commit_title="docs(website): add Privacy Policy and Terms pages (#50)"
```

**Option 2: Use Auto-Merge**

Enable auto-merge and let GitHub merge when checks pass:

```bash
gh pr merge PR_NUMBER --auto --squash
```

**Option 3: Switch to Main Worktree**

Navigate to the worktree that has `main` checked out:

```bash
# Find which worktree has main
git worktree list | grep main

# Navigate to that worktree
cd /path/to/main-worktree

# Merge from there
gh pr merge PR_NUMBER --squash --delete-branch
```

**Option 4: Merge from GitHub Web UI**

When automation fails, use the GitHub web interface:

1. Navigate to the PR on GitHub
2. Click "Squash and merge" button
3. Confirm the merge

**Prevention:**

When creating worktrees for feature branches, avoid checking out `main` in multiple worktrees:

```bash
# Good - each worktree has its own branch
git worktree add ~/worktrees/feature-a -b feature-a
git worktree add ~/worktrees/feature-b -b feature-b

# Avoid - multiple worktrees with main
git worktree add ~/worktrees/work-1 main  # First is OK
git worktree add ~/worktrees/work-2 main  # This will fail
```

**Why This Matters:**

This worktree limitation only affects the merge operation itself. You can:

- ✅ Create PRs from worktree branches
- ✅ Push changes from worktrees
- ✅ Review and approve PRs
- ✅ Run CI/CD workflows
- ❌ Merge PRs using `gh pr merge` when main is checked out elsewhere

The GitHub API workaround bypasses the local git checkout, making it the most reliable option when working with worktrees.

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
