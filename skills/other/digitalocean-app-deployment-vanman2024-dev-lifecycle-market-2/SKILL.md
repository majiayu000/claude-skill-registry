---
name: digitalocean-app-deployment
description: DigitalOcean App Platform deployment using doctl CLI for containerized applications, web services, static sites, and databases. Includes app spec generation, deployment orchestration, environment management, domain configuration, and health monitoring. Use when deploying to App Platform, managing app specs, configuring databases, or when user mentions App Platform, app spec, managed deployment, or PaaS deployment.
allowed-tools: Bash, Read, Write, Edit
---

# DigitalOcean App Platform Deployment Skill

This skill provides comprehensive deployment lifecycle management for applications deployed to DigitalOcean App Platform using doctl CLI and app specs.

## Overview

The deployment lifecycle consists of five phases:
1. **Pre-Deployment Validation** - Application readiness, app spec validation, configuration
2. **App Spec Generation** - Create/update app spec based on project detection
3. **Deployment** - Create or update app, configure services and databases
4. **Domain & Environment Management** - Custom domains, environment variables, scaling
5. **Post-Deployment Verification** - Health checks, deployment status validation

## Supported Application Types

- **Web Services**: Node.js, Python, Go, Ruby, PHP applications
- **Static Sites**: React, Vue, Next.js static exports, Hugo, Jekyll
- **Workers**: Background jobs, queue processors, scheduled tasks
- **Databases**: PostgreSQL, MySQL, Redis (managed databases)
- **Docker**: Custom Docker containers

## Available Scripts

### 1. Application Validation

**Script**: `scripts/validate-app.sh <app-path>`

**Purpose**: Validates application is ready for App Platform deployment

**Checks**:
- Dockerfile present (for Docker apps) OR supported runtime detected
- Environment configuration (.env.example present)
- No hardcoded secrets in code or Dockerfile
- Port configuration matches App Platform requirements (8080 default)
- Build command specified or detectable
- Resource requirements reasonable

**Usage**:
```bash
# Validate Docker app
./scripts/validate-app.sh /path/to/docker-app

# Validate Node.js app
./scripts/validate-app.sh /path/to/nodejs-app

# Validate static site
STATIC_SITE=true ./scripts/validate-app.sh /path/to/static-site

# Verbose mode
VERBOSE=1 ./scripts/validate-app.sh .
```

**Exit Codes**:
- `0`: Validation passed
- `1`: Validation failed (must fix before deployment)

### 2. Generate App Spec

**Script**: `scripts/generate-app-spec.sh <app-path> <app-name>`

**Purpose**: Generates DigitalOcean app spec from project detection

**Actions**:
- Detects application type (Docker, Node.js, Python, static)
- Generates appropriate app spec configuration
- Configures build and run commands
- Sets up environment variables
- Defines health checks
- Configures resource limits
- Outputs app spec to .do/app.yaml

**Usage**:
```bash
# Generate app spec for Docker app
./scripts/generate-app-spec.sh /path/to/app myapp

# Generate with custom port
PORT=3000 ./scripts/generate-app-spec.sh /path/to/app myapp

# Generate with database
DATABASE=postgres ./scripts/generate-app-spec.sh /path/to/app myapp

# Generate for static site
STATIC_SITE=true ./scripts/generate-app-spec.sh /path/to/app myapp

# Generate with custom domain
DOMAIN=myapp.example.com ./scripts/generate-app-spec.sh /path/to/app myapp
```

**Environment Variables**:
- `APP_TYPE`: `docker`, `nodejs`, `python`, `static` (auto-detected if not specified)
- `PORT`: Port to run on (default: 8080 for App Platform)
- `DATABASE`: Database type (`postgres`, `mysql`, `redis`)
- `STATIC_SITE`: Set to `true` for static site deployments
- `DOMAIN`: Custom domain to configure
- `REGION`: DigitalOcean region (default: nyc)
- `INSTANCE_SIZE`: App instance size (default: basic-xxs)
- `INSTANCE_COUNT`: Number of instances (default: 1)

**Exit Codes**:
- `0`: App spec generated successfully
- `1`: Generation failed

