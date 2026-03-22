---
name: railway-deploy
description: >-
  Manage Railway deployments using the CLI. Use when a user asks to deploy to
  Railway, check deployment status, manage Railway services, set environment
  variables on Railway, view Railway logs, link a Railway project, add a
  database on Railway, scale Railway services, manage Railway environments,
  rollback a Railway deployment, or run commands with Railway env vars.
  Covers the full deploy lifecycle from project setup to production monitoring.
license: Apache-2.0
compatibility: "Requires Railway CLI installed (npm i -g @railway/cli or brew install railway)"
metadata:
  author: terminal-skills
  version: "1.0.0"
  category: devops
  tags: ["railway", "deploy", "cloud", "hosting", "paas"]
---

# Railway Deploy

## Overview

Deploy, manage, and monitor applications on Railway using the CLI. Covers the full lifecycle: project setup, service configuration, environment variables, deployments, scaling, logs, and debugging.

## Instructions

### Task A: Project Setup & Linking

First verify the CLI is installed. If `railway` is not found, install it:

```bash
npm i -g @railway/cli   # or: brew install railway
```

Check if already linked to a project:

```bash
railway status
```

If not linked, either create a new project or link to an existing one:

```bash
railway init    # Create a new project
railway link    # Link to an existing project
```

After linking, confirm with `railway status` to verify project, service, and environment context.

For CI/CD or headless environments, use token auth:

```bash
RAILWAY_TOKEN=xxx railway up       # Project-scoped token
RAILWAY_API_TOKEN=xxx railway up   # Account-scoped token
```

### Task B: Deploy

```bash
# Deploy current directory and stream logs
railway up

# Deploy without waiting for logs
railway up --detach

# Target a specific service
railway up -s my-service

# Deploy to a specific environment
railway up -e staging
```

To remove the latest deployment:

```bash
railway down
```

To redeploy the latest deployment (same code, fresh build):

```bash
railway redeploy
```

To restart a service without rebuilding:

```bash
railway restart
```

### Task C: Manage Services & Resources

```bash
# Add a service interactively
railway add

# Add a database
railway add --database postgres   # also: mysql, redis, mongo

# Add a service from a GitHub repo
railway add --repo user/repo

# Switch linked service context
railway service

# Scale a service
railway scale

# Generate a Railway subdomain or add a custom domain
railway domain
railway domain example.com

# Manage persistent volumes
railway volume list
railway volume add
railway volume delete

# Delete the entire project
railway delete
```

### Task D: Environment Variables

```bash
# List all variables for current service/environment
railway variable list

# Set a variable
railway variable set DATABASE_URL=postgres://user:pass@host:5432/db

# Set multiple variables
railway variable set KEY1=value1 KEY2=value2

# Delete a variable
railway variable delete SECRET_KEY
```

### Task E: Environments

```bash
# Switch environment interactively
railway environment

# Create a new environment
railway environment new staging

# Delete an environment
railway environment delete dev

# Deploy to a specific environment
railway up -e production
```

### Task F: Logs & Debugging

```bash
# Stream live logs
railway logs

# View build logs
railway logs --build

# View last N lines
railway logs -n 100

# SSH into the running container
railway ssh

# Connect to a database shell (e.g., psql, mysql, redis-cli)
railway connect
```

### Task G: Local Development

```bash
# Run a command with Railway environment variables injected
railway run npm start
railway run python manage.py migrate

# Open an interactive shell with Railway env vars
railway shell
```

## Examples

### Example 1: Deploy a Node.js app from scratch

**User request:** "Deploy my Node.js app to Railway"

**Actions taken:**

```bash
$ railway login
> Opening browser for authentication...
> Logged in as andrey@example.com

$ railway init
> Created project "my-node-app" in workspace "Personal"

$ railway up
> Uploading 2.3 MB...
> Build started
> Installing dependencies...
> Build completed in 34s
> Deployment live at my-node-app.up.railway.app

$ railway domain
> Service domain: my-node-app.up.railway.app
```

### Example 2: Add a Postgres database and wire it up

**User request:** "Add a database to my Railway project and set it up"

**Actions taken:**

