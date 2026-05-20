---
name: flyio
description: Deploy and scale full-stack applications globally on Fly.io platform
when-to-use: When deploying web applications, APIs, databases, or microservices that need global distribution and automatic scaling
version: "1.1"
source: https://fly.io/docs/
generated: 2026-01-21
updated: 2026-01-21
---

# Fly.io Platform Skill

## Overview

Fly.io is a platform for deploying full-stack applications and databases globally. It runs your apps on Machines (fast-launching VMs) close to your users and scales compute resources automatically based on demand.

## When to Use This Skill

Use Fly.io when you need to:
- Deploy web applications with global distribution
- Run Docker containers in production
- Scale applications automatically based on load
- Deploy databases (Postgres, Redis) close to users
- Run background jobs and workers
- Build multi-region applications with low latency

## Core Concepts

### Applications
An app on Fly.io can be anything from a simple frontend web app to a complex arrangement of processes and Machines all doing their own thing. Applications are defined using `fly.toml` configuration files.

### Machines
Firecracker micro-VMs that run your application code. Machines can:
- Start in milliseconds
- Scale to zero when idle (autostop/autostart)
- Run anywhere in Fly.io's global network
- Be sized from minimal (shared-cpu-1x) to performance-optimized

### Fly Launch
The primary deployment framework that manages the complete application lifecycle:
- Creates and configures applications
- Detects project types automatically
- Builds Docker images
- Provisions resources (IPs, volumes, databases)
- Deploys and scales applications

## Quick Start

### 1. Install flyctl

**macOS/Linux:**
```bash
curl -L https://fly.io/install.sh | sh
```

**Windows:**
```powershell
pwsh -Command "iwr https://fly.io/install.ps1 -useb | iex"
```

### 2. Sign up or log in

```bash
fly auth signup  # Create new account
fly auth login   # Existing account
```

### 3. Launch your application

```bash
cd your-app
fly launch
```

This will:
- Scan your project and detect the framework
- Create a `fly.toml` configuration file
- Build your application as a Docker image
- Deploy your app to Fly.io
- Allocate IP addresses (IPv6 dedicated, IPv4 shared)

### 4. Deploy updates

```bash
fly deploy
```

## Common Commands

### Application Management

```bash
# Launch new app (interactive)
fly launch

# Launch with custom options
fly launch --name my-app --region ord --no-deploy

# Deploy app updates
fly deploy

# Deploy without rebuilding
fly deploy --image registry.fly.io/my-app:latest

# Check app status
fly status

# View app information
fly info

# Open app in browser
fly open

# View logs
fly logs

# SSH into Machine
fly ssh console

# List all apps
fly apps list

# Destroy app
fly apps destroy my-app
```

### Machine Management

```bash
# List Machines
fly machines list

# Create Machine
fly machines run registry.fly.io/my-app:latest

# Stop Machine
fly machines stop <machine-id>

# Start Machine
fly machines start <machine-id>

# Destroy Machine
fly machines destroy <machine-id>
```

### Scaling

```bash
# Scale Machine count
fly scale count 3

# Scale to specific regions
fly scale count 2 --region ord --region iad

# Scale Machine resources
fly scale vm shared-cpu-2x --memory 2048

# Configure autoscaling
fly autoscale set min=1 max=10
```

### Secrets Management

```bash
# Set secret
fly secrets set DATABASE_URL=postgres://...

# List secrets (names only, not values)
fly secrets list

# Unset secret
fly secrets unset DATABASE_URL

# Import secrets from file
fly secrets import < .env.production
```

### Volumes (Persistent Storage)

```bash
# Create volume
fly volumes create data --size 10

# List volumes
fly volumes list

# Delete volume
fly volumes delete vol_abc123

# Extend volume size
fly volumes extend vol_abc123 --size 20
```

### Databases

```bash
# Create Postgres cluster
fly postgres create --name my-db

# Attach Postgres to app
fly postgres attach --app my-app my-db

# Create Redis instance
fly redis create --name my-redis

# Connect to Postgres
fly postgres connect --app my-db
```

## Configuration (fly.toml)

### Basic Structure

```toml
# App name
app = "my-app"

# Primary region
primary_region = "ord"

# Build configuration
[build]
  dockerfile = "Dockerfile"

# HTTP service
[[services]]
  protocol = "tcp"
  internal_port = 8080

  [[services.ports]]
    port = 80
    handlers = ["http"]

  [[services.ports]]
    port = 443
    handlers = ["tls", "http"]

# Machine VM size
[vm]
  size = "shared-cpu-1x"
  memory_mb = 256

# Auto stop/start
[auto_stop_machines]
  enabled = true
  min_machines_running = 0

[auto_start_machines]
  enabled = true
```

### Advanced Features

**Environment Variables:**
```toml
[env]
  PORT = "8080"
  NODE_ENV = "production"
```

