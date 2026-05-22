---
name: railway-project-management
description: Comprehensive Railway.com project, environment, and variable management. Use when creating Railway projects, managing environments, configuring services, setting variables, syncing environments, managing PR environments, or organizing Railway infrastructure.
---

# Railway Project Management

Comprehensive management of Railway.com projects, environments, services, and variables using the Railway CLI.

## Overview

This skill provides complete workflows for:
- Creating and linking Railway projects
- Managing environments (production, staging, PR environments)
- Adding services from GitHub, Docker, or local sources
- Configuring variables (service, shared, reference, sealed)
- Syncing and duplicating environments
- Project settings and validation

## Prerequisites

- Railway CLI installed and authenticated (use `railway-auth` skill)
- Git repository (for GitHub integrations)
- Docker (optional, for container deployments)

## Workflow

### 1. Project Creation and Linking

**Create new Railway project:**
```bash
# Initialize new project interactively
railway init

# Create project with specific name
railway init --name "my-project"

# Link to existing project (interactive)
railway link

# Link to specific project by ID
railway link -p <project-id>

# Link to project with specific environment and service
railway link -p <project-id> -e <environment-id> -s <service-id>

# Check current project status
railway status
```

**Project information:**
```bash
# View project details
railway status

# View project in browser
railway open

# Unlink from current project
railway unlink
```

### 2. Environment Management

**Create and switch environments:**
```bash
# List all environments
railway environment

# Create new empty environment
railway environment --name staging

# Create duplicate of current environment
railway environment --name production-backup --duplicate

# Switch to specific environment
railway environment production

# Delete environment (interactive)
railway environment delete
```

**Environment types:**
- **Production**: Main deployment environment
- **Staging**: Pre-production testing
- **PR Environments**: Auto-created per pull request
- **Custom**: Any named environment for specific needs

See `references/environment-types.md` for detailed guide.

### 3. Service Operations

**Add services from different sources:**

```bash
# Add service from GitHub repository
railway add --repo owner/repo

# Add service from current directory
railway add

# Add Docker image
railway add --image postgres:15

# Add template (e.g., database)
railway add --template postgres
```

**Service sources:**
- **GitHub**: Auto-deploy from repository
- **Docker**: Deploy container images
- **Local**: Deploy from current directory
- **Templates**: Pre-configured services (databases, etc.)

See `references/service-sources.md` for detailed configurations.

### 4. Variable Management

**Set variables at different scopes:**

```bash
# Set service variable (current service only)
railway variables set API_KEY=secret123

# Set shared variable (all services in environment)
railway variables set --shared DATABASE_URL=postgres://...

# Set sealed variable (enhanced security)
railway variables set --sealed STRIPE_KEY=sk_live_...

# Reference variable from another service
railway variables set API_URL='${{ api-service.PUBLIC_URL }}'

# Delete variable
railway variables delete API_KEY

# List all variables
railway variables list
```

**Variable types:**

1. **Service Variables**: Isolated to specific service
2. **Shared Variables**: Available to all services in environment
3. **Reference Variables**: Reference other service variables using `${{ service.VAR }}` syntax
4. **Sealed Variables**: Enhanced security, cannot be unsealed or viewed after creation

**Variable scoping:**
```
Project
├── Environment (production)
│   ├── Service A
│   │   ├── Service variables (API_KEY)
│   │   └── Can access shared variables
│   ├── Service B
│   │   ├── Service variables (DB_PASSWORD)
│   │   └── Can access shared variables
│   └── Shared variables (LOG_LEVEL, NODE_ENV)
```

See `references/variable-scoping.md` for advanced patterns.

### 5. Configuration and Settings

**Project settings:**
```bash
# View project settings in browser
railway open --settings

# Enable/configure PR environments
# (Done via dashboard - automated per PR)

# Configure deployment triggers
# (Done via dashboard - branch filters, paths)
```

**Service settings:**
```bash
# View service in browser
railway open

# Configure via railway.json or railway.toml
cat > railway.json <<EOF
{
  "build": {
    "builder": "NIXPACKS",
    "buildCommand": "npm run build"
  },
  "deploy": {
    "startCommand": "npm start",
    "healthcheckPath": "/health",
    "restartPolicyType": "ON_FAILURE"
  }
}
EOF
```

**Advanced configuration:**
- Health checks and restart policies
- Resource limits (CPU, memory)
- Custom build commands
- Root directory overrides
- Networking and domains

### 6. Verification and Validation

**Verify project setup:**
```bash
# Check project status
railway status

# List all environments
railway environment

# List services
railway list

# Check variables
railway variables list

# View logs
railway logs

# Open in browser for visual verification
railway open
```

**Common validation checks:**
- ✅ Project linked correctly
- ✅ Environments created (production, staging)
- ✅ Services deployed successfully
- ✅ Variables set at correct scope
- ✅ PR environments enabled (if needed)
- ✅ All services healthy

## Common Workflows

### Initialize New Full-Stack Project

Use the automation script:
```bash
.claude/skills/railway-project-management/scripts/init-project.sh
```

Or manually:
```bash
# 1. Initialize project
railway init --name my-app

# 2. Create environments
railway environment --name staging
railway environment --name production

# 3. Add services (in production)
railway environment production
railway add --repo owner/frontend-repo
railway add --repo owner/api-repo
railway add --template postgres

# 4. Set shared variables
railway variables set --shared NODE_ENV=production
railway variables set --shared LOG_LEVEL=info

# 5. Replicate to staging
railway environment staging
# (Set staging-specific variables)

# 6. Enable PR environments (via dashboard)
railway open --settings
```

### Sync Variables Between Environments

Use the automation script:
```bash
.claude/skills/railway-project-management/scripts/sync-env.sh production staging
```

