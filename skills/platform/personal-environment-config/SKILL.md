---
name: personal-environment-config
description: Manage environment variables and deployment configuration across local and production environments. Use this skill when asked to "add environment variable", "configure production", "sync env vars", "set up credentials", "add API keys to production", "configure new integration", "what env vars are needed", or any task involving environment configuration between local development and Oracle Cloud production. Covers .env file management, Docker Compose environment passing, GitHub Secrets, and integration-specific configurations (Google OAuth, Slack, WhatsApp, JIRA, etc.).
---

# Environment Configuration Management

Manage environment variables and configuration across local development and Oracle Cloud production.

## Environment Files Overview

| File | Purpose | Slack App | Use When |
|------|---------|-----------|----------|
| `.env` | **Local development** | orienter-test (A0A7JQ1KXLJ) | Running locally, testing changes |
| `.env.production` | **Production reference** | orienter (A0A2CCF4EEA) | Updating GitHub Secrets, deploying |
| `.env.test` | Test app backup | orienter-test | Reference for test credentials |

### Key Difference: Slack Apps
- **Local (.env)**: Uses `orienter-test` app with `-test` suffix commands (`/ai-test`, `/health-test`, etc.)
- **Production (.env.production)**: Uses `orienter` app with standard commands (`/ai`, `/health`, etc.)

## Environment Overview

| Environment | Location | .env File | Container Config |
|-------------|----------|-----------|------------------|
| **Local Dev** | Workstation | `.env` (project root) | `docker/docker-compose.local.yml` |
| **Production** | Oracle Cloud | `~/orienter/.env` | `docker/docker-compose.prod.yml` |

## Quick Reference: Adding New Environment Variables

### Step 1: Add to Local `.env`
```bash
echo 'NEW_VAR=value' >> .env
```

### Step 2: Add to Production `.env`
```bash
export OCI_HOST=152.70.172.33 OCI_USER=opc
ssh $OCI_USER@$OCI_HOST "echo 'NEW_VAR=value' >> ~/orienter/.env"
```

### Step 3: Restart Containers (to pick up new vars)
```bash
# Local
./run.sh dev stop && ./run.sh dev

# Production
ssh $OCI_USER@$OCI_HOST "cd ~/orienter/docker && docker compose --env-file ../.env -f docker-compose.yml -f docker-compose.prod.yml -f docker-compose.r2.yml up -d --force-recreate"
```

### Step 4: Verify Variables Loaded
```bash
# Local - check if var is in container
docker exec orienter-opencode env | grep NEW_VAR

# Production
ssh $OCI_USER@$OCI_HOST "docker exec orienter-opencode env | grep NEW_VAR"
```

## Environment Files

### Local Development (`.env`)
Located at project root. Loaded by:
- `scripts/dev.sh` - exports all vars before starting services
- Docker Compose - via `--env-file` flag

### Production (`~/orienter/.env`)
Located on Oracle Cloud server. Loaded by:
- Docker Compose at container startup
- Must recreate containers to pick up new vars

### Template (`templates/organization/config.example.json`)
Reference template for required configuration. Update when adding new integrations.

## Integration-Specific Configurations

For detailed configuration requirements per integration, see [references/integrations.md](references/integrations.md).

### Google OAuth (Quick Reference)
```bash
# Required variables
GOOGLE_OAUTH_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_OAUTH_CLIENT_SECRET=GOCSPX-your-secret

# Callback URLs to register in Google Cloud Console
# Local:      http://127.0.0.1:8766/oauth/google/callback
# Production: https://ai.proph.bet/oauth/callback
```

### Slack Bot
```bash
SLACK_BOT_TOKEN=xoxb-...
SLACK_SIGNING_SECRET=...
SLACK_APP_TOKEN=xapp-...
```

### WhatsApp Cloud API
```bash
WHATSAPP_CLOUD_API_ENABLED=true  # false for local Baileys mode
WHATSAPP_CLOUD_API_PHONE_NUMBER_ID=...
WHATSAPP_CLOUD_API_ACCESS_TOKEN=...
```

### JIRA
```bash
JIRA_HOST=your-site.atlassian.net
JIRA_EMAIL=your-email@domain.com
JIRA_API_TOKEN=your-api-token
```

## Comparing Environments

### View All Variables Diff
```bash
# Export local vars
grep -v '^#' .env | grep '=' | sort > /tmp/local-env.txt

# Export production vars
ssh $OCI_USER@$OCI_HOST "grep -v '^#' ~/orienter/.env | grep '=' | sort" > /tmp/prod-env.txt

# Compare
diff /tmp/local-env.txt /tmp/prod-env.txt
```

### Check Specific Variable
```bash
# Local
grep "VAR_NAME" .env

# Production  
ssh $OCI_USER@$OCI_HOST "grep 'VAR_NAME' ~/orienter/.env"
```

## Docker Compose Environment Passing

Variables from `.env` are passed to containers via compose files:

```yaml
# docker-compose.yml (base)
services:
  opencode:
    environment:
      - NODE_ENV=${NODE_ENV:-production}
      - GOOGLE_OAUTH_CLIENT_ID=${GOOGLE_OAUTH_CLIENT_ID}
      - GOOGLE_OAUTH_CLIENT_SECRET=${GOOGLE_OAUTH_CLIENT_SECRET}
```

**Important**: After adding new env vars:
1. Add to `.env` files (both environments)
2. Add to `docker-compose.yml` or overlay if container needs it
3. Recreate containers with `--force-recreate`

## GitHub Secrets (CI/CD)

**IMPORTANT**: When updating GitHub Secrets, use values from `.env.production` (NOT `.env`).

