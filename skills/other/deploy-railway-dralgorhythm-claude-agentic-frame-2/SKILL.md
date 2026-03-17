---
name: deploy-railway
description: Deploy applications to Railway. Use when deploying services, databases, or full-stack applications to Railway PaaS. Covers Railway CLI and configuration.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Deploy to Railway

## Why Railway?

- Zero config deployments
- Automatic HTTPS
- Built-in databases
- Environment management
- Preview environments

## Quick Start

```bash
# Install CLI
npm install -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Deploy
railway up
```

## Configuration

### railway.json
```json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "npm start",
    "healthcheckPath": "/health",
    "restartPolicyType": "ON_FAILURE"
  }
}
```

### Environment Variables
```bash
# Set variable
railway variables set DATABASE_URL=postgres://...

# Set from file
railway variables set < .env.production
```

## Database Setup

```bash
# Add PostgreSQL
railway add --database postgres

# Get connection URL
railway variables get DATABASE_URL
```

## Deployment Workflow

### 1. Connect Repo
```bash
railway link
```

### 2. Configure Build
Railway auto-detects most frameworks. Override with:
```bash
# Nixpacks (default)
railway up

# Dockerfile
railway up --dockerfile
```

### 3. Set Domain
```bash
railway domain
```

## Best Practices

1. **Use Preview Environments**: Test PRs before merge
2. **Separate Databases**: Different DB per environment
3. **Use Variables**: Never hardcode secrets
4. **Health Checks**: Enable for reliability
5. **Logs**: Use `railway logs` for debugging

## Common Commands

```bash
# View logs
railway logs

# Open dashboard
railway open

# Run command in environment
railway run npm run migrate

# List services
railway status
```