### Add Database to Existing Project

```bash
# 1. Switch to desired environment
railway environment production

# 2. Add database template
railway add --template postgres

# 3. Set shared DATABASE_URL
# (Usually auto-set by Railway)

# 4. Reference in other services
railway variables set DATABASE_URL='${{ postgres.DATABASE_URL }}'
```

### Configure PR Environments

```bash
# 1. Enable in project settings
railway open --settings

# 2. Configure PR environment settings:
# - Base environment to duplicate
# - Services to include
# - Variable handling

# 3. PR environments auto-create on new PRs
# - Each PR gets isolated environment
# - Auto-deploys on PR updates
# - Auto-deletes on PR close/merge
```

## Reference Variables Pattern

```bash
# Service A exposes PUBLIC_URL
railway variables set --service api-service PUBLIC_URL=https://api.railway.app

# Service B references it
railway variables set --service frontend API_URL='${{ api-service.PUBLIC_URL }}'

# Service C uses multiple references
railway variables set --service worker \
  API_URL='${{ api-service.PUBLIC_URL }}' \
  DB_URL='${{ postgres.DATABASE_URL }}'
```

**Benefits:**
- DRY (Don't Repeat Yourself)
- Auto-updates when source changes
- Type-safe service connections
- Clear dependency graph

## Security Best Practices

### Sealed Variables
```bash
# Use sealed for production secrets
railway environment production
railway variables set --sealed STRIPE_SECRET_KEY=sk_live_...
railway variables set --sealed AWS_SECRET_ACCESS_KEY=...

# Regular variables for non-sensitive config
railway variables set --shared NODE_ENV=production
```

**When to use sealed variables:**
- API keys and secrets
- Database passwords
- OAuth client secrets
- Encryption keys
- Any sensitive credential

**Sealed variable characteristics:**
- Cannot be viewed after creation (not even in UI)
- Cannot be unsealed
- Can only be overwritten or deleted
- Enhanced security for compliance

### Variable Organization
```bash
# Shared variables: Cross-service configuration
railway variables set --shared NODE_ENV=production
railway variables set --shared LOG_LEVEL=info
railway variables set --shared REGION=us-west-2

# Service variables: Service-specific config
railway variables set --service api PORT=3000
railway variables set --service api API_VERSION=v1

# Sealed variables: Secrets
railway variables set --sealed DATABASE_PASSWORD=...
railway variables set --sealed JWT_SECRET=...
```

## Environment Strategies

### Strategy 1: Production + Staging
```
production (main branch)
├── All services
├── Production data
└── Sealed secrets

staging (develop branch)
├── All services
├── Test data
└── Staging secrets
```

### Strategy 2: Production + PR Environments
```
production (main branch)
├── All services
└── Production data

PR-123 (auto-created)
├── All services (from production template)
├── Isolated test data
└── Auto-deploys on PR updates
```

### Strategy 3: Multi-Environment Pipeline
```
development → staging → production
     ↓            ↓          ↓
  Dev data   Test data  Prod data
  Dev URLs   Stage URLs Prod URLs
```

## Troubleshooting

### Project Not Linked
```bash
# Symptom: "No project linked"
# Solution:
railway link
# Or specify project ID:
railway link -p abc123
```

### Wrong Environment
```bash
# Check current environment
railway status

# Switch to correct environment
railway environment production
```

### Variable Not Found
```bash
# List all variables to verify
railway variables list

# Check variable scope (service vs shared)
railway variables list --service api
railway variables list --shared

# Set if missing
railway variables set VAR_NAME=value
```

### Service Not Deploying
```bash
# Check deployment logs
railway logs --deployment

# Check service status
railway status

# Redeploy
railway up
```

## Related Skills

- **railway-auth**: Authenticate with Railway CLI
- **railway-deployment**: Deploy services and manage deployments
- **railway-troubleshooting**: Debug Railway issues
- **railway-cli**: Core Railway CLI operations
- **railway-observability**: Monitor Railway services

## Quick Reference

### Project Operations
| Command | Description |
|---------|-------------|
| `railway init` | Initialize new project |
| `railway link` | Link to existing project |
| `railway unlink` | Unlink current project |
| `railway status` | Show project status |
| `railway open` | Open project in browser |

### Environment Operations
| Command | Description |
|---------|-------------|
| `railway environment` | List/switch environments |
| `railway environment --name <name>` | Create new environment |
| `railway environment --duplicate` | Duplicate current environment |
| `railway environment delete` | Delete environment |

### Service Operations
| Command | Description |
|---------|-------------|
| `railway add` | Add service from current directory |
| `railway add --repo <owner/repo>` | Add from GitHub |
| `railway add --image <image>` | Add Docker image |
| `railway add --template <name>` | Add template service |
| `railway list` | List all services |

### Variable Operations
| Command | Description |
|---------|-------------|
| `railway variables set KEY=value` | Set service variable |
| `railway variables set --shared KEY=value` | Set shared variable |
| `railway variables set --sealed KEY=value` | Set sealed variable |
| `railway variables delete KEY` | Delete variable |
| `railway variables list` | List all variables |

## Additional Resources

- **References**:
  - `references/environment-types.md`: Detailed environment guide
  - `references/variable-scoping.md`: Variable scoping patterns
  - `references/service-sources.md`: Service deployment sources

- **Scripts**:
  - `scripts/init-project.sh`: Initialize complete project
  - `scripts/sync-env.sh`: Sync variables between environments

- **Railway Documentation**:
  - [Projects](https://docs.railway.app/reference/projects)
  - [Environments](https://docs.railway.app/reference/environments)
  - [Variables](https://docs.railway.app/reference/variables)
  - [PR Environments](https://docs.railway.app/reference/environments#pr-environments)
