---
name: cloudflare-pages
version: "1.0.0"
description: Cloudflare Pages - Full-stack JAMstack platform with global CDN, serverless functions, Git integration, and native bindings to Workers, KV, R2, D1, and Durable Objects
---

# Cloudflare Pages Skill

**Cloudflare Pages** is a JAMstack platform for deploying full-stack applications to Cloudflare's global network. It combines static site hosting with serverless Pages Functions, automatic Git deployments, and native integrations with the Cloudflare ecosystem (Workers, KV, R2, D1, Durable Objects).

**Key Value Proposition**: Deploy static sites and full-stack applications with zero configuration, automatic preview deployments, unlimited bandwidth, and seamless access to Cloudflare's edge computing and storage services.

## When to Use This Skill

- Deploying static sites or JAMstack applications
- Building full-stack apps with serverless functions
- Configuring Pages Functions with bindings (KV, R2, D1)
- Setting up Git-based CI/CD with preview deployments
- Configuring headers, redirects, and routing
- Troubleshooting build or deployment issues
- Migrating from other hosting platforms to Pages

## When NOT to Use This Skill

- For Cloudflare Workers alone (use workers skill)
- For general Cloudflare CDN/DNS configuration
- For non-web applications or APIs without UI
- For container-based deployments (Pages is serverless)

---

## Core Concepts

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    Cloudflare Pages                              │
│              Global Edge Network (300+ PoPs)                     │
└─────────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│  Static Assets │   │ Pages Functions│   │   Bindings    │
├───────────────┤    ├───────────────┤    ├───────────────┤
│ • HTML/CSS/JS │    │ • /functions/ │    │ • KV          │
│ • Images      │    │ • Middleware  │    │ • R2          │
│ • _headers    │    │ • Routing     │    │ • D1          │
│ • _redirects  │    │ • TypeScript  │    │ • DO          │
│ • _routes.json│    │ • Workers API │    │ • Queues      │
└───────────────┘    └───────────────┘    │ • AI          │
        │                     │            └───────────────┘
        └─────────────────────┼─────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│  Deployment   │    │   Domains     │    │   Builds      │
├───────────────┤    ├───────────────┤    ├───────────────┤
│ • Git (GH/GL) │    │ • Custom      │    │ • 20 min max  │
│ • Direct      │    │ • *.pages.dev │    │ • 500/mo free │
│ • Wrangler    │    │ • Preview URLs│    │ • Env vars    │
│ • API         │    │               │    │ • Presets     │
└───────────────┘    └───────────────┘    └───────────────┘
```

### Platform Limits

| Resource | Free | Pro | Business | Enterprise |
|----------|------|-----|----------|------------|
| Builds/month | 500 | 5,000 | 20,000 | Unlimited |
| Custom domains | 100 | 250 | 500 | 500 |
| Files per site | 20,000 | 20,000 | 20,000 | 20,000 |
| File size | 25 MB | 25 MB | 25 MB | 25 MB |
| Preview deployments | Unlimited | Unlimited | Unlimited | Unlimited |
| Build timeout | 20 min | 20 min | 20 min | 20 min |

### Configuration Limits

| Config | Limit |
|--------|-------|
| Header rules | 100 max |
| Static redirects | 2,000 max |
| Dynamic redirects | 100 max |
| Redirect line length | 1,000 chars |
| Header line length | 2,000 chars |
| Projects per account | 100 (soft) |

---

## Quick Start

### Deploy with Git Integration

```bash
# 1. Connect repository in Cloudflare Dashboard
# Workers & Pages > Create application > Connect to Git

# 2. Configure build settings
# - Production branch: main
# - Build command: npm run build
# - Build output: dist

# 3. Push to deploy
git push origin main
```

### Deploy with Wrangler CLI

```bash
# Install Wrangler
npm install -g wrangler

# Login to Cloudflare
wrangler login

# Create a new project
npx wrangler pages project create my-site

# Deploy to production
npx wrangler pages deploy ./dist

