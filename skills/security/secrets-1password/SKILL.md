---
name: secrets-1password
description: 1Password Developer CLI skill for secure secrets management. This skill should be used when creating, reading, updating, or deleting secrets in 1Password vaults, injecting secrets into script execution, or setting up 1Password CLI authentication.
---

# 1Password Developer CLI Skill

This skill provides workflows and helper scripts for managing secrets through the 1Password Developer CLI (`op`).

## Quick Start Onboarding

### Step 1: Install 1Password CLI

**macOS (Homebrew):**
```bash
brew install --cask 1password-cli
```

**macOS (Direct Download):**
```bash
curl -sS https://downloads.1password.com/mac/op-arm64/pkg/op_darwin_arm64_v2.30.0.pkg -o op.pkg
sudo installer -pkg op.pkg -target /
rm op.pkg
```

**Linux:**
```bash
curl -sS https://downloads.1password.com/linux/op-arm64-v2.30.0.zip -o op.zip
unzip -d op op.zip
sudo mv op/op /usr/local/bin/
rm -rf op op.zip
```

**Verify installation:**
```bash
op --version
```

### Step 2: Authenticate

**Interactive Login (Personal/Team Account):**
```bash
op account add
op signin
```

**Service Account (Automation):**
```bash
export OP_SERVICE_ACCOUNT_TOKEN="your-service-account-token"
```

To create a service account:
1. Go to 1Password.com → Settings → Developer → Service Accounts
2. Create new service account with appropriate vault access
3. Save the token securely

**Verify authentication:**
```bash
op account list
```

### Step 3: Verify Setup

Run the check script to confirm everything is working:

```bash
python3 scripts/op_check.py
```

Expected output:
```
✅ 1Password CLI installed: v2.30.0
✅ Authenticated as: user@example.com
✅ Vaults accessible: 3
```

## Core Operations

### List Vaults and Items

```bash
# List all accessible vaults
python3 scripts/op_list.py --vaults

# List items in a vault
python3 scripts/op_list.py --items --vault "Development"

# List items with category filter
python3 scripts/op_list.py --items --vault "Development" --category login
```

### Create Secrets

```bash
# Create a password/credential
python3 scripts/op_create.py \
  --vault "Development" \
  --title "API Key - OpenAI" \
  --category password \
  --password "sk-abc123..."

# Create a login with username/password
python3 scripts/op_create.py \
  --vault "Development" \
  --title "GitHub Account" \
  --category login \
  --username "myuser" \
  --password "mypassword" \
  --url "https://github.com"

# Create with custom fields
python3 scripts/op_create.py \
  --vault "Development" \
  --title "Database Credentials" \
  --category password \
  --field "host=db.example.com" \
  --field "port=5432" \
  --field "database=production"
```

### Read Secrets

```bash
# Get full item as JSON
python3 scripts/op_read.py --vault "Development" --item "API Key - OpenAI"

# Get specific field value only
python3 scripts/op_read.py --vault "Development" --item "API Key - OpenAI" --field password

# Get item by ID
python3 scripts/op_read.py --id "abc123xyz"
```

### Update Secrets

```bash
# Update password field
python3 scripts/op_update.py \
  --vault "Development" \
  --item "API Key - OpenAI" \
  --password "sk-new-key..."

# Update custom field
python3 scripts/op_update.py \
  --vault "Development" \
  --item "Database Credentials" \
  --field "host=new-db.example.com"

# Add new field to existing item
python3 scripts/op_update.py \
  --vault "Development" \
  --item "Database Credentials" \
  --field "replica_host=replica.example.com"
```

### Delete Secrets

```bash
# Delete item (moves to trash)
python3 scripts/op_delete.py --vault "Development" --item "Old API Key"

# Delete permanently (requires --force)
python3 scripts/op_delete.py --vault "Development" --item "Old API Key" --force

# Delete by ID
python3 scripts/op_delete.py --id "abc123xyz"
```

### Run Commands with Injected Secrets

The most powerful feature: inject secrets into any command without exposing them in plaintext.

```bash
# Run command with secrets from .env template
python3 scripts/op_run.py --env-file .env.tpl -- npm start

# Run with inline secret reference
python3 scripts/op_run.py \
  --secret "API_KEY=op://Development/OpenAI/password" \
  -- curl -H "Authorization: Bearer \$API_KEY" https://api.example.com

# Multiple secrets
python3 scripts/op_run.py \
  --secret "DB_HOST=op://Development/Database/host" \
  --secret "DB_PASS=op://Development/Database/password" \
  -- python migrate.py
```

**.env.tpl template format:**
```
DATABASE_URL=op://Development/Database/url
API_KEY=op://Development/OpenAI/password
SECRET_KEY=op://Development/App/secret
```

## Secret Reference Syntax

1Password uses URI-style references to identify secrets:

```
op://vault-name/item-name/field-name
```

**Examples:**
```
op://Development/OpenAI API Key/password
op://Production/Database/username
op://Shared/AWS/access-key-id
op://Personal/GitHub Token/credential
```

**Field names for common categories:**
| Category | Common Fields |
|----------|---------------|
| Login | `username`, `password`, `url` |
| Password | `password` |
| API Credential | `credential`, `username` |
| Database | `username`, `password`, `hostname`, `port`, `database` |
| SSH Key | `private_key`, `public_key` |

## Security Best Practices

1. **Never log secrets** - Scripts output metadata only, never secret values directly
2. **Use service accounts** - For CI/CD and automation, create dedicated service accounts with minimal vault access
3. **Prefer `op run`** - Inject secrets at runtime rather than exporting to environment
4. **Rotate regularly** - Use 1Password's built-in rotation features for credentials
5. **Audit access** - Review service account usage in 1Password admin console

## Item Categories

| Category | Use Case |
|----------|----------|
| `login` | Website/service credentials with username, password, URL |
| `password` | Simple password or API key |
| `secure-note` | Text notes, configuration snippets |
| `credit-card` | Payment cards |
| `identity` | Personal information |
| `document` | File attachments |
| `database` | Database connection credentials |
| `api-credential` | API keys and tokens |
| `ssh-key` | SSH key pairs |

## Troubleshooting

### "not signed in"

```bash
# Re-authenticate
op signin

# Or check service account token
echo $OP_SERVICE_ACCOUNT_TOKEN
```

### "vault not found"

```bash
# List available vaults
op vault list

# Check vault name (case-sensitive)
op vault get "Vault Name"
```

### "item not found"

```bash
# Search for item
op item list --vault "Vault" | grep -i "search term"

# List all items in vault
op item list --vault "Vault"
```

### Permission denied

Service accounts need explicit vault access:
1. Go to 1Password.com → Settings → Developer → Service Accounts
2. Edit the service account
3. Add vault access with appropriate permissions (read/write)

## Script Reference

All scripts are in the `scripts/` directory and output JSON by default.

| Script | Purpose |
|--------|---------|
| `op_check.py` | Verify CLI installation and authentication |
| `op_list.py` | List vaults and items |
| `op_create.py` | Create new secrets |
| `op_read.py` | Read/retrieve secrets |
| `op_update.py` | Update existing secrets |
| `op_delete.py` | Delete items |
| `op_run.py` | Execute commands with injected secrets |

For detailed CLI command syntax, see `references/cli_reference.md`.