```bash
$ railway status
> Project: my-node-app
> Service: web
> Environment: production

$ railway add --database postgres
> Added PostgreSQL service to project

# The DATABASE_URL is automatically injected. Verify:
$ railway variable list
> DATABASE_URL=postgres://railway:abc123@host:5432/railway
> PGHOST=host
> PGPORT=5432
> ...

# Run migrations using Railway env vars
$ railway run npx prisma migrate deploy
> Applying migrations...
> 3 migrations applied successfully

$ railway redeploy
> Redeploying web service...
> Deployment live
```

### Example 3: Debug a failing deployment

**User request:** "My Railway deployment is crashing, help me debug it"

**Actions taken:**

```bash
$ railway status
> Project: my-api
> Service: web
> Environment: production

# Check build logs first
$ railway logs --build
> Step 4/8: RUN npm ci
> npm ERR! Could not resolve dependency: peer express@"^4.0.0"

# If build passes but runtime fails, check runtime logs
$ railway logs -n 50
> Error: connect ECONNREFUSED 127.0.0.1:5432

# Verify variables are set
$ railway variable list
> DATABASE_URL=postgres://...@localhost:5432/mydb  # BUG: using localhost

# Fix: point to the Railway-provided database host
$ railway variable set DATABASE_URL=postgres://user:pass@railway-db-host:5432/mydb

$ railway redeploy
> Redeploying...
> Deployment live
```

### Task H: Health Checks and Auto-Rollback

After deploying, verify the service is healthy before considering the deploy complete. If unhealthy, roll back to the previous deployment.

```bash
# Deploy and wait for completion
$ railway up --detach

# Health check loop — verify the service responds
HEALTH_URL="https://your-app.railway.app/api/health"
TIMEOUT=60
DEADLINE=$((SECONDS + TIMEOUT))
HEALTHY=false

while [ $SECONDS -lt $DEADLINE ]; do
  STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$HEALTH_URL" 2>/dev/null || echo "000")
  if [ "$STATUS" = "200" ]; then
    HEALTHY=true
    break
  fi
  echo "Waiting for healthy response... (status: $STATUS)"
  sleep 3
done

if [ "$HEALTHY" = true ]; then
  echo "✅ Deployment healthy!"
else
  echo "❌ Health check failed! Rolling back..."
  railway rollback
  echo "⏪ Rolled back to previous deployment"
fi
```

**Automated deploy script with health verification:**

```python
# deploy_railway.py — Deploy with health check and auto-rollback
import subprocess
import time
import httpx

def deploy_with_health_check(health_url, timeout=60):
    """Deploy to Railway, verify health, rollback on failure."""
    print("🚀 Deploying to Railway...")
    subprocess.run(["railway", "up", "--detach"], check=True)

    print(f"🏥 Health checking {health_url}...")
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            r = httpx.get(health_url, timeout=5)
            if r.status_code == 200:
                print("✅ Healthy!")
                return True
        except httpx.RequestError:
            pass
        time.sleep(3)

    print("❌ Unhealthy! Rolling back...")
    subprocess.run(["railway", "rollback"], check=True)
    print("⏪ Rolled back")
    return False
```

## Guidelines

- Always run `railway status` first to confirm project, service, and environment context before making changes.
- Use `railway up --detach` in CI/CD pipelines to avoid blocking on log output.
- Use `RAILWAY_TOKEN` for project-scoped CI/CD auth and `RAILWAY_API_TOKEN` for account-level operations.
- Use `-s service-name` and `-e environment-name` flags when managing multi-service projects to avoid acting on the wrong target.
- Use `railway run` to execute one-off commands (migrations, seeds) with production env vars without deploying.
- If a deployment fails, check build logs (`railway logs --build`) first, then runtime logs (`railway logs`).
- Use `railway connect` to get a database shell directly without needing connection strings locally.
- Add `--json` to any command for machine-readable output in scripts.
- Use `railway variable set` to update env vars, then `railway redeploy` to pick up the changes.
- Use `railway environment new` to create staging/preview environments that mirror production config.
- If `railway` command is not found, install via `npm i -g @railway/cli` or `brew install railway`.
- If `railway login` fails or times out, use `railway login --browserless` for headless/SSH environments.