# Deploy preview
npx wrangler pages deploy ./dist --branch=staging
```

### Deploy via Dashboard

1. Go to **Workers & Pages** > **Create application**
2. Click **Get started** under Pages
3. Drag and drop your build folder or zip file
4. Enter project name and deploy

---

## Build Configuration

### Framework Presets

Cloudflare provides presets for 31+ frameworks:

| Framework | Build Command | Output Directory |
|-----------|---------------|------------------|
| **React (Vite)** | `npm run build` | `dist` |
| **Next.js** | `npx @cloudflare/next-on-pages@1` | `.vercel/output/static` |
| **Astro** | `npm run build` | `dist` |
| **SvelteKit** | `npm run build` | `.svelte-kit/cloudflare` |
| **Nuxt** | `npm run build` | `dist` |
| **Remix** | `npm run build` | `public` |
| **Vue (Vite)** | `npm run build` | `dist` |
| **Angular** | `npm run build` | `dist/<project>` |
| **Gatsby** | `gatsby build` | `public` |
| **Hugo** | `hugo` | `public` |
| **Docusaurus** | `npm run build` | `build` |
| **Eleventy** | `npx @11ty/eleventy` | `_site` |

### System Environment Variables

These are automatically injected during builds:

| Variable | Description | Example |
|----------|-------------|---------|
| `CF_PAGES` | Always `1` on Pages | `1` |
| `CF_PAGES_COMMIT_SHA` | Git commit hash | `a1b2c3d...` |
| `CF_PAGES_BRANCH` | Branch name | `main` |
| `CF_PAGES_URL` | Deployment URL | `https://abc.pages.dev` |
| `CI` | Always `true` | `true` |

### Custom Environment Variables

```bash
# Set via dashboard: Settings > Environment variables

# Or in wrangler.toml
[vars]
API_URL = "https://api.example.com"

# Secrets (encrypted)
# Set via: wrangler pages secret put SECRET_NAME
```

### Monorepo Configuration

```
my-monorepo/
├── apps/
│   └── web/          # Root directory: apps/web
│       ├── src/
│       └── package.json
└── packages/
```

Set **Root directory** to `apps/web` in build settings.

---

## Pages Functions

### Directory Structure

```
my-project/
├── functions/
│   ├── _middleware.js      # Global middleware
│   ├── api/
│   │   ├── _middleware.js  # API-specific middleware
│   │   ├── index.js        # GET /api
│   │   ├── users/
│   │   │   ├── index.js    # GET /api/users
│   │   │   └── [id].js     # GET /api/users/:id
│   │   └── [[catchall]].js # Catch-all
│   └── health.js           # GET /health
├── public/
│   └── index.html
└── package.json
```

### Basic Function

```typescript
// functions/api/hello.ts
export const onRequestGet: PagesFunction = async (context) => {
  return new Response(JSON.stringify({ message: "Hello!" }), {
    headers: { "Content-Type": "application/json" }
  });
};

// Handle multiple methods
export const onRequest: PagesFunction = async (context) => {
  const { request } = context;

  if (request.method === "POST") {
    const body = await request.json();
    return new Response(JSON.stringify(body));
  }

  return new Response("Method not allowed", { status: 405 });
};
```

### Dynamic Routes

```typescript
// functions/users/[id].ts
export const onRequestGet: PagesFunction = async (context) => {
  const { id } = context.params;  // string
  return new Response(`User: ${id}`);
};

// functions/files/[[path]].ts (catch-all)
export const onRequestGet: PagesFunction = async (context) => {
  const { path } = context.params;  // string[]
  return new Response(`Path: ${path.join("/")}`);
};
```

### Middleware

```typescript
// functions/_middleware.ts
export const onRequest: PagesFunction = async (context) => {
  // Before handler
  console.log(`${context.request.method} ${context.request.url}`);

  try {
    // Call next handler
    const response = await context.next();

    // After handler - modify response
    response.headers.set("X-Custom-Header", "value");
    return response;
  } catch (err) {
    return new Response("Server Error", { status: 500 });
  }
};

// Chain multiple middlewares
export const onRequest = [errorHandler, auth, logging];

async function errorHandler(context) {
  try {
    return await context.next();
  } catch (err) {
    return new Response(err.message, { status: 500 });
  }
}

async function auth(context) {
  const token = context.request.headers.get("Authorization");
  if (!token) {
    return new Response("Unauthorized", { status: 401 });
  }
  return context.next();
}
```

### TypeScript Support