**Process Groups:**
```toml
[processes]
  web = "node server.js"
  worker = "node worker.js"
```

**HTTP Service with Health Checks:**
```toml
[[services]]
  protocol = "tcp"
  internal_port = 8080

  [[services.http_checks]]
    interval = "10s"
    timeout = "2s"
    grace_period = "5s"
    method = "GET"
    path = "/health"

  [[services.tcp_checks]]
    interval = "15s"
    timeout = "2s"
    grace_period = "5s"
```

**Mounted Volumes:**
```toml
[mounts]
  source = "data"
  destination = "/data"
```

## Architecture & Deployment Blueprints

### 1. Resilient Applications with Multiple Machines

**Pattern**: Build high-availability apps using multiple Machines across regions

**Key Concepts**:
- Each Machine runs on a single physical host (no automatic failover)
- Service-based apps automatically get 2 Machines with autostop/autostart
- Apps with volumes get only 1 Machine (requires manual replication)
- Standby Machines for worker processes watch primary and start if it fails

**Configuration Example**:
```toml
[http_service]
  internal_port = 8080
  force_https = true
  auto_stop_machines = "stop"
  auto_start_machines = true
  min_machines_running = 0

  [http_service.concurrency]
    type = "requests"
    soft_limit = 200
```

**Scaling Commands**:
```bash
# Add redundancy with multiple Machines
fly scale count 2

# Multi-region deployment for geographic redundancy
fly scale count 20 --region ams,ewr,gig

# Create standby Machine for workers
fly machine clone <id> --standby-for <id>
fly machine run <image> --standby-for <machine-id>
```

**Cost Efficiency**:
- Stopped Machines charge only for rootfs storage (~$0.18/month for 1.2GB)
- No CPU or RAM charges when stopped
- Makes redundancy financially practical for side projects

**When to Use**:
- ✅ Production systems with paying users
- ✅ Customer-facing services requiring 99.9% uptime
- ✅ Regulated environments needing geographic availability
- ⚠️ Optional for staging/internal tools/side projects

### 2. Architecture Patterns

**Available Patterns from Fly.io Blueprints**:

#### N-Tier Architecture
- Multiple Machine resilience for high availability
- Session persistence strategies (sticky sessions)
- Shared Nothing architectural approaches

#### Multi-Region Database Patterns
- Deploy databases close to users
- Use fly-replay for write forwarding
- Read replicas in multiple regions

#### Networking & Connectivity
- Private application access via Flycast
- WireGuard VPN integration
- Cross-deployment bridging
- SSH server deployment for secure access

### 3. Scaling & Performance Blueprints

**Autoscaling Configuration**:
```toml
[http_service.concurrency]
  type = "requests"
  soft_limit = 200
  hard_limit = 250

[auto_stop_machines]
  enabled = true
  min_machines_running = 0

[auto_start_machines]
  enabled = true
```

**Machine Autoscaling**:
```bash
# Set autoscaling bounds
fly autoscale set min=2 max=10

# Configure concurrency limits
fly scale concurrency soft=200 hard=250

# Private app autostart/autostop
# (automatically configured for internal services)
```

**Volume Forking**:
- Fork volumes for rapid Machine initialization
- Faster cold starts with pre-populated data
- Useful for read-heavy workloads

### 4. Background Jobs & Automation

**Distributed Work Queue**:
```bash
# Deploy worker Machines
fly machines run <image> --env WORKER=true --region ord

# Use standby workers for redundancy
fly machine run <image> --env WORKER=true --standby-for <primary-id>
```

**Cron-Based Task Scheduling**:
```dockerfile
# Using Supercronic for cron execution
FROM alpine:latest
RUN apk add --no-cache supercronic
COPY crontab /etc/crontab
CMD ["supercronic", "/etc/crontab"]
```

**Infrastructure Automation**:
- Alternatives to Terraform for Fly.io infrastructure
- Programmatic Machine creation via fly-machines API
- Event-driven automation using webhooks

### 5. Developer Workflow Blueprints

**Zero-Downtime Deployments**:
```bash
# Default behavior with multiple Machines
fly deploy

# Rolling deployment with custom strategy
fly deploy --strategy rolling
```

**Application Rollback**:
```bash
# List recent releases
fly releases

# Rollback to previous version
fly releases rollback
```

**GitHub Preview Environments**:
```yaml
# .github/workflows/preview.yml
name: Deploy Preview
on: pull_request

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: superfly/flyctl-actions@1.3
        with:
          args: "deploy --app my-app-pr-${{ github.event.pull_request.number }}"
```

**Staging/Production Isolation**:
```bash
# Create separate apps for environments
fly launch --name myapp-staging --org staging
fly launch --name myapp-production --org production

# Deploy to specific environment
fly deploy --app myapp-staging
fly deploy --app myapp-production
```

