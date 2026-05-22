---
name: netlify-deploy
description: >-
  Deploy web projects to Netlify using the Netlify CLI (npx netlify). Handles
  authentication verification, site linking, framework detection, preview and
  production deploys, and netlify.toml configuration. Use when the user asks to
  deploy, host, publish, or ship a site on Netlify.
allowed-tools:
  - Bash
  - Read
  - Write
  - AskUserQuestion
  - WebSearch
metadata:
  version: "1.0.0"
  author: "platxa-skill-generator"
  tags:
    - automation
    - deployment
    - netlify
    - devops
    - ci-cd
  provenance:
    upstream_source: "netlify-deploy"
    upstream_sha: "c0e08fdaa8ed6929110c97d1b867d101fd70218f"
    regenerated_at: "2026-02-04T20:00:00Z"
    generator_version: "1.0.0"
    intent_confidence: 0.76
---

# Netlify Deploy

Deploy web projects to Netlify with automatic framework detection, preview URLs, and production releases.

## Overview

Automate the full Netlify deployment lifecycle: verify CLI authentication, link the local project to a Netlify site, detect the framework and build settings, run a preview deploy for validation, then promote to production when confirmed.

**What it automates:**
- Authentication checks and recovery via `npx netlify status` / `npx netlify login`
- Site linking by Git remote or interactive `npx netlify init`
- Framework-aware build configuration (Next.js, Vite, Astro, SvelteKit, static HTML)
- Preview deploys with unique draft URLs and production deploys with `--prod`

**Time saved:** ~5-15 minutes per deployment cycle

## Triggers

### When to Run

This automation activates when the user:
- Asks to "deploy", "publish", "host", or "ship" to Netlify
- Wants a preview URL for a branch or PR
- Needs to set up a new Netlify site from a local project
- Asks to push changes to production on Netlify

### Manual Invocation

```
/netlify-deploy [options]
```

| Option | Description |
|--------|-------------|
| `--prod` | Deploy directly to production (skip preview) |
| `--dir=path` | Override publish directory |
| `--message="text"` | Attach deploy message for audit trail |

## Process

### Step 1: Verify Authentication

Check that the Netlify CLI has a valid session:

```bash
npx netlify status
```

**Authenticated** output includes the logged-in email and linked site name.
**Not authenticated** shows `Not logged in` or an auth error.

If not authenticated, prompt the user to log in:

```bash
npx netlify login
```

This opens a browser for OAuth. After completion, re-run `npx netlify status` to confirm. If browser auth is unavailable, the user can set `NETLIFY_AUTH_TOKEN` as an environment variable with a personal access token from the Netlify dashboard.

### Step 2: Check Site Link

From `npx netlify status` output, determine whether the project is linked to a Netlify site.

**If linked:** proceed to Step 3.

**If not linked:** attempt Git-based linking first:

```bash
npx netlify link --git-remote-url "$(git remote get-url origin)"
```

If that fails (no matching site), create a new site interactively:

```bash
npx netlify init
```

The init wizard walks through team selection, site name, build command, and publish directory.

### Step 3: Detect Build Settings

Read `package.json` to identify the framework and infer build configuration:

| Framework | Build Command | Publish Dir |
|-----------|---------------|-------------|
| Next.js | `npm run build` | `.next` |
| Vite (React/Vue) | `npm run build` | `dist` |
| Astro | `npm run build` | `dist` |
| SvelteKit | `npm run build` | `build` |
| Static HTML | (none) | `.` |

If `netlify.toml` exists, the CLI uses it automatically. If it does not exist and the framework is detected, create one:

```toml
[build]
  command = "npm run build"
  publish = "dist"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

Ensure dependencies are installed before building:

```bash
npm install   # or yarn install / pnpm install
```

### Step 4: Deploy

**Preview deploy** (default, safe for testing):

```bash
npx netlify deploy
```

Returns a unique draft URL like `https://507f1f77--my-app.netlify.app`.

**Production deploy** (after preview is verified or when `--prod` is requested):

```bash
npx netlify deploy --prod
```

Returns the live production URL.

Add a deploy message for the audit log:

```bash
npx netlify deploy --prod --message="v1.2.0 release - fix auth redirect"
```

### Step 5: Report Results

After deployment, report:
- **Draft URL** or **Production URL** (clickable)
- **Deploy ID** from CLI output
- **Dashboard link**: `npx netlify open` to view in Netlify dashboard
- Any build warnings or errors from the deploy log

## Verification

### Success Indicators

- `npx netlify deploy` exits with code 0
- Output contains `Website draft URL:` or `Website URL:` with a valid HTTPS link
- The URL is accessible (HTTP 200) when fetched

### Failure Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| `Not logged in` | Auth token expired or missing | Run `npx netlify login` or set `NETLIFY_AUTH_TOKEN` |
| `No site linked` | Project not connected to Netlify | Run `npx netlify link` or `npx netlify init` |
| `Build failed (exit code 1)` | Build command errored | Run build locally (`npm run build`), fix errors, retry |
| `Publish directory not found` | Build output missing | Verify publish dir in `netlify.toml` matches actual output |
| `Network timeout` | Sandbox blocking outbound traffic | Rerun with `sandbox_permissions=require_escalated` |

## Examples

### Example 1: First-Time Deploy (New Project)

```
User: Deploy this React app to Netlify

[Runs: npx netlify status]
→ Not logged in

[Runs: npx netlify login]
→ Browser opens, user authenticates

[Runs: npx netlify status]
→ Logged in as user@example.com, no site linked

[Runs: npx netlify init]
→ Site created: my-react-app.netlify.app

[Runs: npm install && npx netlify deploy --prod]
→ Website URL: https://my-react-app.netlify.app

"Deployed to production: https://my-react-app.netlify.app"
```

### Example 2: Preview Deploy on Existing Site

```
User: Push a preview of my changes

[Runs: npx netlify status]
→ Logged in, site: my-react-app

[Runs: npx netlify deploy]
→ Draft URL: https://6425ee--my-react-app.netlify.app

"Preview ready: https://6425ee--my-react-app.netlify.app
 Run `npx netlify deploy --prod` to promote to production."
```

### Example 3: Monorepo Subdirectory Deploy

```
User: Deploy the frontend package from packages/web

[Reads: packages/web/package.json → Vite detected]
[Writes: packages/web/netlify.toml with base = "packages/web"]
[Runs: cd packages/web && npm install && npx netlify deploy --prod]
→ Website URL: https://my-monorepo-web.netlify.app
```

## Safety

### Idempotency

Running `npx netlify deploy` multiple times is safe. Each deploy creates a new immutable snapshot with its own URL. Previous deploys remain accessible via their draft URLs.

### Reversibility

Production deploys can be rolled back from the Netlify dashboard (Deploys tab) by publishing a previous deploy. The CLI does not have a direct rollback command.

### Prerequisites

Before running, ensure:
- [ ] Node.js >= 16 is installed (`node --version`)
- [ ] The project has a `package.json` or static HTML files
- [ ] Git remote is configured if using Git-based site linking
- [ ] Network access is available (not blocked by sandbox)

## Bundled References

- [CLI Commands Reference](references/cli-commands.md) -- Full command reference for `npx netlify`
- [netlify.toml Configuration](references/netlify-toml.md) -- Build config, redirects, headers, and context overrides
