---
name: kamal
description: Deploy containerized web applications to any Linux server using Kamal. Use when users need to deploy, configure, debug, or manage Kamal deployments including initial setup, configuration of deploy.yml, deployment workflows, rollbacks, managing accessories (databases, Redis), troubleshooting deployment issues, or understanding Kamal commands and best practices.
---

# Kamal Deployment

Kamal is a zero-downtime deployment tool for containerized applications, originally built by 37signals for deploying Rails apps but works with any containerized web application.

## Core Concepts

**Philosophy**: Kamal uses an imperative "push" model where you explicitly tell servers what to do, unlike declarative tools like Kubernetes. It combines SSH, Docker, and Kamal Proxy to achieve zero-downtime deployments.

**Components**:
- **SSH/SSHKit**: Remote command execution
- **Docker**: Container runtime and image management
- **Kamal Proxy**: Reverse proxy for zero-downtime deployments (routes traffic between container versions)
- **Accessories**: Supporting services (PostgreSQL, MySQL, Redis, etc.)

## When to Use This Skill

Use this skill when you need to:
- Set up Kamal for a new project
- Configure `config/deploy.yml` or understand configuration options
- Deploy applications or troubleshoot deployment failures
- Manage multiple environments (staging, production)
- Configure accessories (databases, Redis, etc.)
- Debug deployment issues or container problems
- Perform rollbacks or maintenance mode
- Understand Kamal commands and workflows
- Set up CI/CD pipelines with Kamal

## Quick Start Workflow

### Initial Setup
```bash
# 1. Install Kamal
gem install kamal

# 2. Initialize configuration
cd your-app
kamal init

# 3. Edit config/deploy.yml
# - Set service name and image
# - Add server IP addresses
# - Configure registry credentials
# - Set environment variables

# 4. Configure secrets in .kamal/secrets
KAMAL_REGISTRY_PASSWORD=your-token
RAILS_MASTER_KEY=your-key

# 5. Run initial setup (installs Docker, deploys everything)
kamal setup
```

### Standard Deploy
```bash
kamal deploy              # Build, push, deploy with zero downtime
kamal deploy -d staging   # Deploy to staging environment
kamal app logs -f         # Follow application logs
```

### Common Operations
```bash
kamal app exec -i --reuse "bin/rails console"  # Rails console
kamal app logs -g "error"                       # Search logs
kamal rollback <version>                        # Rollback
kamal app maintenance                           # Maintenance mode
kamal app live                                  # Exit maintenance
```

## Configuration Patterns

### Basic deploy.yml Structure
```yaml
service: myapp
image: username/myapp

servers:
  web:
    - 192.168.1.10

registry:
  server: ghcr.io
  username: myuser
  password:
    - KAMAL_REGISTRY_PASSWORD

env:
  secret:
    - RAILS_MASTER_KEY
  clear:
    RAILS_ENV: production

proxy:
  ssl: true
  host: example.com
```

### Multi-Server with Roles
```yaml
servers:
  web:
    hosts:
      - 192.168.1.10
      - 192.168.1.11
  worker:
    hosts:
      - 192.168.1.12
    cmd: bundle exec sidekiq
```

### Accessories (Supporting Services)
```yaml
accessories:
  postgres:
    image: postgres:15
    host: 192.168.1.20
    port: 5432
    env:
      secret:
        - POSTGRES_PASSWORD
      clear:
        POSTGRES_DB: myapp_production
    directories:
      - data:/var/lib/postgresql/data
  
  redis:
    image: redis:7
    host: 192.168.1.21
    directories:
      - data:/data
```

For comprehensive configuration options, see **references/configuration.md**.

## Essential Commands

### Deployment
- `kamal init` - Initialize configuration files
- `kamal setup` - First-time setup (installs Docker, deploys everything)
- `kamal deploy` - Standard deploy with zero downtime
- `kamal redeploy` - Fast redeploy (skips proxy setup)
- `kamal rollback VERSION` - Rollback to previous version

### Application Management
- `kamal app logs [-f]` - View logs (follow with -f)
- `kamal app exec "COMMAND"` - Run command in container
- `kamal app exec -i --reuse "bash"` - Interactive shell
- `kamal app maintenance` - Enable maintenance mode
- `kamal app live` - Disable maintenance mode
- `kamal app containers` - List all containers (for rollback)
- `kamal app version` - Show deployed version

