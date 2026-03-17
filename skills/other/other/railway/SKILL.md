---
name: railway
description: "Deploy and troubleshoot Railway projects via the `railway` CLI. This skill should be used when deploying code, checking deployment status, viewing build/deployment logs, diagnosing failed deployments, managing environment variables, or debugging Railway services. Triggers on: deploy to railway, railway logs, deployment failed, check railway status, railway troubleshoot."
---

# Railway

Deploy and troubleshoot Railway projects. Focused on diagnosing deployment failures and build issues.

## Troubleshooting Decision Tree

When a deployment fails or behaves unexpectedly, follow this sequence:

```
1. railway status --json     → Check deployment status (FAILED/SUCCESS/etc.)
2. railway logs --build      → Check build-phase errors
3. railway logs --deployment → Check runtime errors  
4. railway logs              → Stream live application logs
5. railway ssh               → Direct container access for debugging
6. railway open              → Dashboard fallback when CLI insufficient
```

## Quick Diagnostics

Check current project/service context:
```bash
railway status
```

Get detailed deployment state as JSON (includes status, config, volumes, domains):
```bash
railway status --json
```

Parse deployment status programmatically:
```bash
railway status --json | jq '.services.edges[0].node.serviceInstances.edges[0].node.latestDeployment.status'
```

## Viewing Logs

**Build logs** (compilation, dependency install, Dockerfile steps):
```bash
railway logs --build
```

**Deployment logs** (startup, runtime initialization):
```bash
railway logs --deployment
```

**Application logs** (live stream from running service):
```bash
railway logs
```

**JSON format** for parsing:
```bash
railway logs --json | jq -r '.message'
```

**Specific service** (when project has multiple services):
```bash
railway logs -s <service-name> --build
railway logs -s <service-name>
```

## Common Failure Patterns

### "No deployments found"
The deployment may have failed before logs were created. Check:
```bash
railway status --json | jq '.services.edges[].node.serviceInstances.edges[].node.latestDeployment'
```

### Build failures
```bash
# Check build logs
railway logs --build

# Common causes:
# - Missing dependencies in package.json/requirements.txt
# - Dockerfile errors
# - Build command failures
```

### Runtime crashes
```bash
# Check deployment logs for startup errors
railway logs --deployment

# Then check application logs
railway logs

# Common causes:
# - Missing environment variables
# - Port binding issues (use PORT env var)
# - Database connection failures
```

### Service not accessible
```bash
# Check domain configuration
railway status --json | jq '.services.edges[].node.serviceInstances.edges[].node.domains'

# Verify service is running
railway status --json | jq '.services.edges[].node.serviceInstances.edges[].node.latestDeployment.status'
```

## Deploying

Deploy current directory:
```bash
railway up
```

Deploy without streaming logs (CI/scripts):
```bash
railway up --detach
```

Deploy to specific service:
```bash
railway up -s <service-name>
```

Redeploy latest (after config change):
```bash
railway redeploy -y
```

Rollback (remove most recent deployment):
```bash
railway down
```

## Environment Variables

View all variables:
```bash
railway variables
```

View as JSON:
```bash
railway variables --json
```

Set a variable:
```bash
railway variables --set "KEY=value"
```

Set multiple without triggering redeploy:
```bash
railway variables --set "A=1" --set "B=2" --skip-deploys
railway redeploy -y  # Deploy once after all changes
```

## Direct Container Access

SSH into running service:
```bash
railway ssh
```

Connect to database shell:
```bash
railway connect           # Interactive selection
railway connect postgres  # Direct psql
railway connect redis     # Direct redis-cli
```

## Local Development

Run command with Railway environment variables:
```bash
railway run npm start
railway run python app.py
```

Open shell with Railway vars loaded:
```bash
railway shell
echo $DATABASE_URL  # Railway vars available
```

## Project Management

Link directory to project:
```bash
railway link
railway link <project-id>
```

Switch environment:
```bash
railway environment production
railway environment staging
```

Create new environment:
```bash
railway env new staging
```

Open dashboard in browser:
```bash
railway open
```

## Key JSON Paths

When parsing `railway status --json`:

| Path | Description |
|------|-------------|
| `.services.edges[].node.name` | Service names |
| `.services.edges[].node.serviceInstances.edges[].node.latestDeployment.status` | Deployment status |
| `.services.edges[].node.serviceInstances.edges[].node.latestDeployment.meta` | Build config, commands |
| `.services.edges[].node.serviceInstances.edges[].node.domains` | Domain configuration |
| `.volumes.edges[].node.volumeInstances.edges[].node` | Volume mounts, sizes |
| `.environments.edges[].node.name` | Environment names |

## Railway Environment Variables

These are automatically available in Railway deployments:

| Variable | Description |
|----------|-------------|
| `PORT` | Port to bind to |
| `RAILWAY_ENVIRONMENT` | Current environment name |
| `RAILWAY_SERVICE_NAME` | Service name |
| `RAILWAY_PUBLIC_DOMAIN` | Public domain URL |
| `RAILWAY_PRIVATE_DOMAIN` | Internal domain (service-to-service) |
| `DATABASE_URL` | Database connection string (if database provisioned) |
