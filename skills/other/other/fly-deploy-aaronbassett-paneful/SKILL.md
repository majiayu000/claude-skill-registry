---
name: fly-deploy
description: Quick MVP deployment to fly.io for JavaScript (Next.js, RedwoodSDK, Express), Rust (Axum, Rocket), Python (FastAPI), and generic Dockerfiles. Use when deploying applications to fly.io, setting up databases (Postgres, volumes, Tigris object storage), managing secrets, configuring custom domains, setting up GitHub Actions workflows, creating review apps for pull requests, or troubleshooting fly.io deployments. Covers complete deployment workflows from initial setup through production.
---

# Fly.io Deployment

Quick MVP deployment to fly.io with support for multiple languages, databases, GitHub integration, and production-ready configurations.

## When to Use This Skill

Use this skill when you need to:
- Deploy a new application to fly.io quickly
- Migrate existing applications to fly.io
- Set up databases (Managed Postgres, SQLite with volumes, or Tigris object storage)
- Configure secrets and environment variables
- Add custom domains with SSL certificates
- Set up GitHub Actions for continuous deployment
- Create PR review apps (preview environments)
- Troubleshoot deployment or runtime issues
- Optimize fly.io configurations for cost and performance

## Quick Start

### New Application

```bash
# From your app directory
fly launch

# Follow interactive prompts:
# - Choose app name
# - Select region
# - Configure resources
# - Deploy immediately or create config only
```

### Existing Application

```bash
# Deploy app with existing fly.toml
fly deploy

# Build on fly.io servers (recommended for CI/CD)
fly deploy --remote-only
```

## Workflow Decision Tree

### 1. Choose Your Starting Point