### 3. Deploy to App Platform

**Script**: `scripts/deploy-to-app-platform.sh <app-spec-path> [app-id]`

**Purpose**: Deploys application to DigitalOcean App Platform

**Actions**:
- Validates doctl authentication
- Creates new app OR updates existing app
- Uploads app spec
- Triggers deployment
- Monitors deployment progress
- Captures deployment URL
- Verifies deployment completed

**Usage**:
```bash
# Create new app
./scripts/deploy-to-app-platform.sh .do/app.yaml

# Update existing app
./scripts/deploy-to-app-platform.sh .do/app.yaml abc123-app-id

# Deploy with monitoring
MONITOR=true ./scripts/deploy-to-app-platform.sh .do/app.yaml

# Deploy and wait for completion
WAIT=true ./scripts/deploy-to-app-platform.sh .do/app.yaml abc123-app-id
```

**Environment Variables**:
- `MONITOR`: Set to `true` to monitor deployment progress
- `WAIT`: Set to `true` to wait for deployment completion
- `TIMEOUT`: Deployment timeout in minutes (default: 15)

**Exit Codes**:
- `0`: Deployment successful
- `1`: Deployment failed

### 4. Update Environment Variables

**Script**: `scripts/update-env-vars.sh <app-id>`

**Purpose**: Updates environment variables for deployed app

**Actions**:
- Retrieves current app spec
- Prompts for updated environment variables
- Updates app spec with new variables
- Triggers redeployment to apply changes
- Verifies redeployment successful

**Usage**:
```bash
# Update env vars interactively
./scripts/update-env-vars.sh abc123-app-id

# Update from .env file
ENV_FILE=.env.production ./scripts/update-env-vars.sh abc123-app-id

# Update specific variables
KEY1=value1 KEY2=value2 ./scripts/update-env-vars.sh abc123-app-id
```

**Exit Codes**:
- `0`: Environment variables updated successfully
- `1`: Update failed

### 5. Configure Domain

**Script**: `scripts/configure-domain.sh <app-id> <domain>`

**Purpose**: Configures custom domain for App Platform app

**Actions**:
- Validates domain ownership
- Adds domain to app configuration
- Configures SSL/TLS certificate
- Updates DNS configuration
- Verifies domain is accessible

**Usage**:
```bash
# Add custom domain
./scripts/configure-domain.sh abc123-app-id myapp.example.com

# Add domain with www redirect
WWW_REDIRECT=true ./scripts/configure-domain.sh abc123-app-id myapp.example.com

# Force HTTPS
FORCE_HTTPS=true ./scripts/configure-domain.sh abc123-app-id myapp.example.com
```

**Exit Codes**:
- `0`: Domain configured successfully
- `1`: Configuration failed

### 6. Scale Application

**Script**: `scripts/scale-app.sh <app-id> <instance-count> [instance-size]`

**Purpose**: Scales app horizontally or vertically

**Actions**:
- Updates app spec with new instance configuration
- Triggers redeployment with new scale
- Monitors scaling progress
- Verifies all instances healthy

**Usage**:
```bash
# Scale to 3 instances
./scripts/scale-app.sh abc123-app-id 3

# Scale and change instance size
./scripts/scale-app.sh abc123-app-id 2 professional-xs

# Available instance sizes:
# - basic-xxs, basic-xs, basic-s, basic-m
# - professional-xs, professional-s, professional-m, professional-l
```

**Exit Codes**:
- `0`: Scaling successful
- `1`: Scaling failed

### 7. Health Check

**Script**: `scripts/health-check.sh <app-id>`

**Purpose**: Validates App Platform deployment health

**Checks**:
- App deployment status (active/deploying/failed)
- All components healthy
- HTTP endpoint responding
- Database connectivity (if configured)
- SSL certificate valid
- Resource usage within limits
- Recent deployment logs

**Usage**:
```bash
# Check app health
./scripts/health-check.sh abc123-app-id

# Continuous monitoring (runs every 60s)
MONITOR=true ./scripts/health-check.sh abc123-app-id

# Detailed health report
DETAILED=true ./scripts/health-check.sh abc123-app-id
```

