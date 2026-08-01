---
name: railway-deploy-demolinator-talal-s-tda
description: Automated Railway deployment and configuration management. Handles environment
  variables, service deployment, health checks, and rollback procedures.
---

# Railway Deploy Skill

## Description
Automated Railway deployment and configuration management. Handles environment variables, service deployment, health checks, and rollback procedures.

## Capabilities
- Set/update environment variables
- Trigger redeployments
- Check deployment status
- View deployment logs
- Verify service health
- Rollback to previous deployments
- Manage multiple services (backend, auth server, database)

## Inputs
- `--service` (required): Service to deploy (backend|auth-server|all)
- `--action` (required): Action to perform (deploy|config|status|rollback)
- `--env-vars` (optional): Environment variables to set (KEY=VALUE format, comma-separated)
- `--wait` (optional): Wait for deployment to complete (default: true)
- `--health-check` (optional): Run health checks after deployment (default: true)

## Process

### Action: config (Set Environment Variables)
```
1. Parse environment variables from --env-vars
2. For each KEY=VALUE pair:
   a. Validate variable name (no spaces, valid characters)
   b. Set in Railway using CLI or API
   c. Confirm variable is set
3. Optionally trigger redeploy (--redeploy flag)
```

### Action: deploy (Deploy Service)
```
1. Check current deployment status
2. Trigger new deployment:
   a. Push latest code to GitHub (if needed)
   b. Railway auto-deploys or use `railway up`
3. Monitor deployment progress:
   a. Check build logs
   b. Wait for "Deployed" status
   c. Capture any build errors
4. Run health checks:
   a. GET {service_url}/health
   b. Verify 200 OK response
   c. Check response time
5. Verify service functionality:
   a. Backend: Test /api/health endpoint
   b. Auth Server: Test /health endpoint
   c. Check database connectivity
```

### Action: status (Check Deployment Status)
```
1. Get latest deployment info:
   a. Deployment ID
   b. Status (Building, Deployed, Failed)
   c. Commit hash
   d. Deployed timestamp
2. Get service metrics:
   a. CPU usage
   b. Memory usage
   c. Request count
3. Check service health:
   a. Uptime
   b. Recent errors
   c. Response times
```

### Action: rollback (Rollback Deployment)
```
1. List recent deployments (last 10)
2. Select previous stable deployment
3. Redeploy that version
4. Wait for rollback to complete
5. Run health checks
6. Verify service is working
```

## Railway Project Configuration

### Project Details
```yaml
Project ID: 1a580b9d-e43b-4faf-a523-b3454b9d3bf1
Services:
  - Backend (FastAPI):
      ID: ac8b8441-def7-49e9-af64-47dd171ae1c2
      URL: https://tda-backend-production.up.railway.app
      Required Env Vars:
        - AUTH_SERVER_URL
        - DATABASE_URL
        - CORS_ORIGINS

  - Auth Server (Better Auth):
      ID: (auth server service ID)
      URL: https://auth-server-production-8251.up.railway.app
      Required Env Vars:
        - DATABASE_URL
        - BETTER_AUTH_SECRET
        - CORS_ORIGINS
```

## Output Format

### Config Success
```json
{
  "action": "config",
  "service": "backend",
  "variables_set": [
    "AUTH_SERVER_URL=https://auth-server-production-8251.up.railway.app"
  ],
  "redeployment_triggered": true,
  "status": "SUCCESS"
}
```

### Deploy Success
```json
{
  "action": "deploy",
  "service": "backend",
  "deployment_id": "abc123",
  "status": "DEPLOYED",
  "build_time": "2m 15s",
  "health_check": "PASS",
  "url": "https://tda-backend-production.up.railway.app"
}
```

### Deploy Failure
```json
{
  "action": "deploy",
  "service": "backend",
  "status": "FAILED",
  "error": "Build failed: Module not found",
  "logs": "...",
  "rollback_recommended": true
}
```

## Example Usage

### Set Environment Variable
```bash
claude-code /railway-deploy --service backend --action config --env-vars "AUTH_SERVER_URL=https://auth-server-production-8251.up.railway.app"
```

### Deploy Backend
```bash
claude-code /railway-deploy --service backend --action deploy --wait true --health-check true
```

### Deploy All Services
```bash
claude-code /railway-deploy --service all --action deploy
```

### Check Status
```bash
claude-code /railway-deploy --service backend --action status
```

### Rollback
```bash
claude-code /railway-deploy --service backend --action rollback
```