**New App (No fly.toml)**
→ See: [Deploying New Applications](#deploying-new-applications)

**Existing fly.io App**
→ See: [Deploying Existing Applications](#deploying-existing-applications)

**Migrating from Another Platform**
→ See: [references/deployment-workflow.md](references/deployment-workflow.md) + Language-specific guides

### 2. Choose Your Language/Framework

Navigate to the appropriate language guide:

**JavaScript/Node.js:**
- Next.js → [references/languages/javascript.md#nextjs](references/languages/javascript.md)
- Express → [references/languages/javascript.md#express](references/languages/javascript.md)
- RedwoodJS → [references/languages/javascript.md#redwoodjs](references/languages/javascript.md)

**Python:**
- FastAPI → [references/languages/python.md#fastapi](references/languages/python.md)
- Django → [references/languages/python.md#django](references/languages/python.md)
- Flask → [references/languages/python.md#flask](references/languages/python.md)

**Rust:**
- Axum → [references/languages/rust.md#axum](references/languages/rust.md)
- Rocket → [references/languages/rust.md#rocket](references/languages/rust.md)

**Generic Dockerfile:**
→ See: [references/deployment-workflow.md](references/deployment-workflow.md)

Each language guide includes:
- Optimized Dockerfiles (see also: `assets/dockerfiles/`)
- fly.toml configuration examples
- Framework-specific best practices
- Common issues and solutions

### 3. Add Data Persistence (Optional)

Choose based on your needs:

**Managed Postgres** (Recommended for production SQL databases)
→ See: [references/data-persistence.md#managed-postgres](references/data-persistence.md)
→ Script: `scripts/init_postgres.sh`

**Volumes** (For SQLite, file uploads, or local storage)
→ See: [references/data-persistence.md#fly-volumes](references/data-persistence.md)

**Tigris Object Storage** (For media files, user uploads, S3-compatible)
→ See: [references/data-persistence.md#tigris-object-storage](references/data-persistence.md)
→ Script: `scripts/setup_tigris.sh`

**External Database** (Supabase, PlanetScale, Neon, etc.)
→ See: [references/data-persistence.md#external-databases](references/data-persistence.md)

### 4. Configure Secrets

→ See: [references/secrets-and-env.md](references/secrets-and-env.md)

```bash
# Set secrets
fly secrets set DATABASE_URL=postgres://...
fly secrets set API_KEY=abc123

# Generate random secrets
fly secrets set SECRET_KEY=$(openssl rand -hex 32)
```

### 5. Add Custom Domain (Optional)

→ See: [references/domains-and-networking.md](references/domains-and-networking.md)

```bash
# Add custom domain
fly certs add example.com

# View DNS instructions
fly certs show example.com
```

### 6. Set Up CI/CD (Optional)

**GitHub Actions Deployment:**
→ See: [references/github-integration.md](references/github-integration.md)
→ Template: `assets/workflows/deploy.yml`

**PR Review Apps:**
→ See: [references/github-integration.md#review-apps](references/github-integration.md)
→ Template: `assets/workflows/review-apps.yml`
→ Script: `scripts/setup_review_apps.sh`

## Deploying New Applications

### Step 1: Prepare Your Application

Ensure your app has:
1. **Dockerfile** or package.json/requirements.txt (for buildpacks)
2. **Health endpoint** (e.g., `/health` returning 200 OK)
3. **Port configuration** reading from `PORT` environment variable
4. **Bind to 0.0.0.0** (not localhost or 127.0.0.1)

Example Dockerfiles available in: `assets/dockerfiles/`
- `nextjs.Dockerfile`
- `express.Dockerfile`
- `fastapi.Dockerfile`
- `axum.Dockerfile`
- `rocket.Dockerfile`

### Step 2: Initialize fly.io App

```bash
fly launch
```

Interactive prompts will:
- Detect your app type
- Suggest a name
- Choose a region
- Create `fly.toml`
- Optionally deploy immediately

**Useful flags:**
```bash
# Skip deployment, just create config
fly launch --no-deploy

# Specify app name
fly launch --name my-app

# Choose region
fly launch --region ord  # Chicago
```

### Step 3: Configure fly.toml

Review and adjust `fly.toml`:

```toml
app = "my-app"
primary_region = "ord"

[build]
  dockerfile = "Dockerfile"

[env]
  PORT = "8080"

[http_service]
  internal_port = 8080
  force_https = true
  auto_stop_machines = "stop"
  auto_start_machines = true
  min_machines_running = 0  # Scale to zero for cost savings

  [[http_service.checks]]
    grace_period = "10s"
    interval = "30s"
    path = "/health"

[[vm]]
  memory = "256mb"
  cpus = 1
```

→ For complete fly.toml reference: [references/deployment-workflow.md](references/deployment-workflow.md)

### Step 4: Deploy

```bash
fly deploy
```

Your app will be available at: `https://my-app.fly.dev`

## Deploying Existing Applications

For apps with existing `fly.toml`:

```bash
# Standard deployment
fly deploy

# Remote build (recommended for CI/CD)
fly deploy --remote-only

# Specific deployment strategy
fly deploy --strategy rolling  # Zero downtime (default)
fly deploy --strategy immediate  # Faster, brief downtime
```

## Common Tasks

### Adding a Database

**Managed Postgres (Recommended):**
```bash
# Using the provided script
./scripts/init_postgres.sh --app my-app

# Or manually
fly postgres create --name my-app-db
fly postgres attach my-app-db
```

**Tigris Object Storage:**
```bash
# Using the provided script
./scripts/setup_tigris.sh --app my-app

# Or manually
fly storage create
```

→ See: [references/data-persistence.md](references/data-persistence.md)

### Managing Secrets

```bash
# Set secrets
fly secrets set DATABASE_URL=postgres://...
fly secrets set API_KEY=secret123

# List secrets (names only)
fly secrets list

# Remove secrets
fly secrets unset API_KEY
```

→ See: [references/secrets-and-env.md](references/secrets-and-env.md)

### Setting Up Review Apps

```bash
# Using the provided script
./scripts/setup_review_apps.sh --org personal --region ord

# Or copy template manually
cp assets/workflows/review-apps.yml .github/workflows/
```

→ See: [references/github-integration.md#review-apps](references/github-integration.md)

### Adding Custom Domain

```bash
# Add domain
fly certs add example.com

# Get your app's IP addresses
fly ips list

# Configure DNS (A and AAAA records)
# Then verify
fly certs show example.com
```

→ See: [references/domains-and-networking.md](references/domains-and-networking.md)

### Scaling

```bash
# Scale memory
fly scale memory 512

# Scale machine size
fly scale vm shared-cpu-2x

# Scale instance count
fly scale count 3

# Scale across regions
fly scale count 2 --region ord,iad
```

→ See: [references/deployment-workflow.md#scaling](references/deployment-workflow.md)

## Troubleshooting

### Common Issues

**App won't start:**
```bash
# Check logs
fly logs

# Verify port configuration
# App must listen on PORT env var and bind to 0.0.0.0
```

**Health checks failing:**
```bash
# Test health endpoint
fly ssh console -C "curl http://localhost:8080/health"

# Adjust grace period in fly.toml if needed
```

**Database connection errors:**
```bash
# Verify DATABASE_URL is set
fly secrets list

# Test from within app
fly ssh console
echo $DATABASE_URL
```

**Deployment slow or timing out:**
```bash
# Use remote builder
fly deploy --remote-only

# Check build cache
fly deploy --no-cache
```

→ For comprehensive troubleshooting: [references/troubleshooting.md](references/troubleshooting.md)

### Debugging Commands

```bash
# View app status
fly status

# Stream logs
fly logs

# SSH into running machine
fly ssh console

# List machines
fly machine list

# View deployments
fly releases

# Check health checks
fly checks list
```

## Reference Documentation

### Core Guides

- **[Deployment Workflow](references/deployment-workflow.md)** - fly.toml configuration, deployment strategies, scaling
- **[Data Persistence](references/data-persistence.md)** - Postgres, volumes, Tigris, external databases
- **[Secrets Management](references/secrets-and-env.md)** - Environment variables, secret handling, security
- **[GitHub Integration](references/github-integration.md)** - GitHub Actions, review apps, CI/CD
- **[Custom Domains](references/domains-and-networking.md)** - DNS setup, SSL certificates, networking
- **[Troubleshooting](references/troubleshooting.md)** - Common issues, debugging techniques, solutions

### Language-Specific Guides

- **[JavaScript/Node.js](references/languages/javascript.md)** - Next.js, Express, RedwoodJS
- **[Python](references/languages/python.md)** - FastAPI, Django, Flask
- **[Rust](references/languages/rust.md)** - Axum, Rocket

## Bundled Resources

### Scripts (`scripts/`)

Automation scripts for common tasks:

- **`setup_review_apps.sh`** - Generate GitHub Actions workflow for PR review apps
- **`init_postgres.sh`** - Create and attach Managed Postgres database
- **`setup_tigris.sh`** - Configure Tigris object storage bucket

All scripts include help text. Run with `--help` or without arguments for usage.

### Dockerfile Templates (`assets/dockerfiles/`)

Production-ready Dockerfiles for each framework:

- **`nextjs.Dockerfile`** - Next.js with standalone output (minimal image)
- **`express.Dockerfile`** - Express.js with multi-stage build
- **`fastapi.Dockerfile`** - FastAPI with uvicorn
- **`axum.Dockerfile`** - Axum with optimized Rust build
- **`rocket.Dockerfile`** - Rocket with multi-stage build

Copy and customize for your app.

### GitHub Actions Workflows (`assets/workflows/`)

Ready-to-use workflow templates:

- **`deploy.yml`** - Basic deployment on push to main
- **`review-apps.yml`** - PR review apps with automatic cleanup
- **`test-and-deploy.yml`** - Run tests before deploying

Copy to `.github/workflows/` and customize.

## Best Practices

1. **Always use health checks** - Ensures reliable deployments
2. **Start with minimal resources** - Scale up based on actual usage
3. **Use Managed Postgres** for production - Don't run unmanaged databases
4. **Set secrets properly** - Never commit secrets to git
5. **Use remote builds for CI/CD** - `fly deploy --remote-only`
6. **Test locally first** - Build and test Docker images locally
7. **Monitor logs regularly** - `fly logs` helps catch issues early
8. **Use review apps** - Test changes before merging
9. **Configure graceful shutdown** - Handle SIGTERM properly
10. **Keep dependencies updated** - Security and performance

## Quick Reference

```bash
# Essential commands
fly launch              # Create new app
fly deploy             # Deploy app
fly status             # Check app status
fly logs               # View logs
fly ssh console        # SSH into machine

# Database
fly postgres create    # Create database
fly postgres attach    # Attach to app
fly storage create     # Create Tigris bucket

# Configuration
fly secrets set KEY=value    # Set secret
fly secrets list            # List secrets
fly scale memory 512        # Scale memory
fly scale count 3           # Scale instances

# Domains
fly certs add example.com   # Add domain
fly certs show example.com  # Check certificate
fly ips list               # Get IP addresses

# Troubleshooting
fly logs                    # Stream logs
fly ssh console            # Access machine
fly checks list            # View health checks
fly releases               # View deployments
```

## Getting Help

- **Documentation:** https://fly.io/docs/
- **Community Forum:** https://community.fly.io/
- **Status Page:** https://status.flyio.net/
- **This Skill:** Check [references/troubleshooting.md](references/troubleshooting.md) for common issues

---

**Note:** fly.io changes frequently. This skill is based on documentation current as of January 2026. If commands or features have changed, consult the official fly.io documentation at https://fly.io/docs/
