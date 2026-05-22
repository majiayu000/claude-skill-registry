---
name: deploy-frappe
description: Deploy Frappe HRMS code changes to AWS production. Use when you need to deploy Python/API changes to the Frappe Docker container.
allowed-tools: Bash, Read, Grep, WebFetch
user-invocable: true
---

# /deploy-frappe - Frappe HRMS Deployment

## What This Command Does

Deploys code changes from the `production` branch to AWS EC2 running Frappe Docker.

**IMPORTANT:** Frappe Docker uses `--preload`, so Python code changes require rebuilding the Docker image. This command handles that automatically.

**TEST LOCALLY FIRST:** Always test your changes in the local development environment before deploying to production. Use `/local-frappe` to set up and manage local development.

## Quick Reference

| Deployment Type | Method | Time |
|-----------------|--------|------|
| Python/API changes | Full rebuild via GitHub Actions | 5-10 min |
| Python/API changes (no cache) | Full rebuild with `no_cache=true` | 8-12 min |
| DocType schema changes | Rebuild + `bench migrate` | 8-12 min |
| Config/data only | SSM command (no rebuild) | 2-3 min |
| Emergency rollback | SSM with previous tag | 2-3 min |

## ⚠️ CRITICAL: Docker Build Caching Issue

**Problem discovered 2026-01-29:** When pushing Python/API code changes, the build may use cached Docker layers and **NOT include your new code**.

### When to Use `no_cache=true`

| Scenario | Use `no_cache=true`? |
|----------|---------------------|
| Python code changes (`.py` files) | **YES** - Always |
| DocType JSON changes | **YES** - Always |
| Workflow config changes | No - Cache is fine |
| Dependencies changes (`apps.json`) | **YES** - Always |

### How to Deploy with No Cache

**Option 1: Manual Workflow Dispatch (Recommended)**
```bash
gh workflow run build-and-deploy.yml --repo Bebang-Enterprise-Inc/hrms -f no_cache=true
```

**Option 2: Via GitHub UI**
1. Go to https://github.com/Bebang-Enterprise-Inc/hrms/actions
2. Select "Build and Deploy Frappe HRMS"
3. Click "Run workflow"
4. **Check `no_cache` checkbox** ← IMPORTANT
5. Click "Run workflow"

### Why This Happens

The Docker build uses layer caching. The HRMS app is cloned during build via `apps.json`. If the git clone step is cached, your new commits won't be included even though they're in the repo.

**Build time comparison:**
- With cache: ~30 seconds (may miss code changes)
- Without cache: ~5 minutes (guaranteed fresh code)

## Infrastructure (UPDATED 2026-01-29 - DOCKER SWARM)

| Component | Value |
|-----------|-------|
| EC2 Instance | `i-026b7477d27bd46d6` |
| Docker Image | `samkarazi/bebang-erpnext-hrms:v15` |
| Site | `hq.bebang.ph` |
| Region | `ap-southeast-1` |
| Server Path | `/home/ubuntu/frappe_docker` |
| **Orchestration** | **Docker Swarm** (migrated 2026-01-29) |
| Stack Name | `frappe` |
| Stack File | `stack.yml` |
| Frontend Port | 80 (ADMS receiver uses 8080) |

### Swarm Services (9 total)

| Service | Replicas | Purpose |
|---------|----------|---------|
| `frappe_backend` | 1 | Gunicorn API server |
| `frappe_frontend` | 1 | Nginx reverse proxy |
| `frappe_websocket` | 1 | Socket.IO server |
| `frappe_queue-short` | 1 | Short job queue worker |
| `frappe_queue-long` | 1 | Long job queue worker |
| `frappe_scheduler` | 1 | Background scheduler |
| `frappe_db` | 1 | MariaDB database |
| `frappe_redis-cache` | 1 | Redis cache |
| `frappe_redis-queue` | 1 | Redis queue |

### Volume Configuration

The site data is stored in external volumes:

| Volume | Purpose |
|--------|---------|
| `bebang-hrms_sites` | Site data, configs |
| `bebang-hrms_db-data` | MariaDB data |
| `bebang-hrms_logs` | Application logs |
| `bebang-hrms_redis-queue-data` | Redis queue data |

**Backups:** `/home/ubuntu/backups/swarm-migration-20260129/` (pre-migration backup)

## Deployment Methods

### Method 1: PR Workflow (Recommended) - INCLUDES AUTO-CLEANUP

