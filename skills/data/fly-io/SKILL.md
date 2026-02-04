---
name: fly-io
description: Deploys applications globally on Fly.io edge infrastructure with Firecracker VMs, multi-region deployment, and usage-based pricing. Use when deploying to multiple regions, running containers at the edge, or needing fast cold starts.
---

# Fly.io

Global edge deployment platform running applications in Firecracker micro-VMs close to users.

## Quick Start

```bash
# Install flyctl
curl -L https://fly.io/install.sh | sh

# Or on macOS
brew install flyctl

# Login
fly auth login

# Launch app (creates fly.toml)
fly launch

# Deploy
fly deploy
```

## Project Setup

### fly.toml

```toml
app = "my-app"
primary_region = "ord"

[build]
  dockerfile = "Dockerfile"

[http_service]
  internal_port = 3000
  force_https = true
  auto_stop_machines = true
  auto_start_machines = true
  min_machines_running = 1

  [http_service.concurrency]
    type = "requests"
    hard_limit = 250
    soft_limit = 200

[[vm]]
  cpu_kind = "shared"
  cpus = 1
  memory_mb = 256
```

### Basic Dockerfile

```dockerfile
FROM node:20-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

EXPOSE 3000

CMD ["node", "dist/index.js"]
```

## Deployment

### Deploy from Git

```bash
# First deploy creates app
fly launch

# Subsequent deploys
fly deploy

# Deploy specific Dockerfile
fly deploy --dockerfile Dockerfile.prod

# Deploy with build args
fly deploy --build-arg API_KEY=$API_KEY
```

### Deploy Strategies

```toml
[deploy]
  strategy = "rolling"  # default
  # strategy = "immediate"
  # strategy = "canary"
  # strategy = "bluegreen"
```

## Regions

### Multi-Region Deployment

```bash
# Add regions
fly regions add ams lhr syd

# List regions
fly regions list

# Remove region
fly regions remove syd
```

### Region Configuration

```toml
app = "my-app"
primary_region = "ord"

# Scale to multiple regions
[[vm]]
  memory = "256mb"
  cpu_kind = "shared"
  cpus = 1

  [vm.processes]
    web = 2  # 2 machines per region
```

### Available Regions

| Code | Location |
|------|----------|
| `ord` | Chicago |
| `iad` | Virginia |
| `lax` | Los Angeles |
| `ams` | Amsterdam |
| `lhr` | London |
| `fra` | Frankfurt |
| `syd` | Sydney |
| `nrt` | Tokyo |
| `sin` | Singapore |

## Secrets & Environment

### Secrets (Encrypted)

```bash
# Set secrets
fly secrets set DATABASE_URL=postgres://... API_KEY=secret

# List secrets
fly secrets list

# Unset secret
fly secrets unset API_KEY
```

### Environment Variables

```toml
# fly.toml
[env]
  NODE_ENV = "production"
  LOG_LEVEL = "info"
```

### Per-Region Environment

```toml
[[env]]
  NODE_ENV = "production"

  [[env.region]]
    region = "ord"
    CDN_URL = "https://us-cdn.example.com"

  [[env.region]]
    region = "ams"
    CDN_URL = "https://eu-cdn.example.com"
```

## Scaling

### Machine Scaling

```bash
# Scale up
fly scale count 3

# Scale per region
fly scale count 2 --region ord
fly scale count 1 --region ams

# Scale VM size
fly scale vm shared-cpu-1x
fly scale vm dedicated-cpu-1x
fly scale memory 512
```

### Auto-scaling

```toml
[http_service]
  auto_stop_machines = true
  auto_start_machines = true
  min_machines_running = 1
  max_machines_running = 10

  [http_service.concurrency]
    type = "requests"
    soft_limit = 100
    hard_limit = 250
```

## Databases

### Postgres

```bash
# Create Postgres cluster
fly postgres create

# Attach to app
fly postgres attach my-postgres-db

# Connect
fly postgres connect -a my-postgres-db

# Proxy to local
fly proxy 5432 -a my-postgres-db
```

### Redis

```bash
# Create Redis
fly redis create

# Get connection string
fly redis status my-redis
```

### LiteFS (SQLite)

```bash
# Create LiteFS cluster
fly apps create my-app-litefs

# Configure in fly.toml
[mounts]
  source = "litefs"
  destination = "/var/lib/litefs"
```

## Volumes (Persistent Storage)

```bash
# Create volume
fly volumes create mydata --size 1 --region ord

# List volumes
fly volumes list

# Destroy volume
fly volumes destroy vol_xxx
```

```toml
# fly.toml
[mounts]
  source = "mydata"
  destination = "/data"
```

## Networking

### Custom Domains

```bash
# Add domain
fly certs add example.com

# Check certificate status
fly certs show example.com
```

### Private Networking

```toml
# Internal services communicate via .internal DNS
# api.internal:3000
```

### Static IPs

```bash
# Allocate IPv4 (paid)
fly ips allocate-v4

# List IPs
fly ips list
```

## Health Checks

```toml
[http_service]
  internal_port = 3000

  [[http_service.checks]]
    grace_period = "5s"
    interval = "10s"
    timeout = "2s"
    path = "/health"
    method = "GET"
    protocol = "http"
```

## Processes

### Multiple Processes

```toml
[processes]
  web = "node dist/server.js"
  worker = "node dist/worker.js"

[[http_service]]
  processes = ["web"]
  internal_port = 3000

[[services]]
  processes = ["worker"]
  internal_port = 0
```

### Background Workers

```toml
[processes]
  worker = "node dist/worker.js"

[[services]]
  processes = ["worker"]
  internal_port = 0
  auto_stop_machines = false
```

## Node.js Configuration

### Optimized Dockerfile

```dockerfile
FROM node:20-alpine AS builder

WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build
RUN npm prune --production

FROM node:20-alpine

WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./

ENV NODE_ENV=production
USER node

CMD ["node", "dist/index.js"]
```

### Next.js

```toml
app = "my-nextjs-app"
primary_region = "ord"

[build]
  dockerfile = "Dockerfile"

[http_service]
  internal_port = 3000
  force_https = true
  auto_stop_machines = true
  auto_start_machines = true

[[vm]]
  memory = "512mb"
  cpu_kind = "shared"
  cpus = 1
```

## CLI Commands

```bash
# App management
fly apps create my-app
fly apps list
fly apps destroy my-app

# Deployment
fly deploy
fly deploy --strategy immediate
fly status

# Logs
fly logs
fly logs -a my-app

# SSH
fly ssh console
fly ssh console -C "node -v"

# Monitoring
fly status
fly dashboard

# Scaling
fly scale show
fly scale count 3
fly scale memory 512

# Regions
fly regions list
fly regions add ord ams

# Secrets
fly secrets set KEY=value
fly secrets list
```

See [references/configuration.md](references/configuration.md) for complete fly.toml options.
