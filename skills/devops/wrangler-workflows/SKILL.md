---
name: Wrangler Workflows
description: This skill should be used when the user mentions "wrangler", "wrangler.toml", "wrangler.jsonc", "wrangler commands", "local development", "wrangler dev", "wrangler deploy", "wrangler publish", "secrets management", "wrangler tail", "wrangler d1", "wrangler kv", or discusses Cloudflare Workers CLI, configuration files, or deployment workflows.
version: 0.1.0
---

# Wrangler Workflows

## Purpose

This skill provides comprehensive guidance for using Wrangler, the Cloudflare Workers CLI tool. It covers common commands, configuration file management, local development workflows, secrets handling, and deployment processes. Use this skill when working with Wrangler CLI operations, configuring Workers projects, or managing Workers deployments.

## Wrangler Overview

Wrangler is the official CLI tool for Cloudflare Workers. It handles:
- Project initialization and scaffolding
- Local development and testing
- Configuration management
- Deployment and publishing
- Resource management (KV, D1, R2, etc.)
- Secrets and environment variables
- Logs and debugging

### Installation

```bash
# Install globally via npm
npm install -g wrangler

# Or use npx (no install needed)
npx wrangler

# Verify installation
wrangler --version
```

### Authentication

```bash
# Login to Cloudflare account
wrangler login

# Or use API token
export CLOUDFLARE_API_TOKEN=your-token
wrangler whoami
```

## Common Commands

### Development Commands

**Start local development server:**
```bash
# Local mode (uses local resources when possible)
wrangler dev

# Remote mode (uses remote resources)
wrangler dev --remote

# Custom port
wrangler dev --port 3000

# With live reload
wrangler dev --live-reload
```

**Tail logs (real-time):**
```bash
# Production logs
wrangler tail

# With filters
wrangler tail --status error
wrangler tail --method POST
wrangler tail --search "user-id"

# Pretty print
wrangler tail --format pretty
```

### Deployment Commands

**Deploy to Cloudflare:**
```bash
# Deploy to production
wrangler deploy

# Deploy to specific environment
wrangler deploy --env staging
wrangler deploy --env production

# Dry run (validate without deploying)
wrangler deploy --dry-run

# Legacy command (same as deploy)
wrangler publish
```

**Manage deployments:**
```bash
# List deployments
wrangler deployments list

# View deployment details
wrangler deployments view [deployment-id]

# Rollback to previous deployment
wrangler rollback [deployment-id]
```

### Resource Management

**KV Commands:**
```bash
# Create KV namespace
wrangler kv:namespace create NAMESPACE_NAME

# List namespaces
wrangler kv:namespace list

# Put key-value
wrangler kv:key put KEY "value" --namespace-id=xxx

# Get value
wrangler kv:key get KEY --namespace-id=xxx

# Delete key
wrangler kv:key delete KEY --namespace-id=xxx

# List keys
wrangler kv:key list --namespace-id=xxx

# Bulk operations
wrangler kv:bulk put data.json --namespace-id=xxx
wrangler kv:bulk delete keys.json --namespace-id=xxx
```

**D1 Commands:**
```bash
# Create database
wrangler d1 create DATABASE_NAME

# List databases
wrangler d1 list

# Execute SQL
wrangler d1 execute DB_NAME --command="SELECT * FROM users"
wrangler d1 execute DB_NAME --file=query.sql

# Remote mode (production)
wrangler d1 execute DB_NAME --remote --command="SELECT * FROM users"

# Migrations
wrangler d1 migrations create DB_NAME migration_name
wrangler d1 migrations list DB_NAME
wrangler d1 migrations apply DB_NAME
wrangler d1 migrations apply DB_NAME --remote
```

**R2 Commands:**
```bash
# Create bucket
wrangler r2 bucket create BUCKET_NAME

# List buckets
wrangler r2 bucket list

# Upload object
wrangler r2 object put BUCKET_NAME/key.txt --file=local-file.txt

# Download object
wrangler r2 object get BUCKET_NAME/key.txt --file=output.txt

# Delete object
wrangler r2 object delete BUCKET_NAME/key.txt

# List objects
wrangler r2 object list BUCKET_NAME
```

### Secrets Management

```bash
# Add secret
wrangler secret put SECRET_NAME
# (prompts for value)

# List secrets
wrangler secret list

# Delete secret
wrangler secret delete SECRET_NAME

# Bulk secrets
wrangler secret bulk data.json
```

See `references/wrangler-commands-cheatsheet.md` for complete command reference.

## Configuration Files

