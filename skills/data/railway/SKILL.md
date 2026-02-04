---
name: railway
description: Deploys applications on Railway with zero-config detection, databases, and automatic CI/CD. Use when deploying Node.js apps, setting up databases, or needing simple PaaS deployment.
---

# Railway

Modern deployment platform with zero-config builds, instant databases, and automatic CI/CD.

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

# Get deployment URL
railway domain
```

## Deployment Methods

### From GitHub

1. Connect GitHub account at railway.app
2. Select repository
3. Railway auto-detects framework
4. Automatic deploys on push

### From CLI

```bash
# Link to existing project
railway link

# Deploy current directory
railway up

# Deploy with logs
railway up --detach
```

### From Template

Use Railway's template gallery for pre-configured stacks.

## Project Configuration

### railway.json

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS",
    "buildCommand": "npm run build"
  },
  "deploy": {
    "startCommand": "npm start",
    "healthcheckPath": "/health",
    "healthcheckTimeout": 300,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 3
  }
}
```

### Environment Detection

Railway automatically detects:
- **Node.js** - package.json
- **Python** - requirements.txt, Pipfile
- **Go** - go.mod
- **Ruby** - Gemfile
- **Rust** - Cargo.toml
- **Docker** - Dockerfile

## Environment Variables

### CLI

```bash
# Set variable
railway variables set API_KEY=secret

# Set multiple
railway variables set API_KEY=secret DB_URL=postgres://...

# List variables
railway variables

# Delete variable
railway variables delete API_KEY
```

### Dashboard

1. Select service
2. Variables tab
3. Add key-value pairs
4. Redeploy for changes

### Reference Variables

```bash
# Reference other services
DATABASE_URL=${{Postgres.DATABASE_URL}}
REDIS_URL=${{Redis.REDIS_URL}}
```

## Databases

### Provision Database

```bash
# Add PostgreSQL
railway add postgresql

# Add MySQL
railway add mysql

# Add Redis
railway add redis

# Add MongoDB
railway add mongodb
```

### Connection Strings

Automatically available as environment variables:

| Service | Variable |
|---------|----------|
| PostgreSQL | `DATABASE_URL`, `PGHOST`, `PGPORT`, etc. |
| MySQL | `MYSQL_URL`, `MYSQLHOST`, etc. |
| Redis | `REDIS_URL`, `REDISHOST`, etc. |
| MongoDB | `MONGO_URL` |

### Database Management

```bash
# Connect to database shell
railway connect

# Run database migrations
railway run npm run migrate
```

## Node.js Deployment

### package.json

```json
{
  "scripts": {
    "build": "tsc",
    "start": "node dist/index.js"
  },
  "engines": {
    "node": "20"
  }
}
```

### Express/Fastify

```typescript
// Use PORT from environment
const port = process.env.PORT || 3000;
app.listen(port, '0.0.0.0', () => {
  console.log(`Server running on port ${port}`);
});
```

## Next.js Deployment

```json
{
  "scripts": {
    "build": "next build",
    "start": "next start -p $PORT"
  }
}
```

Railway automatically:
- Detects Next.js
- Runs build
- Starts with correct PORT

## Dockerfile Deployment

### Basic Dockerfile

```dockerfile
FROM node:20-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

EXPOSE 3000
CMD ["npm", "start"]
```

### Multi-stage Build

```dockerfile
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:20-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./
EXPOSE 3000
CMD ["node", "dist/index.js"]
```

## Custom Domains

### Add Domain

```bash
railway domain
# Returns: your-app.up.railway.app

# Or add custom domain in dashboard
# 1. Service settings > Domains
# 2. Add custom domain
# 3. Configure DNS (CNAME to railway.app)
```

### DNS Configuration

```
CNAME your-app.up.railway.app
```

## Scaling

### Horizontal Scaling

Configure in dashboard:
- Instance count
- Resource limits (CPU, RAM)

### Auto-scaling

Railway Pro plans support auto-scaling based on:
- CPU usage
- Memory usage
- Request count

## Healthchecks

### Configuration

```json
{
  "deploy": {
    "healthcheckPath": "/health",
    "healthcheckTimeout": 300
  }
}
```

### Endpoint

```typescript
app.get('/health', (req, res) => {
  res.status(200).json({ status: 'healthy' });
});
```

## Logs & Monitoring

### CLI

```bash
# Stream logs
railway logs

# Follow logs
railway logs -f

# Specific service
railway logs --service my-service
```

### Dashboard

Real-time logs, metrics, and deployment history in the Railway dashboard.

## Preview Environments

### Pull Request Previews

Enable in project settings:
1. Settings > Environments
2. Enable PR environments
3. Each PR gets isolated environment

### Environment Variables per Environment

```bash
# Production
railway variables set --environment production API_URL=https://api.example.com

# Staging
railway variables set --environment staging API_URL=https://staging-api.example.com
```

## CLI Commands

```bash
# Project management
railway init          # Initialize new project
railway link          # Link to existing project
railway unlink        # Unlink project

# Deployment
railway up            # Deploy current directory
railway up --detach   # Deploy without logs

# Variables
railway variables     # List variables
railway variables set KEY=value

# Database
railway add postgresql  # Add database
railway connect        # Connect to database

# Logs & shell
railway logs          # View logs
railway run <cmd>     # Run command in Railway env
railway shell         # Interactive shell

# Domains
railway domain        # Get/create domain
```

## Monorepo Support

### Root Configuration

```json
{
  "build": {
    "rootDirectory": "apps/api"
  }
}
```

### Multiple Services

Deploy each app as separate Railway service, all in same project.

See [references/configuration.md](references/configuration.md) for complete configuration options.