**The `production` branch is protected.** Use the PR workflow.

**Note:** The GitHub Actions workflow automatically cleans up old images after each successful deployment, keeping the 4 most recent versions. No manual cleanup needed when using this method.

```bash
# 1. Create feature branch (if not already on one)
/feature-branch my-api-change

# 2. Commit your changes
git add .
git commit -m "feat: Add employee_clearance API"

# 3. Deploy via PR (auto-merges when CI passes)
/pr-deploy --auto-merge
```

This creates a PR, enables auto-merge, and GitHub Actions builds and deploys when the PR merges.

See `/workflow` for the full deployment workflow.

### Method 1b: Manual Workflow Dispatch

For triggering a rebuild without merging (e.g., to force `no_cache`):

1. Go to https://github.com/Bebang-Enterprise-Inc/hrms/actions
2. Select "Build and Deploy Frappe HRMS"
3. Click "Run workflow"
4. Options:
   - **`no_cache`**: Build without Docker cache (**USE THIS FOR CODE CHANGES**)
   - `skip_build`: Skip image rebuild (deploy existing)
   - `run_migrate`: Run `bench migrate` after deploy

### Method 2: AWS SSM Direct (Quick Deploy via Swarm Rolling Update)

Use when image is already built and you need to update services with zero downtime:

```bash
# Get AWS credentials
export AWS_ACCESS_KEY_ID=$(doppler secrets get AWS_ACCESS_KEY_ID --project bei-erp --config dev --plain)
export AWS_SECRET_ACCESS_KEY=$(doppler secrets get AWS_SECRET_ACCESS_KEY --project bei-erp --config dev --plain)
export AWS_DEFAULT_REGION=ap-southeast-1

# Rolling update all services (ZERO DOWNTIME) + CLEANUP OLD IMAGES
aws ssm send-command \
  --instance-ids "i-026b7477d27bd46d6" \
  --document-name "AWS-RunShellScript" \
  --parameters 'commands=[
    "echo === Updating services ===",
    "docker service update --image samkarazi/bebang-erpnext-hrms:v15 frappe_backend",
    "docker service update --image samkarazi/bebang-erpnext-hrms:v15 frappe_frontend",
    "docker service update --image samkarazi/bebang-erpnext-hrms:v15 frappe_websocket",
    "docker service update --image samkarazi/bebang-erpnext-hrms:v15 frappe_queue-short",
    "docker service update --image samkarazi/bebang-erpnext-hrms:v15 frappe_queue-long",
    "docker service update --image samkarazi/bebang-erpnext-hrms:v15 frappe_scheduler",
    "docker service ls",
    "echo === Cleaning up old images (keeping 4 newest) ===",
    "docker container prune -f",
    "IMAGES=$(docker images samkarazi/bebang-erpnext-hrms --format \"{{.ID}}\" | tail -n +5)",
    "if [ -n \"$IMAGES\" ]; then docker rmi $IMAGES 2>/dev/null || true; fi",
    "docker image prune -f",
    "df -h / | tail -1"
  ]' \
  --output json
```

**Benefits of Swarm (migrated 2026-01-29):**
- Zero-downtime rolling updates
- Automatic rollback on failure (`docker service rollback <service>`)
- No CSS 404 issues (containers fully recreated)

**Check service status:**
```bash
aws ssm send-command \
  --instance-ids "i-026b7477d27bd46d6" \
  --document-name "AWS-RunShellScript" \
  --parameters 'commands=["docker service ls"]' \
  --output json
```

### Method 3: Manual Image Build (Recovery/Debug)

Use when GitHub Actions fails or you need custom build:

```bash
# 1. Clone frappe_docker
git clone https://github.com/frappe/frappe_docker.git
cd frappe_docker

# 2. Copy apps.json from BEI-ERP repo
cat > apps.json << 'EOF'
[
    {"url": "https://github.com/frappe/erpnext", "branch": "version-15"},
    {"url": "https://github.com/frappe/payments", "branch": "version-15"},
    {"url": "https://github.com/Bebang-Enterprise-Inc/hrms", "branch": "production"}
]
EOF
# Note: Repo is public, so no authentication needed for cloning

# 3. Build image
export APPS_JSON_BASE64=$(base64 -w 0 apps.json)
docker build \
  --no-cache \
  --build-arg FRAPPE_BRANCH=version-15 \
  --build-arg PYTHON_VERSION=3.11.6 \
  --build-arg NODE_VERSION=20.19.2 \
  --build-arg APPS_JSON_BASE64=$APPS_JSON_BASE64 \
  --file images/custom/Containerfile \
  --tag bebang/erpnext-hrms:v15-$(date +%Y%m%d) \
  --tag bebang/erpnext-hrms:v15 \
  .

# 4. Push to Docker Hub
docker login
docker push bebang/erpnext-hrms:v15-$(date +%Y%m%d)
docker push bebang/erpnext-hrms:v15

# 5. Deploy to server (via SSM - see Method 2)
```