The `.env` file contains LOCAL/TEST credentials (orienter-test Slack app), while `.env.production` contains PRODUCTION credentials (orienter Slack app).

### Updating GitHub Secrets Workflow

```bash
# 1. Get the production value from .env.production
grep "SECRET_NAME" .env.production

# 2. Set the GitHub secret with production value
gh secret set SECRET_NAME --body "production-value-from-env-production"

# 3. List secrets to verify
gh secret list
```

### Example: Updating Slack Secrets in GitHub
```bash
# Use .env.production values (NOT .env which has test app)
gh secret set SLACK_BOT_TOKEN --body "$(grep SLACK_BOT_TOKEN .env.production | cut -d= -f2)"
gh secret set SLACK_SIGNING_SECRET --body "$(grep SLACK_SIGNING_SECRET .env.production | cut -d= -f2)"
gh secret set SLACK_APP_TOKEN --body "$(grep SLACK_APP_TOKEN .env.production | cut -d= -f2)"
```

### Production Secrets Reference
| Secret | Source | Description |
|--------|--------|-------------|
| `SLACK_BOT_TOKEN` | `.env.production` | Production Slack bot token (orienter app) |
| `SLACK_SIGNING_SECRET` | `.env.production` | Production Slack signing secret |
| `SLACK_APP_TOKEN` | `.env.production` | Production Slack app token |
| `OCI_SSH_KEY` | SSH key file | SSH private key for Oracle Cloud |
| `GHCR_TOKEN` | GitHub | GitHub Container Registry token |

## Common Tasks

| Task | Command |
|------|---------|
| Add var to local | `echo 'VAR=value' >> .env` |
| Add var to production | `ssh $OCI_USER@$OCI_HOST "echo 'VAR=value' >> ~/orienter/.env"` |
| View local env | `cat .env` |
| View production env | `ssh $OCI_USER@$OCI_HOST "cat ~/orienter/.env"` |
| Restart local | `./run.sh dev stop && ./run.sh dev` |
| Restart production | See "Force recreate containers" above |
| Check var in container | `docker exec CONTAINER env \| grep VAR` |
| Compare envs | See "Comparing Environments" above |

## PostgreSQL Database Configuration

### DATABASE_URL Format
```bash
DATABASE_URL=postgresql://USER:PASSWORD@HOST:PORT/DATABASE

# Examples:
DATABASE_URL=postgresql://orient:aibot123@localhost:5432/whatsapp_bot_0
DATABASE_URL=postgresql://postgres:mypassword@db.example.com:5432/production_db
```

### Required Variables
```bash
# .env file - used by both application and Docker Compose
POSTGRES_USER=orient
POSTGRES_PASSWORD=aibot123
DATABASE_URL=postgresql://orient:aibot123@localhost:5432/whatsapp_bot_0
```

### Docker Compose PostgreSQL Setup
The `docker/docker-compose.infra.yml` file uses environment variables:
```yaml
services:
  postgres:
    environment:
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
      - POSTGRES_DB=${POSTGRES_DB:-whatsapp_bot_0}
```

**Start PostgreSQL:**
```bash
docker compose -f docker/docker-compose.infra.yml up -d postgres
```

**Verify PostgreSQL is running:**
```bash
docker logs orienter-postgres-0 2>&1 | tail -5
# Should show: "database system is ready to accept connections"
```

### Common PostgreSQL Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `ECONNREFUSED` | PostgreSQL not running | Start with `docker compose -f docker/docker-compose.infra.yml up -d postgres` |
| `password authentication failed for user "X"` | Wrong credentials | Check DATABASE_URL user/password matches POSTGRES_USER/POSTGRES_PASSWORD |
| `database "X" does not exist` | DB not created | Check POSTGRES_DB or create with `docker exec orienter-postgres-0 createdb -U $POSTGRES_USER dbname` |

### Troubleshooting: Password Authentication Failed

**Error:** `password authentication failed for user "aibot"`

**Cause:** DATABASE_URL uses different credentials than what PostgreSQL was configured with.

**Debug steps:**
```bash
# 1. Check what credentials PostgreSQL was started with
docker exec orienter-postgres-0 env | grep POSTGRES

# 2. Check your DATABASE_URL format
grep DATABASE_URL .env

# 3. Ensure they match:
#    - DATABASE_URL user must match POSTGRES_USER
#    - DATABASE_URL password must match POSTGRES_PASSWORD
```

**Fix:**
```bash
# If .env has POSTGRES_USER=orient but DATABASE_URL has user "aibot":
# Update DATABASE_URL to use correct user
DATABASE_URL=postgresql://orient:aibot123@localhost:5432/whatsapp_bot_0
```

### Package-Level .env Files

Some packages (like `packages/dashboard/`) may have their own `.env` files that override root `.env`:

```bash
# Check if dashboard has its own .env
cat packages/dashboard/.env

# Add DATABASE_URL if missing
echo 'DATABASE_URL=postgresql://orient:aibot123@localhost:5432/whatsapp_bot_0' >> packages/dashboard/.env
```

## Troubleshooting

### "Variable not set" in container
Container wasn't recreated after adding var:
```bash
# Production - force recreate
ssh $OCI_USER@$OCI_HOST "cd ~/orienter/docker && docker compose --env-file ../.env -f docker-compose.yml -f docker-compose.prod.yml -f docker-compose.r2.yml up -d --force-recreate opencode whatsapp-bot"
```

### Variable in .env but not in container
Check if variable is passed in docker-compose.yml environment section.

### OAuth callback URL mismatch
Ensure callback URLs are registered in the OAuth provider (Google Cloud Console, Slack App Settings).