```typescript
// functions/api/data.ts
interface Env {
  KV: KVNamespace;
  DB: D1Database;
  BUCKET: R2Bucket;
  API_KEY: string;
}

export const onRequestGet: PagesFunction<Env> = async (context) => {
  const { env, request, params, waitUntil, passThroughOnException } = context;

  // Access bindings
  const value = await env.KV.get("key");
  const result = await env.DB.prepare("SELECT * FROM users").all();

  return Response.json({ value, users: result.results });
};
```

---

## Bindings

### KV Namespace

```typescript
// functions/api/kv.ts
interface Env {
  MY_KV: KVNamespace;
}

export const onRequest: PagesFunction<Env> = async ({ env }) => {
  // Write
  await env.MY_KV.put("key", "value");
  await env.MY_KV.put("json", JSON.stringify({ foo: "bar" }));
  await env.MY_KV.put("expiring", "data", { expirationTtl: 3600 });

  // Read
  const value = await env.MY_KV.get("key");
  const json = await env.MY_KV.get("json", { type: "json" });

  // List
  const list = await env.MY_KV.list({ prefix: "user:" });

  // Delete
  await env.MY_KV.delete("key");

  return Response.json({ value, json });
};
```

```bash
# Local development
npx wrangler pages dev ./dist --kv=MY_KV
```

### R2 Bucket

```typescript
// functions/api/files.ts
interface Env {
  BUCKET: R2Bucket;
}

export const onRequest: PagesFunction<Env> = async ({ env, request }) => {
  const url = new URL(request.url);
  const key = url.pathname.slice(1);

  switch (request.method) {
    case "PUT":
      await env.BUCKET.put(key, request.body, {
        httpMetadata: { contentType: request.headers.get("content-type") }
      });
      return new Response("Uploaded");

    case "GET":
      const object = await env.BUCKET.get(key);
      if (!object) return new Response("Not found", { status: 404 });
      return new Response(object.body, {
        headers: { "Content-Type": object.httpMetadata?.contentType || "application/octet-stream" }
      });

    case "DELETE":
      await env.BUCKET.delete(key);
      return new Response("Deleted");
  }
};
```

```bash
# Local development
npx wrangler pages dev ./dist --r2=BUCKET
```

### D1 Database

```typescript
// functions/api/users.ts
interface Env {
  DB: D1Database;
}

export const onRequestGet: PagesFunction<Env> = async ({ env }) => {
  const { results } = await env.DB
    .prepare("SELECT * FROM users WHERE active = ?")
    .bind(1)
    .all();

  return Response.json(results);
};

export const onRequestPost: PagesFunction<Env> = async ({ env, request }) => {
  const { name, email } = await request.json();

  const result = await env.DB
    .prepare("INSERT INTO users (name, email) VALUES (?, ?)")
    .bind(name, email)
    .run();

  return Response.json({ id: result.meta.last_row_id });
};
```

```bash
# Local development
npx wrangler pages dev ./dist --d1=DB=<database-id>
```

### Durable Objects

```typescript
// functions/api/counter.ts
interface Env {
  COUNTER: DurableObjectNamespace;
}

export const onRequest: PagesFunction<Env> = async ({ env, request }) => {
  const id = env.COUNTER.idFromName("global");
  const stub = env.COUNTER.get(id);
  return stub.fetch(request);
};
```

```bash
# Local development (requires Worker with DO)
npx wrangler pages dev ./dist --do=COUNTER=CounterDO@counter-worker
```

### Service Bindings

```typescript
// functions/api/proxy.ts
interface Env {
  AUTH_SERVICE: Fetcher;
}

export const onRequest: PagesFunction<Env> = async ({ env, request }) => {
  // Call another Worker
  return env.AUTH_SERVICE.fetch(request);
};
```

### Queue Producer

```typescript
// functions/api/jobs.ts
interface Env {
  MY_QUEUE: Queue;
}

export const onRequestPost: PagesFunction<Env> = async ({ env, request }) => {
  const job = await request.json();

  await env.MY_QUEUE.send({
    type: "process",
    data: job
  });

  return Response.json({ queued: true });
};
```

### Workers AI

```typescript
// functions/api/ai.ts
interface Env {
  AI: Ai;
}

export const onRequestPost: PagesFunction<Env> = async ({ env, request }) => {
  const { prompt } = await request.json();

  const response = await env.AI.run("@cf/meta/llama-2-7b-chat-int8", {
    messages: [{ role: "user", content: prompt }]
  });

  return Response.json(response);
};
```

---

## Static Configuration

