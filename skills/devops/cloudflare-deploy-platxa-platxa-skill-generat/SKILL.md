---
name: cloudflare-deploy
description: >-
  Deploy applications to Cloudflare using Workers, Pages, D1, KV, R2, and
  related services via the Wrangler CLI. Handles authentication, project
  detection, wrangler.jsonc configuration, preview and production deploys, and
  binding setup. Use when the user asks to deploy, host, publish, or set up a
  project on Cloudflare.
allowed-tools:
  - Bash
  - Read
  - Write
  - Grep
  - Glob
  - WebSearch
metadata:
  version: "1.0.0"
  author: "platxa-skill-generator"
  tags:
    - automation
    - deployment
    - cloudflare
    - devops
    - serverless
    - edge-computing
  provenance:
    upstream_source: "cloudflare-deploy"
    upstream_sha: "c0e08fdaa8ed6929110c97d1b867d101fd70218f"
    regenerated_at: "2026-02-04T15:54:06Z"
    generator_version: "1.0.0"
    intent_confidence: 0.68
---

# Cloudflare Deploy

Deploy applications to Cloudflare with automatic project detection, Wrangler CLI orchestration, and production releases.

## Overview

Automate the full Cloudflare deployment lifecycle: verify Wrangler authentication, detect the project type (Worker, Pages site, full-stack app), configure bindings (D1, KV, R2, Durable Objects), run a preview deploy, then promote to production.

**What it automates:**
- Authentication checks via `npx wrangler whoami` and recovery with `wrangler login`
- Project type detection from `wrangler.jsonc`, `wrangler.toml`, or `package.json`
- Wrangler configuration generation for new projects
- Preview deploys with unique URLs and production deploys with `--env production`
- Binding setup for D1 databases, KV namespaces, R2 buckets, and Durable Objects

**Time saved:** ~10-20 minutes per deployment cycle

## Triggers

### When to Run

This automation activates when the user:
- Asks to "deploy", "publish", "host", or "ship" to Cloudflare
- Wants to set up a new Cloudflare Workers or Pages project
- Needs to configure bindings (D1, KV, R2) for a Worker
- Asks to push changes to production on Cloudflare
- Wants a preview URL for testing before production release

### Manual Invocation

```
/cloudflare-deploy [options]
```

| Option | Description |
|--------|-------------|
| `--pages` | Force Pages deployment instead of Worker |
| `--env=name` | Target a specific Wrangler environment |
| `--dry-run` | Preview what would be deployed without executing |

## Process

### Step 1: Verify Authentication

Check that Wrangler has a valid session:

```bash
npx wrangler whoami
```

**Authenticated** output shows the account name and ID.
**Not authenticated** shows an error or prompts for login.

If not authenticated, prompt the user to log in:

```bash
npx wrangler login
```

This opens a browser for OAuth. After completion, re-run `npx wrangler whoami` to confirm. For CI/CD or headless environments, the user should set `CLOUDFLARE_API_TOKEN` as an environment variable with an API token from the Cloudflare dashboard (My Profile > API Tokens).

### Step 2: Detect Project Type

Determine the deployment target by inspecting the project:

1. **Check for `wrangler.jsonc` or `wrangler.toml`**: If present, read to determine if the project is a Worker, Pages Function, or Durable Object.
2. **Check `package.json`**: Look for framework indicators to determine if this is a Pages site.
3. **Check directory structure**: Look for `functions/` (Pages Functions), `src/index.ts` (Worker), or static HTML.

| Indicator | Deploy Target | Command |
|-----------|---------------|---------|
| `wrangler.jsonc` with `main` field | Worker | `npx wrangler deploy` |
| `wrangler.jsonc` with `pages_build_output_dir` | Pages | `npx wrangler pages deploy` |
| Next.js / Vite / Astro in `package.json` | Pages | `npx wrangler pages deploy <dir>` |
| Static HTML only | Pages | `npx wrangler pages deploy .` |
| No config file, TypeScript entry | New Worker | Create `wrangler.jsonc` first |

### Step 3: Configure Wrangler

If no `wrangler.jsonc` exists, generate one based on the detected project type.

**For a Worker:**

```jsonc
{
  "name": "my-worker",
  "main": "src/index.ts",
  "compatibility_date": "2024-12-01",
  "compatibility_flags": ["nodejs_compat"]
}
```

**For a Pages project with functions:**

```jsonc
{
  "name": "my-pages-site",
  "pages_build_output_dir": "dist",
  "compatibility_date": "2024-12-01"
}
```

**Adding bindings** (append to `wrangler.jsonc` as needed):

```jsonc
{
  "d1_databases": [
    { "binding": "DB", "database_name": "my-db", "database_id": "<id>" }
  ],
  "kv_namespaces": [
    { "binding": "MY_KV", "id": "<id>" }
  ],
  "r2_buckets": [
    { "binding": "BUCKET", "bucket_name": "my-bucket" }
  ]
}
```

Create resources before deploying:

```bash
npx wrangler d1 create my-db          # Returns database_id
npx wrangler kv namespace create MY_KV # Returns namespace id
npx wrangler r2 bucket create my-bucket
```

### Step 4: Install Dependencies and Build

Ensure dependencies are installed and the project builds:

```bash
npm install
npm run build   # If build script exists in package.json
```

