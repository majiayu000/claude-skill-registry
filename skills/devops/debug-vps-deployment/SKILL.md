---
name: debug-vps-deployment
description: Deploys to archivist@194.163.189.144 VPS and iteratively debugs until successful. Use when deploying to VPS, debugging deployment failures, investigating container issues, checking health endpoints, or fixing OtterStack errors. Triggers on "deploy to vps", "debug deployment", or "fix container failure".
---

# Debug VPS Deployment

Deploy to the production VPS (archivist@194.163.189.144) and iteratively debug failures until successful deployment.

## Objective

This skill connects to the specific VPS, triggers OtterStack deployments, monitors output for failures, diagnoses root causes, applies fixes, and redeploys until the application is successfully running and healthy.

## VPS Connection Details

```bash
# SSH Connection
SSH_HOST="archivist@194.163.189.144"
SSH_USER="archivist"
OTTERSTACK_PATH="~/OtterStack/otterstack"

# Verify connection
ssh ${SSH_HOST} "echo 'Connection successful'"
```

## Quick Start Deployment

```bash
# 1. Verify OtterStack is available
ssh ${SSH_HOST} "${OTTERSTACK_PATH} --help"

# 2. Check project exists
ssh ${SSH_HOST} "${OTTERSTACK_PATH} status <project-name>"

# 3. Deploy with verbose output
ssh ${SSH_HOST} "${OTTERSTACK_PATH} deploy <project-name> -v"

# 4. If it succeeds, verify endpoints. If it fails, proceed to debugging.
```

## Deployment Workflow

### Stage 1: Pre-Flight Checks

Before deploying, verify the environment is ready:

```bash
# Check SSH access
ssh ${SSH_HOST} "echo 'SSH OK'"

# Check OtterStack installation
ssh ${SSH_HOST} "${OTTERSTACK_PATH} --version" || \
  ssh ${SSH_HOST} "ls -l ~/OtterStack/otterstack"

# List existing projects
ssh ${SSH_HOST} "${OTTERSTACK_PATH} project list"

# Check current deployment status
ssh ${SSH_HOST} "${OTTERSTACK_PATH} status <project-name>"
```

### Stage 2: Trigger Deployment

Deploy with verbose output to see all stages:

```bash
ssh ${SSH_HOST} "${OTTERSTACK_PATH} deploy <project-name> -v"
```

### Stage 3: Monitor Deployment Stages

Watch the output for these sequential stages:

1. **"Fetching latest changes..."** → Git operations (only for remote repos)
2. **"Validating compose file..."** → Syntax and env var validation
3. **"Pulling images..."** → Docker image downloads
4. **"Starting services..."** → Container creation and startup
5. **"Waiting for containers to be healthy..."** → Health check polling
6. **"Applying Traefik priority labels..."** → Traffic routing setup (if Traefik enabled)
7. **"Deployment successful!"** → All done

If any stage fails, proceed to the corresponding debugging section below.

## Failure Diagnosis Decision Tree

### Failure Type 1: "compose validation failed"

**Symptoms:**
- Error during "Validating compose file..." stage
- Message like: `variable MYVAR is not set`
- Or: `services.web.image is undefined`

**Diagnosis Commands:**
```bash
# View full validation output
ssh ${SSH_HOST} "cd ~/.otterstack/repos/<project> && docker compose config"

# Check which env vars are set
ssh ${SSH_HOST} "${OTTERSTACK_PATH} env list <project-name>"

# View the env file being used
ssh ${SSH_HOST} "cat ~/.otterstack/envfiles/<project-name>.env"
```

**Common Causes:**
1. **Missing environment variables** → Variable used in compose file but not set
2. **Invalid YAML syntax** → Parse errors in compose file
3. **Undefined service references** → Service/network/volume doesn't exist

**Fix:**
```bash
# Add missing environment variables
ssh ${SSH_HOST} "${OTTERSTACK_PATH} env set <project> VAR value"

# For invalid syntax: fix compose file locally, commit, push, redeploy

# Verify fix
ssh ${SSH_HOST} "${OTTERSTACK_PATH} deploy <project-name> -v"
```

### Failure Type 2: "failed to start services"

**Symptoms:**
- Error during "Starting services..." stage
- Containers exit immediately
- Message like: `container exited with code 1`