## Post-Deployment Steps

### Automatic Image Cleanup (ALWAYS RUN)

**After every deployment, clean up old images to prevent disk space issues.**

The server has limited storage (50 GB). Each deployment creates a new ~2.5 GB image. Without cleanup, the disk fills up within days.

**Policy:** Keep the 4 most recent images, remove all older ones.

```bash
# Run this after every successful deployment
aws ssm send-command \
  --instance-ids "i-026b7477d27bd46d6" \
  --document-name "AWS-RunShellScript" \
  --parameters 'commands=[
    "echo \"=== Cleaning up old Docker images (keeping 4 newest) ===\"",
    "docker container prune -f",
    "IMAGES=$(docker images samkarazi/bebang-erpnext-hrms --format \"{{.ID}}\" | tail -n +5)",
    "if [ -n \"$IMAGES\" ]; then docker rmi $IMAGES 2>/dev/null || true; fi",
    "docker image prune -f",
    "echo \"=== Disk usage after cleanup ===\"",
    "df -h / | tail -1"
  ]' \
  --output json
```

**What this does:**
1. Removes exited containers (from previous deployments)
2. Lists all bebang-erpnext-hrms images, skips the 4 newest, removes the rest
3. Removes any remaining dangling images
4. Reports disk usage

**Expected savings:** ~2.5 GB per old image removed.

### Run Migrations (if schema changed)

```bash
# Get the backend container ID
aws ssm send-command \
  --instance-ids "i-026b7477d27bd46d6" \
  --document-name "AWS-RunShellScript" \
  --parameters 'commands=["docker exec $(docker ps -qf name=frappe_backend) bench --site hq.bebang.ph migrate"]' \
  --output json
```

### Clear Cache

```bash
aws ssm send-command \
  --instance-ids "i-026b7477d27bd46d6" \
  --document-name "AWS-RunShellScript" \
  --parameters 'commands=["docker exec $(docker ps -qf name=frappe_backend) bench --site hq.bebang.ph clear-cache"]' \
  --output json
```

### Verify API

```bash
# Use frappe.ping (doesn't require auth)
curl https://hq.bebang.ph/api/method/frappe.ping
# Expected: {"message":"pong"}

# Or check login page
curl -s -o /dev/null -w "%{http_code}" https://hq.bebang.ph/login
# Expected: 200
```

## Emergency Rollback

### Option A: Swarm Service Rollback (Fastest)

Docker Swarm keeps previous service state for instant rollback:

```bash
# Rollback individual services
aws ssm send-command \
  --instance-ids "i-026b7477d27bd46d6" \
  --document-name "AWS-RunShellScript" \
  --parameters 'commands=[
    "docker service rollback frappe_backend",
    "docker service rollback frappe_frontend",
    "docker service rollback frappe_websocket",
    "docker service rollback frappe_queue-short",
    "docker service rollback frappe_queue-long",
    "docker service rollback frappe_scheduler",
    "docker service ls"
  ]' \
  --output json
```

### Option B: Deploy Previous Image Tag

```bash
# Find previous tag from Docker Hub or deployment logs
# Tags are formatted: v15-YYYYMMDD-HHMMSS or v15-<short-sha>

aws ssm send-command \
  --instance-ids "i-026b7477d27bd46d6" \
  --document-name "AWS-RunShellScript" \
  --parameters 'commands=[
    "docker service update --image samkarazi/bebang-erpnext-hrms:v15-PREVIOUS_TAG frappe_backend",
    "docker service update --image samkarazi/bebang-erpnext-hrms:v15-PREVIOUS_TAG frappe_frontend",
    "docker service update --image samkarazi/bebang-erpnext-hrms:v15-PREVIOUS_TAG frappe_websocket",
    "docker service update --image samkarazi/bebang-erpnext-hrms:v15-PREVIOUS_TAG frappe_queue-short",
    "docker service update --image samkarazi/bebang-erpnext-hrms:v15-PREVIOUS_TAG frappe_queue-long",
    "docker service update --image samkarazi/bebang-erpnext-hrms:v15-PREVIOUS_TAG frappe_scheduler"
  ]' \
  --output json
```