### Headers (_headers)

```
# Apply to all paths
/*
  X-Frame-Options: DENY
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin

# API CORS headers
/api/*
  Access-Control-Allow-Origin: *
  Access-Control-Allow-Methods: GET, POST, PUT, DELETE
  Access-Control-Allow-Headers: Content-Type

# Cache static assets
/assets/*
  Cache-Control: public, max-age=31536000, immutable

# Security headers for HTML
/*.html
  Content-Security-Policy: default-src 'self'
  X-XSS-Protection: 1; mode=block

# Remove header (prefix with !)
/public/*
  ! X-Robots-Tag
```

**Note**: Custom headers do NOT apply to Pages Functions responses.

### Redirects (_redirects)

```
# Simple redirect (302 default)
/home /

# Permanent redirect
/old-page /new-page 301

# External redirect
/twitter https://twitter.com/example

# Splat (wildcard)
/blog/* https://blog.example.com/:splat

# Placeholder
/users/:id /profiles/:id 301

# Proxy (200 status, relative URLs only)
/api/* /functions/api/:splat 200

# Force trailing slash
/about /about/ 301
```

**Limits**: 2,000 static + 100 dynamic redirects max.

### Routes (_routes.json)

```json
{
  "version": 1,
  "include": ["/api/*", "/auth/*"],
  "exclude": ["/api/health", "/static/*"]
}
```

- Controls which paths invoke Functions
- `exclude` takes precedence over `include`
- Paths not matching either are served as static assets
- Max 100 rules combined

---

## Deployment Methods

### Git Integration (Recommended)

**GitHub Setup**:
1. Workers & Pages > Create application > Connect to Git
2. Select GitHub and authorize
3. Choose repository
4. Configure build settings
5. Deploy

**GitLab Setup**:
- Requires Maintainer role or higher
- Grants access to all repositories on account

**Branch Configuration**:
- Production branch: `main` (configurable)
- Preview branches: All non-production (configurable)
- Custom rules: Include/exclude patterns

### Direct Upload (Wrangler)

```bash
# Create project
npx wrangler pages project create my-app

# List projects
npx wrangler pages project list

# Deploy production
npx wrangler pages deploy ./dist

# Deploy preview
npx wrangler pages deploy ./dist --branch=feature-x

# List deployments
npx wrangler pages deployment list --project-name=my-app
```

### API Deployment

```bash
# Create deployment via API
curl -X POST \
  "https://api.cloudflare.com/client/v4/accounts/{account_id}/pages/projects/{project_name}/deployments" \
  -H "Authorization: Bearer {api_token}" \
  -F "manifest=@manifest.json" \
  -F "file1=@dist/index.html"
```

---

## Local Development

### Wrangler Dev Server

```bash
# Basic development
npx wrangler pages dev ./dist

# With bindings
npx wrangler pages dev ./dist \
  --kv=MY_KV \
  --r2=BUCKET \
  --d1=DB=<database-id> \
  --port=8788

# With live reload (framework dev server)
npx wrangler pages dev -- npm run dev

# Proxy to another server
npx wrangler pages dev --proxy=3000
```

### wrangler.toml Configuration

```toml
name = "my-pages-project"
pages_build_output_dir = "./dist"

# Compatibility
compatibility_date = "2024-01-01"
compatibility_flags = ["nodejs_compat"]

# Environment variables
[vars]
API_URL = "https://api.example.com"

# KV binding
[[kv_namespaces]]
binding = "MY_KV"
id = "abc123"

# R2 binding
[[r2_buckets]]
binding = "BUCKET"
bucket_name = "my-bucket"

# D1 binding
[[d1_databases]]
binding = "DB"
database_name = "my-db"
database_id = "xyz789"

# Durable Objects
[[durable_objects.bindings]]
name = "COUNTER"
class_name = "Counter"
script_name = "counter-worker"

# Service binding
[[services]]
binding = "AUTH"
service = "auth-worker"
```

---

## Branch Build Controls

### Preview Deployments

```
Settings > Builds & deployments > Configure Preview deployments
```

Options:
- **All non-production branches**: Default, deploys everything
- **None**: Disables preview builds
- **Custom branches**: Selective deployment

### Custom Branch Rules

