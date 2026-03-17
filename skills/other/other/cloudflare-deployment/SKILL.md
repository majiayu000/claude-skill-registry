---
name: cloudflare-deployment
description: Deploy and manage Cloudflare Workers, Pages, KV, R2, and D1 using wrangler CLI or MCP server. Use when working with Cloudflare services, serverless functions, or edge deployments.
---

# Cloudflare Deployment Skill

## When to Activate

Activate this skill when:
- Setting up Cloudflare Workers or Pages
- Working with KV, R2, or D1 storage
- Deploying applications to Cloudflare
- Configuring wrangler.toml
- Managing Cloudflare resources

## Quick Commands

```bash
# Install wrangler
pnpm add -g wrangler

# Login
wrangler login

# Initialize new Worker
wrangler init my-worker

# Local development
wrangler dev

# Deploy to Cloudflare
wrangler deploy

# View logs
wrangler tail my-worker
```

## Service Overview

| Service | Purpose | Use Case |
|---------|---------|----------|
| **Workers** | Serverless functions | API endpoints, middleware |
| **Pages** | Static sites + functions | SvelteKit, Next.js |
| **KV** | Key-value storage | Caching, session data |
| **R2** | Object storage | Files, images, backups |
| **D1** | SQLite database | Structured data |

## Workers Setup

```bash
wrangler init my-worker --type javascript
cd my-worker
wrangler dev
wrangler deploy
```

### Basic Worker

```javascript
export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (url.pathname === '/api/hello') {
      return new Response(JSON.stringify({ message: 'Hello!' }), {
        headers: { 'Content-Type': 'application/json' }
      });
    }

    return new Response('Not found', { status: 404 });
  }
}
```

## KV Storage

```bash
# Create namespace
wrangler kv namespace create MY_KV

# Add to wrangler.toml
# kv_namespaces = [{ binding = "MY_KV", id = "abc123" }]
```

```javascript
// In Worker
export default {
  async fetch(request, env) {
    // Write
    await env.MY_KV.put("key", "value");

    // Read
    const value = await env.MY_KV.get("key");

    return new Response(value);
  }
}
```

## R2 Storage

```bash
wrangler r2 bucket create my-bucket
# Add: r2_buckets = [{ binding = "MY_BUCKET", bucket_name = "my-bucket" }]
```

```javascript
// In Worker
await env.MY_BUCKET.put("file.txt", "content");
const object = await env.MY_BUCKET.get("file.txt");
const text = await object.text();
```

## D1 Database

```bash
wrangler d1 create my-database
wrangler d1 execute my-database --command="CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)"
# Add: d1_databases = [{ binding = "DB", database_name = "my-database", database_id = "..." }]
```

```javascript
// In Worker
const { results } = await env.DB.prepare(
  "SELECT * FROM users WHERE id = ?"
).bind(1).all();

return Response.json(results);
```

## Pages Deployment

```bash
# Deploy static site
wrangler pages deploy ./build --project-name=my-site

# With SvelteKit
pnpm add -D @sveltejs/adapter-cloudflare
pnpm build
wrangler pages deploy .svelte-kit/cloudflare
```

## wrangler.toml Configuration

```toml
name = "my-worker"
main = "src/index.js"
compatibility_date = "2024-01-01"

# Automatic resource provisioning (v4.45.0+)
kv_namespaces = [{ binding = "MY_KV" }]
r2_buckets = [{ binding = "MY_BUCKET" }]
d1_databases = [{ binding = "DB" }]
```

## Development Modes

```bash
# Local (simulated resources)
wrangler dev

# Remote (real Cloudflare resources)
wrangler dev --remote
```

## Worker Secrets

```bash
# Set secret
wrangler secret put API_KEY --name my-worker

# Access in code
const apiKey = env.API_KEY;
```

## Best Practices

### DO ✅
- Use `wrangler dev` for local testing first
- Use environment-specific configs
- Monitor logs with `wrangler tail`
- Use automatic resource provisioning

### DON'T ❌
- Hardcode account IDs
- Skip local testing
- Commit wrangler.toml with production IDs
- Ignore rate limits

## Common Patterns

### KV + R2 Caching

```javascript
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const cacheKey = url.pathname;

    // Check KV cache
    let content = await env.MY_KV.get(cacheKey);
    if (content) return new Response(content);

    // Fetch from R2
    const object = await env.MY_BUCKET.get(cacheKey.slice(1));
    if (!object) return new Response("Not found", { status: 404 });

    content = await object.text();

    // Cache in KV
    await env.MY_KV.put(cacheKey, content, { expirationTtl: 3600 });

    return new Response(content);
  }
}
```

## Related Resources

See `AgentUsage/cloudflare_guide.md` for complete documentation including:
- MCP server configuration
- Advanced D1 patterns
- Production deployment strategies
- Troubleshooting guide