**Diagnosis Commands:**
```bash
# OtterStack automatically shows last 50 lines on failure
# For more context:
ssh ${SSH_HOST} "docker compose -p <project>-<sha> logs --tail=100"

# Check container status
ssh ${SSH_HOST} "docker ps -a --filter name=<project>"

# Inspect specific container
ssh ${SSH_HOST} "docker logs <container-name> --tail=50"
```

**Common Causes & Fixes:**

#### Missing Files
**Error**: `ENOENT: no such file or directory`

**Diagnosis**:
```bash
# Check if files exist in container
ssh ${SSH_HOST} "docker exec <container> ls -la /app"
```

**Fix**: Update Dockerfile COPY paths, commit, push, redeploy.

#### Permission Denied
**Error**: `EACCES: permission denied`

**Diagnosis**:
```bash
# Check file/directory ownership
ssh ${SSH_HOST} "docker exec <container> ls -la /app/data"
```

**Fix**: Update Dockerfile to set correct ownership:
```dockerfile
RUN mkdir -p /app/data && chown -R app:app /app/data
USER app
```

#### Native Module Errors (Node.js)
**Error**: `Error: Could not locate the bindings file`

**Fix**: Add rebuild step to Dockerfile:
```dockerfile
RUN npm rebuild better-sqlite3  # Or other native module
```

#### Migration Failures
**Error**: `no such table: sessions` or `relation does not exist`

**Diagnosis**:
```bash
# Check if migrations ran
ssh ${SSH_HOST} "docker logs <container> | grep -A5 'migration'"
```

**Fix**: Ensure migration files are copied to correct path in Dockerfile.

#### Database Connection Failures
**Error**: `connection refused` or `ECONNREFUSED`

**Diagnosis**:
```bash
# Check if database service is running
ssh ${SSH_HOST} "docker ps | grep database"

# Test connection from container
ssh ${SSH_HOST} "docker exec <container> curl database:5432"
```

**Fix**: Verify database service exists in compose file and is healthy.

### Failure Type 3: "health check failed"

**Symptoms:**
- Error during "Waiting for containers to be healthy..." stage
- Timeout after 5 minutes
- Message like: `container myapp-web-1 is unhealthy`

**Diagnosis Commands:**
```bash
# Check container status
ssh ${SSH_HOST} "docker ps --format 'table {{.Names}}\t{{.Status}}'"

# View recent logs
ssh ${SSH_HOST} "docker logs <container> --tail=50"

# Test health check manually
ssh ${SSH_HOST} "docker exec <container> curl -f http://127.0.0.1:8080/health"

# Check what health check is defined
ssh ${SSH_HOST} "docker inspect <container> | grep -A10 Healthcheck"
```

**Common Causes & Fixes:**

#### Wrong Endpoint
**Error**: Health check returns 404

**Diagnosis**: Check application logs for available routes

**Fix**: Update health check in compose file to correct endpoint:
```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://127.0.0.1:8080/healthz"]  # Correct path
```

#### IPv6/IPv4 Mismatch
**Error**: `connection refused` when testing health check

**Diagnosis**:
```bash
# Check if localhost resolves to IPv6
ssh ${SSH_HOST} "docker exec <container> ping -c1 localhost"

# Test with explicit IPv4
ssh ${SSH_HOST} "docker exec <container> curl http://127.0.0.1:8080/health"
```

**Fix**: Use `127.0.0.1` instead of `localhost` in health check:
```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://127.0.0.1:8080/health"]
```

#### Slow Startup
**Error**: Timeout before app is actually ready

**Diagnosis**: Check how long app takes to start from logs

**Fix**: Increase `start_period` in health check:
```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://127.0.0.1:8080/health"]
  interval: 10s
  timeout: 3s
  retries: 3
  start_period: 60s  # Increased from 30s
```

#### Port Mismatch
**Error**: Connection refused on health check port

**Diagnosis**:
```bash
# Check what ports app is listening on
ssh ${SSH_HOST} "docker exec <container> netstat -tlnp"
```

**Fix**: Update health check to use correct port.

### Failure Type 4: "deployment lock already held"

**Symptoms:**
- Error before deployment starts
- Message: `Error: deployment in progress`

**Diagnosis:**
```bash
# Check lock file
ssh ${SSH_HOST} "cat ~/.otterstack/locks/<project>.lock"

# Extract PID and check if process is running
LOCK_PID=$(ssh ${SSH_HOST} "grep PID ~/.otterstack/locks/<project>.lock | cut -d: -f2")
ssh ${SSH_HOST} "ps -p ${LOCK_PID}"
```

