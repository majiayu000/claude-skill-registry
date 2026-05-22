---
name: adynato-cloudflare
description: Cloudflare Workers and Pages deployment for Adynato projects. Covers wrangler CLI, reading logs for debugging, KV/D1/R2 storage, environment variables, and common errors. Use when deploying to Cloudflare, debugging workers, or configuring edge functions.
---

# Cloudflare Skill

Use this skill when deploying Adynato projects to Cloudflare Workers or Pages.

## Wrangler CLI

### Installation

```bash
npm install -g wrangler

# Or use npx
npx wrangler <command>
```

### Authentication

```bash
# Interactive login (opens browser)
wrangler login

# Check auth status
wrangler whoami

# Use API token (CI/CD)
export CLOUDFLARE_API_TOKEN="your-token"
```

## Reading Logs for Debugging

### Tail Live Logs

```bash
# Stream logs from production
wrangler tail

# Stream logs from specific environment
wrangler tail --env staging

# Filter by status
wrangler tail --status error

# Filter by search term
wrangler tail --search "user-123"

# Filter by IP
wrangler tail --ip 192.168.1.1

# JSON output for parsing
wrangler tail --format json
```

### Log Output Format

```
GET https://example.com/api/users - Ok @ 1/17/2026, 10:30:00 AM
  (log) Processing request for user-123
  (error) Database connection failed
```

### Adding Console Logs

```typescript
// Workers log to wrangler tail
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    console.log('Request received:', request.url)
    console.log('Headers:', Object.fromEntries(request.headers))

    try {
      const result = await doSomething()
      console.log('Result:', JSON.stringify(result))
      return Response.json(result)
    } catch (error) {
      console.error('Error:', error.message, error.stack)
      return Response.json({ error: 'Internal error' }, { status: 500 })
    }
  }
}
```

### Debugging Tips

1. **Always log request context first**
   ```typescript
   console.log(`[${request.method}] ${new URL(request.url).pathname}`)
   ```

2. **Log before and after async operations**
   ```typescript
   console.log('Fetching from KV...')
   const value = await env.MY_KV.get(key)
   console.log('KV result:', value ? 'found' : 'not found')
   ```

3. **Use structured logging**
   ```typescript
   console.log(JSON.stringify({
     type: 'request',
     path: url.pathname,
     method: request.method,
     timestamp: Date.now()
   }))
   ```

## Deployment

### Deploy Worker

```bash
# Deploy to production
wrangler deploy

# Deploy to specific environment
wrangler deploy --env staging

# Dry run (see what would be deployed)
wrangler deploy --dry-run

# Deploy specific script
wrangler deploy src/worker.ts
```

### Deploy Pages

```bash
# Deploy to Pages
wrangler pages deploy ./dist

# Deploy with specific project
wrangler pages deploy ./dist --project-name=my-site

# Deploy to specific branch
wrangler pages deploy ./dist --branch=preview
```

## Configuration

### wrangler.toml

```toml
name = "my-worker"
main = "src/index.ts"
compatibility_date = "2026-01-17"

# Environment variables (non-secret)
[vars]
API_URL = "https://api.example.com"
NODE_ENV = "production"

# KV Namespaces
[[kv_namespaces]]
binding = "MY_KV"
id = "abc123"

# D1 Databases
[[d1_databases]]
binding = "DB"
database_name = "my-database"
database_id = "def456"

# R2 Buckets
[[r2_buckets]]
binding = "BUCKET"
bucket_name = "my-bucket"

# Durable Objects
[[durable_objects.bindings]]
name = "MY_DO"
class_name = "MyDurableObject"

# Staging environment
[env.staging]
name = "my-worker-staging"
vars = { API_URL = "https://staging-api.example.com" }

[[env.staging.kv_namespaces]]
binding = "MY_KV"
id = "staging-kv-id"
```

### Secrets

```bash
# Add secret (interactive)
wrangler secret put MY_SECRET

# Add secret from stdin
echo "secret-value" | wrangler secret put MY_SECRET

# Add to specific environment
wrangler secret put MY_SECRET --env staging

# List secrets
wrangler secret list

# Delete secret
wrangler secret delete MY_SECRET
```

