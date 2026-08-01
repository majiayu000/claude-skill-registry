---
name: 1password-cli
description: Use this skill when working with the 1Password CLI (`op` command) for
  secrets management, retrieving API keys, injecting secrets into development environments,
  or any task involving 1Password vault op
---

---
name: 1password-cli
description: Use this skill when working with the 1Password CLI (`op` command) for secrets management, retrieving API keys, injecting secrets into development environments, or any task involving 1Password vault operations. Triggers on: "1password", "op command", "secrets management", "api keys from vault", "op run", "op read", "service account token".
---

# 1Password CLI Skill

Use this skill when working with the 1Password CLI (`op` command) for secrets management, retrieving API keys, or injecting secrets into development environments.

## Installation

```bash
# macOS
brew install 1password-cli

# Verify installation
op --version
```

## Authentication Methods

### 1. Desktop App Integration (Interactive - Recommended for Development)

Enable biometric authentication (Touch ID/Windows Hello) through the 1Password desktop app:

1. Open 1Password app > Settings > Developer
2. Enable "Integrate with 1Password CLI"
3. Run any `op` command - you'll be prompted to authenticate

```bash
# This will prompt for biometric auth
op vault list
```

### 2. Service Account Token (Non-Interactive - CI/CD & Automation)

For automated environments without user interaction:

```bash
# Set the service account token as environment variable
export OP_SERVICE_ACCOUNT_TOKEN="ops_..."

# Now commands work without prompts
op vault list
```

Create service accounts in 1Password.com > Developer Tools > Service Accounts.

### 3. Manual Sign In (Legacy)

```bash
# Sign in and create a session
eval $(op signin)

# Or for a specific account
eval $(op signin --account my-team.1password.com)
```

## Secret Reference Syntax

Secret references use the URI format: `op://vault/item/[section/]field`

```
op://vault-name/item-name/field-name           # Simple field
op://vault-name/item-name/section/field-name   # Field in a section
op://Private/GitHub/password                    # Example: GitHub password
op://dev/Stripe/publishable-key                # Example: Stripe key
```

### Get Secret References

```bash
# Get reference for a specific field
op item get "GitHub" --vault Private --fields password --format json | jq -r '.reference'

# Output: op://Private/GitHub/password
```

## Reading Secrets

### Read a Single Secret

```bash
# Using secret reference
op read "op://vault-name/item-name/field-name"

# Examples
op read "op://Private/API Keys/openai-key"
op read "op://dev/Database/password"
```

### Get Item Details

```bash
# Get full item as JSON
op item get "item-name" --vault "vault-name" --format json

# Get specific field
op item get "GitHub" --fields password

# Get multiple fields
op item get "Database" --fields username,password
```

### List Items

```bash
# List all vaults
op vault list

# List items in a vault
op item list --vault "Private"

# Search for items
op item list --tags api-key
```

## Injecting Secrets into Environment Variables

### Using `op run`

The most secure way to use secrets - they exist only during command execution:

```bash
# Set secret reference in environment
export DB_PASSWORD="op://app-prod/database/password"

# Run command with secrets injected
op run -- ./my-script.sh

# Secrets are automatically masked in output
op run -- printenv DB_PASSWORD  # Shows: <concealed by 1Password>

# Disable masking if needed
op run --no-masking -- printenv DB_PASSWORD
```

### Using .env Files

Create a `.env` file with secret references:

```bash
# .env file
DATABASE_URL="op://dev/postgres/connection-string"
API_KEY="op://dev/my-api/key"
SECRET_TOKEN="op://dev/app/secret-token"
```

Run with the env file:

```bash
op run --env-file=.env -- npm start
op run --env-file=.env -- python app.py
```

### Environment-Specific Secrets

Use variables to switch between environments:

```bash
# .env file with variable
DB_PASSWORD="op://$APP_ENV/database/password"

# Switch environments
APP_ENV=dev op run --env-file=.env -- ./start.sh
APP_ENV=prod op run --env-file=.env -- ./start.sh
```

## Common Use Cases

### Retrieve API Keys for Development

```bash
# Get a single API key
OPENAI_KEY=$(op read "op://Private/OpenAI/api-key")

# Use in a command
curl -H "Authorization: Bearer $(op read 'op://Private/OpenAI/api-key')" ...
```

### Populate Environment for Local Development

```bash
# Create .env.local with secret references
cat > .env.local << 'EOF'
SUPABASE_URL="op://dev/Supabase/url"
SUPABASE_KEY="op://dev/Supabase/service-role-key"
ANTHROPIC_API_KEY="op://dev/Anthropic/api-key"
EOF

# Start development server with secrets
op run --env-file=.env.local -- npm run dev
```

### Export Secrets to Shell Session

```bash
# Export secrets for current shell session
export GITHUB_TOKEN=$(op read "op://Private/GitHub/token")
export NPM_TOKEN=$(op read "op://Private/npm/token")
```

### Use in Scripts

```bash
#!/bin/bash
# deploy.sh - uses 1Password for secrets

# Ensure we have access
op whoami > /dev/null 2>&1 || eval $(op signin)

# Get deployment credentials
DEPLOY_KEY=$(op read "op://prod/deploy/ssh-key")
API_TOKEN=$(op read "op://prod/api/token")

# Use in deployment...
```

## Creating and Managing Items

### Create a New Item

```bash
# Create API key item
op item create \
  --category "API Credential" \
  --title "My API Key" \
  --vault "dev" \
  --fields "api-key=sk-abc123"

# Create login item
op item create \
  --category Login \
  --title "Service Account" \
  --vault Private \
  --fields "username=admin,password=secret123"
```

### Update an Item

```bash
# Update a field
op item edit "My API Key" --vault dev "api-key=sk-newkey456"
```

### Delete an Item

```bash
op item delete "Old API Key" --vault dev
```

## Security Best Practices

1. **Use Service Accounts for CI/CD**: Never use personal credentials in automated environments

2. **Limit Vault Access**: Service accounts should only access vaults they need

3. **Use `op run` Over Export**: Secrets only exist during command execution, not in shell history

4. **Avoid Logging Secrets**: `op run` masks secrets by default - keep it enabled

5. **Rotate Service Account Tokens**: Regularly rotate tokens used in CI/CD pipelines

6. **Use Secret References in Code**: Store references, not secrets, in configuration files

7. **Audit Access**: Review service account usage reports in 1Password.com

## Troubleshooting

### "You are not currently signed in"

```bash
# Check current session
op whoami

# Sign in again
eval $(op signin)

# Or set service account token
export OP_SERVICE_ACCOUNT_TOKEN="ops_..."
```

### "Item not found"

```bash
# List available vaults to verify access
op vault list

# Search for the item
op item list --vault "vault-name" | grep "item-name"
```

### Desktop App Integration Not Working

1. Ensure 1Password app is running and unlocked
2. Check Settings > Developer > "Integrate with 1Password CLI" is enabled
3. Restart terminal after enabling integration

## Quick Reference

| Command | Description |
|---------|-------------|
| `op vault list` | List all accessible vaults |
| `op item list --vault X` | List items in vault X |
| `op item get "Name"` | Get item details |
| `op read "op://..."` | Read a secret value |
| `op run -- cmd` | Run command with secrets |
| `op run --env-file=.env -- cmd` | Run with .env secrets |
| `op whoami` | Check current session |
| `op signin` | Sign in interactively |