### Option C: Return to Docker Compose (Last Resort)

If Swarm has issues, revert to Docker Compose:

```bash
aws ssm send-command \
  --instance-ids "i-026b7477d27bd46d6" \
  --document-name "AWS-RunShellScript" \
  --parameters 'commands=[
    "docker stack rm frappe",
    "sleep 30",
    "cd /home/ubuntu/frappe_docker",
    "docker compose -f pwd.yml -f volumes-override.yml up -d"
  ]' \
  --output json
```

## GitHub Secrets Required

These must be set in GitHub repo settings:

| Secret | Description | Where to get |
|--------|-------------|--------------|
| `DOCKERHUB_USERNAME` | Docker Hub username | Docker Hub account |
| `DOCKERHUB_TOKEN` | Docker Hub access token | Docker Hub > Account Settings > Security |
| `AWS_ACCESS_KEY_ID` | AWS IAM access key | `doppler secrets get AWS_ACCESS_KEY_ID --project bei-erp --config dev --plain` |
| `AWS_SECRET_ACCESS_KEY` | AWS IAM secret key | `doppler secrets get AWS_SECRET_ACCESS_KEY --project bei-erp --config dev --plain` |

## Common Issues

### Docker Cache Not Picking Up Code Changes (CRITICAL!)

**Symptom:** Build completes quickly (~2 minutes instead of ~10-15), but new APIs/pages return "module has no attribute" or 404 errors.

**Cause:** Docker's build cache doesn't detect when git repo contents change during `bench get-app`. Even though you pushed code, the build serves cached layers from previous builds.

**Build Time Indicator:**
| Build Time | What It Means | Action Required |
|------------|---------------|-----------------|
| ~2 min | CACHED - Old code deployed | Rebuild with `no_cache=true` |
| ~5-10 min | FRESH - New code deployed | None - working correctly |

**Fix:** ALWAYS use `no_cache=true` for code changes:
```bash
gh workflow run "Build and Deploy Frappe HRMS" --repo Bebang-Enterprise-Inc/hrms -f no_cache=true -f run_migrate=true
```

**This is NORMAL Docker behavior**, not corruption. The `apps.json` file didn't change, so Docker cached the layer where apps are cloned.

**Prevention:** Use `no_cache=true` whenever deploying:
- New API files
- Modified API files
- New www pages (like custom login)
- DocType changes
- Any Python code changes

**When `no_cache` is NOT needed:**
- Config-only changes (site_config.json)
- Data imports via SQL
- Clear cache operations

### Custom Login Page Not Serving (404)

**Symptom:** Created `hrms/www/login.html` but `/login` still shows Frappe's default login.

**Cause:** Frappe's `/login` route is handled specially and bypasses `page_renderer` hook.

**Fix:** Use `website_redirects` hook to redirect to a different route:

```python
# hrms/hooks.py
website_redirects = [
    {"source": "/login", "target": "/bei-login", "redirect_http_status": 302},
]
```

Then create `hrms/www/bei-login.html` and `hrms/www/bei-login.py`.

**Verification:**
```bash
curl -sI https://hq.bebang.ph/login | grep -i location
# Should show: Location: /bei-login
```

---

### "not whitelisted" Error

**Cause:** Function not in `@frappe.whitelist()` or `__init__.py` not updated

**Fix:**
1. Add `@frappe.whitelist()` decorator to function
2. Add import to `hrms/api/__init__.py`
3. Rebuild and deploy

### Container starts but API fails

**Check:**
```bash
# View logs
aws ssm send-command \
  --instance-ids "i-026b7477d27bd46d6" \
  --document-name "AWS-RunShellScript" \
  --parameters 'commands=["cd /home/ubuntu/frappe_docker && docker compose -f pwd.yml -f volumes-override.yml logs --tail=100 backend"]' \
  --output json
```

### Build fails: "Could not find branch"

**Cause:** Branch name in apps.json doesn't exist

**Fix:** Verify branch exists: `git ls-remote https://github.com/Bebang-Enterprise-Inc/hrms production`

### Port 8080 already in use

**Cause:** ADMS receiver nginx container uses port 8080

