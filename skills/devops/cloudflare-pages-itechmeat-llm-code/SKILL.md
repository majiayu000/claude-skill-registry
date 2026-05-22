---
name: cloudflare-pages
description: "Deploy full-stack applications on Cloudflare Pages. Covers Git integration, Direct Upload, Wrangler CLI, build configuration, Pages Functions (file-based routing), bindings, headers/redirects, custom domains, environment variables. Keywords: Cloudflare Pages, Pages Functions, Git deployment, Direct Upload, Wrangler, pages.dev, _headers, _redirects, _routes.json, preview deployments."
---

# Cloudflare Pages

Full-stack application hosting with Git-based or Direct Upload deployments to Cloudflare's global network.

## Quick Navigation

- Deployment methods → `references/deployment.md`
- Build configuration → `references/build.md`
- Pages Functions → `references/functions.md`
- Bindings → `references/bindings.md`
- Headers & Redirects → `references/headers-redirects.md`
- Custom domains → `references/domains.md`
- Wrangler CLI → `references/wrangler.md`

## When to Use

- Deploying static sites or JAMstack applications
- Building full-stack apps with serverless functions
- Configuring Git-based CI/CD deployments
- Using Direct Upload for prebuilt assets
- Setting up preview deployments for branches/PRs
- Configuring custom domains and redirects

## Deployment Methods

| Method          | Best For                      | Limits                               |
| --------------- | ----------------------------- | ------------------------------------ |
| Git integration | CI/CD from GitHub/GitLab      | Cannot switch to Direct Upload later |
| Direct Upload   | Prebuilt assets, CI pipelines | Wrangler: 20k files, 25 MiB/file     |
| C3 CLI          | New project scaffolding       | Framework-dependent                  |

### Quick Deploy

```bash
# Create project
npx wrangler pages project create my-project

# Deploy
npx wrangler pages deploy ./dist

# Preview deployment (branch)
npx wrangler pages deploy ./dist --branch=feature-x
```

## Build Configuration

```bash
# Framework presets (command → output directory)
# React (Vite): npm run build → dist
# Next.js:      npx @cloudflare/next-on-pages@1 → .vercel/output/static
# Nuxt.js:      npm run build → dist
# Astro:        npm run build → dist
# SvelteKit:    npm run build → .svelte-kit/cloudflare
# Hugo:         hugo → public
```

### Environment Variables (build-time)

| Variable              | Value          |
| --------------------- | -------------- |
| `CF_PAGES`            | `1`            |
| `CF_PAGES_BRANCH`     | Branch name    |
| `CF_PAGES_COMMIT_SHA` | Commit SHA     |
| `CF_PAGES_URL`        | Deployment URL |

## Pages Functions

File-based routing in `/functions` directory:

```
/functions/index.js       → example.com/
/functions/api/users.js   → example.com/api/users
/functions/users/[id].js  → example.com/users/:id
```

```javascript
// functions/api/hello.js
export function onRequest(context) {
  return new Response("Hello from Pages Function!");
}
```

### Handler Types

| Export          | Trigger     |
| --------------- | ----------- |
| `onRequest`     | All methods |
| `onRequestGet`  | GET only    |
| `onRequestPost` | POST only   |

### Context Object

```typescript
interface EventContext {
  request: Request;
  env: Env; // Bindings
  params: Params; // Route parameters
  waitUntil(promise: Promise<any>): void;
  next(): Promise<Response>;
  data: Record<string, any>;
}
```

## Bindings

Access Cloudflare resources via `context.env`:

| Binding    | Access Pattern                           |
| ---------- | ---------------------------------------- |
| KV         | `context.env.MY_KV.get("key")`           |
| R2         | `context.env.MY_BUCKET.get("file")`      |
| D1         | `context.env.MY_DB.prepare("...").all()` |
| Workers AI | `context.env.AI.run(model, input)`       |

> For detailed binding configuration, see: `cloudflare-workers` skill.

## Headers & Redirects

Create `_headers` and `_redirects` in build output directory.

```txt
# _headers
/*
  X-Frame-Options: DENY
/static/*
  Cache-Control: public, max-age=31536000, immutable
```

```txt
# _redirects
/old-page /new-page 301
/blog/* https://blog.example.com/:splat
```

> **Warning:** `_headers` and `_redirects` do NOT apply to Pages Functions responses.

## Functions Invocation Routes

Control when Functions are invoked with `_routes.json`:

```json
{
  "version": 1,
  "include": ["/api/*"],
  "exclude": ["/static/*"]
}
```

## Wrangler Configuration

```jsonc
// wrangler.jsonc
{
  "name": "my-pages-app",
  "pages_build_output_dir": "./dist",
  "compatibility_date": "2024-01-01",
  "kv_namespaces": [{ "binding": "KV", "id": "<NAMESPACE_ID>" }],
  "d1_databases": [{ "binding": "DB", "database_name": "my-db", "database_id": "<ID>" }]
}
```

### Local Development

```bash
npx wrangler pages dev ./dist

# With bindings
npx wrangler pages dev ./dist --kv=MY_KV --d1=MY_DB=<ID>
```

## Critical Prohibitions

- Do NOT expect `_headers`/`_redirects` to apply to Pages Functions responses — attach headers in code
- Do NOT convert Direct Upload project to Git integration — not supported
- Do NOT exceed redirect limits — 2,000 static + 100 dynamic redirects max
- Do NOT use absolute URLs for proxying in `_redirects` — relative URLs only
- Do NOT edit bindings in dashboard when using Wrangler config — file is source of truth
- Do NOT store secrets in `wrangler.toml` — use dashboard or `.dev.vars` for local

## Common Gotchas

| Issue                  | Solution                                              |
| ---------------------- | ----------------------------------------------------- |
| Functions not invoked  | Check `_routes.json` include/exclude patterns         |
| Headers not applied    | Ensure not a Functions response; attach in code       |
| Build fails            | Check build command exit code (must be 0)             |
| Custom domain inactive | Verify DNS CNAME points to `<site>.pages.dev`         |
| Preview URLs indexed   | Default `X-Robots-Tag: noindex` applied automatically |

## Quick Recipes

### Conditional Build Command

```bash
#!/bin/bash
if [ "$CF_PAGES_BRANCH" == "production" ]; then
  npm run build:prod
else
  npm run build:dev
fi
```

### SPA Fallback (404.html)

Upload `404.html` in build output root for SPA routing.

### Disable Functions for Static Assets

```json
// _routes.json
{
  "version": 1,
  "include": ["/api/*"],
  "exclude": ["/*"]
}
```

## Related Skills

- `cloudflare-workers` — Worker runtime, bindings API details
- `cloudflare-d1` — D1 SQL database operations
- `cloudflare-r2` — R2 object storage
- `cloudflare-kv` — KV namespace operations
