---
name: render
description: Deploys web applications on Render with automatic builds, managed databases, and zero-config SSL. Use when deploying web services, static sites, or setting up managed infrastructure.
---

# Render

Cloud platform for deploying web services, static sites, and databases with automatic builds from Git.

## Quick Start

1. Connect GitHub/GitLab at render.com
2. Create new Web Service
3. Select repository
4. Render auto-detects framework
5. Deploy

## Service Types

### Web Service

Long-running HTTP servers:

```yaml
# render.yaml
services:
  - type: web
    name: api
    runtime: node
    buildCommand: npm install && npm run build
    startCommand: npm start
    envVars:
      - key: NODE_ENV
        value: production
```

### Static Site

Frontend applications:

```yaml
services:
  - type: web
    name: frontend
    runtime: static
    buildCommand: npm install && npm run build
    staticPublishPath: ./dist
```

### Background Worker

Non-HTTP processes:

```yaml
services:
  - type: worker
    name: worker
    runtime: node
    buildCommand: npm install && npm run build
    startCommand: npm run worker
```

### Cron Job

Scheduled tasks:

```yaml
services:
  - type: cron
    name: daily-cleanup
    runtime: node
    buildCommand: npm install
    startCommand: npm run cleanup
    schedule: "0 0 * * *"
```

## Configuration

### render.yaml (Blueprint)

```yaml
# render.yaml
services:
  - type: web
    name: my-app
    runtime: node
    region: oregon

    # Build
    buildCommand: npm ci && npm run build
    startCommand: npm start

    # Environment
    envVars:
      - key: NODE_ENV
        value: production
      - key: DATABASE_URL
        fromDatabase:
          name: mydb
          property: connectionString

    # Health check
    healthCheckPath: /health

    # Scaling
    plan: starter
    numInstances: 1

    # Auto-deploy
    autoDeploy: true

    # Branch
    branch: main

databases:
  - name: mydb
    plan: starter
    databaseName: myapp
    user: myuser

envVarGroups:
  - name: shared-settings
    envVars:
      - key: LOG_LEVEL
        value: info
```

### Environment Variables

```yaml
envVars:
  # Static value
  - key: API_KEY
    value: my-secret-key

  # Sync from group
  - key: LOG_LEVEL
    fromGroup: shared-settings

  # From database
  - key: DATABASE_URL
    fromDatabase:
      name: mydb
      property: connectionString

  # From service
  - key: API_URL
    fromService:
      name: api
      type: web
      property: host
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
const port = process.env.PORT || 10000;

app.listen(port, '0.0.0.0', () => {
  console.log(`Server running on port ${port}`);
});
```

## Next.js Deployment

### Configuration

```yaml
services:
  - type: web
    name: nextjs-app
    runtime: node
    buildCommand: npm ci && npm run build
    startCommand: npm start
    envVars:
      - key: NODE_ENV
        value: production
```

Render auto-detects Next.js and configures appropriately.

## Static Site Deployment

### React/Vite

```yaml
services:
  - type: web
    name: react-app
    runtime: static
    buildCommand: npm ci && npm run build
    staticPublishPath: ./dist
    routes:
      - type: rewrite
        source: /*
        destination: /index.html
```

### Headers & Redirects

```yaml
services:
  - type: web
    name: static-site
    runtime: static
    staticPublishPath: ./dist
    headers:
      - path: /*
        name: X-Frame-Options
        value: DENY
    routes:
      - type: redirect
        source: /old-path
        destination: /new-path
        status: 301
```

## Databases

### PostgreSQL

```yaml
databases:
  - name: mydb
    plan: starter  # starter, standard, pro
    databaseName: myapp
    user: myuser
    region: oregon
```

### Redis

```yaml
services:
  - type: redis
    name: cache
    plan: starter
    maxmemoryPolicy: allkeys-lru
```

### Connection

```yaml
envVars:
  - key: DATABASE_URL
    fromDatabase:
      name: mydb
      property: connectionString

  - key: REDIS_URL
    fromService:
      name: cache
      type: redis
      property: connectionString
```

## Scaling

### Instance Types

| Plan | RAM | CPU |
|------|-----|-----|
| Free | 512 MB | Shared |
| Starter | 512 MB | 0.5 |
| Standard | 2 GB | 1 |
| Pro | 4 GB | 2 |
| Pro Plus | 8 GB | 4 |

### Horizontal Scaling

```yaml
services:
  - type: web
    name: api
    plan: standard
    numInstances: 3
```

### Auto-Scaling (Team plans)

Configure in dashboard:
- Min/max instances
- CPU/memory thresholds

## Custom Domains

1. Add domain in service settings
2. Configure DNS:

```
# A record
@ -> render IP

# CNAME for subdomain
www -> your-app.onrender.com
```

3. SSL certificate auto-provisioned

## Health Checks

```yaml
services:
  - type: web
    healthCheckPath: /health
```

```typescript
app.get('/health', (req, res) => {
  res.status(200).json({ status: 'ok' });
});
```

## Dockerfile Deployment

```yaml
services:
  - type: web
    name: docker-app
    runtime: docker
    dockerfilePath: ./Dockerfile
    dockerContext: .
```

```dockerfile
FROM node:20-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

EXPOSE 10000

CMD ["node", "dist/index.js"]
```

## Preview Environments

Enable in service settings:
1. Pull Request Previews: On
2. Each PR gets unique URL
3. Auto-deleted on merge

## Monorepo Support

### Root Directory

```yaml
services:
  - type: web
    name: api
    rootDir: apps/api
    buildCommand: npm ci && npm run build
    startCommand: npm start
```

### Multiple Services

```yaml
services:
  - type: web
    name: web
    rootDir: apps/web
    buildCommand: npm ci && npm run build
    staticPublishPath: ./dist

  - type: web
    name: api
    rootDir: apps/api
    buildCommand: npm ci && npm run build
    startCommand: npm start
```

## Persistent Disk

```yaml
services:
  - type: web
    name: app
    disk:
      name: data
      mountPath: /data
      sizeGB: 10
```

## Private Services

Internal services not exposed to internet:

```yaml
services:
  - type: pserv  # Private service
    name: internal-api
    runtime: node
    buildCommand: npm ci && npm run build
    startCommand: npm start
```

Access via internal DNS: `internal-api:10000`

## CLI (Render CLI)

```bash
# Install
npm install -g @render/cli

# Login
render login

# Deploy
render deploy

# Logs
render logs --service my-app

# SSH
render ssh my-app
```

See [references/configuration.md](references/configuration.md) for complete render.yaml options.