**Fix:** Use port 80 for Frappe frontend instead:
```bash
# In pwd.yml, change frontend ports from 8080:8080 to 80:8080
sed -i "s/8080:8080/80:8080/g" pwd.yml
```

### Frontend container won't start

**Cause:** Old containers from previous stacks still running

**Check:**
```bash
docker ps -a | grep -E "bebang|frappe"
```

**Fix:**
```bash
# Stop old stack containers
docker stop bebang-hrms-frontend-1 bebang-hrms-backend-1 ...
docker rm bebang-hrms-frontend-1 bebang-hrms-backend-1 ...
```

### New Domain Returns 404 (Site Not Found)

**Symptom:** Added new domain (e.g., hq.bebang.ph) but all pages return 404 or "Site not found".

**Cause 1:** Missing site symlink in `/home/frappe/frappe-bench/sites/`

**Fix:**
```bash
# Create symlink for new domain pointing to actual site
aws ssm send-command \
  --instance-ids "i-026b7477d27bd46d6" \
  --document-name "AWS-RunShellScript" \
  --parameters 'commands=["docker exec frappe_docker-backend-1 bash -c \"cd /home/frappe/frappe-bench/sites && ln -sf hrms.bebang.ph hq.bebang.ph\""]'
```

**Cause 2:** Wrong `FRAPPE_SITE_NAME_HEADER` in pwd.yml

| Setting | Effect |
|---------|--------|
| `FRAPPE_SITE_NAME_HEADER: frontend` | ❌ BROKEN - All requests routed to non-existent "frontend" site |
| `FRAPPE_SITE_NAME_HEADER: $host` | ✅ CORRECT - Uses actual hostname for routing |

**Fix:**
```bash
aws ssm send-command \
  --instance-ids "i-026b7477d27bd46d6" \
  --document-name "AWS-RunShellScript" \
  --parameters 'commands=["cd /home/ubuntu/frappe_docker && sed -i \"s/FRAPPE_SITE_NAME_HEADER: frontend/FRAPPE_SITE_NAME_HEADER: \\$host/g\" pwd.yml && docker compose -f pwd.yml -f volumes-override.yml restart frontend"]'
```

**Verify site routing:**
```bash
curl -sI https://hq.bebang.ph/api/method/frappe.ping | grep -i x-frappe-site-name
# Should show: X-Frappe-Site-Name: hrms.bebang.ph
```

## DO NOT DO

1. **NEVER use `docker commit`** - Corrupts the Python environment (learned 2026-01-22)
2. **NEVER edit files directly in container** - Changes lost on restart (--preload)
3. **NEVER use `-v` flag with `docker compose down`** - Deletes all data volumes
4. **NEVER skip `bench migrate`** after DocType changes
5. **NEVER assume server paths** - Always verify with `ls` first
6. **NEVER modify pwd.yml directly without restoring from git first** - sed errors accumulate
7. **NEVER set `FRAPPE_SITE_NAME_HEADER: frontend`** - Breaks multi-site routing (learned 2026-01-28)
8. **NEVER forget site symlinks for new domains** - Each domain needs symlink in sites/ directory (learned 2026-01-28)
9. **NEVER run `bench build` in production containers** - Causes CSS 404 errors (learned 2026-01-28)
10. **NEVER run `bench get-app` in production containers** - Official Frappe Docker policy
11. **NEVER use `docker compose up --no-deps`** - Doesn't refresh assets, causes CSS 404 (learned 2026-01-29)

---

## CRITICAL: Setup Wizard Redirect Loop Issue (2026-01-29) ✅

### Status: FIXED (Database Value Changed)

If `/app` causes infinite redirect loop after Google OAuth login with `setup_wizard.load_languages` being called repeatedly:

**Root Cause:** `tabDefaultValue` table has:
```sql
defkey='desktop:home_page' defvalue='setup-wizard'
```

**Fix:**
```sql
-- Run via bench console or direct MariaDB
UPDATE tabDefaultValue SET defvalue='Workspaces'
WHERE defkey='desktop:home_page' AND parent='__default';
```

**Also ensure these are set:**
```sql
-- Mark setup as complete
UPDATE tabDefaultValue SET defvalue='1'
WHERE defkey='setup_complete' AND parent='__default';

-- Mark HRMS app as setup complete
UPDATE `tabInstalled Application` SET is_setup_complete=1
WHERE app_name='hrms';
```

