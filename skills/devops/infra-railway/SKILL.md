---
name: railway
description: Railway deployment and infrastructure management skill. This skill should be used when deploying applications to Railway, managing Railway services, checking deployment status, viewing logs, configuring environment variables, or troubleshooting Railway deployments.
---

# Railway Deployment Skill

This skill provides workflows and knowledge for deploying and managing applications on Railway.

## Overview

Railway is a modern cloud platform for deploying applications. This skill integrates with the Railway MCP tools to provide deployment, monitoring, and management capabilities.

## Prerequisites

Before using Railway MCP tools:

1. **Install Railway CLI:** https://docs.railway.com/guides/cli
2. **Authenticate:** Run `railway login` in terminal
3. **Link project:** Run `railway link` in the project directory

## Available MCP Tools

| Tool | Purpose |
|------|---------|
| `check-railway-status` | Verify CLI is installed and authenticated |
| `list-projects` | List all Railway projects for the account |
| `list-services` | List services in the linked project |
| `list-deployments` | List deployments with status and metadata |
| `list-variables` | Show environment variables for a service |
| `set-variables` | Set environment variables |
| `get-logs` | Get build or deployment logs |
| `deploy` | Upload and deploy from local directory |
| `generate-domain` | Generate a Railway domain for the service |
| `link-service` | Link to a specific Railway service |
| `link-environment` | Link to a specific Railway environment |
| `create-environment` | Create a new Railway environment |
| `create-project-and-link` | Create and link a new Railway project |
| `deploy-template` | Search and deploy Railway templates |

## Deployment Workflow

### First-Time Setup

1. **Verify CLI authentication:**
   ```
   Use check-railway-status to confirm Railway CLI is logged in
   ```

2. **Link project (if not linked):**
   - User runs `railway login` in terminal
   - User runs `railway link` in the project directory
   - Or use `create-project-and-link` for new projects

3. **Configure root directory** (for monorepos):
   - If app is in a subdirectory (e.g., `web/`, `app/`, `frontend/`), configure in Railway Dashboard:
   - Service → Settings → Source → Root Directory

### Deployment Process

1. **Check current status:**
   ```
   list-deployments with json=true to see recent deployment statuses
   ```

2. **If deployment failed, check logs:**
   ```
   get-logs with logType="build" and the failed deploymentId
   ```

3. **Common build failures:**
   - Missing root directory configuration (monorepos)
   - Syntax errors in code
   - Missing dependencies
   - Invalid environment variables

4. **Deploy changes:**
   - Push to GitHub (auto-deploy if connected)
   - Or use `deploy` tool for manual deployment

### Environment Variables

1. **View current variables:**
   ```
   list-variables with json=true
   ```

2. **Set new variables:**
   ```
   set-variables with variables array like ["KEY=value", "KEY2=value2"]
   ```

3. **Common patterns:**
   - `NEXT_PUBLIC_*` - Next.js client-safe public variables
   - `DATABASE_URL` - Database connection string
   - `*_API_KEY` - API keys (server-side only)

### Domain Configuration

1. **Generate Railway domain:**
   ```
   generate-domain to get a *.up.railway.app domain
   ```

2. **Custom domains:**
   - Configure in Railway Dashboard: Service → Settings → Public Networking
   - Add CNAME record at DNS provider pointing to Railway domain

## Framework-Specific Configuration

### Next.js

**railway.toml** (place in app root):
```toml
[build]
builder = "nixpacks"

[deploy]
startCommand = "npm run start"
healthcheckPath = "/"
healthcheckTimeout = 300
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 10
```

### Node.js/Express

**railway.toml:**
```toml
[build]
builder = "nixpacks"

[deploy]
startCommand = "node server.js"
healthcheckPath = "/health"
```

### Python/FastAPI

**railway.toml:**
```toml
[build]
builder = "nixpacks"

[deploy]
startCommand = "uvicorn main:app --host 0.0.0.0 --port $PORT"
healthcheckPath = "/health"
```

### Python/Django

**railway.toml:**
```toml
[build]
builder = "nixpacks"
buildCommand = "python manage.py collectstatic --noinput"

[deploy]
startCommand = "gunicorn myproject.wsgi --bind 0.0.0.0:$PORT"
healthcheckPath = "/health"
```

## Troubleshooting

### "Railpack could not determine how to build"

**Cause:** Root directory not set for monorepo structures.

**Fix:** Set Root Directory in Railway Dashboard → Service → Settings → Source.

### Build Syntax Errors

**Cause:** Code pushed with syntax errors.

**Fix:** 
1. Check build logs: `get-logs` with `logType="build"`
2. Fix the error locally
3. Push the fix to trigger new deployment

### Missing Environment Variables

**Cause:** Required environment variables not set.

**Fix:**
1. Check current vars: `list-variables`
2. Set missing vars: `set-variables`

### Domain Not Working

**Cause:** DNS not configured or not propagated.

**Fix:**
1. Verify CNAME record points to Railway domain
2. Wait for DNS propagation (up to 72 hours)
3. Check Railway Dashboard for verification status

### Port Configuration

Railway automatically provides a `PORT` environment variable. Ensure your application listens on `0.0.0.0:$PORT`.

**Node.js:**
```javascript
const port = process.env.PORT || 3000;
app.listen(port, '0.0.0.0', () => console.log(`Listening on ${port}`));
```

**Python:**
```python
import os
port = int(os.environ.get("PORT", 8000))
```

## Custom Domain Setup by Provider

### Cloudflare (Recommended)

1. Add CNAME record: `@` → Railway domain
2. Enable Cloudflare proxy (orange cloud)
3. Set SSL/TLS to "Full" (not Full Strict)
4. Enable Universal SSL

### GoDaddy / Providers Without CNAME Flattening

GoDaddy and some providers don't support CNAME flattening for root domains. Options:

1. **Use subdomain:** `www.domain.com` or `app.domain.com` with CNAME record
2. **Migrate DNS to Cloudflare:** Change nameservers in registrar
3. **Use forwarding:** Forward root to www subdomain

### Standard CNAME Setup

For subdomains on any provider:

1. In Railway: Add custom domain (e.g., `app.yourdomain.com`)
2. Copy the CNAME target (e.g., `abc123.up.railway.app`)
3. In DNS: Add CNAME record pointing subdomain to Railway target
4. Wait for verification in Railway Dashboard

## Project Configuration Template

After importing this skill, add project-specific details to your local skill copy:

```markdown
## Project Configuration

- **Project Name:** [Your Project]
- **Project ID:** [from Railway Dashboard]
- **Environment ID:** [from Railway Dashboard]
- **Service ID:** [from Railway Dashboard]
- **Root Directory:** [e.g., web/, app/, or /]
- **Custom Domain:** [if configured]
- **Dashboard URL:** https://railway.com/project/[project-id]

### Required Environment Variables

| Variable | Description |
|----------|-------------|
| ... | ... |
```