## Common Errors

### "No account id found"

```
Error: No account id found, quitting...
```

**Fix:** Add account_id to wrangler.toml or login:

```bash
wrangler login
# or
wrangler whoami  # to verify auth
```

```toml
# wrangler.toml
account_id = "your-account-id"
```

### "Worker not found"

```
Error: worker not found
```

**Fix:** Check worker name matches wrangler.toml:

```bash
# List all workers
wrangler deployments list

# Check wrangler.toml name field
```

### "KV namespace not found"

```
Error: namespace not found
```

**Fix:** Create the namespace first:

```bash
# Create KV namespace
wrangler kv:namespace create MY_KV

# Use the returned id in wrangler.toml
```

### "Script too large"

```
Error: Script startup exceeded CPU time limit
```

**Fix:**
- Bundle size limit is 10MB (25MB on paid)
- Check for large dependencies
- Use dynamic imports for rarely-used code

```bash
# Check bundle size
wrangler deploy --dry-run --outdir=./dist
ls -la ./dist
```

### "Binding not found"

```
Error: Cannot find binding "MY_KV"
```

**Fix:** Ensure binding is in wrangler.toml and matches code:

```typescript
// Code expects env.MY_KV
interface Env {
  MY_KV: KVNamespace  // Must match wrangler.toml binding
}
```

## KV Storage

```bash
# Create namespace
wrangler kv:namespace create MY_KV

# List namespaces
wrangler kv:namespace list

# Put value
wrangler kv:key put --binding=MY_KV "my-key" "my-value"

# Get value
wrangler kv:key get --binding=MY_KV "my-key"

# List keys
wrangler kv:key list --binding=MY_KV

# Delete key
wrangler kv:key delete --binding=MY_KV "my-key"

# Bulk upload
wrangler kv:bulk put --binding=MY_KV data.json
```

## D1 Database

```bash
# Create database
wrangler d1 create my-database

# Execute SQL
wrangler d1 execute my-database --command="SELECT * FROM users"

# Execute SQL file
wrangler d1 execute my-database --file=./schema.sql

# Export database
wrangler d1 export my-database --output=backup.sql

# List databases
wrangler d1 list
```

## R2 Storage

```bash
# Create bucket
wrangler r2 bucket create my-bucket

# List buckets
wrangler r2 bucket list

# Upload file
wrangler r2 object put my-bucket/path/file.txt --file=./local-file.txt

# Download file
wrangler r2 object get my-bucket/path/file.txt

# Delete file
wrangler r2 object delete my-bucket/path/file.txt
```

## Local Development

```bash
# Start local dev server
wrangler dev

# Dev with specific port
wrangler dev --port 8787

# Dev with local mode (no network to Cloudflare)
wrangler dev --local

# Dev with specific environment
wrangler dev --env staging

# Dev with live reload
wrangler dev --live-reload
```

## CI/CD with GitHub Actions

```yaml
name: Deploy to Cloudflare

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install dependencies
        run: npm ci

      - name: Deploy Worker
        run: npx wrangler deploy
        env:
          CLOUDFLARE_API_TOKEN: ${{ secrets.CLOUDFLARE_API_TOKEN }}
```

### Required Secrets

| Secret | Description |
|--------|-------------|
| `CLOUDFLARE_API_TOKEN` | API token with Workers edit permission |
| `CLOUDFLARE_ACCOUNT_ID` | Optional, can be in wrangler.toml |

## Debugging Checklist

When a worker fails:

1. **Check live logs**
   ```bash
   wrangler tail --status error
   ```

2. **Check recent deployments**
   ```bash
   wrangler deployments list
   ```

3. **Rollback if needed**
   ```bash
   wrangler rollback
   ```

4. **Test locally**
   ```bash
   wrangler dev
   ```

5. **Check bindings**
   ```bash
   wrangler kv:namespace list
   wrangler d1 list
   wrangler r2 bucket list
   ```

6. **Verify secrets**
   ```bash
   wrangler secret list
   ```