**Clear cache after:**
```bash
docker compose -f pwd.yml -f volumes-override.yml exec -T backend bench --site hrms.bebang.ph clear-cache
```

**Reference:** `docs/plans/FRAPPE_DEPLOYMENT_FIX_PLAN_2026-01-29.md`

---

## CSS 404 Asset Desync Issue - RESOLVED (2026-01-29, Updated 2026-01-29) ✅

### Status: PERMANENTLY FIXED

The GitHub Actions workflow has been updated to prevent CSS 404 errors. Every deployment now:
1. Runs Swarm rolling updates (recreates containers with fresh assets)
2. **Flushes Redis cache** (prevents stale HTML serving old asset hashes)
3. Verifies CSS/JS assets load correctly after deploy (fails workflow on 404)

**Commits:**
- `48f1c2f9b` - fix: Add asset volume reset and CSS health check to deployment
- `TBD` - fix: Add Redis flush step to prevent stale HTML caching

### The Original Problem

Running `bench build` or `bench migrate` in production containers caused CSS/JS 404 errors:
- Browser requests `desk.bundle.ABC123.css`
- Server only has `desk.bundle.XYZ789.css`
- Result: Entire application breaks (no styling)

**This caused 4 production outages, now prevented by workflow fix.**

### Root Cause

