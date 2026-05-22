---
name: vercel-deploy
description: >-
  Deploy applications to Vercel using the bundled deploy.sh claimable-preview
  flow. Packages projects into tarballs, auto-detects frameworks from
  package.json, uploads to the deployment endpoint, and returns a Preview URL
  and Claim URL. Use when the user asks to deploy to Vercel, wants a preview
  URL, or says to push a project live.
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
metadata:
  version: "1.0.0"
  author: "platxa-skill-generator"
  tags:
    - automation
    - deployment
    - vercel
    - devops
    - frontend
  provenance:
    upstream_source: "vercel-deploy"
    upstream_sha: "c0e08fdaa8ed6929110c97d1b867d101fd70218f"
    regenerated_at: "2026-02-04T15:55:15Z"
    generator_version: "1.0.0"
    intent_confidence: 0.58
---

# Vercel Deploy

Deploy any project to Vercel instantly via the claimable-preview flow. No Vercel account or CLI authentication required.

## Overview

This skill automates Vercel deployments through a bundled `scripts/deploy.sh` script that uses Vercel's claimable deployment endpoint. The script packages the project, detects the framework, uploads it, and returns two URLs: a live Preview URL and a Claim URL to transfer ownership to a Vercel account.

**What it automates:**
- Project packaging into `.tar.gz` (excludes `node_modules`, `.git`, `.env*`)
- Framework detection from `package.json` dependencies (40+ frameworks)
- Upload to `codex-deploy-skills.vercel.sh/api/deploy`
- Preview URL and Claim URL retrieval

**Time saved:** ~5-10 minutes per deployment

## Triggers

### When to Run

This automation activates when the user:
- Asks to "deploy", "publish", "host", or "push live" to Vercel
- Wants a preview URL for their project
- Says to deploy a frontend, full-stack app, or static site to Vercel
- Mentions Vercel by name in a deployment context

### Manual Invocation

```
/vercel-deploy [path]
```

| Argument | Description |
|----------|-------------|
| `path` | Directory to deploy or a `.tgz` file (defaults to `.`) |

## Process

### Step 1: Validate Project

Before deploying, verify the project directory exists and contains deployable content:

```bash
ls package.json 2>/dev/null || ls *.html 2>/dev/null || echo "No deployable content found"
```

For projects with `package.json`, ensure dependencies can be resolved. For static HTML projects without `package.json`, the script handles them natively.

### Step 2: Run the Deploy Script

Execute the bundled deployment script:

```bash
bash scripts/deploy.sh [path-to-project]
```

The script performs these steps internally:
1. **Package**: Creates a staging directory, copies files (excluding `node_modules`, `.git`, `.env*`), and generates a `.tar.gz` archive
2. **Detect framework**: Parses `package.json` for known dependency signatures
3. **Upload**: POSTs the tarball to the deployment endpoint via `curl`
4. **Return URLs**: Extracts `previewUrl` and `claimUrl` from the JSON response

Pass a `.tgz` file directly to skip the packaging step:

```bash
bash scripts/deploy.sh /path/to/project.tgz
```

### Step 3: Handle Static HTML Projects

For projects without `package.json`:
- Framework is set to `null` (Vercel serves static files)
- If exactly one `.html` file exists and it is not named `index.html`, the script renames it to `index.html` so Vercel serves it at the root path (`/`)

### Step 4: Present Results

Always show both URLs to the user after a successful deployment:

```
Preview URL: https://skill-deploy-abc123.vercel.app
Claim URL:   https://vercel.com/claim-deployment?code=...

View your site at the Preview URL.
To transfer this deployment to your Vercel account, visit the Claim URL.
```

The script also outputs structured JSON to stdout for programmatic consumption:

```json
{
  "previewUrl": "https://skill-deploy-abc123.vercel.app",
  "claimUrl": "https://vercel.com/claim-deployment?code=...",
  "deploymentId": "dpl_...",
  "projectId": "prj_..."
}
```

## Framework Detection

The deploy script auto-detects frameworks by matching dependency names in `package.json`. Detection order matters -- more specific frameworks are checked first.