**Per-User Development Environments**:
```bash
# Create ephemeral dev environment
fly machines run <image> --name dev-$USERNAME --region ord

# Destroy when done
fly machines destroy dev-$USERNAME
```

### 6. Deployment Patterns

#### Static Site (Node.js)

```dockerfile
FROM node:18-alpine as builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
```

#### API Server (Python FastAPI)

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
```

#### Multi-region Deployment

```bash
# Deploy to multiple regions
fly deploy --region ord,iad,lhr

# Or configure in fly.toml
```

```toml
[regions]
  ord = 2  # 2 Machines in Chicago
  iad = 2  # 2 Machines in Virginia
  lhr = 1  # 1 Machine in London
```

## Best Practices

### Performance

1. **Use health checks** - Configure HTTP/TCP checks for automatic recovery
2. **Enable autoscaling** - Set min/max Machine counts based on load
3. **Choose regions wisely** - Deploy close to users and dependencies
4. **Optimize Docker images** - Use multi-stage builds, minimal base images
5. **Use volumes sparingly** - Volumes add latency; use managed databases when possible

### Security

1. **Use secrets** - Never hardcode credentials in `fly.toml` or Dockerfile
2. **Enable HTTPS** - Fly.io provides free TLS certificates
3. **Private networking** - Use Fly.io private network (6PN) for inter-app communication
4. **Least privilege** - Deploy tokens and access controls appropriately
5. **Regular updates** - Keep base images and dependencies current

### Cost Optimization

1. **Autostop/autostart** - Enable for low-traffic apps to scale to zero
2. **Right-size Machines** - Don't over-provision CPU/RAM
3. **Use shared CPUs** - Sufficient for most workloads
4. **Monitor usage** - Check `fly dashboard` for resource consumption
5. **Clean up unused apps** - Destroy test/staging apps when not needed

### Reliability

1. **Multiple Machines** - Run at least 2 Machines for high availability
2. **Health checks** - Automatic traffic routing away from unhealthy Machines
3. **Rolling deployments** - Default behavior prevents downtime during updates
4. **Backup volumes** - Snapshot important data regularly
5. **Monitor logs** - Use `fly logs` or integrate with logging services

## Troubleshooting

### Common Issues

**App won't start:**
```bash
# Check logs
fly logs

# Verify configuration
fly config validate

# SSH into Machine
fly ssh console
```

**Port binding errors:**
- Ensure app listens on `0.0.0.0` not `localhost`
- Match `internal_port` in fly.toml with app's listening port
- Check `PORT` environment variable

**Build failures:**
```bash
# Build locally to test
fly deploy --local-only

# Use remote builder
fly deploy --remote-only

# Check Dockerfile syntax
docker build .
```

**Slow performance:**
- Check Machine size (CPU/RAM)
- Review autoscaling configuration
- Verify database connection pooling
- Enable connection reuse
- Check region proximity to users/services

**Database connection issues:**
- Verify `DATABASE_URL` secret is set
- Check Postgres cluster status: `fly status --app my-db`
- Use Fly.io private network addresses (`.internal`)
- Ensure connection pooling (pgbouncer)

### Getting Help

```bash
# Community forum
fly open https://community.fly.io

# Documentation
fly docs

# Support
fly support

# Status page
fly open https://status.fly.io
```

## Resources

### Official Documentation
- Fly.io Docs: https://fly.io/docs/
- flyctl Reference: https://fly.io/docs/flyctl/
- Fly Launch: https://fly.io/docs/launch/
- App Configuration: https://fly.io/docs/reference/configuration/

### Community
- Community Forum: https://community.fly.io
- GitHub: https://github.com/superfly
- Twitter: @flydotio

### Pricing
- Free tier: 3 shared-cpu-1x Machines (256MB RAM)
- Additional resources: Pay-as-you-go
- Pricing calculator: https://fly.io/docs/about/pricing/

## Examples in Repository

See `knowledge/` directory for:
- Multi-region deployment examples
- Database integration patterns
- Background worker configurations
- Advanced networking setups

## Changelog

### Version 1.1 (2026-01-21)
- ✨ Added comprehensive Architecture & Deployment Blueprints section
- ✨ Added resilient applications pattern with multiple Machines
- ✨ Added autoscaling configuration examples
- ✨ Added background jobs and automation patterns
- ✨ Added developer workflow blueprints (zero-downtime, rollback, preview environments)
- ✨ Added cost efficiency guidance for stopped Machines
- ✨ Enhanced scaling commands with multi-region examples
- ✨ Added standby Machine pattern for worker processes

### Version 1.0 (2026-01-21)
- Initial skill creation
- Core Fly.io concepts and quick start guide
- Common commands and configuration
- Basic deployment patterns
- Best practices for performance, security, cost, and reliability
- Troubleshooting guide

---

**Version:** 1.1
**Last Updated:** 2026-01-21
**Source:** Fly.io Official Documentation + Blueprints
**Maintained By:** Claude Command and Control