From [GitHub Issue #790](https://github.com/frappe/frappe_docker/issues/790):
> "Any new nginx images which have new assets at `/usr/share/nginx/html`, will not propagate these changes if the volume already exists."

**Architecture flaw:**
1. Assets are baked into Docker image at build time
2. Assets volume (`bebang-hrms_sites`) persists between deployments
3. `bench migrate` regenerates assets in backend container
4. Frontend container still has OLD assets from image/volume
5. `assets.json` points to NEW hashes, CSS files have OLD hashes

### Official Frappe Policy

From [Frappe Docker FAQ](https://github.com/frappe/frappe_docker/wiki/Frequently-Asked-Questions):
> "You cannot build assets using `bench build` in running production containers. It will mess up the attached assets volume."

### The Fix: Delete Assets Before Deploy

**ALWAYS delete the assets volume before deployment:**

```bash
# Add to GitHub Actions BEFORE docker compose up
docker compose -f pwd.yml -f volumes-override.yml down
docker volume rm bebang-hrms_assets 2>/dev/null || true
docker compose -f pwd.yml -f volumes-override.yml up -d
```

**Or via SSM:**
```bash
aws ssm send-command \
  --instance-ids "i-026b7477d27bd46d6" \
  --document-name "AWS-RunShellScript" \
  --parameters 'commands=["cd /home/ubuntu/frappe_docker && docker compose -f pwd.yml -f volumes-override.yml down && docker volume rm bebang-hrms_assets 2>/dev/null || true && docker compose -f pwd.yml -f volumes-override.yml up -d"]'
```

### Permanent Fix: Docker Swarm - NOW ACTIVE ✅

Docker Swarm was deployed on 2026-01-29. It automatically recreates containers on deployment:

```bash
# Swarm is already initialized and running
docker service ls  # View all 9 services

# Deploy updates via rolling updates (zero downtime)
docker service update --image samkarazi/bebang-erpnext-hrms:v15-newtag frappe_backend
```

**Why Swarm works:** Rolling updates recreate containers with fresh assets, eliminating stale CSS/JS issues.

### Volume Safety Reference

| Volume | Contains | Safe to Delete? |
|--------|----------|-----------------|
| `bebang-hrms_sites` | Site configs, uploads | **NO** - Data loss |
| `bebang-hrms_db-data` | MariaDB database | **NO** - Data loss |
| `bebang-hrms_logs` | Log files | **YES** - Just logs |
| `bebang-hrms_assets` | Compiled CSS/JS | **YES** - Regenerated from image |

**Your DocTypes, employees, APIs - all safe.** Only compiled CSS/JS is deleted and recreated.

### EMERGENCY FIX: CSS 404 (If It Happens Again)

**Fastest fix (30 seconds):**
```bash
export AWS_ACCESS_KEY_ID=$(doppler secrets get AWS_ACCESS_KEY_ID --project bei-erp --config dev --plain)
export AWS_SECRET_ACCESS_KEY=$(doppler secrets get AWS_SECRET_ACCESS_KEY --project bei-erp --config dev --plain)
export AWS_DEFAULT_REGION=ap-southeast-1

# 1. Force redeploy all services (recreates containers with fresh assets)
aws ssm send-command --instance-ids "i-026b7477d27bd46d6" --document-name "AWS-RunShellScript" \
  --parameters 'commands=[
    "docker service update --force frappe_backend",
    "docker service update --force frappe_frontend"
  ]'

# 2. Wait 60 seconds for services to converge

# 3. Flush Redis (CRITICAL - clears cached HTML with old hashes)
aws ssm send-command --instance-ids "i-026b7477d27bd46d6" --document-name "AWS-RunShellScript" \
  --parameters 'commands=[
    "docker exec $(docker ps -qf name=frappe_redis-cache) redis-cli FLUSHALL",
    "docker exec $(docker ps -qf name=frappe_redis-queue) redis-cli FLUSHALL"
  ]'
```

**Why this works:** The CSS 404 happens when:
1. `assets.json` has hash A (from cache/migrate)
2. Actual CSS files have hash B (from Docker image)
3. Redis caches HTML referencing hash A
4. Force redeploy syncs assets.json to hash B
5. Redis flush clears cached HTML, forcing fresh generation with hash B

### How to Diagnose CSS 404

```bash
# 1. Check what HTML is requesting
curl -s https://hq.bebang.ph/ | grep -oP "website\.bundle\.[A-Z0-9]+\.css"

# 2. Check what CSS files actually exist (Swarm)
aws ssm send-command --instance-ids "i-026b7477d27bd46d6" --document-name "AWS-RunShellScript" \
  --parameters 'commands=["docker exec $(docker ps -qf name=frappe_frontend) ls /home/frappe/frappe-bench/sites/assets/frappe/dist/css/ | grep website"]'

# 3. Check what assets.json says
aws ssm send-command --instance-ids "i-026b7477d27bd46d6" --document-name "AWS-RunShellScript" \
  --parameters 'commands=["docker exec $(docker ps -qf name=frappe_backend) cat /home/frappe/frappe-bench/sites/assets/assets.json | grep website.bundle.css"]'

# 4. If hashes don't match → Force redeploy + Redis flush (see above)
```

### Research Reference

Full research report: `docs/reports/FRAPPE_DOCKER_DEPLOYMENT_RESEARCH_2026-01-28.md`

Sources:
- [GitHub Issue #790](https://github.com/frappe/frappe_docker/issues/790)
- [Frappe Docker FAQ](https://github.com/frappe/frappe_docker/wiki/Frequently-Asked-Questions)
- [Community Discussion](https://discuss.frappe.io/t/best-way-to-deploy-new-versions-of-custom-app-in-self-hosted-docker-setup/96317)

## Server Discovery Commands

If you're unsure about server configuration, run these:

```bash
# List home directory to find frappe location
aws ssm send-command --instance-ids "i-026b7477d27bd46d6" --document-name "AWS-RunShellScript" \
  --parameters 'commands=["ls -la /home/ubuntu/"]' --output text --query 'Command.CommandId'

# List docker volumes
aws ssm send-command --instance-ids "i-026b7477d27bd46d6" --document-name "AWS-RunShellScript" \
  --parameters 'commands=["docker volume ls | grep -E bebang|frappe|sites"]' --output text --query 'Command.CommandId'

# List running containers
aws ssm send-command --instance-ids "i-026b7477d27bd46d6" --document-name "AWS-RunShellScript" \
  --parameters 'commands=["docker ps --format \"{{.Names}} {{.Image}}\""]' --output text --query 'Command.CommandId'

# Check what's using a port
aws ssm send-command --instance-ids "i-026b7477d27bd46d6" --document-name "AWS-RunShellScript" \
  --parameters 'commands=["lsof -i :8080 || ss -tlnp | grep 8080"]' --output text --query 'Command.CommandId'

# Get command output
aws ssm get-command-invocation --command-id "<COMMAND_ID>" --instance-id "i-026b7477d27bd46d6" \
  --query '[Status, StandardOutputContent]' --output text
```

## Files Reference

| File | Purpose |
|------|---------|
| `.github/helper/apps.json` | Apps included in Docker image |
| `.github/workflows/build-and-deploy.yml` | CI/CD workflow |
| `hrms/api/__init__.py` | API function exports |
| `hrms/api/*.py` | API endpoint files |

## Related Skills

- `/local-frappe` - **Test locally first** before production deployment
- `/frappe-sql-bulk` - For data imports (no rebuild needed)
- `/frappe-external-app` - For React apps via API