**Fix:**
```bash
# If process is dead, remove stale lock
ssh ${SSH_HOST} "rm ~/.otterstack/locks/<project>.lock"

# If process is alive, wait for it to finish
# Or check logs: tail -f ~/.otterstack/logs/<project>.log
```

### Failure Type 5: Traefik routing issues

**Symptoms:**
- Deployment succeeds but endpoints return 404/502
- Traefik dashboard doesn't show new routes

**Diagnosis:**
```bash
# Check if containers are running
ssh ${SSH_HOST} "docker ps | grep <project>"

# Check Traefik routes
ssh ${SSH_HOST} "curl -s http://localhost:8080/api/http/routers | grep <project>"

# Check container labels
ssh ${SSH_HOST} "docker inspect <container> | grep -A20 Labels"

# Check container network
ssh ${SSH_HOST} "docker network inspect <network> | grep <container>"
```

**Common Causes:**
1. **Container not on Traefik network** → Add network to compose file
2. **No Traefik labels** → Ensure labels are defined
3. **Priority not applied** → Check OtterStack applied priority labels

**Fix**: Verify compose file has correct Traefik configuration.

## Iterative Fix-Deploy Loop

When deployment fails, follow this loop:

### Step 1: Capture Error
- Note exact error message from deployment output
- Identify which stage failed (validation, startup, health check)
- Save container logs if available

### Step 2: Diagnose Root Cause
- Use decision tree above to identify cause
- Run diagnostic commands to confirm hypothesis
- Compare with known issues in OtterStack TROUBLESHOOTING.md

### Step 3: Apply Fix

**If environment variable issue:**
```bash
ssh ${SSH_HOST} "${OTTERSTACK_PATH} env set <project> VAR value"
```

**If compose file issue:**
1. Fix locally in docker-compose.yml
2. Commit and push to git
3. Redeploy (OtterStack will pull latest)

**If application code issue:**
1. Fix code locally
2. Commit and push
3. Redeploy (image will be rebuilt)

**If Dockerfile issue:**
1. Fix Dockerfile locally
2. Commit and push
3. Redeploy (image will be rebuilt)

### Step 4: Redeploy and Verify
```bash
ssh ${SSH_HOST} "${OTTERSTACK_PATH} deploy <project-name> -v"
```

### Step 5: Repeat Until Successful
Continue the loop until deployment succeeds and all verifications pass.

## Real Example: Aperture Deployment

This is the actual sequence of iterations from the Aperture deployment:

### Iteration 1: Environment Variables Missing
**Error**:
```
WARN The "DATABASE_URL" variable is not set. Defaulting to a blank string
```

**Fix**:
```bash
ssh archivist@194.163.189.144 "~/OtterStack/otterstack env set aperture DATABASE_URL 'postgres://...'"
```

**Outcome**: Variables loaded, but next issue appeared.

### Iteration 2: Container Name Conflicts
**Error**:
```
The container name "/aperture-web" is already in use
```

**Fix**: Removed `container_name:` directives from docker-compose.yml locally, committed, pushed.

**Outcome**: Containers started, but new issue appeared.

### Iteration 3: Native Module Bindings
**Error**:
```
Error: Could not locate the bindings file. Tried: better_sqlite3.node
```

**Fix**: Added to Dockerfile:
```dockerfile
RUN npm rebuild better-sqlite3
```
Committed, pushed, redeployed.

**Outcome**: Bindings loaded, but new issue appeared.

### Iteration 4: Database Path Permissions
**Error**:
```
SqliteError: unable to open database file, code: 'SQLITE_CANTOPEN'
```

**Fix**: Added `DATABASE_PATH` environment variable pointing to `/app/data/db/aperture.db` and ensured directory ownership in Dockerfile.

**Outcome**: Database opened, but new issue appeared.

### Iteration 5: Missing Migrations
**Error**:
```
[DB] No migrations directory found, skipping migrations
Failed to start server: SqliteError: no such table: sessions
```

**Fix**: Updated Dockerfile to copy migrations to correct location:
```dockerfile
COPY src/migrations ./dist/migrations  # Was copying to ./src/migrations
```

**Outcome**: Migrations ran successfully, but new issue appeared.

### Iteration 6: Web Health Check Failure
**Error**:
```
container aperture-web-1 is unhealthy
```

**Diagnosis**: Health check used `localhost` which resolved to ::1 (IPv6), but nginx only listened on 0.0.0.0:80 (IPv4).