**Exit Codes**:
- `0`: All health checks passed
- `1`: One or more health checks failed

### 8. Manage Deployment

**Script**: `scripts/manage-deployment.sh <action> <app-id>`

**Purpose**: Manage App Platform app lifecycle

**Actions**:
- `info`: Show app information and status
- `logs`: View app logs
- `restart`: Restart app components
- `rollback`: Rollback to previous deployment
- `destroy`: Delete app completely
- `list`: List all apps in account

**Usage**:
```bash
# Show app info
./scripts/manage-deployment.sh info abc123-app-id

# View logs (last 100 lines)
./scripts/manage-deployment.sh logs abc123-app-id

# View logs (follow)
FOLLOW=true ./scripts/manage-deployment.sh logs abc123-app-id

# Restart app
./scripts/manage-deployment.sh restart abc123-app-id

# Rollback to previous version
./scripts/manage-deployment.sh rollback abc123-app-id

# List all apps
./scripts/manage-deployment.sh list

# Destroy app (requires confirmation)
./scripts/manage-deployment.sh destroy abc123-app-id
```

## Available Templates

### 1. App Spec Template (Docker)

**File**: `templates/app-spec-docker.yaml`

**Purpose**: App spec for Docker-based applications

**Variables**:
- `{{APP_NAME}}`: Application name
- `{{GITHUB_REPO}}`: GitHub repository (optional)
- `{{BRANCH}}`: Git branch (default: main)
- `{{DOCKERFILE_PATH}}`: Path to Dockerfile
- `{{HTTP_PORT}}`: HTTP port (default: 8080)
- `{{HEALTH_PATH}}`: Health check endpoint
- `{{INSTANCE_SIZE}}`: Instance size
- `{{INSTANCE_COUNT}}`: Number of instances
- `{{ENV_VARS}}`: Environment variables

**Example**:
```yaml
name: {{APP_NAME}}
region: nyc
services:
- name: web
  dockerfile_path: {{DOCKERFILE_PATH}}
  github:
    repo: {{GITHUB_REPO}}
    branch: {{BRANCH}}
    deploy_on_push: true
  http_port: {{HTTP_PORT}}
  health_check:
    http_path: {{HEALTH_PATH}}
  instance_count: {{INSTANCE_COUNT}}
  instance_size_slug: {{INSTANCE_SIZE}}
  envs: {{ENV_VARS}}
```

### 2. App Spec Template (Node.js)

**File**: `templates/app-spec-nodejs.yaml`

**Purpose**: App spec for Node.js applications

**Example**:
```yaml
name: {{APP_NAME}}
region: nyc
services:
- name: web
  environment_slug: node-js
  github:
    repo: {{GITHUB_REPO}}
    branch: {{BRANCH}}
    deploy_on_push: true
  build_command: npm install && npm run build
  run_command: npm start
  http_port: 8080
  health_check:
    http_path: /health
  instance_count: 1
  instance_size_slug: basic-xxs
  envs:
  - key: NODE_ENV
    value: production
```

### 3. App Spec Template (Static Site)

**File**: `templates/app-spec-static.yaml`

**Purpose**: App spec for static site deployments

**Example**:
```yaml
name: {{APP_NAME}}
region: nyc
static_sites:
- name: frontend
  github:
    repo: {{GITHUB_REPO}}
    branch: {{BRANCH}}
    deploy_on_push: true
  build_command: npm install && npm run build
  output_dir: /dist
  routes:
  - path: /
```

### 4. App Spec Template (With Database)

**File**: `templates/app-spec-with-database.yaml`

**Purpose**: App spec with managed database

**Example**:
```yaml
name: {{APP_NAME}}
region: nyc
services:
- name: api
  environment_slug: python
  run_command: gunicorn app:app
  http_port: 8080
  envs:
  - key: DATABASE_URL
    scope: RUN_AND_BUILD_TIME
    type: SECRET
databases:
- name: db
  engine: PG
  version: "15"
  production: true
  cluster_name: {{APP_NAME}}-db
```

### 5. Deployment Configuration

**File**: `templates/deployment-config.json`

**Purpose**: Track App Platform deployments