For Pages projects, verify the publish directory exists after build:

| Framework | Build Command | Output Dir |
|-----------|---------------|------------|
| Next.js (static) | `npm run build` | `out` |
| Vite | `npm run build` | `dist` |
| Astro | `npm run build` | `dist` |
| SvelteKit | `npm run build` | `build` |
| Static HTML | (none) | `.` |

### Step 5: Deploy

**Worker deployment:**

```bash
npx wrangler deploy
```

**Pages deployment (direct upload):**

```bash
npx wrangler pages deploy ./dist
```

**Pages deployment (first time, create project):**

```bash
npx wrangler pages project create my-site --production-branch main
npx wrangler pages deploy ./dist --project-name my-site
```

**Environment-specific deployment:**

```bash
npx wrangler deploy --env staging
npx wrangler deploy --env production
```

### Step 6: Report Results

After deployment, report:
- **Worker URL** or **Pages URL** (from CLI output)
- **Deployment ID** for audit trail
- **Bindings status**: confirm D1, KV, R2 bindings are active
- Any build warnings or deployment errors from Wrangler output

## Verification

### Success Indicators

- `npx wrangler deploy` or `npx wrangler pages deploy` exits with code 0
- Output contains the deployed URL (e.g., `https://my-worker.username.workers.dev`)
- Bindings are listed in the deployment output without errors

### Failure Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| `Not logged in` / `Authentication error` | Token expired or missing | Run `npx wrangler login` or set `CLOUDFLARE_API_TOKEN` |
| `Could not resolve main` | Missing entry point in `wrangler.jsonc` | Set `"main": "src/index.ts"` in config |
| `Build failed` | TypeScript or bundler errors | Run `npm run build` locally, fix errors, retry |
| `D1 database not found` | Database ID mismatch | Run `npx wrangler d1 list` and update `wrangler.jsonc` |
| `Script too large` | Worker exceeds 10MB compressed limit | Split into multiple Workers or use `--minify` |
| `Network timeout` | Sandbox blocking outbound traffic | Rerun with `sandbox_permissions=require_escalated` |
| `Compatibility date too old` | API changes require newer date | Update `compatibility_date` in `wrangler.jsonc` |

## Examples

### Example 1: Deploy a New Worker

```
User: Deploy this TypeScript worker to Cloudflare

[Runs: npx wrangler whoami]
-> Logged in as dev@acme.org, Account: My Account

[Reads: wrangler.jsonc not found]
[Reads: src/index.ts exists]
[Writes: wrangler.jsonc with name, main, compatibility_date]

[Runs: npm install && npx wrangler deploy]
-> Deployed to https://my-worker.username.workers.dev

"Deployed Worker: https://my-worker.username.workers.dev"
```

### Example 2: Deploy a Pages Site with D1

```
User: Deploy my Astro site with a D1 database to Cloudflare

[Runs: npx wrangler whoami]
-> Logged in

[Reads: package.json -> Astro detected]
[Runs: npx wrangler d1 create my-db]
-> Created database "my-db" with ID abc123

[Writes: wrangler.jsonc with pages_build_output_dir and d1 binding]
[Runs: npm install && npm run build]
[Runs: npx wrangler pages deploy ./dist --project-name my-astro-site]
-> Deployed to https://my-astro-site.pages.dev

"Deployed to Pages: https://my-astro-site.pages.dev
 D1 database 'my-db' bound as DB."
```

### Example 3: Deploy to Staging Environment

```
User: Push this worker to staging

[Reads: wrangler.jsonc has [env.staging] config]
[Runs: npx wrangler deploy --env staging]
-> Deployed to https://staging.my-worker.username.workers.dev

"Staging deploy: https://staging.my-worker.username.workers.dev
 Run `npx wrangler deploy --env production` to promote."
```

## Safety

### Idempotency

Running `npx wrangler deploy` multiple times is safe. Each deploy creates a new version. Cloudflare keeps the previous version for instant rollback.

### Reversibility

Roll back a Worker deployment:

```bash
npx wrangler rollback
```

Pages deployments can be rolled back from the Cloudflare dashboard (Workers & Pages > Deployments) by selecting a previous deployment.

### Prerequisites

Before running, ensure:
- [ ] Node.js >= 18 is installed (`node --version`)
- [ ] The project has a `package.json` or static files
- [ ] Network access is available (not blocked by sandbox)
- [ ] Wrangler is available (`npx wrangler --version`)

## Product Decision Tree

When the user needs to pick the right Cloudflare product:

```
Run code at edge?        -> Workers (npx wrangler deploy)
Full-stack web app?      -> Pages (npx wrangler pages deploy)
Key-value storage?       -> KV (wrangler kv namespace create)
SQL database?            -> D1 (wrangler d1 create)
File/object storage?     -> R2 (wrangler r2 bucket create)
Stateful coordination?   -> Durable Objects (configure in wrangler.jsonc)
AI inference?            -> Workers AI (bind ai in wrangler.jsonc)
Scheduled tasks?         -> Cron Triggers (configure in wrangler.jsonc)
```

## Bundled References

- [Wrangler CLI Reference](references/wrangler-cli.md) -- Full command reference for `npx wrangler`
- [Wrangler Configuration](references/wrangler-config.md) -- wrangler.jsonc settings, bindings, and environments