```
# Include patterns
feat/*      # Match feat/login, feat/dashboard
release-*   # Match release-1.0, release-2.0

# Exclude patterns
dependabot/*  # Skip dependency updates
wip/*         # Skip work-in-progress

# Order: excludes evaluated first, then includes
```

### Skip Builds

Add to commit message:
```
git commit -m "Update docs [CI SKIP]"
git commit -m "Minor fix [skip ci]"
```

---

## Rollbacks

### Via Dashboard

1. Go to project > Deployments
2. Find the deployment to rollback to
3. Click three dots > Rollback to this deployment

### Via Wrangler

```bash
# List deployments
npx wrangler pages deployment list --project-name=my-app

# Rollback (redeploy a previous deployment)
# Note: Direct rollback command not available;
# redeploy the specific commit or use dashboard
```

---

## Troubleshooting

### Build Failures

```
Error: Build command failed
```

**Solutions**:
1. Check build logs for specific error
2. Verify build command and output directory
3. Test locally: `npm run build`
4. Check Node.js version compatibility
5. Review environment variables

### Function 500 Errors

```
Error: Internal Server Error
```

**Solutions**:
1. Check function logs in dashboard
2. Verify bindings are configured
3. Test locally with `wrangler pages dev`
4. Check for unhandled promise rejections

### Static Asset 404

```
Error: Page not found
```

**Solutions**:
1. Verify build output directory is correct
2. Check `_routes.json` isn't excluding the path
3. Confirm file exists in build output
4. Review `_redirects` for conflicts

### Binding Not Found

```
Error: Cannot read property of undefined
```

**Solutions**:
1. Verify binding is configured in dashboard
2. Check binding name matches code
3. For local dev, pass binding flags to wrangler
4. Verify wrangler.toml configuration

### Headers/Redirects Not Working

**Possible causes**:
1. File not in correct location (must be in build output)
2. Syntax errors in file
3. For Functions responses, use code instead
4. Exceeded limit (100 headers, 2100 redirects)

---

## Best Practices

### Project Structure

```
my-app/
├── functions/           # Server-side code
│   ├── _middleware.ts   # Global middleware
│   └── api/             # API routes
├── public/              # Static assets (copied to dist)
│   ├── _headers         # Header rules
│   ├── _redirects       # Redirect rules
│   └── robots.txt
├── src/                 # Source code
├── dist/                # Build output (gitignored)
├── wrangler.toml        # Wrangler config
└── package.json
```

### Security Recommendations

1. Use environment variables for secrets
2. Implement CORS properly for APIs
3. Add security headers (CSP, X-Frame-Options)
4. Validate and sanitize user input
5. Use HTTPS-only custom domains
6. Review function permissions and bindings

### Performance Tips

1. Use `_routes.json` to skip Functions for static paths
2. Set appropriate Cache-Control headers
3. Optimize images before upload
4. Use code splitting for large apps
5. Leverage Cloudflare's global CDN

---

## Resources

### Official Documentation
- [Pages Documentation](https://developers.cloudflare.com/pages/)
- [Functions Guide](https://developers.cloudflare.com/pages/functions/)
- [Framework Guides](https://developers.cloudflare.com/pages/framework-guides/)
- [Platform Limits](https://developers.cloudflare.com/pages/platform/limits/)

### Tools
- [Wrangler CLI](https://developers.cloudflare.com/workers/wrangler/)
- [C3 (Create Cloudflare)](https://developers.cloudflare.com/pages/get-started/c3/)

### Related Services
- [Workers](https://developers.cloudflare.com/workers/)
- [KV](https://developers.cloudflare.com/kv/)
- [R2](https://developers.cloudflare.com/r2/)
- [D1](https://developers.cloudflare.com/d1/)
- [Durable Objects](https://developers.cloudflare.com/durable-objects/)

### Community
- [Discord](https://discord.cloudflare.com/)
- [Community Forum](https://community.cloudflare.com/)
- [@CloudflareDev](https://twitter.com/CloudflareDev)

---

## Version History

- **1.0.0** (2026-01-13): Initial skill release
  - Complete Pages platform documentation
  - Static site and full-stack deployment guides
  - Pages Functions with routing and middleware
  - All bindings (KV, R2, D1, DO, Queues, AI)
  - Build configuration and framework presets
  - Headers, redirects, and routes configuration
  - Git integration and direct upload methods
  - Local development with Wrangler
  - Branch build controls and rollbacks
  - Troubleshooting guide