**Structure**:
```json
{
  "version": "1.0.0",
  "deployments": [
    {
      "id": "deployment-uuid-here",
      "appId": "abc123-app-id",
      "appName": "myapp",
      "appType": "docker",
      "platform": "digitalocean-app-platform",
      "region": "nyc",
      "url": "https://myapp-abc123.ondigitalocean.app",
      "customDomain": "myapp.example.com",
      "status": "active",
      "deployedAt": "2025-11-02T19:00:00Z",
      "deployedBy": "user@example.com",
      "version": "1.0.0",
      "metadata": {
        "gitCommit": "abc123",
        "gitBranch": "main",
        "instanceSize": "basic-xxs",
        "instanceCount": 1,
        "database": {
          "engine": "postgres",
          "version": "15"
        }
      },
      "components": [
        {
          "name": "web",
          "type": "service",
          "port": 8080,
          "healthCheck": "/health"
        }
      ],
      "environmentVariables": [
        {
          "name": "DATABASE_URL",
          "scope": "RUN_AND_BUILD_TIME",
          "type": "secret",
          "isSet": true
        },
        {
          "name": "NODE_ENV",
          "value": "production",
          "scope": "RUN_TIME"
        }
      ],
      "health": {
        "lastCheck": "2025-11-02T19:05:00Z",
        "status": "healthy",
        "uptime": "99.9%",
        "activeDeployment": true
      }
    }
  ],
  "metadata": {
    "lastUpdated": "2025-11-02T19:05:00Z",
    "totalDeployments": 1,
    "activeDeployments": 1
  }
}
```

### 6. Deployment Checklist

**File**: `templates/deployment-checklist.md`

**Purpose**: Pre-deployment checklist for App Platform

**Contents**:
- [ ] doctl installed and authenticated
- [ ] Application validated locally
- [ ] Dockerfile present (for Docker apps) OR runtime detected
- [ ] Build command specified
- [ ] Port configured (8080 recommended for App Platform)
- [ ] All required environment variables identified
- [ ] .env.example created with all required variables
- [ ] No hardcoded secrets in code or Dockerfile
- [ ] Health check endpoint implemented (recommended)
- [ ] Database requirements identified (if applicable)
- [ ] Custom domain DNS records ready (if applicable)
- [ ] Resource requirements estimated
- [ ] Error handling and logging configured

## Examples

### Example 1: Docker FastAPI App

**File**: `examples/docker-fastapi-deployment.md`

**Shows**:
- Complete Docker-based FastAPI app deployment
- App spec generation for Docker
- Environment variable management
- Health check configuration
- Database integration (PostgreSQL)
- Custom domain setup

### Example 2: Node.js Express App

**File**: `examples/nodejs-express-deployment.md`

**Shows**:
- Node.js runtime deployment (no Docker)
- Build and run command configuration
- Environment detection
- Automatic SSL/TLS
- Scaling configuration

### Example 3: Static Site (Next.js)

**File**: `examples/static-site-deployment.md`

**Shows**:
- Next.js static export deployment
- Build optimization
- CDN configuration
- Custom domain with SSL
- Deploy on push configuration

### Example 4: Background Worker

**File**: `examples/background-worker-deployment.md`

**Shows**:
- Worker component deployment
- No HTTP port configuration
- Queue/job processing setup
- Resource allocation for workers
- Log monitoring

## Deployment Workflow

### Initial Deployment

1. **Validate Application**:
   ```bash
   ./scripts/validate-app.sh /path/to/app
   ```

2. **Generate App Spec**:
   ```bash
   ./scripts/generate-app-spec.sh /path/to/app myapp
   ```

3. **Deploy to App Platform**:
   ```bash
   ./scripts/deploy-to-app-platform.sh .do/app.yaml
   ```

4. **Verify Health**:
   ```bash
   ./scripts/health-check.sh <app-id>
   ```

5. **Configure Domain (Optional)**:
   ```bash
   ./scripts/configure-domain.sh <app-id> myapp.example.com
   ```

### Update Deployment

1. **Update App Spec** (if needed):
   ```bash
   ./scripts/generate-app-spec.sh /path/to/app myapp
   ```

