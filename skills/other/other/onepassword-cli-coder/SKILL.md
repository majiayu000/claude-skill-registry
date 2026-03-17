---
name: onepassword-cli-coder
description: This skill guides integrating 1Password CLI (op) for secret management in development workflows. Use when loading secrets for infrastructure, deployments, or local development.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# 1Password CLI Coder

## Overview

The 1Password CLI (`op`) provides secure secret injection into development workflows without exposing credentials in code, environment files, or shell history.

### IMPORTANT: ALWAYS reference to */.*/skills/onepassword-cli-coder/resources/1passwrd_agents_guide.md before and/or after any 1password operation. Ask to the user to set 1password Service Account Token if you can't find it in the vault to manage GitHub action workflows auth operations or if working with containers/sandboxes. ###

### IF NECESSARY (or requested by the user) use this skill in combination with 1password-direnv-secrets skill ( */.*/skills/1password-direnv-secrets/ )

## Core Patterns

### we always use 'AI DEV' vault for our API KEYs or SECRET TOKENS to: store, search, find, copy the reference, use in env and config files, ecc

### Always check first wich credentials/items are needed for the requested task and deeply search for related items in the AI DEV vault (NEVER READ THE REAL KEYS) to copy the op reference and use it in config/env files if necessary. If you can't find the necessary item always ask to the user to create one or provide the correct item name
 
You found command reference for searching items and copying related reference in */.*/skills/onepassword-cli-coder/resources/1passwrd_agents_guide.md

### Secret Reference Format

```
op://AI DEV/<item>/credential
```


Examples:
```
op://AI DEV/JINA.AI API key/credential
op://AI DEV/Morph API key/credential
op://AI DEV/Exa API/credential
```

### Item Naming Conventions

## IF NECESSARY you can purpose to the user to let you create a specific new 1passwrd vault for this project/repo + the creation and storing in it of the env vars, keys, tokens, ecc needed to accomplish the requested task/operation

If you have to create items to store credentials (or the user ask you to do it)
use `{environment}-{service}` format for item names:

| Pattern | Example | Notes |
|---------|---------|-------|
| `{env}-{service}` | `production-rails` | Primary app secrets |
| `{env}-{provider}` | `production-dockerhub` | External service credentials |
| `{env}-{provider}-{resource}` | `production-hetzner-s3` | Provider with multiple resources |

**DO:**
- Use kebab-case (no spaces, no underscores)
- Prefix with environment (`production-`, `staging-`, `development-`)
- Keep names descriptive but concise

**DON'T:**
- Use spaces in item names (`Production Rails` → `production-rails`)
- Use generic names (`API Key` → `production-stripe`)
- Mix environments in one item (create separate items per environment)

### Field Naming

Use semantic field names that describe the credential type:

| Good | Bad | Why |
|------|-----|-----|
| `access_token` | `value` | Self-documenting |
| `master_key` | `secret` | Specific purpose clear |
| `secret_access_key` | `key` | Matches AWS naming |
| `api_token` | `token` | Distinguishes from other tokens |

Field naming rules:
- Match the provider's terminology when possible (AWS uses `access_key_id`, `secret_access_key`)
- Use snake_case for consistency
- Be specific: `database_password` not just `password` when item has multiple credentials

### Environment File (.op.env)

Create `.op.env` in project root:

```bash
# AWS credentials
AWS_ACCESS_KEY_ID=op://Infrastructure/AWS/access_key_id
AWS_SECRET_ACCESS_KEY=op://Infrastructure/AWS/secret_access_key
AWS_REGION=op://Infrastructure/AWS/region

# DigitalOcean
DIGITALOCEAN_TOKEN=op://Infrastructure/DigitalOcean/api_token

# Database
DATABASE_URL=op://Production/PostgreSQL/connection_string

# API Keys
STRIPE_SECRET_KEY=op://Production/Stripe/secret_key
OPENAI_API_KEY=op://Development/OpenAI/api_key
```

**Critical:** Add to `.gitignore`:
```gitignore
# 1Password - NEVER commit
.op.env
*.op.env
```

