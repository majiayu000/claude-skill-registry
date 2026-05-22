---
name: otterstack-usage
description: Complete guide for using OtterStack - a Git-driven Docker Compose deployment tool with zero-downtime deployments. Use when deploying Docker Compose apps, managing projects, configuring environment variables, or troubleshooting deployments. Triggers on "how to use otterstack", "otterstack commands", "deploy with otterstack", "otterstack project", "otterstack env", or questions about OtterStack usage.
---

# OtterStack Usage Guide

Complete reference for using OtterStack - a deployment orchestration tool for Docker Compose applications with zero-downtime deployments via Traefik priority-based routing.

## What is OtterStack?

OtterStack is a **Git-driven deployment orchestrator** for Docker Compose applications running on a single VPS. It provides:

- **Zero-downtime deployments** using Traefik priority-based routing
- **Git worktree isolation** - each deployment gets its own directory
- **Health check validation** before traffic switching
- **Automatic rollback** if deployments fail
- **Environment variable management** with smart type detection
- **Deployment history** and retention policies

### Core Concepts

1. **Projects**: A project is a Docker Compose application tracked in git
2. **Worktrees**: Each deployment creates an isolated git worktree
3. **Deployments**: Deploy any git ref (commit, branch, tag)
4. **Priority Routing**: New containers start at priority 200, old at 100
5. **Health Checks**: Validates containers before traffic switch (5 min timeout)

## Installation

```bash
go build ./cmd/otterstack
./otterstack version
```

## Quick Start

### 1. Add Your First Project

**Local repository:**
```bash
otterstack project add myapp /srv/myapp
```

**Remote repository:**
```bash
otterstack project add myapp https://github.com/user/repo.git
```

**With Traefik zero-downtime routing:**
```bash
otterstack project add myapp https://github.com/user/repo.git --traefik-routing
```

**Custom compose file:**
```bash
otterstack project add myapp /srv/myapp --compose-file docker-compose.prod.yml
```

### 2. Configure Environment Variables

OtterStack now has **smart environment variable management** with auto-discovery!

**Option 1: Auto-discovery during project add**
```bash
# Create .env.<project-name> in current directory
echo "DATABASE_URL=postgres://localhost/mydb" > .env.myapp
echo "API_KEY=secret123" >> .env.myapp

# Add project - OtterStack will auto-discover and load the file
otterstack project add myapp /srv/myapp

# Prompts interactively for any missing variables
```

**Option 2: Set variables manually**
```bash
otterstack env set myapp DATABASE_URL=postgres://localhost/mydb
otterstack env set myapp API_KEY=secret DEBUG=false
```

**Option 3: Load from file**
```bash
otterstack env load myapp .env.production
```

**Option 4: Interactive scan (for existing projects)**
```bash
otterstack env scan myapp
# Scans compose file, prompts for missing variables
```

**List variables:**
```bash
otterstack env list myapp
otterstack env list myapp --show-values  # Show actual values
```

**Get specific variable:**
```bash
otterstack env get myapp DATABASE_URL
```

**Remove variables:**
```bash
otterstack env unset myapp DEBUG
```

### 3. Deploy

**Deploy default branch:**
```bash
otterstack deploy myapp
```

**Deploy specific ref:**
```bash
otterstack deploy myapp --ref feature/new-ui
otterstack deploy myapp --ref v1.2.3
otterstack deploy myapp --ref a1b2c3d4
```

**Force deploy (skip validations - use carefully!):**
```bash
otterstack deploy myapp --force
```

### 4. Check Status

**List all projects:**
```bash
otterstack project list
```

**View project details:**
```bash
otterstack status myapp
```

**Check deployment history:**
```bash
otterstack deployments myapp
```

### 5. Manage Projects

**Remove project:**
```bash
otterstack project remove myapp
```

**Force remove (skip confirmation):**
```bash
otterstack project remove myapp --force
```

## Environment Variable Management

### Smart Type Detection

OtterStack automatically detects variable types from names:

| Pattern | Type | Validation |
|---------|------|------------|
| `DATABASE_URL`, `API_ENDPOINT` | URL | Must have scheme (https://) |
| `ADMIN_EMAIL`, `SUPPORT_EMAIL` | Email | Valid email format |
| `HTTP_PORT`, `DB_PORT` | Port | 1-65535 |
| `WORKER_COUNT`, `MAX_CONNECTIONS`, `TIMEOUT` | Integer | Valid number |
| `DEBUG_ENABLED`, `FEATURE_FLAG`, `USE_SSL` | Boolean | Yes/No dialog |
| Everything else | String | Basic validation |

### Interactive Prompts

When you run `env scan` or `project add`, OtterStack:

1. **Parses compose file** to find all `${VAR}` references
2. **Checks stored values** to identify missing variables
3. **Groups prompts**: Required first, optional second
4. **Type-aware UI**: Booleans use Yes/No dialogs, others use validated text inputs
5. **Shows context**: "Used by: web, worker"
6. **Generates `.env.example`** for documentation

### Supported Variable Formats

OtterStack parses these Docker Compose formats:

```yaml
services:
  web:
    environment:
      - DATABASE_URL=${DATABASE_URL}              # Required
      - API_URL=${API_URL:-https://api.example.com}  # Optional with default
      - SECRET_KEY=${SECRET_KEY:?Secret key required}  # Required with error message
      - DEBUG=$DEBUG                              # Simple form
```

## Zero-Downtime Deployments with Traefik

### Prerequisites

1. **Traefik running** and connected to Docker
2. **Compose file has Traefik labels:**

```yaml
services:
  web:
    image: myapp:latest
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.web.rule=Host(`myapp.example.com`)"
```

3. **Project added with `--traefik-routing` flag**

### How It Works

```
1. [Old Containers Serving] → Priority: 100

2. [Start New Containers] → No Traefik labels yet

3. [Health Check] → Wait up to 5 minutes

4. [Apply Priority Labels] → New: 200, Old: 100

5. [Traffic Switches] → Traefik routes to higher priority

6. [Stop Old Containers] → Deployment complete
```

If health checks fail at step 3, old containers keep serving traffic.

### Deployment Flow

**Without Traefik:**
- Start new containers
- Stop old containers immediately
- Brief downtime during switch

**With Traefik:**
- Start new containers (no traffic)
- Wait for healthy
- Switch traffic priority
- Stop old containers
- Zero downtime!

## Command Reference

### Project Management

```bash
# Add project
otterstack project add <name> <repo-path-or-url> [flags]
  --compose-file string    Path to compose file (default: docker-compose.yml)
  --traefik-routing        Enable zero-downtime Traefik routing

# List projects
otterstack project list

# Remove project
otterstack project remove <name> [--force]

# View project status
otterstack status <name>
```

### Environment Variables

```bash
# Set variables
otterstack env set <project> KEY=VALUE [KEY=VALUE...]

# Get variable
otterstack env get <project> [KEY]

# List variables
otterstack env list <project> [--show-values]

# Load from file
otterstack env load <project> <file>

# Interactive scan
otterstack env scan <project>

# Remove variables
otterstack env unset <project> KEY [KEY...]
```

### Deployment

```bash
# Deploy
otterstack deploy <project> [flags]
  --ref string     Git ref to deploy (commit, branch, tag)
  --force          Skip validation checks

# View deployment history
otterstack deployments <project>
```

### Global Flags

```bash
--config string    Config file (default: $HOME/.otterstack.yaml)
--data-dir string  Data directory (default: $HOME/.otterstack)
--verbose          Verbose output
--help            Show help
--version         Show version
```

## Common Workflows

### First-Time Project Setup

```bash
# 1. Create .env file
cat > .env.myapp <<EOF
DATABASE_URL=postgres://user:pass@localhost/mydb
REDIS_URL=redis://localhost:6379
API_KEY=your-secret-key
EOF

# 2. Add project (auto-discovers .env.myapp)
otterstack project add myapp https://github.com/user/repo.git --traefik-routing

# 3. Verify configuration
otterstack env list myapp

# 4. Deploy
otterstack deploy myapp
```

### Adding Variables to Existing Project

```bash
# Option 1: Interactive scan
otterstack env scan myapp

# Option 2: Manual set
otterstack env set myapp NEW_VAR=value

# Option 3: Load from file
otterstack env load myapp .env.new
```

### Deploying a Feature Branch

```bash
# Deploy feature branch
otterstack deploy myapp --ref feature/new-ui

# Check status
otterstack status myapp

# If good, merge to main and deploy
git checkout main
git merge feature/new-ui
git push
otterstack deploy myapp --ref main
```

### Rolling Back a Deployment

```bash
# Deploy previous commit
otterstack deploy myapp --ref HEAD~1

# Or deploy specific commit
otterstack deploy myapp --ref a1b2c3d
```

### Updating Environment Variables

```bash
# Update variable
otterstack env set myapp API_KEY=new-key

# Redeploy for changes to take effect
otterstack deploy myapp
```

## Pre-Deployment Validation

OtterStack validates environment variables **before** starting deployment:

```bash
$ otterstack deploy myapp

Validating environment variables...
❌ ERROR: Missing required environment variables

The following variables are required but not set:

  DATABASE_URL
    • Required by: web, worker
    • Error: Database connection required

  API_KEY
    • Required by: web

To fix this, you can:
  1. Set variables individually:
     otterstack env set myapp DATABASE_URL=<value>
     otterstack env set myapp API_KEY=<value>

  2. Use interactive scan:
     otterstack env scan myapp

  3. Load from file:
     otterstack env load myapp .env.myapp

Error: missing required environment variables
```

This prevents wasted deployment attempts with incomplete configuration!

## Troubleshooting

### "Project not found"

```bash
# List all projects
otterstack project list

# Verify project name matches exactly
```

### "Lock file exists"

Another deployment is in progress or a previous one failed:

```bash
# Wait for deployment to finish, or if stuck:
rm ~/.otterstack/locks/<project>.lock

# Then retry
otterstack deploy myapp
```

### "Missing required environment variables"

```bash
# Scan for missing variables
otterstack env scan myapp

# Or check what's missing
otterstack env list myapp
```

### "Health check failed"

Containers didn't become healthy within 5 minutes:

```bash
# Check container logs
docker compose -f /path/to/worktree/docker-compose.yml logs

# Check container status
docker compose -f /path/to/worktree/docker-compose.yml ps

# Fix issues, then redeploy
otterstack deploy myapp
```

### "Compose file not found"

```bash
# Verify compose file path
cat ~/.otterstack/projects.db | grep compose_file

# Update if wrong
# (Currently requires manual DB edit - future feature)
```

### Environment Variables Not Working

```bash
# Verify variables are set
otterstack env list myapp --show-values

# Check compose file syntax
grep -E '\$\{[A-Z_]+\}' docker-compose.yml

# Redeploy after setting variables
otterstack deploy myapp
```

## Best Practices

### 1. Environment Variables

- ✅ Use `.env.<project-name>` files during initial setup
- ✅ Run `env scan` to catch missing variables early
- ✅ Use type-appropriate variable names (DATABASE_URL, HTTP_PORT)
- ✅ Store secrets securely, never commit to git
- ✅ Generate `.env.example` for documentation
- ❌ Don't hardcode values in compose files
- ❌ Don't skip the pre-deployment validation

### 2. Docker Compose Files

- ✅ Use `${VAR}` syntax for environment variables
- ✅ Provide defaults with `${VAR:-default}` when possible
- ✅ Include health checks for all services
- ✅ Use Traefik labels for zero-downtime deployments
- ❌ Don't use `container_name` (breaks worktree isolation)
- ❌ Don't use `env_file` (OtterStack manages env vars)

### 3. Deployments

- ✅ Deploy to staging/testing first
- ✅ Use `--traefik-routing` for production apps
- ✅ Tag important releases: `git tag v1.0.0`
- ✅ Keep deployment history: check retention policy
- ✅ Monitor health checks during deployment
- ❌ Don't use `--force` in production unless necessary
- ❌ Don't deploy without testing env vars first

### 4. Project Organization

- ✅ Use descriptive project names
- ✅ Document required env vars in README
- ✅ Keep compose files simple and standard
- ✅ Use semantic versioning for tags
- ❌ Don't mix projects in the same repo
- ❌ Don't commit environment-specific config

## Advanced Topics

### Worktree Management

OtterStack creates git worktrees for each deployment:

```bash
# Worktrees are stored at:
~/.otterstack/worktrees/<project>/<commit-hash>/

# Each worktree is isolated with its own:
# - Git checkout
# - Docker Compose state
# - Environment file
```

### Retention Policy

Old worktrees are cleaned up based on retention policy:
- Failed deployments: Kept for debugging
- Successful deployments: Configurable retention

### Direct Compose Access

You can interact with deployed containers directly:

```bash
# Find worktree path
WORKTREE=$(ls -t ~/.otterstack/worktrees/myapp | head -1)

# Use docker compose directly
docker compose -f ~/.otterstack/worktrees/myapp/$WORKTREE/docker-compose.yml logs
docker compose -f ~/.otterstack/worktrees/myapp/$WORKTREE/docker-compose.yml exec web bash
```

### Health Check Configuration

Compose file health check example:

```yaml
services:
  web:
    image: myapp:latest
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 10s
      timeout: 5s
      retries: 3
      start_period: 30s
```

## Version History

### v0.2.0 (2026-01-11)

- ✨ Enhanced environment variable management
- ✨ Auto-discovery of `.env.<project-name>` files
- ✨ Smart type detection and validation
- ✨ Interactive `env scan` command
- ✨ Pre-deployment validation gate
- ✨ Automatic `.env.example` generation

### Earlier Versions

- v0.2.0-rc.4: Fixed double-locking bug
- v0.2.0-rc.3: Fixed TOCTOU race condition
- v0.2.0-rc.2: Real-time Docker output streaming

## Getting Help

```bash
# General help
otterstack --help

# Command-specific help
otterstack project --help
otterstack env --help
otterstack deploy --help

# Version info
otterstack version
```

## Related Files

- `README.md` - Overview and quick start
- `IMPROVEMENTS.md` - Proposed enhancements based on deployment experience
- `TROUBLESHOOTING.md` - Common issues and solutions
- `.claude/plans/enhanced-env-var-management.md` - Implementation plan for env var features

## Summary

OtterStack makes Docker Compose deployments **simple** and **safe**:

1. **Add project** with `project add`
2. **Configure env vars** with `env scan` or auto-discovery
3. **Deploy** with `deploy`
4. **Zero downtime** with Traefik routing
5. **Automatic rollback** if things fail

The enhanced environment variable management ensures you never deploy with missing configuration, and the interactive prompts make setup a breeze!

## Usage in Orchestration

This skill is referenced during **Phase 4: Setup** and **Phase 5: Deployment** of the `/deploy-otterstack` command.

### Integration Points

The orchestration command uses this skill's documentation to execute OtterStack commands in three modes:

1. **Project Setup Mode** - Check if project exists and add if needed
2. **Environment Variable Setup Mode** - Load/scan/configure environment variables
3. **Deployment Mode** - Execute deployment with verbose monitoring

### Project Setup Mode

When the orchestration command needs to set up a new project:

**Check if project exists:**
```bash
# Local
otterstack project list | grep -q "^${PROJECT_NAME}$"

# VPS
ssh archivist@194.163.189.144 "~/OtterStack/otterstack project list | grep -q '^${PROJECT_NAME}$'"
```

**Add project if missing (local):**
```bash
otterstack project add ${PROJECT_NAME} /path/to/repo --traefik-routing
```

**Add project if missing (remote/VPS):**
```bash
# Get remote git URL
REPO_URL=$(git config --get remote.origin.url)

# Add to VPS
ssh archivist@194.163.189.144 "~/OtterStack/otterstack project add ${PROJECT_NAME} ${REPO_URL} --traefik-routing"
```

### Environment Variable Setup Mode

When the orchestration command configures environment variables:

**Auto-load from .env file if exists:**
```bash
if [ -f ".env.${PROJECT_NAME}" ]; then
  # Local
  otterstack env load ${PROJECT_NAME} .env.${PROJECT_NAME}

  # VPS
  scp .env.${PROJECT_NAME} archivist@194.163.189.144:/tmp/
  ssh archivist@194.163.189.144 "~/OtterStack/otterstack env load ${PROJECT_NAME} /tmp/.env.${PROJECT_NAME}"
fi
```

**Interactive scan for missing variables:**
```bash
# Local
otterstack env scan ${PROJECT_NAME}

# VPS
ssh archivist@194.163.189.144 "~/OtterStack/otterstack env scan ${PROJECT_NAME}"
```

**Validate all required vars are set:**
```bash
# Local
otterstack env list ${PROJECT_NAME}

# VPS
ssh archivist@194.163.189.144 "~/OtterStack/otterstack env list ${PROJECT_NAME}"
```

**Set individual variables:**
```bash
# Local
otterstack env set ${PROJECT_NAME} DATABASE_URL="postgres://..."

# VPS
ssh archivist@194.163.189.144 "~/OtterStack/otterstack env set ${PROJECT_NAME} DATABASE_URL='postgres://...'"
```

### Deployment Mode

When the orchestration command executes deployment:

**Deploy with verbose output for monitoring:**
```bash
# Local
otterstack deploy ${PROJECT_NAME} -v

# VPS
ssh archivist@194.163.189.144 "~/OtterStack/otterstack deploy ${PROJECT_NAME} -v"
```

**Monitor deployment stages:**
The orchestration command watches for these sequential stages:
1. "Fetching latest changes..." → Git operations (remote repos only)
2. "Validating compose file..." → Syntax and env var validation
3. "Pulling images..." → Docker image downloads
4. "Starting services..." → Container creation and startup
5. "Waiting for containers to be healthy..." → Health check polling
6. "Applying Traefik priority labels..." → Traffic routing setup
7. "Deployment successful!" → Completion

**Check deployment status:**
```bash
# Local
otterstack status ${PROJECT_NAME}

# VPS
ssh archivist@194.163.189.144 "~/OtterStack/otterstack status ${PROJECT_NAME}"
```

**View deployment history:**
```bash
# Local
otterstack deployments ${PROJECT_NAME}

# VPS
ssh archivist@194.163.189.144 "~/OtterStack/otterstack deployments ${PROJECT_NAME}"
```

### Quick Reference for Orchestration

Commands used by `/deploy-otterstack`:

**Pre-flight checks:**
```bash
# Verify OtterStack is installed
which otterstack || command -v otterstack

# VPS: Test SSH connection
ssh -o ConnectTimeout=5 archivist@194.163.189.144 "echo 'SSH OK'"

# VPS: Verify OtterStack on VPS
ssh archivist@194.163.189.144 "~/OtterStack/otterstack --version"
```

**Project existence check:**
```bash
# Returns exit code 0 if exists, 1 if not
otterstack project list | grep -q "^${PROJECT_NAME}$" && echo "exists" || echo "missing"
```

**Quick deployment status:**
```bash
otterstack status ${PROJECT_NAME} 2>&1
```

**Force redeploy if lock stuck:**
```bash
# Local
rm ~/.otterstack/locks/${PROJECT_NAME}.lock
otterstack deploy ${PROJECT_NAME} -v

# VPS
ssh archivist@194.163.189.144 "rm ~/.otterstack/locks/${PROJECT_NAME}.lock"
ssh archivist@194.163.189.144 "~/OtterStack/otterstack deploy ${PROJECT_NAME} -v"
```

**Get previous deployment SHA (for rollback):**
```bash
# Local
otterstack deployments ${PROJECT_NAME} | tail -2 | head -1 | awk '{print $2}'

# VPS
ssh archivist@194.163.189.144 "~/OtterStack/otterstack deployments ${PROJECT_NAME} | tail -2 | head -1 | awk '{print \$2}'"
```

**Deploy specific ref (rollback):**
```bash
# Local
otterstack deploy ${PROJECT_NAME} --ref ${PREVIOUS_SHA} -v

# VPS
ssh archivist@194.163.189.144 "~/OtterStack/otterstack deploy ${PROJECT_NAME} --ref ${PREVIOUS_SHA} -v"
```

### Context Passing

The orchestration command maintains these variables that inform OtterStack commands:

- `PROJECT_NAME` - Name of the project being deployed
- `DEPLOYMENT_TARGET` - "local" or "vps"
- `SSH_PREFIX` - Empty for local, "ssh archivist@194.163.189.144" for VPS
- `OTTERSTACK_CMD` - "otterstack" for local, "~/OtterStack/otterstack" for VPS
- `REPO_PATH` - Local repository path
- `REPO_URL` - Git repository URL (for VPS)

Commands are constructed as:
```bash
${SSH_PREFIX} ${OTTERSTACK_CMD} [subcommand] [args]
```

### Error Handling

The orchestration command handles these OtterStack error scenarios:

| Error | OtterStack Message | Orchestration Action |
|-------|-------------------|----------------------|
| Missing env vars | "variable X is not set" | Run `env scan` or prompt user |
| Project not found | "project not found" | Add project with `project add` |
| Lock held | "deployment in progress" | Wait or remove stale lock |
| Validation failed | "compose validation failed" | Invoke debug-vps-deployment |
| Health check failed | "container unhealthy" | Invoke debug-vps-deployment |

### Related Commands

- `/deploy-otterstack` - Full orchestration command that uses this skill in Phases 4 and 5