2. **Deploy Update**:
   ```bash
   ./scripts/deploy-to-app-platform.sh .do/app.yaml <app-id>
   ```

3. **Verify Health**:
   ```bash
   ./scripts/health-check.sh <app-id>
   ```

### Update Environment Variables Only

1. **Update Env Vars**:
   ```bash
   ./scripts/update-env-vars.sh <app-id>
   ```

2. **Verify Redeployment**:
   ```bash
   ./scripts/manage-deployment.sh info <app-id>
   ```

### Scale Application

1. **Scale**:
   ```bash
   ./scripts/scale-app.sh <app-id> 3 professional-xs
   ```

2. **Verify Health**:
   ```bash
   ./scripts/health-check.sh <app-id>
   ```

## Security Best Practices

1. **Never Hardcode Secrets**: Always use environment variables in app spec
2. **Use Secret Type**: Mark sensitive env vars as `type: SECRET`
3. **Scope Variables**: Use appropriate scope (RUN_TIME, BUILD_TIME, RUN_AND_BUILD_TIME)
4. **Enable HTTPS**: Always configure SSL/TLS for custom domains
5. **Database Security**: Use managed databases with automatic backups
6. **Access Control**: Use DigitalOcean teams for multi-user access
7. **Monitor Logs**: Regularly check logs for security issues
8. **Rotate Secrets**: Use update-env-vars.sh to rotate API keys

## App Platform vs Droplets

### Use App Platform When:
- Need managed infrastructure (auto-scaling, load balancing)
- Want zero-downtime deployments
- Need managed databases
- Want automatic SSL/TLS
- Deploy from Git (GitHub, GitLab)
- Need CDN for static sites
- Want simplified deployment workflow

### Use Droplets When:
- Need full server control
- Custom system configurations required
- Non-standard ports or networking
- Legacy applications
- Cost optimization for stable workloads
- Custom security requirements

## Troubleshooting

### Build Failures

```bash
# View build logs
./scripts/manage-deployment.sh logs <app-id>

# Common issues:
# - Missing build dependencies
# - Incorrect build command
# - Port mismatch (App Platform expects 8080)
# - Missing environment variables at build time
```

### Deployment Failures

```bash
# Check deployment status
./scripts/manage-deployment.sh info <app-id>

# View recent logs
./scripts/manage-deployment.sh logs <app-id>

# Common issues:
# - Health check failing
# - Application not binding to 0.0.0.0:8080
# - Missing runtime environment variables
# - Database connection issues
```

### Health Check Failures

```bash
# Check app status
./scripts/health-check.sh <app-id>

# View logs for errors
./scripts/manage-deployment.sh logs <app-id>

# Common issues:
# - Health check path incorrect
# - App not responding on port 8080
# - Database not accessible
# - Insufficient resources
```

## Cost Optimization

### Instance Sizing
- **basic-xxs**: $5/month - Small apps, testing
- **basic-xs**: $12/month - Low-traffic apps
- **professional-xs**: $24/month - Production apps
- Scale down during off-hours using scaling scripts

### Database Costs
- **Dev Database**: $7/month - Development/testing
- **Basic Database**: $15/month - Small production
- **Production Database**: $60+/month - High availability

## Integration with Dev Lifecycle

This skill integrates with:
- `/deployment:prepare` - Pre-deployment validation
- `/deployment:deploy` - Execute App Platform deployment
- `/deployment:validate` - Post-deployment verification
- `/deployment:rollback` - Rollback to previous deployment

## Comparison: App Platform vs Droplet Deployment

| Feature | App Platform | Droplet |
|---------|-------------|---------|
| Setup Complexity | Low | Medium-High |
| Management | Fully Managed | Self-Managed |
| Scaling | Automatic | Manual |
| Load Balancing | Built-in | Requires Setup |
| SSL/TLS | Automatic | Manual |
| Database | Managed | Self-Hosted |
| Git Integration | Native | Manual |
| Zero Downtime | Yes | Requires Config |
| Cost (Small App) | ~$5-12/mo | ~$4-6/mo |
| Best For | Web apps, APIs, Static sites | Custom configs, Legacy apps |