Wrangler supports two configuration formats:
1. **wrangler.toml** - TOML format (traditional)
2. **wrangler.jsonc** - JSON with comments (modern, recommended)

### Basic wrangler.jsonc Structure

```jsonc
{
  "name": "my-worker",
  "main": "src/index.ts",
  "compatibility_date": "2024-01-01",

  // Environment variables
  "vars": {
    "ENVIRONMENT": "production"
  },

  // KV namespaces
  "kv_namespaces": [
    {
      "binding": "MY_KV",
      "id": "abc123..."
    }
  ],

  // D1 databases
  "d1_databases": [
    {
      "binding": "DB",
      "database_name": "my-db",
      "database_id": "xyz789..."
    }
  ],

  // R2 buckets
  "r2_buckets": [
    {
      "binding": "MY_BUCKET",
      "bucket_name": "uploads"
    }
  ],

  // Workers AI
  "ai": {
    "binding": "AI"
  }
}
```

### Multi-Environment Configuration

```jsonc
{
  "name": "my-worker",
  "main": "src/index.ts",
  "compatibility_date": "2024-01-01",

  // Default (production) configuration
  "vars": {
    "ENVIRONMENT": "production"
  },
  "kv_namespaces": [
    {
      "binding": "CACHE",
      "id": "prod-id"
    }
  ],

  // Environment-specific overrides
  "env": {
    "staging": {
      "vars": {
        "ENVIRONMENT": "staging"
      },
      "kv_namespaces": [
        {
          "binding": "CACHE",
          "id": "staging-id"
        }
      ]
    },
    "development": {
      "vars": {
        "ENVIRONMENT": "development"
      },
      "kv_namespaces": [
        {
          "binding": "CACHE",
          "id": "dev-id"
        }
      ]
    }
  }
}
```

Deploy to specific environment:
```bash
wrangler deploy --env staging
wrangler deploy --env development
```

See `references/wrangler-config-options.md` for all configuration options and `examples/wrangler-jsonc-template.jsonc` for annotated template.

## Local Development Workflow

### Step 1: Initialize Project

```bash
# Create new project
npm create cloudflare@latest

# Or initialize in existing directory
npm init cloudflare
```

### Step 2: Configure wrangler.jsonc

Create or update `wrangler.jsonc` with bindings, environment variables, and settings.

### Step 3: Develop Locally

```bash
# Start dev server
wrangler dev

# Worker accessible at http://localhost:8787
```

### Step 4: Test Locally

```bash
# Local KV (simulated)
wrangler dev

# Remote resources (real KV, D1, etc.)
wrangler dev --remote
```

### Step 5: Deploy

```bash
# Deploy to production
wrangler deploy
```

## Remote vs Local Mode

### Local Mode (Default)

- Bindings are simulated locally where possible
- KV, Cache API work with local storage
- D1 uses local SQLite
- Vectorize and Workflows require `--remote`

```bash
wrangler dev
```

### Remote Mode

- Uses actual Cloudflare resources
- All bindings work as in production
- May incur charges (AI, etc.)
- Required for Vectorize, Workflows, AI Gateway

```bash
wrangler dev --remote
```

**Important**: Some bindings like Vectorize don't support local mode and always require `--remote`.

## Secrets Best Practices

### Adding Secrets

```bash
# Interactive (secure, recommended)
wrangler secret put API_KEY

# From file (be careful)
wrangler secret put DB_PASSWORD < password.txt

# Bulk from JSON
cat secrets.json | wrangler secret bulk
```

### Secrets vs Environment Variables

| Feature | Secrets | Environment Variables |
|---------|---------|----------------------|
| **Storage** | Encrypted, not in config | Plain text in wrangler.jsonc |
| **Use case** | API keys, passwords | Non-sensitive config |
| **Deployment** | Set via CLI | Committed to git |
| **Access** | Same as env vars in code | Same as secrets in code |

**Rule**: Never commit secrets to version control. Use `wrangler secret put` for sensitive data.

## Debugging and Logs

### Real-Time Logs

```bash
# Tail production logs
wrangler tail

# Filter by status
wrangler tail --status error
wrangler tail --status ok

# Filter by method
wrangler tail --method POST

# Search logs
wrangler tail --search "user-123"

# Multiple filters
wrangler tail --status error --method POST
```

### Local Development Debugging

```bash
# Start with debugging
wrangler dev

# Console.log output visible in terminal
# Use Chrome DevTools for breakpoints
```

### Console Output

In Worker code:
```javascript
console.log('Info message', { data: 'value' });
console.error('Error:', error);
console.warn('Warning');
```