### Running Commands with Secrets

```bash
# Single command
op run --env-file=.op.env -- terraform plan

# With environment variable prefix
op run --env-file=.op.env -- rails server

# Inline secret reference
op run -- printenv DATABASE_URL
```

## Integration Patterns

### Makefile Integration

```makefile
OP ?= op
OP_ENV_FILE ?= .op.env

# Prefix for all commands needing secrets
CMD = $(OP) run --env-file=$(OP_ENV_FILE) --

deploy:
	$(CMD) kamal deploy

console:
	$(CMD) rails console

migrate:
	$(CMD) rails db:migrate
```

### Docker Compose

```yaml
# docker-compose.yml
services:
  app:
    build: .
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
```

```bash
# Run with secrets injected
op run --env-file=.op.env -- docker compose up
```

### Kamal Deployment

```yaml
# config/deploy.yml
env:
  secret:
    - RAILS_MASTER_KEY
    - DATABASE_URL
    - REDIS_URL
```

```bash
# .kamal/secrets (loaded by Kamal)
RAILS_MASTER_KEY=$(op read "op://Production/Rails/master_key")
DATABASE_URL=$(op read "op://Production/PostgreSQL/url")
REDIS_URL=$(op read "op://Production/Redis/url")
```

### CI/CD (GitHub Actions)

```yaml
# .github/workflows/deploy.yml
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: 1password/load-secrets-action@v2
        with:
          export-env: true
        env:
          OP_SERVICE_ACCOUNT_TOKEN: ${{ secrets.OP_SERVICE_ACCOUNT_TOKEN }}
          AWS_ACCESS_KEY_ID: op://CI/AWS/access_key_id
          AWS_SECRET_ACCESS_KEY: op://CI/AWS/secret_access_key

      - run: terraform apply -auto-approve
```

## CLI Commands

### NEVER LAUNCH COMMANDS FOR Reading Secrets ###
### NEVER READ REAL SECRETS even if you have to create them: create with related cli commands to store in the vault but never read or hardcode directly the real key/token ###


### Injecting into Commands

```bash
# Single secret inline
DATABASE_URL=$(op read "op://Production/DB/url") rails db:migrate

# Multiple secrets via env file
op run --env-file=.op.env -- ./deploy.sh

# With account specification
op run --account my-team --env-file=.op.env -- terraform apply
```

### Managing Items

```bash
# List vaults
op vault list

# List items in vault
op item list --vault Infrastructure

# Get item details
op item get "AWS" --vault Infrastructure

# Create item
op item create \
  --category login \
  --vault Infrastructure \
  --title "New Service" \
  --field username=admin \
  --field password=secret123
```

## Project Setup

### Initial Configuration

```bash
# Sign in (creates session)
op signin

# Verify access
op vault list

# Create project env file
cat > .op.env << 'EOF'
# Infrastructure secrets
AWS_ACCESS_KEY_ID=op://Infrastructure/AWS/access_key_id
AWS_SECRET_ACCESS_KEY=op://Infrastructure/AWS/secret_access_key

# Application secrets
DATABASE_URL=op://Production/Database/url
REDIS_URL=op://Production/Redis/url
EOF

# Test secret loading
op run --env-file=.op.env -- env | grep -E '^(AWS|DATABASE|REDIS)'
```

### Placeholder Workflow

Create items with placeholder values upfront, populate with real credentials later:

```bash
# 1. Create item with placeholder values
op item create \
  --vault myproject \
  --category login \
  --title "production-rails" \
  --field master_key="PLACEHOLDER_UPDATE_BEFORE_DEPLOY"

# 2. Create .kamal/secrets referencing the item
cat > .kamal/secrets << 'EOF'
RAILS_MASTER_KEY=$(op read "op://myproject/production-rails/master_key")
EOF

# 3. Update deployment docs to match
# docs/DEPLOYMENT.md should reference same paths

# 4. Later: Update with real value
op item edit "production-rails" \
  --vault myproject \
  master_key="actual_secret_value_here"
```