| Category | Frameworks | Vercel Identifier |
|----------|-----------|-------------------|
| React meta-frameworks | Next.js, Gatsby, Remix, React Router v7, Blitz | `nextjs`, `gatsby`, `remix`, `react-router`, `blitzjs` |
| Vue ecosystem | Nuxt, VitePress, VuePress, Gridsome | `nuxtjs`, `vitepress`, `vuepress`, `gridsome` |
| Svelte ecosystem | SvelteKit, Svelte, Sapper | `sveltekit-1`, `svelte`, `sapper` |
| Other SSR/SSG | Astro, SolidStart, Docusaurus, Eleventy, Hexo | `astro`, `solidstart-1`, `docusaurus-2`, `eleventy`, `hexo` |
| Component frameworks | Angular, Ember, Preact, Stencil, Dojo, Polymer | `angular`, `ember`, `preact`, `stencil`, `dojo`, `polymer` |
| Backend | NestJS, Hono, Fastify, Elysia, Express, h3, Nitro | `nestjs`, `hono`, `fastify`, `elysia`, `express`, `h3`, `nitro` |
| Build tools | Vite, Parcel | `vite`, `parcel` |
| Specialty | Hydrogen (Shopify), RedwoodJS, Sanity, Storybook, UmiJS | `hydrogen`, `redwoodjs`, `sanity`, `storybook`, `umijs` |

Static HTML projects (no `package.json`) use `null` as the framework value.

## Verification

### Success Indicators

- `deploy.sh` exits with code 0
- Output JSON contains a non-empty `previewUrl` field
- Preview URL is an HTTPS link matching `*.vercel.app`
- Claim URL is present for account transfer

### Failure Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| `Error: Input must be a directory or a .tgz file` | Invalid path argument | Verify the path exists and is a directory or `.tgz` |
| Network timeout or DNS error | Sandbox blocks outbound requests | Rerun with `sandbox_permissions=require_escalated` |
| `"error"` in JSON response | Server-side deployment failure | Check error message; common causes: oversized tarball, invalid project structure |
| Empty `previewUrl` in response | Malformed server response | Retry the deployment; check network connectivity |
| `curl` not found | Missing system dependency | Install curl (`apt install curl` or equivalent) |

### Escalated Network Access

The deployment requires outbound HTTPS to `codex-deploy-skills.vercel.sh`. When sandboxing blocks this:

```
The deploy needs escalated network access to reach Vercel's deployment endpoint.
Rerun with sandbox_permissions=require_escalated to proceed.
```

## Examples

### Example 1: Deploy Current Directory

```
User: Deploy this to Vercel

[Validates: package.json exists, detects Next.js]
[Runs: bash scripts/deploy.sh .]
→ Detected framework: nextjs
→ Deployment successful!

Preview URL: https://skill-deploy-a1b2c3.vercel.app
Claim URL:   https://vercel.com/claim-deployment?code=abc123

Your site is live at the Preview URL.
Visit the Claim URL to transfer it to your Vercel account.
```

### Example 2: Deploy a Subdirectory

```
User: Deploy the frontend folder to Vercel

[Runs: bash scripts/deploy.sh ./frontend]
→ Detected framework: vite
→ Deployment successful!

Preview URL: https://skill-deploy-d4e5f6.vercel.app
Claim URL:   https://vercel.com/claim-deployment?code=def456
```

### Example 3: Deploy Static HTML

```
User: Put this HTML page on Vercel

[Validates: no package.json, found page.html]
[Runs: bash scripts/deploy.sh .]
→ Renaming page.html to index.html...
→ Deployment successful!

Preview URL: https://skill-deploy-g7h8i9.vercel.app
```

### Example 4: Deploy Pre-built Tarball

```
User: Deploy this tarball I already have

[Runs: bash scripts/deploy.sh /tmp/my-project.tgz]
→ Using provided tarball...
→ Deployment successful!

Preview URL: https://skill-deploy-j0k1l2.vercel.app
```

## Safety

### Idempotency

Each deployment creates a new independent preview with its own URL. Running the skill multiple times produces multiple deployments -- previous previews remain accessible.

### Reversibility

Deployments are ephemeral previews. Claiming a deployment transfers it to a Vercel account where it can be deleted from the dashboard. Unclaimed previews expire automatically.

### Prerequisites

Before running, ensure:
- [ ] `curl` is installed and available on PATH
- [ ] `tar` is installed for project packaging
- [ ] Network access to `codex-deploy-skills.vercel.sh` is available
- [ ] Project contains deployable content (`package.json` or HTML files)

### Packaging Rules

The script excludes these paths from the deployment tarball:
- `node_modules/` -- rebuilt by Vercel during build
- `.git/` -- version history not needed for deploy
- `.env` and `.env.*` -- secrets must not be uploaded

## Bundled References

- [Vercel Project Configuration](references/vercel-config.md) -- vercel.json settings, build overrides, and environment variables
- [Troubleshooting Guide](references/troubleshooting.md) -- Common deployment failures and resolution steps