### Accessories
- `kamal accessory boot NAME` - Start accessory
- `kamal accessory logs NAME [-f]` - View accessory logs
- `kamal accessory exec NAME "CMD"` - Run command in accessory

### Troubleshooting
- `kamal config` - Show parsed configuration
- `kamal lock status` - Check deployment lock
- `kamal lock release` - Release stuck lock
- `kamal server exec "CMD"` - Run command on host

### Multiple Environments
- `kamal deploy -d staging` - Deploy to staging
- `kamal deploy -h 192.168.1.10` - Deploy to specific host
- `kamal deploy -r web` - Deploy to specific role

For complete command reference, see **references/commands.md**.

## Common Workflows

### Deploy with Database Migration

**Using pre-deploy hook** (recommended):

Create `.kamal/hooks/pre-deploy`:
```bash
#!/bin/bash
kamal app exec -p -q "bin/rails db:migrate"
```

```bash
chmod +x .kamal/hooks/pre-deploy
kamal deploy
```

### Rollback Workflow
```bash
# Check what went wrong
kamal app logs

# List available versions
kamal app containers

# Rollback to previous version
kamal rollback abc123def
```

### Debugging Failed Deployments

1. **Check logs**: `kamal app logs -n 500`
2. **Check container status**: `kamal server exec "docker ps -a"`
3. **Test health endpoint**: `kamal app exec "curl localhost:3000/up"`
4. **Check configuration**: `kamal config`
5. **Release stuck locks**: `kamal lock release`

### Multiple Environments Pattern

Create environment-specific configs:
- `config/deploy.yml` (production)
- `config/deploy.staging.yml`

```bash
kamal setup -d staging
kamal deploy -d staging
kamal deploy  # production
```

For detailed workflows, troubleshooting guides, and best practices, see **references/workflows.md**.

## Database and Accessory Management

### Running Commands in Accessories
```bash
# PostgreSQL
kamal accessory exec postgres "psql -U myapp"
kamal accessory exec postgres "pg_dump -U myapp myapp_production" > backup.sql

# Redis
kamal accessory exec redis "redis-cli"

# MySQL
kamal accessory exec mysql "mysql -u root -p myapp_production"
```

### Litestream (SQLite Replication)
```bash
kamal accessory exec litestream "litestream generations /data/production.sqlite3"
kamal accessory exec litestream "litestream restore /data/production.sqlite3"
```

## Configuration for Common Scenarios

### Custom SSH User/Port
```yaml
ssh:
  user: deploy
  port: 2222
```

### Custom Build Context
```yaml
builder:
  context: .
  dockerfile: Dockerfile.production
  args:
    RUBY_VERSION: 3.2.0
```

### Health Check Configuration
```yaml
healthcheck:
  path: /up
  port: 3000
  interval: 10
  max_attempts: 7
```

### Aliases for Common Commands
```yaml
aliases:
  console: app exec --interactive --reuse "bin/rails console"
  shell: app exec --interactive --reuse "bash"
  logs: app logs -f
```

Use: `kamal console` instead of full command.

## CI/CD Integration

### GitHub Actions Example
```yaml
- name: Deploy
  env:
    KAMAL_REGISTRY_PASSWORD: ${{ secrets.REGISTRY_TOKEN }}
    RAILS_MASTER_KEY: ${{ secrets.RAILS_MASTER_KEY }}
  run: |
    gem install kamal
    kamal deploy
```

## Key Limitations

1. **No automatic state reconciliation** - Kamal won't automatically decommission containers if you remove them from config
2. **No dynamic provisioning** - Cannot auto-scale or provision servers on demand
3. **Single-server load balancing only** - Kamal Proxy balances containers on each server, not across servers (use external load balancer for that)

## References

This skill includes comprehensive reference documentation:

- **configuration.md** - Complete `config/deploy.yml` reference with all options, registry configurations, accessory setups, and example configurations
- **commands.md** - Detailed command reference for all Kamal CLI commands with options and examples
- **workflows.md** - Common deployment workflows, troubleshooting patterns, CI/CD integration, security best practices, and production guidelines

Read these references when you need detailed information about specific configuration options, commands, or deployment patterns.