Visible in:
- `wrangler dev` terminal output
- `wrangler tail` for production
- Cloudflare Dashboard → Workers → Logs

## TypeScript Support

Wrangler automatically supports TypeScript:

```typescript
// src/index.ts
export interface Env {
  MY_KV: KVNamespace;
  DB: D1Database;
  API_KEY: string;
}

export default {
  async fetch(
    request: Request,
    env: Env,
    ctx: ExecutionContext
  ): Promise<Response> {
    const value = await env.MY_KV.get('key');
    return new Response(value);
  }
};
```

Install types:
```bash
npm install -D @cloudflare/workers-types
```

Update tsconfig.json:
```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ES2022",
    "lib": ["ES2022"],
    "types": ["@cloudflare/workers-types"]
  }
}
```

## Common Workflows

### New Project Setup

```bash
# 1. Create project
npm create cloudflare@latest my-worker

# 2. Navigate to project
cd my-worker

# 3. Install dependencies
npm install

# 4. Configure wrangler.jsonc
# (edit wrangler.jsonc)

# 5. Develop locally
wrangler dev

# 6. Deploy
wrangler deploy
```

### Adding D1 Database

```bash
# 1. Create database
wrangler d1 create my-database

# 2. Add to wrangler.jsonc
# "d1_databases": [{ "binding": "DB", "database_id": "..." }]

# 3. Create migrations
wrangler d1 migrations create my-database create_users_table

# 4. Write SQL in migrations/0001_create_users_table.sql

# 5. Apply migrations locally
wrangler d1 migrations apply my-database

# 6. Apply to production
wrangler d1 migrations apply my-database --remote
```

### Managing Multiple Environments

```bash
# Deploy to staging
wrangler deploy --env staging

# Tail staging logs
wrangler tail --env staging

# Execute on staging D1
wrangler d1 execute DB --env staging --remote --command="SELECT COUNT(*) FROM users"

# Deploy to production
wrangler deploy --env production
```

## Troubleshooting

### Common Issues

**Issue**: "Vectorize bindings not working in local dev"
- **Solution**: Use `wrangler dev --remote`, Vectorize doesn't support local mode

**Issue**: "Authentication failed"
- **Solution**: Run `wrangler login` or set `CLOUDFLARE_API_TOKEN`

**Issue**: "Binding not found in env"
- **Solution**: Check wrangler.jsonc configuration, ensure binding name matches

**Issue**: "D1 migrations not applying"
- **Solution**: Ensure you're using `--remote` flag for production: `wrangler d1 migrations apply DB --remote`

**Issue**: "Secrets not updating"
- **Solution**: Secrets require redeployment: `wrangler secret put KEY` then `wrangler deploy`

### Getting Help

```bash
# General help
wrangler --help

# Command-specific help
wrangler dev --help
wrangler deploy --help
wrangler d1 --help

# Version info
wrangler --version
```

## Best Practices

### Configuration Management

- Use `wrangler.jsonc` for modern projects (JSON with comments)
- Commit wrangler.jsonc to version control
- Never commit secrets to git
- Use environment-specific configurations for staging/production
- Keep compatibility_date current

### Development Workflow

- Always test with `wrangler dev` before deploying
- Use `--remote` when testing bindings that don't support local mode
- Run `wrangler deploy --dry-run` to validate before deploying
- Use `wrangler tail` to debug production issues
- Version control migrations (D1, Durable Objects)

### Deployment Strategy

- Use environments for staging/production separation
- Test migrations in staging before production
- Use `wrangler deployments list` to track deployment history
- Keep Workers small and focused
- Monitor logs with `wrangler tail` after deployment

### Security

- Always use `wrangler secret put` for sensitive data
- Rotate secrets regularly
- Use service bindings for internal-only Workers
- Validate all user input in Worker code
- Use HTTPS for external API calls

## Additional Resources

### Reference Files

For detailed information, consult:
- **`references/wrangler-commands-cheatsheet.md`** - Complete command reference with examples
- **`references/wrangler-config-options.md`** - All configuration options for wrangler.jsonc

### Example Files

Working examples in `examples/`:
- **`wrangler-jsonc-template.jsonc`** - Comprehensive annotated configuration template

### Documentation Links

For the latest Wrangler documentation:
- Wrangler commands: https://developers.cloudflare.com/workers/wrangler/commands/
- Configuration: https://developers.cloudflare.com/workers/wrangler/configuration/
- Migration guides: https://developers.cloudflare.com/workers/wrangler/migration/

Use the cloudflare-docs-specialist agent to search documentation and fetch the latest Wrangler information.