**Fix**: Changed health check to use `127.0.0.1` instead of `localhost` in docker-compose.yml.

**Outcome**: ✅ **SUCCESS! Deployment completed.**

### Final Status
```bash
# Check deployment
ssh archivist@194.163.189.144 "~/OtterStack/otterstack status aperture"
# Output: Status: active, SHA: e2d6223

# Verify endpoints
curl -I https://aperture-api.archivist.lol
# Output: HTTP/1.1 200 OK

curl -I https://aperture.archivist.lol
# Output: HTTP/1.1 200 OK
```

**Total iterations**: 6
**Time**: ~2 hours (including investigation time)
**Key lesson**: Each fix revealed the next issue - systematic debugging is essential.

## Success Verification

Once deployment completes without errors, verify success:

### 1. Check Deployment Status
```bash
ssh ${SSH_HOST} "${OTTERSTACK_PATH} status <project-name}"
```

**Expected output:**
```
Status: active
Commit: abc1234
Started: 2025-01-11 10:30:00
```

### 2. Check Container Health
```bash
ssh ${SSH_HOST} "docker ps --format 'table {{.Names}}\t{{.Status}}' | grep <project>"
```

**Expected output:**
```
project-abc1234-web-1      Up 2 minutes (healthy)
project-abc1234-worker-1   Up 2 minutes (healthy)
```

All containers should show `(healthy)` status.

### 3. Test Endpoints
```bash
# Test API endpoint
ssh ${SSH_HOST} "curl -I https://api.example.com/health"

# Or test from local machine
curl -I https://api.example.com/health
```

**Expected output:**
```
HTTP/1.1 200 OK
```

### 4. Check Application Logs
```bash
ssh ${SSH_HOST} "docker logs <container-name> --tail=20"
```

**Expected**: No errors, should see normal application startup and health check logs.

### 5. Verify Traefik Routing (if enabled)
```bash
ssh ${SSH_HOST} "curl -s http://localhost:8080/api/http/routers | grep <project>"
```

**Expected**: Router entries with correct domains and priorities.

## Troubleshooting Tips

### Container Keeps Restarting
```bash
# Check restart count
ssh ${SSH_HOST} "docker ps -a | grep <project>"

# View logs across restarts
ssh ${SSH_HOST} "docker logs <container> --tail=100"
```

**Common causes**: Crash on startup, missing dependencies, wrong command

### Old Containers Not Stopping
```bash
# List all project containers
ssh ${SSH_HOST} "docker ps -a | grep <project>"

# Manually stop old deployment
ssh ${SSH_HOST} "docker compose -p <old-project-name> down"
```

### Deployment Succeeds but App Doesn't Work
```bash
# Check container can reach internal services
ssh ${SSH_HOST} "docker exec <container> curl http://database:5432"

# Check environment variables in container
ssh ${SSH_HOST} "docker exec <container> env | grep DATABASE"

# Check file permissions
ssh ${SSH_HOST} "docker exec <container> ls -la /app"
```

### Git Pull Fails (Remote Repos)
```bash
# Check SSH keys
ssh ${SSH_HOST} "ssh -T git@github.com"

# Check network
ssh ${SSH_HOST} "ping -c3 github.com"

# Manually pull to see error
ssh ${SSH_HOST} "cd ~/.otterstack/repos/<project> && git pull"
```

## Emergency Rollback

If a deployment breaks production:

```bash
# Option 1: Deploy previous commit
ssh ${SSH_HOST} "${OTTERSTACK_PATH} deploy <project> --ref <previous-commit-sha>"

# Option 2: Manually switch back to old containers
# (Only if new containers still starting)
ssh ${SSH_HOST} "docker compose -p <old-project-name> up -d"
ssh ${SSH_HOST} "docker compose -p <new-project-name> down"
```

## Success Criteria

Deployment is successful when:

✅ **Deployment command completes without errors**
- "Deployment successful!" message appears
- No timeout or failure messages

✅ **All containers are healthy**
- `docker ps` shows all containers with `(healthy)` status
- No containers in restarting loop

✅ **Endpoints return expected responses**
- HTTP 200 from health endpoints
- Application responds correctly to test requests

✅ **No errors in logs**
- Recent logs show normal operation
- No crash traces or error messages

✅ **Traffic is being routed correctly** (if Traefik enabled)
- Public domain resolves to application
- Traefik shows active router with correct priority