### Set Multiple Variables and Deploy
```bash
claude-code /railway-deploy --service backend --action config --env-vars "AUTH_SERVER_URL=https://auth.railway.app,CORS_ORIGINS=https://frontend.vercel.app" --redeploy
```

## Environment Variables Management

### Critical Backend Variables
```bash
# Auth Server URL (REQUIRED)
AUTH_SERVER_URL=https://auth-server-production-8251.up.railway.app

# Database (auto-set by Railway)
DATABASE_URL=postgresql://...

# CORS Origins
CORS_ORIGINS=https://frontend-peach-xi-69.vercel.app,http://localhost:3000
```

### Critical Auth Server Variables
```bash
# Database (auto-set by Railway)
DATABASE_URL=postgresql://...

# Better Auth Secret (REQUIRED)
BETTER_AUTH_SECRET=<random-secret>

# CORS Origins
CORS_ORIGINS=https://frontend-peach-xi-69.vercel.app,https://tda-backend-production.up.railway.app
```

## Health Check Verification

### Backend Health Check
```bash
curl https://tda-backend-production.up.railway.app/health
# Expected: {"status":"healthy"}
```

### Auth Server Health Check
```bash
curl https://auth-server-production-8251.up.railway.app/health
# Expected: {"status":"healthy"}
```

### Database Connectivity
```bash
# Check backend logs for:
✅ Using database: postgresql://...
✅ Database connection pool initialized
```

## Common Issues & Solutions

### Issue: Deployment Stuck in "Building"
**Cause**: Build hanging, dependency issues
**Solution**:
```bash
claude-code /railway-deploy --service backend --action rollback
# Then check logs to identify build issue
```

### Issue: Service Healthy but Not Responding
**Cause**: Port configuration, firewall rules
**Solution**: Check Railway service settings, ensure PORT is set correctly

### Issue: Environment Variable Not Applied
**Cause**: Typo in variable name, redeployment needed
**Solution**:
```bash
# Re-set variable
claude-code /railway-deploy --service backend --action config --env-vars "VAR_NAME=value" --redeploy
```

### Issue: Database Connection Timeout
**Cause**: DATABASE_URL incorrect, network issues
**Solution**: Verify DATABASE_URL in Railway, check Neon database status

## Deployment Best Practices

### 1. Pre-Deployment Checklist
- ✅ All tests passing locally
- ✅ Dependencies updated
- ✅ Environment variables documented
- ✅ Database migrations ready

### 2. Deployment Steps
```bash
# 1. Deploy backend first
claude-code /railway-deploy --service backend --action deploy

# 2. Deploy auth server
claude-code /railway-deploy --service auth-server --action deploy

# 3. Run health checks
claude-code /railway-deploy --service all --action status

# 4. Test authentication flow
claude-code /browser-test-auth --url https://frontend-peach-xi-69.vercel.app
```

### 3. Post-Deployment Verification
- ✅ All services show "Deployed" status
- ✅ Health checks return 200 OK
- ✅ Authentication test passes
- ✅ No errors in logs

### 4. Rollback Procedure
```bash
# If deployment fails:
claude-code /railway-deploy --service backend --action rollback
claude-code /railway-deploy --service backend --action status
# Verify service is working
```

## Integration with CI/CD

### GitHub Actions Workflow
```yaml
name: Deploy to Railway

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Set Railway Environment Variables
        run: |
          claude-code /railway-deploy \
            --service backend \
            --action config \
            --env-vars "AUTH_SERVER_URL=${{ secrets.AUTH_SERVER_URL }}"

      - name: Deploy Backend
        run: |
          claude-code /railway-deploy \
            --service backend \
            --action deploy \
            --wait true

      - name: Health Check
        run: |
          claude-code /railway-deploy \
            --service backend \
            --action status

      - name: Test Authentication
        run: |
          claude-code /browser-test-auth \
            --url https://frontend-peach-xi-69.vercel.app
```

## Dependencies
- Railway CLI installed and authenticated
- Railway project ID and service IDs configured
- Git repository connected to Railway
- Required environment variables documented

## Success Criteria
- ✅ Deployment completes without errors
- ✅ Service shows "Deployed" status in Railway
- ✅ Health check returns 200 OK
- ✅ All environment variables set correctly
- ✅ Service responds to requests within acceptable time

## Maintenance Notes
- Keep Railway CLI updated: `railway update`
- Document all environment variable changes
- Maintain rollback history (last 10 deployments)
- Monitor deployment times and optimize build process
- Archive deployment logs for troubleshooting