**Benefits:**
- Infrastructure code can be written before credentials exist
- All secret paths documented in code/docs from the start
- Reduces "forgot to update the docs" friction during deployment
- Team members can see what secrets are needed without having access to values

**Documentation Sync:**
Keep `.kamal/secrets` (or equivalent) and deployment docs in sync:

```markdown
<!-- docs/DEPLOYMENT.md -->
## Required Secrets

| Secret | 1Password Path | Purpose |
|--------|----------------|---------|
| `RAILS_MASTER_KEY` | `op://myproject/production-rails/master_key` | Decrypt credentials |
| `DOCKERHUB_TOKEN` | `op://myproject/production-dockerhub/access_token` | Pull images |
```

### Vault Organization

**Single-Vault Approach (Simpler)**

Use one vault with naming conventions for environment separation:

```
Vault: myproject
Items:
  - production-rails
  - production-dockerhub
  - production-hetzner-s3
  - staging-rails
  - staging-dockerhub
  - development-rails
```

Benefits:
- Simpler permission management (one vault to configure)
- Item names are self-documenting with environment prefix
- Easier to see all project secrets at a glance

**Multi-Vault Approach (Team Scale)**

Separate vaults when you need different access controls:

| Vault | Purpose | Access |
|-------|---------|--------|
| `Infrastructure` | Cloud provider credentials | DevOps team |
| `Production` | Production app secrets | Deploy systems |
| `Staging` | Staging environment | Dev team |
| `Development` | Local dev secrets | Individual devs |
| `Shared` | Cross-team API keys | All teams |

**When to Use Which:**
- **Single vault**: Solo developer, small team, single project
- **Multi-vault**: Multiple teams, strict access control requirements, compliance needs

## Security Best Practices

### DO

- Use `.op.env` files for project-specific secret mapping
- Add all `.op.env` variants to `.gitignore`
- Use service accounts for CI/CD (not personal accounts)
- Scope vault access by team/environment
- Rotate secrets regularly via 1Password

### DON'T

- Never commit `.op.env` files
- Never use `op read` output in logs or echo statements
- Never store session tokens in scripts
- Avoid hardcoding vault/item names - use variables

### Audit Logging

```bash
# Check recent access events
op events-api

# Specific vault events
op audit-events list --vault Production
```

## Troubleshooting

### Session Expired

```bash
# Re-authenticate
op signin

# Check current session
op whoami
```

### Item Not Found

```bash
# Verify vault access
op vault list

# Search for item
op item list --vault Infrastructure | grep -i aws

# Check exact field names
op item get "AWS" --vault Infrastructure --format json | jq '.fields[].label'
```

### Permission Denied

```bash
# Check account permissions
op vault list

# Verify specific vault access
op vault get Infrastructure
```

## Multiple Accounts

For managing multiple 1Password accounts (personal + work), use `--account` flag or `OP_ACCOUNT` env var:

```bash
# Specify account per command
op vault list --account acme.1password.com

# Set default for shell session
export OP_ACCOUNT=acme.1password.com

# With op run
op run --account acme.1password.com --env-file=.op.env -- ./deploy.sh
```

**Key rule:** Always specify account in automation scripts - never rely on "last signed in".

See [resources/multiple-accounts.md](resources/multiple-accounts.md) for detailed patterns including cross-account workflows and Makefile integration.

## Multi-Environment Pattern

```bash
# .op.env.production
DATABASE_URL=op://Production/Database/url
REDIS_URL=op://Production/Redis/url

# .op.env.staging
DATABASE_URL=op://Staging/Database/url
REDIS_URL=op://Staging/Redis/url

# .op.env.development
DATABASE_URL=op://Development/Database/url
REDIS_URL=op://Development/Redis/url
```

```makefile
ENV ?= development
OP_ENV_FILE = .op.env.$(ENV)

deploy:
	op run --env-file=$(OP_ENV_FILE) -- kamal deploy

# Usage: make deploy ENV=production
```
