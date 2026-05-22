---
name: deploy-cloudflare
description: Deploy to Cloudflare edge platform. Use when deploying static sites to Pages, serverless functions to Workers, or configuring CDN/DNS. Covers Wrangler CLI.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Deploy to Cloudflare

## Why Cloudflare?

- Global edge network (300+ cities)
- Zero cold starts (Workers)
- Automatic HTTPS and DDoS protection
- Integrated CDN and DNS
- Generous free tier

## Quick Start

```bash
# Install Wrangler
npm install -g wrangler

# Login
wrangler login

# Deploy Pages
wrangler pages deploy ./dist

# Deploy Worker
wrangler deploy
```

## Cloudflare Pages

### Deploy Static Site
```bash
# One-time deploy
wrangler pages deploy ./dist --project-name=my-app

# Connect Git repo (auto-deploy)
wrangler pages project create my-app --production-branch=main
```

### Build Configuration
```toml
# wrangler.toml (Pages Functions)
name = "my-app"
compatibility_date = "2025-01-01"

[build]
command = "npm run build"
```

## Cloudflare Workers

### Worker Configuration
```toml
# wrangler.toml
name = "my-worker"
main = "src/index.ts"
compatibility_date = "2025-01-01"

[vars]
ENVIRONMENT = "production"

[[kv_namespaces]]
binding = "MY_KV"
id = "abc123"
```

### Basic Worker
```typescript
export default {
  async fetch(request, env, ctx) {
    return new Response('Hello from the edge!', {
      headers: { 'Content-Type': 'text/plain' }
    });
  }
};
```

## Environment & Secrets

```bash
# Set secret (encrypted)
wrangler secret put API_KEY

# Set variable (plain text)
wrangler pages secret put API_URL

# Bulk upload
echo "SECRET_KEY" | wrangler secret put SECRET_KEY
```

## DNS Management

```bash
# List DNS records
wrangler dns list example.com

# Add A record
wrangler dns create example.com --type A --name www --content 1.2.3.4

# Update record
wrangler dns update example.com --type A --name www --content 5.6.7.8
```

## Deployment Workflow

### 1. Initialize Project
```bash
wrangler init my-project
cd my-project
```

### 2. Develop Locally
```bash
wrangler dev
```

### 3. Deploy
```bash
# Production
wrangler deploy

# Preview
wrangler deploy --env staging
```

## Best Practices

1. **Use Environments**: Separate staging and production
2. **Versioning**: Rollback via dashboard if needed
3. **Edge Caching**: Leverage Cache API for performance
4. **Rate Limiting**: Protect Workers with rate limits
5. **Monitoring**: Enable Workers Analytics

## Common Commands

```bash
# View logs (tail)
wrangler tail

# List deployments
wrangler deployments list

# Rollback
wrangler rollback --message "Revert breaking change"

# KV operations
wrangler kv:key put --binding=MY_KV "key" "value"
wrangler kv:key get --binding=MY_KV "key"
```

## Anti-Patterns

- **Don't** store secrets in wrangler.toml (use `wrangler secret`)
- **Don't** deploy without testing locally (`wrangler dev`)
- **Don't** ignore compatibility_date (affects runtime behavior)
- **Don't** use Workers for long-running tasks (30s limit)
